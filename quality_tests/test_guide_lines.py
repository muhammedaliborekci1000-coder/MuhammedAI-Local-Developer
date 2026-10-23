"""
Quality Test: Guide Lines
Guide lines system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.guide_lines import (
    GuideLineType,
    GuideLineStyle,
    GuideLine,
    GuideLinesConfig,
    GuideLinesResult,
    GuideLinesManager
)


def test_guide_line_type_enum():
    """
    Test: GuideLineType enum.
    """
    print("=" * 70)
    print("TEST: GuideLineType Enum")
    print("=" * 70)
    
    assert GuideLineType.INDENT.value == "indent"
    assert GuideLineType.BRACKET.value == "bracket"
    assert GuideLineType.COLUMN.value == "column"
    assert GuideLineType.EDGE.value == "edge"
    assert GuideLineType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(GuideLineType)}")
    
    print("\n" + "=" * 70)
    print("PASS: GuideLineType enum")
    print("=" * 70)


def test_guide_line_style_enum():
    """
    Test: GuideLineStyle enum.
    """
    print("=" * 70)
    print("TEST: GuideLineStyle Enum")
    print("=" * 70)
    
    assert GuideLineStyle.SOLID.value == "solid"
    assert GuideLineStyle.DASHED.value == "dashed"
    assert GuideLineStyle.DOTTED.value == "dotted"
    assert GuideLineStyle.DOUBLE.value == "double"
    
    print(f"  All enum values verified")
    print(f"  Total styles: {len(GuideLineStyle)}")
    
    print("\n" + "=" * 70)
    print("PASS: GuideLineStyle enum")
    print("=" * 70)


def test_guide_line_dataclass():
    """
    Test: GuideLine dataclass.
    """
    print("=" * 70)
    print("TEST: GuideLine Dataclass")
    print("=" * 70)
    
    guide_line = GuideLine(
        id="guide_1",
        type=GuideLineType.COLUMN,
        column=80,
        style=GuideLineStyle.DASHED
    )
    
    assert guide_line.id == "guide_1", "ID eşleşmeli"
    assert guide_line.type == GuideLineType.COLUMN, "Type eşleşmeli"
    assert guide_line.column == 80, "Column eşleşmeli"
    
    print(f"  ID: {guide_line.id}")
    print(f"  Type: {guide_line.type.value}")
    print(f"  Column: {guide_line.column}")
    
    print("\n" + "=" * 70)
    print("PASS: GuideLine dataclass")
    print("=" * 70)


def test_guide_lines_config_dataclass():
    """
    Test: GuideLinesConfig dataclass.
    """
    print("=" * 70)
    print("TEST: GuideLinesConfig Dataclass")
    print("=" * 70)
    
    config = GuideLinesConfig(
        enabled=True,
        show_indent_guides=True
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.show_indent_guides == True, "Show indent guides eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Show indent guides: {config.show_indent_guides}")
    
    print("\n" + "=" * 70)
    print("PASS: GuideLinesConfig dataclass")
    print("=" * 70)


def test_guide_lines_result_dataclass():
    """
    Test: GuideLinesResult dataclass.
    """
    print("=" * 70)
    print("TEST: GuideLinesResult Dataclass")
    print("=" * 70)
    
    result = GuideLinesResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.guide_lines, list), "Guide lines list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Guide lines: {len(result.guide_lines)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: GuideLinesResult dataclass")
    print("=" * 70)


def test_guide_lines_manager_initialization():
    """
    Test: GuideLinesManager initialization.
    """
    print("=" * 70)
    print("TEST: GuideLinesManager Initialization")
    print("=" * 70)
    
    config = GuideLinesConfig()
    manager = GuideLinesManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.guide_lines) == 0, "Guide lines boş olmalı"
    
    print(f"  Guide lines: {len(manager.guide_lines)}")
    
    print("\n" + "=" * 70)
    print("PASS: GuideLinesManager initialization")
    print("=" * 70)


def test_add_guide_line():
    """
    Test: Add guide line.
    """
    print("=" * 70)
    print("TEST: Add Guide Line")
    print("=" * 70)
    
    manager = GuideLinesManager()
    
    guide_line = GuideLine(
        id="",
        type=GuideLineType.COLUMN,
        column=80
    )
    
    result = manager.add_guide_line(guide_line)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.guide_lines) > 0, "Guide line eklenmeli"
    
    print(f"  Guide line added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add guide line")
    print("=" * 70)


def test_remove_guide_line():
    """
    Test: Remove guide line.
    """
    print("=" * 70)
    print("TEST: Remove Guide Line")
    print("=" * 70)
    
    manager = GuideLinesManager()
    
    guide_line = GuideLine(
        id="",
        type=GuideLineType.COLUMN,
        column=80
    )
    
    result = manager.add_guide_line(guide_line)
    guide_line_id = result.guide_lines[0].id
    
    result = manager.remove_guide_line(guide_line_id)
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert guide_line_id not in manager.guide_lines, "Guide line silinmeli"
    
    print(f"  Guide line removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove guide line")
    print("=" * 70)


def test_get_guide_line():
    """
    Test: Get guide line.
    """
    print("=" * 70)
    print("TEST: Get Guide Line")
    print("=" * 70)
    
    manager = GuideLinesManager()
    
    guide_line = GuideLine(
        id="",
        type=GuideLineType.COLUMN,
        column=80
    )
    
    result = manager.add_guide_line(guide_line)
    guide_line_id = result.guide_lines[0].id
    
    retrieved_guide_line = manager.get_guide_line(guide_line_id)
    
    assert retrieved_guide_line is not None, "Guide line bulunmalı"
    assert retrieved_guide_line.id == guide_line_id, "ID eşleşmeli"
    
    print(f"  Guide line: {retrieved_guide_line.type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get guide line")
    print("=" * 70)


def test_get_all_guide_lines():
    """
    Test: Get all guide lines.
    """
    print("=" * 70)
    print("TEST: Get All Guide Lines")
    print("=" * 70)
    
    manager = GuideLinesManager()
    
    guide_line = GuideLine(
        id="",
        type=GuideLineType.COLUMN,
        column=80
    )
    
    manager.add_guide_line(guide_line)
    guide_lines = manager.get_all_guide_lines()
    
    assert len(guide_lines) > 0, "Guide lines olmalı"
    
    print(f"  Total guide lines: {len(guide_lines)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all guide lines")
    print("=" * 70)


def test_get_guide_lines_by_type():
    """
    Test: Get guide lines by type.
    """
    print("=" * 70)
    print("TEST: Get Guide Lines by Type")
    print("=" * 70)
    
    manager = GuideLinesManager()
    
    guide_line = GuideLine(
        id="",
        type=GuideLineType.COLUMN,
        column=80
    )
    
    manager.add_guide_line(guide_line)
    guide_lines = manager.get_guide_lines_by_type(GuideLineType.COLUMN)
    
    assert len(guide_lines) > 0, "Column guide lines olmalı"
    
    print(f"  Column guide lines: {len(guide_lines)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get guide lines by type")
    print("=" * 70)


def test_generate_indent_guides():
    """
    Test: Generate indent guides.
    """
    print("=" * 70)
    print("TEST: Generate Indent Guides")
    print("=" * 70)
    
    manager = GuideLinesManager()
    
    text = "    indented line"
    result = manager.generate_indent_guides(text)
    
    assert result.success == True, "Generation başarılı olmalı"
    
    print(f"  Indent guides: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate indent guides")
    print("=" * 70)


def test_add_column_guide():
    """
    Test: Add column guide.
    """
    print("=" * 70)
    print("TEST: Add Column Guide")
    print("=" * 70)
    
    config = GuideLinesConfig(show_column_guides=True)
    manager = GuideLinesManager(config)
    
    result = manager.add_column_guide(80)
    
    assert result.success == True, "Column guide başarılı olmalı"
    
    print(f"  Column guide: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add column guide")
    print("=" * 70)


def test_add_edge_guide():
    """
    Test: Add edge guide.
    """
    print("=" * 70)
    print("TEST: Add Edge Guide")
    print("=" * 70)
    
    manager = GuideLinesManager()
    
    result = manager.add_edge_guide("left")
    
    assert result.success == True, "Edge guide başarılı olmalı"
    
    print(f"  Edge guide: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add edge guide")
    print("=" * 70)


def test_set_guide_line_enabled():
    """
    Test: Set guide line enabled.
    """
    print("=" * 70)
    print("TEST: Set Guide Line Enabled")
    print("=" * 70)
    
    manager = GuideLinesManager()
    
    guide_line = GuideLine(
        id="",
        type=GuideLineType.COLUMN,
        column=80
    )
    
    result = manager.add_guide_line(guide_line)
    guide_line_id = result.guide_lines[0].id
    
    result = manager.set_guide_line_enabled(guide_line_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Guide line enabled state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set guide line enabled")
    print("=" * 70)


def test_set_guide_line_visible():
    """
    Test: Set guide line visible.
    """
    print("=" * 70)
    print("TEST: Set Guide Line Visible")
    print("=" * 70)
    
    manager = GuideLinesManager()
    
    guide_line = GuideLine(
        id="",
        type=GuideLineType.COLUMN,
        column=80
    )
    
    result = manager.add_guide_line(guide_line)
    guide_line_id = result.guide_lines[0].id
    
    result = manager.set_guide_line_visible(guide_line_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Guide line visible state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set guide line visible")
    print("=" * 70)


def test_clear_guide_lines():
    """
    Test: Clear guide lines.
    """
    print("=" * 70)
    print("TEST: Clear Guide Lines")
    print("=" * 70)
    
    manager = GuideLinesManager()
    
    guide_line = GuideLine(
        id="",
        type=GuideLineType.COLUMN,
        column=80
    )
    
    manager.add_guide_line(guide_line)
    result = manager.clear_guide_lines()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.guide_lines) == 0, "Guide lines temizlenmeli"
    
    print(f"  Cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear guide lines")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = GuideLinesManager()
    
    new_config = GuideLinesConfig(indent_size=8)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.indent_size == 8, "Config güncellenmeli"
    
    print(f"  Indent size: {manager.config.indent_size}")
    
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
    
    config = GuideLinesConfig(indent_size=8)
    manager = GuideLinesManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.indent_size == 8, "Config eşleşmeli"
    
    print(f"  Indent size: {retrieved_config.indent_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_guide_line_type_enum()
        test2 = test_guide_line_style_enum()
        test3 = test_guide_line_dataclass()
        test4 = test_guide_lines_config_dataclass()
        test5 = test_guide_lines_result_dataclass()
        test6 = test_guide_lines_manager_initialization()
        test7 = test_add_guide_line()
        test8 = test_remove_guide_line()
        test9 = test_get_guide_line()
        test10 = test_get_all_guide_lines()
        test11 = test_get_guide_lines_by_type()
        test12 = test_generate_indent_guides()
        test13 = test_add_column_guide()
        test14 = test_add_edge_guide()
        test15 = test_set_guide_line_enabled()
        test16 = test_set_guide_line_visible()
        test17 = test_clear_guide_lines()
        test18 = test_update_config()
        test19 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"GuideLineType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"GuideLineStyle Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"GuideLine Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"GuideLinesConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"GuideLinesResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"GuideLinesManager Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Add Guide Line: {'PASS' if test7 else 'FAIL'}")
        print(f"Remove Guide Line: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Guide Line: {'PASS' if test9 else 'FAIL'}")
        print(f"Get All Guide Lines: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Guide Lines by Type: {'PASS' if test11 else 'FAIL'}")
        print(f"Generate Indent Guides: {'PASS' if test12 else 'FAIL'}")
        print(f"Add Column Guide: {'PASS' if test13 else 'FAIL'}")
        print(f"Add Edge Guide: {'PASS' if test14 else 'FAIL'}")
        print(f"Set Guide Line Enabled: {'PASS' if test15 else 'FAIL'}")
        print(f"Set Guide Line Visible: {'PASS' if test16 else 'FAIL'}")
        print(f"Clear Guide Lines: {'PASS' if test17 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test19 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19])
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
