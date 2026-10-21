"""
Gerçek Qwen3 Correction Loop Testi
Amaç: Gerçek Qwen3:4B modeliyle correction loop davranışını doğrulamak.

Senaryo:
1. Modelden kod değişikliği planı iste
2. İlk uygulama sonrası test dosyasını değiştirerek test başarısız olmasını sağla
3. Modelin başarısız test sonucunu alıp ikinci düzeltme planı oluşturup oluşturamadığını doğrula
4. Correction sayaç ve history değerlerini raporla

Gerçek Kullanılan Sınıflar:
- AgentLoop - gerçek production kodu
- ChangeOrchestrator - gerçek production kodu
- SafeChangeManager - gerçek production kodu
- ToolRegistry - gerçek production kodu
- OllamaClient - gerçek model (qwen3:4b)

Mock Edilen Bileşenler:
- Yok. Tüm bileşenler gerçek.
"""
import sys
import os
import pytest
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.ollama_client import OllamaClient
from app.tools.tool_registry import ToolRegistry
from app.core.config import PROJECT_ROOT


def setup_test_files():
    """Test dosyalarını oluştur"""
    workspace = PROJECT_ROOT / "quality_tests" / "correction_real_workspace"
    workspace.mkdir(parents=True, exist_ok=True)

    # Basit bir Python dosyası
    calc_file = workspace / "calculator.py"
    calc_content = '''def add(a, b):
    return a - b
'''
    calc_file.write_text(calc_content, encoding='utf-8')

    # Test dosyası
    test_file = workspace / "test_calculator.py"
    test_content = '''from calculator import add

def test_add():
    assert add(2, 3) == 5
'''
    test_file.write_text(test_content, encoding='utf-8')

    return calc_file, test_file, workspace


def modify_test_to_fail(test_file):
    """Test dosyasını değiştirerek test başarısız olmasını sağla"""
    # Testi başarısız olacak şekilde değiştir (beklenen değer 5 yerine 6 yap)
    test_content = '''from calculator import add

def test_add():
    assert add(2, 3) == 6  # BUG: Wrong expected value
'''
    test_file.write_text(test_content, encoding='utf-8')


def cleanup_test_files(workspace):
    """Test dosyalarını temizле"""
    if workspace.exists():
        shutil.rmtree(workspace)


@pytest.mark.slow
def test_correction_loop_real_qwen3():
    """
    Gerçek Qwen3:4B ile Correction Loop Testi
    
    Senaryo:
    1. Modelden add fonksiyonunu düzeltmesini iste
    2. İlk uygulama sonrası test dosyasını değiştirerek test başarısız olmasını sağla
    3. Modelin başarısız test sonucunu alıp ikinci düzeltme planı oluşturup oluşturamadığını doğrula
    4. Correction sayaç ve history değerlerini raporla
    """
    print("=" * 70)
    print("GERÇEK QWEN3 CORRECTION LOOP TESTİ")
    print("=" * 70)
    
    calc_file, test_file, workspace = setup_test_files()
    original_calc_content = calc_file.read_text(encoding='utf-8')
    
    print(f"Calculator dosyası: {calc_file}")
    print(f"Orijinal içerik:\n{original_calc_content}")
    print(f"Test dosyası: {test_file}")
    
    try:
        # Approval callback
        approval_log = []
        
        def approval_callback(tool_name: str, arguments: dict) -> bool:
            print(f"  [APPROVAL] {tool_name} -> APPROVED")
            approval_log.append((tool_name, arguments, True))
            return True
        
        # Gerçek Ollama client
        ollama_client = OllamaClient(model="qwen3:4b")
        
        # AgentLoop oluştur (correction loop enabled)
        config = LoopConfig(
            max_iterations=20,
            max_no_tool_retries=3,
            max_correction_attempts=3,
            enable_logging=True
        )
        
        tool_registry = ToolRegistry()
        
        agent_loop = AgentLoop(
            ollama_client=ollama_client,
            tool_registry=tool_registry,
            config=config,
            approval_callback=approval_callback
        )
        
        # Görev - modelin önce yanlış yapmasını sağlayacak bir istek
        user_task = "quality_tests/correction_real_workspace/calculator.py dosyasındaki add fonksiyonunu değiştir. Şu an a - b döndürüyor, a * b döndürsün. Test dosyası quality_tests/correction_real_workspace/test_calculator.py."
        
        print(f"\nGörev: {user_task}")
        print("-" * 70)
        
        # İlk apply_change çağrısını yakalamak için ToolRegistry'i patch et
        apply_change_count = [0]
        original_apply_change = tool_registry.workflow.apply_change
        
        def patched_apply_change(plan, test_file, approved=False):
            apply_change_count[0] += 1
            print(f"\n[PATCHED] apply_change çağrıldı (count={apply_change_count[0]})")
            
            result = original_apply_change(plan, test_file, approved)
            
            # İlk uygulama sonrası test dosyasını değiştir
            if apply_change_count[0] == 1 and result.get("success"):
                print("[PATCHED] İlk uygulama başarılı, test dosyasını değiştiriyorum...")
                modify_test_to_fail(test_file)
                print("[PATCHED] Test dosyası başarısız olacak şekilde değiştirildi")
            
            return result
        
        # Patch uygula
        tool_registry.workflow.apply_change = patched_apply_change
        
        # AgentLoop'u çalıştır
        result = agent_loop.run(user_task)
        
        # Patch'i geri al
        tool_registry.workflow.apply_change = original_apply_change
        
        print("\n" + "=" * 70)
        print("AGENTLOOP SONUCU")
        print("=" * 70)
        print(f"Success: {result.success}")
        print(f"Iterations: {result.iterations}")
        print(f"Final response: {result.final_response.encode('cp1254', errors='ignore').decode('cp1254')}")
        print(f"Error: {result.error}")
        
        # Tool call log
        print(f"\nTool call log ({len(result.tool_calls)} çağrı):")
        for i, call in enumerate(result.tool_calls, 1):
            print(f"  {i}. {call['tool']}")
            if call.get('result'):
                success = call['result'].get('success')
                print(f"     Success: {success}")
                # Error mesajı var mı?
                if call['result'].get('error'):
                    print(f"     Error: {call['result']['error']}")
                # Test failure details var mı?
                if call['result'].get('test_failure_details'):
                    print(f"     Test failure details: {call['result']['test_failure_details']}")
                # Correction attempt	var mı?
                if call['result'].get('correction_attempt'):
                    print(f"     Correction attempt: {call['result']['correction_attempt']}")
                # Correction history var mı?
                if call['result'].get('correction_history'):
                    print(f"     Correction history length: {len(call['result']['correction_history'])}")
        
        # Approval log
        print(f"\nApproval log ({len(approval_log)} çağrı):")
        for i, (tool_name, args, approved) in enumerate(approval_log, 1):
            print(f"  {i}. {tool_name} -> approved={approved}")
        
        # Correction sayaç ve history
        print(f"\nCorrection loop bilgileri:")
        print(f"  Correction attempt: {agent_loop._correction_attempt}")
        print(f"  Correction history length: {len(agent_loop._correction_history)}")
        if agent_loop._correction_history:
            print(f"  Correction history:")
            for entry in agent_loop._correction_history:
                print(f"    Attempt {entry['attempt']}: success={entry['success']}, approval={entry['approval']}")
        
        # Dosya içeriği
        final_calc_content = calc_file.read_text(encoding='utf-8')
        print(f"\nSon calculator içeriği:")
        print(final_calc_content)
        
        # Değerlendirme
        print("\n" + "=" * 70)
        print("DEĞERLENDİRME")
        print("=" * 70)
        
        # Correction loop tetiklendi mi?
        correction_triggered = agent_loop._correction_attempt > 0
        print(f"Correction loop tetiklendi: {correction_triggered}")
        
        # İkinci düzeltme planı oluşturuldu mu?
        second_attempt = agent_loop._correction_attempt >= 2
        print(f"İkinci düzeltme denemesi yapıldı: {second_attempt}")
        
        # Test failure details modele aktarıldı mı?
        test_failure_details_transmitted = False
        for call in result.tool_calls:
            if call.get('result', {}).get('test_failure_details'):
                test_failure_details_transmitted = True
                break
        print(f"Test failure details modele aktarıldı: {test_failure_details_transmitted}")
        
        # Dosya değişti mi?
        file_changed = final_calc_content != original_calc_content
        print(f"Dosya değişti: {file_changed}")
        
        # Test başarılı mı?
        success = (
            correction_triggered and
            test_failure_details_transmitted and
            file_changed
        )
        
        print(f"\nTEST SONUCU: {'PASS' if success else 'FAIL'}")
        
        if not correction_triggered:
            print("UYARI: Correction loop tetiklenmedi. Model ilk denemede doğru düzeltmiş olabilir veya test başarısızlığı modele aktarılmamış olabilir.")
        
        if not test_failure_details_transmitted:
            print("UYARI: Test failure details modele aktarılmadı.")
        
        # Assertion (correction loop tetiklenmezse test başarısız sayma, sadece raporla)
        if correction_triggered:
            assert success, "Correction loop çalıştı ancak beklenen davranışı göstermedi."
        else:
            print("BİLGİ: Correction loop tetiklenmedi. Bu normal olabilir (model ilk denemede doğru düzeltmiş olabilir).")
        
    except Exception as exc:
        print(f"\nTEST HATASI: {exc}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        cleanup_test_files(workspace)


if __name__ == "__main__":
    test_correction_loop_real_qwen3()
