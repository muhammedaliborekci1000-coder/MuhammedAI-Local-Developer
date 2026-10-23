"""
Quality Test: Git Diff
Git diff system testleri.
"""

import sys
import os
import tempfile
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.git_diff import (
    GitDiffEngine,
    DiffType,
    DiffView,
    DiffLine,
    DiffHunk,
    FileDiff,
    GitDiffResult
)


def test_diff():
    """
    Test: Git diff.
    """
    print("=" * 70)
    print("TEST: Git Diff")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Git repo oluştur
        subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmpdir, capture_output=True)
        
        # Dosya oluştur ve commit et
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Hello World")
        
        subprocess.run(["git", "add", "test.txt"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=tmpdir, capture_output=True)
        
        # Dosyayı değiştir
        with open(test_file, "w") as f:
            f.write("Hello World\nNew Line")
        
        # Diff al
        engine = GitDiffEngine(tmpdir)
        result = engine.diff()
        
        assert result.success, "Diff başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Total files: {result.total_files}")
        print(f"  Total added: {result.total_added}")
        print(f"  Total removed: {result.total_removed}")
    
    print("\n" + "=" * 70)
    print("PASS: Git diff")
    print("=" * 70)


def test_diff_staged():
    """
    Test: Staged diff.
    """
    print("=" * 70)
    print("TEST: Staged Diff")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Git repo oluştur
        subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmpdir, capture_output=True)
        
        # Dosya oluştur ve commit et
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Hello World")
        
        subprocess.run(["git", "add", "test.txt"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=tmpdir, capture_output=True)
        
        # Dosyayı değiştir ve stage et
        with open(test_file, "w") as f:
            f.write("Hello World\nNew Line")
        subprocess.run(["git", "add", "test.txt"], cwd=tmpdir, capture_output=True)
        
        # Staged diff al
        engine = GitDiffEngine(tmpdir)
        result = engine.diff(staged=True)
        
        assert result.success, "Diff başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Total files: {result.total_files}")
    
    print("\n" + "=" * 70)
    print("PASS: Staged diff")
    print("=" * 70)


def test_diff_file_path():
    """
    Test: Diff specific file.
    """
    print("=" * 70)
    print("TEST: Diff Specific File")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Git repo oluştur
        subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmpdir, capture_output=True)
        
        # Dosyaları oluştur ve commit et
        test_file1 = os.path.join(tmpdir, "test1.txt")
        test_file2 = os.path.join(tmpdir, "test2.txt")
        
        with open(test_file1, "w") as f:
            f.write("Hello")
        with open(test_file2, "w") as f:
            f.write("World")
        
        subprocess.run(["git", "add", "."], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=tmpdir, capture_output=True)
        
        # Sadece bir dosyayı değiştir
        with open(test_file1, "w") as f:
            f.write("Hello\nNew")
        
        # Sadece o dosya için diff al
        engine = GitDiffEngine(tmpdir)
        result = engine.diff(file_path="test1.txt")
        
        assert result.success, "Diff başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Total files: {result.total_files}")
    
    print("\n" + "=" * 70)
    print("PASS: Diff specific file")
    print("=" * 70)


def test_get_diff_stats():
    """
    Test: Get diff stats.
    """
    print("=" * 70)
    print("TEST: Get Diff Stats")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Git repo oluştur
        subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmpdir, capture_output=True)
        
        # Dosya oluştur ve commit et
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Hello World")
        
        subprocess.run(["git", "add", "test.txt"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=tmpdir, capture_output=True)
        
        # Dosyayı değiştir
        with open(test_file, "w") as f:
            f.write("Hello World\nNew Line")
        
        # İstatistikleri al
        engine = GitDiffEngine(tmpdir)
        stats = engine.get_diff_stats()
        
        assert "files" in stats, "Files istatistiği olmalı"
        assert "additions" in stats, "Additions istatistiği olmalı"
        assert "deletions" in stats, "Deletions istatistiği olmalı"
        
        print(f"  Files: {stats['files']}")
        print(f"  Additions: {stats['additions']}")
        print(f"  Deletions: {stats['deletions']}")
    
    print("\n" + "=" * 70)
    print("PASS: Get diff stats")
    print("=" * 70)


def test_generate_patch():
    """
    Test: Generate patch.
    """
    print("=" * 70)
    print("TEST: Generate Patch")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Git repo oluştur
        subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmpdir, capture_output=True)
        
        # Dosya oluştur ve commit et
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Hello World")
        
        subprocess.run(["git", "add", "test.txt"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=tmpdir, capture_output=True)
        
        # Dosyayı değiştir
        with open(test_file, "w") as f:
            f.write("Hello World\nNew Line")
        
        # Patch oluştur
        engine = GitDiffEngine(tmpdir)
        patch = engine.generate_patch()
        
        assert patch is not None, "Patch oluşturulmalı"
        assert len(patch) > 0, "Patch boş olmamalı"
        
        print(f"  Patch generated: {patch is not None}")
        print(f"  Patch length: {len(patch)}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate patch")
    print("=" * 70)


def test_diff_type_enum():
    """
    Test: DiffType enum.
    """
    print("=" * 70)
    print("TEST: DiffType Enum")
    print("=" * 70)
    
    assert DiffType.ADDED.value == "added"
    assert DiffType.REMOVED.value == "removed"
    assert DiffType.MODIFIED.value == "modified"
    assert DiffType.UNCHANGED.value == "unchanged"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(DiffType)}")
    
    print("\n" + "=" * 70)
    print("PASS: DiffType enum")
    print("=" * 70)


def test_diff_view_enum():
    """
    Test: DiffView enum.
    """
    print("=" * 70)
    print("TEST: DiffView Enum")
    print("=" * 70)
    
    assert DiffView.INLINE.value == "inline"
    assert DiffView.SIDE_BY_SIDE.value == "side_by_side"
    assert DiffView.UNIFIED.value == "unified"
    
    print(f"  All enum values verified")
    print(f"  Total views: {len(DiffView)}")
    
    print("\n" + "=" * 70)
    print("PASS: DiffView enum")
    print("=" * 70)


def test_diff_line_dataclass():
    """
    Test: DiffLine dataclass.
    """
    print("=" * 70)
    print("TEST: DiffLine Dataclass")
    print("=" * 70)
    
    line = DiffLine(
        line_number=1,
        content="Hello",
        type=DiffType.ADDED
    )
    
    assert line.line_number == 1, "Line number eşleşmeli"
    assert line.content == "Hello", "Content eşleşmeli"
    assert line.type == DiffType.ADDED, "Type eşleşmeli"
    
    print(f"  Line number: {line.line_number}")
    print(f"  Content: {line.content}")
    print(f"  Type: {line.type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: DiffLine dataclass")
    print("=" * 70)


def test_diff_hunk_dataclass():
    """
    Test: DiffHunk dataclass.
    """
    print("=" * 70)
    print("TEST: DiffHunk Dataclass")
    print("=" * 70)
    
    hunk = DiffHunk(
        old_start=1,
        old_count=5,
        new_start=1,
        new_count=6,
        header="@@ -1,5 +1,6 @@"
    )
    
    assert hunk.old_start == 1, "Old start eşleşmeli"
    assert hunk.new_start == 1, "New start eşleşmeli"
    
    print(f"  Old start: {hunk.old_start}")
    print(f"  New start: {hunk.new_start}")
    print(f"  Header: {hunk.header}")
    
    print("\n" + "=" * 70)
    print("PASS: DiffHunk dataclass")
    print("=" * 70)


def test_file_diff_dataclass():
    """
    Test: FileDiff dataclass.
    """
    print("=" * 70)
    print("TEST: FileDiff Dataclass")
    print("=" * 70)
    
    file_diff = FileDiff(
        file_path="/path/to/file.txt",
        old_file="/path/to/old.txt",
        new_file="/path/to/new.txt"
    )
    
    assert file_diff.file_path == "/path/to/file.txt", "File path eşleşmeli"
    assert file_diff.old_file == "/path/to/old.txt", "Old file eşleşmeli"
    
    print(f"  File path: {file_diff.file_path}")
    print(f"  Old file: {file_diff.old_file}")
    print(f"  New file: {file_diff.new_file}")
    
    print("\n" + "=" * 70)
    print("PASS: FileDiff dataclass")
    print("=" * 70)


def test_git_diff_result_dataclass():
    """
    Test: GitDiffResult dataclass.
    """
    print("=" * 70)
    print("TEST: GitDiffResult Dataclass")
    print("=" * 70)
    
    result = GitDiffResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.diffs, list), "Diffs list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Diffs: {len(result.diffs)}")
    
    print("\n" + "=" * 70)
    print("PASS: GitDiffResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_diff()
        test2 = test_diff_staged()
        test3 = test_diff_file_path()
        test4 = test_get_diff_stats()
        test5 = test_generate_patch()
        test6 = test_diff_type_enum()
        test7 = test_diff_view_enum()
        test8 = test_diff_line_dataclass()
        test9 = test_diff_hunk_dataclass()
        test10 = test_file_diff_dataclass()
        test11 = test_git_diff_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Git Diff: {'PASS' if test1 else 'FAIL'}")
        print(f"Staged Diff: {'PASS' if test2 else 'FAIL'}")
        print(f"Diff Specific File: {'PASS' if test3 else 'FAIL'}")
        print(f"Get Diff Stats: {'PASS' if test4 else 'FAIL'}")
        print(f"Generate Patch: {'PASS' if test5 else 'FAIL'}")
        print(f"DiffType Enum: {'PASS' if test6 else 'FAIL'}")
        print(f"DiffView Enum: {'PASS' if test7 else 'FAIL'}")
        print(f"DiffLine Dataclass: {'PASS' if test8 else 'FAIL'}")
        print(f"DiffHunk Dataclass: {'PASS' if test9 else 'FAIL'}")
        print(f"FileDiff Dataclass: {'PASS' if test10 else 'FAIL'}")
        print(f"GitDiffResult Dataclass: {'PASS' if test11 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11])
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
