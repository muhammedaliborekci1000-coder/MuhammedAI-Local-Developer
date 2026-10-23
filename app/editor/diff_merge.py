"""
MuhammedAI Local Developer - Diff Merge
Diff merge engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class MergeStrategy(Enum):
    """Merge strategy."""
    AUTO = "auto"
    MANUAL = "manual"
    THEIRS = "theirs"
    OURS = "ours"
    UNION = "union"
    INTERSECTION = "intersection"


class MergeStatus(Enum):
    """Merge status."""
    SUCCESS = "success"
    CONFLICT = "conflict"
    FAILED = "failed"
    PENDING = "pending"
    ABORTED = "aborted"
    SKIPPED = "skipped"


class ConflictResolution(Enum):
    """Conflict resolution."""
    ACCEPT_OURS = "accept_ours"
    ACCEPT_THEIRS = "accept_theirs"
    ACCEPT_BOTH = "accept_both"
    MANUAL_EDIT = "manual_edit"
    MARK_UNRESOLVED = "mark_unresolved"


class MergeAction(Enum):
    """Merge action."""
    MERGE = "merge"
    RESOLVE = "resolve"
    ABORT = "abort"
    CONTINUE = "continue"
    SKIP = "skip"
    PREVIEW = "preview"
    AUTO_MERGE = "auto_merge"


@dataclass
class ConflictInfo:
    """Conflict information."""
    line_number: int
    our_content: str
    their_content: str
    base_content: str
    file_path: str
    is_resolved: bool = False
    resolution: Optional[ConflictResolution] = None
    resolved_content: Optional[str] = None


@dataclass
class MergeResult:
    """Merge result."""
    success: bool
    action: Optional[str] = None
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    merged_content: Optional[str] = None
    conflicts: List[ConflictInfo] = field(default_factory=list)
    total_conflicts: int = 0
    resolved_conflicts: int = 0
    status: Optional[MergeStatus] = None


@dataclass
class MergeConfig:
    """Merge configuration."""
    strategy: MergeStrategy = MergeStrategy.AUTO
    auto_resolve: bool = False
    default_resolution: Optional[ConflictResolution] = None
    show_conflicts: bool = True
    show_base: bool = True
    show_ours: bool = True
    show_theirs: bool = True
    line_numbers: bool = True
    whitespace_ignored: bool = False
    case_sensitive: bool = True


class DiffMergeEngine:
    """
    Diff merge engine.
    
    Özellikler:
    - 3-way merge
    - Conflict resolution
    - Merge preview
    - Auto-merge
    - Multiple merge strategies
    - Conflict detection
    - Conflict tracking
    - Manual resolution
    - Automatic resolution
    - Base content comparison
    - Our content comparison
    - Their content comparison
    - Merge statistics
    - Merge history
    - Configuration management
    - Status tracking
    """
    
    def __init__(self, config: Optional[MergeConfig] = None):
        """Initialize diff merge engine."""
        self.config = config or MergeConfig()
        self.conflicts: List[ConflictInfo] = []
        self.merge_history: List[Tuple[str, str]] = []  # (action, target)
        self.current_status = MergeStatus.PENDING
    
    def merge(
        self,
        base_content: str,
        our_content: str,
        their_content: str,
        file_path: str = "file.txt"
    ) -> MergeResult:
        """
        3-way merge yap.
        
        Args:
            base_content: Base içerik
            our_content: Bizim içerik
            their_content: Onların içerik
            file_path: Dosya yolu
            
        Returns:
            MergeResult: Merge sonucu
        """
        result = MergeResult(success=False)
        result.action = MergeAction.MERGE.value
        
        try:
            self.conflicts.clear()
            
            # Basit 3-way merge algoritması
            base_lines = base_content.splitlines()
            our_lines = our_content.splitlines()
            their_lines = their_content.splitlines()
            
            # Çakışmaları tespit et
            max_lines = max(len(base_lines), len(our_lines), len(their_lines))
            
            for i in range(max_lines):
                base_line = base_lines[i] if i < len(base_lines) else ""
                our_line = our_lines[i] if i < len(our_lines) else ""
                their_line = their_lines[i] if i < len(their_lines) else ""
                
                # Çakışma kontrol�
                if our_line != their_line and (our_line != base_line or their_line != base_line):
                    conflict = ConflictInfo(
                        line_number=i + 1,
                        our_content=our_line,
                        their_content=their_line,
                        base_content=base_line,
                        file_path=file_path
                    )
                    self.conflicts.append(conflict)
            
            # Auto-merge
            if self.config.auto_resolve and self.conflicts:
                result = self.auto_merge(base_content, our_content, their_content, file_path)
            else:
                # Merge içeriğini oluştur
                if not self.conflicts:
                    merged_lines = our_lines if our_lines else their_lines
                    result.merged_content = "\n".join(merged_lines)
                    result.status = MergeStatus.SUCCESS
                    self.current_status = MergeStatus.SUCCESS
                else:
                    result.merged_content = our_content  # Default to ours
                    result.status = MergeStatus.CONFLICT
                    self.current_status = MergeStatus.CONFLICT
                
                result.conflicts = self.conflicts
                result.total_conflicts = len(self.conflicts)
                result.resolved_conflicts = 0
                result.success = True
                result.message = f"Merge completed with {len(self.conflicts)} conflicts"
            
            self.merge_history.append(("merge", file_path))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.status = MergeStatus.FAILED
        
        return result
    
    def resolve_conflict(
        self,
        line_number: int,
        resolution: ConflictResolution,
        custom_content: Optional[str] = None
    ) -> MergeResult:
        """
        Çakışmayı çöz.
        
        Args:
            line_number: Satır numarası
            resolution: Çözüm stratejisi
            custom_content: Özel içerik (manual_edit için)
            
        Returns:
            MergeResult: Çözüm sonucu
        """
        result = MergeResult(success=False)
        result.action = MergeAction.RESOLVE.value
        
        try:
            conflict = None
            for c in self.conflicts:
                if c.line_number == line_number:
                    conflict = c
                    break
            
            if not conflict:
                result.errors.append(f"Conflict not found at line {line_number}")
                return result
            
            # Çözüm uygula
            conflict.resolution = resolution
            conflict.is_resolved = True
            
            if resolution == ConflictResolution.ACCEPT_OURS:
                conflict.resolved_content = conflict.our_content
            elif resolution == ConflictResolution.ACCEPT_THEIRS:
                conflict.resolved_content = conflict.their_content
            elif resolution == ConflictResolution.ACCEPT_BOTH:
                conflict.resolved_content = f"{conflict.our_content}\n{conflict.their_content}"
            elif resolution == ConflictResolution.MANUAL_EDIT and custom_content:
                conflict.resolved_content = custom_content
            elif resolution == ConflictResolution.MARK_UNRESOLVED:
                conflict.is_resolved = False
                conflict.resolved_content = None
            
            result.conflicts = [conflict]
            result.resolved_conflicts = sum(1 for c in self.conflicts if c.is_resolved)
            result.total_conflicts = len(self.conflicts)
            result.success = True
            result.message = f"Resolved conflict at line {line_number}"
            
            self.merge_history.append(("resolve", str(line_number)))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def abort_merge(self) -> MergeResult:
        """
        Merge'i iptal et.
        
        Returns:
            MergeResult: İptal sonucu
        """
        result = MergeResult(success=False)
        result.action = MergeAction.ABORT.value
        
        try:
            self.conflicts.clear()
            self.current_status = MergeStatus.ABORTED
            result.status = MergeStatus.ABORTED
            result.success = True
            result.message = "Merge aborted"
            
            self.merge_history.append(("abort", "all"))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def continue_merge(self) -> MergeResult:
        """
        Merge'e devam et.
        
        Returns:
            MergeResult: Devam sonucu
        """
        result = MergeResult(success=False)
        result.action = MergeAction.CONTINUE.value
        
        try:
            unresolved = [c for c in self.conflicts if not c.is_resolved]
            
            if unresolved:
                result.errors.append(f"Cannot continue: {len(unresolved)} unresolved conflicts")
                return result
            
            self.current_status = MergeStatus.SUCCESS
            result.status = MergeStatus.SUCCESS
            result.success = True
            result.message = "Merge continued successfully"
            
            self.merge_history.append(("continue", "all"))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def skip_conflict(self, line_number: int) -> MergeResult:
        """
        Çakışmayı atla.
        
        Args:
            line_number: Satır numarası
            
        Returns:
            MergeResult: Atlama sonucu
        """
        result = MergeResult(success=False)
        result.action = MergeAction.SKIP.value
        
        try:
            conflict = None
            for c in self.conflicts:
                if c.line_number == line_number:
                    conflict = c
                    break
            
            if not conflict:
                result.errors.append(f"Conflict not found at line {line_number}")
                return result
            
            # Çakışmayı çözülmüş olarak işaretle (atlandı)
            conflict.resolution = ConflictResolution.MARK_UNRESOLVED
            conflict.is_resolved = True
            
            result.conflicts = [conflict]
            result.resolved_conflicts = sum(1 for c in self.conflicts if c.is_resolved)
            result.total_conflicts = len(self.conflicts)
            result.success = True
            result.message = f"Skipped conflict at line {line_number}"
            
            self.merge_history.append(("skip", str(line_number)))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def preview_merge(
        self,
        base_content: str,
        our_content: str,
        their_content: str
    ) -> MergeResult:
        """
        Merge önizlemesi yap.
        
        Args:
            base_content: Base içerik
            our_content: Bizim içerik
            their_content: Onların içerik
            
        Returns:
            MergeResult: Önizleme sonucu
        """
        result = MergeResult(success=False)
        result.action = MergeAction.PREVIEW.value
        
        try:
            # Önizleme için merge yap (gerçekten uygulamadan)
            preview_conflicts = []
            
            base_lines = base_content.splitlines()
            our_lines = our_content.splitlines()
            their_lines = their_content.splitlines()
            
            max_lines = max(len(base_lines), len(our_lines), len(their_lines))
            
            for i in range(max_lines):
                base_line = base_lines[i] if i < len(base_lines) else ""
                our_line = our_lines[i] if i < len(our_lines) else ""
                their_line = their_lines[i] if i < len(their_lines) else ""
                
                if our_line != their_line and (our_line != base_line or their_line != base_line):
                    conflict = ConflictInfo(
                        line_number=i + 1,
                        our_content=our_line,
                        their_content=their_line,
                        base_content=base_line,
                        file_path="preview"
                    )
                    preview_conflicts.append(conflict)
            
            result.conflicts = preview_conflicts
            result.total_conflicts = len(preview_conflicts)
            result.success = True
            result.message = f"Preview: {len(preview_conflicts)} potential conflicts"
            
            self.merge_history.append(("preview", "all"))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def auto_merge(
        self,
        base_content: str,
        our_content: str,
        their_content: str,
        file_path: str = "file.txt"
    ) -> MergeResult:
        """
        Otomatik merge yap.
        
        Args:
            base_content: Base içerik
            our_content: Bizim içerik
            their_content: Onların içerik
            file_path: Dosya yolu
            
        Returns:
            MergeResult: Auto-merge sonucu
        """
        result = MergeResult(success=False)
        result.action = MergeAction.AUTO_MERGE.value
        
        try:
            # Önce merge yap
            merge_result = self.merge(base_content, our_content, their_content, file_path)
            
            if not merge_result.success:
                return merge_result
            
            # Çakışmaları otomatik çöz
            for conflict in self.conflicts:
                if self.config.default_resolution:
                    resolution = self.config.default_resolution
                else:
                    # Varsayılan: our'u kabul et
                    resolution = ConflictResolution.ACCEPT_OURS
                
                resolve_result = self.resolve_conflict(
                    conflict.line_number,
                    resolution
                )
                
                if not resolve_result.success:
                    result.errors.extend(resolve_result.errors)
            
            # Merge içeriğini oluştur
            base_lines = base_content.splitlines()
            our_lines = our_content.splitlines()
            their_lines = their_content.splitlines()
            
            merged_lines = []
            max_lines = max(len(base_lines), len(our_lines), len(their_lines))
            
            for i in range(max_lines):
                conflict = None
                for c in self.conflicts:
                    if c.line_number == i + 1:
                        conflict = c
                        break
                
                if conflict and conflict.is_resolved and conflict.resolved_content:
                    merged_lines.append(conflict.resolved_content)
                elif i < len(our_lines):
                    merged_lines.append(our_lines[i])
                elif i < len(their_lines):
                    merged_lines.append(their_lines[i])
            
            result.merged_content = "\n".join(merged_lines)
            result.conflicts = self.conflicts
            result.total_conflicts = len(self.conflicts)
            result.resolved_conflicts = sum(1 for c in self.conflicts if c.is_resolved)
            result.status = MergeStatus.SUCCESS
            self.current_status = MergeStatus.SUCCESS
            result.success = True
            result.message = f"Auto-merge completed: {result.resolved_conflicts}/{result.total_conflicts} resolved"
            
            self.merge_history.append(("auto_merge", file_path))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.status = MergeStatus.FAILED
        
        return result
    
    def get_conflicts(self) -> List[ConflictInfo]:
        """
        Çakışmaları al.
        
        Returns:
            List[ConflictInfo]: Çakışma listesi
        """
        return self.conflicts
    
    def get_conflict(self, line_number: int) -> Optional[ConflictInfo]:
        """
        Çakışma al.
        
        Args:
            line_number: Satır numarası
            
        Returns:
            Optional[ConflictInfo]: Çakışma bilgisi
        """
        for conflict in self.conflicts:
            if conflict.line_number == line_number:
                return conflict
        return None
    
    def get_unresolved_conflicts(self) -> List[ConflictInfo]:
        """
        Çözülmemiş çakışmaları al.
        
        Returns:
            List[ConflictInfo]: Çakışma listesi
        """
        return [c for c in self.conflicts if not c.is_resolved]
    
    def get_resolved_conflicts(self) -> List[ConflictInfo]:
        """
        Çözülmüş çakışmaları al.
        
        Returns:
            List[ConflictInfo]: Çakışma listesi
        """
        return [c for c in self.conflicts if c.is_resolved]
    
    def get_merge_status(self) -> MergeStatus:
        """
        Merge durumunu al.
        
        Returns:
            MergeStatus: Durum
        """
        return self.current_status
    
    def get_merge_history(self) -> List[Tuple[str, str]]:
        """
        Merge geçmişini al.
        
        Returns:
            List[Tuple[str, str]]: Geçmiş
        """
        return self.merge_history
    
    def clear_history(self) -> MergeResult:
        """
        Geçmişi temizle.
        
        Returns:
            MergeResult: Temizleme sonucu
        """
        result = MergeResult(success=False)
        
        try:
            self.merge_history.clear()
            result.success = True
            result.message = "Merge history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        İstatistikleri al.
        
        Returns:
            Dict[str, Any]: İstatistikler
        """
        return {
            "total_conflicts": len(self.conflicts),
            "resolved_conflicts": sum(1 for c in self.conflicts if c.is_resolved),
            "unresolved_conflicts": sum(1 for c in self.conflicts if not c.is_resolved),
            "status": self.current_status.value
        }
    
    def update_config(self, config: MergeConfig) -> MergeResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            MergeResult: Güncelleme sonucu
        """
        result = MergeResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> MergeConfig:
        """
        Konfigürasyon al.
        
        Returns:
            MergeConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = DiffMergeEngine()
    
    base = "Line 1\nLine 2\nLine 3"
    ours = "Line 1\nLine 2 modified\nLine 3"
    theirs = "Line 1\nLine 2 changed\nLine 3"
    
    result = engine.merge(base, ours, theirs, "test.txt")
    print(f"Merge: {result.success}")
    print(f"Total conflicts: {result.total_conflicts}")
