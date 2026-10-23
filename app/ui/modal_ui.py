"""
MuhammedAI Local Developer - Modal UI
Modal UI system for web UI.
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from enum import Enum


class ModalType(Enum):
    """Modal type."""
    ALERT = "alert"
    CONFIRM = "confirm"
    PROMPT = "prompt"
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    CUSTOM = "custom"


class ModalSize(Enum):
    """Modal size."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extra_large"
    FULLSCREEN = "fullscreen"
    CUSTOM = "custom"


class ModalPosition(Enum):
    """Modal position."""
    CENTER = "center"
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    CUSTOM = "custom"


@dataclass
class Modal:
    """Modal."""
    id: str
    type: ModalType
    title: str
    content: str
    is_open: bool = False
    is_closable: bool = True
    is_draggable: bool = False
    is_resizable: bool = False
    show_overlay: bool = True
    close_on_overlay_click: bool = True
    close_on_escape: bool = True
    size: ModalSize = ModalSize.MEDIUM
    position: ModalPosition = ModalPosition.CENTER
    on_confirm: Optional[Callable] = None
    on_cancel: Optional[Callable] = None
    on_close: Optional[Callable] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModalConfig:
    """Modal configuration."""
    enabled: bool = True
    default_size: ModalSize = ModalSize.MEDIUM
    default_position: ModalPosition = ModalPosition.CENTER
    show_overlay: bool = True
    close_on_overlay_click: bool = True
    close_on_escape: bool = True
    enable_animation: bool = True
    animation_duration: int = 300  # milliseconds
    max_modals: int = 5
    enable_stack: bool = True


@dataclass
class ModalResult:
    """Modal result."""
    success: bool
    modal: Optional[Modal] = None
    modals: List[Modal] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class ModalUIManager:
    """
    Modal UI manager.
    
    Özellikler:
    - Modal types (alert, confirm, prompt, info, success, warning, error)
    - Modal sizes (small, medium, large, extra_large, fullscreen)
    - Modal positions (center, top, bottom, left, right)
    - Modal callbacks (on_confirm, on_cancel, on_close)
    - Overlay
    - Close on overlay click
    - Close on escape
    - Draggable modals
    - Resizable modals
    - Animation
    - Modal stack
    """
    
    def __init__(self, config: Optional[ModalConfig] = None):
        """
        Initialize modal UI manager.
        
        Args:
            config: Modal configuration
        """
        self.config = config or ModalConfig()
        self.modals: Dict[str, Modal] = {}
        self.modal_stack: List[str] = []
        self.modal_id_counter = 0
        self._next_modal_id()
    
    def _next_modal_id(self) -> str:
        """
        Generate next modal ID.
        
        Returns:
            str: Modal ID
        """
        self.modal_id_counter += 1
        return f"modal_{self.modal_id_counter}"
    
    def add_modal(self, modal: Modal) -> ModalResult:
        """
        Add a modal.
        
        Args:
            modal: Modal to add
            
        Returns:
            ModalResult: Add result
        """
        result = ModalResult(success=True)
        
        try:
            if len(self.modals) >= self.config.max_modals:
                result.errors.append(f"Maximum modals reached (max {self.config.max_modals})")
                result.success = False
                return result
            
            if not modal.id:
                modal.id = self._next_modal_id()
            
            self.modals[modal.id] = modal
            
            if self.config.enable_stack:
                self.modal_stack.append(modal.id)
            
            result.modal = modal
            result.modals = self.get_all_modals()
            result.message = f"Modal '{modal.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_modal(self, modal_id: str) -> ModalResult:
        """
        Remove a modal.
        
        Args:
            modal_id: Modal ID
            
        Returns:
            ModalResult: Remove result
        """
        result = ModalResult(success=False)
        
        try:
            if modal_id in self.modals:
                del self.modals[modal_id]
                
                if modal_id in self.modal_stack:
                    self.modal_stack.remove(modal_id)
                
                result.success = True
                result.modals = self.get_all_modals()
                result.message = f"Modal '{modal_id}' removed"
            else:
                result.errors.append("Modal not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_modal(self, modal_id: str) -> Optional[Modal]:
        """
        Get modal by ID.
        
        Args:
            modal_id: Modal ID
            
        Returns:
            Optional[Modal]: Modal
        """
        return self.modals.get(modal_id)
    
    def get_all_modals(self) -> List[Modal]:
        """
        Get all modals.
        
        Returns:
            List[Modal]: All modals
        """
        return list(self.modals.values())
    
    def get_open_modals(self) -> List[Modal]:
        """
        Get open modals.
        
        Returns:
            List[Modal]: Open modals
        """
        return [m for m in self.modals.values() if m.is_open]
    
    def open_modal(self, modal_id: str) -> ModalResult:
        """
        Open a modal.
        
        Args:
            modal_id: Modal ID
            
        Returns:
            ModalResult: Open result
        """
        result = ModalResult(success=False)
        
        try:
            modal = self.modals.get(modal_id)
            if modal:
                modal.is_open = True
                
                if self.config.enable_stack and modal_id not in self.modal_stack:
                    self.modal_stack.append(modal_id)
                
                result.success = True
                result.modal = modal
                result.message = f"Modal '{modal_id}' opened"
            else:
                result.errors.append("Modal not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def close_modal(self, modal_id: str) -> ModalResult:
        """
        Close a modal.
        
        Args:
            modal_id: Modal ID
            
        Returns:
            ModalResult: Close result
        """
        result = ModalResult(success=False)
        
        try:
            modal = self.modals.get(modal_id)
            if modal:
                modal.is_open = False
                
                if modal.on_close:
                    modal.on_close()
                
                result.success = True
                result.modal = modal
                result.message = f"Modal '{modal_id}' closed"
            else:
                result.errors.append("Modal not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def confirm_modal(self, modal_id: str) -> ModalResult:
        """
        Confirm a modal.
        
        Args:
            modal_id: Modal ID
            
        Returns:
            ModalResult: Confirm result
        """
        result = ModalResult(success=False)
        
        try:
            modal = self.modals.get(modal_id)
            if modal:
                if modal.on_confirm:
                    modal.on_confirm()
                
                modal.is_open = False
                result.success = True
                result.modal = modal
                result.message = f"Modal '{modal_id}' confirmed"
            else:
                result.errors.append("Modal not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def cancel_modal(self, modal_id: str) -> ModalResult:
        """
        Cancel a modal.
        
        Args:
            modal_id: Modal ID
            
        Returns:
            ModalResult: Cancel result
        """
        result = ModalResult(success=False)
        
        try:
            modal = self.modals.get(modal_id)
            if modal:
                if modal.on_cancel:
                    modal.on_cancel()
                
                modal.is_open = False
                result.success = True
                result.modal = modal
                result.message = f"Modal '{modal_id}' cancelled"
            else:
                result.errors.append("Modal not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_modal_size(self, modal_id: str, size: ModalSize) -> ModalResult:
        """
        Set modal size.
        
        Args:
            modal_id: Modal ID
            size: Modal size
            
        Returns:
            ModalResult: Set result
        """
        result = ModalResult(success=False)
        
        try:
            modal = self.modals.get(modal_id)
            if modal:
                modal.size = size
                result.success = True
                result.modal = modal
                result.message = f"Modal '{modal_id}' size set to {size.value}"
            else:
                result.errors.append("Modal not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_modal_position(self, modal_id: str, position: ModalPosition) -> ModalResult:
        """
        Set modal position.
        
        Args:
            modal_id: Modal ID
            position: Modal position
            
        Returns:
            ModalResult: Set result
        """
        result = ModalResult(success=False)
        
        try:
            modal = self.modals.get(modal_id)
            if modal:
                modal.position = position
                result.success = True
                result.modal = modal
                result.message = f"Modal '{modal_id}' position set to {position.value}"
            else:
                result.errors.append("Modal not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def close_all_modals(self) -> ModalResult:
        """
        Close all modals.
        
        Returns:
            ModalResult: Close result
        """
        result = ModalResult(success=True)
        
        try:
            for modal in self.modals.values():
                modal.is_open = False
                if modal.on_close:
                    modal.on_close()
            
            self.modal_stack.clear()
            result.message = "All modals closed"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def clear_all_modals(self) -> ModalResult:
        """
        Clear all modals.
        
        Returns:
            ModalResult: Clear result
        """
        result = ModalResult(success=True)
        
        try:
            self.modals.clear()
            self.modal_stack.clear()
            result.message = "All modals cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: ModalConfig) -> ModalResult:
        """
        Update modal configuration.
        
        Args:
            config: New configuration
            
        Returns:
            ModalResult: Update result
        """
        result = ModalResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> ModalConfig:
        """
        Get modal configuration.
        
        Returns:
            ModalConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = ModalConfig()
    manager = ModalUIManager(config)
    
    # Modal ekle
    modal = Modal(
        id="",
        type=ModalType.INFO,
        title="Info",
        content="This is an info modal"
    )
    
    result = manager.add_modal(modal)
    
    print(f"Modal added: {result.message}")
    
    # Tüm modalları al
    modals = manager.get_all_modals()
    
    print(f"Total modals: {len(modals)}")
