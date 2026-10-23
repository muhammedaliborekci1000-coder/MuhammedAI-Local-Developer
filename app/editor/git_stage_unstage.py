"""
MuhammedAI Local Developer - Git Stage/Unstage
Git stage/unstage engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class StageMode(Enum):
    """Stage mode."""
    FILE = "file"
    DIRECTORY = "directory"
    PATTERN = "pattern"
    PATCH = "patch"
    ALL = "all"


class StageStatus(Enum):
    """Stage status."""
    STAGED = "staged"
    UNSTAGED = "unstaged"
    PARTIALLY_STAGED = "partially_staged"
    IGNORED = "ignored"


@dataclass
class StagedFile:
    """Staged file."""
    file_path: str
    status: StageStatus
    staged_lines: List[int] = field(default_factory=list)
    unstaged_lines: List[int] = field(default_factory=list)
    is_new: bool = False
    is_modified: bool = False
    is_deleted: bool = False


@dataclass
class StageConfig:
    """Stage configuration."""
    auto_stage: bool = False
    track_changes: bool = True
    show_status: bool = True
    confirm_before_stage: bool = False
    confirm_before_unstage: bool = False
    preserve_index: bool = True


@dataclass
class StageResult:
    """Stage result."""
    success: bool
    staged_files: List[str] = field(default_factory=list)
    unstaged_files: List[str] = field(default_factory=list)
    total_staged: int = 0
    total_unstaged: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class GitStageUnstageEngine:
    """
    Git stage/unstage engine.
    
    Özellikler:
    - Stage files
    - Unstage files
    - Stage all
    - Unstage all
    - Stage by pattern
    - Unstage by pattern
    - Get staged files
    - Get unstaged files
    - Stage status tracking
    - Partial staging
    - Patch staging
    - Interactive staging
    - Stage history
    - Stage validation
    - File status checking
    - Batch operations
    - Stage filtering
    """
    
    def __init__(self, config: Optional[StageConfig] = None):
        """Initialize git stage/unstage engine."""
        self.config = config or StageConfig()
        self.staged_files: Dict[str, StagedFile] = {}
        self.stage_history: List[Tuple[str, str]] = []  # (action, file_path)
    
    def stage_file(self, file_path: str, is_new: bool = False) -> StageResult:
        """
        Dosyayı stage et.
        
        Args:
            file_path: Dosya yolu
            is_new: Yeni dosya mı
            
        Returns:
            StageResult: Stage sonucu
        """
        result = StageResult(success=False)
        
        try:
            staged_file = StagedFile(
                file_path=file_path,
                status=StageStatus.STAGED,
                is_new=is_new,
                is_modified=not is_new
            )
            
            self.staged_files[file_path] = staged_file
            self.stage_history.append(("stage", file_path))
            
            result.success = True
            result.staged_files.append(file_path)
            result.total_staged = 1
            result.message = f"Staged: {file_path}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def unstage_file(self, file_path: str) -> StageResult:
        """
        Dosyayı unstage et.
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            StageResult: Unstage sonucu
        """
        result = StageResult(success=False)
        
        try:
            if file_path in self.staged_files:
                del self.staged_files[file_path]
                self.stage_history.append(("unstage", file_path))
                
                result.success = True
                result.unstaged_files.append(file_path)
                result.total_unstaged = 1
                result.message = f"Unstaged: {file_path}"
            else:
                result.errors.append(f"File not staged: {file_path}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def stage_all(self, file_paths: List[str]) -> StageResult:
        """
        Tüm dosyaları stage et.
        
        Args:
            file_paths: Dosya yolları
            
        Returns:
            StageResult: Stage sonucu
        """
        result = StageResult(success=False)
        
        try:
            staged_count = 0
            
            for file_path in file_paths:
                staged_file = StagedFile(
                    file_path=file_path,
                    status=StageStatus.STAGED,
                    is_modified=True
                )
                
                self.staged_files[file_path] = staged_file
                self.stage_history.append(("stage", file_path))
                staged_count += 1
            
            result.success = True
            result.staged_files = file_paths
            result.total_staged = staged_count
            result.message = f"Staged {staged_count} files"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def unstage_all(self) -> StageResult:
        """
        Tüm dosyaları unstage et.
        
        Returns:
            StageResult: Unstage sonucu
        """
        result = StageResult(success=False)
        
        try:
            unstaged_files = list(self.staged_files.keys())
            
            for file_path in unstaged_files:
                self.stage_history.append(("unstage", file_path))
            
            self.staged_files.clear()
            
            result.success = True
            result.unstaged_files = unstaged_files
            result.total_unstaged = len(unstaged_files)
            result.message = f"Unstaged {len(unstaged_files)} files"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def stage_by_pattern(self, pattern: str, file_paths: List[str]) -> StageResult:
        """
        Pattern'e göre stage et.
        
        Args:
            pattern: Pattern
            file_paths: Dosya yolları
            
        Returns:
            StageResult: Stage sonucu
        """
        result = StageResult(success=False)
        
        try:
            import fnmatch
            
            matched_files = [
                fp for fp in file_paths
                if fnmatch.fnmatch(fp, pattern)
            ]
            
            staged_count = 0
            for file_path in matched_files:
                staged_file = StagedFile(
                    file_path=file_path,
                    status=StageStatus.STAGED,
                    is_modified=True
                )
                
                self.staged_files[file_path] = staged_file
                self.stage_history.append(("stage", file_path))
                staged_count += 1
            
            result.success = True
            result.staged_files = matched_files
            result.total_staged = staged_count
            result.message = f"Staged {staged_count} files matching '{pattern}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def unstage_by_pattern(self, pattern: str) -> StageResult:
        """
        Pattern'e göre unstage et.
        
        Args:
            pattern: Pattern
            
        Returns:
            StageResult: Unstage sonucu
        """
        result = StageResult(success=False)
        
        try:
            import fnmatch
            
            matched_files = [
                fp for fp in self.staged_files.keys()
                if fnmatch.fnmatch(fp, pattern)
            ]
            
            for file_path in matched_files:
                del self.staged_files[file_path]
                self.stage_history.append(("unstage", file_path))
            
            result.success = True
            result.unstaged_files = matched_files
            result.total_unstaged = len(matched_files)
            result.message = f"Unstaged {len(matched_files)} files matching '{pattern}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_staged_files(self) -> List[StagedFile]:
        """
        Stage edilmiş dosyaları al.
        
        Returns:
            List[StagedFile]: Stage edilmiş dosyalar
        """
        return list(self.staged_files.values())
    
    def get_unstaged_files(self, all_files: List[str]) -> List[str]:
        """
        Stage edilmemiş dosyaları al.
        
        Args:
            all_files: Tüm dosyalar
            
        Returns:
            List[str]: Stage edilmemiş dosyalar
        """
        return [fp for fp in all_files if fp not in self.staged_files]
    
    def get_file_status(self, file_path: str) -> Optional[StageStatus]:
        """
        Dosya durumunu al.
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            Optional[StageStatus]: Dosya durumu
        """
        if file_path in self.staged_files:
            return self.staged_files[file_path].status
        return StageStatus.UNSTAGED
    
    def stage_partial(
        self,
        file_path: str,
        lines: List[int]
    ) -> StageResult:
        """
        Kısmi stage et.
        
        Args:
            file_path: Dosya yolu
            lines: Satır numaraları
            
        Returns:
            StageResult: Stage sonucu
        """
        result = StageResult(success=False)
        
        try:
            if file_path in self.staged_files:
                self.staged_files[file_path].staged_lines.extend(lines)
                self.staged_files[file_path].status = StageStatus.PARTIALLY_STAGED
            else:
                staged_file = StagedFile(
                    file_path=file_path,
                    status=StageStatus.PARTIALLY_STAGED,
                    staged_lines=lines,
                    is_modified=True
                )
                self.staged_files[file_path] = staged_file
            
            self.stage_history.append(("partial_stage", file_path))
            
            result.success = True
            result.staged_files.append(file_path)
            result.total_staged = 1
            result.message = f"Partially staged {len(lines)} lines in {file_path}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_stage_history(self) -> List[Tuple[str, str]]:
        """
        Stage geçmişini al.
        
        Returns:
            List[Tuple[str, str]]: Geçmiş
        """
        return self.stage_history
    
    def clear_history(self) -> StageResult:
        """
        Geçmişi temizle.
        
        Returns:
            StageResult: Temizleme sonucu
        """
        result = StageResult(success=False)
        
        try:
            self.stage_history.clear()
            result.success = True
            result.message = "Stage history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_staged_count(self) -> int:
        """
        Stage edilmiş dosya sayısını al.
        
        Returns:
            int: Sayı
        """
        return len(self.staged_files)
    
    def is_staged(self, file_path: str) -> bool:
        """
        Dosya staged mi kontrol et.
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            bool: Staged mi
        """
        return file_path in self.staged_files
    
    def update_config(self, config: StageConfig) -> StageResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            StageResult: Güncelleme sonucu
        """
        result = StageResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> StageConfig:
        """
        Konfigürasyon al.
        
        Returns:
            StageConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = GitStageUnstageEngine()
    
    # Dosyayı stage et
    result = engine.stage_file("test.py")
    print(f"Stage: {result.success}")
    
    # Tüm dosyaları stage et
    result = engine.stage_all(["test.py", "test2.py"])
    print(f"Stage all: {result.success}")
