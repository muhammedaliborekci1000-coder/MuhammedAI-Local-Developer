"""
Quality Test: Code Editor UI
Code editor UI system testleri for UI module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.ui.code_editor_ui import (
    EditorMode,
    EditorTheme,
    EditorPanel,
    EditorTab,
    EditorState,
    EditorUIConfig,
    EditorUIResult,
    CodeEditorUIManager
)


def test_editor_mode_enum():
    """
    Test: EditorMode enum.
    """
    print("=" * 70)
    print("TEST: EditorMode Enum")
    print("=" * 70)
    
    assert EditorMode.EDIT.value == "edit"
    assert EditorMode.VIEW.value == "view"
    assert EditorMode.DIFF.value == "diff"
    assert EditorMode.MERGE.value == "merge"
    assert EditorMode.DEBUG.value == "debug"
    assert EditorMode.PREVIEW.value == "preview"
    assert EditorMode.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(EditorMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: EditorMode enum")
    print("=" * 70)


def test_editor_theme_enum():
    """
    Test: EditorTheme enum.
    """
    print("=" * 70)
    print("TEST: EditorTheme Enum")
    print("=" * 70)
    
    assert EditorTheme.LIGHT.value == "light"
    assert EditorTheme.DARK.value == "dark"
    assert EditorTheme.HIGH_CONTRAST.value == "high_contrast"
    assert EditorTheme.MONOKAI.value == "monokai"
    assert EditorTheme.SOLARIZED.value == "solarized"
    assert EditorTheme.DRACULA.value == "dracula"
    assert EditorTheme.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total themes: {len(EditorTheme)}")
    
    print("\n" + "=" * 70)
    print("PASS: EditorTheme enum")
    print("=" * 70)


def test_editor_panel_enum():
    """
    Test: EditorPanel enum.
    """
    print("=" * 70)
    print("TEST: EditorPanel Enum")
    print("=" * 70)
    
    assert EditorPanel.MAIN.value == "main"
    assert EditorPanel.SIDEBAR.value == "sidebar"
    assert EditorPanel.BOTTOM.value == "bottom"
    assert EditorPanel.TOP.value == "top"
    assert EditorPanel.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total panels: {len(EditorPanel)}")
    
    print("\n" + "=" * 70)
    print("PASS: EditorPanel enum")
    print("=" * 70)


def test_editor_tab_dataclass():
    """
    Test: EditorTab dataclass.
    """
    print("=" * 70)
    print("TEST: EditorTab Dataclass")
    print("=" * 70)
    
    tab = EditorTab(
        id="tab_1",
        file_path="test.py",
        content="print('Hello')",
        language="python"
    )
    
    assert tab.id == "tab_1", "ID eşleşmeli"
    assert tab.file_path == "test.py", "File path eşleşmeli"
    assert tab.content == "print('Hello')", "Content eşleşmeli"
    assert tab.language == "python", "Language eşleşmeli"
    
    print(f"  ID: {tab.id}")
    print(f"  File path: {tab.file_path}")
    print(f"  Language: {tab.language}")
    
    print("\n" + "=" * 70)
    print("PASS: EditorTab dataclass")
    print("=" * 70)


def test_editor_state_dataclass():
    """
    Test: EditorState dataclass.
    """
    print("=" * 70)
    print("TEST: EditorState Dataclass")
    print("=" * 70)
    
    state = EditorState(
        mode=EditorMode.EDIT,
        theme=EditorTheme.DARK
    )
    
    assert state.mode == EditorMode.EDIT, "Mode eşleşmeli"
    assert state.theme == EditorTheme.DARK, "Theme eşleşmeli"
    assert state.font_size == 14, "Font size eşleşmeli"
    
    print(f"  Mode: {state.mode.value}")
    print(f"  Theme: {state.theme.value}")
    print(f"  Font size: {state.font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: EditorState dataclass")
    print("=" * 70)


def test_editor_ui_config_dataclass():
    """
    Test: EditorUIConfig dataclass.
    """
    print("=" * 70)
    print("TEST: EditorUIConfig Dataclass")
    print("=" * 70)
    
    config = EditorUIConfig(
        enabled=True,
        show_tabs=True
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.show_tabs == True, "Show tabs eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Show tabs: {config.show_tabs}")
    
    print("\n" + "=" * 70)
    print("PASS: EditorUIConfig dataclass")
    print("=" * 70)


def test_editor_ui_result_dataclass():
    """
    Test: EditorUIResult dataclass.
    """
    print("=" * 70)
    print("TEST: EditorUIResult Dataclass")
    print("=" * 70)
    
    result = EditorUIResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.tabs, list), "Tabs list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Tabs: {len(result.tabs)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: EditorUIResult dataclass")
    print("=" * 70)


def test_code_editor_ui_manager_initialization():
    """
    Test: CodeEditorUIManager initialization.
    """
    print("=" * 70)
    print("TEST: CodeEditorUIManager Initialization")
    print("=" * 70)
    
    config = EditorUIConfig()
    manager = CodeEditorUIManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.tabs) == 0, "Tabs boş olmalı"
    assert manager.active_tab_id is None, "Active tab None olmalı"
    
    print(f"  Tabs: {len(manager.tabs)}")
    print(f"  Active tab: {manager.active_tab_id}")
    
    print("\n" + "=" * 70)
    print("PASS: CodeEditorUIManager initialization")
    print("=" * 70)


def test_add_tab():
    """
    Test: Add tab.
    """
    print("=" * 70)
    print("TEST: Add Tab")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    result = manager.add_tab("test.py", "print('Hello')", "python")
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert result.tab is not None, "Tab olmalı"
    assert len(manager.tabs) > 0, "Tab eklenmeli"
    
    print(f"  Tab added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add tab")
    print("=" * 70)


def test_remove_tab():
    """
    Test: Remove tab.
    """
    print("=" * 70)
    print("TEST: Remove Tab")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    result = manager.add_tab("test.py", "print('Hello')", "python")
    tab_id = result.tab.id
    
    result = manager.remove_tab(tab_id)
    
    assert result.success == True, "Silme başarılı olmalı"
    assert tab_id not in manager.tabs, "Tab silinmeli"
    
    print(f"  Tab removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove tab")
    print("=" * 70)


def test_get_tab():
    """
    Test: Get tab.
    """
    print("=" * 70)
    print("TEST: Get Tab")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    result = manager.add_tab("test.py", "print('Hello')", "python")
    tab_id = result.tab.id
    
    retrieved_tab = manager.get_tab(tab_id)
    
    assert retrieved_tab is not None, "Tab bulunmalı"
    assert retrieved_tab.id == tab_id, "ID eşleşmeli"
    
    print(f"  Tab: {retrieved_tab.file_path}")
    
    print("\n" + "=" * 70)
    print("PASS: Get tab")
    print("=" * 70)


def test_get_all_tabs():
    """
    Test: Get all tabs.
    """
    print("=" * 70)
    print("TEST: Get All Tabs")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    manager.add_tab("test1.py", "print('Hello1')", "python")
    manager.add_tab("test2.py", "print('Hello2')", "python")
    
    tabs = manager.get_all_tabs()
    
    assert len(tabs) == 2, "2 tab olmalı"
    
    print(f"  Total tabs: {len(tabs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all tabs")
    print("=" * 70)


def test_get_active_tab():
    """
    Test: Get active tab.
    """
    print("=" * 70)
    print("TEST: Get Active Tab")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    manager.add_tab("test.py", "print('Hello')", "python")
    
    active_tab = manager.get_active_tab()
    
    assert active_tab is not None, "Active tab olmalı"
    assert active_tab.is_active == True, "Active olmalı"
    
    print(f"  Active tab: {active_tab.file_path}")
    
    print("\n" + "=" * 70)
    print("PASS: Get active tab")
    print("=" * 70)


def test_set_active_tab():
    """
    Test: Set active tab.
    """
    print("=" * 70)
    print("TEST: Set Active Tab")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    result1 = manager.add_tab("test1.py", "print('Hello1')", "python")
    result2 = manager.add_tab("test2.py", "print('Hello2')", "python")
    
    tab_id = result1.tab.id
    result = manager.set_active_tab(tab_id)
    
    assert result.success == True, "Set başarılı olmalı"
    assert manager.active_tab_id == tab_id, "Active tab eşleşmeli"
    
    print(f"  Active tab set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set active tab")
    print("=" * 70)


def test_update_tab_content():
    """
    Test: Update tab content.
    """
    print("=" * 70)
    print("TEST: Update Tab Content")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    result = manager.add_tab("test.py", "print('Hello')", "python")
    tab_id = result.tab.id
    
    result = manager.update_tab_content(tab_id, "print('World')")
    
    assert result.success == True, "Update başarılı olmalı"
    assert result.tab.is_modified == True, "Modified olmalı"
    
    print(f"  Tab content updated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update tab content")
    print("=" * 70)


def test_set_cursor_position():
    """
    Test: Set cursor position.
    """
    print("=" * 70)
    print("TEST: Set Cursor Position")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    result = manager.add_tab("test.py", "print('Hello')", "python")
    tab_id = result.tab.id
    
    result = manager.set_cursor_position(tab_id, 5, 10)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Cursor set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set cursor position")
    print("=" * 70)


def test_set_selection():
    """
    Test: Set selection.
    """
    print("=" * 70)
    print("TEST: Set Selection")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    result = manager.add_tab("test.py", "print('Hello')", "python")
    tab_id = result.tab.id
    
    result = manager.set_selection(tab_id, 0, 10)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Selection set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set selection")
    print("=" * 70)


def test_clear_selection():
    """
    Test: Clear selection.
    """
    print("=" * 70)
    print("TEST: Clear Selection")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    result = manager.add_tab("test.py", "print('Hello')", "python")
    tab_id = result.tab.id
    
    manager.set_selection(tab_id, 0, 10)
    result = manager.clear_selection(tab_id)
    
    assert result.success == True, "Clear başarılı olmalı"
    
    print(f"  Selection cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear selection")
    print("=" * 70)


def test_set_editor_mode():
    """
    Test: Set editor mode.
    """
    print("=" * 70)
    print("TEST: Set Editor Mode")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    result = manager.set_editor_mode(EditorMode.VIEW)
    
    assert result.success == True, "Set başarılı olmalı"
    assert manager.state.mode == EditorMode.VIEW, "Mode eşleşmeli"
    
    print(f"  Mode set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set editor mode")
    print("=" * 70)


def test_set_editor_theme():
    """
    Test: Set editor theme.
    """
    print("=" * 70)
    print("TEST: Set Editor Theme")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    result = manager.set_editor_theme(EditorTheme.LIGHT)
    
    assert result.success == True, "Set başarılı olmalı"
    assert manager.state.theme == EditorTheme.LIGHT, "Theme eşleşmeli"
    
    print(f"  Theme set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set editor theme")
    print("=" * 70)


def test_set_font_size():
    """
    Test: Set font size.
    """
    print("=" * 70)
    print("TEST: Set Font Size")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    result = manager.set_font_size(16)
    
    assert result.success == True, "Set başarılı olmalı"
    assert manager.state.font_size == 16, "Font size eşleşmeli"
    
    print(f"  Font size set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set font size")
    print("=" * 70)


def test_set_font_family():
    """
    Test: Set font family.
    """
    print("=" * 70)
    print("TEST: Set Font Family")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    result = manager.set_font_family("Arial")
    
    assert result.success == True, "Set başarılı olmalı"
    assert manager.state.font_family == "Arial", "Font family eşleşmeli"
    
    print(f"  Font family set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set font family")
    print("=" * 70)


def test_toggle_line_numbers():
    """
    Test: Toggle line numbers.
    """
    print("=" * 70)
    print("TEST: Toggle Line Numbers")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    result = manager.toggle_line_numbers()
    
    assert result.success == True, "Toggle başarılı olmalı"
    
    print(f"  Line numbers toggled: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle line numbers")
    print("=" * 70)


def test_toggle_word_wrap():
    """
    Test: Toggle word wrap.
    """
    print("=" * 70)
    print("TEST: Toggle Word Wrap")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    result = manager.toggle_word_wrap()
    
    assert result.success == True, "Toggle başarılı olmalı"
    
    print(f"  Word wrap toggled: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle word wrap")
    print("=" * 70)


def test_toggle_minimap():
    """
    Test: Toggle minimap.
    """
    print("=" * 70)
    print("TEST: Toggle Minimap")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    result = manager.toggle_minimap()
    
    assert result.success == True, "Toggle başarılı olmalı"
    
    print(f"  Minimap toggled: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle minimap")
    print("=" * 70)


def test_clear_all_tabs():
    """
    Test: Clear all tabs.
    """
    print("=" * 70)
    print("TEST: Clear All Tabs")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    manager.add_tab("test.py", "print('Hello')", "python")
    
    result = manager.clear_all_tabs()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.tabs) == 0, "Tabs temizlenmeli"
    
    print(f"  Tabs cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear all tabs")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = CodeEditorUIManager()
    
    new_config = EditorUIConfig(max_tabs=30)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_tabs == 30, "Config güncellenmeli"
    
    print(f"  Max tabs: {manager.config.max_tabs}")
    
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
    
    config = EditorUIConfig(max_tabs=30)
    manager = CodeEditorUIManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_tabs == 30, "Config eşleşmeli"
    
    print(f"  Max tabs: {retrieved_config.max_tabs}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_editor_mode_enum()
        test2 = test_editor_theme_enum()
        test3 = test_editor_panel_enum()
        test4 = test_editor_tab_dataclass()
        test5 = test_editor_state_dataclass()
        test6 = test_editor_ui_config_dataclass()
        test7 = test_editor_ui_result_dataclass()
        test8 = test_code_editor_ui_manager_initialization()
        test9 = test_add_tab()
        test10 = test_remove_tab()
        test11 = test_get_tab()
        test12 = test_get_all_tabs()
        test13 = test_get_active_tab()
        test14 = test_set_active_tab()
        test15 = test_update_tab_content()
        test16 = test_set_cursor_position()
        test17 = test_set_selection()
        test18 = test_clear_selection()
        test19 = test_set_editor_mode()
        test20 = test_set_editor_theme()
        test21 = test_set_font_size()
        test22 = test_set_font_family()
        test23 = test_toggle_line_numbers()
        test24 = test_toggle_word_wrap()
        test25 = test_toggle_minimap()
        test26 = test_clear_all_tabs()
        test27 = test_update_config()
        test28 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"EditorMode Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"EditorTheme Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"EditorPanel Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"EditorTab Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"EditorState Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"EditorUIConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"EditorUIResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"CodeEditorUIManager Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Add Tab: {'PASS' if test9 else 'FAIL'}")
        print(f"Remove Tab: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Tab: {'PASS' if test11 else 'FAIL'}")
        print(f"Get All Tabs: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Active Tab: {'PASS' if test13 else 'FAIL'}")
        print(f"Set Active Tab: {'PASS' if test14 else 'FAIL'}")
        print(f"Update Tab Content: {'PASS' if test15 else 'FAIL'}")
        print(f"Set Cursor Position: {'PASS' if test16 else 'FAIL'}")
        print(f"Set Selection: {'PASS' if test17 else 'FAIL'}")
        print(f"Clear Selection: {'PASS' if test18 else 'FAIL'}")
        print(f"Set Editor Mode: {'PASS' if test19 else 'FAIL'}")
        print(f"Set Editor Theme: {'PASS' if test20 else 'FAIL'}")
        print(f"Set Font Size: {'PASS' if test21 else 'FAIL'}")
        print(f"Set Font Family: {'PASS' if test22 else 'FAIL'}")
        print(f"Toggle Line Numbers: {'PASS' if test23 else 'FAIL'}")
        print(f"Toggle Word Wrap: {'PASS' if test24 else 'FAIL'}")
        print(f"Toggle Minimap: {'PASS' if test25 else 'FAIL'}")
        print(f"Clear All Tabs: {'PASS' if test26 else 'FAIL'}")
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
