"""
Quality Test: Organize Imports
Organize imports system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.organize_imports import (
    OrganizeImportsEngine,
    ImportGroup,
    ImportAction,
    ImportStatement,
    ImportEdit,
    OrganizeImportsResult
)


def test_organize_imports():
    """
    Test: Organize imports.
    """
    print("=" * 70)
    print("TEST: Organize Imports")
    print("=" * 70)
    
    code = """
import sys
import os
import re

def main():
    print(os.getcwd())
"""
    
    engine = OrganizeImportsEngine()
    result = engine.organize_imports(code, "python")
    
    assert result.success, "Organize imports başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Imports: {len(result.imports)}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Organize imports")
    print("=" * 70)


def test_sort_imports():
    """
    Test: Sort imports.
    """
    print("=" * 70)
    print("TEST: Sort Imports")
    print("=" * 70)
    
    code = """
import re
import os
import sys

def main():
    print(os.getcwd())
"""
    
    engine = OrganizeImportsEngine()
    result = engine.organize_imports(code, "python", sort_alphabetically=True)
    
    assert result.success, "Sort başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Imports sorted: {len(result.imports)}")
    
    print("\n" + "=" * 70)
    print("PASS: Sort imports")
    print("=" * 70)


def test_group_imports():
    """
    Test: Group imports.
    """
    print("=" * 70)
    print("TEST: Group Imports")
    print("=" * 70)
    
    code = """
import sys
import numpy as np
from .local_module import func

def main():
    pass
"""
    
    engine = OrganizeImportsEngine()
    result = engine.organize_imports(code, "python", group_imports=True)
    
    assert result.success, "Group başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Imports grouped: {len(result.imports)}")
    
    for imp in result.imports:
        print(f"    {imp.module}: {imp.group.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Group imports")
    print("=" * 70)


def test_remove_unused_imports():
    """
    Test: Remove unused imports.
    """
    print("=" * 70)
    print("TEST: Remove Unused Imports")
    print("=" * 70)
    
    code = """
import sys
import os
import re

def main():
    print(os.getcwd())
"""
    
    engine = OrganizeImportsEngine()
    result = engine.organize_imports(code, "python", remove_unused=True)
    
    assert result.success, "Remove unused başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Unused imports: {len(result.unused_imports)}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove unused imports")
    print("=" * 70)


def test_parse_import_line():
    """
    Test: Parse import line.
    """
    print("=" * 70)
    print("TEST: Parse Import Line")
    print("=" * 70)
    
    engine = OrganizeImportsEngine()
    
    # Simple import
    stmt1 = engine._parse_import_line("import os", 0)
    assert stmt1 is not None, "Import parse edilmeli"
    assert stmt1.module == "os", "Module eşleşmeli"
    
    # Import with alias
    stmt2 = engine._parse_import_line("import numpy as np", 0)
    assert stmt2 is not None, "Import parse edilmeli"
    assert stmt2.alias == "np", "Alias eşleşmeli"
    
    # From import
    stmt3 = engine._parse_import_line("from datetime import datetime", 0)
    assert stmt3 is not None, "From import parse edilmeli"
    assert stmt3.is_from == True, "From import olmalı"
    
    print(f"  Simple import: {stmt1.module if stmt1 else 'N/A'}")
    print(f"  Import with alias: {stmt2.alias if stmt2 else 'N/A'}")
    print(f"  From import: {stmt3.is_from if stmt3 else 'N/A'}")
    
    print("\n" + "=" * 70)
    print("PASS: Parse import line")
    print("=" * 70)


def test_detect_missing_imports():
    """
    Test: Detect missing imports.
    """
    print("=" * 70)
    print("TEST: Detect Missing Imports")
    print("=" * 70)
    
    code = """
def main():
    print(os.getcwd())
"""
    
    engine = OrganizeImportsEngine()
    missing = engine.detect_missing_imports(code)
    
    print(f"  Missing imports: {len(missing)}")
    for imp in missing:
        print(f"    {imp}")
    
    print("\n" + "=" * 70)
    print("PASS: Detect missing imports")
    print("=" * 70)


def test_add_missing_imports():
    """
    Test: Add missing imports.
    """
    print("=" * 70)
    print("TEST: Add Missing Imports")
    print("=" * 70)
    
    code = """
def main():
    print(os.getcwd())
"""
    
    engine = OrganizeImportsEngine()
    missing = engine.detect_missing_imports(code)
    
    if missing:
        fixed_code, result = engine.add_missing_imports(code, missing)
        
        assert result.success, "Add missing başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Added imports: {len(missing)}")
    
    print("\n" + "=" * 70)
    print("PASS: Add missing imports")
    print("=" * 70)


def test_preview_organize():
    """
    Test: Preview organize.
    """
    print("=" * 70)
    print("TEST: Preview Organize")
    print("=" * 70)
    
    code = """
import sys
import os

def main():
    print(os.getcwd())
"""
    
    engine = OrganizeImportsEngine()
    result = engine.preview_organize(code, "python")
    
    assert result.success, "Preview başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Preview code length: {len(result.organized_code)}")
    
    print("\n" + "=" * 70)
    print("PASS: Preview organize")
    print("=" * 70)


def test_import_group_enum():
    """
    Test: ImportGroup enum.
    """
    print("=" * 70)
    print("TEST: ImportGroup Enum")
    print("=" * 70)
    
    assert ImportGroup.STANDARD_LIBRARY.value == "standard_library"
    assert ImportGroup.THIRD_PARTY.value == "third_party"
    assert ImportGroup.LOCAL.value == "local"
    assert ImportGroup.UNKNOWN.value == "unknown"
    
    print(f"  All enum values verified")
    print(f"  Total groups: {len(ImportGroup)}")
    
    print("\n" + "=" * 70)
    print("PASS: ImportGroup enum")
    print("=" * 70)


def test_import_action_enum():
    """
    Test: ImportAction enum.
    """
    print("=" * 70)
    print("TEST: ImportAction Enum")
    print("=" * 70)
    
    assert ImportAction.ADD.value == "add"
    assert ImportAction.REMOVE.value == "remove"
    assert ImportAction.SORT.value == "sort"
    assert ImportAction.GROUP.value == "group"
    assert ImportAction.FORMAT.value == "format"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(ImportAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: ImportAction enum")
    print("=" * 70)


def test_import_statement_dataclass():
    """
    Test: ImportStatement dataclass.
    """
    print("=" * 70)
    print("TEST: ImportStatement Dataclass")
    print("=" * 70)
    
    stmt = ImportStatement(
        module="os",
        alias=None,
        names=[],
        is_from=False,
        line=0,
        group=ImportGroup.STANDARD_LIBRARY
    )
    
    assert stmt.module == "os", "Module eşleşmeli"
    assert stmt.group == ImportGroup.STANDARD_LIBRARY, "Group eşleşmeli"
    
    print(f"  Module: {stmt.module}")
    print(f"  Group: {stmt.group.value}")
    print(f"  Line: {stmt.line}")
    
    print("\n" + "=" * 70)
    print("PASS: ImportStatement dataclass")
    print("=" * 70)


def test_import_edit_dataclass():
    """
    Test: ImportEdit dataclass.
    """
    print("=" * 70)
    print("TEST: ImportEdit Dataclass")
    print("=" * 70)
    
    edit = ImportEdit(
        start_line=0,
        end_line=1,
        old_text="import sys",
        new_text="import os"
    )
    
    assert edit.old_text == "import sys", "Old text eşleşmeli"
    assert edit.new_text == "import os", "New text eşleşmeli"
    
    print(f"  Old text: {edit.old_text}")
    print(f"  New text: {edit.new_text}")
    print(f"  Start line: {edit.start_line}")
    
    print("\n" + "=" * 70)
    print("PASS: ImportEdit dataclass")
    print("=" * 70)


def test_organize_imports_result_dataclass():
    """
    Test: OrganizeImportsResult dataclass.
    """
    print("=" * 70)
    print("TEST: OrganizeImportsResult Dataclass")
    print("=" * 70)
    
    result = OrganizeImportsResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.imports, list), "Imports list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Imports: {len(result.imports)}")
    
    print("\n" + "=" * 70)
    print("PASS: OrganizeImportsResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_organize_imports()
        test2 = test_sort_imports()
        test3 = test_group_imports()
        test4 = test_remove_unused_imports()
        test5 = test_parse_import_line()
        test6 = test_detect_missing_imports()
        test7 = test_add_missing_imports()
        test8 = test_preview_organize()
        test9 = test_import_group_enum()
        test10 = test_import_action_enum()
        test11 = test_import_statement_dataclass()
        test12 = test_import_edit_dataclass()
        test13 = test_organize_imports_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Organize Imports: {'PASS' if test1 else 'FAIL'}")
        print(f"Sort Imports: {'PASS' if test2 else 'FAIL'}")
        print(f"Group Imports: {'PASS' if test3 else 'FAIL'}")
        print(f"Remove Unused Imports: {'PASS' if test4 else 'FAIL'}")
        print(f"Parse Import Line: {'PASS' if test5 else 'FAIL'}")
        print(f"Detect Missing Imports: {'PASS' if test6 else 'FAIL'}")
        print(f"Add Missing Imports: {'PASS' if test7 else 'FAIL'}")
        print(f"Preview Organize: {'PASS' if test8 else 'FAIL'}")
        print(f"ImportGroup Enum: {'PASS' if test9 else 'FAIL'}")
        print(f"ImportAction Enum: {'PASS' if test10 else 'FAIL'}")
        print(f"ImportStatement Dataclass: {'PASS' if test11 else 'FAIL'}")
        print(f"ImportEdit Dataclass: {'PASS' if test12 else 'FAIL'}")
        print(f"OrganizeImportsResult Dataclass: {'PASS' if test13 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13])
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
