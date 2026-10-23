"""
MuhammedAI Local Developer - Terminal Split
Terminal split management engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class SplitDirection(Enum):
    """Split direction."""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class SplitRatio(Enum):
    """Split ratio."""
    EQUAL = "equal"
    TOP_HEAVY = "top_heavy"
    BOTTOM_HEAVY = "bottom_heavy"
    LEFT_HEAVY = "left_heavy"
    RIGHT_HEAVY = "right_heavy"
    CUSTOM = "custom"


@dataclass
class SplitConfig:
    """Split configuration."""
    direction: SplitDirection = SplitDirection.HORIZONTAL
    ratio: SplitRatio = SplitRatio.EQUAL
    custom_ratio: float = 0.5
    show_divider: bool = True
    divider_width: int = 1
    show_notifications: bool = True


@dataclass
class SplitResult:
    """Split result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    split_id: Optional[str] = None
    parent_panel_id: Optional[str] = None
    child_panel_id: Optional[str] = None


@dataclass
class Split:
    """Terminal split."""
    id: str
    parent_panel_id: str
    child_panel_id: str
    direction: SplitDirection
    ratio: SplitRatio
    custom_ratio: float
    created_at: str = ""


class TerminalSplitEngine:
    """
    Terminal split management engine.
    
    Özellikler:
    - Split panel
    - Split direction
    - Split ratio
    - Custom ratio
    - Split undo
    - Split merge
    - Split history
    - Multiple splits
    - Split navigation
    - Split resize
    - Split divider
    """
    
    def __init__(self, config: Optional[SplitConfig] = None):
        """Initialize terminal split engine."""
        self.config = config or SplitConfig()
        self.splits: Dict[str, Split] = {}
        self.split_history: List[Dict[str, Any]] = []
        self._split_counter = 0
    
    def split_panel(
        self,
        parent_panel_id: str,
        child_panel_id: str,
        direction: Optional[SplitDirection] = None,
        ratio: Optional[SplitRatio] = None,
        custom_ratio: Optional[float] = None
    ) -> SplitResult:
        """
        Paneli böl.
        
        Args:
            parent_panel_id: Ebeveyn panel ID
            child_panel_id: Çocuk panel ID
            direction: Bölme yönü
            ratio: Bölme oranı
            custom_ratio: Özel oran
            
        Returns:
            SplitResult: Bölme sonucu
        """
        result = SplitResult(success=False)
        result.parent_panel_id = parent_panel_id
        result.child_panel_id = child_panel_id
        
        try:
            # Generate split ID
            split_id = f"split_{self._split_counter}"
            self._split_counter += 1
            
            # Create split
            split = Split(
                id=split_id,
                parent_panel_id=parent_panel_id,
                child_panel_id=child_panel_id,
                direction=direction or self.config.direction,
                ratio=ratio or self.config.ratio,
                custom_ratio=custom_ratio or self.config.custom_ratio,
                created_at=self._get_timestamp()
            )
            
            # Add to splits
            self.splits[split_id] = split
            
            # Add to history
            self.split_history.append({
                "action": "split",
                "split_id": split_id,
                "parent_panel_id": parent_panel_id,
                "child_panel_id": child_panel_id,
                "direction": split.direction.value,
                "ratio": split.ratio.value,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.split_id = split_id
            result.message = f"Panel split: {direction.value if direction else self.config.direction.value}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def merge_split(self, split_id: str) -> SplitResult:
        """
        Bölmeyi birleştir.
        
        Args:
            split_id: Split ID
            
        Returns:
            SplitResult: Birleştirme sonucu
        """
        result = SplitResult(success=False)
        result.split_id = split_id
        
        try:
            if split_id not in self.splits:
                result.errors.append(f"Split not found: {split_id}")
                return result
            
            # Get split
            split = self.splits[split_id]
            
            # Remove split
            del self.splits[split_id]
            
            # Add to history
            self.split_history.append({
                "action": "merge",
                "split_id": split_id,
                "parent_panel_id": split.parent_panel_id,
                "child_panel_id": split.child_panel_id,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.parent_panel_id = split.parent_panel_id
            result.child_panel_id = split.child_panel_id
            result.message = f"Split merged: {split_id}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def resize_split(self, split_id: str, custom_ratio: float) -> SplitResult:
        """
        Bölmeyi yeniden boyutlandır.
        
        Args:
            split_id: Split ID
            custom_ratio: Özel oran (0.0 - 1.0)
            
        Returns:
            SplitResult: Yeniden boyutlandırma sonucu
        """
        result = SplitResult(success=False)
        result.split_id = split_id
        
        try:
            if split_id not in self.splits:
                result.errors.append(f"Split not found: {split_id}")
                return result
            
            if not 0.0 <= custom_ratio <= 1.0:
                result.errors.append("Custom ratio must be between 0.0 and 1.0")
                return result
            
            # Update split
            self.splits[split_id].custom_ratio = custom_ratio
            self.splits[split_id].ratio = SplitRatio.CUSTOM
            
            # Add to history
            self.split_history.append({
                "action": "resize",
                "split_id": split_id,
                "custom_ratio": custom_ratio,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.message = f"Split resized: {custom_ratio}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def change_direction(self, split_id: str, direction: SplitDirection) -> SplitResult:
        """
        Bölme yönünü değiştir.
        
        Args:
            split_id: Split ID
            direction: Yeni yön
            
        Returns:
            SplitResult: Yön değiştirme sonucu
        """
        result = SplitResult(success=False)
        result.split_id = split_id
        
        try:
            if split_id not in self.splits:
                result.errors.append(f"Split not found: {split_id}")
                return result
            
            # Update direction
            self.splits[split_id].direction = direction
            
            # Add to history
            self.split_history.append({
                "action": "change_direction",
                "split_id": split_id,
                "direction": direction.value,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.message = f"Split direction changed: {direction.value}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_split(self, split_id: str) -> Optional[Split]:
        """
        Bölme al.
        
        Args:
            split_id: Split ID
            
        Returns:
            Optional[Split]: Split
        """
        return self.splits.get(split_id)
    
    def get_all_splits(self) -> List[Split]:
        """
        Tüm bölmeleri al.
        
        Returns:
            List[Split]: Splits
        """
        return list(self.splits.values())
    
    def get_splits_by_panel(self, panel_id: str) -> List[Split]:
        """
        Panele göre bölmeleri al.
        
        Args:
            panel_id: Panel ID
            
        Returns:
            List[Split]: Splits
        """
        return [
            split for split in self.splits.values()
            if split.parent_panel_id == panel_id or split.child_panel_id == panel_id
        ]
    
    def get_split_history(self) -> List[Dict[str, Any]]:
        """
        Bölme geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.split_history
    
    def clear_history(self) -> SplitResult:
        """
        Geçmişi temizle.
        
        Returns:
            SplitResult: Temizleme sonucu
        """
        result = SplitResult(success=False)
        
        try:
            self.split_history.clear()
            result.success = True
            result.message = "Split history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def undo_last_split(self) -> SplitResult:
        """
        Son bölmeyi geri al.
        
        Returns:
            SplitResult: Geri alma sonucu
        """
        result = SplitResult(success=False)
        
        try:
            # Find last split action
            last_split = None
            for entry in reversed(self.split_history):
                if entry["action"] == "split":
                    last_split = entry
                    break
            
            if not last_split:
                result.errors.append("No split to undo")
                return result
            
            # Merge the split
            split_id = last_split["split_id"]
            return self.merge_split(split_id)
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: SplitConfig) -> SplitResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            SplitResult: Güncelleme sonucu
        """
        result = SplitResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> SplitConfig:
        """
        Konfigürasyon al.
        
        Returns:
            SplitConfig: Konfigürasyon
        """
        return self.config
    
    def _get_timestamp(self) -> str:
        """
        Zaman damgası al.
        
        Returns:
            str: ISO format zaman damgası
        """
        return datetime.now().isoformat()


if __name__ == "__main__":
    # Basit test
    engine = TerminalSplitEngine()
    
    print("Terminal Split Engine initialized")
    print(f"Direction: {engine.config.direction.value}")
