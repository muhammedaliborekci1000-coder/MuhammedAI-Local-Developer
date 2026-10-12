"""
Unit Test: Correction Loop (Gerçek AgentLoop.run() ile)
Amaç: Correction loop davranışını gerçek AgentLoop.run() ile test etmek,
ancak OllamaClient.chat(), ToolRegistry.execute() ve SafeChangeManager.apply_patch_and_test()
mock'layarak kontrollü test sonuçları sağlamak.

NOT: Bu testler simülasyon niteliğindedir. Gerçek AI modeli kullanılmaz.
Correction sayaç ve history değerleri production kodu (AgentLoop) tarafından oluşturulur.
"""

import pytest
import sys
import os
import shutil
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.ollama_client import OllamaClient
from app.ai.tool_parser import ToolParser, ToolCall, ParseResult
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


def test_correction_fail_then_success_unit(workspace):
    """
    TEST A — Fail then success (Unit Test)
    Gerçek AgentLoop.run() kullanarak correction loop testi.
    İlk plan başarısız, ikinci plan başarılı olur.
    """
    print("\n" + "=" * 70)
    print("TEST A — Fail then Success (Unit)")
    print("=" * 70)

    calculator_file = workspace / "calculator.py"
    original_code = 'def add(a, b):\n    return a - b\n'
    with open(calculator_file, 'w', encoding='utf-8') as f:
        f.write(original_code)

    test_file = workspace / "test_calculator.py"
    test_code = '''
def test_add():
    assert add(2, 3) == 5
'''
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_code)

    relative_calc = str(calculator_file.relative_to(PROJECT_ROOT))
    relative_test = str(test_file.relative_to(PROJECT_ROOT))

    ollama_client = OllamaClient()
    tool_registry = ToolRegistry()
    config = LoopConfig(
        max_iterations=20,
        max_correction_attempts=3,
        enable_logging=False
    )

    approval_count = [0]
    def approval_callback(tool_name, arguments):
        approval_count[0] += 1
        print(f"Approval: {tool_name} -> APPROVED")
        return True

    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback
    )

    # OllamaClient.chat mock - dummy yanıt döndür
    chat_call_count = [0]
    def mock_chat(self, message, response_format=None):
        chat_call_count[0] += 1
        print(f"Mock chat (count={chat_call_count[0]})")
        return "Processing request..."

    # ToolParser.parse mock - kontrollü ToolCall nesneleri döndür
    parse_count = [0]
    def mock_parse(self, ai_response):
        parse_count[0] += 1
        print(f"Mock parse (count={parse_count[0]})")

        if parse_count[0] == 1:
            return ParseResult(
                success=True,
                tool_calls=[
                    ToolCall(
                        name="read_file",
                        arguments={"relative_path": relative_calc},
                        raw_text='read_file'
                    )
                ],
                raw_response=ai_response
            )
        elif parse_count[0] == 2:
            return ParseResult(
                success=True,
                tool_calls=[
                    ToolCall(
                        name="create_change_plan",
                        arguments={
                            "file_path": relative_calc,
                            "problem": "add function returns a - b instead of a + b"
                        },
                        raw_text='create_change_plan'
                    )
                ],
                raw_response=ai_response
            )
        elif parse_count[0] == 3:
            return ParseResult(
                success=True,
                tool_calls=[
                    ToolCall(
                        name="create_change_plan",
                        arguments={
                            "file_path": relative_calc,
                            "problem": "add function returns a - b instead of a + b (correction)"
                        },
                        raw_text='create_change_plan correction'
                    )
                ],
                raw_response=ai_response
            )
        else:
            return ParseResult(success=True, tool_calls=[], raw_response=ai_response)

    # ToolParser.validate_tool_call mock - her zaman True döndür
    def mock_validate_tool_call(self, tool_call, available_tools):
        print(f"Mock validate_tool_call: {tool_call.name}")
        return True

    # ToolRegistry.execute mock - kontrollü sonuçlar döndür
    execute_count = [0]
    original_execute = tool_registry.execute
    def mock_execute(name, arguments, approved=False):
        execute_count[0] += 1
        print(f"Mock execute (count={execute_count[0]}, tool={name}, approved={approved})")

        if name == "read_file":
            with open(calculator_file, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"success": True, "content": content, "file_path": arguments.get("relative_path")}

        elif name == "create_change_plan":
            file_path = arguments.get("file_path", relative_calc)
            with open(calculator_file, 'r', encoding='utf-8') as f:
                current_content = f.read()

            plan = {
                "file": file_path,
                "old_code": current_content,
                "new_code": 'def add(a, b):\n    return a + b\n',
                "reason": "Fix add function to return a + b instead of a - b"
            }

            result = {
                "success": True,
                "result": {
                    "plan": plan,
                    "validation": {"valid": True, "errors": []}
                },
                "plan": plan,
                "validation": {"valid": True, "errors": []}
            }
            print(f"  -> create_change_plan result: {result}")
            return result

        else:
            return original_execute(name, arguments, approved)

    # ToolRegistry.workflow.apply_change mock - test sonuçlarını kontrol et
    apply_count = [0]
    original_workflow_apply = tool_registry.workflow.apply_change
    def mock_workflow_apply_change(plan, test_file, approved=False):
        apply_count[0] += 1
        print(f"Mock workflow.apply_change (count={apply_count[0]})")

        if apply_count[0] == 1:
            # İlk çağrıda başarısız döndür (correction loop tetiklenmeli)
            print("  -> başarısız döndürülüyor")
            result = original_workflow_apply(plan, test_file, approved)
            result["success"] = False
            result["test"] = {"success": False}
            result["test_failure_details"] = {
                "stdout": "",
                "stderr": "AssertionError: assert add(2, 3) == 5",
                "returncode": 1,
                "error": "Test failed"
            }
            # Orchestrator reset YAPMA - production kodunda reset_for_correction() çağrılıyor
            return result
        else:
            # İkinci ve sonraki çağrılarda başarılı döndür
            print("  -> başarılı döndürülüyor")
            # Dosyayı güncelle
            with open(calculator_file, 'w', encoding='utf-8') as f:
                f.write('def add(a, b):\n    return a + b\n')
            return {"success": True, "test": {"success": True}}

    with patch.object(OllamaClient, 'chat', mock_chat):
        with patch.object(ToolParser, 'parse', mock_parse):
            with patch.object(ToolParser, 'validate_tool_call', mock_validate_tool_call):
                with patch.object(tool_registry, 'execute', mock_execute):
                    with patch.object(tool_registry.workflow, 'apply_change', mock_workflow_apply_change):
                        user_task = f"Fix the add function in {relative_calc}. The function currently returns a - b but should return a + b. Use apply_change tool with {relative_test} to verify."
                        result = agent_loop.run(user_task)

    print(f"\nSonuç:")
    print(f"Success: {result.success}")
    print(f"Approval count: {approval_count[0]}")
    print(f"Chat call count: {chat_call_count[0]}")
    print(f"Execute count: {execute_count[0]}")
    print(f"Apply count: {apply_count[0]}")
    print(f"Correction attempt: {agent_loop._correction_attempt}")
    print(f"Correction history length: {len(agent_loop._correction_history)}")

    assert agent_loop._correction_attempt > 0, "Correction loop başlatılmadı"
    print("✓ Correction loop başlatıldı (production kodu tarafından).")

    assert len(agent_loop._correction_history) > 0, "Correction history boş"
    print("✓ Correction history dolu (production kodu tarafından oluşturuldu).")

    history = agent_loop._correction_history
    print(f"\nCorrection history:")
    for entry in history:
        print(f"  Attempt {entry['attempt']}: success={entry['success']}, approval={entry['approval']}")

    assert history[0]["success"] is False, "İlk deneme başarısız olmalı"
    print("✓ İlk deneme başarısız.")

    assert history[-1]["success"] is True, "Son deneme başarılı olmalı"
    print("✓ Son deneme başarılı.")

    assert result.success is True, "Sonuç başarısız"
    print("✓ Sonuç başarılı.")

    with open(calculator_file, 'r', encoding='utf-8') as f:
        final_code = f.read()
    assert "return a + b" in final_code or "return a+b" in final_code, "Son kod doğru değil"
    print("✓ Son kod doğru.")

    assert apply_count[0] == 2, f"Apply count yanlış: {apply_count[0]} (beklenen: 2)"
    print("✓ Apply count doğru (2).")

    print("\n" + "=" * 70)
    print("TEST A: PASS")
    print("=" * 70)


def test_correction_approval_rejected_unit(workspace):
    """
    TEST B — Approval Rejected (Unit Test)
    Onay callback'i manipüle ederek reddedilme senaryosu.
    """
    print("\n" + "=" * 70)
    print("TEST B — Approval Rejected (Unit)")
    print("=" * 70)

    calculator_file = workspace / "calculator.py"
    original_code = 'def add(a, b):\n    return a - b\n'
    with open(calculator_file, 'w', encoding='utf-8') as f:
        f.write(original_code)

    test_file = workspace / "test_calculator.py"
    test_code = '''
def test_add():
    assert add(2, 3) == 5
'''
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_code)

    relative_calc = str(calculator_file.relative_to(PROJECT_ROOT))
    relative_test = str(test_file.relative_to(PROJECT_ROOT))

    ollama_client = OllamaClient()
    tool_registry = ToolRegistry()
    config = LoopConfig(
        max_iterations=20,
        max_correction_attempts=3,
        enable_logging=False
    )

    approval_count = [0]
    def approval_callback(tool_name, arguments):
        approval_count[0] += 1
        if tool_name == "apply_change" and approval_count[0] == 2:
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

    # OllamaClient.chat mock
    chat_call_count = [0]
    def mock_chat(self, message, response_format=None):
        chat_call_count[0] += 1
        print(f"Mock chat (count={chat_call_count[0]})")
        return "Processing request..."

    # ToolParser.parse mock
    parse_count = [0]
    def mock_parse(self, ai_response):
        parse_count[0] += 1
        print(f"Mock parse (count={parse_count[0]})")

        if parse_count[0] == 1:
            return ParseResult(
                success=True,
                tool_calls=[
                    ToolCall(
                        name="read_file",
                        arguments={"relative_path": relative_calc},
                        raw_text='read_file'
                    )
                ],
                raw_response=ai_response
            )
        elif parse_count[0] == 2:
            return ParseResult(
                success=True,
                tool_calls=[
                    ToolCall(
                        name="create_change_plan",
                        arguments={
                            "file_path": relative_calc,
                            "problem": "add function returns a - b instead of a + b"
                        },
                        raw_text='create_change_plan'
                    )
                ],
                raw_response=ai_response
            )
        elif parse_count[0] == 3:
            return ParseResult(
                success=True,
                tool_calls=[
                    ToolCall(
                        name="create_change_plan",
                        arguments={
                            "file_path": relative_calc,
                            "problem": "add function returns a - b instead of a + b (correction)"
                        },
                        raw_text='create_change_plan correction'
                    )
                ],
                raw_response=ai_response
            )
        else:
            return ParseResult(success=True, tool_calls=[], raw_response=ai_response)

    # ToolRegistry.execute mock
    execute_count = [0]
    original_execute = tool_registry.execute
    def mock_execute(name, arguments, approved=False):
        execute_count[0] += 1
        print(f"Mock execute (count={execute_count[0]}, tool={name})")

        if name == "read_file":
            with open(calculator_file, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"success": True, "content": content, "file_path": arguments.get("relative_path")}

        elif name == "create_change_plan":
            file_path = arguments.get("file_path", relative_calc)
            with open(calculator_file, 'r', encoding='utf-8') as f:
                current_content = f.read()

            plan = {
                "file": file_path,
                "old_code": current_content,
                "new_code": 'def add(a, b):\n    return a + b\n',
                "reason": "Fix add function"
            }

            return {
                "success": True,
                "result": {
                    "plan": plan,
                    "validation": {"valid": True, "errors": []}
                },
                "plan": plan,
                "validation": {"valid": True, "errors": []}
            }

        else:
            return original_execute(name, arguments, approved)

    # ToolRegistry.workflow.apply_change mock - başarısız döndür (correction loop tetiklenmeli)
    apply_count = [0]
    original_workflow_apply = tool_registry.workflow.apply_change
    def mock_workflow_apply_change(plan, test_file, approved=False):
        apply_count[0] += 1
        print(f"Mock workflow.apply_change (count={apply_count[0]})")
        print("  -> başarısız döndürülüyor")
        result = original_workflow_apply(plan, test_file, approved)
        result["success"] = False
        result["test"] = {"success": False}
        result["test_failure_details"] = {
            "stdout": "",
            "stderr": "AssertionError: assert add(2, 3) == 5",
            "returncode": 1,
            "error": "Test failed"
        }
        # Orchestrator reset YAPMA - production kodunda reset_for_correction() çağrılıyor
        return result

    # ToolParser.validate_tool_call mock - her zaman True döndür
    def mock_validate_tool_call(self, tool_call, available_tools):
        print(f"Mock validate_tool_call: {tool_call.name}")
        return True

    with patch.object(OllamaClient, 'chat', mock_chat):
        with patch.object(ToolParser, 'parse', mock_parse):
            with patch.object(ToolParser, 'validate_tool_call', mock_validate_tool_call):
                with patch.object(tool_registry, 'execute', mock_execute):
                    with patch.object(tool_registry.workflow, 'apply_change', mock_workflow_apply_change):
                        user_task = f"Fix the add function in {relative_calc}. The function currently returns a - b but should return a + b. Use apply_change tool with {relative_test} to verify."
                        result = agent_loop.run(user_task)

    print(f"\nSonuç:")
    print(f"Success: {result.success}")
    print(f"Approval count: {approval_count[0]}")
    print(f"Correction attempt: {agent_loop._correction_attempt}")
    print(f"Correction history length: {len(agent_loop._correction_history)}")

    assert approval_count[0] == 2, f"Approval count yanlış: {approval_count[0]} (beklenen: 2)"
    print("✓ Approval 2 kez çağrıldı.")

    history = agent_loop._correction_history
    print(f"\nCorrection history:")
    for entry in history:
        print(f"  Attempt {entry['attempt']}: approval={entry['approval']}, success={entry['success']}")

    if len(history) > 1:
        assert history[0]["approval"] == "approved", "İlk plan onaylanmalı"
        assert history[1]["approval"] == "rejected", "Correction planı reddedilmeli"
        print("✓ İlk plan onaylandı, correction planı reddedildi.")

    with open(calculator_file, 'r', encoding='utf-8') as f:
        final_code = f.read()
    assert final_code == original_code, "Dosya değiştirilmemeli"
    print("✓ Dosya değiştirilmedi.")

    print("\n" + "=" * 70)
    print("TEST B: PASS")
    print("=" * 70)


def test_correction_max_attempts_unit(workspace):
    """
    TEST C — Max Attempts (Unit Test)
    Maksimum deneme sınırı mantığını doğrular.
    """
    print("\n" + "=" * 70)
    print("TEST C — Max Attempts (Unit)")
    print("=" * 70)

    calculator_file = workspace / "calculator.py"
    original_code = 'def add(a, b):\n    return a - b\n'
    with open(calculator_file, 'w', encoding='utf-8') as f:
        f.write(original_code)

    test_file = workspace / "test_calculator.py"
    test_code = '''
def test_add():
    assert add(2, 3) == 5
'''
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_code)

    relative_calc = str(calculator_file.relative_to(PROJECT_ROOT))
    relative_test = str(test_file.relative_to(PROJECT_ROOT))

    ollama_client = OllamaClient()
    tool_registry = ToolRegistry()
    config = LoopConfig(
        max_iterations=20,
        max_correction_attempts=3,
        enable_logging=False
    )

    approval_count = [0]
    def approval_callback(tool_name, arguments):
        approval_count[0] += 1
        print(f"Approval: {tool_name} -> APPROVED")
        return True

    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback
    )

    # OllamaClient.chat mock - dummy yanıt döndür
    chat_call_count = [0]
    def mock_chat(self, message, response_format=None):
        chat_call_count[0] += 1
        print(f"Mock chat (count={chat_call_count[0]})")
        return "Processing request..."

    # ToolParser.parse mock - her zaman create_change_plan döndür
    parse_count = [0]
    def mock_parse(self, ai_response):
        parse_count[0] += 1
        print(f"Mock parse (count={parse_count[0]})")

        if parse_count[0] == 1:
            return ParseResult(
                success=True,
                tool_calls=[
                    ToolCall(
                        name="read_file",
                        arguments={"relative_path": relative_calc},
                        raw_text='read_file'
                    )
                ],
                raw_response=ai_response
            )
        elif parse_count[0] <= 5:
            return ParseResult(
                success=True,
                tool_calls=[
                    ToolCall(
                        name="create_change_plan",
                        arguments={
                            "file_path": relative_calc,
                            "problem": f"add function returns a - b instead of a + b (attempt {parse_count[0]})"
                        },
                        raw_text='create_change_plan'
                    )
                ],
                raw_response=ai_response
            )
        else:
            return ParseResult(success=True, tool_calls=[], raw_response=ai_response)

    # ToolRegistry.execute mock
    execute_count = [0]
    original_execute = tool_registry.execute
    def mock_execute(name, arguments, approved=False):
        execute_count[0] += 1
        print(f"Mock execute (count={execute_count[0]}, tool={name})")

        if name == "read_file":
            with open(calculator_file, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"success": True, "content": content, "file_path": arguments.get("relative_path")}

        elif name == "create_change_plan":
            file_path = arguments.get("file_path", relative_calc)
            with open(calculator_file, 'r', encoding='utf-8') as f:
                current_content = f.read()

            plan = {
                "file": file_path,
                "old_code": current_content,
                "new_code": 'def add(a, b):\n    return a + b\n',
                "reason": "Fix add function"
            }

            return {
                "success": True,
                "result": {
                    "plan": plan,
                    "validation": {"valid": True, "errors": []}
                },
                "plan": plan,
                "validation": {"valid": True, "errors": []}
            }

        else:
            return original_execute(name, arguments, approved)

    # ToolRegistry.workflow.apply_change mock - her zaman başarısız döndür (max attempts tetiklenmeli)
    apply_count = [0]
    original_workflow_apply = tool_registry.workflow.apply_change
    def mock_workflow_apply_change(plan, test_file, approved=False):
        apply_count[0] += 1
        print(f"Mock workflow.apply_change (count={apply_count[0]})")
        print("  -> başarısız döndürülüyor")
        result = original_workflow_apply(plan, test_file, approved)
        result["success"] = False
        result["test"] = {"success": False}
        result["test_failure_details"] = {
            "stdout": "",
            "stderr": "AssertionError: assert add(2, 3) == 5",
            "returncode": 1,
            "error": "Test failed"
        }
        # Orchestrator reset YAPMA - production kodunda reset_for_correction() çağrılıyor
        return result

    # ToolParser.validate_tool_call mock - her zaman True döndür
    def mock_validate_tool_call(self, tool_call, available_tools):
        print(f"Mock validate_tool_call: {tool_call.name}")
        return True

    with patch.object(OllamaClient, 'chat', mock_chat):
        with patch.object(ToolParser, 'parse', mock_parse):
            with patch.object(ToolParser, 'validate_tool_call', mock_validate_tool_call):
                with patch.object(tool_registry, 'execute', mock_execute):
                    with patch.object(tool_registry.workflow, 'apply_change', mock_workflow_apply_change):
                        user_task = f"Fix the add function in {relative_calc}. The function currently returns a - b but should return a + b. Use apply_change tool with {relative_test} to verify."
                        result = agent_loop.run(user_task)

    print(f"\nSonuç:")
    print(f"Success: {result.success}")
    print(f"Correction attempt: {agent_loop._correction_attempt}")
    print(f"Correction history length: {len(agent_loop._correction_history)}")

    assert agent_loop._correction_attempt > 0, "Correction loop başlatılmadı"

    # Production düzeltmesi sonrası:
    # - APPLY_FAILED state'i eklendi (test başarısızlığı için)
    # - reset_for_correction() metodu eklendi (correction loop için)
    # - AgentLoop._execute_tool_call içinde reset_for_correction() çağrılıyor
    # - Orchestrator.reset() workaround'u kaldırıldı
    print(f"✓ Correction attempt: {agent_loop._correction_attempt}")
    print(f"✓ Max attempts sınırı: {config.max_correction_attempts}")
    print("  (Production düzeltmesi: APPLY_FAILED state ve reset_for_correction() eklendi)")

    history = agent_loop._correction_history
    print(f"\nCorrection history:")
    for entry in history:
        print(f"  Attempt {entry['attempt']}: success={entry['success']}, approval={entry['approval']}")

    print("✓ Correction loop çalıştı.")

    # Maksimum deneme sınırı kontrolü
    assert agent_loop._correction_attempt == config.max_correction_attempts, \
        f"Correction attempt {agent_loop._correction_attempt}, expected {config.max_correction_attempts}"
    print(f"✓ Maksimum deneme sınırına ulaşıldı: {agent_loop._correction_attempt}/{config.max_correction_attempts}")

    # max_attempts_reached flag kontrolü
    found_max_attempts = False
    for tool_call in result.tool_calls:
        orchestration = tool_call.get("result", {}).get("orchestration", {})
        if orchestration.get("max_attempts_reached"):
            found_max_attempts = True
            print("✓ max_attempts_reached flag bulundu")
    assert found_max_attempts, "max_attempts_reached flag bulunamadı"

    with open(calculator_file, 'r', encoding='utf-8') as f:
        final_code = f.read()
    assert final_code == original_code, "Dosya rollback yapılmadı"
    print("✓ Dosya rollback yapıldı.")

    print("\n" + "=" * 70)
    print("TEST C: PASS")
    print("=" * 70)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
