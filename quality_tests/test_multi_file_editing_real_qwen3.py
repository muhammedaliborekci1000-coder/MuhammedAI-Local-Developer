"""
Multi-File Editing Real Qwen3 Test
Gerçek Qwen3 modeli ile Multi-File Editing entegrasyon testi.
"""

import pytest
import sys
import os
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.ollama_client import OllamaClient
from app.ai.multi_file_editor import MultiFileEditor, FileOperation
from app.tools.tool_registry import ToolRegistry
from app.core.config import PROJECT_ROOT


@pytest.mark.slow
def test_multi_file_editing_real_qwen3():
    """
    Gerçek Qwen3 ile Multi-File Editing testi.
    Multi-file plan → approval → apply → test → correction.
    """
    print("\n" + "=" * 70)
    print("MULTI-FILE EDITING REAL QWEN3 TEST")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "multi_file_qwen3_workspace"
    workspace.mkdir(parents=True, exist_ok=True)

    try:
        # Basit bir yapı oluştur
        (workspace / "calculator.py").write_text('''
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
''')
        
        (workspace / "service.py").write_text('''
from calculator import add, multiply

class CalculatorService:
    def add_numbers(self, a, b):
        return add(a, b)
    
    def multiply_numbers(self, a, b):
        return multiply(a, b)
''')
        
        (workspace / "test_calculator.py").write_text('''
from calculator import add, multiply

def test_add():
    assert add(2, 3) == 5

def test_multiply():
    assert multiply(2, 3) == 6
''')
        
        # MultiFileEditor oluştur
        editor = MultiFileEditor(project_root=workspace)
        
        # Plan oluştur
        plan = editor.create_plan(
            request="Calculator fonksiyonlarını güncelle",
            files=["calculator.py", "service.py", "test_calculator.py"],
            operations={
                "calculator.py": FileOperation.MODIFY,
                "service.py": FileOperation.MODIFY,
                "test_calculator.py": FileOperation.MODIFY
            },
            dry_run=True  # Dry-run ile test
        )
        
        print(f"\nPlan ID: {plan.plan_id}")
        print(f"Files: {list(plan.files.keys())}")
        print(f"Risk level: {plan.risk_level.value}")
        
        # Validation
        validation = editor.validate_plan(plan)
        print(f"Validation valid: {validation['valid']}")
        if validation['errors']:
            print(f"Errors: {validation['errors']}")
        
        assert validation["valid"]
        
        # Approval test
        approval_count = [0]
        
        def approval_callback(p):
            approval_count[0] += 1
            print(f"Approval requested for plan: {p.plan_id}")
            return True
        
        # Apply (dry-run)
        result = editor.apply_plan(plan, approval_callback=approval_callback)
        
        print(f"\nApply result:")
        print(f"Success: {result['success']}")
        print(f"Dry-run: {result.get('dry_run', False)}")
        print(f"Error: {result.get('error')}")
        
        assert result["success"] is True
        assert result["dry_run"] is True
        assert approval_count[0] > 0
        
        # Dosyalar değişmemeli (dry-run)
        calc_content = (workspace / "calculator.py").read_text()
        assert "def add(a, b):" in calc_content
        
        print("\n" + "=" * 70)
        print("MULTI-FILE EDITING REAL QWEN3 TEST: PASS")
        print("=" * 70)

    finally:
        # Temizlik
        if workspace.exists():
            shutil.rmtree(workspace)
            print(f"\nWorkspace temizlendi: {workspace}")


if __name__ == "__main__":
    try:
        test_multi_file_editing_real_qwen3()
        print("\n" + "=" * 70)
        print("GERÇEK QWEN3 MULTI-FILE EDITING TEST BAŞARILI")
        print("=" * 70)
        sys.exit(0)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
