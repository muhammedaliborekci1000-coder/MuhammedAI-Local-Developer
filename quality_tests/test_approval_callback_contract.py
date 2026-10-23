"""
Quality Test: Approval Callback Contract
Amaç: Onay callback'in doğru sözleşmeyi uyguladığını doğrulamak.
- Coroutine döndürdüğünde reddetme
- Bool olmayan değer döndürdüğünde reddetme
- Hata durumunda reddetme
"""

import sys
import os
import asyncio
import inspect

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.ollama_client import OllamaClient
from app.ai.change_orchestrator import ChangeOrchestrator
from app.tools.tool_registry import ToolRegistry


def test_coroutine_callback_rejected():
    """
    Test: Async callback (coroutine döndüren) senkron çağrıldığında reddedilmeli.
    Not: Coroutine close() çağrıldığı için callback body çalışmaz, bu beklenen davranıştır.
    Önemli olan onayın reddedilmesidir.
    """
    print("=" * 70)
    print("TEST: Coroutine Callback Rejected")
    print("=" * 70)
    
    registry = ToolRegistry()
    ai = OllamaClient()
    
    # Async callback (coroutine döndürür)
    async def async_callback(tool_name: str, arguments: dict) -> bool:
        return True
    
    config = LoopConfig(max_iterations=10, enable_logging=False)
    
    agent_loop = AgentLoop(
        ollama_client=ai,
        tool_registry=registry,
        config=config,
        approval_callback=async_callback
    )
    
    # Tool call simülasyonu
    from app.ai.tool_parser import ToolCall
    tool_call = ToolCall(
        name="apply_change",
        arguments={"plan": {"file": "test.py"}, "test_file": "test.py"},
        raw_text='{"tool": "apply_change", "arguments": {...}}'
    )
    
    result = agent_loop._execute_tool_call(tool_call)
    
    print(f"Sonuç: {result}")
    
    # Doğrulama
    passed = (
        not result.get("success") and  # Sonuç başarısız
        result.get("requires_approval") == True  # Onay gerektiren araç
    )
    
    print(f"{'PASS' if passed else 'FAIL'}: Coroutine callback reddedildi")
    print("=" * 70)
    
    assert passed


def test_non_bool_callback_rejected():
    """
    Test: Bool olmayan değer döndüren callback reddedilmeli.
    """
    print("=" * 70)
    print("TEST: Non-Bool Callback Rejected")
    print("=" * 70)
    
    registry = ToolRegistry()
    ai = OllamaClient()
    
    # Callback çağrıldı mı kontrolü
    callback_called = []
    
    # String döndüren callback
    def string_callback(tool_name: str, arguments: dict) -> str:
        callback_called.append((tool_name, arguments))
        return "yes"  # Truthy ama bool değil
    
    config = LoopConfig(max_iterations=10, enable_logging=False)
    
    agent_loop = AgentLoop(
        ollama_client=ai,
        tool_registry=registry,
        config=config,
        approval_callback=string_callback
    )
    
    from app.ai.tool_parser import ToolCall
    tool_call = ToolCall(
        name="apply_change",
        arguments={"plan": {"file": "test.py"}, "test_file": "test.py"},
        raw_text='{"tool": "apply_change", "arguments": {...}}'
    )
    
    result = agent_loop._execute_tool_call(tool_call)
    
    print(f"Sonuç: {result}")
    print(f"Callback çağrıldı: {len(callback_called) > 0}")
    
    # Doğrulama
    passed = (
        len(callback_called) > 0 and  # Callback çağrıldı
        not result.get("success") and  # Sonuç başarısız
        result.get("requires_approval") == True  # Onay gerektiren araç
    )
    
    print(f"{'PASS' if passed else 'FAIL'}: Non-bool callback reddedildi")
    print("=" * 70)
    
    assert passed


def test_callback_exception_rejected():
    """
    Test: Hata fırlatan callback reddedilmeli.
    """
    print("=" * 70)
    print("TEST: Callback Exception Rejected")
    print("=" * 70)
    
    registry = ToolRegistry()
    ai = OllamaClient()
    
    # Callback çağrıldı mı kontrolü
    callback_called = []
    
    # Hata fırlatan callback
    def error_callback(tool_name: str, arguments: dict) -> bool:
        callback_called.append((tool_name, arguments))
        raise ValueError("Test error")
    
    config = LoopConfig(max_iterations=10, enable_logging=False)
    
    agent_loop = AgentLoop(
        ollama_client=ai,
        tool_registry=registry,
        config=config,
        approval_callback=error_callback
    )
    
    from app.ai.tool_parser import ToolCall
    tool_call = ToolCall(
        name="apply_change",
        arguments={"plan": {"file": "test.py"}, "test_file": "test.py"},
        raw_text='{"tool": "apply_change", "arguments": {...}}'
    )
    
    result = agent_loop._execute_tool_call(tool_call)
    
    print(f"Sonuç: {result}")
    print(f"Callback çağrıldı: {len(callback_called) > 0}")
    
    # Doğrulama
    passed = (
        len(callback_called) > 0 and  # Callback çağrıldı
        not result.get("success") and  # Sonuç başarısız
        result.get("requires_approval") == True  # Onay gerektiren araç
    )
    
    print(f"{'PASS' if passed else 'FAIL'}: Hata fırlatan callback reddedildi")
    print("=" * 70)
    
    assert passed


def test_orchestrator_coroutine_rejected():
    """
    Test: ChangeOrchestrator'da coroutine callback reddedilmeli.
    Not: Coroutine close() çağrıldığı için callback body çalışmaz, bu beklenen davranıştır.
    Önemli olan onayın reddedilmesidir.
    """
    print("=" * 70)
    print("TEST: Orchestrator Coroutine Rejected")
    print("=" * 70)
    
    from app.tools.change_workflow import ChangeWorkflow
    from app.ai.change_orchestrator import OrchestratorState
    
    workflow = ChangeWorkflow()
    
    # Async callback
    async def async_callback(tool_name: str, arguments: dict) -> bool:
        return True
    
    orchestrator = ChangeOrchestrator(workflow, approval_callback=async_callback)
    
    # Manuel plan set et (dosya okumadan)
    orchestrator._current_plan = {
        "file": "test.py",
        "function": "test",
        "problem": "Test problem",
        "change": "Test change",
        "old_code": "old",
        "new_code": "new",
        "reason": "Test"
    }
    orchestrator._state = OrchestratorState.PLAN_READY
    
    approved = orchestrator.request_approval()
    
    print(f"Sonuç: {approved}")
    print(f"State: {orchestrator.get_state()}")
    
    # Doğrulama
    passed = (
        not approved and  # Onay reddedildi
        orchestrator.get_state() == "REJECTED"  # State REJECTED
    )
    
    print(f"{'PASS' if passed else 'FAIL'}: Orchestrator coroutine reddedildi")
    print("=" * 70)
    
    assert passed


if __name__ == "__main__":
    try:
        test1 = test_coroutine_callback_rejected()
        test2 = test_non_bool_callback_rejected()
        test3 = test_callback_exception_rejected()
        test4 = test_orchestrator_coroutine_rejected()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Coroutine Callback: {'PASS' if test1 else 'FAIL'}")
        print(f"Non-Bool Callback: {'PASS' if test2 else 'FAIL'}")
        print(f"Callback Exception: {'PASS' if test3 else 'FAIL'}")
        print(f"Orchestrator Coroutine: {'PASS' if test4 else 'FAIL'}")
        
        all_passed = test1 and test2 and test3 and test4
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
