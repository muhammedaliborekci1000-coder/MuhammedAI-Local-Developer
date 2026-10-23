"""
Quality Test: Git Stage/Unstage
Git stage/unstage system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.git_stage_unstage import (
    GitStageUnstageEngine,
    StageMode,
    StageStatus,
    StagedFile,
    StageConfig,
    StageResult
)


def test_stage_file():
    """
    Test: Stage file.
    """
    print("=" * 70)
    print("TEST: Stage File")
    print("=" * 70)
    
    engine = GitStageUnstageEngine()
    
    result = engine.stage_file("test.py")
    
    assert result.success, "Stage başarılı olmalı"
    assert result.total_staged == 1, "1 dosya staged olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total staged: {result.total_staged}")
    
    print("\n" + "=" * 70)
    print("PASS: Stage file")
    print("=" * 70)


def test_unstage_file():
    """
    Test: Unstage file.
    """
    print("=" * 70)
    print("TEST: Unstage File")
    print("=" * 70)
    
    engine = GitStageUnstageEngine()
    
    engine.stage_file("test.py")
    result = engine.unstage_file("test.py")
    
    assert result.success, "Unstage başarılı olmalı"
    assert result.total_unstaged == 1, "1 dosya unstaged olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total unstaged: {result.total_unstaged}")
    
    print("\n" + "=" * 70)
    print("PASS: Unstage file")
    print("=" * 70)


def test_stage_all():
    """
    Test: Stage all.
    """
    print("=" * 70)
    print("TEST: Stage All")
    print("=" * 70)
    
    engine = GitStageUnstageEngine()
    
    files = ["test.py", "test2.py", "test3.py"]
    result = engine.stage_all(files)
    
    assert result.success, "Stage all başarılı olmalı"
    assert result.total_staged == 3, "3 dosya staged olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total staged: {result.total_staged}")
    
    print("\n" + "=" * 70)
    print("PASS: Stage all")
    print("=" * 70)


def test_unstage_all():
    """
    Test: Unstage all.
    """
    print("=" * 70)
    print("TEST: Unstage All")
    print("=" * 70)
    
    engine = GitStageUnstageEngine()
    
    files = ["test.py", "test2.py"]
    engine.stage_all(files)
    result = engine.unstage_all()
    
    assert result.success, "Unstage all başarılı olmalı"
    assert result.total_unstaged == 2, "2 dosya unstaged olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total unstaged: {result.total_unstaged}")
    
    print("\n" + "=" * 70)
    print("PASS: Unstage all")
    print("=" * 70)


def test_stage_by_pattern():
    """
    Test: Stage by pattern.
    """
    print("=" * 70)
    print("TEST: Stage By Pattern")
    print("=" * 70)
    
    engine = GitStageUnstageEngine()
    
    files = ["test.py", "test2.py", "other.txt"]
    result = engine.stage_by_pattern("*.py", files)
    
    assert result.success, "Pattern stage başarılı olmalı"
    assert result.total_staged == 2, "2 dosya staged olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total staged: {result.total_staged}")
    
    print("\n" + "=" * 70)
    print("PASS: Stage by pattern")
    print("=" * 70)


def test_unstage_by_pattern():
    """
    Test: Unstage by pattern.
    """
    print("=" * 70)
    print("TEST: Unstage By Pattern")
    print("=" * 70)
    
    engine = GitStageUnstageEngine()
    
    files = ["test.py", "test2.py", "other.txt"]
    engine.stage_all(files)
    result = engine.unstage_by_pattern("*.py")
    
    assert result.success, "Pattern unstage başarılı olmalı"
    assert result.total_unstaged == 2, "2 dosya unstaged olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total unstaged: {result.total_unstaged}")
    
    print("\n" + "=" * 70)
    print("PASS: Unstage by pattern")
    print("=" * 70)


def test_get_staged_files():
    """
    Test: Get staged files.
    """
    print("=" * 70)
    print("TEST: Get Staged Files")
    print("=" * 70)
    
    engine = GitStageUnstageEngine()
    
    engine.stage_file("test.py")
    engine.stage_file("test2.py")
    
    staged = engine.get_staged_files()
    
    assert len(staged) == 2, "2 staged dosya olmalı"
    
    print(f"  Staged files: {len(staged)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get staged files")
    print("=" * 70)


def test_get_unstaged_files():
    """
    Test: Get unstaged files.
    """
    print("=" * 70)
    print("TEST: Get Unstaged Files")
    print("=" * 70)
    
    engine = GitStageUnstageEngine()
    
    all_files = ["test.py", "test2.py", "test3.py"]
    engine.stage_file("test.py")
    
    unstaged = engine.get_unstaged_files(all_files)
    
    assert len(unstaged) == 2, "2 unstaged dosya olmalı"
    
    print(f"  Unstaged files: {len(unstaged)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get unstaged files")
    print("=" * 70)


def test_get_file_status():
    """
    Test: Get file status.
    """
    print("=" * 70)
    print("TEST: Get File Status")
    print("=" * 70)
    
    engine = GitStageUnstageEngine()
    
    engine.stage_file("test.py")
    
    status = engine.get_file_status("test.py")
    
    assert status == StageStatus.STAGED, "Status STAGED olmalı"
    
    print(f"  Status: {status.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get file status")
    print("=" * 70)


def test_stage_partial():
    """
    Test: Stage partial.
    """
    print("=" * 70)
    print("TEST: Stage Partial")
    print("=" * 70)
    
    engine = GitStageUnstageEngine()
    
    result = engine.stage_partial("test.py", [1, 2, 3])
    
    assert result.success, "Partial stage başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Stage partial")
    print("=" * 70)


def test_get_stage_history():
    """
    Test: Get stage history.
    """
    print("=" * 70)
    print("TEST: Get Stage History")
    print("=" * 70)
    
    engine = GitStageUnstageEngine()
    
    engine.stage_file("test.py")
    engine.unstage_file("test.py")
    
    history = engine.get_stage_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {history}")
    
    print("\n" + "=" * 70)
    print("PASS: Get stage history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = GitStageUnstageEngine()
    
    engine.stage_file("test.py")
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_stage_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_get_staged_count():
    """
    Test: Get staged count.
    """
    print("=" * 70)
    print("TEST: Get Staged Count")
    print("=" * 70)
    
    engine = GitStageUnstageEngine()
    
    engine.stage_file("test.py")
    engine.stage_file("test2.py")
    
    count = engine.get_staged_count()
    
    assert count == 2, "2 staged dosya olmalı"
    
    print(f"  Staged count: {count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get staged count")
    print("=" * 70)


def test_is_staged():
    """
    Test: Is staged.
    """
    print("=" * 70)
    print("TEST: Is Staged")
    print("=" * 70)
    
    engine = GitStageUnstageEngine()
    
    engine.stage_file("test.py")
    
    is_staged = engine.is_staged("test.py")
    
    assert is_staged == True, "Staged olmalı"
    
    print(f"  Is staged: {is_staged}")
    
    print("\n" + "=" * 70)
    print("PASS: Is staged")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = GitStageUnstageEngine()
    
    new_config = StageConfig(auto_stage=True)
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
    
    engine = GitStageUnstageEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.auto_stage == False, "Config eşleşmeli"
    
    print(f"  Auto stage: {config.auto_stage}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_stage_mode_enum():
    """
    Test: StageMode enum.
    """
    print("=" * 70)
    print("TEST: StageMode Enum")
    print("=" * 70)
    
    assert StageMode.FILE.value == "file"
    assert StageMode.DIRECTORY.value == "directory"
    assert StageMode.PATTERN.value == "pattern"
    assert StageMode.PATCH.value == "patch"
    assert StageMode.ALL.value == "all"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(StageMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: StageMode enum")
    print("=" * 70)


def test_stage_status_enum():
    """
    Test: StageStatus enum.
    """
    print("=" * 70)
    print("TEST: StageStatus Enum")
    print("=" * 70)
    
    assert StageStatus.STAGED.value == "staged"
    assert StageStatus.UNSTAGED.value == "unstaged"
    assert StageStatus.PARTIALLY_STAGED.value == "partially_staged"
    assert StageStatus.IGNORED.value == "ignored"
    
    print(f"  All enum values verified")
    print(f"  Total statuses: {len(StageStatus)}")
    
    print("\n" + "=" * 70)
    print("PASS: StageStatus enum")
    print("=" * 70)


def test_staged_file_dataclass():
    """
    Test: StagedFile dataclass.
    """
    print("=" * 70)
    print("TEST: StagedFile Dataclass")
    print("=" * 70)
    
    staged_file = StagedFile(
        file_path="test.py",
        status=StageStatus.STAGED,
        is_new=True
    )
    
    assert staged_file.file_path == "test.py", "File path eşleşmeli"
    assert staged_file.status == StageStatus.STAGED, "Status eşleşmeli"
    assert staged_file.is_new == True, "Is new eşleşmeli"
    
    print(f"  File path: {staged_file.file_path}")
    print(f"  Status: {staged_file.status.value}")
    print(f"  Is new: {staged_file.is_new}")
    
    print("\n" + "=" * 70)
    print("PASS: StagedFile dataclass")
    print("=" * 70)


def test_stage_config_dataclass():
    """
    Test: StageConfig dataclass.
    """
    print("=" * 70)
    print("TEST: StageConfig Dataclass")
    print("=" * 70)
    
    config = StageConfig(
        auto_stage=True,
        track_changes=True,
        show_status=True
    )
    
    assert config.auto_stage == True, "Auto stage eşleşmeli"
    assert config.track_changes == True, "Track changes eşleşmeli"
    assert config.show_status == True, "Show status eşleşmeli"
    
    print(f"  Auto stage: {config.auto_stage}")
    print(f"  Track changes: {config.track_changes}")
    print(f"  Show status: {config.show_status}")
    
    print("\n" + "=" * 70)
    print("PASS: StageConfig dataclass")
    print("=" * 70)


def test_stage_result_dataclass():
    """
    Test: StageResult dataclass.
    """
    print("=" * 70)
    print("TEST: StageResult Dataclass")
    print("=" * 70)
    
    result = StageResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.staged_files, list), "Staged files list olmalı"
    assert isinstance(result.unstaged_files, list), "Unstaged files list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Staged files: {len(result.staged_files)}")
    print(f"  Unstaged files: {len(result.unstaged_files)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: StageResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_stage_file()
        test2 = test_unstage_file()
        test3 = test_stage_all()
        test4 = test_unstage_all()
        test5 = test_stage_by_pattern()
        test6 = test_unstage_by_pattern()
        test7 = test_get_staged_files()
        test8 = test_get_unstaged_files()
        test9 = test_get_file_status()
        test10 = test_stage_partial()
        test11 = test_get_stage_history()
        test12 = test_clear_history()
        test13 = test_get_staged_count()
        test14 = test_is_staged()
        test15 = test_update_config()
        test16 = test_get_config()
        test17 = test_stage_mode_enum()
        test18 = test_stage_status_enum()
        test19 = test_staged_file_dataclass()
        test20 = test_stage_config_dataclass()
        test21 = test_stage_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Stage File: {'PASS' if test1 else 'FAIL'}")
        print(f"Unstage File: {'PASS' if test2 else 'FAIL'}")
        print(f"Stage All: {'PASS' if test3 else 'FAIL'}")
        print(f"Unstage All: {'PASS' if test4 else 'FAIL'}")
        print(f"Stage By Pattern: {'PASS' if test5 else 'FAIL'}")
        print(f"Unstage By Pattern: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Staged Files: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Unstaged Files: {'PASS' if test8 else 'FAIL'}")
        print(f"Get File Status: {'PASS' if test9 else 'FAIL'}")
        print(f"Stage Partial: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Stage History: {'PASS' if test11 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Staged Count: {'PASS' if test13 else 'FAIL'}")
        print(f"Is Staged: {'PASS' if test14 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test16 else 'FAIL'}")
        print(f"StageMode Enum: {'PASS' if test17 else 'FAIL'}")
        print(f"StageStatus Enum: {'PASS' if test18 else 'FAIL'}")
        print(f"StagedFile Dataclass: {'PASS' if test19 else 'FAIL'}")
        print(f"StageConfig Dataclass: {'PASS' if test20 else 'FAIL'}")
        print(f"StageResult Dataclass: {'PASS' if test21 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21])
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
