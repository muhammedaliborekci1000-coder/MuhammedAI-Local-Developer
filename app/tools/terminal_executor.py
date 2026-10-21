"""
Terminal Executor
Terminal komutları için güvenli executor.
"""

import subprocess
import re
import sys
import time
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Callable

from app.core.config import PROJECT_ROOT
from app.tools.terminal_security import TerminalSecurityPolicy, RiskLevel


@dataclass
class TerminalCommand:
    """Terminal komutu."""
    command: str
    shell: str = "powershell"  # powershell, cmd, python
    working_directory: Optional[str] = None
    timeout: int = 30
    environment: Optional[dict] = None
    dry_run: bool = False
    reason: str = ""


@dataclass
class TerminalCommandResult:
    """Terminal komut sonucu."""
    command: str
    exit_code: Optional[int]
    stdout: str
    stderr: str
    duration: float
    timed_out: bool
    terminated: bool
    success: bool
    error: Optional[str]
    risk_level: RiskLevel
    approval_required: bool
    working_directory: Optional[str]


class TerminalExecutor:
    """
    Terminal komutları için güvenli executor.
    
    Özellikler:
    - Command validation
    - Risk classification
    - Workspace security
    - Timeout
    - Process termination
    - stdout/stderr capture
    - Exit code
    - Secret redaction
    - Dry-run
    """
    
    def __init__(
        self,
        project_root: Path = PROJECT_ROOT,
        security_policy: Optional[TerminalSecurityPolicy] = None
    ):
        """
        Args:
            project_root: Proje kök dizini
            security_policy: Security policy (opsiyonel)
        """
        self.project_root = Path(project_root)
        self.security_policy = security_policy or TerminalSecurityPolicy(project_root)
        
        # Maximum output limit
        self.max_output_chars = 10000
    
    def _redact_secrets(self, text: str) -> str:
        """
        Secret redaction.
        
        Args:
            text: Metin
            
        Returns:
            str: Redacted metin
        """
        if not text:
            return text
        
        # Secret patterns
        patterns = [
            r'api[_-]?key\s*[:=]\s*[\'"]?[\w\-]+[\'"]?',
            r'token\s*[:=]\s*[\'"]?[\w\-\.]+[\'"]?',
            r'password\s*[:=]\s*[\'"]?[\w]+[\'"]?',
            r'secret\s*[:=]\s*[\'"]?[\w\-]+[\'"]?',
            r'authorization\s*[:=]\s*[\'"]?bearer\s+[\w\-\.]+[\'"]?',
            r'private[_-]?key\s*[:=]\s*[\'"]?[\w\-]+[\'"]?',
        ]
        
        redacted = text
        for pattern in patterns:
            redacted = re.sub(pattern, '[REDACTED]', redacted, flags=re.IGNORECASE)
        
        return redacted
    
    def _truncate_output(self, text: str) -> str:
        """
        Output truncation.
        
        Args:
            text: Metin
            
        Returns:
            str: Truncated metin
        """
        if len(text) <= self.max_output_chars:
            return text
        
        return text[:self.max_output_chars] + "\n[OUTPUT TRUNCATED]"
    
    def _build_shell_command(self, cmd: TerminalCommand) -> list:
        """
        Shell command build et.
        
        Args:
            cmd: Terminal komutu
            
        Returns:
            list: Shell komutu
        """
        if cmd.shell == "python":
            return [sys.executable, "-c", cmd.command]
        elif cmd.shell == "powershell":
            return ["powershell", "-Command", cmd.command]
        elif cmd.shell == "cmd":
            return ["cmd", "/c", cmd.command]
        else:
            # Default: powershell
            return ["powershell", "-Command", cmd.command]
    
    def execute(
        self,
        cmd: TerminalCommand,
        approval_callback: Optional[Callable] = None
    ) -> TerminalCommandResult:
        """
        Terminal komutu çalıştır.
        
        Args:
            cmd: Terminal komutu
            approval_callback: Approval callback
            
        Returns:
            TerminalCommandResult: Komut sonucu
        """
        start_time = time.time()
        
        # Risk classification
        risk_level = self.security_policy.classify_risk(cmd.command)
        
        # Approval requirement
        approval_required = self.security_policy.requires_approval(cmd.command)
        
        # Validation
        valid, errors = self.security_policy.validate_command(
            cmd.command,
            cmd.working_directory
        )
        
        if not valid:
            return TerminalCommandResult(
                command=cmd.command,
                exit_code=None,
                stdout="",
                stderr="",
                duration=time.time() - start_time,
                timed_out=False,
                terminated=False,
                success=False,
                error="; ".join(errors),
                risk_level=risk_level,
                approval_required=approval_required,
                working_directory=cmd.working_directory
            )
        
        # Approval
        if approval_required:
            if approval_callback is None:
                return TerminalCommandResult(
                    command=cmd.command,
                    exit_code=None,
                    stdout="",
                    stderr="",
                    duration=time.time() - start_time,
                    timed_out=False,
                    terminated=False,
                    success=False,
                    error="Approval required but no callback provided",
                    risk_level=risk_level,
                    approval_required=approval_required,
                    working_directory=cmd.working_directory
                )
            approved = approval_callback(cmd)
            if not approved:
                return TerminalCommandResult(
                    command=cmd.command,
                    exit_code=None,
                    stdout="",
                    stderr="",
                    duration=time.time() - start_time,
                    timed_out=False,
                    terminated=False,
                    success=False,
                    error="Approval rejected",
                    risk_level=risk_level,
                    approval_required=approval_required,
                    working_directory=cmd.working_directory
                )
        
        # Dry-run
        if cmd.dry_run:
            return TerminalCommandResult(
                command=cmd.command,
                exit_code=None,
                stdout="[DRY-RUN: Command not executed]",
                stderr="[DRY-RUN: Command not executed]",
                duration=time.time() - start_time,
                timed_out=False,
                terminated=False,
                success=True,
                error=None,
                risk_level=risk_level,
                approval_required=approval_required,
                working_directory=cmd.working_directory
            )
        
        # Working directory
        cwd = str(self.project_root)
        if cmd.working_directory:
            if self.security_policy.validate_workspace(cmd.working_directory):
                cwd = str(Path(cmd.working_directory).resolve())
        
        # Build shell command
        shell_cmd = self._build_shell_command(cmd)
        
        try:
            # Execute
            result = subprocess.run(
                shell_cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=cmd.timeout,
                env=cmd.environment
            )
            
            stdout = self._redact_secrets(result.stdout)
            stdout = self._truncate_output(stdout)
            
            stderr = self._redact_secrets(result.stderr)
            stderr = self._truncate_output(stderr)
            
            return TerminalCommandResult(
                command=cmd.command,
                exit_code=result.returncode,
                stdout=stdout,
                stderr=stderr,
                duration=time.time() - start_time,
                timed_out=False,
                terminated=False,
                success=result.returncode == 0,
                error=None,
                risk_level=risk_level,
                approval_required=approval_required,
                working_directory=cmd.working_directory
            )
            
        except subprocess.TimeoutExpired:
            return TerminalCommandResult(
                command=cmd.command,
                exit_code=None,
                stdout="",
                stderr="",
                duration=time.time() - start_time,
                timed_out=True,
                terminated=True,
                success=False,
                error=f"Command timed out after {cmd.timeout}s",
                risk_level=risk_level,
                approval_required=approval_required,
                working_directory=cmd.working_directory
            )
            
        except Exception as exc:
            return TerminalCommandResult(
                command=cmd.command,
                exit_code=None,
                stdout="",
                stderr="",
                duration=time.time() - start_time,
                timed_out=False,
                terminated=False,
                success=False,
                error=f"Command execution failed: {exc}",
                risk_level=risk_level,
                approval_required=approval_required,
                working_directory=cmd.working_directory
            )
    
    def execute_simple(
        self,
        command: str,
        shell: str = "powershell",
        timeout: int = 30,
        dry_run: bool = False
    ) -> TerminalCommandResult:
        """
        Basit command execution.
        
        Args:
            command: Terminal komutu
            shell: Shell tipi
            timeout: Timeout
            dry_run: Dry-run
            
        Returns:
            TerminalCommandResult: Komut sonucu
        """
        cmd = TerminalCommand(
            command=command,
            shell=shell,
            timeout=timeout,
            dry_run=dry_run
        )
        
        return self.execute(cmd)
