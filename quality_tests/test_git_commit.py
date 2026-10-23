"""
Quality Test: Git Commit
Git commit system testleri.
"""

import sys
import os
import tempfile
import subprocess
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.git_commit import (
    GitCommitEngine,
    CommitAction,
    CommitAuthor,
    Commit,
    GitCommitResult
)


def test_commit():
    """
    Test: Git commit.
    """
    print("=" * 70)
    print("TEST: Git Commit")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Git repo oluştur
        subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmpdir, capture_output=True)
        
        # Dosya oluştur ve stage et
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Hello World")
        
        engine = GitCommitEngine(tmpdir)
        stage_result = engine.stage_files(["test.txt"])
        
        if stage_result.success:
            # Commit et
            commit_result = engine.commit("Initial commit")
            
            assert commit_result.success, "Commit başarılı olmalı"
            assert commit_result.commit_hash is not None, "Commit hash olmalı"
            
            print(f"  Success: {commit_result.success}")
            print(f"  Commit hash: {commit_result.commit_hash}")
            print(f"  Message: {commit_result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Git commit")
    print("=" * 70)


def test_stage_files():
    """
    Test: Stage files.
    """
    print("=" * 70)
    print("TEST: Stage Files")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Git repo oluştur
        subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmpdir, capture_output=True)
        
        # Dosya oluştur
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Hello World")
        
        engine = GitCommitEngine(tmpdir)
        result = engine.stage_files(["test.txt"])
        
        assert result.success, "Staging başarılı olmalı"
        assert len(result.staged_files) > 0, "Staged files olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Staged files: {result.staged_files}")
        print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Stage files")
    print("=" * 70)


def test_unstage_files():
    """
    Test: Unstage files.
    """
    print("=" * 70)
    print("TEST: Unstage Files")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Git repo oluştur
        subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmpdir, capture_output=True)
        
        # Dosya oluştur ve stage et
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Hello World")
        
        engine = GitCommitEngine(tmpdir)
        engine.stage_files(["test.txt"])
        
        # Unstage et
        result = engine.unstage_files(["test.txt"])
        
        assert result.success, "Unstaging başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Unstaged files: {result.unstaged_files}")
        print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Unstage files")
    print("=" * 70)


def test_get_commit_history():
    """
    Test: Get commit history.
    """
    print("=" * 70)
    print("TEST: Get Commit History")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Git repo oluştur
        subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmpdir, capture_output=True)
        
        # Dosya oluştur, stage et ve commit et
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Hello World")
        
        engine = GitCommitEngine(tmpdir)
        engine.stage_files(["test.txt"])
        engine.commit("Initial commit")
        
        # Geçmişi al
        history = engine.get_commit_history()
        
        assert len(history) > 0, "Commit geçmişi olmalı"
        
        print(f"  Total commits: {len(history)}")
        print(f"  Latest commit: {history[0].message if history else None}")
    
    print("\n" + "=" * 70)
    print("PASS: Get commit history")
    print("=" * 70)


def test_get_staged_files():
    """
    Test: Get staged files.
    """
    print("=" * 70)
    print("TEST: Get Staged Files")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Git repo oluştur
        subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmpdir, capture_output=True)
        
        # Dosya oluştur ve stage et
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Hello World")
        
        engine = GitCommitEngine(tmpdir)
        engine.stage_files(["test.txt"])
        
        # Staged dosyaları al
        staged_files = engine.get_staged_files()
        
        assert len(staged_files) > 0, "Staged dosyalar olmalı"
        
        print(f"  Staged files: {staged_files}")
    
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
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Git repo oluştur
        subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmpdir, capture_output=True)
        
        # Dosya oluştur ve commit et
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Hello World")
        
        engine = GitCommitEngine(tmpdir)
        engine.stage_files(["test.txt"])
        engine.commit("Initial commit")
        
        # Dosyayı değiştir
        with open(test_file, "w") as f:
            f.write("Hello World\nNew Line")
        
        # Unstaged dosyaları al
        unstaged_files = engine.get_unstaged_files()
        
        assert len(unstaged_files) > 0, "Unstaged dosyalar olmalı"
        
        print(f"  Unstaged files: {unstaged_files}")
    
    print("\n" + "=" * 70)
    print("PASS: Get unstaged files")
    print("=" * 70)


def test_amend_commit():
    """
    Test: Amend commit.
    """
    print("=" * 70)
    print("TEST: Amend Commit")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Git repo oluştur
        subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmpdir, capture_output=True)
        
        # Dosya oluştur, stage et ve commit et
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Hello World")
        
        engine = GitCommitEngine(tmpdir)
        engine.stage_files(["test.txt"])
        engine.commit("Initial commit")
        
        # Commit'i değiştir
        result = engine.amend_commit("Updated commit message")
        
        assert result.success, "Amend başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Commit hash: {result.commit_hash}")
        print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Amend commit")
    print("=" * 70)


def test_commit_action_enum():
    """
    Test: CommitAction enum.
    """
    print("=" * 70)
    print("TEST: CommitAction Enum")
    print("=" * 70)
    
    assert CommitAction.CREATE.value == "create"
    assert CommitAction.AMEND.value == "amend"
    assert CommitAction.CHERRY_PICK.value == "cherry_pick"
    assert CommitAction.REVERT.value == "revert"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(CommitAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: CommitAction enum")
    print("=" * 70)


def test_commit_author_dataclass():
    """
    Test: CommitAuthor dataclass.
    """
    print("=" * 70)
    print("TEST: CommitAuthor Dataclass")
    print("=" * 70)
    
    author = CommitAuthor(
        name="Test User",
        email="test@test.com"
    )
    
    assert author.name == "Test User", "Name eşleşmeli"
    assert author.email == "test@test.com", "Email eşleşmeli"
    
    print(f"  Name: {author.name}")
    print(f"  Email: {author.email}")
    
    print("\n" + "=" * 70)
    print("PASS: CommitAuthor dataclass")
    print("=" * 70)


def test_commit_dataclass():
    """
    Test: Commit dataclass.
    """
    print("=" * 70)
    print("TEST: Commit Dataclass")
    print("=" * 70)
    
    author = CommitAuthor(name="Test", email="test@test.com")
    commit = Commit(
        hash="abc123",
        author=author,
        date=datetime.now(),
        message="Test commit"
    )
    
    assert commit.hash == "abc123", "Hash eşleşmeli"
    assert commit.message == "Test commit", "Message eşleşmeli"
    
    print(f"  Hash: {commit.hash}")
    print(f"  Message: {commit.message}")
    print(f"  Author: {commit.author.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Commit dataclass")
    print("=" * 70)


def test_git_commit_result_dataclass():
    """
    Test: GitCommitResult dataclass.
    """
    print("=" * 70)
    print("TEST: GitCommitResult Dataclass")
    print("=" * 70)
    
    result = GitCommitResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.staged_files, list), "Staged files list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Staged files: {len(result.staged_files)}")
    
    print("\n" + "=" * 70)
    print("PASS: GitCommitResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_commit()
        test2 = test_stage_files()
        test3 = test_unstage_files()
        test4 = test_get_commit_history()
        test5 = test_get_staged_files()
        test6 = test_get_unstaged_files()
        test7 = test_amend_commit()
        test8 = test_commit_action_enum()
        test9 = test_commit_author_dataclass()
        test10 = test_commit_dataclass()
        test11 = test_git_commit_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Git Commit: {'PASS' if test1 else 'FAIL'}")
        print(f"Stage Files: {'PASS' if test2 else 'FAIL'}")
        print(f"Unstage Files: {'PASS' if test3 else 'FAIL'}")
        print(f"Get Commit History: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Staged Files: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Unstaged Files: {'PASS' if test6 else 'FAIL'}")
        print(f"Amend Commit: {'PASS' if test7 else 'FAIL'}")
        print(f"CommitAction Enum: {'PASS' if test8 else 'FAIL'}")
        print(f"CommitAuthor Dataclass: {'PASS' if test9 else 'FAIL'}")
        print(f"Commit Dataclass: {'PASS' if test10 else 'FAIL'}")
        print(f"GitCommitResult Dataclass: {'PASS' if test11 else 'FAIL'}")
        
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
