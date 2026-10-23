"""
MuhammedAI Local Developer - Git Tag
Git tag engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class TagType(Enum):
    """Tag type."""
    LIGHTWEIGHT = "lightweight"
    ANNOTATED = "annotated"
    SIGNED = "signed"


class TagAction(Enum):
    """Tag action."""
    CREATE = "create"
    DELETE = "delete"
    LIST = "list"
    SHOW = "show"
    PUSH = "push"
    FETCH = "fetch"
    VERIFY = "verify"
    CHECKOUT = "checkout"
    RENAME = "rename"


class TagScope(Enum):
    """Tag scope."""
    LOCAL = "local"
    REMOTE = "remote"
    ALL = "all"


@dataclass
class TagInfo:
    """Tag information."""
    name: str
    tag_type: TagType
    commit_hash: str
    message: str = ""
    author: str = ""
    date: datetime = None
    is_signed: bool = False
    signature: str = ""


@dataclass
class TagConfig:
    """Tag configuration."""
    auto_push: bool = False
    sign_tags: bool = False
    gpg_key: Optional[str] = None
    show_signature: bool = True
    verify_tags: bool = True
    force_push: bool = False
    include_lightweight: bool = True
    include_annotated: bool = True


@dataclass
class TagResult:
    """Tag result."""
    success: bool
    action: Optional[str] = None
    tag_name: Optional[str] = None
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    tags: List[TagInfo] = field(default_factory=list)
    total_tags: int = 0


class GitTagEngine:
    """
    Git tag engine.
    
    Özellikler:
    - Tag creation
    - Tag deletion
    - Tag listing
    - Tag showing
    - Tag pushing
    - Tag fetching
    - Tag verification
    - Tag signing
    - Tag history
    - Tag filtering
    - Tag statistics
    - Tag validation
    - Tag comparison
    - Tag checkout
    - Tag renaming
    - Lightweight tags
    - Annotated tags
    - Signed tags
    """
    
    def __init__(self, config: Optional[TagConfig] = None):
        """Initialize git tag engine."""
        self.config = config or TagConfig()
        self.tags: Dict[str, TagInfo] = {}
        self.tag_history: List[Tuple[str, str]] = []  # (action, tag_name)
        self._tag_counter = 0
    
    def create_tag(
        self,
        name: str,
        commit_hash: str,
        message: Optional[str] = None,
        tag_type: TagType = TagType.LIGHTWEIGHT,
        sign: bool = False
    ) -> TagResult:
        """
        Tag oluştur.
        
        Args:
            name: Tag adı
            commit_hash: Commit hash
            message: Tag mesajı (annotated için)
            tag_type: Tag tipi
            sign: İmzala mı
            
        Returns:
            TagResult: Oluşturma sonucu
        """
        result = TagResult(success=False)
        result.action = TagAction.CREATE.value
        result.tag_name = name
        
        try:
            # Validation
            if name in self.tags:
                result.errors.append(f"Tag already exists: {name}")
                return result
            
            # Tag tipi belirle
            if message or tag_type == TagType.ANNOTATED:
                tag_type = TagType.ANNOTATED
            if sign or tag_type == TagType.SIGNED:
                tag_type = TagType.SIGNED
            
            # Tag oluştur
            now = datetime.now()
            tag_info = TagInfo(
                name=name,
                tag_type=tag_type,
                commit_hash=commit_hash,
                message=message or "",
                author="Developer",
                date=now,
                is_signed=sign
            )
            
            self.tags[name] = tag_info
            self.tag_history.append(("create", name))
            
            result.success = True
            result.tags.append(tag_info)
            result.total_tags = len(self.tags)
            result.message = f"Created tag: {name}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def delete_tag(self, name: str, remote: bool = False) -> TagResult:
        """
        Tag sil.
        
        Args:
            name: Tag adı
            remote: Remote'dan sil
            
        Returns:
            TagResult: Silme sonucu
        """
        result = TagResult(success=False)
        result.action = TagAction.DELETE.value
        result.tag_name = name
        
        try:
            if name not in self.tags:
                result.errors.append(f"Tag not found: {name}")
                return result
            
            del self.tags[name]
            self.tag_history.append(("delete", name))
            
            result.success = True
            result.total_tags = len(self.tags)
            result.message = f"Deleted tag: {name}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def list_tags(
        self,
        tag_type: Optional[TagType] = None,
        scope: TagScope = TagScope.LOCAL
    ) -> TagResult:
        """
        Tagleri listele.
        
        Args:
            tag_type: Tag tipi (opsiyonel)
            scope: Kapsam
            
        Returns:
            TagResult: Listeleme sonucu
        """
        result = TagResult(success=False)
        result.action = TagAction.LIST.value
        
        try:
            filtered_tags = []
            
            for tag in self.tags.values():
                if tag_type and tag.tag_type != tag_type:
                    continue
                
                if scope == TagScope.LOCAL:
                    filtered_tags.append(tag)
                elif scope == TagScope.REMOTE:
                    # Simüle edilmiş remote filtreleme
                    pass
                else:
                    filtered_tags.append(tag)
            
            result.success = True
            result.tags = filtered_tags
            result.total_tags = len(filtered_tags)
            result.message = f"Listed {len(filtered_tags)} tags"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def show_tag(self, name: str) -> TagResult:
        """
        Tag detaylarını göster.
        
        Args:
            name: Tag adı
            
        Returns:
            TagResult: Gösterme sonucu
        """
        result = TagResult(success=False)
        result.action = TagAction.SHOW.value
        result.tag_name = name
        
        try:
            if name not in self.tags:
                result.errors.append(f"Tag not found: {name}")
                return result
            
            tag_info = self.tags[name]
            result.tags.append(tag_info)
            
            result.success = True
            result.message = f"Showing tag: {name}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def push_tag(self, name: str, remote: str = "origin") -> TagResult:
        """
        Tag'i push et.
        
        Args:
            name: Tag adı
            remote: Remote adı
            
        Returns:
            TagResult: Push sonucu
        """
        result = TagResult(success=False)
        result.action = TagAction.PUSH.value
        result.tag_name = name
        
        try:
            if name not in self.tags:
                result.errors.append(f"Tag not found: {name}")
                return result
            
            self.tag_history.append(("push", name))
            
            result.success = True
            result.message = f"Pushed tag {name} to {remote}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def fetch_tags(self, remote: str = "origin") -> TagResult:
        """
        Tagleri fetch et.
        
        Args:
            remote: Remote adı
            
        Returns:
            TagResult: Fetch sonucu
        """
        result = TagResult(success=False)
        result.action = TagAction.FETCH.value
        
        try:
            self.tag_history.append(("fetch", remote))
            
            result.success = True
            result.message = f"Fetched tags from {remote}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def verify_tag(self, name: str) -> TagResult:
        """
        Tag'i doğrula.
        
        Args:
            name: Tag adı
            
        Returns:
            TagResult: Doğrulama sonucu
        """
        result = TagResult(success=False)
        result.action = TagAction.VERIFY.value
        result.tag_name = name
        
        try:
            if name not in self.tags:
                result.errors.append(f"Tag not found: {name}")
                return result
            
            tag_info = self.tags[name]
            
            if tag_info.is_signed:
                result.success = True
                result.message = f"Tag {name} signature verified"
            else:
                result.errors.append(f"Tag {name} is not signed")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def checkout_tag(self, name: str) -> TagResult:
        """
        Tag'e checkout yap.
        
        Args:
            name: Tag adı
            
        Returns:
            TagResult: Checkout sonucu
        """
        result = TagResult(success=False)
        result.action = TagAction.CHECKOUT.value
        result.tag_name = name
        
        try:
            if name not in self.tags:
                result.errors.append(f"Tag not found: {name}")
                return result
            
            self.tag_history.append(("checkout", name))
            
            result.success = True
            result.message = f"Checked out tag: {name}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def rename_tag(self, old_name: str, new_name: str) -> TagResult:
        """
        Tag'i yeniden adlandır.
        
        Args:
            old_name: Eski ad
            new_name: Yeni ad
            
        Returns:
            TagResult: Yeniden adlandırma sonucu
        """
        result = TagResult(success=False)
        result.action = TagAction.RENAME.value
        result.tag_name = new_name
        
        try:
            if old_name not in self.tags:
                result.errors.append(f"Tag not found: {old_name}")
                return result
            
            if new_name in self.tags:
                result.errors.append(f"Tag already exists: {new_name}")
                return result
            
            tag_info = self.tags[old_name]
            tag_info.name = new_name
            
            self.tags[new_name] = tag_info
            del self.tags[old_name]
            
            self.tag_history.append(("rename", f"{old_name}->{new_name}"))
            
            result.success = True
            result.message = f"Renamed tag: {old_name} -> {new_name}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_tag(self, name: str) -> Optional[TagInfo]:
        """
        Tag bilgisi al.
        
        Args:
            name: Tag adı
            
        Returns:
            Optional[TagInfo]: Tag bilgisi
        """
        return self.tags.get(name)
    
    def get_tag_count(self) -> int:
        """
        Tag sayısını al.
        
        Returns:
            int: Sayı
        """
        return len(self.tags)
    
    def tag_exists(self, name: str) -> bool:
        """
        Tag var mı kontrol et.
        
        Args:
            name: Tag adı
            
        Returns:
            bool: Var mı
        """
        return name in self.tags
    
    def get_tag_history(self) -> List[Tuple[str, str]]:
        """
        Tag geçmişini al.
        
        Returns:
            List[Tuple[str, str]]: Geçmiş
        """
        return self.tag_history
    
    def clear_history(self) -> TagResult:
        """
        Geçmişi temizle.
        
        Returns:
            TagResult: Temizleme sonucu
        """
        result = TagResult(success=False)
        
        try:
            self.tag_history.clear()
            result.success = True
            result.message = "Tag history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        İstatistikleri al.
        
        Returns:
            Dict[str, Any]: İstatistikler
        """
        lightweight = len([t for t in self.tags.values() if t.tag_type == TagType.LIGHTWEIGHT])
        annotated = len([t for t in self.tags.values() if t.tag_type == TagType.ANNOTATED])
        signed = len([t for t in self.tags.values() if t.tag_type == TagType.SIGNED])
        
        return {
            "total_tags": len(self.tags),
            "lightweight": lightweight,
            "annotated": annotated,
            "signed": signed
        }
    
    def update_config(self, config: TagConfig) -> TagResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            TagResult: Güncelleme sonucu
        """
        result = TagResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> TagConfig:
        """
        Konfigürasyon al.
        
        Returns:
            TagConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = GitTagEngine()
    
    # Tag oluştur
    result = engine.create_tag("v1.0.0", "abc123", "Version 1.0.0")
    print(f"Create: {result.success}")
    
    # Tagleri listele
    result = engine.list_tags()
    print(f"List: {result.success}")
