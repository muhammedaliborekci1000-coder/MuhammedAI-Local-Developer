"""
Quality Test: Enhanced Multi-File Editor
Multi-file editing gelişmiş özellikleri testleri.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.multi_file_editor import (
    MultiFileEditor,
    FileOperation,
    RiskLevel,
    FileChange,
    MultiFileChangePlan
)


def test_conflict_detection():
    """
    Test: Conflict detection.
    """
    print("=" * 70)
    print("TEST: Conflict Detection")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = os.path.join(temp_dir, "test.py")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('print("hello")')
        
        # Editor oluştur
        editor = MultiFileEditor(project_root=Path(temp_dir))
        
        # Plan oluştur
        plan = editor.create_plan(
            request="Test change",
            files=["test.py"],
            operations={"test.py": FileOperation.MODIFY}
        )
        
        # Dosyayı disk'te değiştir (conflict oluştur)
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('print("changed")')
        
        # Conflict detection
        conflicts = editor.detect_conflicts(plan)
        
        assert len(conflicts) > 0, "Conflict tespit edilmeli"
        assert "test.py" in conflicts, "test.py conflict olmalı"
        print(f"  Conflicts: {conflicts}")
        
        print("\n" + "=" * 70)
        print("PASS: Conflict detection")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_syntax_validation():
    """
    Test: Syntax validation.
    """
    print("=" * 70)
    print("TEST: Syntax Validation")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Editor oluştur
        editor = MultiFileEditor(project_root=Path(temp_dir))
        
        # Plan oluştur (syntax error ile)
        plan = editor.create_plan(
            request="Test change",
            files=["test.py"],
            operations={"test.py": FileOperation.CREATE}
        )
        
        # Syntax error içeren içerik
        plan.files["test.py"].proposed_content = 'def broken(:\n    pass'
        
        # Syntax validation
        syntax_errors = editor.validate_syntax(plan)
        
        assert len(syntax_errors) > 0, "Syntax error tespit edilmeli"
        assert "test.py" in syntax_errors, "test.py syntax error olmalı"
        print(f"  Syntax errors: {syntax_errors}")
        
        print("\n" + "=" * 70)
        print("PASS: Syntax validation")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_impact_analysis():
    """
    Test: Impact analysis.
    """
    print("=" * 70)
    print("TEST: Impact Analysis")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Editor oluştur
        editor = MultiFileEditor(project_root=Path(temp_dir))
        
        # Plan oluştur
        plan = editor.create_plan(
            request="Test change",
            files=["test.py", "utils.py"],
            operations={"test.py": FileOperation.MODIFY, "utils.py": FileOperation.MODIFY}
        )
        
        # Impact analysis
        impact = editor.analyze_impact(plan)
        
        assert "affected_files" in impact, "affected_files olmalı"
        assert "risk_score" in impact, "risk_score olmalı"
        assert impact["affected_files"] == 2, "2 dosya etkilenmeli"
        print(f"  Affected files: {impact['affected_files']}")
        print(f"  Risk score: {impact['risk_score']}")
        print(f"  Recommendations: {impact['recommendations']}")
        
        print("\n" + "=" * 70)
        print("PASS: Impact analysis")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_change_history():
    """
    Test: Change history tracking.
    """
    print("=" * 70)
    print("TEST: Change History Tracking")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = os.path.join(temp_dir, "test.py")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('print("hello")')
        
        # Editor oluştur
        editor = MultiFileEditor(project_root=Path(temp_dir))
        
        # Plan oluştur ve uygula (dry-run)
        plan = editor.create_plan(
            request="Test change",
            files=["test.py"],
            operations={"test.py": FileOperation.MODIFY},
            dry_run=True
        )
        
        plan.files["test.py"].proposed_content = 'print("changed")'
        
        # History'ye ekle
        editor.add_to_history(plan)
        
        # History al
        history = editor.get_change_history(limit=10)
        
        assert len(history) > 0, "History dolu olmalı"
        assert history[0]["plan_id"] == plan.plan_id, "Plan ID eşleşmeli"
        print(f"  History count: {len(history)}")
        print(f"  Last plan ID: {history[0]['plan_id']}")
        
        print("\n" + "=" * 70)
        print("PASS: Change history tracking")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_undo_functionality():
    """
    Test: Undo functionality.
    """
    print("=" * 70)
    print("TEST: Undo Functionality")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = os.path.join(temp_dir, "test.py")
        original_content = 'print("hello")'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(original_content)
        
        # Editor oluştur
        editor = MultiFileEditor(project_root=Path(temp_dir))
        
        # Plan oluştur
        plan = editor.create_plan(
            request="Test change",
            files=["test.py"],
            operations={"test.py": FileOperation.MODIFY}
        )
        
        new_content = 'print("changed")'
        plan.files["test.py"].proposed_content = new_content
        plan.files["test.py"].original_content = original_content
        
        # Dosyayı değiştir
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        # History'ye ekle
        editor.add_to_history(plan)
        
        # Undo
        undo_result = editor.undo_last_change()
        
        assert undo_result is not None, "Undo sonucu olmalı"
        assert undo_result["success"], "Undo başarılı olmalı"
        assert "test.py" in undo_result["reverted_files"], "Dosya revert edilmeli"
        print(f"  Reverted files: {undo_result['reverted_files']}")
        
        # Dosya içeriğini kontrol et
        current_content = Path(test_file).read_text(encoding='utf-8')
        assert current_content == original_content, "İçerik original olmalı"
        print(f"  Content restored: {current_content}")
        
        print("\n" + "=" * 70)
        print("PASS: Undo functionality")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_post_apply_verification():
    """
    Test: Post-apply verification.
    """
    print("=" * 70)
    print("TEST: Post-Apply Verification")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = os.path.join(temp_dir, "test.py")
        proposed_content = 'print("hello")'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(proposed_content)
        
        # Editor oluştur
        editor = MultiFileEditor(project_root=Path(temp_dir))
        
        # Plan oluştur
        plan = editor.create_plan(
            request="Test change",
            files=["test.py"],
            operations={"test.py": FileOperation.MODIFY}
        )
        
        plan.files["test.py"].proposed_content = proposed_content
        plan.files["test.py"].original_content = proposed_content
        
        # Verification
        verification = editor.verify_changes(plan)
        
        assert verification["verified"], "Verification başarılı olmalı"
        assert len(verification["errors"]) == 0, "Error olmamalı"
        print(f"  Verified: {verification['verified']}")
        print(f"  Errors: {verification['errors']}")
        
        print("\n" + "=" * 70)
        print("PASS: Post-apply verification")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_enhanced_apply_plan():
    """
    Test: Enhanced apply plan (with all validations).
    """
    print("=" * 70)
    print("TEST: Enhanced Apply Plan")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = os.path.join(temp_dir, "test.py")
        original_content = 'print("hello")'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(original_content)
        
        # Editor oluştur
        editor = MultiFileEditor(project_root=Path(temp_dir))
        
        # Plan oluştur
        plan = editor.create_plan(
            request="Test change",
            files=["test.py"],
            operations={"test.py": FileOperation.MODIFY},
            dry_run=True
        )
        
        plan.files["test.py"].proposed_content = 'print("changed")'
        plan.files["test.py"].original_content = original_content
        plan.approval_required = False
        
        # Apply (dry-run)
        result = editor.apply_plan(plan)
        
        assert result["success"], "Apply başarılı olmalı"
        assert result["dry_run"], "Dry-run olmalı"
        assert "impact" in result, "Impact analizi olmalı"
        print(f"  Success: {result['success']}")
        print(f"  Dry-run: {result['dry_run']}")
        print(f"  Impact: {result['impact']}")
        
        print("\n" + "=" * 70)
        print("PASS: Enhanced apply plan")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    try:
        test1 = test_conflict_detection()
        test2 = test_syntax_validation()
        test3 = test_impact_analysis()
        test4 = test_change_history()
        test5 = test_undo_functionality()
        test6 = test_post_apply_verification()
        test7 = test_enhanced_apply_plan()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Conflict Detection: {'PASS' if test1 else 'FAIL'}")
        print(f"Syntax Validation: {'PASS' if test2 else 'FAIL'}")
        print(f"Impact Analysis: {'PASS' if test3 else 'FAIL'}")
        print(f"Change History: {'PASS' if test4 else 'FAIL'}")
        print(f"Undo Functionality: {'PASS' if test5 else 'FAIL'}")
        print(f"Post-Apply Verification: {'PASS' if test6 else 'FAIL'}")
        print(f"Enhanced Apply Plan: {'PASS' if test7 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7])
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
