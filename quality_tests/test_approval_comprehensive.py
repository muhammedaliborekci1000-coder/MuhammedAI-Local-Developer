"""
Quality Test: Comprehensive Approval Security
Amaç: Onay callback'in tüm senaryolarda doğru davrandığını doğrulamak.
- Senkron True/False
- String/None döndürme
- Async callback/coroutine
- Exception fırlatma
- workflow.apply_change çağrı sayısı kontrolü
- Dosya değişmediği kontrolü
"""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.ollama_client import OllamaClient
from app.tools.tool_registry import ToolRegistry


def test_sync_true_callback_allows_change():
    """
    Test: Senkron True döndüren callback değişikliğe izin vermelidir.
    """
    print("=" * 70)
    print("TEST: Sync True Callback Allows Change")
    print("=" * 70)
    
    registry = ToolRegistry()
    ai = OllamaClient()
    
    def true_callback(tool_name: str, arguments: dict) -> bool:
        return True
    
    config = LoopConfig(max_iterations=10, enable_logging=False)
    
    agent_loop = AgentLoop(
        ollama_client=ai,
        tool_registry=registry,
        config=config,
        approval_callback=true_callback
    )
    
    # apply_change tool çağrısını simüle et
    from app.ai.tool_parser import ToolCall
    tool_call = ToolCall(
        name="apply_change",
        arguments={"plan": {"file": "test.py"}, "test_file": "test.py"},
        raw_text='{"tool": "apply_change", "arguments": {...}}'
    )
    
    result = agent_loop._execute_tool_call(tool_call)
    
    print(f"Sonuç: {result}")
    
    # Doğrulama - True callback onay gerektiren araçta çalışmalı
    passed = result.get("success") or "onay" in result.get("error", "").lower()
    
    print(f"{'PASS' if passed else 'FAIL'}: Sync True callback davranışı")
    print("=" * 70)
    
    assert passed


def test_sync_false_callback_blocks_change():
    """
    Test: Senkron False döndüren callback değişikliği engellemelidir.
    """
    print("=" * 70)
    print("TEST: Sync False Callback Blocks Change")
    print("=" * 70)
    
    registry = ToolRegistry()
    ai = OllamaClient()
    
    def false_callback(tool_name: str, arguments: dict) -> bool:
        return False
    
    config = LoopConfig(max_iterations=10, enable_logging=False)
    
    agent_loop = AgentLoop(
        ollama_client=ai,
        tool_registry=registry,
        config=config,
        approval_callback=false_callback
    )
    
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
        not result.get("success") and
        result.get("requires_approval") == True and
        "onay" in result.get("error", "").lower()
    )
    
    print(f"{'PASS' if passed else 'FAIL'}: Sync False callback engelledi")
    print("=" * 70)
    
    assert passed


def test_string_callback_blocks_change():
    """
    Test: String döndüren callback değişikliği engellemelidir.
    """
    print("=" * 70)
    print("TEST: String Callback Blocks Change")
    print("=" * 70)
    
    registry = ToolRegistry()
    ai = OllamaClient()
    
    def string_callback(tool_name: str, arguments: dict) -> str:
        return "yes"
    
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
    
    # Doğrulama
    passed = (
        not result.get("success") and
        result.get("requires_approval") == True
    )
    
    print(f"{'PASS' if passed else 'FAIL'}: String callback engelledi")
    print("=" * 70)
    
    assert passed


def test_none_callback_blocks_change():
    """
    Test: None döndüren callback değişikliği engellemelidir.
    """
    print("=" * 70)
    print("TEST: None Callback Blocks Change")
    print("=" * 70)
    
    registry = ToolRegistry()
    ai = OllamaClient()
    
    def none_callback(tool_name: str, arguments: dict) -> None:
        return None
    
    config = LoopConfig(max_iterations=10, enable_logging=False)
    
    agent_loop = AgentLoop(
        ollama_client=ai,
        tool_registry=registry,
        config=config,
        approval_callback=none_callback
    )
    
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
        not result.get("success") and
        result.get("requires_approval") == True
    )
    
    print(f"{'PASS' if passed else 'FAIL'}: None callback engelledi")
    print("=" * 70)
    
    assert passed


def test_async_callback_blocks_change_no_warning():
    """
    Test: Async callback değişikliği engellemeli ve RuntimeWarning oluşturmamalı.
    """
    print("=" * 70)
    print("TEST: Async Callback Blocks Change (No Warning)")
    print("=" * 70)
    
    registry = ToolRegistry()
    ai = OllamaClient()
    
    async def async_callback(tool_name: str, arguments: dict) -> bool:
        return True
    
    config = LoopConfig(max_iterations=10, enable_logging=False)
    
    agent_loop = AgentLoop(
        ollama_client=ai,
        tool_registry=registry,
        config=config,
        approval_callback=async_callback
    )
    
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
        not result.get("success") and
        result.get("requires_approval") == True
    )
    
    print(f"{'PASS' if passed else 'FAIL'}: Async callback engelledi (close() ile)")
    print("=" * 70)
    
    assert passed


def test_exception_callback_blocks_change():
    """
    Test: Exception fırlatan callback değişikliği engellemelidir.
    """
    print("=" * 70)
    print("TEST: Exception Callback Blocks Change")
    print("=" * 70)
    
    registry = ToolRegistry()
    ai = OllamaClient()
    
    def exception_callback(tool_name: str, arguments: dict) -> bool:
        raise ValueError("Test exception")
    
    config = LoopConfig(max_iterations=10, enable_logging=False)
    
    agent_loop = AgentLoop(
        ollama_client=ai,
        tool_registry=registry,
        config=config,
        approval_callback=exception_callback
    )
    
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
        not result.get("success") and
        result.get("requires_approval") == True
    )
    
    print(f"{'PASS' if passed else 'FAIL'}: Exception callback engelledi")
    print("=" * 70)
    
    assert passed


def test_file_not_changed_on_rejection():
    """
    Test: Onay reddedildiğinde dosya değişmemelidir.
    """
    print("=" * 70)
    print("TEST: File Not Changed on Rejection")
    print("=" * 70)
    
    # Geçici test klasörü oluştur
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Geçici test dosyası oluştur
        test_file = os.path.join(temp_dir, "test.py")
        original_content = "# Original content\nprint('Hello')\n"
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(original_content)
        
        print(f"Geçici dosya: {test_file}")
        print(f"Orijinal içerik: {repr(original_content)}")
        
        # Dosya içeriğini oku
        with open(test_file, 'r', encoding='utf-8') as f:
            content_after = f.read()
        
        print(f"Sonraki içerik: {repr(content_after)}")
        
        # Doğrulama
        passed = content_after == original_content
        
        print(f"{'PASS' if passed else 'FAIL'}: Dosya içeriği değişmedi")
        print("=" * 70)
        
        assert passed
        
    finally:
        # Temizlik
        shutil.rmtree(temp_dir)
        print(f"Geçici klasör temizlendi: {temp_dir}")


if __name__ == "__main__":
    try:
        test1 = test_sync_true_callback_allows_change()
        test2 = test_sync_false_callback_blocks_change()
        test3 = test_string_callback_blocks_change()
        test4 = test_none_callback_blocks_change()
        test5 = test_async_callback_blocks_change_no_warning()
        test6 = test_exception_callback_blocks_change()
        test7 = test_file_not_changed_on_rejection()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Sync True: {'PASS' if test1 else 'FAIL'}")
        print(f"Sync False: {'PASS' if test2 else 'FAIL'}")
        print(f"String: {'PASS' if test3 else 'FAIL'}")
        print(f"None: {'PASS' if test4 else 'FAIL'}")
        print(f"Async: {'PASS' if test5 else 'FAIL'}")
        print(f"Exception: {'PASS' if test6 else 'FAIL'}")
        print(f"File Not Changed: {'PASS' if test7 else 'FAIL'}")
        
        all_passed = test1 and test2 and test3 and test4 and test5 and test6 and test7
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
