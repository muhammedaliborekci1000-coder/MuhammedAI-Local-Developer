"""
MuhammedAI Local Developer - Component Library
Component library system for web UI.
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from enum import Enum


class ComponentType(Enum):
    """Component type."""
    BUTTON = "button"
    INPUT = "input"
    SELECT = "select"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    TOGGLE = "toggle"
    SLIDER = "slider"
    PROGRESS = "progress"
    SPINNER = "spinner"
    BADGE = "badge"
    TAG = "tag"
    CARD = "card"
    ALERT = "alert"
    MODAL = "modal"
    DROPDOWN = "dropdown"
    MENU = "menu"
    TABLE = "table"
    LIST = "list"
    CUSTOM = "custom"


class ComponentCategory(Enum):
    """Component category."""
    FORM = "form"
    NAVIGATION = "navigation"
    DATA_DISPLAY = "data_display"
    FEEDBACK = "feedback"
    LAYOUT = "layout"
    TYPOGRAPHY = "typography"
    MEDIA = "media"
    OVERLAY = "overlay"
    CUSTOM = "custom"


class ComponentVariant(Enum):
    """Component variant."""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    DANGER = "danger"
    WARNING = "warning"
    INFO = "info"
    LIGHT = "light"
    DARK = "dark"
    CUSTOM = "custom"


@dataclass
class Component:
    """Component."""
    id: str
    type: ComponentType
    category: ComponentCategory
    name: str
    description: str
    variant: ComponentVariant = ComponentVariant.PRIMARY
    is_enabled: bool = True
    is_visible: bool = True
    props: Dict[str, Any] = field(default_factory=dict)
    events: Dict[str, Callable] = field(default_factory=dict)
    styles: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComponentTemplate:
    """Component template."""
    id: str
    name: str
    component_type: ComponentType
    category: ComponentCategory
    template: str
    default_props: Dict[str, Any] = field(default_factory=dict)
    is_public: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComponentLibraryConfig:
    """Component library configuration."""
    enabled: bool = True
    enable_caching: bool = True
    enable_search: bool = True
    enable_filtering: bool = True
    enable_sorting: bool = True
    max_components: int = 100
    max_templates: int = 50
    enable_custom_components: bool = True
    enable_import_export: bool = True


@dataclass
class ComponentLibraryResult:
    """Component library result."""
    success: bool
    component: Optional[Component] = None
    components: List[Component] = field(default_factory=list)
    template: Optional[ComponentTemplate] = None
    templates: List[ComponentTemplate] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class ComponentLibraryManager:
    """
    Component library manager.
    
    Özellikler:
    - Component types (button, input, select, checkbox, radio, toggle, slider, progress, spinner, badge, tag, card, alert, modal, dropdown, menu, table, list)
    - Component categories (form, navigation, data_display, feedback, layout, typography, media, overlay)
    - Component variants (primary, secondary, success, danger, warning, info, light, dark)
    - Component templates
    - Component props
    - Component events
    - Component styles
    - Search
    - Filter
    - Sort
    - Import/Export
    - Custom components
    """
    
    def __init__(self, config: Optional[ComponentLibraryConfig] = None):
        """
        Initialize component library manager.
        
        Args:
            config: Component library configuration
        """
        self.config = config or ComponentLibraryConfig()
        self.components: Dict[str, Component] = {}
        self.templates: Dict[str, ComponentTemplate] = {}
        self.component_id_counter = 0
        self.template_id_counter = 0
        self._next_component_id()
        self._next_template_id()
    
    def _next_component_id(self) -> str:
        """
        Generate next component ID.
        
        Returns:
            str: Component ID
        """
        self.component_id_counter += 1
        return f"component_{self.component_id_counter}"
    
    def _next_template_id(self) -> str:
        """
        Generate next template ID.
        
        Returns:
            str: Template ID
        """
        self.template_id_counter += 1
        return f"template_{self.template_id_counter}"
    
    def add_component(self, component: Component) -> ComponentLibraryResult:
        """
        Add a component.
        
        Args:
            component: Component to add
            
        Returns:
            ComponentLibraryResult: Add result
        """
        result = ComponentLibraryResult(success=True)
        
        try:
            if len(self.components) >= self.config.max_components:
                result.errors.append(f"Maximum components reached (max {self.config.max_components})")
                result.success = False
                return result
            
            if not component.id:
                component.id = self._next_component_id()
            
            self.components[component.id] = component
            result.component = component
            result.components = self.get_all_components()
            result.message = f"Component '{component.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_component(self, component_id: str) -> ComponentLibraryResult:
        """
        Remove a component.
        
        Args:
            component_id: Component ID
            
        Returns:
            ComponentLibraryResult: Remove result
        """
        result = ComponentLibraryResult(success=False)
        
        try:
            if component_id in self.components:
                del self.components[component_id]
                result.success = True
                result.components = self.get_all_components()
                result.message = f"Component '{component_id}' removed"
            else:
                result.errors.append("Component not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_component(self, component_id: str) -> Optional[Component]:
        """
        Get component by ID.
        
        Args:
            component_id: Component ID
            
        Returns:
            Optional[Component]: Component
        """
        return self.components.get(component_id)
    
    def get_all_components(self) -> List[Component]:
        """
        Get all components.
        
        Returns:
            List[Component]: All components
        """
        return list(self.components.values())
    
    def get_components_by_type(self, component_type: ComponentType) -> List[Component]:
        """
        Get components by type.
        
        Args:
            component_type: Component type
            
        Returns:
            List[Component]: Components
        """
        return [c for c in self.components.values() if c.type == component_type]
    
    def get_components_by_category(self, category: ComponentCategory) -> List[Component]:
        """
        Get components by category.
        
        Args:
            category: Component category
            
        Returns:
            List[Component]: Components
        """
        return [c for c in self.components.values() if c.category == category]
    
    def search_components(self, query: str) -> List[Component]:
        """
        Search components by name or description.
        
        Args:
            query: Search query
            
        Returns:
            List[Component]: Matching components
        """
        if not self.config.enable_search:
            return []
        
        query_lower = query.lower()
        return [
            c for c in self.components.values()
            if query_lower in c.name.lower() or query_lower in c.description.lower()
        ]
    
    def add_template(self, template: ComponentTemplate) -> ComponentLibraryResult:
        """
        Add a component template.
        
        Args:
            template: Template to add
            
        Returns:
            ComponentLibraryResult: Add result
        """
        result = ComponentLibraryResult(success=True)
        
        try:
            if len(self.templates) >= self.config.max_templates:
                result.errors.append(f"Maximum templates reached (max {self.config.max_templates})")
                result.success = False
                return result
            
            if not template.id:
                template.id = self._next_template_id()
            
            self.templates[template.id] = template
            result.template = template
            result.templates = self.get_all_templates()
            result.message = f"Template '{template.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_template(self, template_id: str) -> ComponentLibraryResult:
        """
        Remove a template.
        
        Args:
            template_id: Template ID
            
        Returns:
            ComponentLibraryResult: Remove result
        """
        result = ComponentLibraryResult(success=False)
        
        try:
            if template_id in self.templates:
                del self.templates[template_id]
                result.success = True
                result.templates = self.get_all_templates()
                result.message = f"Template '{template_id}' removed"
            else:
                result.errors.append("Template not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_template(self, template_id: str) -> Optional[ComponentTemplate]:
        """
        Get template by ID.
        
        Args:
            template_id: Template ID
            
        Returns:
            Optional[ComponentTemplate]: Template
        """
        return self.templates.get(template_id)
    
    def get_all_templates(self) -> List[ComponentTemplate]:
        """
        Get all templates.
        
        Returns:
            List[ComponentTemplate]: All templates
        """
        return list(self.templates.values())
    
    def get_templates_by_type(self, component_type: ComponentType) -> List[ComponentTemplate]:
        """
        Get templates by component type.
        
        Args:
            component_type: Component type
            
        Returns:
            List[ComponentTemplate]: Templates
        """
        return [t for t in self.templates.values() if t.component_type == component_type]
    
    def create_component_from_template(self, template_id: str, props: Optional[Dict[str, Any]] = None) -> ComponentLibraryResult:
        """
        Create a component from template.
        
        Args:
            template_id: Template ID
            props: Component props
            
        Returns:
            ComponentLibraryResult: Create result
        """
        result = ComponentLibraryResult(success=False)
        
        try:
            template = self.templates.get(template_id)
            if not template:
                result.errors.append("Template not found")
                return result
            
            merged_props = {**template.default_props}
            if props:
                merged_props.update(props)
            
            component = Component(
                id=self._next_component_id(),
                type=template.component_type,
                category=template.category,
                name=f"{template.name}_instance",
                description=f"Instance of {template.name}",
                props=merged_props
            )
            
            self.components[component.id] = component
            result.component = component
            result.components = self.get_all_components()
            result.success = True
            result.message = f"Component created from template '{template_id}'"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_component_enabled(self, component_id: str, enabled: bool) -> ComponentLibraryResult:
        """
        Set component enabled state.
        
        Args:
            component_id: Component ID
            enabled: Enabled state
            
        Returns:
            ComponentLibraryResult: Set result
        """
        result = ComponentLibraryResult(success=False)
        
        try:
            component = self.components.get(component_id)
            if component:
                component.is_enabled = enabled
                result.success = True
                result.component = component
                result.message = f"Component '{component_id}' {'enabled' if enabled else 'disabled'}"
            else:
                result.errors.append("Component not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_component_visible(self, component_id: str, visible: bool) -> ComponentLibraryResult:
        """
        Set component visible state.
        
        Args:
            component_id: Component ID
            visible: Visible state
            
        Returns:
            ComponentLibraryResult: Set result
        """
        result = ComponentLibraryResult(success=False)
        
        try:
            component = self.components.get(component_id)
            if component:
                component.is_visible = visible
                result.success = True
                result.component = component
                result.message = f"Component '{component_id}' {'visible' if visible else 'hidden'}"
            else:
                result.errors.append("Component not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_component_props(self, component_id: str, props: Dict[str, Any]) -> ComponentLibraryResult:
        """
        Update component props.
        
        Args:
            component_id: Component ID
            props: Props to update
            
        Returns:
            ComponentLibraryResult: Update result
        """
        result = ComponentLibraryResult(success=False)
        
        try:
            component = self.components.get(component_id)
            if component:
                component.props.update(props)
                result.success = True
                result.component = component
                result.message = f"Component '{component_id}' props updated"
            else:
                result.errors.append("Component not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clear_all_components(self) -> ComponentLibraryResult:
        """
        Clear all components.
        
        Returns:
            ComponentLibraryResult: Clear result
        """
        result = ComponentLibraryResult(success=True)
        
        try:
            self.components.clear()
            result.message = "All components cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def clear_all_templates(self) -> ComponentLibraryResult:
        """
        Clear all templates.
        
        Returns:
            ComponentLibraryResult: Clear result
        """
        result = ComponentLibraryResult(success=True)
        
        try:
            self.templates.clear()
            result.message = "All templates cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: ComponentLibraryConfig) -> ComponentLibraryResult:
        """
        Update component library configuration.
        
        Args:
            config: New configuration
            
        Returns:
            ComponentLibraryResult: Update result
        """
        result = ComponentLibraryResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> ComponentLibraryConfig:
        """
        Get component library configuration.
        
        Returns:
            ComponentLibraryConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = ComponentLibraryConfig()
    manager = ComponentLibraryManager(config)
    
    # Component ekle
    component = Component(
        id="",
        type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        name="Submit Button",
        description="A submit button"
    )
    
    result = manager.add_component(component)
    
    print(f"Component added: {result.message}")
    
    # Tüm component'ları al
    components = manager.get_all_components()
    
    print(f"Total components: {len(components)}")
