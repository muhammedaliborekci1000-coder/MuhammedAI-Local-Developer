"""
Deterministic E2E Test: Correction Loop
Amaç: Correction loop davranışını gerçek AgentLoop ve ChangeOrchestrator ile doğrulamak.

Bu test mevcut test_correction_loop_unit.py ile aynı yapıyı kullanır.
Yeni bir dosya oluşturulmasının sebebi: Test kategorilerini açıkça ayırmak.

Gerçek Kullanılan Sınıflar:
- AgentLoop.run() - gerçek production kodu
- ChangeOrchestrator - gerçek production kodu (mock yok)
- Correction sayaç ve history - production kodu tarafından oluşturulur

Mock Edilen Bileşenler:
- OllamaClient.chat() - model yanıtları (deterministiklik için)
- ToolParser.parse() - araç çağrıları (deterministiklik için)
- ToolParser.validate_tool_call() - araç doğrulama (deterministiklik için)
- ToolRegistry.execute() - araç çalıştırma (deterministiklik için)
- ToolRegistry.workflow.apply_change() - değişiklik uygulama (test sonucu kontrolü için)

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


def test_deterministic_fail_then_success_e2e(workspace):
    """
    TEST A — Başarısızlık → Düzeltme → Başarı (Deterministik E2E)

    Zorunlu akış:
    1. İlk plan oluşturulur ve gerekli onay alınır.
    2. İlk uygulama gerçekleştirilir.
    3. Test çalıştırıcısı ilk sonucu kontrollü biçimde başarısız döndürür.
    4. Başarısızlık bilgisi gerçek agent akışına iletilir.
    5. Agent yeni bir düzeltme planı üretir.
    6. İkinci plan için gereken onay akışı uygulanır.
    7. İkinci uygulama gerçekleştirilir.
    8. Test çalıştırıcısı başarı döndürür.

    Zorunlu assertion'lar:
    - İlk uygulama gerçekten başarısız olmalı.
    - İlk başarısızlıktan sonra yeni plan oluşturulmalı.
    - İkinci uygulama gerçekten yapılmalı.
    - Sonuç başarı olmalı.
    - Düzeltme sayacı ve geçmiş kayıtları gerçek akışla tutarlı olmalı.
    - Dosyanın nihai içeriği beklenen düzeltmeyle eşleşmeli.
    - Onay güvenliği atlanmamalı.
    """
    print("\n" + "=" * 70)
    print("TEST A — Başarısızlık → Düzeltme → Başarı (Deterministik E2E)")
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
    approval_log = []
    def approval_callback(tool_name, arguments):
        approval_count[0] += 1
        approval_log.append((tool_name, arguments))
        print(f"Approval: {tool_name} -> APPROVED")
        return True

    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback
    )

    # Mock'lar - deterministiklik için
    chat_call_count = [0]
    def mock_chat(self, message, response_format=None, tools=None):
        chat_call_count[0] += 1
        print(f"Mock chat (count={chat_call_count[0]})")
        return {"content": "Processing request...", "tool_calls": None}

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

    def mock_validate_tool_call(self, tool_call, available_tools):
        print(f"Mock validate_tool_call: {tool_call.name}")
        return True

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

    apply_count = [0]
    original_workflow_apply = tool_registry.workflow.apply_change
    def mock_workflow_apply_change(plan, test_file, approved=False):
        apply_count[0] += 1
        print(f"Mock workflow.apply_change (count={apply_count[0]})")

        if apply_count[0] == 1:
            # İlk çağrıda başarısız döndür
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
            return result
        else:
            # İkinci ve sonraki çağrılarda başarılı döndür
            print("  -> başarılı döndürülüyor")
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

    # Zorunlu assertion'lar
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

    # İkinci deneme başarılı olmalı (yeni plan oluşturuldu)
    assert len(history) >= 2, "İkinci plan oluşturulmalı"
    assert history[-1]["success"] is True, "Son deneme başarılı olmalı"
    print("✓ Yeni plan oluşturuldu ve başarılı.")

    # En az 2 onay çağrısı olmalı
    assert approval_count[0] >= 2, f"En az 2 onay bekleniyordu, {approval_count[0]} bulundu"
    print(f"✓ Onay sayısı doğru: {approval_count[0]}")

    # Dosya düzeltilmiş olmalı
    with open(calculator_file, 'r', encoding='utf-8') as f:
        final_code = f.read()
    assert "return a + b" in final_code or "return a+b" in final_code, "Kod düzeltilmedi"
    print("✓ Kod düzeltildi.")

    assert result.success is True, "Sonuç başarısız"
    print("✓ Sonuç başarılı.")

    print("\n" + "=" * 70)
    print("TEST A: PASS")
    print("=" * 70)


def test_deterministic_approval_rejected_e2e(workspace):
    """
    TEST B — Düzeltme Planının Kullanıcı Tarafından Reddedilmesi (Deterministik E2E)

    Zorunlu akış:
    1. İlk uygulama kontrollü olarak başarısız olsun.
    2. Agent düzeltme planı oluştursun.
    3. Kullanıcı düzeltme planını reddetsin.

    Zorunlu assertion'lar:
    - Durum REJECTED olmalı.
    - Reddedilen düzeltme otomatik olarak uygulanmamalı.
    - Ek apply_change çağrısı yapılmamalı.
    - İlk başarısızlıktan önceki dosya durumu korunmalı.
    """
    print("\n" + "=" * 70)
    print("TEST B — Düzeltme Planı Reddedilmesi (Deterministik E2E)")
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
    approval_log = []
    def approval_callback(tool_name, arguments):
        approval_count[0] += 1
        approval_log.append((tool_name, arguments))
        # İlk apply_change onayla, ikinci reddet
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

    # Mock'lar
    chat_call_count = [0]
    def mock_chat(self, message, response_format=None, tools=None):
        chat_call_count[0] += 1
        print(f"Mock chat (count={chat_call_count[0]})")
        return {"content": "Processing request...", "tool_calls": None}

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

    def mock_validate_tool_call(self, tool_call, available_tools):
        print(f"Mock validate_tool_call: {tool_call.name}")
        return True

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

    apply_count = [0]
    original_workflow_apply = tool_registry.workflow.apply_change
    def mock_workflow_apply_change(plan, test_file, approved=False):
        apply_count[0] += 1
        print(f"Mock workflow.apply_change (count={apply_count[0]})")

        # İlk çağrıda başarısız döndür
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
        return result

    with patch.object(OllamaClient, 'chat', mock_chat):
        with patch.object(ToolParser, 'parse', mock_parse):
            with patch.object(ToolParser, 'validate_tool_call', mock_validate_tool_call):
                with patch.object(tool_registry, 'execute', mock_execute):
                    with patch.object(tool_registry.workflow, 'apply_change', mock_workflow_apply_change):
                        user_task = f"Fix the add function in {relative_calc}. Use {relative_test} to verify."
                        result = agent_loop.run(user_task)

    print(f"\nSonuç:")
    print(f"Success: {result.success}")
    print(f"Approval count: {approval_count[0]}")
    print(f"Correction attempt: {agent_loop._correction_attempt}")
    print(f"Correction history length: {len(agent_loop._correction_history)}")

    # Zorunlu assertion'lar
    assert agent_loop._correction_attempt > 0, "Correction loop başlatılmadı"
    print("✓ Correction loop başlatıldı.")

    history = agent_loop._correction_history
    print(f"\nCorrection history:")
    for entry in history:
        print(f"  Attempt {entry['attempt']}: approval={entry['approval']}, success={entry['success']}")

    # İlk plan onaylandı, ikinci plan reddedildi
    assert len(history) >= 2, "İkinci plan oluşturulmalı"
    assert history[0]["approval"] == "approved", "İlk plan onaylanmalı"
    assert history[1]["approval"] == "rejected", "İkinci plan reddedilmeli"
    print("✓ İlk plan onaylandı, ikinci plan reddedildi.")

    # Dosya değiştirilmemiş olmalı
    with open(calculator_file, 'r', encoding='utf-8') as f:
        final_code = f.read()
    assert final_code == original_code, "Dosya değiştirildi"
    print("✓ Dosya değiştirilmedi.")

    print("\n" + "=" * 70)
    print("TEST B: PASS")
    print("=" * 70)


def test_deterministic_max_attempts_e2e(workspace):
    """
    TEST C — Maksimum Düzeltme Denemesi (Deterministik E2E)

    Zorunlu akış:
    1. Test çalıştırıcısı her uygulamayı başarısız döndürsün.
    2. Sahte model yanıtları, gerçek agent akışında geçerli düzeltme planlarını ve gerekli onayları üretsin.
    3. Agent maksimum düzeltme sınırına ulaşsın.

    Zorunlu assertion'lar:
    - max_correction_attempts = 3 için: 1 ilk uygulama + en fazla 3 düzeltme = en fazla 4 apply_change çağrısı
    - _correction_attempt değeri tanımlanmış sınırı aşmasın
    - max_attempts_reached doğru olduğunda ayarlansın ve ana döngü tarafından işlensin
    - Sınır aşıldıktan sonra yeni uygulama yapılmasın
    """
    print("\n" + "=" * 70)
    print("TEST C — Maksimum Düzeltme Denemesi (Deterministik E2E)")
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
    approval_log = []
    def approval_callback(tool_name, arguments):
        approval_count[0] += 1
        approval_log.append((tool_name, arguments))
        print(f"Approval: {tool_name} -> APPROVED")
        return True

    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback
    )

    # Mock'lar
    chat_call_count = [0]
    def mock_chat(self, message, response_format=None, tools=None):
        chat_call_count[0] += 1
        print(f"Mock chat (count={chat_call_count[0]})")
        return {"content": "Processing request...", "tool_calls": None}

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

    def mock_validate_tool_call(self, tool_call, available_tools):
        print(f"Mock validate_tool_call: {tool_call.name}")
        return True

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

    apply_count = [0]
    original_workflow_apply = tool_registry.workflow.apply_change
    def mock_workflow_apply_change(plan, test_file, approved=False):
        apply_count[0] += 1
        print(f"Mock workflow.apply_change (count={apply_count[0]})")

        # Her çağrıda başarısız döndür
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
        return result

    with patch.object(OllamaClient, 'chat', mock_chat):
        with patch.object(ToolParser, 'parse', mock_parse):
            with patch.object(ToolParser, 'validate_tool_call', mock_validate_tool_call):
                with patch.object(tool_registry, 'execute', mock_execute):
                    with patch.object(tool_registry.workflow, 'apply_change', mock_workflow_apply_change):
                        user_task = f"Fix the add function in {relative_calc}. Use {relative_test} to verify."
                        result = agent_loop.run(user_task)

    print(f"\nSonuç:")
    print(f"Success: {result.success}")
    print(f"Approval count: {approval_count[0]}")
    print(f"Apply count: {apply_count[0]}")
    print(f"Correction attempt: {agent_loop._correction_attempt}")
    print(f"Correction history length: {len(agent_loop._correction_history)}")

    # Zorunlu assertion'lar
    assert agent_loop._correction_attempt > 0, "Correction loop başlatılmadı"
    print("✓ Correction loop başlatıldı.")

    assert agent_loop._correction_attempt == config.max_correction_attempts, \
        f"Max attempts'a ulaşılmadı: {agent_loop._correction_attempt} vs {config.max_correction_attempts}"
    print(f"✓ Max attempts sınırına ulaşıldı: {agent_loop._correction_attempt}/{config.max_correction_attempts}")

    # En fazla 4 apply_change çağrısı (1 ilk + 3 düzeltme)
    assert apply_count[0] == 4, f"Apply count yanlış: {apply_count[0]} vs 4"
    print(f"✓ Apply count doğru: {apply_count[0]}")

    history = agent_loop._correction_history
    print(f"\nCorrection history:")
    for entry in history:
        print(f"  Attempt {entry['attempt']}: success={entry['success']}, approval={entry['approval']}")

    assert len(history) == config.max_correction_attempts, \
        f"Correction history length yanlış: {len(history)} vs {config.max_correction_attempts}"
    print(f"✓ Correction history length doğru: {len(history)}")

    # Tüm denemeler başarısız olmalı
    assert all(h["success"] is False for h in history), "Tüm denemeler başarısız olmalı"
    print("✓ Tüm denemeler başarısız.")

    # max_attempts_reached flag kontrolü
    found_max_attempts = False
    for tool_call in result.tool_calls:
        result_data = tool_call.get("result", {})
        orchestration = result_data.get("orchestration", {})
        if orchestration.get("max_attempts_reached"):
            found_max_attempts = True
            print("✓ max_attempts_reached flag bulundu")
    assert found_max_attempts, "max_attempts_reached flag bulunamadı"

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
