"""
Quality Test: LSP Server
LSP server system testleri.
"""

import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.lsp_server import (
    LSPServer,
    ServerCapability,
    TextDocumentSyncKind,
    ServerInfo,
    ServerCapabilities,
    InitializeParams,
    InitializeResult,
    TextDocumentItem,
    DocumentState
)


def test_server_capability_enum():
    """
    Test: ServerCapability enum.
    """
    print("=" * 70)
    print("TEST: ServerCapability Enum")
    print("=" * 70)
    
    assert ServerCapability.TEXT_DOCUMENT_SYNC.value == "textDocumentSync"
    assert ServerCapability.COMPLETION.value == "completionProvider"
    assert ServerCapability.HOVER.value == "hoverProvider"
    assert ServerCapability.DEFINITION.value == "definitionProvider"
    
    print(f"  All enum values verified")
    print(f"  Total capabilities: {len(ServerCapability)}")
    
    print("\n" + "=" * 70)
    print("PASS: ServerCapability enum")
    print("=" * 70)


def test_text_document_sync_kind_enum():
    """
    Test: TextDocumentSyncKind enum.
    """
    print("=" * 70)
    print("TEST: TextDocumentSyncKind Enum")
    print("=" * 70)
    
    assert TextDocumentSyncKind.NONE.value == 0
    assert TextDocumentSyncKind.FULL.value == 1
    assert TextDocumentSyncKind.INCREMENTAL.value == 2
    
    print(f"  All enum values verified")
    print(f"  Total kinds: {len(TextDocumentSyncKind)}")
    
    print("\n" + "=" * 70)
    print("PASS: TextDocumentSyncKind enum")
    print("=" * 70)


def test_server_info_dataclass():
    """
    Test: ServerInfo dataclass.
    """
    print("=" * 70)
    print("TEST: ServerInfo Dataclass")
    print("=" * 70)
    
    info = ServerInfo(name="Test Server", version="1.0.0")
    
    assert info.name == "Test Server", "Name eşleşmeli"
    assert info.version == "1.0.0", "Version eşleşmeli"
    
    print(f"  Name: {info.name}")
    print(f"  Version: {info.version}")
    
    print("\n" + "=" * 70)
    print("PASS: ServerInfo dataclass")
    print("=" * 70)


def test_server_capabilities_dataclass():
    """
    Test: ServerCapabilities dataclass.
    """
    print("=" * 70)
    print("TEST: ServerCapabilities Dataclass")
    print("=" * 70)
    
    capabilities = ServerCapabilities(
        textDocumentSync=1,
        hoverProvider=True,
        definitionProvider=True
    )
    
    assert capabilities.textDocumentSync == 1, "textDocumentSync eşleşmeli"
    assert capabilities.hoverProvider == True, "hoverProvider eşleşmeli"
    
    print(f"  TextDocumentSync: {capabilities.textDocumentSync}")
    print(f"  HoverProvider: {capabilities.hoverProvider}")
    
    print("\n" + "=" * 70)
    print("PASS: ServerCapabilities dataclass")
    print("=" * 70)


def test_initialize_params_dataclass():
    """
    Test: InitializeParams dataclass.
    """
    print("=" * 70)
    print("TEST: InitializeParams Dataclass")
    print("=" * 70)
    
    params = InitializeParams(
        processId=12345,
        rootUri="file:///path/to/project",
        trace="off"
    )
    
    assert params.processId == 12345, "Process ID eşleşmeli"
    assert params.rootUri == "file:///path/to/project", "Root URI eşleşmeli"
    
    print(f"  Process ID: {params.processId}")
    print(f"  Root URI: {params.rootUri}")
    
    print("\n" + "=" * 70)
    print("PASS: InitializeParams dataclass")
    print("=" * 70)


def test_initialize_result_dataclass():
    """
    Test: InitializeResult dataclass.
    """
    print("=" * 70)
    print("TEST: InitializeResult Dataclass")
    print("=" * 70)
    
    result = InitializeResult(
        capabilities=ServerCapabilities(),
        serverInfo=ServerInfo(name="Test", version="1.0")
    )
    
    assert result.serverInfo.name == "Test", "Server name eşleşmeli"
    assert isinstance(result.capabilities, ServerCapabilities), "Capabilities type eşleşmeli"
    
    print(f"  Server Name: {result.serverInfo.name}")
    print(f"  Server Version: {result.serverInfo.version}")
    
    print("\n" + "=" * 70)
    print("PASS: InitializeResult dataclass")
    print("=" * 70)


def test_text_document_item_dataclass():
    """
    Test: TextDocumentItem dataclass.
    """
    print("=" * 70)
    print("TEST: TextDocumentItem Dataclass")
    print("=" * 70)
    
    item = TextDocumentItem(
        uri="file:///test.py",
        languageId="python",
        version=1,
        text="def hello(): pass"
    )
    
    assert item.uri == "file:///test.py", "URI eşleşmeli"
    assert item.languageId == "python", "Language ID eşleşmeli"
    
    print(f"  URI: {item.uri}")
    print(f"  Language: {item.languageId}")
    
    print("\n" + "=" * 70)
    print("PASS: TextDocumentItem dataclass")
    print("=" * 70)


def test_document_state_dataclass():
    """
    Test: DocumentState dataclass.
    """
    print("=" * 70)
    print("TEST: DocumentState Dataclass")
    print("=" * 70)
    
    state = DocumentState(
        uri="file:///test.py",
        version=1,
        text="def hello(): pass",
        languageId="python"
    )
    
    assert state.uri == "file:///test.py", "URI eşleşmeli"
    assert state.version == 1, "Version eşleşmeli"
    
    print(f"  URI: {state.uri}")
    print(f"  Version: {state.version}")
    
    print("\n" + "=" * 70)
    print("PASS: DocumentState dataclass")
    print("=" * 70)


def test_lsp_server_initialization():
    """
    Test: LSP server initialization.
    """
    print("=" * 70)
    print("TEST: LSP Server Initialization")
    print("=" * 70)
    
    server = LSPServer()
    
    assert server.server_name == "MuhammedAI LSP Server", "Server name eşleşmeli"
    assert server.version == "1.0.0", "Version eşleşmeli"
    assert server.is_initialized == False, "Initialized olmamalı"
    assert server.is_shutdown == False, "Shutdown olmamalı"
    
    print(f"  Server Name: {server.server_name}")
    print(f"  Version: {server.version}")
    print(f"  Initialized: {server.is_initialized}")
    
    print("\n" + "=" * 70)
    print("PASS: LSP server initialization")
    print("=" * 70)


def test_lsp_server_custom_initialization():
    """
    Test: LSP server custom initialization.
    """
    print("=" * 70)
    print("TEST: LSP Server Custom Initialization")
    print("=" * 70)
    
    server = LSPServer(server_name="Custom Server", version="2.0.0")
    
    assert server.server_name == "Custom Server", "Custom name eşleşmeli"
    assert server.version == "2.0.0", "Custom version eşleşmeli"
    
    print(f"  Server Name: {server.server_name}")
    print(f"  Version: {server.version}")
    
    print("\n" + "=" * 70)
    print("PASS: LSP server custom initialization")
    print("=" * 70)


def test_lsp_server_capabilities():
    """
    Test: LSP server capabilities.
    """
    print("=" * 70)
    print("TEST: LSP Server Capabilities")
    print("=" * 70)
    
    server = LSPServer()
    
    assert server.capabilities.textDocumentSync == 1, "textDocumentSync eşleşmeli"
    assert server.capabilities.completionProvider is not None, "completionProvider olmalı"
    assert server.capabilities.hoverProvider == True, "hoverProvider eşleşmeli"
    assert server.capabilities.definitionProvider == True, "definitionProvider eşleşmeli"
    
    print(f"  TextDocumentSync: {server.capabilities.textDocumentSync}")
    print(f"  HoverProvider: {server.capabilities.hoverProvider}")
    print(f"  DefinitionProvider: {server.capabilities.definitionProvider}")
    
    print("\n" + "=" * 70)
    print("PASS: LSP server capabilities")
    print("=" * 70)


def test_lsp_server_documents():
    """
    Test: LSP server documents.
    """
    print("=" * 70)
    print("TEST: LSP Server Documents")
    print("=" * 70)
    
    server = LSPServer()
    
    assert len(server.documents) == 0, "Documents boş olmalı"
    
    # Add document
    server.documents["file:///test.py"] = DocumentState(
        uri="file:///test.py",
        version=1,
        text="test",
        languageId="python"
    )
    
    assert len(server.documents) == 1, "1 document olmalı"
    assert "file:///test.py" in server.documents, "Document eklenmeli"
    
    print(f"  Documents: {len(server.documents)}")
    
    print("\n" + "=" * 70)
    print("PASS: LSP server documents")
    print("=" * 70)


def test_lsp_server_handle_initialize():
    """
    Test: LSP server handle initialize.
    """
    print("=" * 70)
    print("TEST: LSP Server Handle Initialize")
    print("=" * 70)
    
    async def _test():
        server = LSPServer()
        
        params = {
            "processId": 12345,
            "rootUri": "file:///path/to/project",
            "capabilities": {}
        }
        
        result = await server._handle_initialize(params)
        
        assert result is not None, "Result olmalı"
        assert "capabilities" in result, "Capabilities olmalı"
        assert "serverInfo" in result, "ServerInfo olmalı"
        
        print(f"  Capabilities: {len(result['capabilities'])} keys")
        print(f"  Server Name: {result['serverInfo']['name']}")
    
    asyncio.run(_test())
    
    print("\n" + "=" * 70)
    print("PASS: LSP server handle initialize")
    print("=" * 70)


def test_lsp_server_handle_shutdown():
    """
    Test: LSP server handle shutdown.
    """
    print("=" * 70)
    print("TEST: LSP Server Handle Shutdown")
    print("=" * 70)
    
    async def _test():
        server = LSPServer()
        
        result = await server._handle_shutdown()
        
        assert result is not None, "Result olmalı"
        assert server.is_shutdown == True, "Shutdown olmalı"
        
        print(f"  Shutdown: {server.is_shutdown}")
    
    asyncio.run(_test())
    
    print("\n" + "=" * 70)
    print("PASS: LSP server handle shutdown")
    print("=" * 70)


def test_lsp_server_handle_did_open():
    """
    Test: LSP server handle didOpen.
    """
    print("=" * 70)
    print("TEST: LSP Server Handle DidOpen")
    print("=" * 70)
    
    async def _test():
        server = LSPServer()
        
        params = {
            "textDocument": {
                "uri": "file:///test.py",
                "languageId": "python",
                "version": 1,
                "text": "def hello(): pass"
            }
        }
        
        await server._handle_did_open(params)
        
        assert "file:///test.py" in server.documents, "Document eklenmeli"
        assert server.documents["file:///test.py"].languageId == "python", "Language ID eşleşmeli"
        
        print(f"  Documents: {len(server.documents)}")
        print(f"  Language: {server.documents['file:///test.py'].languageId}")
    
    asyncio.run(_test())
    
    print("\n" + "=" * 70)
    print("PASS: LSP server handle didOpen")
    print("=" * 70)


def test_lsp_server_handle_did_change():
    """
    Test: LSP server handle didChange.
    """
    print("=" * 70)
    print("TEST: LSP Server Handle DidChange")
    print("=" * 70)
    
    async def _test():
        server = LSPServer()
        
        # First open document
        await server._handle_did_open({
            "textDocument": {
                "uri": "file:///test.py",
                "languageId": "python",
                "version": 1,
                "text": "old text"
            }
        })
        
        # Then change it
        params = {
            "textDocument": {
                "uri": "file:///test.py",
                "version": 2
            },
            "contentChanges": [{"text": "new text"}]
        }
        
        await server._handle_did_change(params)
        
        assert server.documents["file:///test.py"].text == "new text", "Text güncellenmeli"
        assert server.documents["file:///test.py"].version == 2, "Version güncellenmeli"
        
        print(f"  Text: {server.documents['file:///test.py'].text}")
        print(f"  Version: {server.documents['file:///test.py'].version}")
    
    asyncio.run(_test())
    
    print("\n" + "=" * 70)
    print("PASS: LSP server handle didChange")
    print("=" * 70)


def test_lsp_server_handle_did_close():
    """
    Test: LSP server handle didClose.
    """
    print("=" * 70)
    print("TEST: LSP Server Handle DidClose")
    print("=" * 70)
    
    async def _test():
        server = LSPServer()
        
        # First open document
        await server._handle_did_open({
            "textDocument": {
                "uri": "file:///test.py",
                "languageId": "python",
                "version": 1,
                "text": "test"
            }
        })
        
        # Then close it
        params = {
            "textDocument": {
                "uri": "file:///test.py"
            }
        }
        
        await server._handle_did_close(params)
        
        assert "file:///test.py" not in server.documents, "Document silinmeli"
        
        print(f"  Documents: {len(server.documents)}")
    
    asyncio.run(_test())
    
    print("\n" + "=" * 70)
    print("PASS: LSP server handle didClose")
    print("=" * 70)


def test_lsp_server_handle_completion():
    """
    Test: LSP server handle completion.
    """
    print("=" * 70)
    print("TEST: LSP Server Handle Completion")
    print("=" * 70)
    
    async def _test():
        server = LSPServer()
        
        # Open document first
        await server._handle_did_open({
            "textDocument": {
                "uri": "file:///test.py",
                "languageId": "python",
                "version": 1,
                "text": "test"
            }
        })
        
        params = {
            "textDocument": {"uri": "file:///test.py"},
            "position": {"line": 0, "character": 0}
        }
        
        result = await server._handle_completion(params)
        
        assert result is not None, "Result olmalı"
        assert "items" in result, "Items olmalı"
        assert isinstance(result["items"], list), "Items list olmalı"
        
        print(f"  Items: {len(result['items'])}")
    
    asyncio.run(_test())
    
    print("\n" + "=" * 70)
    print("PASS: LSP server handle completion")
    print("=" * 70)


def test_lsp_server_handle_hover():
    """
    Test: LSP server handle hover.
    """
    print("=" * 70)
    print("TEST: LSP Server Handle Hover")
    print("=" * 70)
    
    async def _test():
        server = LSPServer()
        
        # Open document first
        await server._handle_did_open({
            "textDocument": {
                "uri": "file:///test.py",
                "languageId": "python",
                "version": 1,
                "text": "test"
            }
        })
        
        params = {
            "textDocument": {"uri": "file:///test.py"},
            "position": {"line": 0, "character": 0}
        }
        
        result = await server._handle_hover(params)
        
        assert result is not None, "Result olmalı"
        assert "contents" in result, "Contents olmalı"
        
        print(f"  Contents: {result['contents']}")
    
    asyncio.run(_test())
    
    print("\n" + "=" * 70)
    print("PASS: LSP server handle hover")
    print("=" * 70)


def test_lsp_server_handle_definition():
    """
    Test: LSP server handle definition.
    """
    print("=" * 70)
    print("TEST: LSP Server Handle Definition")
    print("=" * 70)
    
    async def _test():
        server = LSPServer()
        
        # Open document first
        await server._handle_did_open({
            "textDocument": {
                "uri": "file:///test.py",
                "languageId": "python",
                "version": 1,
                "text": "test"
            }
        })
        
        params = {
            "textDocument": {"uri": "file:///test.py"},
            "position": {"line": 0, "character": 0}
        }
        
        result = await server._handle_definition(params)
        
        assert result is not None, "Result olmalı"
        assert isinstance(result, list), "Result list olmalı"
        
        print(f"  Locations: {len(result)}")
    
    asyncio.run(_test())
    
    print("\n" + "=" * 70)
    print("PASS: LSP server handle definition")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_server_capability_enum()
        test2 = test_text_document_sync_kind_enum()
        test3 = test_server_info_dataclass()
        test4 = test_server_capabilities_dataclass()
        test5 = test_initialize_params_dataclass()
        test6 = test_initialize_result_dataclass()
        test7 = test_text_document_item_dataclass()
        test8 = test_document_state_dataclass()
        test9 = test_lsp_server_initialization()
        test10 = test_lsp_server_custom_initialization()
        test11 = test_lsp_server_capabilities()
        test12 = test_lsp_server_documents()
        test13 = test_lsp_server_handle_initialize()
        test14 = test_lsp_server_handle_shutdown()
        test15 = test_lsp_server_handle_did_open()
        test16 = test_lsp_server_handle_did_change()
        test17 = test_lsp_server_handle_did_close()
        test18 = test_lsp_server_handle_completion()
        test19 = test_lsp_server_handle_hover()
        test20 = test_lsp_server_handle_definition()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"ServerCapability Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"TextDocumentSyncKind Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"ServerInfo Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"ServerCapabilities Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"InitializeParams Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"InitializeResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"TextDocumentItem Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"DocumentState Dataclass: {'PASS' if test8 else 'FAIL'}")
        print(f"LSP Server Initialization: {'PASS' if test9 else 'FAIL'}")
        print(f"LSP Server Custom Initialization: {'PASS' if test10 else 'FAIL'}")
        print(f"LSP Server Capabilities: {'PASS' if test11 else 'FAIL'}")
        print(f"LSP Server Documents: {'PASS' if test12 else 'FAIL'}")
        print(f"LSP Server Handle Initialize: {'PASS' if test13 else 'FAIL'}")
        print(f"LSP Server Handle Shutdown: {'PASS' if test14 else 'FAIL'}")
        print(f"LSP Server Handle DidOpen: {'PASS' if test15 else 'FAIL'}")
        print(f"LSP Server Handle DidChange: {'PASS' if test16 else 'FAIL'}")
        print(f"LSP Server Handle DidClose: {'PASS' if test17 else 'FAIL'}")
        print(f"LSP Server Handle Completion: {'PASS' if test18 else 'FAIL'}")
        print(f"LSP Server Handle Hover: {'PASS' if test19 else 'FAIL'}")
        print(f"LSP Server Handle Definition: {'PASS' if test20 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20])
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
