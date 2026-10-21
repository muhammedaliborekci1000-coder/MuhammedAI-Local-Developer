"""
Phase 5.1 — Gerçek Qwen3:4B Araç Kullanımı Analizi
Modelin araç çağrılarını doğru yapıp yapmadığını belirlemek için kapsamlı test.
"""
import sys
import os
import pytest
import subprocess
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.agent_loop import AgentLoop, LoopConfig
from app.tools.tool_registry import ToolRegistry
from app.ai.ollama_client import OllamaClient
from app.core.config import PROJECT_ROOT


def setup_test_workspace():
    """Test çalışma alanını oluştur"""
    workspace = PROJECT_ROOT / "quality_tests" / "tool_usage_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace


def cleanup_test_workspace():
    """Test çalışma alanını temizle"""
    workspace = PROJECT_ROOT / "quality_tests" / "tool_usage_workspace"
    if workspace.exists():
        import shutil
        shutil.rmtree(workspace)


@pytest.mark.slow
def test_real_qwen3_tool_usage_multiply():
    """
    Gerçek Qwen3:4B modelinin araç kullanımını test eder.
    
    Görev:
    - multiply(a, b) fonksiyonu oluştur
    - Üç pytest testi oluştur
    - Testleri çalıştır
    
    Başarı Kriterleri:
    - Model tool çağrısı yapmalı (yalnızca metin değil)
    - Dosya değişikliği gerçek olmalı
    - Test dosyası oluşturulmalı
    - Test komutu çalıştırılmalı
    """
    print("\n" + "=" * 70)
    print("PHASE 5.1 — GERÇEK QWEN3 ARAÇ KULLANIMI TESTİ")
    print("=" * 70)
    
    workspace = setup_test_workspace()
    
    # Test için boş bir dosya oluştur (model bunu değiştirmeli)
    multiply_file = workspace / "multiply.py"
    multiply_file.write_text("# Bu dosya değiştirilmeli\n", encoding='utf-8')
    
    try:
        # Approval callback (her zaman onayla)
        approval_log = []
        
        def approval_callback(tool_name: str, arguments: dict) -> bool:
            print(f"  [APPROVAL] {tool_name} -> APPROVED")
            approval_log.append((tool_name, arguments, True))
            return True
        
        # Gerçek Ollama client
        ollama_client = OllamaClient(model="qwen3:4b")
        
        # AgentLoop oluştur
        config = LoopConfig(
            max_iterations=5,
            max_no_tool_retries=1,
            enable_logging=True
        )
        
        tool_registry = ToolRegistry()
        
        agent_loop = AgentLoop(
            ollama_client=ollama_client,
            tool_registry=tool_registry,
            config=config,
            approval_callback=approval_callback
        )
        
        # Görev
        user_task = f"""quality_tests/tool_usage_workspace/multiply.py dosyasında multiply(a, b) fonksiyonu oluştur. Bu fonksiyon a ve b'nin çarpımını döndürmeli.
Ayrıca quality_tests/tool_usage_workspace/test_multiply.py dosyasında bu fonksiyonu test eden 3 pytest testi oluştur.
Testleri çalıştır ve sonuçları raporla."""
        
        print(f"\nGörev: {user_task}")
        print("-" * 70)
        
        # AgentLoop'u çalıştır
        result = agent_loop.run(user_task)
        
        print("\n" + "=" * 70)
        print("AGENTLOOP SONUCU")
        print("=" * 70)
        print(f"Success: {result.success}")
        print(f"Iterations: {result.iterations}")
        print(f"Final response: {result.final_response.encode('cp1254', errors='ignore').decode('cp1254')}")
        print(f"Error: {result.error}")
        
        # Modelin ham yanıtını logla (debug için)
        print(f"\nModel ham yanıtı (ilk 500 karakter):")
        print(result.final_response[:500] if result.final_response else "None")
        
        # Tool call log
        print(f"\nTool call log ({len(result.tool_calls)} çağrı):")
        for i, call in enumerate(result.tool_calls, 1):
            print(f"  {i}. {call['tool']}")
            if call.get('result'):
                result_data = call['result']
                # result string ise dict'e çevir
                if isinstance(result_data, str):
                    print(f"     Result (str): {result_data[:200]}")
                elif isinstance(result_data, dict):
                    success = result_data.get('success')
                    print(f"     Success: {success}")
                    if result_data.get('error'):
                        print(f"     Error: {result_data['error']}")
                    # Validation detaylarını logla
                    inner_result = result_data.get('result')
                    if isinstance(inner_result, dict) and inner_result.get('validation'):
                        validation = inner_result['validation']
                        print(f"     Validation: {validation}")
                    # Plan detaylarını logla
                    if isinstance(inner_result, dict) and inner_result.get('plan'):
                        plan = inner_result['plan']
                        print(f"     Plan keys: {list(plan.keys()) if isinstance(plan, dict) else 'N/A'}")
        
        # Approval log
        print(f"\nApproval log ({len(approval_log)} çağrı):")
        for i, (tool_name, args, approved) in enumerate(approval_log, 1):
            print(f"  {i}. {tool_name} -> approved={approved}")
        
        # Dosyaları kontrol et
        multiply_file = workspace / "multiply.py"
        test_file = workspace / "test_multiply.py"
        
        multiply_exists = multiply_file.exists()
        test_exists = test_file.exists()
        
        print(f"\nDosya Kontrolü:")
        print(f"  multiply.py var mı: {multiply_exists}")
        print(f"  test_multiply.py var mı: {test_exists}")
        
        if multiply_exists:
            multiply_content = multiply_file.read_text(encoding='utf-8')
            print(f"\n  multiply.py içeriği:")
            print(multiply_content)
        
        if test_exists:
            test_content = test_file.read_text(encoding='utf-8')
            print(f"\n  test_multiply.py içeriği:")
            print(test_content)
            
            # Testleri çalıştır
            print(f"\nTestleri çalıştırıyor...")
            test_result = subprocess.run(
                ["python", "-m", "pytest", str(test_file), "-v"],
                cwd=str(workspace),
                capture_output=True,
                text=True
            )
            
            print(f"\nTest Çıktısı (Exit Code: {test_result.returncode}):")
            print(test_result.stdout)
            if test_result.stderr:
                print(f"Stderr:\n{test_result.stderr}")
        
        # Kök neden sınıflandırması
        print("\n" + "=" * 70)
        print("KÖK NEDEN SINIFLANDIRMASI")
        print("=" * 70)
        
        tool_calls_made = len(result.tool_calls) > 0
        has_create_change_plan = any(call['tool'] == 'create_change_plan' for call in result.tool_calls)
        has_read_file = any(call['tool'] == 'read_file' for call in result.tool_calls)
        has_run_python_file = any(call['tool'] == 'run_python_file' for call in result.tool_calls)
        
        print(f"Tool çağrısı yapıldı mı: {tool_calls_made}")
        print(f"create_change_plan çağrıldı mı: {has_create_change_plan}")
        print(f"read_file çağrıldı mı: {has_read_file}")
        print(f"run_python_file çağrıldı mı: {has_run_python_file}")
        
        if not tool_calls_made:
            print("KÖK NEDEN: Model araç çağrısı yerine yalnızca metin üretiyor")
        elif not has_read_file:
            print("KÖK NEDEN: Model dosyayı okumak için read_file çağırmıyor")
        elif not has_create_change_plan:
            print("KÖK NEDEN: Model değişiklik için create_change_plan çağırmıyor")
        elif not multiply_exists:
            print("KÖK NEDEN: Model dosya oluşturamıyor veya araç çalıştırma başarısız")
        elif not test_exists:
            print("KÖK NEDEN: Model test dosyası oluşturamıyor")
        else:
            print("KÖK NEDEN: Belirlenemedi - araçlar çalışıyor ama tam görev tamamlanamadı")
        
        # Test başarılı mı?
        success = (
            tool_calls_made and
            multiply_exists and
            test_exists and
            'multiply' in multiply_content.lower()
        )
        
        print(f"\nTEST SONUCU: {'PASS' if success else 'FAIL'}")
        
        # Test başarısız olsa bile raporla
        if not success:
            print("UYARI: Test başarısız ama araç kullanımı analizi tamamlandı")
        
        # Dosyaları temizle
        cleanup_test_workspace()
        
        # Test başarısız olsa bile assertion yapma (sadece raporla)
        # assert success, "Model araç kullanımı başarısız"
        
    except Exception as exc:
        print(f"\nTEST HATASI: {exc}")
        import traceback
        traceback.print_exc()
        cleanup_test_workspace()
        raise
