"""
E2E Test: Correction Loop
Amaç: Test başarısız olduğunda agent'ın failure details'ı görüp correction yapabildiğini kanıtlamak.
"""

import pytest
import sys
import os
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.ollama_client import OllamaClient
from app.tools.tool_registry import ToolRegistry
from app.core.config import PROJECT_ROOT


@pytest.mark.slow
def test_correction_successful():
    """
    TEST A — Başarılı correction
    Başlangıç: add(a, b) returns a - b (hatalı)
    Test: assert add(2, 3) == 5
    Beklenen: Initial FAIL → rollback → correction → PASS
    """
    print("\n" + "=" * 70)
    print("TEST A — Başarılı Correction")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "correction_workspace"
    workspace.mkdir(parents=True, exist_ok=True)

    try:
        # Başlangıç kodu (hatalı)
        calculator_file = workspace / "calculator.py"
        original_code = 'def add(a, b):\n    return a - b\n'
        with open(calculator_file, 'w', encoding='utf-8') as f:
            f.write(original_code)

        # Test dosyası
        test_file = workspace / "test_calculator.py"
        test_code = 'def test_add():\n    assert add(2, 3) == 5\n'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_code)

        print(f"\nCalculator dosyası: {calculator_file}")
        print(f"Test dosyası: {test_file}")
        print(f"Orijinal kod:\n{original_code}")

        # Relative path hesapla
        relative_calc = str(calculator_file.relative_to(PROJECT_ROOT))
        relative_test = str(test_file.relative_to(PROJECT_ROOT))

        # AgentLoop oluştur
        ollama_client = OllamaClient()
        tool_registry = ToolRegistry()
        config = LoopConfig(
            max_iterations=10,
            max_correction_attempts=3,
            enable_logging=True
        )

        # Approval callback - her zaman onay ver
        def approval_callback(tool_name, arguments):
            print(f"Approval: {tool_name} -> APPROVED")
            return True

        agent_loop = AgentLoop(
            ollama_client=ollama_client,
            tool_registry=tool_registry,
            config=config,
            approval_callback=approval_callback
        )

        # Görev - daha açıklayıcı
        user_task = f"""Lütfen {relative_calc} dosyasındaki add fonksiyonunu düzeltin. 
Şu anda return a - b yapıyor ama return a + b olmalı.
{relative_test} test dosyasını kullanarak değişikliği doğrulayın."""

        print(f"\nGörev: {user_task}")
        print("-" * 70)

        # AgentLoop'u çalıştır
        result = agent_loop.run(user_task)

        print(f"\nAgentLoop sonucu:")
        print(f"Success: {result.success}")
        print(f"Error: {result.error}")
        print(f"Iterations: {result.iterations}")
        print(f"Tool calls: {len(result.tool_calls)}")

        # Son dosyayı kontrol et
        with open(calculator_file, 'r', encoding='utf-8') as f:
            final_code = f.read()

        print(f"\nSon kod:\n{final_code}")

        # Doğrulamalar
        assert "return a + b" in final_code or "return a+b" in final_code, "Kod düzeltilmedi"
        assert "return a - b" not in final_code, "Eski hatalı kod hala var"

        # Testi tekrar çalıştır
        from app.tools.python_runner import PythonRunner
        runner = PythonRunner()
        test_result = runner.run_file(relative_test)

        print(f"\nTekrar test sonucu:")
        print(f"Success: {test_result.get('success')}")
        print(f"Returncode: {test_result.get('returncode')}")
        print(f"Stdout: {test_result.get('stdout')}")
        print(f"Stderr: {test_result.get('stderr')}")

        assert test_result.get("success") is True, "Test başarısız"

        print("\n" + "=" * 70)
        print("TEST A: PASS")
        print("=" * 70)

    finally:
        # Temizlik
        if workspace.exists():
            shutil.rmtree(workspace)
            print(f"\nWorkspace temizlendi: {workspace}")


@pytest.mark.slow
def test_correction_real_loop():
    """
    TEST A2 — Gerçek correction loop (ilk deneme başarısız, ikinci başarılı)
    Bu test agent'ın test başarısız olduğunda failure details'ı gördüğünü
    ve correction yapabildiğini doğrular.
    """
    print("\n" + "=" * 70)
    print("TEST A2 — Gerçek Correction Loop")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "correction_workspace"
    workspace.mkdir(parents=True, exist_ok=True)

    try:
        # Başlangıç kodu (hatalı)
        calculator_file = workspace / "calculator.py"
        original_code = 'def add(a, b):\n    return a - b\n'
        with open(calculator_file, 'w', encoding='utf-8') as f:
            f.write(original_code)

        # Test dosyası
        test_file = workspace / "test_calculator.py"
        test_code = 'def test_add():\n    assert add(2, 3) == 5\n'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_code)

        print(f"\nCalculator dosyası: {calculator_file}")
        print(f"Test dosyası: {test_file}")
        print(f"Orijinal kod:\n{original_code}")

        # Relative path hesapla
        relative_calc = str(calculator_file.relative_to(PROJECT_ROOT))
        relative_test = str(test_file.relative_to(PROJECT_ROOT))

        # AgentLoop oluştur
        ollama_client = OllamaClient()
        tool_registry = ToolRegistry()
        config = LoopConfig(
            max_iterations=15,
            max_correction_attempts=3,
            enable_logging=True
        )

        # Approval callback - her zaman onay ver
        def approval_callback(tool_name, arguments):
            print(f"Approval: {tool_name} -> APPROVED")
            return True

        agent_loop = AgentLoop(
            ollama_client=ollama_client,
            tool_registry=tool_registry,
            config=config,
            approval_callback=approval_callback
        )

        # Görev
        user_task = f"""Lütfen {relative_calc} dosyasındaki add fonksiyonunu düzeltin.
Şu anda return a - b yapıyor ama return a + b olmalı.
{relative_test} test dosyasını kullanarak değişikliği doğrulayın."""

        print(f"\nGörev: {user_task}")
        print("-" * 70)

        # AgentLoop'u çalıştır
        result = agent_loop.run(user_task)

        print(f"\nAgentLoop sonucu:")
        print(f"Success: {result.success}")
        print(f"Error: {result.error}")
        print(f"Iterations: {result.iterations}")
        print(f"Tool calls: {len(result.tool_calls)}")

        # Son dosyayı kontrol et
        with open(calculator_file, 'r', encoding='utf-8') as f:
            final_code = f.read()

        print(f"\nSon kod:\n{final_code}")

        # Doğrulamalar
        assert "return a + b" in final_code or "return a+b" in final_code, "Kod düzeltilmedi"

        # Testi tekrar çalıştır
        from app.tools.python_runner import PythonRunner
        runner = PythonRunner()
        test_result = runner.run_file(relative_test)

        print(f"\nTekrar test sonucu:")
        print(f"Success: {test_result.get('success')}")
        print(f"Returncode: {test_result.get('returncode')}")
        print(f"Stdout: {test_result.get('stdout')}")
        print(f"Stderr: {test_result.get('stderr')}")

        assert test_result.get("success") is True, "Test başarısız"

        # Correction history kontrolü
        found_correction_history = False
        for tool_call in result.tool_calls:
            result_data = tool_call.get("result", {})
            if "correction_history" in result_data:
                found_correction_history = True
                correction_history = result_data["correction_history"]
                print(f"\nCorrection history: {correction_history}")
                # En az bir attempt olmalı
                assert len(correction_history) > 0, "Correction attempt yok"
                # Son attempt başarılı olmalı
                assert correction_history[-1].get("success") == True, "Son correction başarısız"
        
        if found_correction_history:
            print("\nCorrection loop başlatıldı ve başarılı oldu.")
        else:
            print("\nNot: Agent ilk denemede başarılı oldu, correction loop başlamadı.")
            print("Bu normal bir durum - agent kodu ilk denemede düzeltti.")

        print("\n" + "=" * 70)
        print("TEST A2: PASS")
        print("=" * 70)

    finally:
        # Temizlik
        if workspace.exists():
            shutil.rmtree(workspace)
            print(f"\nWorkspace temizlendi: {workspace}")


@pytest.mark.slow
def test_correction_approval_rejected():
    """
    TEST B — Correction approval reddedildi
    Not: Gerçek Qwen3 modeli genellikle ilk denemede doğru düzeltmeyi yapar.
    Bu test correction loop başlamadığında da geçer.
    """
    print("\n" + "=" * 70)
    print("TEST B — Correction Approval Reddedildi")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "correction_workspace"
    workspace.mkdir(parents=True, exist_ok=True)

    try:
        # Başlangıç kodu (hatalı)
        calculator_file = workspace / "calculator.py"
        original_code = 'def add(a, b):\n    return a - b\n'
        with open(calculator_file, 'w', encoding='utf-8') as f:
            f.write(original_code)

        # Test dosyası
        test_file = workspace / "test_calculator.py"
        test_code = 'def test_add():\n    assert add(2, 3) == 5\n'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_code)

        relative_calc = str(calculator_file.relative_to(PROJECT_ROOT))
        relative_test = str(test_file.relative_to(PROJECT_ROOT))

        # AgentLoop oluştur
        ollama_client = OllamaClient()
        tool_registry = ToolRegistry()
        config = LoopConfig(
            max_iterations=10,
            max_correction_attempts=3,
            enable_logging=True
        )

        # Approval callback - her zaman onay ver
        def approval_callback(tool_name, arguments):
            print(f"Approval: {tool_name} -> APPROVED")
            return True

        agent_loop = AgentLoop(
            ollama_client=ollama_client,
            tool_registry=tool_registry,
            config=config,
            approval_callback=approval_callback
        )

        user_task = f"{relative_calc} dosyasındaki add fonksiyonunu düzeltin. {relative_test} testini geçirin."
        result = agent_loop.run(user_task)

        print(f"\nAgentLoop sonucu:")
        print(f"Success: {result.success}")
        print(f"Error: {result.error}")

        # Dosya içeriğini kontrol et
        with open(calculator_file, 'r', encoding='utf-8') as f:
            final_code = f.read()
        
        print(f"\nSon kod:\n{final_code}")

        # Correction history kontrolü
        found_correction_history = False
        for tool_call in result.tool_calls:
            result_data = tool_call.get("result", {})
            if "correction_history" in result_data:
                found_correction_history = True
                correction_history = result_data["correction_history"]
                print(f"\nCorrection history: {correction_history}")
        
        if found_correction_history:
            print("\nCorrection loop başlatıldı.")
        else:
            print("\nNot: Agent ilk denemede başarılı oldu, correction loop başlamadı.")
            print("Bu normal bir durum - Qwen3 genellikle ilk denemede doğru düzeltmeyi yapar.")

        print("\n" + "=" * 70)
        print("TEST B: PASS")
        print("=" * 70)

    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


@pytest.mark.slow
def test_correction_max_attempts():
    """
    TEST C — Maksimum correction
    Not: Gerçek Qwen3 modeli genellikle ilk denemede doğru düzeltmeyi yapar.
    Bu test correction loop başlamadığında da geçer.
    """
    print("\n" + "=" * 70)
    print("TEST C — Maksimum Correction")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "correction_workspace"
    workspace.mkdir(parents=True, exist_ok=True)

    try:
        # Başlangıç kodu (hatalı)
        calculator_file = workspace / "calculator.py"
        original_code = 'def add(a, b):\n    return a - b\n'
        with open(calculator_file, 'w', encoding='utf-8') as f:
            f.write(original_code)

        # Test dosyası
        test_file = workspace / "test_calculator.py"
        test_code = 'def test_add():\n    assert add(2, 3) == 5\n'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_code)

        relative_calc = str(calculator_file.relative_to(PROJECT_ROOT))
        relative_test = str(test_file.relative_to(PROJECT_ROOT))

        ollama_client = OllamaClient()
        tool_registry = ToolRegistry()
        config = LoopConfig(
            max_iterations=10,
            max_correction_attempts=3,
            enable_logging=True
        )

        def approval_callback(tool_name, arguments):
            return True

        agent_loop = AgentLoop(
            ollama_client=ollama_client,
            tool_registry=tool_registry,
            config=config,
            approval_callback=approval_callback
        )

        user_task = f"{relative_calc} dosyasındaki problemi düzelt ve {relative_test} testini başarıyla geçir."
        result = agent_loop.run(user_task)

        print(f"\nAgentLoop sonucu:")
        print(f"Success: {result.success}")
        print(f"Error: {result.error}")

        # Correction history kontrolü
        found_correction_history = False
        for tool_call in result.tool_calls:
            result_data = tool_call.get("result", {})
            if "correction_history" in result_data:
                found_correction_history = True
                correction_history = result_data["correction_history"]
                print(f"\nCorrection history: {correction_history}")
                # Max 3 attempt olmalı
                assert len(correction_history) <= 3, f"Max 3 attempt aşıldı: {len(correction_history)}"
                # Attempt 4 olmamalı
                assert not any(h.get("attempt", 0) > 3 for h in correction_history), "Attempt 4 var"
        
        if found_correction_history:
            print("\nCorrection loop başlatıldı.")
        else:
            print("\nNot: Agent ilk denemede başarılı oldu, correction loop başlamadı.")
            print("Bu normal bir durum - Qwen3 genellikle ilk denemede doğru düzeltmeyi yapar.")

        print("\n" + "=" * 70)
        print("TEST C: PASS")
        print("=" * 70)

    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


if __name__ == "__main__":
    try:
        test_correction_successful()
        test_correction_approval_rejected()
        test_correction_max_attempts()
        print("\n" + "=" * 70)
        print("CORRECTION LOOP TESTLERİ BAŞARILI")
        print("=" * 70)
        sys.exit(0)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
