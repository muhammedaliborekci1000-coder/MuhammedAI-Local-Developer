"""
Quality Test: Component Library
Component library system testleri for UI module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.ui.component_library import (
    ComponentType,
    ComponentCategory,
    ComponentVariant,
    Component,
    ComponentTemplate,
    ComponentLibraryConfig,
    ComponentLibraryResult,
    ComponentLibraryManager
)


def test_component_type_enum():
    """
    Test: ComponentType enum.
    """
    print("=" * 70)
    print("TEST: ComponentType Enum")
    print("=" * 70)
    
    assert ComponentType.BUTTON.value == "button"
    assert ComponentType.INPUT.value == "input"
    assert ComponentType.SELECT.value == "select"
    assert ComponentType.CHECKBOX.value == "checkbox"
    assert ComponentType.RADIO.value == "radio"
    assert ComponentType.TOGGLE.value == "toggle"
    assert ComponentType.SLIDER.value == "slider"
    assert ComponentType.PROGRESS.value == "progress"
    assert ComponentType.SPINNER.value == "spinner"
    assert ComponentType.BADGE.value == "badge"
    assert ComponentType.TAG.value == "tag"
    assert ComponentType.CARD.value == "card"
    assert ComponentType.ALERT.value == "alert"
    assert ComponentType.MODAL.value == "modal"
    assert ComponentType.DROPDOWN.value == "dropdown"
    assert ComponentType.MENU.value == "menu"
    assert ComponentType.TABLE.value == "table"
    assert ComponentType.LIST.value == "list"
    assert ComponentType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(ComponentType)}")
    
    print("\n" + "=" * 70)
    print("PASS: ComponentType enum")
    print("=" * 70)


def test_component_category_enum():
    """
    Test: ComponentCategory enum.
    """
    print("=" * 70)
    print("TEST: ComponentCategory Enum")
    print("=" * 70)
    
    assert ComponentCategory.FORM.value == "form"
    assert ComponentCategory.NAVIGATION.value == "navigation"
    assert ComponentCategory.DATA_DISPLAY.value == "data_display"
    assert ComponentCategory.FEEDBACK.value == "feedback"
    assert ComponentCategory.LAYOUT.value == "layout"
    assert ComponentCategory.TYPOGRAPHY.value == "typography"
    assert ComponentCategory.MEDIA.value == "media"
    assert ComponentCategory.OVERLAY.value == "overlay"
    assert ComponentCategory.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total categories: {len(ComponentCategory)}")
    
    print("\n" + "=" * 70)
    print("PASS: ComponentCategory enum")
    print("=" * 70)


def test_component_variant_enum():
    """
    Test: ComponentVariant enum.
    """
    print("=" * 70)
    print("TEST: ComponentVariant Enum")
    print("=" * 70)
    
    assert ComponentVariant.PRIMARY.value == "primary"
    assert ComponentVariant.SECONDARY.value == "secondary"
    assert ComponentVariant.SUCCESS.value == "success"
    assert ComponentVariant.DANGER.value == "danger"
    assert ComponentVariant.WARNING.value == "warning"
    assert ComponentVariant.INFO.value == "info"
    assert ComponentVariant.LIGHT.value == "light"
    assert ComponentVariant.DARK.value == "dark"
    assert ComponentVariant.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total variants: {len(ComponentVariant)}")
    
    print("\n" + "=" * 70)
    print("PASS: ComponentVariant enum")
    print("=" * 70)


def test_component_dataclass():
    """
    Test: Component dataclass.
    """
    print("=" * 70)
    print("TEST: Component Dataclass")
    print("=" * 70)
    
    component = Component(
        id="component_1",
        type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        name="Submit Button",
        description="A submit button"
    )
    
    assert component.id == "component_1", "ID eşleşmeli"
    assert component.type == ComponentType.BUTTON, "Type eşleşmeli"
    assert component.category == ComponentCategory.FORM, "Category eşleşmeli"
    assert component.name == "Submit Button", "Name eşleşmeli"
    
    print(f"  ID: {component.id}")
    print(f"  Type: {component.type.value}")
    print(f"  Category: {component.category.value}")
    print(f"  Name: {component.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Component dataclass")
    print("=" * 70)


def test_component_template_dataclass():
    """
    Test: ComponentTemplate dataclass.
    """
    print("=" * 70)
    print("TEST: ComponentTemplate Dataclass")
    print("=" * 70)
    
    template = ComponentTemplate(
        id="template_1",
        name="Button Template",
        component_type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        template="<button>{{text}}</button>"
    )
    
    assert template.id == "template_1", "ID eşleşmeli"
    assert template.name == "Button Template", "Name eşleşmeli"
    assert template.component_type == ComponentType.BUTTON, "Type eşleşmeli"
    
    print(f"  ID: {template.id}")
    print(f"  Name: {template.name}")
    print(f"  Type: {template.component_type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: ComponentTemplate dataclass")
    print("=" * 70)


def test_component_library_config_dataclass():
    """
    Test: ComponentLibraryConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ComponentLibraryConfig Dataclass")
    print("=" * 70)
    
    config = ComponentLibraryConfig(
        enabled=True,
        enable_search=True
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.enable_search == True, "Enable search eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Enable search: {config.enable_search}")
    
    print("\n" + "=" * 70)
    print("PASS: ComponentLibraryConfig dataclass")
    print("=" * 70)


def test_component_library_result_dataclass():
    """
    Test: ComponentLibraryResult dataclass.
    """
    print("=" * 70)
    print("TEST: ComponentLibraryResult Dataclass")
    print("=" * 70)
    
    result = ComponentLibraryResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.components, list), "Components list olmalı"
    assert isinstance(result.templates, list), "Templates list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Components: {len(result.components)}")
    print(f"  Templates: {len(result.templates)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ComponentLibraryResult dataclass")
    print("=" * 70)


def test_component_library_manager_initialization():
    """
    Test: ComponentLibraryManager initialization.
    """
    print("=" * 70)
    print("TEST: ComponentLibraryManager Initialization")
    print("=" * 70)
    
    config = ComponentLibraryConfig()
    manager = ComponentLibraryManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.components) == 0, "Components boş olmalı"
    assert len(manager.templates) == 0, "Templates boş olmalı"
    
    print(f"  Components: {len(manager.components)}")
    print(f"  Templates: {len(manager.templates)}")
    
    print("\n" + "=" * 70)
    print("PASS: ComponentLibraryManager initialization")
    print("=" * 70)


def test_add_component():
    """
    Test: Add component.
    """
    print("=" * 70)
    print("TEST: Add Component")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    component = Component(
        id="",
        type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        name="Submit Button",
        description="A submit button"
    )
    
    result = manager.add_component(component)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert result.component is not None, "Component olmalı"
    assert len(manager.components) > 0, "Component eklenmeli"
    
    print(f"  Component added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add component")
    print("=" * 70)


def test_remove_component():
    """
    Test: Remove component.
    """
    print("=" * 70)
    print("TEST: Remove Component")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    component = Component(
        id="",
        type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        name="Submit Button",
        description="A submit button"
    )
    
    result = manager.add_component(component)
    component_id = result.component.id
    
    result = manager.remove_component(component_id)
    
    assert result.success == True, "Silme başarılı olmalı"
    assert component_id not in manager.components, "Component silinmeli"
    
    print(f"  Component removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove component")
    print("=" * 70)


def test_get_component():
    """
    Test: Get component.
    """
    print("=" * 70)
    print("TEST: Get Component")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    component = Component(
        id="",
        type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        name="Submit Button",
        description="A submit button"
    )
    
    result = manager.add_component(component)
    component_id = result.component.id
    
    retrieved_component = manager.get_component(component_id)
    
    assert retrieved_component is not None, "Component bulunmalı"
    assert retrieved_component.id == component_id, "ID eşleşmeli"
    
    print(f"  Component: {retrieved_component.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get component")
    print("=" * 70)


def test_get_all_components():
    """
    Test: Get all components.
    """
    print("=" * 70)
    print("TEST: Get All Components")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    component = Component(
        id="",
        type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        name="Submit Button",
        description="A submit button"
    )
    
    manager.add_component(component)
    components = manager.get_all_components()
    
    assert len(components) > 0, "Components olmalı"
    
    print(f"  Total components: {len(components)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all components")
    print("=" * 70)


def test_get_components_by_type():
    """
    Test: Get components by type.
    """
    print("=" * 70)
    print("TEST: Get Components by Type")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    component = Component(
        id="",
        type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        name="Submit Button",
        description="A submit button"
    )
    
    manager.add_component(component)
    components = manager.get_components_by_type(ComponentType.BUTTON)
    
    assert len(components) > 0, "Button components olmalı"
    
    print(f"  Button components: {len(components)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get components by type")
    print("=" * 70)


def test_get_components_by_category():
    """
    Test: Get components by category.
    """
    print("=" * 70)
    print("TEST: Get Components by Category")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    component = Component(
        id="",
        type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        name="Submit Button",
        description="A submit button"
    )
    
    manager.add_component(component)
    components = manager.get_components_by_category(ComponentCategory.FORM)
    
    assert len(components) > 0, "Form components olmalı"
    
    print(f"  Form components: {len(components)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get components by category")
    print("=" * 70)


def test_search_components():
    """
    Test: Search components.
    """
    print("=" * 70)
    print("TEST: Search Components")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    component = Component(
        id="",
        type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        name="Submit Button",
        description="A submit button"
    )
    
    manager.add_component(component)
    components = manager.search_components("submit")
    
    assert len(components) > 0, "Arama sonucu olmalı"
    
    print(f"  Search results: {len(components)}")
    
    print("\n" + "=" * 70)
    print("PASS: Search components")
    print("=" * 70)


def test_add_template():
    """
    Test: Add template.
    """
    print("=" * 70)
    print("TEST: Add Template")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    template = ComponentTemplate(
        id="",
        name="Button Template",
        component_type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        template="<button>{{text}}</button>"
    )
    
    result = manager.add_template(template)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert result.template is not None, "Template olmalı"
    assert len(manager.templates) > 0, "Template eklenmeli"
    
    print(f"  Template added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add template")
    print("=" * 70)


def test_remove_template():
    """
    Test: Remove template.
    """
    print("=" * 70)
    print("TEST: Remove Template")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    template = ComponentTemplate(
        id="",
        name="Button Template",
        component_type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        template="<button>{{text}}</button>"
    )
    
    result = manager.add_template(template)
    template_id = result.template.id
    
    result = manager.remove_template(template_id)
    
    assert result.success == True, "Silme başarılı olmalı"
    assert template_id not in manager.templates, "Template silinmeli"
    
    print(f"  Template removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove template")
    print("=" * 70)


def test_get_template():
    """
    Test: Get template.
    """
    print("=" * 70)
    print("TEST: Get Template")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    template = ComponentTemplate(
        id="",
        name="Button Template",
        component_type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        template="<button>{{text}}</button>"
    )
    
    result = manager.add_template(template)
    template_id = result.template.id
    
    retrieved_template = manager.get_template(template_id)
    
    assert retrieved_template is not None, "Template bulunmalı"
    assert retrieved_template.id == template_id, "ID eşleşmeli"
    
    print(f"  Template: {retrieved_template.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get template")
    print("=" * 70)


def test_get_all_templates():
    """
    Test: Get all templates.
    """
    print("=" * 70)
    print("TEST: Get All Templates")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    template = ComponentTemplate(
        id="",
        name="Button Template",
        component_type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        template="<button>{{text}}</button>"
    )
    
    manager.add_template(template)
    templates = manager.get_all_templates()
    
    assert len(templates) > 0, "Templates olmalı"
    
    print(f"  Total templates: {len(templates)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all templates")
    print("=" * 70)


def test_get_templates_by_type():
    """
    Test: Get templates by type.
    """
    print("=" * 70)
    print("TEST: Get Templates by Type")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    template = ComponentTemplate(
        id="",
        name="Button Template",
        component_type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        template="<button>{{text}}</button>"
    )
    
    manager.add_template(template)
    templates = manager.get_templates_by_type(ComponentType.BUTTON)
    
    assert len(templates) > 0, "Button templates olmalı"
    
    print(f"  Button templates: {len(templates)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get templates by type")
    print("=" * 70)


def test_create_component_from_template():
    """
    Test: Create component from template.
    """
    print("=" * 70)
    print("TEST: Create Component from Template")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    template = ComponentTemplate(
        id="",
        name="Button Template",
        component_type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        template="<button>{{text}}</button>",
        default_props={"text": "Submit"}
    )
    
    result = manager.add_template(template)
    template_id = result.template.id
    
    result = manager.create_component_from_template(template_id, {"text": "Click Me"})
    
    assert result.success == True, "Create başarılı olmalı"
    
    print(f"  Component created: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Create component from template")
    print("=" * 70)


def test_set_component_enabled():
    """
    Test: Set component enabled.
    """
    print("=" * 70)
    print("TEST: Set Component Enabled")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    component = Component(
        id="",
        type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        name="Submit Button",
        description="A submit button"
    )
    
    result = manager.add_component(component)
    component_id = result.component.id
    
    result = manager.set_component_enabled(component_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Component enabled state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set component enabled")
    print("=" * 70)


def test_set_component_visible():
    """
    Test: Set component visible.
    """
    print("=" * 70)
    print("TEST: Set Component Visible")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    component = Component(
        id="",
        type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        name="Submit Button",
        description="A submit button"
    )
    
    result = manager.add_component(component)
    component_id = result.component.id
    
    result = manager.set_component_visible(component_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Component visible state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set component visible")
    print("=" * 70)


def test_update_component_props():
    """
    Test: Update component props.
    """
    print("=" * 70)
    print("TEST: Update Component Props")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    component = Component(
        id="",
        type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        name="Submit Button",
        description="A submit button"
    )
    
    result = manager.add_component(component)
    component_id = result.component.id
    
    result = manager.update_component_props(component_id, {"text": "Submit"})
    
    assert result.success == True, "Update başarılı olmalı"
    
    print(f"  Component props updated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update component props")
    print("=" * 70)


def test_clear_all_components():
    """
    Test: Clear all components.
    """
    print("=" * 70)
    print("TEST: Clear All Components")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    component = Component(
        id="",
        type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        name="Submit Button",
        description="A submit button"
    )
    
    manager.add_component(component)
    result = manager.clear_all_components()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.components) == 0, "Components temizlenmeli"
    
    print(f"  All components cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear all components")
    print("=" * 70)


def test_clear_all_templates():
    """
    Test: Clear all templates.
    """
    print("=" * 70)
    print("TEST: Clear All Templates")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    template = ComponentTemplate(
        id="",
        name="Button Template",
        component_type=ComponentType.BUTTON,
        category=ComponentCategory.FORM,
        template="<button>{{text}}</button>"
    )
    
    manager.add_template(template)
    result = manager.clear_all_templates()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.templates) == 0, "Templates temizlenmeli"
    
    print(f"  All templates cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear all templates")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = ComponentLibraryManager()
    
    new_config = ComponentLibraryConfig(max_components=200)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_components == 200, "Config güncellenmeli"
    
    print(f"  Max components: {manager.config.max_components}")
    
    print("\n" + "=" * 70)
    print("PASS: Update config")
    print("=" * 70)


def test_get_config():
    """
    Test: Get config.
    """
    print("=" * 70)
    print("TEST: Get Config")
    print("=" * 70)
    
    config = ComponentLibraryConfig(max_components=200)
    manager = ComponentLibraryManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_components == 200, "Config eşleşmeli"
    
    print(f"  Max components: {retrieved_config.max_components}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_component_type_enum()
        test2 = test_component_category_enum()
        test3 = test_component_variant_enum()
        test4 = test_component_dataclass()
        test5 = test_component_template_dataclass()
        test6 = test_component_library_config_dataclass()
        test7 = test_component_library_result_dataclass()
        test8 = test_component_library_manager_initialization()
        test9 = test_add_component()
        test10 = test_remove_component()
        test11 = test_get_component()
        test12 = test_get_all_components()
        test13 = test_get_components_by_type()
        test14 = test_get_components_by_category()
        test15 = test_search_components()
        test16 = test_add_template()
        test17 = test_remove_template()
        test18 = test_get_template()
        test19 = test_get_all_templates()
        test20 = test_get_templates_by_type()
        test21 = test_create_component_from_template()
        test22 = test_set_component_enabled()
        test23 = test_set_component_visible()
        test24 = test_update_component_props()
        test25 = test_clear_all_components()
        test26 = test_clear_all_templates()
        test27 = test_update_config()
        test28 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"ComponentType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"ComponentCategory Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"ComponentVariant Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"Component Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"ComponentTemplate Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"ComponentLibraryConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"ComponentLibraryResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"ComponentLibraryManager Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Add Component: {'PASS' if test9 else 'FAIL'}")
        print(f"Remove Component: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Component: {'PASS' if test11 else 'FAIL'}")
        print(f"Get All Components: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Components by Type: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Components by Category: {'PASS' if test14 else 'FAIL'}")
        print(f"Search Components: {'PASS' if test15 else 'FAIL'}")
        print(f"Add Template: {'PASS' if test16 else 'FAIL'}")
        print(f"Remove Template: {'PASS' if test17 else 'FAIL'}")
        print(f"Get Template: {'PASS' if test18 else 'FAIL'}")
        print(f"Get All Templates: {'PASS' if test19 else 'FAIL'}")
        print(f"Get Templates by Type: {'PASS' if test20 else 'FAIL'}")
        print(f"Create Component from Template: {'PASS' if test21 else 'FAIL'}")
        print(f"Set Component Enabled: {'PASS' if test22 else 'FAIL'}")
        print(f"Set Component Visible: {'PASS' if test23 else 'FAIL'}")
        print(f"Update Component Props: {'PASS' if test24 else 'FAIL'}")
        print(f"Clear All Components: {'PASS' if test25 else 'FAIL'}")
        print(f"Clear All Templates: {'PASS' if test26 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test27 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test28 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25, test26, test27, test28])
        print(f"\nTOPLAM: {'PASS' if all_passed else 'FAIL'}")
        print("=" * 70)
        
        sys.exit(0 if all_passed else 1)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
