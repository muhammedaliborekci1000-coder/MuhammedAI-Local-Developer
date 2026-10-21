"""
MuhammedAI Local Developer - Multi-File Editor
Vibe & Replace / Multi-File Intelligent Editing sistemi.
"""

import hashlib
import difflib
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum

from app.core.config import PROJECT_ROOT
from app.ai.codebase_index import CodebaseIndex
from app.ai.memory import MemorySystem, MemoryCategory, MemoryScope, MemorySource
from app.ai.project_rules import ProjectRules


class FileOperation(Enum):
    """Dosya operasyon türleri."""
    MODIFY = "modify"
    CREATE = "create"
    DELETE = "delete"


class RiskLevel(Enum):
    """Risk seviyeleri."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class FileChange:
    """Tek dosya değişikliği."""
    path: str
    operation: FileOperation
    original_content: str = ""
    proposed_content: str = ""
    diff: str = ""
    affected_symbols: List[str] = field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.MEDIUM
    reason: str = ""
    backup_path: str = ""


@dataclass
class MultiFileChangePlan:
    """Multi-file değişiklik planı."""
    plan_id: str
    request: str
    workspace: str
    files: Dict[str, FileChange] = field(default_factory=dict)
    diff: str = ""
    risk_level: RiskLevel = RiskLevel.MEDIUM
    affected_symbols: List[str] = field(default_factory=list)
    affected_dependencies: List[str] = field(default_factory=list)
    required_tests: List[str] = field(default_factory=list)
    approval_required: bool = True
    dry_run: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class MultiFileEditor:
    """
    Multi-file editing sistemi.
    
    Özellikler:
    - CodebaseIndex ile dosya keşfi
    - Dependency analizi
    - Diff generation
    - Validation
    - Approval
    - Backup
    - Atomic apply
    - Rollback
    - Dry-run
    """
    
    def __init__(
        self,
        project_root: Path = PROJECT_ROOT,
        codebase_index: Optional[CodebaseIndex] = None,
        memory_system: Optional[MemorySystem] = None,
        project_rules: Optional[ProjectRules] = None
    ):
        """
        Args:
            project_root: Proje kök dizini
            codebase_index: Codebase index (opsiyonel)
            memory_system: Memory system (opsiyonel)
            project_rules: Project rules (opsiyonel)
        """
        self.project_root = Path(project_root)
        self.codebase_index = codebase_index
        self.memory_system = memory_system
        self.project_rules = project_rules
        
        # Protected paths
        self.protected_patterns = [
            ".git",
            ".venv",
            "venv",
            "memory",
            "logs",
            ".env",
            "credentials",
            "private_key",
            "*.key",
            "*.pem",
            "secrets"
        ]
    
    def discover_files(
        self,
        query: str,
        max_files: int = 20
    ) -> List[str]:
        """
        CodebaseIndex kullanarak ilgili dosyaları keşfet.
        
        Args:
            query: Sorgu
            max_files: Maksimum dosya sayısı
            
        Returns:
            List[str]: İlgili dosya yolları
        """
        if not self.codebase_index:
            return []
        
        # Symbol search
        symbols = self.codebase_index.search_symbols(query)
        
        # Dosya yollarını topla
        file_paths = set()
        for symbol in symbols:
            if symbol.file:
                file_paths.add(symbol.file)
        
        # Dependency graph kullan
        for file_path in list(file_paths):
            deps = self.codebase_index.get_file_dependencies(file_path)
            file_paths.update(deps)
        
        # Reverse dependency
        for file_path in list(file_paths):
            dependents = self.codebase_index.get_dependents(file_path)
            file_paths.update(dependents)
        
        # Test dosyalarını bul
        for file_path in list(file_paths):
            related = self.codebase_index.find_related_files(file_path)
            for item in related:
                if "test" in item["file"].lower():
                    file_paths.add(item["file"])
        
        # Filter protected paths
        filtered = []
        for fp in file_paths:
            if self._is_protected_path(fp):
                continue
            filtered.append(fp)
        
        return filtered[:max_files]
    
    def create_plan(
        self,
        request: str,
        files: List[str],
        operations: Dict[str, FileOperation],
        dry_run: bool = False
    ) -> MultiFileChangePlan:
        """
        Multi-file değişiklik planı oluştur.
        
        Args:
            request: Kullanıcı isteği
            files: Dosya listesi
            operations: Dosya operasyonları
            dry_run: Dry-run modu
            
        Returns:
            MultiFileChangePlan: Değişiklik planı
        """
        plan_id = self._generate_plan_id(request)
        
        plan = MultiFileChangePlan(
            plan_id=plan_id,
            request=request,
            workspace=str(self.project_root),
            dry_run=dry_run
        )
        
        # Dosya değişikliklerini oluştur
        for file_path in files:
            if self._is_protected_path(file_path):
                continue
            
            operation = operations.get(file_path, FileOperation.MODIFY)
            
            file_change = FileChange(
                path=file_path,
                operation=operation,
                risk_level=self._assess_risk(file_path, operation)
            )
            
            # İçeriği oku
            full_path = self.project_root / file_path
            if full_path.exists():
                file_change.original_content = full_path.read_text(encoding='utf-8')
            
            plan.files[file_path] = file_change
        
        # Diff oluştur
        plan.diff = self._generate_unified_diff(plan)
        
        # Risk seviyesi hesapla
        plan.risk_level = self._calculate_overall_risk(plan)
        
        return plan
    
    def validate_plan(self, plan: MultiFileChangePlan) -> Dict[str, Any]:
        """
        Plan validasyonu.
        
        Args:
            plan: Değişiklik planı
            
        Returns:
            Dict: Validasyon sonucu
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # 1. Workspace boundary
        for file_path in plan.files.keys():
            if not self._is_within_workspace(file_path):
                result["valid"] = False
                result["errors"].append(f"Workspace dışı dosya: {file_path}")
        
        # 2. Protected paths
        for file_path in plan.files.keys():
            if self._is_protected_path(file_path):
                result["valid"] = False
                result["errors"].append(f"Korunan dosya: {file_path}")
        
        # 3. Duplicate paths
        paths = [fc.path for fc in plan.files.values()]
        if len(paths) != len(set(paths)):
            result["valid"] = False
            result["errors"].append("Duplicate dosya yolları")
            return result
        
        # 4. Empty changes
        for file_path, file_change in plan.files.items():
            if file_change.operation == FileOperation.MODIFY:
                if file_change.original_content == file_change.proposed_content:
                    result["valid"] = False
                    result["errors"].append(f"Boş değişiklik: {file_path}")
                    return result
        
        # 5. Rules compliance
        if self.project_rules:
            rules = self.project_rules.get_relevant_rules(task=plan.request)
            # Rule violation kontrolü (basit)
            for rule in rules:
                if "approval" in rule.content.lower() and not plan.approval_required:
                    result["valid"] = False
                    result["errors"].append(f"Rule ihlali: {rule.content}")
        
        return result
    
    def apply_plan(
        self,
        plan: MultiFileChangePlan,
        approval_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Planı uygula.
        
        Args:
            plan: Değişiklik planı
            approval_callback: Onay callback
            
        Returns:
            Dict: Uygulama sonucu
        """
        result = {
            "success": False,
            "applied_files": [],
            "failed_files": [],
            "backups": {},
            "rollback_performed": False,
            "error": None
        }
        
        # Validation
        validation = self.validate_plan(plan)
        if not validation["valid"]:
            result["error"] = "Plan invalid: " + "; ".join(validation["errors"])
            return result
        
        # Approval
        if plan.approval_required:
            if approval_callback is None:
                result["error"] = "Approval required but no callback provided"
                return result
            approved = approval_callback(plan)
            if not approved:
                result["error"] = "Approval rejected"
                return result
        
        # Dry-run
        if plan.dry_run:
            result["success"] = True
            result["dry_run"] = True
            return result
        
        # Backup tüm dosyalar
        backups = {}
        for file_path in plan.files.keys():
            try:
                from app.tools.backup_manager import BackupManager
                backup_mgr = BackupManager(project_root=self.project_root)
                backup_path = backup_mgr.create_backup(file_path)
                backups[file_path] = backup_path
            except Exception as e:
                result["error"] = f"Backup başarısız {file_path}: {e}"
                return result
        
        result["backups"] = backups
        
        # Apply
        applied = []
        failed = []
        
        for file_path, file_change in plan.files.items():
            try:
                full_path = self.project_root / file_path
                
                if file_change.operation == FileOperation.MODIFY:
                    full_path.write_text(file_change.proposed_content, encoding='utf-8')
                    applied.append(file_path)
                elif file_change.operation == FileOperation.CREATE:
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    full_path.write_text(file_change.proposed_content, encoding='utf-8')
                    applied.append(file_path)
                elif file_change.operation == FileOperation.DELETE:
                    full_path.unlink()
                    applied.append(file_path)
                    
            except Exception as e:
                failed.append(file_path)
                result["error"] = f"Apply başarısız {file_path}: {e}"
        
        result["applied_files"] = applied
        result["failed_files"] = failed
        
        # Partial failure rollback
        if failed:
            self._rollback_all(backups)
            result["rollback_performed"] = True
            result["success"] = False
        else:
            result["success"] = True
        
        return result
    
    def _generate_plan_id(self, request: str) -> str:
        """Plan ID oluştur."""
        hash_obj = hashlib.md5(request.encode())
        return f"plan_{hash_obj.hexdigest()[:12]}"
    
    def _is_within_workspace(self, file_path: str) -> bool:
        """Dosya workspace içinde mi?"""
        try:
            full_path = (self.project_root / file_path).resolve()
            full_path.relative_to(self.project_root.resolve())
            return True
        except ValueError:
            return False
    
    def _is_protected_path(self, file_path: str) -> bool:
        """Korunan dosya mı?"""
        file_path_lower = file_path.lower()
        for pattern in self.protected_patterns:
            if pattern.lower() in file_path_lower:
                return True
        return False
    
    def _assess_risk(self, file_path: str, operation: FileOperation) -> RiskLevel:
        """Risk seviyesi hesapla."""
        if operation == FileOperation.DELETE:
            return RiskLevel.HIGH
        
        if self._is_protected_path(file_path):
            return RiskLevel.CRITICAL
        
        if "config" in file_path.lower() or "security" in file_path.lower():
            return RiskLevel.HIGH
        
        return RiskLevel.MEDIUM
    
    def _calculate_overall_risk(self, plan: MultiFileChangePlan) -> RiskLevel:
        """Genel risk seviyesi."""
        if not plan.files:
            return RiskLevel.LOW
        
        max_risk = RiskLevel.LOW
        for file_change in plan.files.values():
            if file_change.risk_level.value > max_risk.value:
                max_risk = file_change.risk_level
        
        return max_risk
    
    def _generate_unified_diff(self, plan: MultiFileChangePlan) -> str:
        """Unified diff oluştur."""
        lines = []
        
        for file_path, file_change in plan.files.items():
            lines.append(f"=== {file_path} ===")
            
            if file_change.operation == FileOperation.MODIFY:
                diff = difflib.unified_diff(
                    file_change.original_content.splitlines(keepends=True),
                    file_change.proposed_content.splitlines(keepends=True),
                    fromfile=f"a/{file_path}",
                    tofile=f"b/{file_path}"
                )
                lines.extend(diff)
            elif file_change.operation == FileOperation.CREATE:
                lines.append(f"CREATE: {file_path}")
            elif file_change.operation == FileOperation.DELETE:
                lines.append(f"DELETE: {file_path}")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _rollback_all(self, backups: Dict[str, str]) -> None:
        """Tüm dosyaları rollback yap."""
        from app.tools.rollback_manager import RollbackManager
        rollback_mgr = RollbackManager(project_root=self.project_root)
        
        for file_path, backup_path in backups.items():
            try:
                rollback_mgr.rollback(file_path, backup_path)
            except Exception:
                pass
