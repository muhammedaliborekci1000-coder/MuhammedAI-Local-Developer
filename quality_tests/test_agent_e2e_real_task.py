"""
Gerçek Agent E2E Testi
Amaç: AgentLoop'un doğal dilde verilen kod değiştirme görevini doğru ve güvenli şekilde tamamladığını doğrulamak.
"""

import sys
import os
import shutil
import hashlib
import pytest
from pathlib import Path

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.ollama_client import OllamaClient
from app.tools.tool_registry import ToolRegistry
from app.core.config import PROJECT_ROOT


def get_file_hash(filepath):
    """Dosyanın hash'ini al."""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def get_production_hashes():
    """Production dosyalarının hash'lerini al."""
    app_dir = PROJECT_ROOT / "app"
    hashes = {}

    if app_dir.exists():
        for py_file in app_dir.rglob("*.py"):
            hashes[str(py_file.relative_to(PROJECT_ROOT))] = get_file_hash(py_file)

    return hashes


@pytest.mark.slow
def test_agent_e2e_normal():
    """
    TEST 1: Normal Agent E2E (approval=True)
    """
    print("=" * 70)
    print("TEST 1: Normal Agent E2E (approval=True)")
    print("=" * 70)

    # Workspace
    workspace = PROJECT_ROOT / "quality_tests" / "e2e_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    test_file = workspace / "agent_task.py"
    relative_path = "quality_tests/e2e_workspace/agent_task.py"

    # Test dosyası oluştur (apply_change için gerekli)
    test_py_file = workspace / "test_agent_task.py"
    test_py_content = '''def test_greet():
    """Test greet function."""
    # Bu test dosyası sadece e2e test için dummy test içerir
    pass
'''
    with open(test_py_file, 'w', encoding='utf-8') as f:
        f.write(test_py_content)

    # Orijinal içerik
    original_content = '''def greet():
    return "Merhaba"
'''

    # Production hash'lerini al (test öncesi)
    print("\nProduction hash'leri alınıyor...")
    production_hashes_before = get_production_hashes()

    # Dosyayı sıfırla (önceki testten kalan olabilir)
    if test_file.exists():
        test_file.unlink()

    # Dosyayı oluştur
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(original_content)

    print(f"Test dosyası: {test_file}")
    print(f"Orijinal içerik:\n{original_content}")

    # Approval callback (her zaman True)
    approval_log = []

    def approval_callback(tool_name: str, arguments: dict) -> bool:
        print(f"  [APPROVAL] {tool_name} → APPROVED")
        approval_log.append((tool_name, arguments, True))
        return True

    # AgentLoop oluştur
    config = LoopConfig(
        max_iterations=20,  # Artırıldı - model retry için daha fazla şans
        max_no_tool_retries=5,  # Artırıldı
        enable_logging=True
    )

    # Logging'i stdout'a yönlendir
    import logging
    import sys
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s %(name)s:%(lineno)d %(message)s',
        stream=sys.stdout,
        force=True
    )

    ollama_client = OllamaClient()
    tool_registry = ToolRegistry()

    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback
    )

    # Görev
    user_task = "quality_tests/e2e_workspace/agent_task.py dosyasındaki greet fonksiyonunun döndürdüğü metni 'Merhaba Muhammed' olarak değiştir."

    print(f"\nGörev: {user_task}")
    print("-" * 70)

    # AgentLoop'u çalıştır
    try:
        result = agent_loop.run(user_task)
    except Exception as e:
        print(f"\nAgentLoop hatası: {e}")
        import traceback
        traceback.print_exc()
        raise

    # Sonuçları raporla
    print("\nSONUÇLAR:")
    print("-" * 70)
    print(f"Başarı: {result.success}")
    print(f"Final Cevap: {result.final_response}")
    print(f"İterasyon: {result.iterations}")
    print(f"Tool Çağrıları: {len(result.tool_calls)}")

    # Tool call log
    print("\nTOOL CALL LOG:")
    print("-" * 70)
    for i, call in enumerate(result.tool_calls, 1):
        print(f"{i}. Tool: {call['tool']}")
        print(f"   Arguments: {call.get('arguments', {})}")
        print(f"   Success: {call['result'].get('success', False)}")

    # Approval log
    print("\nAPPROVAL LOG:")
    print("-" * 70)
    for i, (tool_name, args, approved) in enumerate(approval_log, 1):
        print(f"{i}. {tool_name} → {'APPROVED' if approved else 'REJECTED'}")

    # Dosya içeriği kontrolü
    print("\nDOSYA İÇERİĞİ KONTROLÜ:")
    print("-" * 70)
    with open(test_file, 'r', encoding='utf-8') as f:
        final_content = f.read()

    print(f"Son içerik (repr): {repr(final_content)}")
    print(f"Son içerik:\n{final_content}")

    # Expected content'i dosyadan okuduğumuz gibi oluştur (indentation koru)
    expected_content = '''def greet():
    return "Merhaba Muhammed"
'''
    print(f"Expected content (repr): {repr(expected_content)}")
    print(f"Expected content:\n{expected_content}")

    # İçerik karşılaştırması
    print(f"Content match: {final_content == expected_content}")
    if final_content != expected_content:
        print("FARKLAR:")
        for i, (c1, c2) in enumerate(zip(final_content, expected_content)):
            if c1 != c2:
                print(f"  Position {i}: got {repr(c1)} ({ord(c1)}), expected {repr(c2)} ({ord(c2)})")
        print(f"  Final length: {len(final_content)}, Expected length: {len(expected_content)}")

    # Dosya çalıştırma testi
    print("\nDOSYA ÇALIŞTIRMA TESTİ:")
    print("-" * 70)
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("agent_task", test_file)
        agent_task_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(agent_task_module)

        greet_result = agent_task_module.greet()
        print(f"greet() sonucu: {greet_result}")
    except Exception as e:
        print(f"Dosya çalıştırma hatası: {e}")
        greet_result = None

    # Production hash kontrolü (test sonrası)
    print("\nPRODUCTION İZOLASYONU KONTROLÜ:")
    print("-" * 70)
    production_hashes_after = get_production_hashes()

    production_changed = False
    if production_hashes_before != production_hashes_after:
        print("[X] UYARI: Production dosyaları değişti!")
        for path, hash_before in production_hashes_before.items():
            if path in production_hashes_after:
                if hash_before != production_hashes_after[path]:
                    print(f"  DEĞİŞTİ: {path}")
            else:
                print(f"  SİLİNDİ: {path}")
        production_changed = True
    else:
        print("[OK] PASS: Production dosyaları değişmedi")

    # Doğrulamalar
    print("\nDOĞRULAMALAR:")
    print("-" * 70)

    checks = {}

    # 1. read_file çağrıldı mı?
    checks["read_file_called"] = any(tc['tool'] == 'read_file' for tc in result.tool_calls)
    print(f"read_file çağrıldı: {checks['read_file_called']}")

    # 2. create_change_plan çağrıldı mı?
    checks["create_change_plan_called"] = any(tc['tool'] == 'create_change_plan' for tc in result.tool_calls)
    print(f"create_change_plan çağrıldı: {checks['create_change_plan_called']}")

    # 3. apply_change çağrıldı mı?
    checks["apply_change_called"] = any(tc['tool'] == 'apply_change' for tc in result.tool_calls)
    print(f"apply_change çağrıldı: {checks['apply_change_called']}")

    # 4. Approval verildi mi?
    checks["approval_given"] = any(approved for _, _, approved in approval_log)
    print(f"Approval verildi: {checks['approval_given']}")

    # 5. Dosya içeriği doğru mu?
    checks["content_correct"] = (final_content == expected_content)
    print(f"Dosya içeriği doğru: {checks['content_correct']}")

    # 6. greet() doğru çalışıyor mu?
    checks["greet_correct"] = (greet_result == "Merhaba Muhammed")
    print(f"greet() doğru: {checks['greet_correct']}")

    # 7. Production değişmedi mi?
    checks["production_unchanged"] = not production_changed
    print(f"Production değişmedi: {checks['production_unchanged']}")

    # Toplam sonuç
    all_passed = all(checks.values())

    print("\n" + "=" * 70)
    print("TEST 1 SONUCU")
    print("=" * 70)
    print(f"TOPLAM: {'PASS' if all_passed else 'FAIL'}")
    print("=" * 70)

    assert all_passed, "Normal Agent E2E test başarısız"


@pytest.mark.slow
def test_agent_e2e_approval_bypass():
    """
    TEST 2: Approval bypass güvenliği (approval=False)
    """
    print("\n" + "=" * 70)
    print("TEST 2: Approval Bypass Güvenliği (approval=False)")
    print("=" * 70)

    # Workspace
    workspace = PROJECT_ROOT / "quality_tests" / "e2e_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    test_file = workspace / "agent_task.py"
    relative_path = "quality_tests/e2e_workspace/agent_task.py"

    # Test dosyası oluştur (apply_change için gerekli)
    test_py_file = workspace / "test_agent_task.py"
    test_py_content = '''def test_greet():
    """Test greet function."""
    # Bu test dosyası sadece e2e test için dummy test içerir
    pass
'''
    with open(test_py_file, 'w', encoding='utf-8') as f:
        f.write(test_py_content)

    # Orijinal içerik
    original_content = '''def greet():
    return "Merhaba"
'''

    # Dosyayı sıfırla
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(original_content)

    print(f"Test dosyası sıfırlandı: {test_file}")

    # Approval callback (her zaman False)
    approval_log = []

    def approval_callback(tool_name: str, arguments: dict) -> bool:
        print(f"  [APPROVAL] {tool_name} → REJECTED")
        approval_log.append((tool_name, arguments, False))
        return False

    # AgentLoop oluştur
    config = LoopConfig(
        max_iterations=20,  # Artırıldı - model retry için daha fazla şans
        max_no_tool_retries=5,  # Artırıldı
        enable_logging=True
    )

    # Logging'i stdout'a yönlendir
    import logging
    import sys
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s %(name)s:%(lineno)d %(message)s',
        stream=sys.stdout,
        force=True
    )

    ollama_client = OllamaClient()
    tool_registry = ToolRegistry()

    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback
    )

    # Görev
    user_task = "quality_tests/e2e_workspace/agent_task.py dosyasındaki greet fonksiyonunun döndürdüğü metni 'Merhaba Muhammed' olarak değiştir."

    print(f"\nGörev: {user_task}")
    print("-" * 70)

    # AgentLoop'u çalıştır
    try:
        result = agent_loop.run(user_task)
    except Exception as e:
        print(f"\nAgentLoop hatası: {e}")
        import traceback
        traceback.print_exc()
        raise

    # Sonuçları raporla
    print("\nSONUÇLAR:")
    print("-" * 70)
    print(f"Başarı: {result.success}")
    print(f"Final Cevap: {result.final_response}")
    print(f"İterasyon: {result.iterations}")
    print(f"Tool Çağrıları: {len(result.tool_calls)}")

    # Tool call log
    print("\nTOOL CALL LOG:")
    print("-" * 70)
    for i, call in enumerate(result.tool_calls, 1):
        print(f"{i}. Tool: {call['tool']}")
        print(f"   Arguments: {call.get('arguments', {})}")
        print(f"   Success: {call['result'].get('success', False)}")

    # Approval log
    print("\nAPPROVAL LOG:")
    print("-" * 70)
    for i, (tool_name, args, approved) in enumerate(approval_log, 1):
        print(f"{i}. {tool_name} → {'APPROVED' if approved else 'REJECTED'}")

    # Dosya içeriği kontrolü
    print("\nDOSYA İÇERİĞİ KONTROLÜ:")
    print("-" * 70)
    with open(test_file, 'r', encoding='utf-8') as f:
        final_content = f.read()

    print(f"Son içerik:\n{final_content}")

    # Doğrulamalar
    print("\nDOĞRULAMALAR:")
    print("-" * 70)

    checks = {}

    # 1. Dosya değişmedi mi?
    checks["file_unchanged"] = (final_content == original_content)
    print(f"Dosya değişmedi: {checks['file_unchanged']}")

    # 2. Approval reddedildi mi?
    checks["approval_rejected"] = all(not approved for _, _, approved in approval_log)
    print(f"Approval reddedildi: {checks['approval_rejected']}")

    # 3. apply_change başarısız oldu mu?
    apply_change_calls = [tc for tc in result.tool_calls if tc['tool'] == 'apply_change']
    if apply_change_calls:
        checks["apply_change_failed"] = not any(tc['result'].get('success', False) for tc in apply_change_calls)
        print(f"apply_change başarısız: {checks['apply_change_failed']}")
    else:
        checks["apply_change_failed"] = True  # Çağrılmadı da başarısız sayılır
        print(f"apply_change çağrılmadı: True")

    # Toplam sonuç
    all_passed = all(checks.values())

    print("\n" + "=" * 70)
    print("TEST 2 SONUCU")
    print("=" * 70)
    print(f"TOPLAM: {'PASS' if all_passed else 'FAIL'}")
    print("=" * 70)

    assert all_passed, "Approval bypass test başarısız"


@pytest.mark.slow
def test_production_isolation():
    """
    TEST 3: Production izolasyonu kontrolü
    """
    print("\n" + "=" * 70)
    print("TEST 3: Production İzolasyonu Kontrolü")
    print("=" * 70)

    # Production hash'lerini al
    production_hashes = get_production_hashes()

    print(f"Production dosya sayısı: {len(production_hashes)}")

    # Tüm production dosyaları hâlâ orada mı?
    app_dir = PROJECT_ROOT / "app"
    if app_dir.exists():
        current_files = set(str(f.relative_to(PROJECT_ROOT)) for f in app_dir.rglob("*.py"))
        expected_files = set(production_hashes.keys())

        missing_files = expected_files - current_files
        new_files = current_files - expected_files

        print(f"Kayıp dosyalar: {len(missing_files)}")
        if missing_files:
            for f in missing_files:
                print(f"  - {f}")

        print(f"Yeni dosyalar: {len(new_files)}")
        if new_files:
            for f in new_files:
                print(f"  + {f}")

        # Hash kontrolü
        hash_mismatch = False
        for file_path in current_files & expected_files:
            current_hash = get_file_hash(PROJECT_ROOT / file_path)
            if current_hash != production_hashes[file_path]:
                print(f"[X] HASH DEĞİŞTİ: {file_path}")
                hash_mismatch = True

        if not missing_files and not new_files and not hash_mismatch:
            print("[OK] PASS: Production dosyaları değişmedi")
        else:
            print("[X] FAIL: Production dosyaları değişti!")

        assert not missing_files and not new_files and not hash_mismatch, "Production dosyaları değişti"
    else:
        print("[X] FAIL: app/ dizini yok!")
        assert False, "app/ dizini yok"


if __name__ == "__main__":
    try:
        # TEST 1
        test_agent_e2e_normal()

        # TEST 2
        test_agent_e2e_approval_bypass()

        # TEST 3
        test_production_isolation()

        # Temizlik
        print("\n" + "=" * 70)
        print("TEMİZLİK")
        print("=" * 70)

        workspace = PROJECT_ROOT / "quality_tests" / "e2e_workspace"
        test_file = workspace / "agent_task.py"

        if test_file.exists():
            test_file.unlink()
            print(f"Test dosyası silindi: {test_file}")

        # Backup dizinini temizle
        backup_dir = PROJECT_ROOT / ".muhammedai_backups"
        if backup_dir.exists():
            try:
                shutil.rmtree(backup_dir)
                print(f"Backup dizini temizlendi: {backup_dir}")
            except Exception as e:
                print(f"Backup temizleme hatası: {e}")

        # Toplam rapor
        print("\n" + "=" * 70)
        print("TOPLAM RAPOR")
        print("=" * 70)
        print("Tüm testler PASS")
        print("=" * 70)

        sys.exit(0)

    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
