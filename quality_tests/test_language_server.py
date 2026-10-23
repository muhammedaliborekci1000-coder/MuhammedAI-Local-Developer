"""
Quality Test: Language Server
Language server system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.language_server import (
    LanguageId,
    ServerStatus,
    LanguageServerConfig,
    ServerProcess,
    LanguageServerManager
)


def test_language_id_enum():
    """
    Test: LanguageId enum.
    """
    print("=" * 70)
    print("TEST: LanguageId Enum")
    print("=" * 70)
    
    assert LanguageId.PYTHON.value == "python"
    assert LanguageId.JAVASCRIPT.value == "javascript"
    assert LanguageId.TYPESCRIPT.value == "typescript"
    assert LanguageId.GO.value == "go"
    assert LanguageId.RUST.value == "rust"
    
    print(f"  All enum values verified")
    print(f"  Total languages: {len(LanguageId)}")
    
    print("\n" + "=" * 70)
    print("PASS: LanguageId enum")
    print("=" * 70)


def test_server_status_enum():
    """
    Test: ServerStatus enum.
    """
    print("=" * 70)
    print("TEST: ServerStatus Enum")
    print("=" * 70)
    
    assert ServerStatus.STOPPED.value == "stopped"
    assert ServerStatus.STARTING.value == "starting"
    assert ServerStatus.RUNNING.value == "running"
    assert ServerStatus.STOPPING.value == "stopping"
    assert ServerStatus.ERROR.value == "error"
    
    print(f"  All enum values verified")
    print(f"  Total statuses: {len(ServerStatus)}")
    
    print("\n" + "=" * 70)
    print("PASS: ServerStatus enum")
    print("=" * 70)


def test_language_server_config_dataclass():
    """
    Test: LanguageServerConfig dataclass.
    """
    print("=" * 70)
    print("TEST: LanguageServerConfig Dataclass")
    print("=" * 70)
    
    config = LanguageServerConfig(
        language_id=LanguageId.PYTHON,
        command=["python"],
        args=["-m", "pylsp"]
    )
    
    assert config.language_id == LanguageId.PYTHON, "Language ID eşleşmeli"
    assert config.command == ["python"], "Command eşleşmeli"
    assert config.enabled == True, "Enabled olmalı"
    
    print(f"  Language: {config.language_id.value}")
    print(f"  Command: {config.command}")
    print(f"  Enabled: {config.enabled}")
    
    print("\n" + "=" * 70)
    print("PASS: LanguageServerConfig dataclass")
    print("=" * 70)


def test_server_process_dataclass():
    """
    Test: ServerProcess dataclass.
    """
    print("=" * 70)
    print("TEST: ServerProcess Dataclass")
    print("=" * 70)
    
    config = LanguageServerConfig(
        language_id=LanguageId.PYTHON,
        command=["python"]
    )
    
    process = ServerProcess(
        config=config,
        status=ServerStatus.STOPPED
    )
    
    assert process.config == config, "Config eşleşmeli"
    assert process.status == ServerStatus.STOPPED, "Status eşleşmeli"
    
    print(f"  Status: {process.status.value}")
    print(f"  PID: {process.pid}")
    
    print("\n" + "=" * 70)
    print("PASS: ServerProcess dataclass")
    print("=" * 70)


def test_language_server_manager_initialization():
    """
    Test: LanguageServerManager initialization.
    """
    print("=" * 70)
    print("TEST: LanguageServerManager Initialization")
    print("=" * 70)
    
    manager = LanguageServerManager()
    
    assert len(manager.configs) > 0, "Default configs olmalı"
    assert len(manager.servers) == 0, "Servers boş olmalı"
    
    print(f"  Default configs: {len(manager.configs)}")
    print(f"  Running servers: {len(manager.servers)}")
    
    print("\n" + "=" * 70)
    print("PASS: LanguageServerManager initialization")
    print("=" * 70)


def test_register_server():
    """
    Test: Register server.
    """
    print("=" * 70)
    print("TEST: Register Server")
    print("=" * 70)
    
    manager = LanguageServerManager()
    
    config = LanguageServerConfig(
        language_id=LanguageId.RUBY,
        command=["ruby"],
        args=["-m", "solargraph"]
    )
    
    result = manager.register_server(config)
    
    assert result == True, "Registration başarılı olmalı"
    assert LanguageId.RUBY in manager.configs, "Ruby config eklenmeli"
    
    print(f"  Registered: {result}")
    print(f"  Ruby in configs: {LanguageId.RUBY in manager.configs}")
    
    print("\n" + "=" * 70)
    print("PASS: Register server")
    print("=" * 70)


def test_unregister_server():
    """
    Test: Unregister server.
    """
    print("=" * 70)
    print("TEST: Unregister Server")
    print("=" * 70)
    
    manager = LanguageServerManager()
    
    # First register
    config = LanguageServerConfig(
        language_id=LanguageId.RUBY,
        command=["ruby"]
    )
    manager.register_server(config)
    
    # Then unregister
    result = manager.unregister_server(LanguageId.RUBY)
    
    assert result == True, "Unregistration başarılı olmalı"
    assert LanguageId.RUBY not in manager.configs, "Ruby config silinmeli"
    
    print(f"  Unregistered: {result}")
    print(f"  Ruby in configs: {LanguageId.RUBY in manager.configs}")
    
    print("\n" + "=" * 70)
    print("PASS: Unregister server")
    print("=" * 70)


def test_get_server_config():
    """
    Test: Get server config.
    """
    print("=" * 70)
    print("TEST: Get Server Config")
    print("=" * 70)
    
    manager = LanguageServerManager()
    
    config = manager.get_server_config(LanguageId.PYTHON)
    
    assert config is not None, "Config olmalı"
    assert config.language_id == LanguageId.PYTHON, "Language ID eşleşmeli"
    
    print(f"  Language: {config.language_id.value}")
    print(f"  Command: {config.command}")
    
    print("\n" + "=" * 70)
    print("PASS: Get server config")
    print("=" * 70)


def test_update_server_config():
    """
    Test: Update server config.
    """
    print("=" * 70)
    print("TEST: Update Server Config")
    print("=" * 70)
    
    manager = LanguageServerManager()
    
    new_config = LanguageServerConfig(
        language_id=LanguageId.PYTHON,
        command=["python3"],
        args=["-m", "pylsp"]
    )
    
    result = manager.update_server_config(LanguageId.PYTHON, new_config)
    
    assert result == True, "Update başarılı olmalı"
    
    updated_config = manager.get_server_config(LanguageId.PYTHON)
    assert updated_config.command == ["python3"], "Command güncellenmeli"
    
    print(f"  Updated: {result}")
    print(f"  New command: {updated_config.command}")
    
    print("\n" + "=" * 70)
    print("PASS: Update server config")
    print("=" * 70)


def test_get_supported_languages():
    """
    Test: Get supported languages.
    """
    print("=" * 70)
    print("TEST: Get Supported Languages")
    print("=" * 70)
    
    manager = LanguageServerManager()
    
    languages = manager.get_supported_languages()
    
    assert len(languages) > 0, "Languages olmalı"
    assert LanguageId.PYTHON in languages, "Python desteklenmeli"
    
    print(f"  Supported languages: {len(languages)}")
    print(f"  Python supported: {LanguageId.PYTHON in languages}")
    
    print("\n" + "=" * 70)
    print("PASS: Get supported languages")
    print("=" * 70)


def test_is_language_supported():
    """
    Test: Is language supported.
    """
    print("=" * 70)
    print("TEST: Is Language Supported")
    print("=" * 70)
    
    manager = LanguageServerManager()
    
    python_supported = manager.is_language_supported(LanguageId.PYTHON)
    ruby_supported = manager.is_language_supported(LanguageId.RUBY)
    
    assert python_supported == True, "Python desteklenmeli"
    
    print(f"  Python supported: {python_supported}")
    print(f"  Ruby supported: {ruby_supported}")
    
    print("\n" + "=" * 70)
    print("PASS: Is language supported")
    print("=" * 70)


def test_get_server_capabilities():
    """
    Test: Get server capabilities.
    """
    print("=" * 70)
    print("TEST: Get Server Capabilities")
    print("=" * 70)
    
    manager = LanguageServerManager()
    
    capabilities = manager.get_server_capabilities(LanguageId.PYTHON)
    
    assert len(capabilities) > 0, "Capabilities olmalı"
    
    print(f"  Capabilities: {capabilities}")
    
    print("\n" + "=" * 70)
    print("PASS: Get server capabilities")
    print("=" * 70)


def test_get_server_status():
    """
    Test: Get server status.
    """
    print("=" * 70)
    print("TEST: Get Server Status")
    print("=" * 70)
    
    manager = LanguageServerManager()
    
    status = manager.get_server_status(LanguageId.PYTHON)
    
    assert status is None, "Başlatılmadıysa None olmalı"
    
    print(f"  Status: {status}")
    
    print("\n" + "=" * 70)
    print("PASS: Get server status")
    print("=" * 70)


def test_get_all_servers():
    """
    Test: Get all servers.
    """
    print("=" * 70)
    print("TEST: Get All Servers")
    print("=" * 70)
    
    manager = LanguageServerManager()
    
    servers = manager.get_all_servers()
    
    assert isinstance(servers, dict), "Dict olmalı"
    
    print(f"  Servers: {len(servers)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all servers")
    print("=" * 70)


def test_enable_server():
    """
    Test: Enable server.
    """
    print("=" * 70)
    print("TEST: Enable Server")
    print("=" * 70)
    
    manager = LanguageServerManager()
    
    # First disable
    manager.disable_server(LanguageId.PYTHON)
    
    # Then enable
    result = manager.enable_server(LanguageId.PYTHON)
    
    assert result == True, "Enable başarılı olmalı"
    
    config = manager.get_server_config(LanguageId.PYTHON)
    assert config.enabled == True, "Enabled olmalı"
    
    print(f"  Enabled: {result}")
    print(f"  Config enabled: {config.enabled}")
    
    print("\n" + "=" * 70)
    print("PASS: Enable server")
    print("=" * 70)


def test_disable_server():
    """
    Test: Disable server.
    """
    print("=" * 70)
    print("TEST: Disable Server")
    print("=" * 70)
    
    manager = LanguageServerManager()
    
    result = manager.disable_server(LanguageId.PYTHON)
    
    assert result == True, "Disable başarılı olmalı"
    
    config = manager.get_server_config(LanguageId.PYTHON)
    assert config.enabled == False, "Disabled olmalı"
    
    print(f"  Disabled: {result}")
    print(f"  Config enabled: {config.enabled}")
    
    print("\n" + "=" * 70)
    print("PASS: Disable server")
    print("=" * 70)


def test_is_server_running():
    """
    Test: Is server running.
    """
    print("=" * 70)
    print("TEST: Is Server Running")
    print("=" * 70)
    
    manager = LanguageServerManager()
    
    is_running = manager.is_server_running(LanguageId.PYTHON)
    
    assert is_running == False, "Başlatılmadıysa False olmalı"
    
    print(f"  Running: {is_running}")
    
    print("\n" + "=" * 70)
    print("PASS: Is server running")
    print("=" * 70)


def test_get_server_pid():
    """
    Test: Get server PID.
    """
    print("=" * 70)
    print("TEST: Get Server PID")
    print("=" * 70)
    
    manager = LanguageServerManager()
    
    pid = manager.get_server_pid(LanguageId.PYTHON)
    
    assert pid is None, "Başlatılmadıysa None olmalı"
    
    print(f"  PID: {pid}")
    
    print("\n" + "=" * 70)
    print("PASS: Get server PID")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_language_id_enum()
        test2 = test_server_status_enum()
        test3 = test_language_server_config_dataclass()
        test4 = test_server_process_dataclass()
        test5 = test_language_server_manager_initialization()
        test6 = test_register_server()
        test7 = test_unregister_server()
        test8 = test_get_server_config()
        test9 = test_update_server_config()
        test10 = test_get_supported_languages()
        test11 = test_is_language_supported()
        test12 = test_get_server_capabilities()
        test13 = test_get_server_status()
        test14 = test_get_all_servers()
        test15 = test_enable_server()
        test16 = test_disable_server()
        test17 = test_is_server_running()
        test18 = test_get_server_pid()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"LanguageId Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"ServerStatus Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"LanguageServerConfig Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"ServerProcess Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"LanguageServerManager Initialization: {'PASS' if test5 else 'FAIL'}")
        print(f"Register Server: {'PASS' if test6 else 'FAIL'}")
        print(f"Unregister Server: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Server Config: {'PASS' if test8 else 'FAIL'}")
        print(f"Update Server Config: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Supported Languages: {'PASS' if test10 else 'FAIL'}")
        print(f"Is Language Supported: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Server Capabilities: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Server Status: {'PASS' if test13 else 'FAIL'}")
        print(f"Get All Servers: {'PASS' if test14 else 'FAIL'}")
        print(f"Enable Server: {'PASS' if test15 else 'FAIL'}")
        print(f"Disable Server: {'PASS' if test16 else 'FAIL'}")
        print(f"Is Server Running: {'PASS' if test17 else 'FAIL'}")
        print(f"Get Server PID: {'PASS' if test18 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18])
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
