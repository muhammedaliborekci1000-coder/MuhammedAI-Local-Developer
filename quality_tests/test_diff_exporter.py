"""
Quality Test: Diff Exporter
Diff exporter system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.diff_exporter import (
    DiffExporterEngine,
    ExportFormat,
    ExportScope,
    ExportAction,
    ExportOptions,
    ExportResult,
    ExportConfig
)


def test_export():
    """
    Test: Export.
    """
    print("=" * 70)
    print("TEST: Export")
    print("=" * 70)
    
    engine = DiffExporterEngine()
    diff_content = ["Line 1", "Line 2", "Line 3"]
    
    result = engine.export(diff_content)
    
    assert result.success, "Dışa aktarma başarılı olmalı"
    assert result.action == ExportAction.EXPORT.value, "Action eşleşmeli"
    assert result.exported_content is not None, "İçerik olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Format: {result.format}")
    print(f"  Total lines: {result.total_lines}")
    
    print("\n" + "=" * 70)
    print("PASS: Export")
    print("=" * 70)


def test_export_as():
    """
    Test: Export as.
    """
    print("=" * 70)
    print("TEST: Export As")
    print("=" * 70)
    
    engine = DiffExporterEngine()
    diff_content = ["Line 1", "Line 2", "Line 3"]
    
    result = engine.export_as(ExportFormat.HTML, diff_content)
    
    assert result.success, "Dışa aktarma başarılı olmalı"
    assert result.action == ExportAction.EXPORT_AS.value, "Action eşleşmeli"
    assert result.format == "html", "Format eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Format: {result.format}")
    
    print("\n" + "=" * 70)
    print("PASS: Export as")
    print("=" * 70)


def test_export_to_file():
    """
    Test: Export to file.
    """
    print("=" * 70)
    print("TEST: Export To File")
    print("=" * 70)
    
    engine = DiffExporterEngine()
    diff_content = ["Line 1", "Line 2", "Line 3"]
    
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        temp_path = f.name
    
    try:
        result = engine.export_to_file(temp_path, diff_content)
        
        assert result.success, "Dışa aktarma başarılı olmalı"
        assert result.action == ExportAction.EXPORT_TO_FILE.value, "Action eşleşmeli"
        assert result.file_path == temp_path, "Dosya yolu eşleşmeli"
        
        print(f"  Success: {result.success}")
        print(f"  File path: {result.file_path}")
        
        print("\n" + "=" * 70)
        print("PASS: Export to file")
        print("=" * 70)
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_export_to_clipboard():
    """
    Test: Export to clipboard.
    """
    print("=" * 70)
    print("TEST: Export To Clipboard")
    print("=" * 70)
    
    engine = DiffExporterEngine()
    diff_content = ["Line 1", "Line 2", "Line 3"]
    
    result = engine.export_to_clipboard(diff_content)
    
    # pyperclip yüklü olmayabilir, bu yüzden sadece kontrol et
    if result.success:
        assert result.action == ExportAction.EXPORT_TO_CLIPBOARD.value, "Action eşleşmeli"
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
    else:
        print(f"  Skipped (pyperclip not available)")
    
    print("\n" + "=" * 70)
    print("PASS: Export to clipboard")
    print("=" * 70)


def test_set_diff_content():
    """
    Test: Set diff content.
    """
    print("=" * 70)
    print("TEST: Set Diff Content")
    print("=" * 70)
    
    engine = DiffExporterEngine()
    diff_content = ["Line 1", "Line 2", "Line 3"]
    file_paths = ["file1.txt", "file2.txt"]
    
    engine.set_diff_content(diff_content, file_paths)
    
    assert len(engine.diff_content) == 3, "İçerik eşleşmeli"
    assert len(engine.file_paths) == 2, "Dosya yolları eşleşmeli"
    
    print(f"  Diff content: {len(engine.diff_content)}")
    print(f"  File paths: {len(engine.file_paths)}")
    
    print("\n" + "=" * 70)
    print("PASS: Set diff content")
    print("=" * 70)


def test_get_export_history():
    """
    Test: Get export history.
    """
    print("=" * 70)
    print("TEST: Get Export History")
    print("=" * 70)
    
    engine = DiffExporterEngine()
    diff_content = ["Line 1", "Line 2", "Line 3"]
    engine.export(diff_content)
    
    history = engine.get_export_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get export history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = DiffExporterEngine()
    diff_content = ["Line 1", "Line 2", "Line 3"]
    engine.export(diff_content)
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_export_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_get_statistics():
    """
    Test: Get statistics.
    """
    print("=" * 70)
    print("TEST: Get Statistics")
    print("=" * 70)
    
    engine = DiffExporterEngine()
    diff_content = ["Line 1", "Line 2", "Line 3"]
    engine.set_diff_content(diff_content, ["file1.txt"])
    
    stats = engine.get_statistics()
    
    assert stats is not None, "İstatistikler olmalı"
    assert stats["total_lines"] == 3, "Toplam satır 3 olmalı"
    
    print(f"  Total lines: {stats['total_lines']}")
    print(f"  Total files: {stats['total_files']}")
    
    print("\n" + "=" * 70)
    print("PASS: Get statistics")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = DiffExporterEngine()
    
    new_config = ExportConfig(format=ExportFormat.HTML)
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
    
    engine = DiffExporterEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.format == ExportFormat.TEXT, "Format eşleşmeli"
    
    print(f"  Format: {config.format.value}")
    print(f"  Scope: {config.scope.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_export_format_enum():
    """
    Test: ExportFormat enum.
    """
    print("=" * 70)
    print("TEST: ExportFormat Enum")
    print("=" * 70)
    
    assert ExportFormat.TEXT.value == "text"
    assert ExportFormat.HTML.value == "html"
    assert ExportFormat.MARKDOWN.value == "markdown"
    assert ExportFormat.JSON.value == "json"
    assert ExportFormat.PDF.value == "pdf"
    assert ExportFormat.PATCH.value == "patch"
    assert ExportFormat.UNIFIED.value == "unified"
    assert ExportFormat.SIDE_BY_SIDE.value == "side_by_side"
    
    print(f"  All enum values verified")
    print(f"  Total formats: {len(ExportFormat)}")
    
    print("\n" + "=" * 70)
    print("PASS: ExportFormat enum")
    print("=" * 70)


def test_export_scope_enum():
    """
    Test: ExportScope enum.
    """
    print("=" * 70)
    print("TEST: ExportScope Enum")
    print("=" * 70)
    
    assert ExportScope.ALL_FILES.value == "all_files"
    assert ExportScope.CURRENT_FILE.value == "current_file"
    assert ExportScope.SELECTED_HUNKS.value == "selected_hunks"
    assert ExportScope.SELECTED_LINES.value == "selected_lines"
    assert ExportScope.VISIBLE_AREA.value == "visible_area"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(ExportScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: ExportScope enum")
    print("=" * 70)


def test_export_action_enum():
    """
    Test: ExportAction enum.
    """
    print("=" * 70)
    print("TEST: ExportAction Enum")
    print("=" * 70)
    
    assert ExportAction.EXPORT.value == "export"
    assert ExportAction.EXPORT_AS.value == "export_as"
    assert ExportAction.EXPORT_TO_FILE.value == "export_to_file"
    assert ExportAction.EXPORT_TO_CLIPBOARD.value == "export_to_clipboard"
    assert ExportAction.EXPORT_TO_EMAIL.value == "export_to_email"
    assert ExportAction.PRINT.value == "print"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(ExportAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: ExportAction enum")
    print("=" * 70)


def test_export_options_dataclass():
    """
    Test: ExportOptions dataclass.
    """
    print("=" * 70)
    print("TEST: ExportOptions Dataclass")
    print("=" * 70)
    
    options = ExportOptions(
        include_line_numbers=False,
        include_context=False
    )
    
    assert options.include_line_numbers == False, "Line numbers eşleşmeli"
    assert options.include_context == False, "Context eşleşmeli"
    
    print(f"  Include line numbers: {options.include_line_numbers}")
    print(f"  Include context: {options.include_context}")
    
    print("\n" + "=" * 70)
    print("PASS: ExportOptions dataclass")
    print("=" * 70)


def test_export_config_dataclass():
    """
    Test: ExportConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ExportConfig Dataclass")
    print("=" * 70)
    
    config = ExportConfig(
        format=ExportFormat.HTML,
        scope=ExportScope.CURRENT_FILE
    )
    
    assert config.format == ExportFormat.HTML, "Format eşleşmeli"
    assert config.scope == ExportScope.CURRENT_FILE, "Scope eşleşmeli"
    
    print(f"  Format: {config.format.value}")
    print(f"  Scope: {config.scope.value}")
    
    print("\n" + "=" * 70)
    print("PASS: ExportConfig dataclass")
    print("=" * 70)


def test_export_result_dataclass():
    """
    Test: ExportResult dataclass.
    """
    print("=" * 70)
    print("TEST: ExportResult Dataclass")
    print("=" * 70)
    
    result = ExportResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ExportResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_export()
        test2 = test_export_as()
        test3 = test_export_to_file()
        test4 = test_export_to_clipboard()
        test5 = test_set_diff_content()
        test6 = test_get_export_history()
        test7 = test_clear_history()
        test8 = test_get_statistics()
        test9 = test_update_config()
        test10 = test_get_config()
        test11 = test_export_format_enum()
        test12 = test_export_scope_enum()
        test13 = test_export_action_enum()
        test14 = test_export_options_dataclass()
        test15 = test_export_config_dataclass()
        test16 = test_export_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Export: {'PASS' if test1 else 'FAIL'}")
        print(f"Export As: {'PASS' if test2 else 'FAIL'}")
        print(f"Export To File: {'PASS' if test3 else 'FAIL'}")
        print(f"Export To Clipboard: {'PASS' if test4 else 'FAIL'}")
        print(f"Set Diff Content: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Export History: {'PASS' if test6 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Statistics: {'PASS' if test8 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test10 else 'FAIL'}")
        print(f"ExportFormat Enum: {'PASS' if test11 else 'FAIL'}")
        print(f"ExportScope Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"ExportAction Enum: {'PASS' if test13 else 'FAIL'}")
        print(f"ExportOptions Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"ExportConfig Dataclass: {'PASS' if test15 else 'FAIL'}")
        print(f"ExportResult Dataclass: {'PASS' if test16 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16])
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
