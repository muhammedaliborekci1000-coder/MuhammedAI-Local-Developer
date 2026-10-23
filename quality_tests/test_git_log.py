"""
Quality Test: Git Log
Git log system testleri.
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.git_log import (
    GitLogEngine,
    LogFormat,
    LogOrder,
    LogFilter,
    LogConfig,
    LogAuthor,
    LogCommit,
    LogResult
)


def test_get_log():
    """
    Test: Get log.
    """
    print("=" * 70)
    print("TEST: Get Log")
    print("=" * 70)
    
    engine = GitLogEngine()
    result = engine.get_log()
    
    assert result.success, "Log alma başarılı olmalı"
    assert result.total_commits > 0, "Commitler olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total commits: {result.total_commits}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Get log")
    print("=" * 70)


def test_get_log_with_format():
    """
    Test: Get log with format.
    """
    print("=" * 70)
    print("TEST: Get Log With Format")
    print("=" * 70)
    
    engine = GitLogEngine()
    result = engine.get_log(format=LogFormat.ONELINE)
    
    assert result.success, "Log alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Format: {result.format}")
    
    print("\n" + "=" * 70)
    print("PASS: Get log with format")
    print("=" * 70)


def test_get_log_by_author():
    """
    Test: Get log by author.
    """
    print("=" * 70)
    print("TEST: Get Log By Author")
    print("=" * 70)
    
    engine = GitLogEngine()
    result = engine.get_log_by_author("Developer")
    
    assert result.success, "Log alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Get log by author")
    print("=" * 70)


def test_get_log_by_date_range():
    """
    Test: Get log by date range.
    """
    print("=" * 70)
    print("TEST: Get Log By Date Range")
    print("=" * 70)
    
    engine = GitLogEngine()
    start_date = datetime.now().replace(hour=0, minute=0, second=0)
    end_date = datetime.now().replace(hour=23, minute=59, second=59)
    
    result = engine.get_log_by_date_range(start_date, end_date)
    
    assert result.success, "Log alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Get log by date range")
    print("=" * 70)


def test_get_log_by_message():
    """
    Test: Get log by message.
    """
    print("=" * 70)
    print("TEST: Get Log By Message")
    print("=" * 70)
    
    engine = GitLogEngine()
    result = engine.get_log_by_message("Feature")
    
    assert result.success, "Log alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Get log by message")
    print("=" * 70)


def test_get_log_by_file():
    """
    Test: Get log by file.
    """
    print("=" * 70)
    print("TEST: Get Log By File")
    print("=" * 70)
    
    engine = GitLogEngine()
    result = engine.get_log_by_file("test.py")
    
    assert result.success, "Log alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Get log by file")
    print("=" * 70)


def test_get_log_by_branch():
    """
    Test: Get log by branch.
    """
    print("=" * 70)
    print("TEST: Get Log By Branch")
    print("=" * 70)
    
    engine = GitLogEngine()
    result = engine.get_log_by_branch("main")
    
    assert result.success, "Log alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Get log by branch")
    print("=" * 70)


def test_get_log_graph():
    """
    Test: Get log graph.
    """
    print("=" * 70)
    print("TEST: Get Log Graph")
    print("=" * 70)
    
    engine = GitLogEngine()
    result = engine.get_log_graph()
    
    assert result.success, "Log alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Get log graph")
    print("=" * 70)


def test_get_commit_by_hash():
    """
    Test: Get commit by hash.
    """
    print("=" * 70)
    print("TEST: Get Commit By Hash")
    print("=" * 70)
    
    engine = GitLogEngine()
    engine.get_log()
    
    commit = engine.get_commit_by_hash(engine.commits[0].hash)
    
    assert commit is not None, "Commit bulunmalı"
    assert commit.hash == engine.commits[0].hash, "Hash eşleşmeli"
    
    print(f"  Commit hash: {commit.hash}")
    print(f"  Commit message: {commit.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Get commit by hash")
    print("=" * 70)


def test_get_log_statistics():
    """
    Test: Get log statistics.
    """
    print("=" * 70)
    print("TEST: Get Log Statistics")
    print("=" * 70)
    
    engine = GitLogEngine()
    engine.get_log()
    
    stats = engine.get_log_statistics()
    
    assert stats is not None, "İstatistikler olmalı"
    assert stats["total_commits"] > 0, "Toplam commit olmalı"
    
    print(f"  Total commits: {stats['total_commits']}")
    print(f"  Authors: {stats['authors']}")
    print(f"  Total insertions: {stats['total_insertions']}")
    
    print("\n" + "=" * 70)
    print("PASS: Get log statistics")
    print("=" * 70)


def test_get_log_history():
    """
    Test: Get log history.
    """
    print("=" * 70)
    print("TEST: Get Log History")
    print("=" * 70)
    
    engine = GitLogEngine()
    engine.get_log()
    
    history = engine.get_log_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get log history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = GitLogEngine()
    engine.get_log()
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_log_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = GitLogEngine()
    
    new_config = LogConfig(max_count=50)
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
    
    engine = GitLogEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.max_count == 100, "Config eşleşmeli"
    
    print(f"  Max count: {config.max_count}")
    print(f"  Show graph: {config.show_graph}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_log_format_enum():
    """
    Test: LogFormat enum.
    """
    print("=" * 70)
    print("TEST: LogFormat Enum")
    print("=" * 70)
    
    assert LogFormat.ONELINE.value == "oneline"
    assert LogFormat.SHORT.value == "short"
    assert LogFormat.MEDIUM.value == "medium"
    assert LogFormat.FULL.value == "full"
    assert LogFormat.FULLER.value == "fuller"
    assert LogFormat.EMAIL.value == "email"
    assert LogFormat.RAW.value == "raw"
    
    print(f"  All enum values verified")
    print(f"  Total formats: {len(LogFormat)}")
    
    print("\n" + "=" * 70)
    print("PASS: LogFormat enum")
    print("=" * 70)


def test_log_order_enum():
    """
    Test: LogOrder enum.
    """
    print("=" * 70)
    print("TEST: LogOrder Enum")
    print("=" * 70)
    
    assert LogOrder.DATE.value == "date"
    assert LogOrder.AUTHOR_DATE.value == "author-date"
    assert LogOrder.TOPO.value == "topo"
    assert LogOrder.REVERSE.value == "reverse"
    
    print(f"  All enum values verified")
    print(f"  Total orders: {len(LogOrder)}")
    
    print("\n" + "=" * 70)
    print("PASS: LogOrder enum")
    print("=" * 70)


def test_log_filter_enum():
    """
    Test: LogFilter enum.
    """
    print("=" * 70)
    print("TEST: LogFilter Enum")
    print("=" * 70)
    
    assert LogFilter.AUTHOR.value == "author"
    assert LogFilter.COMMITTER.value == "committer"
    assert LogFilter.MESSAGE.value == "message"
    assert LogFilter.FILE.value == "file"
    assert LogFilter.DATE_RANGE.value == "date_range"
    assert LogFilter.SINCE.value == "since"
    assert LogFilter.UNTIL.value == "until"
    
    print(f"  All enum values verified")
    print(f"  Total filters: {len(LogFilter)}")
    
    print("\n" + "=" * 70)
    print("PASS: LogFilter enum")
    print("=" * 70)


def test_log_config_dataclass():
    """
    Test: LogConfig dataclass.
    """
    print("=" * 70)
    print("TEST: LogConfig Dataclass")
    print("=" * 70)
    
    config = LogConfig(
        max_count=50,
        show_graph=False
    )
    
    assert config.max_count == 50, "Max count eşleşmeli"
    assert config.show_graph == False, "Show graph eşleşmeli"
    
    print(f"  Max count: {config.max_count}")
    print(f"  Show graph: {config.show_graph}")
    
    print("\n" + "=" * 70)
    print("PASS: LogConfig dataclass")
    print("=" * 70)


def test_log_author_dataclass():
    """
    Test: LogAuthor dataclass.
    """
    print("=" * 70)
    print("TEST: LogAuthor Dataclass")
    print("=" * 70)
    
    author = LogAuthor(name="Developer", email="dev@example.com")
    
    assert author.name == "Developer", "Name eşleşmeli"
    assert author.email == "dev@example.com", "Email eşleşmeli"
    
    print(f"  Name: {author.name}")
    print(f"  Email: {author.email}")
    
    print("\n" + "=" * 70)
    print("PASS: LogAuthor dataclass")
    print("=" * 70)


def test_log_commit_dataclass():
    """
    Test: LogCommit dataclass.
    """
    print("=" * 70)
    print("TEST: LogCommit Dataclass")
    print("=" * 70)
    
    commit = LogCommit(
        hash="abc123",
        short_hash="abc123",
        author=LogAuthor(name="Dev", email="dev@example.com"),
        committer=LogAuthor(name="Dev", email="dev@example.com"),
        date=datetime.now(),
        commit_date=datetime.now(),
        message="Test commit"
    )
    
    assert commit.hash == "abc123", "Hash eşleşmeli"
    assert commit.message == "Test commit", "Message eşleşmeli"
    
    print(f"  Hash: {commit.hash}")
    print(f"  Message: {commit.message}")
    
    print("\n" + "=" * 70)
    print("PASS: LogCommit dataclass")
    print("=" * 70)


def test_log_result_dataclass():
    """
    Test: LogResult dataclass.
    """
    print("=" * 70)
    print("TEST: LogResult Dataclass")
    print("=" * 70)
    
    result = LogResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: LogResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_get_log()
        test2 = test_get_log_with_format()
        test3 = test_get_log_by_author()
        test4 = test_get_log_by_date_range()
        test5 = test_get_log_by_message()
        test6 = test_get_log_by_file()
        test7 = test_get_log_by_branch()
        test8 = test_get_log_graph()
        test9 = test_get_commit_by_hash()
        test10 = test_get_log_statistics()
        test11 = test_get_log_history()
        test12 = test_clear_history()
        test13 = test_update_config()
        test14 = test_get_config()
        test15 = test_log_format_enum()
        test16 = test_log_order_enum()
        test17 = test_log_filter_enum()
        test18 = test_log_config_dataclass()
        test19 = test_log_author_dataclass()
        test20 = test_log_commit_dataclass()
        test21 = test_log_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Get Log: {'PASS' if test1 else 'FAIL'}")
        print(f"Get Log With Format: {'PASS' if test2 else 'FAIL'}")
        print(f"Get Log By Author: {'PASS' if test3 else 'FAIL'}")
        print(f"Get Log By Date Range: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Log By Message: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Log By File: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Log By Branch: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Log Graph: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Commit By Hash: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Log Statistics: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Log History: {'PASS' if test11 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test12 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test14 else 'FAIL'}")
        print(f"LogFormat Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"LogOrder Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"LogFilter Enum: {'PASS' if test17 else 'FAIL'}")
        print(f"LogConfig Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"LogAuthor Dataclass: {'PASS' if test19 else 'FAIL'}")
        print(f"LogCommit Dataclass: {'PASS' if test20 else 'FAIL'}")
        print(f"LogResult Dataclass: {'PASS' if test21 else 'FAIL'}")
        
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
