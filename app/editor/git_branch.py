"""
MuhammedAI Local Developer - Git Branch
Git branch engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class BranchType(Enum):
    """Branch type."""
    LOCAL = "local"
    REMOTE = "remote"
    TRACKING = "tracking"
    DETACHED = "detached"


class BranchStatus(Enum):
    """Branch status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    AHEAD = "ahead"
    BEHIND = "behind"
    DIVERGED = "diverged"
    UP_TO_DATE = "up_to_date"


@dataclass
class Branch:
    """Branch information."""
    name: str
    branch_type: BranchType
    status: BranchStatus
    commit_hash: str
    commit_message: str
    author: str
    created_at: datetime
    last_commit_at: datetime
    is_head: bool = False
    upstream: Optional[str] = None
    ahead_count: int = 0
    behind_count: int = 0


@dataclass
class BranchConfig:
    """Branch configuration."""
    auto_create_tracking: bool = True
    show_remote_branches: bool = True
    show_status: bool = True
    protect_main: bool = True
    main_branch_name: str = "main"
    default_branch_name: str = "main"
    allow_force_delete: bool = False
    confirm_before_delete: bool = True
    confirm_before_switch: bool = True


@dataclass
class BranchResult:
    """Branch result."""
    success: bool
    branches: List[Branch] = field(default_factory=list)
    current_branch: Optional[str] = None
    total_branches: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class GitBranchEngine:
    """
    Git branch engine.
    
    Özellikler:
    - Branch creation
    - Branch deletion
    - Branch switching
    - Branch listing
    - Branch merging
    - Branch comparison
    - Branch history
    - Remote branches
    - Branch tracking
    - Branch status
    - Branch protection
    - Branch naming conventions
    - Branch validation
    - Branch filtering
    - Branch sorting
    """
    
    def __init__(self, config: Optional[BranchConfig] = None):
        """Initialize git branch engine."""
        self.config = config or BranchConfig()
        self.branches: Dict[str, Branch] = {}
        self.current_branch: Optional[str] = None
        self.branch_history: List[Tuple[str, str]] = []  # (action, branch_name)
        self._branch_counter = 0
        
        # Initialize with mock main branch
        self._generate_mock_branches()

    def _generate_mock_branches(self):
        now = datetime.now()
        main_branch = Branch(
            name=self.config.main_branch_name,
            branch_type=BranchType.LOCAL,
            status=BranchStatus.ACTIVE,
            commit_hash="abc123",
            commit_message="Initial commit",
            author="Developer",
            created_at=now,
            last_commit_at=now,
            is_head=True
        )
        self.branches[self.config.main_branch_name] = main_branch
        self.current_branch = self.config.main_branch_name

    def create_branch(
        self,
        name: str,
        from_commit: Optional[str] = None,
        is_tracking: bool = False
    ) -> BranchResult:
        """
        Branch oluştur.
        
        Args:
            name: Branch adı
            from_commit: Commit hash (opsiyonel)
            is_tracking: Tracking branch mi
            
        Returns:
            BranchResult: Oluşturma sonucu
        """
        result = BranchResult(success=False)
        
        try:
            # Validation
            if name in self.branches:
                result.errors.append(f"Branch already exists: {name}")
                return result
            
            if self.config.protect_main and name == self.config.main_branch_name:
                result.errors.append(f"Cannot create protected branch: {name}")
                return result
            
            # Branch oluştur
            now = datetime.now()
            branch_type = BranchType.TRACKING if is_tracking else BranchType.LOCAL
            
            branch = Branch(
                name=name,
                branch_type=branch_type,
                status=BranchStatus.INACTIVE,
                commit_hash=from_commit or "abc123",
                commit_message="Initial commit",
                author="Developer",
                created_at=now,
                last_commit_at=now,
                upstream=f"origin/{name}" if is_tracking else None
            )
            
            self.branches[name] = branch
            self.branch_history.append(("create", name))
            
            result.success = True
            result.branches.append(branch)
            result.total_branches = len(self.branches)
            result.message = f"Created branch: {name}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def delete_branch(self, name: str, force: bool = False) -> BranchResult:
        """
        Branch sil.
        
        Args:
            name: Branch adı
            force: Zorla sil
            
        Returns:
            BranchResult: Silme sonucu
        """
        result = BranchResult(success=False)
        
        try:
            if name not in self.branches:
                result.errors.append(f"Branch not found: {name}")
                return result
            
            branch = self.branches[name]
            
            # Protection check
            if self.config.protect_main and name == self.config.main_branch_name:
                result.errors.append(f"Cannot delete protected branch: {name}")
                return result
            
            if not force and not self.config.allow_force_delete:
                if branch.is_head:
                    result.errors.append(f"Cannot delete active branch: {name}")
                    return result
            
            del self.branches[name]
            self.branch_history.append(("delete", name))
            
            result.success = True
            result.total_branches = len(self.branches)
            result.message = f"Deleted branch: {name}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def switch_branch(self, name: str) -> BranchResult:
        """
        Branch değiştir.
        
        Args:
            name: Branch adı
            
        Returns:
            BranchResult: Değiştirme sonucu
        """
        result = BranchResult(success=False)
        
        try:
            if name not in self.branches:
                result.errors.append(f"Branch not found: {name}")
                return result
            
            # Mevcut branch'i güncelle
            if self.current_branch and self.current_branch in self.branches:
                self.branches[self.current_branch].is_head = False
                self.branches[self.current_branch].status = BranchStatus.INACTIVE
            
            # Yeni branch'i aktif yap
            self.branches[name].is_head = True
            self.branches[name].status = BranchStatus.ACTIVE
            self.current_branch = name
            
            self.branch_history.append(("switch", name))
            
            result.success = True
            result.current_branch = name
            result.branches = [self.branches[name]]
            result.total_branches = len(self.branches)
            result.message = f"Switched to branch: {name}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def list_branches(
        self,
        branch_type: Optional[BranchType] = None,
        show_remote: bool = True
    ) -> BranchResult:
        """
        Branchleri listele.
        
        Args:
            branch_type: Branch tipi (opsiyonel)
            show_remote: Remote branchleri göster
            
        Returns:
            BranchResult: Listeleme sonucu
        """
        result = BranchResult(success=False)
        
        try:
            filtered_branches = []
            
            for branch in self.branches.values():
                if branch_type and branch.branch_type != branch_type:
                    continue
                
                if not show_remote and branch.branch_type == BranchType.REMOTE:
                    continue
                
                filtered_branches.append(branch)
            
            result.success = True
            result.branches = filtered_branches
            result.total_branches = len(filtered_branches)
            result.current_branch = self.current_branch
            result.message = f"Listed {len(filtered_branches)} branches"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_current_branch(self) -> Optional[str]:
        """
        Mevcut branch'i al.
        
        Returns:
            Optional[str]: Branch adı
        """
        return self.current_branch
    
    def get_branch(self, name: str) -> Optional[Branch]:
        """
        Branch bilgisi al.
        
        Args:
            name: Branch adı
            
        Returns:
            Optional[Branch]: Branch bilgisi
        """
        return self.branches.get(name)
    
    def rename_branch(self, old_name: str, new_name: str) -> BranchResult:
        """
        Branch'i yeniden adlandır.
        
        Args:
            old_name: Eski ad
            new_name: Yeni ad
            
        Returns:
            BranchResult: Yeniden adlandırma sonucu
        """
        result = BranchResult(success=False)
        
        try:
            if old_name not in self.branches:
                result.errors.append(f"Branch not found: {old_name}")
                return result
            
            if new_name in self.branches:
                result.errors.append(f"Branch already exists: {new_name}")
                return result
            
            branch = self.branches[old_name]
            branch.name = new_name
            
            self.branches[new_name] = branch
            del self.branches[old_name]
            
            if self.current_branch == old_name:
                self.current_branch = new_name
            
            self.branch_history.append(("rename", f"{old_name}->{new_name}"))
            
            result.success = True
            result.branches.append(branch)
            result.total_branches = len(self.branches)
            result.message = f"Renamed branch: {old_name} -> {new_name}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def compare_branches(self, branch1: str, branch2: str) -> BranchResult:
        """
        Branchleri karşılaştır.
        
        Args:
            branch1: İlk branch
            branch2: İkinci branch
            
        Returns:
            BranchResult: Karşılaştırma sonucu
        """
        result = BranchResult(success=False)
        
        try:
            if branch1 not in self.branches:
                result.errors.append(f"Branch not found: {branch1}")
                return result
            
            if branch2 not in self.branches:
                result.errors.append(f"Branch not found: {branch2}")
                return result
            
            b1 = self.branches[branch1]
            b2 = self.branches[branch2]
            
            # Basit karşılaştırma
            if b1.commit_hash == b2.commit_hash:
                b1.status = BranchStatus.UP_TO_DATE
                b2.status = BranchStatus.UP_TO_DATE
                message = f"Branches {branch1} and {branch2} are identical"
            else:
                b1.status = BranchStatus.DIVERGED
                b2.status = BranchStatus.DIVERGED
                message = f"Branches {branch1} and {branch2} have diverged"
            
            result.success = True
            result.branches = [b1, b2]
            result.message = message
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_branch_history(self) -> List[Tuple[str, str]]:
        """
        Branch geçmişini al.
        
        Returns:
            List[Tuple[str, str]]: Geçmiş
        """
        return self.branch_history
    
    def clear_history(self) -> BranchResult:
        """
        Geçmişi temizle.
        
        Returns:
            BranchResult: Temizleme sonucu
        """
        result = BranchResult(success=False)
        
        try:
            self.branch_history.clear()
            result.success = True
            result.message = "Branch history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_branch_count(self) -> int:
        """
        Branch sayısını al.
        
        Returns:
            int: Sayı
        """
        return len(self.branches)
    
    def branch_exists(self, name: str) -> bool:
        """
        Branch var mı kontrol et.
        
        Args:
            name: Branch adı
            
        Returns:
            bool: Var mı
        """
        return name in self.branches
    
    def update_config(self, config: BranchConfig) -> BranchResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            BranchResult: Güncelleme sonucu
        """
        result = BranchResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> BranchConfig:
        """
        Konfigürasyon al.
        
        Returns:
            BranchConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = GitBranchEngine()
    
    # Branch oluştur
    result = engine.create_branch("feature/test")
    print(f"Create: {result.success}")
    
    # Branch değiştir
    result = engine.switch_branch("feature/test")
    print(f"Switch: {result.success}")
