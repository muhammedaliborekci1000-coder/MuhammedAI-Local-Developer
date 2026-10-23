"""
Quality Test: Git Blame
Git blame system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.git_blame import (
    GitBlameEngine,
    BlameFormat,
    BlameDate,
    BlameInfo,
    BlameConfig,
    BlameResult
)
from datetime import datetime


def test_blame_file():
    """
    Test: Blame file.
    """
    print("=" * 70)
    print("TEST: Blame File")
    print("=" * 70)
    
    engine = GitBlameEngine()
    
    content = "line1\nline2\nline3"
    result = engine.blame_file("test.py", content)
    
    assert result.success, "Blame başarılı olmalı"
    assert result.total_lines == 3, "3 satır olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total lines: {result.total_lines}")
    
    print("\n" + "=" * 70)
    print("PASS: Blame file")
    print("=" * 70)


def test_blame_range():
    """
    Test: Blame range.
    """
    print("=" * 70)
    print("TEST: Blame Range")
    print("=" * 70)
    
    engine = GitBlameEngine()
    
    content = "line1\nline2\nline3\nline4\nline5"
    result = engine.blame_range("test.py", 2, 4, content)
    
    assert result.success, "Range blame başarılı olmalı"
    assert result.total_lines == 3, "3 satır olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total lines: {result.total_lines}")
    
    print("\n" + "=" * 70)
    print("PASS: Blame range")
    print("=" * 70)


def test_get_blame_for_line():
    """
    Test: Get blame for line.
    """
    print("=" * 70)
    print("TEST: Get Blame For Line")
    print("=" * 70)
    
    engine = GitBlameEngine()
    
    content = "line1\nline2\nline3"
    result = engine.get_blame_for_line("test.py", 2, content)
    
    assert result.success, "Satır blame başarılı olmalı"
    assert result.total_lines == 1, "1 satır olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total lines: {result.total_lines}")
    
    print("\n" + "=" * 70)
    print("PASS: Get blame for line")
    print("=" * 70)


def test_format_blame():
    """
    Test: Format blame.
    """
    print("=" * 70)
    print("TEST: Format Blame")
    print("=" * 70)
    
    engine = GitBlameEngine()
    
    blame_info = BlameInfo(
        commit_hash="abc123",
        author="Developer",
        author_email="dev@example.com",
        author_date=datetime.now(),
        commit_date=datetime.now(),
        summary="Test commit"
    )
    
    formatted = engine.format_blame(blame_info)
    
    assert formatted is not None, "Formatlanmış metin olmalı"
    assert "Developer" in formatted, "Yazar olmalı"
    
    print(f"  Formatted: {formatted}")
    
    print("\n" + "=" * 70)
    print("PASS: Format blame")
    print("=" * 70)


def test_get_author_statistics():
    """
    Test: Get author statistics.
    """
    print("=" * 70)
    print("TEST: Get Author Statistics")
    print("=" * 70)
    
    engine = GitBlameEngine()
    
    content = "line1\nline2\nline3"
    engine.blame_file("test.py", content)
    
    stats = engine.get_author_statistics("test.py")
    
    assert len(stats) > 0, "İstatistik olmalı"
    
    print(f"  Statistics: {stats}")
    
    print("\n" + "=" * 70)
    print("PASS: Get author statistics")
    print("=" * 70)


def test_get_commit_statistics():
    """
    Test: Get commit statistics.
    """
    print("=" * 70)
    print("TEST: Get Commit Statistics")
    print("=" * 70)
    
    engine = GitBlameEngine()
    
    content = "line1\nline2\nline3"
    engine.blame_file("test.py", content)
    
    stats = engine.get_commit_statistics("test.py")
    
    assert len(stats) > 0, "İstatistik olmalı"
    
    print(f"  Statistics: {stats}")
    
    print("\n" + "=" * 70)
    print("PASS: Get commit statistics")
    print("=" * 70)


def test_filter_by_author():
    """
    Test: Filter by author.
    """
    print("=" * 70)
    print("TEST: Filter By Author")
    print("=" * 70)
    
    engine = GitBlameEngine()
    
    content = "line1\nline2\nline3"
    engine.blame_file("test.py", content)
    
    filtered = engine.filter_by_author("test.py", "Developer")
    
    assert len(filtered) > 0, "Filtrelenmiş sonuçlar olmalı"
    
    print(f"  Filtered: {len(filtered)}")
    
    print("\n" + "=" * 70)
    print("PASS: Filter by author")
    print("=" * 70)


def test_filter_by_date_range():
    """
    Test: Filter by date range.
    """
    print("=" * 70)
    print("TEST: Filter By Date Range")
    print("=" * 70)
    
    engine = GitBlameEngine()
    
    content = "line1\nline2\nline3"
    engine.blame_file("test.py", content)
    
    start_date = datetime.now().replace(year=2020)
    end_date = datetime.now()
    
    filtered = engine.filter_by_date_range("test.py", start_date, end_date)
    
    assert len(filtered) > 0, "Filtrelenmiş sonuçlar olmalı"
    
    print(f"  Filtered: {len(filtered)}")
    
    print("\n" + "=" * 70)
    print("PASS: Filter by date range")
    print("=" * 70)


def test_clear_cache():
    """
    Test: Clear cache.
    """
    print("=" * 70)
    print("TEST: Clear Cache")
    print("=" * 70)
    
    engine = GitBlameEngine()
    
    content = "line1"
    engine.blame_file("test.py", content)
    
    result = engine.clear_cache("test.py")
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear cache")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = GitBlameEngine()
    
    new_config = BlameConfig(format=BlameFormat.COMPACT)
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
    
    engine = GitBlameEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.format == BlameFormat.DEFAULT, "Config eşleşmeli"
    
    print(f"  Format: {config.format.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_blame_format_enum():
    """
    Test: BlameFormat enum.
    """
    print("=" * 70)
    print("TEST: BlameFormat Enum")
    print("=" * 70)
    
    assert BlameFormat.DEFAULT.value == "default"
    assert BlameFormat.DETAILED.value == "detailed"
    assert BlameFormat.COMPACT.value == "compact"
    assert BlameFormat.MINIMAL.value == "minimal"
    
    print(f"  All enum values verified")
    print(f"  Total formats: {len(BlameFormat)}")
    
    print("\n" + "=" * 70)
    print("PASS: BlameFormat enum")
    print("=" * 70)


def test_blame_date_enum():
    """
    Test: BlameDate enum.
    """
    print("=" * 70)
    print("TEST: BlameDate Enum")
    print("=" * 70)
    
    assert BlameDate.ISO.value == "iso"
    assert BlameDate.RELATIVE.value == "relative"
    assert BlameDate.SHORT.value == "short"
    assert BlameDate.LONG.value == "long"
    
    print(f"  All enum values verified")
    print(f"  Total date formats: {len(BlameDate)}")
    
    print("\n" + "=" * 70)
    print("PASS: BlameDate enum")
    print("=" * 70)


def test_blame_info_dataclass():
    """
    Test: BlameInfo dataclass.
    """
    print("=" * 70)
    print("TEST: BlameInfo Dataclass")
    print("=" * 70)
    
    blame_info = BlameInfo(
        commit_hash="abc123",
        author="Developer",
        author_email="dev@example.com",
        author_date=datetime.now(),
        commit_date=datetime.now(),
        line_number=5
    )
    
    assert blame_info.commit_hash == "abc123", "Commit hash eşleşmeli"
    assert blame_info.author == "Developer", "Author eşleşmeli"
    assert blame_info.line_number == 5, "Line number eşleşmeli"
    
    print(f"  Commit hash: {blame_info.commit_hash}")
    print(f"  Author: {blame_info.author}")
    print(f"  Line number: {blame_info.line_number}")
    
    print("\n" + "=" * 70)
    print("PASS: BlameInfo dataclass")
    print("=" * 70)


def test_blame_config_dataclass():
    """
    Test: BlameConfig dataclass.
    """
    print("=" * 70)
    print("TEST: BlameConfig Dataclass")
    print("=" * 70)
    
    config = BlameConfig(
        format=BlameFormat.DEFAULT,
        date_format=BlameDate.RELATIVE,
        show_author=True
    )
    
    assert config.format == BlameFormat.DEFAULT, "Format eşleşmeli"
    assert config.date_format == BlameDate.RELATIVE, "Date format eşleşmeli"
    assert config.show_author == True, "Show author eşleşmeli"
    
    print(f"  Format: {config.format.value}")
    print(f"  Date format: {config.date_format.value}")
    print(f"  Show author: {config.show_author}")
    
    print("\n" + "=" * 70)
    print("PASS: BlameConfig dataclass")
    print("=" * 70)


def test_blame_result_dataclass():
    """
    Test: BlameResult dataclass.
    """
    print("=" * 70)
    print("TEST: BlameResult Dataclass")
    print("=" * 70)
    
    result = BlameResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.blame_info, list), "Blame info list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Blame info: {len(result.blame_info)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: BlameResult dataclass")
    print("=" * 70)


def test_cache_functionality():
    """
    Test: Cache functionality.
    """
    print("=" * 70)
    print("TEST: Cache Functionality")
    print("=" * 70)
    
    engine = GitBlameEngine()
    
    content = "line1\nline2\nline3"
    
    # İlk çağrı
    result1 = engine.blame_file("test.py", content)
    assert result1.success, "İlk çağrı başarılı olmalı"
    
    # İkinci çağrı (cache'den)
    result2 = engine.blame_file("test.py", content)
    assert result2.success, "Cache'den alma başarılı olmalı"
    assert "cache" in result2.message.lower(), "Cache mesajı olmalı"
    
    print(f"  First call: {result1.message}")
    print(f"  Second call: {result2.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Cache functionality")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_blame_file()
        test2 = test_blame_range()
        test3 = test_get_blame_for_line()
        test4 = test_format_blame()
        test5 = test_get_author_statistics()
        test6 = test_get_commit_statistics()
        test7 = test_filter_by_author()
        test8 = test_filter_by_date_range()
        test9 = test_clear_cache()
        test10 = test_update_config()
        test11 = test_get_config()
        test12 = test_blame_format_enum()
        test13 = test_blame_date_enum()
        test14 = test_blame_info_dataclass()
        test15 = test_blame_config_dataclass()
        test16 = test_blame_result_dataclass()
        test17 = test_cache_functionality()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Blame File: {'PASS' if test1 else 'FAIL'}")
        print(f"Blame Range: {'PASS' if test2 else 'FAIL'}")
        print(f"Get Blame For Line: {'PASS' if test3 else 'FAIL'}")
        print(f"Format Blame: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Author Statistics: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Commit Statistics: {'PASS' if test6 else 'FAIL'}")
        print(f"Filter By Author: {'PASS' if test7 else 'FAIL'}")
        print(f"Filter By Date Range: {'PASS' if test8 else 'FAIL'}")
        print(f"Clear Cache: {'PASS' if test9 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test11 else 'FAIL'}")
        print(f"BlameFormat Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"BlameDate Enum: {'PASS' if test13 else 'FAIL'}")
        print(f"BlameInfo Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"BlameConfig Dataclass: {'PASS' if test15 else 'FAIL'}")
        print(f"BlameResult Dataclass: {'PASS' if test16 else 'FAIL'}")
        print(f"Cache Functionality: {'PASS' if test17 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17])
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
