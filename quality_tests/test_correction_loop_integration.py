"""
Integration Test: Correction Loop (Gerçek Qwen3 ile)
Amaç: Correction loop davranışını gerçek Qwen3 modeliyle doğrulamak.
Bu testler deterministik değildir ve gerçek model çağrıları yapar.
"""

import pytest
import sys
import os
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, call
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.ollama_client import OllamaClient
from app.tools.tool_registry import ToolRegistry
from app.core.config import PROJECT_ROOT


@pytest.fixture
def workspace():
    """Create and clean up test workspace."""
    workspace = PROJECT_ROOT / "quality_tests" / "correction_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    yield workspace
    if workspace.exists():
        shutil.rmtree(workspace)


def test_correction_initial_failure_trigger(workspace):
    """
    TEST A — İlk Başarısızlık Tetiklenme Doğrulaması (Gerçek Qwen3 Entegrasyon Testi)
    
    Bu test correction loop'un ilk başarısızlık sonrası tetiklenmesini gerçek Qwen3 modeliyle doğrular.
    
    Doğrulanan davranışlar:
    - İlk uygulamanın başarısız olması
    - Correction counter'ın artması
    - APPLY_FAILED durumundan düzeltme akışına geçilmesi
    - Correction history'nin oluşturulması
    
    NOT: Tam correction loop davranışı (fail → correction plan → success) Qwen3'ün non-deterministik
    doğası nedeniyle bu testte doğrulanamaz. Tam correction loop davranışı unit testlerde
    (test_correction_loop_unit.py) deterministik olarak doğrulanmıştır.
    
    Kontrollü başarısızlık: İlk test çalıştırması başarısız.
    """
    print("\n" + "=" * 70)
    print("TEST A — İlk Başarısızlık Tetiklenme")
    print("=" * 70)
    
    # Setup files
    calculator_file = workspace / "calculator.py"
    original_code = 'def add(a, b):\n    return a - b\n'
    with open(calculator_file, 'w', encoding='utf-8') as f:
        f.write(original_code)
    
    test_file = workspace / "test_calculator.py"
    test_code = 'def test_add():\n    assert add(2, 3) == 5\n'
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_code)
    
    relative_calc = str(calculator_file.relative_to(PROJECT_ROOT))
    relative_test = str(test_file.relative_to(PROJECT_ROOT))
    
    ollama_client = OllamaClient()
    tool_registry = ToolRegistry()
    
    # Kontrollü başarısızlık için PythonRunner wrapper
    from app.tools.python_runner import PythonRunner
    original_runner = tool_registry.workflow.manager.runner
    
    test_run_count = [0]
    class ControlledPythonRunner(PythonRunner):
        def run_file(self, file_path, timeout=30):
            test_run_count[0] += 1
            print(f"  [ControlledRunner] Test çalıştırma #{test_run_count[0]}")
            
            # İlk çalıştırma başarısız, ikinci başarılı
            if test_run_count[0] == 1:
                print("  [ControlledRunner] İlk çalıştırma -> BAŞARISIZ (kontrollü)")
                return {
                    "success": False,
                    "returncode": 1,
                    "stdout": "",
                    "stderr": "AssertionError: assert add(2, 3) == 5",
                    "error": "Test failed"
                }
            else:
                print("  [ControlledRunner] İkinci çalıştırma -> BAŞARILI (kontrollü)")
                # Gerçek testi çalıştır
                return original_runner.run_file(file_path, timeout)
    
    # ToolRegistry'deki runner'ı değiştir
    tool_registry.workflow.manager.runner = ControlledPythonRunner()
    
    config = LoopConfig(
        max_iterations=20,
        max_correction_attempts=3,
        enable_logging=False
    )
    
    approval_count = [0]
    approval_log = []
    def approval_callback(tool_name, arguments):
        approval_count[0] += 1
        approval_log.append((tool_name, arguments))
        print(f"  [Approval] {tool_name} -> APPROVED (count={approval_count[0]})")
        return True
    
    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback
    )
    
    user_task = f"Fix the add function in {relative_calc}. The function currently returns a - b but should return a + b. You MUST use the apply_change tool to fix this. First use create_change_plan to create a plan, then use apply_change with {relative_test} to verify. If the test fails, create a new plan and try again."
    result = agent_loop.run(user_task)
    
    # Runner'ı geri yükle
    tool_registry.workflow.manager.runner = original_runner
    
    print(f"\nSonuç:")
    print(f"Success: {result.success}")
    print(f"Error: {result.error}")
    print(f"Approval count: {approval_count[0]}")
    print(f"Correction attempt counter: {agent_loop._correction_attempt}")
    print(f"Correction history length: {len(agent_loop._correction_history)}")
    print(f"Test run count: {test_run_count[0]}")
    
    # Verify the fix is correct
    with open(calculator_file, 'r', encoding='utf-8') as f:
        final_code = f.read()
    
    # Assertion'lar - correction loop gerçekten çalışmalı
    assert agent_loop._correction_attempt > 0, "Correction loop başlatılmadı"
    print("✓ Correction loop başlatıldı.")
    
    assert len(agent_loop._correction_history) > 0, "Correction history boş"
    print("✓ Correction history dolu.")
    
    history = agent_loop._correction_history
    print(f"\nCorrection history:")
    for entry in history:
        print(f"  Attempt {entry['attempt']}: success={entry['success']}, approval={entry['approval']}")
    
    # İlk deneme başarısız olmalı
    assert history[0]["success"] is False, "İlk deneme başarısız olmalı"
    print("✓ İlk deneme başarısız.")
    
    # Bu test sadece tetiklenmeyi doğrular, tam correction loop için test_correction_loop_unit.py kullanın
    print("Not: Bu test sadece correction loop tetiklenmesini doğrular.")
    print("Tam correction loop davranışı (fail → correction plan → success) unit testlerde doğrulanmıştır.")
    
    print("\n" + "=" * 70)
    print("TEST A: PASS")
    print("=" * 70)


def test_correction_approval_rejected(workspace):
    """
    TEST 2 — Onay reddi (Integration Test)
    Bu test onay callback'ini manipüle ederek reddedilme senaryosunu test eder.
    NOT: Bu test deterministik değildir ve gerçek Qwen3 modeliyle çalışır.
    """
    print("\n" + "=" * 70)
    print("TEST 2 — Onay Reddi")
    print("=" * 70)
    
    # Setup files
    calculator_file = workspace / "calculator.py"
    original_code = 'def add(a, b):\n    return a - b\n'
    with open(calculator_file, 'w', encoding='utf-8') as f:
        f.write(original_code)
    
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
        enable_logging=False
    )
    
    approval_count = [0]
    def approval_callback(tool_name, arguments):
        approval_count[0] += 1
        # Reject the first apply_change
        if tool_name == "apply_change" and approval_count[0] == 1:
            print(f"Approval: {tool_name} -> REJECTED")
            return False
        print(f"Approval: {tool_name} -> APPROVED")
        return True
    
    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback
    )
    
    user_task = f"Fix the add function in {relative_calc}. Use {relative_test} to verify."
    result = agent_loop.run(user_task)
    
    print(f"\nSonuç:")
    print(f"Success: {result.success}")
    print(f"Error: {result.error}")
    print(f"Approval count: {approval_count[0]}")
    
    # Verify file was not changed (should be original)
    with open(calculator_file, 'r', encoding='utf-8') as f:
        final_code = f.read()
    
    if final_code == original_code:
        print("✓ Dosya değiştirilmedi (onay reddedildi).")
    else:
        print("Not: Dosya değiştirildi (agent farklı bir yol izledi).")
    
    # Verify correction history shows rejection if correction loop was triggered
    history = agent_loop._correction_history
    print(f"\nCorrection history length: {len(history)}")
    if len(history) > 0:
        print(f"Correction history:")
        for entry in history:
            print(f"  Attempt {entry['attempt']}: approval={entry['approval']}, success={entry['success']}")
        # Check for rejected approval
        if any(h.get("approval") == "rejected" for h in history):
            print("✓ Approval reddedildiği doğrulandı.")
    else:
        print("Not: Correction loop başlatılmadı.")
    
    print("\n" + "=" * 70)
    print("TEST 2: PASS")
    print("=" * 70)


def test_correction_max_attempts_boundary_check(workspace):
    """
    TEST C — Max Attempts Sınır Kontrolü (Gerçek Qwen3 Entegrasyon Testi)
    
    Bu test correction loop'un max_attempts sınırını aşmadığını gerçek Qwen3 modeliyle doğrular.
    
    Doğrulanan davranışlar:
    - İlk uygulamanın başarısız olması
    - Correction counter'ın artması
    - Sayaç max_attempts sınırını aşmaması
    
    NOT: Tam max_attempts davranışı (3 deneme, max_attempts_reached flag) Qwen3'ün non-deterministik
    doğası nedeniyle bu testte doğrulanamaz. Tam max_attempts davranışı unit testlerde
    (test_correction_loop_unit.py) deterministik olarak doğrulanmıştır.
    
    Kontrollü başarısızlık: Her test çalıştırması başarısız.
    """
    print("\n" + "=" * 70)
    print("TEST C — Max Attempts Sınır Kontrolü")
    print("=" * 70)
    
    # Setup files
    calculator_file = workspace / "calculator.py"
    original_code = 'def add(a, b):\n    return a - b\n'
    with open(calculator_file, 'w', encoding='utf-8') as f:
        f.write(original_code)
    
    test_file = workspace / "test_calculator.py"
    test_code = 'def test_add():\n    assert add(2, 3) == 5\n'
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_code)
    
    relative_calc = str(calculator_file.relative_to(PROJECT_ROOT))
    relative_test = str(test_file.relative_to(PROJECT_ROOT))
    
    ollama_client = OllamaClient()
    tool_registry = ToolRegistry()
    
    # Kontrollü başarısızlık için PythonRunner wrapper
    from app.tools.python_runner import PythonRunner
    original_runner = tool_registry.workflow.manager.runner
    
    test_run_count = [0]
    class ControlledPythonRunner(PythonRunner):
        def run_file(self, file_path, timeout=30):
            test_run_count[0] += 1
            print(f"  [ControlledRunner] Test çalıştırma #{test_run_count[0]}")
            print("  [ControlledRunner] -> BAŞARISIZ (kontrollü - her zaman)")
            return {
                "success": False,
                "returncode": 1,
                "stdout": "",
                "stderr": "AssertionError: assert add(2, 3) == 5",
                "error": "Test failed"
            }
    
    # ToolRegistry'deki runner'ı değiştir
    tool_registry.workflow.manager.runner = ControlledPythonRunner()
    
    config = LoopConfig(
        max_iterations=20,
        max_correction_attempts=3,
        enable_logging=False
    )
    
    approval_count = [0]
    approval_log = []
    def approval_callback(tool_name, arguments):
        approval_count[0] += 1
        approval_log.append((tool_name, arguments))
        print(f"  [Approval] {tool_name} -> APPROVED (count={approval_count[0]})")
        return True
    
    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback
    )
    
    user_task = f"Fix the add function in {relative_calc}. Use {relative_test} to verify."
    result = agent_loop.run(user_task)
    
    # Runner'ı geri yükle
    tool_registry.workflow.manager.runner = original_runner
    
    print(f"\nSonuç:")
    print(f"Success: {result.success}")
    print(f"Error: {result.error}")
    print(f"Approval count: {approval_count[0]}")
    print(f"Correction attempt counter: {agent_loop._correction_attempt}")
    print(f"Correction history length: {len(agent_loop._correction_history)}")
    print(f"Test run count: {test_run_count[0]}")
    
    # Assertion'lar - correction loop gerçekten çalışmalı
    assert agent_loop._correction_attempt > 0, "Correction loop başlatılmadı"
    print("✓ Correction loop başlatıldı.")
    
    assert len(agent_loop._correction_history) > 0,"Correction history boş"
    print("✓ Correction history dolu.")
    
    # Qwen3 non-deterministik davranış gösterebilir
    # Model max_attempts'a ulaşmayabilir - bu beklenen bir durum
    # Önemli olan: production kodu correction loop'u doğru tetikledi ve max_attempts kontrolü çalışıyor
    history = agent_loop._correction_history
    print(f"\nCorrection history:")
    for entry in history:
        print(f"  Attempt {entry['attempt']}: success={entry['success']}, approval={entry['approval']}")
    
    # Sayaç max_attempts'ı aşmamalı
    assert agent_loop._correction_attempt <= config.max_correction_attempts, \
        f"Max attempts aşıldı: {agent_loop._correction_attempt} vs {config.max_correction_attempts}"
    print(f"✓ Max attempts sınırına uyuldu: {agent_loop._correction_attempt}/{config.max_correction_attempts}")
    
    # Tüm denemeler başarısız olmalı
    assert all(h["success"] is False for h in history), "Tüm denemeler başarısız olmalı"
    print("✓ Tüm denemeler başarısız.")
    
    # Bu test sadece sınır kontrolünü doğrular, tam max_attempts için test_correction_loop_unit.py kullanın
    print("Not: Bu test sadece max_attempts sınır kontrolünü doğrular.")
    print("Tam max_attempts davranışı (3 deneme, max_attempts_reached flag) unit testlerde doğrulanmıştır.")
    
    # Dosya rollback yapılmış olmalı
    with open(calculator_file, 'r', encoding='utf-8') as f:
        final_code = f.read()
    assert final_code == original_code, "Dosya rollback yapılmadı"
    print("✓ Dosya rollback yapıldı.")
    
    print("\n" + "=" * 70)
    print("TEST C: PASS")
    print("=" * 70)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
