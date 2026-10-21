"""
Terminal Security Policy
Terminal komutları için güvenlik politikası ve risk sınıflandırması.
"""

import re
from pathlib import Path
from enum import Enum
from typing import List, Tuple, Optional

from app.core.config import PROJECT_ROOT


class RiskLevel(Enum):
    """Risk seviyeleri."""
    SAFE = "SAFE"
    LOW_RISK = "LOW_RISK"
    MEDIUM_RISK = "MEDIUM_RISK"
    HIGH_RISK = "HIGH_RISK"
    BLOCKED = "BLOCKED"


class TerminalSecurityPolicy:
    """
    Terminal komutları için güvenlik politikası.
    
    Özellikler:
    - Risk sınıflandırması
    - Blocked commands
    - Protected paths
    - Command normalization
    - Workspace validation
    - Secret detection
    - Command chaining kontrolü
    - Redirection kontrolü
    """
    
    def __init__(self, project_root: Path = PROJECT_ROOT):
        """
        Args:
            project_root: Proje kök dizini
        """
        self.project_root = Path(project_root)
        
        # Blocked commands (tam match)
        self.blocked_commands = {
            "format",
            "diskpart",
            "shutdown",
            "reboot",
            "cipher",
        }
        
        # High risk commands (tam match)
        self.high_risk_commands = {
            "del",
            "erase",
            "rmdir",
            "rd",
            "remove-item",
            "rm",
            "pip uninstall",
            "git reset --hard",
            "git clean",
            "git checkout -- .",
            "git restore .",
        }
        
        # Medium risk commands
        self.medium_risk_commands = {
            "pip install",
            "pip upgrade",
            "git push",
            "git commit",
            "git branch -d",
            "git branch -D",
        }
        
        # Safe read-only commands (tam match)
        self.safe_commands = {
            "python --version",
            "python -v",
            "pytest --version",
            "git status",
            "git diff",
            "git log",
            "git branch",
            "git show",
            "dir",
            "ls",
            "pwd",
            "get-childitem",
            "get-location",
            "get-content",
            "type",
        }
        
        # PowerShell dangerous aliases
        self.dangerous_aliases = {
            "iex",
            "invoke-expression",
            "start-process",
        }
        
        # Protected paths
        self.protected_patterns = [
            ".env",
            ".env.",
            "*.pem",
            "*.key",
            "credentials.",
            "secrets.",
            "memory",
            "logs",
            ".git",
            ".ssh",
            "appdata",
            "windows",
            "system32",
        ]
        
        # Secret patterns
        self.secret_patterns = [
            r"api[_-]?key",
            r"token",
            r"password",
            r"secret",
            r"authorization",
            r"bearer",
            r"private[_-]?key",
        ]
    
    def normalize_command(self, command: str) -> str:
        """
        Command normalize et.
        
        Args:
            command: Terminal komutu
            
        Returns:
            str: Normalize edilmiş komut
        """
        # Lowercase
        normalized = command.lower().strip()
        
        # Multiple spaces → single space
        normalized = re.sub(r'\s+', ' ', normalized)
        
        return normalized
    
    def detect_chaining(self, command: str) -> bool:
        """
        Command chaining tespit et.
        
        Args:
            command: Terminal komutu
            
        Returns:
            bool: Chaining var mı
        """
        # && chaining
        if " && " in command or command.endswith(" &&"):
            return True
        
        # ; chaining
        if " ; " in command or command.endswith(" ;"):
            return True
        
        # & chaining (PowerShell)
        if " & " in command or command.endswith(" &"):
            return True
        
        # | pipe
        if " | " in command or command.startswith("| ") or command.endswith(" |"):
            return True
        
        return False
    
    def detect_redirection(self, command: str) -> bool:
        """
        Redirection tespit et.
        
        Args:
            command: Terminal komutu
            
        Returns:
            bool: Redirection var mı
        """
        # > redirection
        if " > " in command or command.endswith(" >"):
            return True
        
        # >> append
        if " >> " in command or command.endswith(" >>"):
            return True
        
        # < input
        if " < " in command or command.startswith("< "):
            return True
        
        # 2> stderr redirect
        if "2>" in command:
            return True
        
        return False
    
    def classify_risk(self, command: str) -> RiskLevel:
        """
        Command risk sınıflandırması.
        
        Args:
            command: Terminal komutu
            
        Returns:
            RiskLevel: Risk seviyesi
        """
        normalized = self.normalize_command(command)
        
        # Blocked commands
        for blocked in self.blocked_commands:
            if blocked in normalized:
                return RiskLevel.BLOCKED
        
        # PowerShell dangerous aliases
        for alias in self.dangerous_aliases:
            if alias in normalized:
                return RiskLevel.HIGH_RISK
        
        # High risk commands
        for high in self.high_risk_commands:
            if high in normalized:
                return RiskLevel.HIGH_RISK
        
        # Medium risk commands
        for medium in self.medium_risk_commands:
            if medium in normalized:
                return RiskLevel.MEDIUM_RISK
        
        # Safe commands (tam match)
        if normalized in self.safe_commands:
            return RiskLevel.SAFE
        
        # Chaining → high risk
        if self.detect_chaining(command):
            return RiskLevel.HIGH_RISK
        
        # Redirection to protected path → high risk
        if self.detect_redirection(command):
            if self._redirection_to_protected(command):
                return RiskLevel.HIGH_RISK
            return RiskLevel.MEDIUM_RISK
        
        # Default: low risk
        return RiskLevel.LOW_RISK
    
    def validate_workspace(self, working_dir: Optional[str] = None) -> bool:
        """
        Workspace validation.
        
        Args:
            working_dir: Working directory
            
        Returns:
            bool: Workspace içinde mi
        """
        if working_dir is None:
            return True
        
        try:
            requested = Path(working_dir).resolve()
            root = self.project_root.resolve()
            
            # Workspace içinde mi
            requested.relative_to(root)
            return True
            
        except ValueError:
            return False
    
    def is_protected_path(self, path: str) -> bool:
        """
        Protected path kontrolü.
        
        Args:
            path: Dosya yolu
            
        Returns:
            bool: Protected mı
        """
        path_lower = path.lower()
        
        for pattern in self.protected_patterns:
            if pattern.lower() in path_lower:
                return True
        
        return False
    
    def detect_secret(self, text: str) -> bool:
        """
        Secret detection.
        
        Args:
            text: Metin
            
        Returns:
            bool: Secret var mı
        """
        text_lower = text.lower()
        
        for pattern in self.secret_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    def _redirection_to_protected(self, command: str) -> bool:
        """
        Redirection protected path'e mi?
        
        Args:
            command: Terminal komutu
            
        Returns:
            bool: Protected path'e mi
        """
        # > veya >> sonrasını al
        match = re.search(r'[>]{1,2}\s*(.+)$', command)
        if match:
            target = match.group(1).strip()
            return self.is_protected_path(target)
        
        return False
    
    def validate_command(
        self,
        command: str,
        working_dir: Optional[str] = None
    ) -> Tuple[bool, List[str]]:
        """
        Command validation.
        
        Args:
            command: Terminal komutu
            working_dir: Working directory
            
        Returns:
            Tuple[bool, List[str]]: (valid, errors)
        """
        errors = []
        
        # Normalize
        normalized = self.normalize_command(command)
        
        # Risk classification
        risk = self.classify_risk(command)
        
        if risk == RiskLevel.BLOCKED:
            errors.append(f"Command blocked: {command}")
            return False, errors
        
        # Workspace validation
        if working_dir and not self.validate_workspace(working_dir):
            errors.append(f"Working directory outside workspace: {working_dir}")
            return False, errors
        
        # Chaining kontrolü
        if self.detect_chaining(command):
            errors.append("Command chaining not allowed")
            return False, errors
        
        # Redirection to protected
        if self.detect_redirection(command) and self._redirection_to_protected(command):
            errors.append("Redirection to protected path not allowed")
            return False, errors
        
        return True, errors
    
    def requires_approval(self, command: str) -> bool:
        """
        Approval gereksinimi.
        
        Args:
            command: Terminal komutu
            
        Returns:
            bool: Approval gerekli mi
        """
        risk = self.classify_risk(command)
        
        # HIGH_RISK ve MEDIUM_RISK approval gerektirir
        return risk in (RiskLevel.HIGH_RISK, RiskLevel.MEDIUM_RISK)
