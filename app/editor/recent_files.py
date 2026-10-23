"""
MuhammedAI Local Developer - Recent Files
Recent files management engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import os
import json
from datetime import datetime


class SortMode(Enum):
    """Sort mode."""
    DATE_DESC = "date_desc"
    DATE_ASC = "date_asc"
    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"
    FREQUENCY = "frequency"


class FilterMode(Enum):
    """Filter mode."""
    ALL = "all"
    PINNED = "pinned"
    UNPINNED = "unpinned"
    BY_EXTENSION = "by_extension"
    BY_PROJECT = "by_project"


@dataclass
class RecentFile:
    """Recent file entry."""
    path: str
    opened_at: str
    last_accessed: str
    access_count: int = 0
    pinned: bool = False
    project: Optional[str] = None


@dataclass
class RecentFilesConfig:
    """Recent files configuration."""
    max_files: int = 50
    max_pinned: int = 10
    persist_to_disk: bool = True
    storage_path: str = ""
    sort_mode: SortMode = SortMode.DATE_DESC
    filter_mode: FilterMode = FilterMode.ALL
    show_notification: bool = True


@dataclass
class RecentFilesResult:
    """Recent files result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    files: List[RecentFile] = field(default_factory=list)
    count: int = 0


class RecentFilesEngine:
    """
    Recent files management engine.
    
    Özellikler:
    - Add to recent files
    - Get recent files
    - Clear recent files
    - Remove from recent files
    - Pin files
    - Unpin files
    - Recent files limit
    - Persist to disk
    - Load from disk
    - Group by project
    - Filter by type
    - Search recent files
    - Sort by date/frequency
    - Access count tracking
    """
    
    def __init__(self, config: Optional[RecentFilesConfig] = None):
        """Initialize recent files engine."""
        self.config = config or RecentFilesConfig()
        self.recent_files: List[RecentFile] = []
        
        # Set default storage path
        if not self.config.storage_path:
            self.config.storage_path = os.path.join(
                os.path.expanduser("~"),
                ".muhammedai",
                "recent_files.json"
            )
        
        # Load from disk if enabled
        if self.config.persist_to_disk:
            self._load_from_disk()
    
    def add_file(self, path: str, project: Optional[str] = None) -> RecentFilesResult:
        """
        Dosyayı son dosyalara ekle.
        
        Args:
            path: Dosya yolu
            project: Proje adı
            
        Returns:
            RecentFilesResult: Ekleme sonucu
        """
        result = RecentFilesResult(success=False)
        
        try:
            now = datetime.now().isoformat()
            
            # Check if file already exists
            existing = None
            for file in self.recent_files:
                if file.path == path:
                    existing = file
                    break
            
            if existing:
                # Update existing
                existing.last_accessed = now
                existing.access_count += 1
                if project:
                    existing.project = project
                
                # Move to front
                self.recent_files.remove(existing)
                self.recent_files.insert(0, existing)
            else:
                # Add new
                new_file = RecentFile(
                    path=path,
                    opened_at=now,
                    last_accessed=now,
                    access_count=1,
                    pinned=False,
                    project=project
                )
                self.recent_files.insert(0, new_file)
            
            # Enforce limit
            self._enforce_limit()
            
            # Persist to disk
            if self.config.persist_to_disk:
                self._save_to_disk()
            
            result.success = True
            result.files = self._get_sorted_files()
            result.count = len(result.files)
            result.message = f"File added to recent: {path}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def remove_file(self, path: str) -> RecentFilesResult:
        """
        Dosyayı son dosyalardan kaldır.
        
        Args:
            path: Dosya yolu
            
        Returns:
            RecentFilesResult: Kaldırma sonucu
        """
        result = RecentFilesResult(success=False)
        
        try:
            # Find and remove
            for file in self.recent_files:
                if file.path == path:
                    self.recent_files.remove(file)
                    
                    # Persist to disk
                    if self.config.persist_to_disk:
                        self._save_to_disk()
                    
                    result.success = True
                    result.files = self._get_sorted_files()
                    result.count = len(result.files)
                    result.message = f"File removed from recent: {path}"
                    return result
            
            result.errors.append(f"File not found in recent: {path}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def pin_file(self, path: str) -> RecentFilesResult:
        """
        Dosyayı sabitle.
        
        Args:
            path: Dosya yolu
            
        Returns:
            RecentFilesResult: Sabitleme sonucu
        """
        result = RecentFilesResult(success=False)
        
        try:
            # Find and pin
            for file in self.recent_files:
                if file.path == path:
                    file.pinned = True
                    
                    # Move pinned files to front
                    self.recent_files.sort(key=lambda x: not x.pinned)
                    
                    # Persist to disk
                    if self.config.persist_to_disk:
                        self._save_to_disk()
                    
                    result.success = True
                    result.files = self._get_sorted_files()
                    result.count = len(result.files)
                    result.message = f"File pinned: {path}"
                    return result
            
            result.errors.append(f"File not found in recent: {path}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def unpin_file(self, path: str) -> RecentFilesResult:
        """
        Dosyanın sabitlemesini kaldır.
        
        Args:
            path: Dosya yolu
            
        Returns:
            RecentFilesResult: Sabitleme kaldırma sonucu
        """
        result = RecentFilesResult(success=False)
        
        try:
            # Find and unpin
            for file in self.recent_files:
                if file.path == path:
                    file.pinned = False
                    
                    # Persist to disk
                    if self.config.persist_to_disk:
                        self._save_to_disk()
                    
                    result.success = True
                    result.files = self._get_sorted_files()
                    result.count = len(result.files)
                    result.message = f"File unpinned: {path}"
                    return result
            
            result.errors.append(f"File not found in recent: {path}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_recent_files(self, limit: Optional[int] = None) -> RecentFilesResult:
        """
        Son dosyaları al.
        
        Args:
            limit: Limit
            
        Returns:
            RecentFilesResult: Son dosyalar
        """
        result = RecentFilesResult(success=False)
        
        try:
            files = self._get_sorted_files()
            
            if limit:
                files = files[:limit]
            
            result.success = True
            result.files = files
            result.count = len(files)
            result.message = f"Retrieved {len(files)} recent files"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def search_files(self, query: str) -> RecentFilesResult:
        """
        Dosya ara.
        
        Args:
            query: Arama sorgusu
            
        Returns:
            RecentFilesResult: Arama sonucu
        """
        result = RecentFilesResult(success=False)
        
        try:
            query_lower = query.lower()
            files = [
                file for file in self.recent_files
                if query_lower in file.path.lower()
            ]
            
            result.success = True
            result.files = files
            result.count = len(files)
            result.message = f"Found {len(files)} files matching '{query}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def filter_by_extension(self, extension: str) -> RecentFilesResult:
        """
    -Uzantıya göre filtrele.
        
        Args:
            extension: Dosya uzantısı
            
        Returns:
            RecentFilesResult: Filtreleme sonucu
        """
        result = RecentFilesResult(success=False)
        
        try:
            ext = extension.lower()
            if not ext.startswith('.'):
                ext = '.' + ext
            
            files = [
                file for file in self.recent_files
                if file.path.lower().endswith(ext)
            ]
            
            result.success = True
            result.files = files
            result.count = len(files)
            result.message = f"Found {len(files)} files with extension '{extension}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def filter_by_project(self, project: str) -> RecentFilesResult:
        """
        Projeye göre filtrele.
        
        Args:
            project: Proje adı
            
        Returns:
            RecentFilesResult: Filtreleme sonucu
        """
        result = RecentFilesResult(success=False)
        
        try:
            files = [
                file for file in self.recent_files
                if file.project == project
            ]
            
            result.success = True
            result.files = files
            result.count = len(files)
            result.message = f"Found {len(files)} files in project '{project}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_pinned_files(self) -> RecentFilesResult:
        """
        Sabitlenmiş dosyaları al.
        
        Returns:
            RecentFilesResult: Sabitlenmiş dosyalar
        """
        result = RecentFilesResult(success=False)
        
        try:
            files = [file for file in self.recent_files if file.pinned]
            
            result.success = True
            result.files = files
            result.count = len(files)
            result.message = f"Retrieved {len(files)} pinned files"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clear_recent_files(self) -> RecentFilesResult:
        """
        Son dosyaları temizle.
        
        Returns:
            RecentFilesResult: Temizleme sonucu
        """
        result = RecentFilesResult(success=False)
        
        try:
            self.recent_files.clear()
            
            # Persist to disk
            if self.config.persist_to_disk:
                self._save_to_disk()
            
            result.success = True
            result.files = []
            result.count = 0
            result.message = "Recent files cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _enforce_limit(self) -> None:
        """
        Limiti uygula.
        """
        # Count pinned files
        pinned_count = sum(1 for file in self.recent_files if file.pinned)
        
        # Enforce pinned limit
        if pinned_count > self.config.max_pinned:
            # Remove oldest unpinned files first
            unpinned = [file for file in self.recent_files if not file.pinned]
            self.recent_files = [file for file in self.recent_files if file.pinned]
            self.recent_files.extend(unpinned[:self.config.max_pinned - pinned_count])
        
        # Enforce total limit
        if len(self.recent_files) > self.config.max_files:
            self.recent_files = self.recent_files[:self.config.max_files]
    
    def _get_sorted_files(self) -> List[RecentFile]:
        """
        Sıralanmış dosyaları al.
        
        Returns:
            List[RecentFile]: Sıralanmış dosyalar
        """
        files = self.recent_files.copy()
        
        if self.config.sort_mode == SortMode.DATE_DESC:
            files.sort(key=lambda x: x.last_accessed, reverse=True)
        elif self.config.sort_mode == SortMode.DATE_ASC:
            files.sort(key=lambda x: x.last_accessed)
        elif self.config.sort_mode == SortMode.NAME_ASC:
            files.sort(key=lambda x: os.path.basename(x.path).lower())
        elif self.config.sort_mode == SortMode.NAME_DESC:
            files.sort(key=lambda x: os.path.basename(x.path).lower(), reverse=True)
        elif self.config.sort_mode == SortMode.FREQUENCY:
            files.sort(key=lambda x: x.access_count, reverse=True)
        
        # Pinned files always first
        files.sort(key=lambda x: not x.pinned)
        
        return files
    
    def _save_to_disk(self) -> None:
        """
        Diske kaydet.
        """
        try:
            # Create directory if needed
            directory = os.path.dirname(self.config.storage_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            # Convert to dict
            data = [
                {
                    "path": file.path,
                    "opened_at": file.opened_at,
                    "last_accessed": file.last_accessed,
                    "access_count": file.access_count,
                    "pinned": file.pinned,
                    "project": file.project
                }
                for file in self.recent_files
            ]
            
            # Write to file
            with open(self.config.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
    
    def _load_from_disk(self) -> None:
        """
        Diskten yükle.
        """
        try:
            if not os.path.exists(self.config.storage_path):
                return
            
            with open(self.config.storage_path, 'r') as f:
                data = json.load(f)
            
            # Convert to RecentFile objects
            self.recent_files = [
                RecentFile(
                    path=item["path"],
                    opened_at=item["opened_at"],
                    last_accessed=item["last_accessed"],
                    access_count=item["access_count"],
                    pinned=item["pinned"],
                    project=item.get("project")
                )
                for item in data
            ]
        except Exception:
            pass
    
    def update_config(self, config: RecentFilesConfig) -> RecentFilesResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            RecentFilesResult: Güncelleme sonucu
        """
        result = RecentFilesResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> RecentFilesConfig:
        """
        Konfigürasyon al.
        
        Returns:
            RecentFilesConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = RecentFilesEngine()
    
    result = engine.add_file("/path/to/file.txt")
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")
