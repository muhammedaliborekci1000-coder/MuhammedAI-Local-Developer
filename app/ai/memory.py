"""
MuhammedAI Local Developer - Memory System
Agent'ın bilgi yönetimi için genişletilmiş memory sistemi.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime, UTC
from enum import Enum

from app.core.config import PROJECT_ROOT


class MemoryCategory(Enum):
    """Memory kategorileri."""
    CONVERSATION = "conversation"
    PROJECT = "project"
    DECISION = "decision"
    PREFERENCE = "preference"
    FACT = "fact"
    TASK = "task"
    FAILURE = "failure"


class MemoryScope(Enum):
    """Memory kapsamları."""
    GLOBAL = "global"
    PROJECT = "project"
    SESSION = "session"


class MemorySource(Enum):
    """Memory kaynakları."""
    USER = "user"
    AGENT = "agent"
    TOOL = "tool"
    TEST = "test"
    CODEBASE = "codebase"
    SYSTEM = "system"


@dataclass
class MemoryRecord:
    """Memory kaydı."""
    id: str
    category: MemoryCategory
    content: str
    scope: MemoryScope
    source: MemorySource
    importance: int = 2  # 1-5
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: Dict[str, Any] = field(default_factory=dict)
    project_id: Optional[str] = None  # Project scope için
    session_id: Optional[str] = None  # Session scope için


class MemorySystem:
    """
    Genişletilmiş memory sistemi.
    
    Özellikler:
    - CRUD işlemleri
    - Search ve relevance
    - Deduplication
    - Conflict resolution
    - Source tracking
    - Persistence
    """
    
    def __init__(self, storage_dir: Optional[Path] = None):
        """
        Args:
            storage_dir: Memory storage dizini
        """
        if storage_dir is None:
            storage_dir = PROJECT_ROOT / "memory"
        
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.records: Dict[str, MemoryRecord] = {}
        self._load_from_disk()
    
    def add(
        self,
        category: MemoryCategory,
        content: str,
        scope: MemoryScope = MemoryScope.SESSION,
        source: MemorySource = MemorySource.AGENT,
        importance: int = 2,
        project_id: Optional[str] = None,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> MemoryRecord:
        """
        Memory kaydı ekle.
        
        Args:
            category: Kategori
            content: İçerik
            scope: Kapsam
            source: Kaynak
            importance: Önem seviyesi (1-5)
            project_id: Proje ID (project scope için)
            session_id: Session ID (session scope için)
            metadata: Ek meta veriler
            
        Returns:
            MemoryRecord: Eklenen kayıt
        """
        # Deduplication kontrolü
        content_hash = self._hash_content(content)
        existing = self._find_duplicate(content_hash, category, scope)
        
        if existing:
            # Güncelle
            existing.content = content
            existing.updated_at = datetime.now(UTC)
            existing.importance = max(existing.importance, importance)
            if metadata:
                existing.metadata.update(metadata)
            self._save_to_disk()
            return existing
        
        # Yeni kayıt
        record_id = self._generate_id(content, category, scope)
        
        record = MemoryRecord(
            id=record_id,
            category=category,
            content=content,
            scope=scope,
            source=source,
            importance=importance,
            project_id=project_id,
            session_id=session_id,
            metadata=metadata or {}
        )
        
        self.records[record_id] = record
        self._save_to_disk()
        
        return record
    
    def get(self, record_id: str) -> Optional[MemoryRecord]:
        """
        Memory kaydı al.
        
        Args:
            record_id: Kayıt ID
            
        Returns:
            Optional[MemoryRecord]: Kayıt veya None
        """
        return self.records.get(record_id)
    
    def search(
        self,
        query: str,
        category: Optional[MemoryCategory] = None,
        scope: Optional[MemoryScope] = None,
        source: Optional[MemorySource] = None,
        min_importance: int = 1,
        project_id: Optional[str] = None,
        session_id: Optional[str] = None,
        limit: int = 20
    ) -> List[MemoryRecord]:
        """
        Memory ara.
        
        Args:
            query: Sorgu metni
            category: Kategori filtresi
            scope: Kapsam filtresi
            source: Kaynak filtresi
            min_importance: Minimum önem seviyesi
            project_id: Proje ID filtresi
            session_id: Session ID filtresi
            limit: Maksimum sonuç
            
        Returns:
            List[MemoryRecord]: Eşleşen kayıtlar
        """
        results = []
        query_lower = query.lower()
        
        for record in self.records.values():
            # Filtreler
            if category and record.category != category:
                continue
            if scope and record.scope != scope:
                continue
            if source and record.source != source:
                continue
            if record.importance < min_importance:
                continue
            if project_id and record.project_id != project_id:
                continue
            if session_id and record.session_id != session_id:
                continue
            
            # Relevance: exact keyword match
            if query_lower in record.content.lower():
                results.append(record)
        
        # Önce importance, sonra recency sırala
        results.sort(key=lambda r: (r.importance, r.updated_at), reverse=True)
        
        return results[:limit]
    
    def update(
        self,
        record_id: str,
        content: Optional[str] = None,
        importance: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[MemoryRecord]:
        """
        Memory kaydı güncelle.
        
        Args:
            record_id: Kayıt ID
            content: Yeni içerik
            importance: Yeni önem seviyesi
            metadata: Yeni meta veriler
            
        Returns:
            Optional[MemoryRecord]: Güncellenmiş kayıt veya None
        """
        record = self.records.get(record_id)
        if not record:
            return None
        
        if content is not None:
            record.content = content
        if importance is not None:
            record.importance = importance
        if metadata is not None:
            record.metadata.update(metadata)
        
        record.updated_at = datetime.now(UTC)
        self._save_to_disk()
        
        return record
    
    def delete(self, record_id: str) -> bool:
        """
        Memory kaydı sil.
        
        Args:
            record_id: Kayıt ID
            
        Returns:
            bool: Silindi mi
        """
        if record_id in self.records:
            del self.records[record_id]
            self._save_to_disk()
            return True
        return False
    
    def clear(
        self,
        scope: Optional[MemoryScope] = None,
        project_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> int:
        """
        Memory temizle.
        
        Args:
            scope: Kapsam filtresi
            project_id: Proje ID filtresi
            session_id: Session ID filtresi
            
        Returns:
            int: Silinen kayıt sayısı
        """
        to_delete = []
        
        for record_id, record in self.records.items():
            if scope and record.scope != scope:
                continue
            if project_id and record.project_id != project_id:
                continue
            if session_id and record.session_id != session_id:
                continue
            to_delete.append(record_id)
        
        for record_id in to_delete:
            del self.records[record_id]
        
        self._save_to_disk()
        return len(to_delete)
    
    def _generate_id(self, content: str, category: MemoryCategory, scope: MemoryScope) -> str:
        """Kayıt ID oluştur."""
        content_hash = self._hash_content(content)
        return f"{category.value}_{scope.value}_{content_hash[:16]}"
    
    def _hash_content(self, content: str) -> str:
        """İçerik hash'i oluştur."""
        return hashlib.md5(content.encode()).hexdigest()
    
    def _find_duplicate(
        self,
        content_hash: str,
        category: MemoryCategory,
        scope: MemoryScope
    ) -> Optional[MemoryRecord]:
        """Duplicate kayıt bul."""
        for record in self.records.values():
            if record.category == category and record.scope == scope:
                if self._hash_content(record.content) == content_hash:
                    return record
        return None
    
    def _save_to_disk(self) -> None:
        """Disk'e kaydet."""
        data = {
            "records": [
                {
                    "id": r.id,
                    "category": r.category.value,
                    "content": r.content,
                    "scope": r.scope.value,
                    "source": r.source.value,
                    "importance": r.importance,
                    "created_at": r.created_at.isoformat(),
                    "updated_at": r.updated_at.isoformat(),
                    "metadata": r.metadata,
                    "project_id": r.project_id,
                    "session_id": r.session_id
                }
                for r in self.records.values()
            ]
        }
        
        # Global memory
        global_file = self.storage_dir / "global.json"
        with open(global_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _load_from_disk(self) -> None:
        """Disk'ten yükle."""
        global_file = self.storage_dir / "global.json"
        
        if not global_file.exists():
            return
        
        try:
            with open(global_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for r_data in data.get("records", []):
                record = MemoryRecord(
                    id=r_data["id"],
                    category=MemoryCategory(r_data["category"]),
                    content=r_data["content"],
                    scope=MemoryScope(r_data["scope"]),
                    source=MemorySource(r_data["source"]),
                    importance=r_data["importance"],
                    created_at=datetime.fromisoformat(r_data["created_at"]),
                    updated_at=datetime.fromisoformat(r_data["updated_at"]),
                    metadata=r_data.get("metadata", {}),
                    project_id=r_data.get("project_id"),
                    session_id=r_data.get("session_id")
                )
                self.records[record.id] = record
        except Exception as e:
            print(f"Memory yükleme hatası: {e}")
