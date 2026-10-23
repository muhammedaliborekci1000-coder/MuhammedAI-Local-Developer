"""
Quality Test: Sort Imports
Sort imports system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.sort_imports import (
    SortImportsEngine,
    ImportType,
    SortOrder,
    ImportStatement,
    SortConfig,
    SortResult
)


def test_sort_imports():
    """
    Test: Sort imports.
    """
    print("=" * 70)
    print("TEST: Sort Imports")
    print("=" * 70)
    
    engine = SortImportsEngine()
    
    content = "import sys\nimport os\nimport json"
    result = engine.sort_imports(content)
    
    assert result.success, "Sıralama başarılı olmalı"
    assert result.imports_sorted > 0, "Import sıralanmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Imports sorted: {result.imports_sorted}")
    
    print("\n" + "=" * 70)
    print("PASS: Sort imports")
    print("=" * 70)


def test_sort_with_from_imports():
    """
    Test: Sort with from imports.
    """
    print("=" * 70)
    print("TEST: Sort With From Imports")
    print("=" * 70)
    
    engine = SortImportsEngine()
    
    content = "from os import path\nimport sys\nfrom json import loads"
    result = engine.sort_imports(content)
    
    assert result.success, "Sıralama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Sort with from imports")
    print("=" * 70)


def test_remove_duplicates():
    """
    Test: Remove duplicates.
    """
    print("=" * 70)
    print("TEST: Remove Duplicates")
    print("=" * 70)
    
    engine = SortImportsEngine()
    engine.config.remove_duplicates = True
    
    content = "import sys\nimport os\nimport sys"
    result = engine.sort_imports(content)
    
    assert result.success, "Sıralama başarılı olmalı"
    assert result.duplicates_removed > 0, "Duplicate kaldırılmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Duplicates removed: {result.duplicates_removed}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove duplicates")
    print("=" * 70)


def test_group_by_type():
    """
    Test: Group by type.
    """
    print("=" * 70)
    print("TEST: Group By Type")
    print("=" * 70)
    
    engine = SortImportsEngine()
    engine.config.group_by_type = True
    
    content = "import sys\nimport requests\nfrom . import module"
    result = engine.sort_imports(content)
    
    assert result.success, "Sıralama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Group by type")
    print("=" * 70)


def test_alphabetical_sort():
    """
    Test: Alphabetical sort.
    """
    print("=" * 70)
    print("TEST: Alphabetical Sort")
    print("=" * 70)
    
    engine = SortImportsEngine()
    engine.config.sort_order = SortOrder.ALPHABETICAL
    
    content = "import sys\nimport os\nimport json"
    result = engine.sort_imports(content)
    
    assert result.success, "Sıralama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Alphabetical sort")
    print("=" * 70)


def test_no_imports():
    """
    Test: No imports.
    """
    print("=" * 70)
    print("TEST: No Imports")
    print("=" * 70)
    
    engine = SortImportsEngine()
    
    content = "def test():\n    pass"
    result = engine.sort_imports(content)
    
    assert result.success, "Başarılı olmalı"
    assert result.imports_sorted == 0, "Import olmamalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: No imports")
    print("=" * 70)


def test_undo_sort():
    """
    Test: Undo sort.
    """
    print("=" * 70)
    print("TEST: Undo Sort")
    print("=" * 70)
    
    engine = SortImportsEngine()
    
    content = "import sys\nimport os"
    engine.sort_imports(content)
    result = engine.undo_sort()
    
    assert result.success, "Geri alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Undo sort")
    print("=" * 70)


def test_get_sort_history():
    """
    Test: Get sort history.
    """
    print("=" * 70)
    print("TEST: Get Sort History")
    print("=" * 70)
    
    engine = SortImportsEngine()
    
    engine.sort_imports("import sys\nimport os")
    history = engine.get_sort_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get sort history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = SortImportsEngine()
    
    engine.sort_imports("import sys\nimport os")
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_sort_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = SortImportsEngine()
    
    new_config = SortConfig(group_by_type=False)
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
    
    engine = SortImportsEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.group_by_type == True, "Config eşleşmeli"
    
    print(f"  Group by type: {config.group_by_type}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_import_type_enum():
    """
    Test: ImportType enum.
    """
    print("=" * 70)
    print("TEST: ImportType Enum")
    print("=" * 70)
    
    assert ImportType.STANDARD_LIBRARY.value == "standard_library"
    assert ImportType.THIRD_PARTY.value == "third_party"
    assert ImportType.LOCAL.value == "local"
    assert ImportType.BUILTIN.value == "builtin"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(ImportType)}")
    
    print("\n" + "=" * 70)
    print("PASS: ImportType enum")
    print("=" * 70)


def test_sort_order_enum():
    """
    Test: SortOrder enum.
    """
    print("=" * 70)
    print("TEST: SortOrder Enum")
    print("=" * 70)
    
    assert SortOrder.ALPHABETICAL.value == "alphabetical"
    assert SortOrder.LENGTH.value == "length"
    assert SortOrder.FREQUENCY.value == "frequency"
    assert SortOrder.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total orders: {len(SortOrder)}")
    
    print("\n" + "=" * 70)
    print("PASS: SortOrder enum")
    print("=" * 70)


def test_import_statement_dataclass():
    """
    Test: ImportStatement dataclass.
    """
    print("=" * 70)
    print("TEST: ImportStatement Dataclass")
    print("=" * 70)
    
    statement = ImportStatement(
        module_name="os",
        import_type=ImportType.STANDARD_LIBRARY,
        line_number=0
    )
    
    assert statement.module_name == "os", "Module name eşleşmeli"
    assert statement.import_type == ImportType.STANDARD_LIBRARY, "Import type eşleşmeli"
    
    print(f"  Module name: {statement.module_name}")
    print(f"  Import type: {statement.import_type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: ImportStatement dataclass")
    print("=" * 70)


def test_sort_config_dataclass():
    """
    Test: SortConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SortConfig Dataclass")
    print("=" * 70)
    
    config = SortConfig(
        group_by_type=True,
        remove_duplicates=True,
        remove_unused=False
    )
    
    assert config.group_by_type == True, "Group by type eşleşmeli"
    assert config.remove_duplicates == True, "Remove duplicates eşleşmeli"
    assert config.remove_unused == False, "Remove unused eşleşmeli"
    
    print(f"  Group by type: {config.group_by_type}")
    print(f"  Remove duplicates: {config.remove_duplicates}")
    print(f"  Remove unused: {config.remove_unused}")
    
    print("\n" + "=" * 70)
    print("PASS: SortConfig dataclass")
    print("=" * 70)


def test_sort_result_dataclass():
    """
    Test: SortResult dataclass.
    """
    print("=" * 70)
    print("TEST: SortResult Dataclass")
    print("=" * 70)
    
    result = SortResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: SortResult dataclass")
    print("=" * 70)


def test_detect_imports():
    """
    Test: Detect imports.
    """
    print("=" * 70)
    print("TEST: Detect Imports")
    print("=" * 70)
    
    engine = SortImportsEngine()
    
    content = "import sys\nimport os\nfrom json import loads"
    imports = engine._detect_imports(content)
    
    assert len(imports) > 0, "Import tespit edilmeli"
    
    print(f"  Imports detected: {len(imports)}")
    
    print("\n" + "=" * 70)
    print("PASS: Detect imports")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_sort_imports()
        test2 = test_sort_with_from_imports()
        test3 = test_remove_duplicates()
        test4 = test_group_by_type()
        test5 = test_alphabetical_sort()
        test6 = test_no_imports()
        test7 = test_undo_sort()
        test8 = test_get_sort_history()
        test9 = test_clear_history()
        test10 = test_update_config()
        test11 = test_get_config()
        test12 = test_import_type_enum()
        test13 = test_sort_order_enum()
        test14 = test_import_statement_dataclass()
        test15 = test_sort_config_dataclass()
        test16 = test_sort_result_dataclass()
        test17 = test_detect_imports()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Sort Imports: {'PASS' if test1 else 'FAIL'}")
        print(f"Sort With From Imports: {'PASS' if test2 else 'FAIL'}")
        print(f"Remove Duplicates: {'PASS' if test3 else 'FAIL'}")
        print(f"Group By Type: {'PASS' if test4 else 'FAIL'}")
        print(f"Alphabetical Sort: {'PASS' if test5 else 'FAIL'}")
        print(f"No Imports: {'PASS' if test6 else 'FAIL'}")
        print(f"Undo Sort: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Sort History: {'PASS' if test8 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test9 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test11 else 'FAIL'}")
        print(f"ImportType Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"SortOrder Enum: {'PASS' if test13 else 'FAIL'}")
        print(f"ImportStatement Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"SortConfig Dataclass: {'PASS' if test15 else 'FAIL'}")
        print(f"SortResult Dataclass: {'PASS' if test16 else 'FAIL'}")
        print(f"Detect Imports: {'PASS' if test17 else 'FAIL'}")
        
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
