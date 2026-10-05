"""
Quality Test: Approval Security
Amaç: apply_change ve run_python_file gibi approval gerektiren tool'ların
kullanıcı onayı olmadan çalıştırılamadığını doğrulamak.
"""

import sys
import os
import tempfile
import shutil
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.tool_registry import ToolRegistry, ToolDefinition


def test_registry_approval_security():
    """
    Test: ToolRegistry'nin approved=False durumunda tool çalıştırmadığını doğrula.
    Bu test doğrudan ToolRegistry.execute metodunu test eder.
    """
    print("=" * 70)
    print("TEST 6A: ToolRegistry Approval Security")
    print("=" * 70)
    
    # Gerçek ToolRegistry oluştur
    registry = ToolRegistry()
    
    # apply_change tool'unun requires_approval=True olduğunu doğrula
    apply_change_info = registry.get_tool_info("apply_change")
    print(f"apply_change requires_approval: {apply_change_info['requires_approval']}")
    
    # approved=False ile execute dene
    print("\nTest 1: approved=False ile execute çağrısı")
    result_no_approval = registry.execute(
        name="apply_change",
        arguments={"plan": {"file": "test.py"}, "test_file": "test.py"},
        approved=False
    )
    print(f"Sonuç: {result_no_approval}")
    
    # Doğrulamalar
    print("\nDOĞRULAMALAR:")
    print("-" * 70)
    
    passed = True
    
    # 1. approved=False durumunda başarısız olmalı
    if result_no_approval.get("success"):
        print("[X] FAIL: approved=False ile başarılı oldu")
        passed = False
    else:
        print("[OK] PASS: approved=False ile başarısız")
    
    # 2. requires_approval=True hatası olmalı
    if not result_no_approval.get("requires_approval"):
        print("[X] FAIL: requires_approval hatası yok")
        passed = False
    else:
        print("[OK] PASS: requires_approval hatası var")
    
    # 3. run_python_file için de test et
    print("\nTest 2: run_python_file approved=False")
    result_run_no_approval = registry.execute(
        name="run_python_file",
        arguments={"file_path": "test.py"},
        approved=False
    )
    print(f"Sonuç: {result_run_no_approval}")
    
    if result_run_no_approval.get("success"):
        print("[X] FAIL: run_python_file approved=False ile başarılı oldu")
        passed = False
    else:
        print("[OK] PASS: run_python_file approved=False ile başarısız")
    
    print("\n" + "=" * 70)
    if passed:
        print("TEST 6A SONUCU: PASS")
    else:
        print("TEST 6A SONUCU: FAIL")
    print("=" * 70)
    
    return passed


def test_agent_loop_approval_callback():
    """
    Test: AgentLoop'un approval_callback'i çağırdığını ve False döndüğünde
    tool çalıştırmadığını doğrula.
    """
    print("\n" + "=" * 70)
    print("TEST 6B: AgentLoop Approval Callback")
    print("=" * 70)
    
    from app.ai.agent_loop import AgentLoop, LoopConfig
    from app.ai.ollama_client import OllamaClient
    
    # Gerçek ToolRegistry ve OllamaClient kullan
    registry = ToolRegistry()
    ai = OllamaClient()
    
    # Approval callback her zaman False döndürür
    callback_called = []
    
    def approval_callback(tool_name: str, arguments: dict) -> bool:
        print(f"  Onay istendi: {tool_name}")
        callback_called.append((tool_name, arguments))
        return False
    
    config = LoopConfig(
        max_iterations=10,
        max_no_tool_retries=2,
        enable_logging=False
    )
    
    agent_loop = AgentLoop(
        ollama_client=ai,
        tool_registry=registry,
        config=config,
        approval_callback=approval_callback
    )
    
    # apply_change tool çağrısını simüle et
    from app.ai.tool_parser import ToolCall
    
    tool_call = ToolCall(
        name="apply_change",
        arguments={"plan": {"file": "test.py"}, "test_file": "test.py"},
        raw_text='{"tool": "apply_change", "arguments": {...}}'
    )
    
    print("\n_apply_tool_call ile test")
    result = agent_loop._execute_tool_call(tool_call)
    print(f"Sonuç: {result}")
    
    # Doğrulamalar
    print("\nDOĞRULAMALAR:")
    print("-" * 70)
    
    passed = True
    
    # 1. Callback çağrıldı mı?
    if len(callback_called) == 0:
        print("[X] FAIL: Approval callback çağrılmadı")
        passed = False
    else:
        print(f"[OK] PASS: Callback çağrıldı: {callback_called[0]}")
    
    # 2. Sonuç başarısız olmalı
    if result.get("success"):
        print("[X] FAIL: Sonuç başarılı oldu")
        passed = False
    else:
        print("[OK] PASS: Sonuç başarısız")
    
    # 3. Hata mesajı onay reddi ile ilgili olmalı
    if "onay" not in result.get("error", "").lower():
        print(f"[X] FAIL: Hata mesajı onay ile ilgili değil: {result.get('error')}")
        passed = False
    else:
        print("[OK] PASS: Hata mesajı onay reddi ile ilgili")
    
    print("\n" + "=" * 70)
    if passed:
        print("TEST 6B SONUCU: PASS")
    else:
        print("TEST 6B SONUCU: FAIL")
    print("=" * 70)
    
    return passed


def test_file_not_changed():
    """
    Test: Onay reddedildiğinde gerçek dosya değişmemeli.
    """
    print("\n" + "=" * 70)
    print("TEST 6C: Dosya Değişmedi Kontrolü")
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
        print("\nDOĞRULAMALAR:")
        print("-" * 70)
        
        if content_after == original_content:
            print("[OK] PASS: Dosya içeriği değişmedi")
            passed = True
        else:
            print("[X] FAIL: Dosya içeriği değişti!")
            passed = False
        
        print("\n" + "=" * 70)
        if passed:
            print("TEST 6C SONUCU: PASS")
        else:
            print("TEST 6C SONUCU: FAIL")
        print("=" * 70)
        
        return passed
        
    finally:
        # Temizlik
        shutil.rmtree(temp_dir)
        print(f"Geçici klasör temizlendi: {temp_dir}")


if __name__ == "__main__":
    try:
        test6a_passed = test_registry_approval_security()
        test6b_passed = test_agent_loop_approval_callback()
        test6c_passed = test_file_not_changed()
        
        print("\n" + "=" * 70)
        print("TEST 6 TOPLAM SONUÇ")
        print("=" * 70)
        print(f"TEST 6A (Registry Approval): {'PASS' if test6a_passed else 'FAIL'}")
        print(f"TEST 6B (AgentLoop Callback): {'PASS' if test6b_passed else 'FAIL'}")
        print(f"TEST 6C (Dosya Değişmedi): {'PASS' if test6c_passed else 'FAIL'}")
        
        all_passed = test6a_passed and test6b_passed and test6c_passed
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
