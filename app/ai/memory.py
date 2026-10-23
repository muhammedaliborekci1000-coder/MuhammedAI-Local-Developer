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
    tags: List[str] = field(default_factory=list)  # Etiketler
    related_ids: List[str] = field(default_factory=list)  # İlişkili memory ID'leri
    access_count: int = 0  # Erişim sayısı
    last_accessed: Optional[datetime] = None  # Son erişim zamanı
    decay_score: float = 0.0  # Decay skoru (0-1)


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
    - Tagging
    - Relationships
    - Decay/aging
    - Consolidation
    - Analytics
    - Export/import
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
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None
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
            tags: Etiketler
            
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
            metadata=metadata or {},
            tags=tags or []
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
        record = self.records.get(record_id)
        if record:
            # Access tracking
            record.access_count += 1
            record.last_accessed = datetime.now(UTC)
        return record
    
    def search(
        self,
        query: str,
        category: Optional[MemoryCategory] = None,
        scope: Optional[MemoryScope] = None,
        source: Optional[MemorySource] = None,
        min_importance: int = 1,
        project_id: Optional[str] = None,
        session_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
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
            tags: Etiket filtresi
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
            if tags and not any(tag in record.tags for tag in tags):
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
    
    def add_tag(self, record_id: str, tag: str) -> bool:
        """
        Memory kaydına etiket ekle.
        
        Args:
            record_id: Kayıt ID
            tag: Etiket
            
        Returns:
            bool: Başarılı mı
        """
        record = self.records.get(record_id)
        if not record:
            return False
        
        if tag not in record.tags:
            record.tags.append(tag)
            self._save_to_disk()
        return True
    
    def remove_tag(self, record_id: str, tag: str) -> bool:
        """
        Memory kaydından etiket kaldır.
        
        Args:
            record_id: Kayıt ID
            tag: Etiket
            
        Returns:
            bool: Başarılı mı
        """
        record = self.records.get(record_id)
        if not record:
            return False
        
        if tag in record.tags:
            record.tags.remove(tag)
            self._save_to_disk()
        return True
    
    def add_relationship(self, record_id: str, related_id: str) -> bool:
        """
        Memory kaydı arasına ilişki ekle.
        
        Args:
            record_id: Kayıt ID
            related_id: İlişkili kayıt ID
            
        Returns:
            bool: Başarılı mı
        """
        record = self.records.get(record_id)
        if not record:
            return False
        
        if related_id not in record.related_ids:
            record.related_ids.append(related_id)
            self._save_to_disk()
        return True
    
    def remove_relationship(self, record_id: str, related_id: str) -> bool:
        """
        Memory kaydı arasındaki ilişkiyi kaldır.
        
        Args:
            record_id: Kayıt ID
            related_id: İlişkili kayıt ID
            
        Returns:
            bool: Başarılı mı
        """
        record = self.records.get(record_id)
        if not record:
            return False
        
        if related_id in record.related_ids:
            record.related_ids.remove(related_id)
            self._save_to_disk()
        return True
    
    def get_related_memories(self, record_id: str) -> List[MemoryRecord]:
        """
        İlişkili memory kayıtlarını al.
        
        Args:
            record_id: Kayıt ID
            
        Returns:
            List[MemoryRecord]: İlişkili kayıtlar
        """
        record = self.records.get(record_id)
        if not record:
            return []
        
        related = []
        for related_id in record.related_ids:
            if related_id in self.records:
                related.append(self.records[related_id])
        
        return related
    
    def apply_decay(self, days_threshold: int = 30) -> int:
        """
        Memory decay uygulama (eski kayıtların önemini azaltma).
        
        Args:
            days_threshold: Gün eşiği
            
        Returns:
            int: Güncellenen kayıt sayısı
        """
        now = datetime.now(UTC)
        updated_count = 0
        
        for record in self.records.values():
            days_since_update = (now - record.updated_at).days
            
            if days_since_update > days_threshold:
                # Decay score hesapla
                decay_factor = min(1.0, (days_since_update - days_threshold) / 100.0)
                record.decay_score = decay_factor
                
                # Importance azalt
                if record.importance > 1:
                    record.importance = max(1, record.importance - 1)
                    updated_count += 1
        
        if updated_count > 0:
            self._save_to_disk()
        
        return updated_count
    
    def consolidate_memories(self, category: MemoryCategory) -> int:
        """
        Benzer memory kayıtlarını konsolide et.
        
        Args:
            category: Kategori
            
        Returns:
            int: Konsolide edilen kayıt sayısı
        """
        category_records = [r for r in self.records.values() if r.category == category]
        consolidated = 0
        
        # Basit konsolidasyon: aynı içerik hash'ine sahip kayıtları birleştir
        seen_hashes = {}
        
        for record in category_records:
            content_hash = self._hash_content(record.content)
            
            if content_hash in seen_hashes:
                # Var olan kaydı güncelle
                existing = seen_hashes[content_hash]
                existing.access_count += record.access_count
                existing.importance = max(existing.importance, record.importance)
                existing.tags.extend(record.tags)
                existing.tags = list(set(existing.tags))  # Deduplicate tags
                existing.related_ids.extend(record.related_ids)
                existing.related_ids = list(set(existing.related_ids))  # Deduplicate
                
                # Bu kaydı sil
                del self.records[record.id]
                consolidated += 1
            else:
                seen_hashes[content_hash] = record
        
        if consolidated > 0:
            self._save_to_disk()
        
        return consolidated
    
    def get_analytics(self) -> Dict[str, Any]:
        """
        Memory analytics al.
        
        Returns:
            Dict: Analytics verileri
        """
        now = datetime.now(UTC)
        
        total_records = len(self.records)
        category_counts = {}
        scope_counts = {}
        source_counts = {}
        tag_counts = {}
        total_access_count = 0
        avg_importance = 0
        
        for record in self.records.values():
            # Category counts
            cat = record.category.value
            category_counts[cat] = category_counts.get(cat, 0) + 1
            
            # Scope counts
            scope = record.scope.value
            scope_counts[scope] = scope_counts.get(scope, 0) + 1
            
            # Source counts
            src = record.source.value
            source_counts[src] = source_counts.get(src, 0) + 1
            
            # Tag counts
            for tag in record.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
            
            # Access count
            total_access_count += record.access_count
            
            # Importance
            avg_importance += record.importance
        
        if total_records > 0:
            avg_importance /= total_records
        
        return {
            "total_records": total_records,
            "category_counts": category_counts,
            "scope_counts": scope_counts,
            "source_counts": source_counts,
            "tag_counts": tag_counts,
            "total_access_count": total_access_count,
            "avg_importance": round(avg_importance, 2),
            "storage_dir": str(self.storage_dir)
        }
    
    def export_memory(self, output_path: Optional[Path] = None) -> str:
        """
        Memory'yi dışa aktar.
        
        Args:
            output_path: Çıktı dosyası yolu
            
        Returns:
            str: JSON string
        """
        if output_path is None:
            output_path = self.storage_dir / "memory_export.json"
        
        data = {
            "exported_at": datetime.now(UTC).isoformat(),
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
                    "session_id": r.session_id,
                    "tags": r.tags,
                    "related_ids": r.related_ids,
                    "access_count": r.access_count,
                    "last_accessed": r.last_accessed.isoformat() if r.last_accessed else None,
                    "decay_score": r.decay_score
                }
                for r in self.records.values()
            ]
        }
        
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_str)
        
        return json_str
    
    def import_memory(self, input_path: Path, merge: bool = True) -> int:
        """
        Memory'yi içe aktar.
        
        Args:
            input_path: Girdi dosyası yolu
            merge: Mevcut memory ile birleştir
            
        Returns:
            int: İçe aktarılan kayıt sayısı
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        imported_count = 0
        
        for r_data in data.get("records", []):
            record_id = r_data["id"]
            
            if merge and record_id in self.records:
                # Mevcut kaydı güncelle
                existing = self.records[record_id]
                existing.access_count += r_data.get("access_count", 0)
                existing.tags.extend(r_data.get("tags", []))
                existing.tags = list(set(existing.tags))
                existing.related_ids.extend(r_data.get("related_ids", []))
                existing.related_ids = list(set(existing.related_ids))
            else:
                # Yeni kayıt oluştur
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
                    session_id=r_data.get("session_id"),
                    tags=r_data.get("tags", []),
                    related_ids=r_data.get("related_ids", []),
                    access_count=r_data.get("access_count", 0),
                    last_accessed=datetime.fromisoformat(r_data["last_accessed"]) if r_data.get("last_accessed") else None,
                    decay_score=r_data.get("decay_score", 0.0)
                )
                self.records[record_id] = record
                imported_count += 1
        
        self._save_to_disk()
        return imported_count
    
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
                    "session_id": r.session_id,
                    "tags": r.tags,
                    "related_ids": r.related_ids,
                    "access_count": r.access_count,
                    "last_accessed": r.last_accessed.isoformat() if r.last_accessed else None,
                    "decay_score": r.decay_score
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
                    session_id=r_data.get("session_id"),
                    tags=r_data.get("tags", []),
                    related_ids=r_data.get("related_ids", []),
                    access_count=r_data.get("access_count", 0),
                    last_accessed=datetime.fromisoformat(r_data["last_accessed"]) if r_data.get("last_accessed") else None,
                    decay_score=r_data.get("decay_score", 0.0)
                )
                self.records[record.id] = record
        except Exception as e:
            print(f"Memory yükleme hatası: {e}")
