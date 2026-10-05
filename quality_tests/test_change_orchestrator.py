"""
TEST A-H: ChangeOrchestrator Tests
Tests ChangeOrchestrator's deterministic workflow
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.change_orchestrator import ChangeOrchestrator, OrchestratorState
from app.tools.change_workflow import ChangeWorkflow
from app.tools.tool_registry import ToolRegistry
from app.core.config import PROJECT_ROOT


def setup_test_files():
    """Test dosyalarını oluştur"""
    workspace = PROJECT_ROOT / "quality_tests" / "e2e_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    
    agent_file = workspace / "agent_task.py"
    test_file = workspace / "test_agent_task.py"
    
    agent_file.write_text('def greet():\n    return "Merhaba"\n', encoding='utf-8')
    test_file.write_text('from agent_task import greet\n\ndef test_greet():\n    assert greet() == "Merhaba Muhammed"\n', encoding='utf-8')
    
    return agent_file, test_file


def cleanup_test_files():
    """Test dosyalarını temizle"""
    workspace = PROJECT_ROOT / "quality_tests" / "e2e_workspace"
    if workspace.exists():
        import shutil
        shutil.rmtree(workspace)


def test_a_approval_true():
    """
    TEST A — Approval True
    Beklenen: create_plan → approval=True → apply → backup → patch → syntax → test → COMPLETE
    """
    print("=" * 70)
    print("TEST A — Approval True")
    print("=" * 70)
    
    agent_file, test_file = setup_test_files()
    
    try:
        # Callback
        approval_log = []
        def approval_callback(tool_name, arguments):
            approval_log.append((tool_name, arguments, True))
            return True
        
        # Orkestratör
        workflow = ChangeWorkflow()
        orchestrator = ChangeOrchestrator(workflow, approval_callback)
        
        # Plan oluştur
        result = orchestrator.create_plan(
            file_path="quality_tests/e2e_workspace/agent_task.py",
            problem="greet fonksiyonunun mesajını değiştirmek"
        )
        
        print(f"Plan sonucu: {result.get('success')}")
        print(f"Plan geçerli: {result.get('result', {}).get('validation', {}).get('valid')}")
        print(f"Durum: {orchestrator.get_state()}")
        
        # Onay iste
        approved = orchestrator.request_approval()
        print(f"Onay: {approved}")
        print(f"Durum: {orchestrator.get_state()}")
        
        # Apply
        if approved:
            apply_result = orchestrator.apply_change("quality_tests/e2e_workspace/test_agent_task.py")
            print(f"Apply sonucu: {apply_result.get('success')}")
            print(f"Durum: {orchestrator.get_state()}")
            
            # Dosya kontrol
            final_content = agent_file.read_text(encoding='utf-8')
            print(f"Son dosya içeriği:\n{final_content}")
            
            # Backup kontrol
            backup_path = apply_result.get('backup')
            print(f"Backup: {backup_path}")
            
            # Test sonucu
            test_result = apply_result.get('test', {})
            print(f"Test sonucu: {test_result.get('success')}")
            
            # Değerlendirme
            success = (
                orchestrator.get_state() == OrchestratorState.COMPLETE.value and
                apply_result.get('success') and
                backup_path and
                test_result.get('success')
            )
            
            print(f"\nTEST A: {'PASS' if success else 'FAIL'}")
            return success
        else:
            print("TEST A: FAIL (onay alınamadı)")
            return False
            
    except Exception as exc:
        print(f"TEST A HATASI: {exc}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        cleanup_test_files()


def test_b_approval_false():
    """
    TEST B — Approval False
    Beklenen: create_plan → approval=False → REJECTED
    Dosya değişmemeli. Backup oluşmamalı.
    """
    print("\n" + "=" * 70)
    print("TEST B — Approval False")
    print("=" * 70)
    
    agent_file, test_file = setup_test_files()
    original_content = agent_file.read_text(encoding='utf-8')
    
    try:
        # Callback (reddet)
        def approval_callback(tool_name, arguments):
            return False
        
        # Orkestratör
        workflow = ChangeWorkflow()
        orchestrator = ChangeOrchestrator(workflow, approval_callback)
        
        # Plan oluştur
        result = orchestrator.create_plan(
            file_path="quality_tests/e2e_workspace/agent_task.py",
            problem="greet fonksiyonunun mesajını değiştirmek"
        )
        
        print(f"Plan sonucu: {result.get('success')}")
        print(f"Durum: {orchestrator.get_state()}")
        
        # Onay iste
        approved = orchestrator.request_approval()
        print(f"Onay: {approved}")
        print(f"Durum: {orchestrator.get_state()}")
        
        # Dosya kontrol
        final_content = agent_file.read_text(encoding='utf-8')
        print(f"Son dosya içeriği:\n{final_content}")
        print(f"Orijinal ile eşleşiyor: {final_content == original_content}")
        
        # Değerlendirme
        success = (
            not approved and
            orchestrator.get_state() == OrchestratorState.REJECTED.value and
            final_content == original_content
        )
        
        print(f"\nTEST B: {'PASS' if success else 'FAIL'}")
        return success
        
    except Exception as exc:
        print(f"TEST B HATASI: {exc}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        cleanup_test_files()


def test_c_no_callback():
    """
    TEST C — Callback yok
    Beklenen: İşlem reddedilmeli. Dosya değişmemeli.
    """
    print("\n" + "=" * 70)
    print("TEST C — Callback yok")
    print("=" * 70)
    
    agent_file, test_file = setup_test_files()
    original_content = agent_file.read_text(encoding='utf-8')
    
    try:
        # Callback yok
        workflow = ChangeWorkflow()
        orchestrator = ChangeOrchestrator(workflow, approval_callback=None)
        
        # Plan oluştur
        result = orchestrator.create_plan(
            file_path="quality_tests/e2e_workspace/agent_task.py",
            problem="greet fonksiyonunun mesajını değiştirmek"
        )
        
        print(f"Plan sonucu: {result.get('success')}")
        print(f"Durum: {orchestrator.get_state()}")
        
        # Onay iste
        approved = orchestrator.request_approval()
        print(f"Onay: {approved}")
        print(f"Durum: {orchestrator.get_state()}")
        
        # Dosya kontrol
        final_content = agent_file.read_text(encoding='utf-8')
        print(f"Son dosya içeriği:\n{final_content}")
        print(f"Orijinal ile eşleşiyor: {final_content == original_content}")
        
        # Değerlendirme
        success = (
            not approved and
            orchestrator.get_state() == OrchestratorState.REJECTED.value and
            final_content == original_content
        )
        
        print(f"\nTEST C: {'PASS' if success else 'FAIL'}")
        return success
        
    except Exception as exc:
        print(f"TEST C HATASI: {exc}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        cleanup_test_files()


def test_d_callback_exception():
    """
    TEST D — Callback exception
    Beklenen: İşlem reddedilmeli. Dosya değişmemeli.
    """
    print("\n" + "=" * 70)
    print("TEST D — Callback exception")
    print("=" * 70)
    
    agent_file, test_file = setup_test_files()
    original_content = agent_file.read_text(encoding='utf-8')
    
    try:
        # Callback exception fırlatır
        def approval_callback(tool_name, arguments):
            raise Exception("Test exception")
        
        workflow = ChangeWorkflow()
        orchestrator = ChangeOrchestrator(workflow, approval_callback)
        
        # Plan oluştur
        result = orchestrator.create_plan(
            file_path="quality_tests/e2e_workspace/agent_task.py",
            problem="greet fonksiyonunun mesajını değiştirmek"
        )
        
        print(f"Plan sonucu: {result.get('success')}")
        print(f"Durum: {orchestrator.get_state()}")
        
        # Onay iste
        approved = orchestrator.request_approval()
        print(f"Onay: {approved}")
        print(f"Durum: {orchestrator.get_state()}")
        
        # Dosya kontrol
        final_content = agent_file.read_text(encoding='utf-8')
        print(f"Son dosya içeriği:\n{final_content}")
        print(f"Orijinal ile eşleşiyor: {final_content == original_content}")
        
        # Değerlendirme
        success = (
            not approved and
            orchestrator.get_state() == OrchestratorState.REJECTED.value and
            final_content == original_content
        )
        
        print(f"\nTEST D: {'PASS' if success else 'FAIL'}")
        return success
        
    except Exception as exc:
        print(f"TEST D HATASI: {exc}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        cleanup_test_files()


def test_e_missing_test_file():
    """
    TEST G — Eksik test_file
    Beklenen: Dosya değişmemeli.
    """
    print("\n" + "=" * 70)
    print("TEST G — Eksik test_file")
    print("=" * 70)
    
    agent_file, test_file = setup_test_files()
    original_content = agent_file.read_text(encoding='utf-8')
    
    try:
        # Callback onay verir
        def approval_callback(tool_name, arguments):
            return True
        
        workflow = ChangeWorkflow()
        orchestrator = ChangeOrchestrator(workflow, approval_callback)
        
        # Plan oluştur
        result = orchestrator.create_plan(
            file_path="quality_tests/e2e_workspace/agent_task.py",
            problem="greet fonksiyonunun mesajını değiştirmek"
        )
        
        print(f"Plan sonucu: {result.get('success')}")
        print(f"Durum: {orchestrator.get_state()}")
        
        # Onay iste
        approved = orchestrator.request_approval()
        print(f"Onay: {approved}")
        print(f"Durum: {orchestrator.get_state()}")
        
        # Apply with empty test_file
        if approved:
            apply_result = orchestrator.apply_change("")
            print(f"Apply sonucu: {apply_result.get('success')}")
            print(f"Hata: {apply_result.get('error')}")
            print(f"Durum: {orchestrator.get_state()}")
        
        # Dosya kontrol
        final_content = agent_file.read_text(encoding='utf-8')
        print(f"Son dosya içeriği:\n{final_content}")
        print(f"Orijinal ile eşleşiyor: {final_content == original_content}")
        
        # Değerlendirme
        success = (
            not apply_result.get('success') and
            final_content == original_content
        )
        
        print(f"\nTEST G: {'PASS' if success else 'FAIL'}")
        return success
        
    except Exception as exc:
        print(f"TEST G HATASI: {exc}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        cleanup_test_files()


if __name__ == "__main__":
    results = {
        'A': test_a_approval_true(),
        'B': test_b_approval_false(),
        'C': test_c_no_callback(),
        'D': test_d_callback_exception(),
        'G': test_e_missing_test_file(),
    }
    
    print("\n\n")
    print("=" * 70)
    print("GENEL ÖZET")
    print("=" * 70)
    for test_name, passed in results.items():
        print(f"TEST {test_name}: {'PASS' if passed else 'FAIL'}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nToplam: {passed}/{total} geçti")
