"""
MuhammedAI Local Developer - File Close
File close engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class CloseMode(Enum):
    """Close mode."""
    CLOSE = "close"
    CLOSE_ALL = "close_all"
    CLOSE_OTHERS = "close_others"
    CLOSE_TO_RIGHT = "close_to_right"
    CLOSE_TO_LEFT = "close_to_left"


class SavePrompt(Enum):
    """Save prompt behavior."""
    ALWAYS = "always"
    NEVER = "never"
    PROMPT = "prompt"


@dataclass
class FileState:
    """File state."""
    path: str
    content: str
    modified: bool = False
    opened_at: str = ""
    last_modified_at: str = ""


@dataclass
class CloseConfig:
    """Close configuration."""
    mode: CloseMode = CloseMode.CLOSE
    save_prompt: SavePrompt = SavePrompt.PROMPT
    auto_save_before_close: bool = False
    keep_recent_files: bool = True
    max_recent_files: int = 20
    show_notification: bool = True


@dataclass
class CloseResult:
    """Close result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    closed_count: int = 0
    saved_count: int = 0
    closed_paths: List[str] = field(default_factory=list)


class FileCloseEngine:
    """
    File close engine.
    
    Özellikler:
    - Close files
    - Close all files
    - Close others
    - Close to right/left
    - Unsaved changes detection
    - Save prompt behavior
    - Auto-save before close
    - Recent files management
    - Reopen support
    - Close history
    - Undo support
    - Smart detection
    """
    
    def __init__(self, config: Optional[CloseConfig] = None):
        """Initialize file close engine."""
        self.config = config or CloseConfig()
        self.open_files: Dict[str, FileState] = {}
        self.close_history: List[Dict[str, Any]] = []
        self.recent_files: List[str] = []
    
    def open_file(self, path: str, content: str) -> None:
        """
        Dosya aç.
        
        Args:
            path: Dosya yolu
            content: İçerik
        """
        now = datetime.now().isoformat()
        self.open_files[path] = FileState(
            path=path,
            content=content,
            modified=False,
            opened_at=now,
            last_modified_at=now
        )
        
        # Add to recent files
        if path not in self.recent_files:
            self.recent_files.insert(0, path)
            if len(self.recent_files) > self.config.max_recent_files:
                self.recent_files.pop()
    
    def update_content(self, path: str, content: str) -> None:
        """
        İçeriği güncelle.
        
        Args:
            path: Dosya yolu
            content: Yeni içerik
        """
        if path in self.open_files:
            self.open_files[path].content = content
            self.open_files[path].modified = True
            self.open_files[path].last_modified_at = datetime.now().isoformat()
    
    def close_file(self, path: str, force: bool = False) -> CloseResult:
        """
        Dosya kapat.
        
        Args:
            path: Dosya yolu
            force: Zorla kapat
            
        Returns:
            CloseResult: Kapatma sonucu
        """
        result = CloseResult(success=False)
        
        try:
            if path not in self.open_files:
                result.errors.append(f"File not open: {path}")
                return result
            
            file_state = self.open_files[path]
            
            # Check for unsaved changes
            if file_state.modified and not force:
                if self.config.save_prompt == SavePrompt.PROMPT:
                    result.errors.append(f"File has unsaved changes: {path}")
                    return result
                elif self.config.save_prompt == SavePrompt.ALWAYS:
                    # Auto-save before close
                    if self.config.auto_save_before_close:
                        # In a real implementation, this would call the save engine
                        pass
            
            # Add to history
            self.close_history.append({
                "path": path,
                "content": file_state.content,
                "modified": file_state.modified,
                "timestamp": datetime.now().isoformat(),
                "reopened": False
            })
            
            # Remove from open files
            del self.open_files[path]
            
            # Add to recent files
            if self.config.keep_recent_files:
                if path in self.recent_files:
                    self.recent_files.remove(path)
                self.recent_files.insert(0, path)
                if len(self.recent_files) > self.config.max_recent_files:
                    self.recent_files.pop()
            
            result.success = True
            result.closed_count = 1
            result.closed_paths = [path]
            result.message = f"File closed: {path}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def close_all(self, force: bool = False) -> CloseResult:
        """
        Tüm dosyaları kapat.
        
        Args:
            force: Zorla kapat
            
        Returns:
            CloseResult: Kapatma sonucu
        """
        result = CloseResult(success=False)
        
        try:
            closed_count = 0
            closed_paths = []
            
            # Get all paths first to avoid modification during iteration
            paths = list(self.open_files.keys())
            
            for path in paths:
                sub_result = self.close_file(path, force)
                if sub_result.success:
                    closed_count += sub_result.closed_count
                    closed_paths.extend(sub_result.closed_paths)
                else:
                    result.errors.extend(sub_result.errors)
            
            result.success = closed_count > 0
            result.closed_count = closed_count
            result.closed_paths = closed_paths
            result.message = f"Closed {closed_count} files"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def close_others(self, keep_path: str, force: bool = False) -> CloseResult:
        """
        Diğerlerini kapat.
        
        Args:
            keep_path: Tutulacak dosya yolu
            force: Zorla kapat
            
        Returns:
            CloseResult: Kapatma sonucu
        """
        result = CloseResult(success=False)
        
        try:
            closed_count = 0
            closed_paths = []
            
            # Get all paths except the one to keep
            paths = [p for p in self.open_files.keys() if p != keep_path]
            
            for path in paths:
                sub_result = self.close_file(path, force)
                if sub_result.success:
                    closed_count += sub_result.closed_count
                    closed_paths.extend(sub_result.closed_paths)
                else:
                    result.errors.extend(sub_result.errors)
            
            result.success = closed_count > 0
            result.closed_count = closed_count
            result.closed_paths = closed_paths
            result.message = f"Closed {closed_count} other files"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def close_to_right(self, path: str, force: bool = False) -> CloseResult:
        """
        Sağdaki dosyaları kapat.
        
        Args:
            path: Referans dosya yolu
            force: Zorla kapat
            
        Returns:
            CloseResult: Kapatma sonucu
        """
        result = CloseResult(success=False)
        
        try:
            closed_count = 0
            closed_paths = []
            
            # Get paths in order
            paths = list(self.open_files.keys())
            
            # Find index of reference path
            if path not in paths:
                result.errors.append(f"File not open: {path}")
                return result
            
            index = paths.index(path)
            
            # Close all paths to the right
            for p in paths[index + 1:]:
                sub_result = self.close_file(p, force)
                if sub_result.success:
                    closed_count += sub_result.closed_count
                    closed_paths.extend(sub_result.closed_paths)
                else:
                    result.errors.extend(sub_result.errors)
            
            result.success = True
            result.closed_count = closed_count
            result.closed_paths = closed_paths
            result.message = f"Closed {closed_count} files to the right"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def close_to_left(self, path: str, force: bool = False) -> CloseResult:
        """
        Soldaki dosyaları kapat.
        
        Args:
            path: Referans dosya yolu
            force: Zorla kapat
            
        Returns:
            CloseResult: Kapatma sonucu
        """
        result = CloseResult(success=False)
        
        try:
            closed_count = 0
            closed_paths = []
            
            # Get paths in order
            paths = list(self.open_files.keys())
            
            # Find index of reference path
            if path not in paths:
                result.errors.append(f"File not open: {path}")
                return result
            
            index = paths.index(path)
            
            # Close all paths to the left
            for p in paths[:index]:
                sub_result = self.close_file(p, force)
                if sub_result.success:
                    closed_count += sub_result.closed_count
                    closed_paths.extend(sub_result.closed_paths)
                else:
                    result.errors.extend(sub_result.errors)
            
            result.success = True
            result.closed_count = closed_count
            result.closed_paths = closed_paths
            result.message = f"Closed {closed_count} files to the left"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def has_unsaved_changes(self, path: str) -> bool:
        """
        Kaydedilmemiş değişiklik var mı?
        
        Args:
            path: Dosya yolu
            
        Returns:
            bool: Kaydedilmemiş değişiklik var mı
        """
        if path in self.open_files:
            return self.open_files[path].modified
        return False
    
    def get_open_files(self) -> List[str]:
        """
        Açık dosyaları al.
        
        Returns:
            List[str]: Açık dosya yolları
        """
        return list(self.open_files.keys())
    
    def get_file_state(self, path: str) -> Optional[FileState]:
        """
        Dosya durumunu al.
        
        Args:
            path: Dosya yolu
            
        Returns:
            Optional[FileState]: Dosya durumu
        """
        return self.open_files.get(path)
    
    def reopen_file(self, path: str) -> CloseResult:
        """
        Dosyayı tekrar aç.
        
        Args:
            path: Dosya yolu
            
        Returns:
            CloseResult: Açma sonucu
        """
        result = CloseResult(success=False)
        
        try:
            # Find in close history
            for item in reversed(self.close_history):
                if item["path"] == path and not item["reopened"]:
                    # Reopen file
                    self.open_file(path, item["content"])
                    item["reopened"] = True
                    
                    result.success = True
                    result.message = f"File reopened: {path}"
                    return result
            
            result.errors.append("Close history not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_close_history(self) -> List[Dict[str, Any]]:
        """
        Kapatma geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.close_history
    
    def clear_history(self) -> CloseResult:
        """
        Geçmişi temizle.
        
        Returns:
            CloseResult: Temizleme sonucu
        """
        result = CloseResult(success=False)
        
        try:
            self.close_history.clear()
            result.success = True
            result.message = "Close history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_recent_files(self) -> List[str]:
        """
        Son dosyaları al.
        
        Returns:
            List[str]: Son dosya yolları
        """
        return self.recent_files
    
    def clear_recent_files(self) -> CloseResult:
        """
        Son dosyaları temizle.
        
        Returns:
            CloseResult: Temizleme sonucu
        """
        result = CloseResult(success=False)
        
        try:
            self.recent_files.clear()
            result.success = True
            result.message = "Recent files cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: CloseConfig) -> CloseResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            CloseResult: Güncelleme sonucu
        """
        result = CloseResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> CloseConfig:
        """
        Konfigürasyon al.
        
        Returns:
            CloseConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = FileCloseEngine()
    
    engine.open_file("test.txt", "Hello World")
    result = engine.close_file("test.txt", force=True)
    
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")
