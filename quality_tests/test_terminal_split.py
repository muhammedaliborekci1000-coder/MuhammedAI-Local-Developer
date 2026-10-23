"""
Quality Test: Terminal Split
Terminal split system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_split import (
    TerminalSplitEngine,
    SplitDirection,
    SplitRatio,
    SplitConfig,
    Split,
    SplitResult
)


def test_split_panel():
    """
    Test: Split panel.
    """
    print("=" * 70)
    print("TEST: Split Panel")
    print("=" * 70)
    
    engine = TerminalSplitEngine()
    result = engine.split_panel("parent_1", "child_1")
    
    assert result.success, "Bölme başarılı olmalı"
    assert result.split_id is not None, "Split ID olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Split ID: {result.split_id}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Split panel")
    print("=" * 70)


def test_split_panel_with_direction():
    """
    Test: Split panel with direction.
    """
    print("=" * 70)
    print("TEST: Split Panel With Direction")
    print("=" * 70)
    
    engine = TerminalSplitEngine()
    result = engine.split_panel("parent_1", "child_1", SplitDirection.VERTICAL)
    
    assert result.success, "Bölme başarılı olmalı"
    assert result.split_id is not None, "Split ID olmalı"
    
    split = engine.get_split(result.split_id)
    assert split.direction == SplitDirection.VERTICAL, "Yön eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Direction: {split.direction.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Split panel with direction")
    print("=" * 70)


def test_split_panel_with_ratio():
    """
    Test: Split panel with ratio.
    """
    print("=" * 70)
    print("TEST: Split Panel With Ratio")
    print("=" * 70)
    
    engine = TerminalSplitEngine()
    result = engine.split_panel("parent_1", "child_1", ratio=SplitRatio.TOP_HEAVY)
    
    assert result.success, "Bölme başarılı olmalı"
    
    split = engine.get_split(result.split_id)
    assert split.ratio == SplitRatio.TOP_HEAVY, "Oran eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Ratio: {split.ratio.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Split panel with ratio")
    print("=" * 70)


def test_split_panel_with_custom_ratio():
    """
    Test: Split panel with custom ratio.
    """
    print("=" * 70)
    print("TEST: Split Panel With Custom Ratio")
    print("=" * 70)
    
    engine = TerminalSplitEngine()
    result = engine.split_panel("parent_1", "child_1", custom_ratio=0.7)
    
    assert result.success, "Bölme başarılı olmalı"
    
    split = engine.get_split(result.split_id)
    assert split.custom_ratio == 0.7, "Özel oran eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Custom ratio: {split.custom_ratio}")
    
    print("\n" + "=" * 70)
    print("PASS: Split panel with custom ratio")
    print("=" * 70)


def test_merge_split():
    """
    Test: Merge split.
    """
    print("=" * 70)
    print("TEST: Merge Split")
    print("=" * 70)
    
    engine = TerminalSplitEngine()
    split_result = engine.split_panel("parent_1", "child_1")
    
    result = engine.merge_split(split_result.split_id)
    
    assert result.success, "Birleştirme başarılı olmalı"
    assert engine.get_split(split_result.split_id) is None, "Split silinmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Merge split")
    print("=" * 70)


def test_resize_split():
    """
    Test: Resize split.
    """
    print("=" * 70)
    print("TEST: Resize Split")
    print("=" * 70)
    
    engine = TerminalSplitEngine()
    split_result = engine.split_panel("parent_1", "child_1")
    
    result = engine.resize_split(split_result.split_id, 0.8)
    
    assert result.success, "Yeniden boyutlandırma başarılı olmalı"
    
    split = engine.get_split(split_result.split_id)
    assert split.custom_ratio == 0.8, "Oran değişmeli"
    
    print(f"  Success: {result.success}")
    print(f"  New ratio: {split.custom_ratio}")
    
    print("\n" + "=" * 70)
    print("PASS: Resize split")
    print("=" * 70)


def test_change_direction():
    """
    Test: Change direction.
    """
    print("=" * 70)
    print("TEST: Change Direction")
    print("=" * 70)
    
    engine = TerminalSplitEngine()
    split_result = engine.split_panel("parent_1", "child_1")
    
    result = engine.change_direction(split_result.split_id, SplitDirection.VERTICAL)
    
    assert result.success, "Yön değiştirme başarılı olmalı"
    
    split = engine.get_split(split_result.split_id)
    assert split.direction == SplitDirection.VERTICAL, "Yön değişmeli"
    
    print(f"  Success: {result.success}")
    print(f"  New direction: {split.direction.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Change direction")
    print("=" * 70)


def test_get_split():
    """
    Test: Get split.
    """
    print("=" * 70)
    print("TEST: Get Split")
    print("=" * 70)
    
    engine = TerminalSplitEngine()
    split_result = engine.split_panel("parent_1", "child_1")
    
    split = engine.get_split(split_result.split_id)
    
    assert split is not None, "Split olmalı"
    assert split.parent_panel_id == "parent_1", "Parent ID eşleşmeli"
    
    print(f"  Split ID: {split.id}")
    print(f"  Parent: {split.parent_panel_id}")
    print(f"  Child: {split.child_panel_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Get split")
    print("=" * 70)


def test_get_all_splits():
    """
    Test: Get all splits.
    """
    print("=" * 70)
    print("TEST: Get All Splits")
    print("=" * 70)
    
    engine = TerminalSplitEngine()
    engine.split_panel("parent_1", "child_1")
    engine.split_panel("parent_2", "child_2")
    
    splits = engine.get_all_splits()
    
    assert len(splits) == 2, "2 split olmalı"
    
    print(f"  Split count: {len(splits)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all splits")
    print("=" * 70)


def test_get_splits_by_panel():
    """
    Test: Get splits by panel.
    """
    print("=" * 70)
    print("TEST: Get Splits By Panel")
    print("=" * 70)
    
    engine = TerminalSplitEngine()
    engine.split_panel("parent_1", "child_1")
    engine.split_panel("parent_1", "child_2")
    
    splits = engine.get_splits_by_panel("parent_1")
    
    assert len(splits) == 2, "2 split olmalı"
    
    print(f"  Split count: {len(splits)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get splits by panel")
    print("=" * 70)


def test_get_split_history():
    """
    Test: Get split history.
    """
    print("=" * 70)
    print("TEST: Get Split History")
    print("=" * 70)
    
    engine = TerminalSplitEngine()
    engine.split_panel("parent_1", "child_1")
    
    history = engine.get_split_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get split history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalSplitEngine()
    engine.split_panel("parent_1", "child_1")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_split_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_undo_last_split():
    """
    Test: Undo last split.
    """
    print("=" * 70)
    print("TEST: Undo Last Split")
    print("=" * 70)
    
    engine = TerminalSplitEngine()
    engine.split_panel("parent_1", "child_1")
    
    result = engine.undo_last_split()
    
    assert result.success, "Geri alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Undo last split")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = TerminalSplitEngine()
    
    new_config = SplitConfig(direction=SplitDirection.VERTICAL)
    result = engine.update_config(new_config)
    
    assert result.success, "Güncelleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
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
    
    engine = TerminalSplitEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.direction == SplitDirection.HORIZONTAL, "Config eşleşmeli"
    
    print(f"  Direction: {config.direction.value}")
    print(f"  Ratio: {config.ratio.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_split_direction_enum():
    """
    Test: SplitDirection enum.
    """
    print("=" * 70)
    print("TEST: SplitDirection Enum")
    print("=" * 70)
    
    assert SplitDirection.HORIZONTAL.value == "horizontal"
    assert SplitDirection.VERTICAL.value == "vertical"
    
    print(f"  All enum values verified")
    print(f"  Total directions: {len(SplitDirection)}")
    
    print("\n" + "=" * 70)
    print("PASS: SplitDirection enum")
    print("=" * 70)


def test_split_ratio_enum():
    """
    Test: SplitRatio enum.
    """
    print("=" * 70)
    print("TEST: SplitRatio Enum")
    print("=" * 70)
    
    assert SplitRatio.EQUAL.value == "equal"
    assert SplitRatio.TOP_HEAVY.value == "top_heavy"
    assert SplitRatio.BOTTOM_HEAVY.value == "bottom_heavy"
    assert SplitRatio.LEFT_HEAVY.value == "left_heavy"
    assert SplitRatio.RIGHT_HEAVY.value == "right_heavy"
    assert SplitRatio.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total ratios: {len(SplitRatio)}")
    
    print("\n" + "=" * 70)
    print("PASS: SplitRatio enum")
    print("=" * 70)


def test_split_config_dataclass():
    """
    Test: SplitConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SplitConfig Dataclass")
    print("=" * 70)
    
    config = SplitConfig(
        direction=SplitDirection.VERTICAL,
        ratio=SplitRatio.CUSTOM,
        custom_ratio=0.7
    )
    
    assert config.direction == SplitDirection.VERTICAL, "Direction eşleşmeli"
    assert config.ratio == SplitRatio.CUSTOM, "Ratio eşleşmeli"
    assert config.custom_ratio == 0.7, "Custom ratio eşleşmeli"
    
    print(f"  Direction: {config.direction.value}")
    print(f"  Ratio: {config.ratio.value}")
    print(f"  Custom ratio: {config.custom_ratio}")
    
    print("\n" + "=" * 70)
    print("PASS: SplitConfig dataclass")
    print("=" * 70)


def test_split_dataclass():
    """
    Test: Split dataclass.
    """
    print("=" * 70)
    print("TEST: Split Dataclass")
    print("=" * 70)
    
    split = Split(
        id="split_1",
        parent_panel_id="parent_1",
        child_panel_id="child_1",
        direction=SplitDirection.HORIZONTAL,
        ratio=SplitRatio.EQUAL,
        custom_ratio=0.5
    )
    
    assert split.id == "split_1", "ID eşleşmeli"
    assert split.parent_panel_id == "parent_1", "Parent ID eşleşmeli"
    assert split.child_panel_id == "child_1", "Child ID eşleşmeli"
    
    print(f"  ID: {split.id}")
    print(f"  Parent: {split.parent_panel_id}")
    print(f"  Child: {split.child_panel_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Split dataclass")
    print("=" * 70)


def test_split_result_dataclass():
    """
    Test: SplitResult dataclass.
    """
    print("=" * 70)
    print("TEST: SplitResult Dataclass")
    print("=" * 70)
    
    result = SplitResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: SplitResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_split_panel()
        test2 = test_split_panel_with_direction()
        test3 = test_split_panel_with_ratio()
        test4 = test_split_panel_with_custom_ratio()
        test5 = test_merge_split()
        test6 = test_resize_split()
        test7 = test_change_direction()
        test8 = test_get_split()
        test9 = test_get_all_splits()
        test10 = test_get_splits_by_panel()
        test11 = test_get_split_history()
        test12 = test_clear_history()
        test13 = test_undo_last_split()
        test14 = test_update_config()
        test15 = test_get_config()
        test16 = test_split_direction_enum()
        test17 = test_split_ratio_enum()
        test18 = test_split_config_dataclass()
        test19 = test_split_dataclass()
        test20 = test_split_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Split Panel: {'PASS' if test1 else 'FAIL'}")
        print(f"Split Panel With Direction: {'PASS' if test2 else 'FAIL'}")
        print(f"Split Panel With Ratio: {'PASS' if test3 else 'FAIL'}")
        print(f"Split Panel With Custom Ratio: {'PASS' if test4 else 'FAIL'}")
        print(f"Merge Split: {'PASS' if test5 else 'FAIL'}")
        print(f"Resize Split: {'PASS' if test6 else 'FAIL'}")
        print(f"Change Direction: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Split: {'PASS' if test8 else 'FAIL'}")
        print(f"Get All Splits: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Splits By Panel: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Split History: {'PASS' if test11 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test12 else 'FAIL'}")
        print(f"Undo Last Split: {'PASS' if test13 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test15 else 'FAIL'}")
        print(f"SplitDirection Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"SplitRatio Enum: {'PASS' if test17 else 'FAIL'}")
        print(f"SplitConfig Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"Split Dataclass: {'PASS' if test19 else 'FAIL'}")
        print(f"SplitResult Dataclass: {'PASS' if test20 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20])
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
