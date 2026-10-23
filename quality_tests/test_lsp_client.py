"""
Quality Test: LSP Client
LSP client system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.lsp_client import (
    LSPClient,
    LSPMessageType,
    LSPErrorCode,
    LSPMethod,
    Position,
    Range,
    Location,
    TextDocumentItem,
    TextDocumentIdentifier,
    VersionedTextDocumentIdentifier,
    CompletionItem,
    CompletionList,
    Diagnostic,
    PublishDiagnosticsParams,
    LSPClientConfig,
    LSPMessage,
    TextEdit
)


def test_lsp_message_type_enum():
    """
    Test: LSPMessageType enum.
    """
    print("=" * 70)
    print("TEST: LSPMessageType Enum")
    print("=" * 70)
    
    assert LSPMessageType.REQUEST.value == "request"
    assert LSPMessageType.RESPONSE.value == "response"
    assert LSPMessageType.NOTIFICATION.value == "notification"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(LSPMessageType)}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPMessageType enum")
    print("=" * 70)


def test_lsp_error_code_enum():
    """
    Test: LSPErrorCode enum.
    """
    print("=" * 70)
    print("TEST: LSPErrorCode Enum")
    print("=" * 70)
    
    assert LSPErrorCode.ParseError.value == -32700
    assert LSPErrorCode.InvalidRequest.value == -32600
    assert LSPErrorCode.MethodNotFound.value == -32601
    assert LSPErrorCode.InvalidParams.value == -32602
    assert LSPErrorCode.InternalError.value == -32603
    
    print(f"  All enum values verified")
    print(f"  Total codes: {len(LSPErrorCode)}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPErrorCode enum")
    print("=" * 70)


def test_lsp_method_enum():
    """
    Test: LSPMethod enum.
    """
    print("=" * 70)
    print("TEST: LSPMethod Enum")
    print("=" * 70)
    
    assert LSPMethod.INITIALIZE.value == "initialize"
    assert LSPMethod.INITIALIZED.value == "initialized"
    assert LSPMethod.SHUTDOWN.value == "shutdown"
    assert LSPMethod.EXIT.value == "exit"
    assert LSPMethod.TEXT_DOCUMENT_COMPLETION.value == "textDocument/completion"
    assert LSPMethod.TEXT_DOCUMENT_HOVER.value == "textDocument/hover"
    
    print(f"  All enum values verified")
    print(f"  Total methods: {len(LSPMethod)}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPMethod enum")
    print("=" * 70)


def test_position_dataclass():
    """
    Test: Position dataclass.
    """
    print("=" * 70)
    print("TEST: Position Dataclass")
    print("=" * 70)
    
    position = Position(line=1, character=0)
    
    assert position.line == 1, "Line eşleşmeli"
    assert position.character == 0, "Character eşleşmeli"
    
    print(f"  Line: {position.line}")
    print(f"  Character: {position.character}")
    
    print("\n" + "=" * 70)
    print("PASS: Position dataclass")
    print("=" * 70)


def test_range_dataclass():
    """
    Test: Range dataclass.
    """
    print("=" * 70)
    print("TEST: Range Dataclass")
    print("=" * 70)
    
    range_obj = Range(
        start=Position(line=1, character=0),
        end=Position(line=2, character=10)
    )
    
    assert range_obj.start.line == 1, "Start line eşleşmeli"
    assert range_obj.end.line == 2, "End line eşleşmeli"
    
    print(f"  Start line: {range_obj.start.line}")
    print(f"  End line: {range_obj.end.line}")
    
    print("\n" + "=" * 70)
    print("PASS: Range dataclass")
    print("=" * 70)


def test_location_dataclass():
    """
    Test: Location dataclass.
    """
    print("=" * 70)
    print("TEST: Location Dataclass")
    print("=" * 70)
    
    location = Location(
        uri="file:///path/to/file.py",
        range=Range(
            start=Position(line=1, character=0),
            end=Position(line=2, character=10)
        )
    )
    
    assert location.uri == "file:///path/to/file.py", "URI eşleşmeli"
    assert location.range.start.line == 1, "Range eşleşmeli"
    
    print(f"  URI: {location.uri}")
    print(f"  Range: {location.range.start.line}-{location.range.end.line}")
    
    print("\n" + "=" * 70)
    print("PASS: Location dataclass")
    print("=" * 70)


def test_text_document_item_dataclass():
    """
    Test: TextDocumentItem dataclass.
    """
    print("=" * 70)
    print("TEST: TextDocumentItem Dataclass")
    print("=" * 70)
    
    item = TextDocumentItem(
        uri="file:///path/to/file.py",
        languageId="python",
        version=1,
        text="def hello(): pass"
    )
    
    assert item.uri == "file:///path/to/file.py", "URI eşleşmeli"
    assert item.languageId == "python", "Language ID eşleşmeli"
    assert item.version == 1, "Version eşleşmeli"
    
    print(f"  URI: {item.uri}")
    print(f"  Language: {item.languageId}")
    print(f"  Version: {item.version}")
    
    print("\n" + "=" * 70)
    print("PASS: TextDocumentItem dataclass")
    print("=" * 70)


def test_completion_item_dataclass():
    """
    Test: CompletionItem dataclass.
    """
    print("=" * 70)
    print("TEST: CompletionItem Dataclass")
    print("=" * 70)
    
    item = CompletionItem(
        label="hello",
        kind=2,
        detail="def hello()",
        documentation="Hello function"
    )
    
    assert item.label == "hello", "Label eşleşmeli"
    assert item.kind == 2, "Kind eşleşmeli"
    
    print(f"  Label: {item.label}")
    print(f"  Kind: {item.kind}")
    print(f"  Detail: {item.detail}")
    
    print("\n" + "=" * 70)
    print("PASS: CompletionItem dataclass")
    print("=" * 70)


def test_completion_list_dataclass():
    """
    Test: CompletionList dataclass.
    """
    print("=" * 70)
    print("TEST: CompletionList Dataclass")
    print("=" * 70)
    
    items = [
        CompletionItem(label="hello"),
        CompletionItem(label="world")
    ]
    
    completion_list = CompletionList(isIncomplete=False, items=items)
    
    assert completion_list.isIncomplete == False, "isIncomplete eşleşmeli"
    assert len(completion_list.items) == 2, "Items sayısı eşleşmeli"
    
    print(f"  Incomplete: {completion_list.isIncomplete}")
    print(f"  Items: {len(completion_list.items)}")
    
    print("\n" + "=" * 70)
    print("PASS: CompletionList dataclass")
    print("=" * 70)


def test_diagnostic_dataclass():
    """
    Test: Diagnostic dataclass.
    """
    print("=" * 70)
    print("TEST: Diagnostic Dataclass")
    print("=" * 70)
    
    diagnostic = Diagnostic(
        range=Range(
            start=Position(line=1, character=0),
            end=Position(line=1, character=10)
        ),
        severity=1,
        message="Error message"
    )
    
    assert diagnostic.message == "Error message", "Message eşleşmeli"
    assert diagnostic.severity == 1, "Severity eşleşmeli"
    
    print(f"  Message: {diagnostic.message}")
    print(f"  Severity: {diagnostic.severity}")
    
    print("\n" + "=" * 70)
    print("PASS: Diagnostic dataclass")
    print("=" * 70)


def test_lsp_client_config_dataclass():
    """
    Test: LSPClientConfig dataclass.
    """
    print("=" * 70)
    print("TEST: LSPClientConfig Dataclass")
    print("=" * 70)
    
    config = LSPClientConfig(
        server_command=["python"],
        server_args=["-m", "pylsp"],
        root_uri="file:///path/to/project"
    )
    
    assert config.server_command == ["python"], "Command eşleşmeli"
    assert config.root_uri == "file:///path/to/project", "Root URI eşleşmeli"
    
    print(f"  Command: {config.server_command}")
    print(f"  Root URI: {config.root_uri}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPClientConfig dataclass")
    print("=" * 70)


def test_lsp_message_dataclass():
    """
    Test: LSPMessage dataclass.
    """
    print("=" * 70)
    print("TEST: LSPMessage Dataclass")
    print("=" * 70)
    
    message = LSPMessage(
        id=1,
        method="initialize",
        params={"key": "value"}
    )
    
    assert message.id == 1, "ID eşleşmeli"
    assert message.method == "initialize", "Method eşleşmeli"
    
    print(f"  ID: {message.id}")
    print(f"  Method: {message.method}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPMessage dataclass")
    print("=" * 70)


def test_lsp_client_initialization():
    """
    Test: LSP client initialization.
    """
    print("=" * 70)
    print("TEST: LSP Client Initialization")
    print("=" * 70)
    
    config = LSPClientConfig()
    client = LSPClient(config)
    
    assert client.config == config, "Config eşleşmeli"
    assert client.is_initialized == False, "Initialized olmamalı"
    assert client.is_shutdown == False, "Shutdown olmamalı"
    
    print(f"  Initialized: {client.is_initialized}")
    print(f"  Shutdown: {client.is_shutdown}")
    
    print("\n" + "=" * 70)
    print("PASS: LSP client initialization")
    print("=" * 70)


def test_lsp_client_config_update():
    """
    Test: LSP client config update.
    """
    print("=" * 70)
    print("TEST: LSP Client Config Update")
    print("=" * 70)
    
    client = LSPClient()
    
    new_config = LSPClientConfig(
        server_command=["python"],
        root_uri="file:///new/path"
    )
    
    client.update_config(new_config)
    
    assert client.config.server_command == ["python"], "Command güncellenmeli"
    assert client.config.root_uri == "file:///new/path", "Root URI güncellenmeli"
    
    print(f"  Command: {client.config.server_command}")
    print(f"  Root URI: {client.config.root_uri}")
    
    print("\n" + "=" * 70)
    print("PASS: LSP client config update")
    print("=" * 70)


def test_lsp_client_get_config():
    """
    Test: LSP client get config.
    """
    print("=" * 70)
    print("TEST: LSP Client Get Config")
    print("=" * 70)
    
    config = LSPClientConfig(
        server_command=["python"],
        root_uri="file:///path"
    )
    
    client = LSPClient(config)
    retrieved_config = client.get_config()
    
    assert retrieved_config.server_command == ["python"], "Command eşleşmeli"
    
    print(f"  Command: {retrieved_config.server_command}")
    
    print("\n" + "=" * 70)
    print("PASS: LSP client get config")
    print("=" * 70)


def test_lsp_client_diagnostics():
    """
    Test: LSP client diagnostics.
    """
    print("=" * 70)
    print("TEST: LSP Client Diagnostics")
    print("=" * 70)
    
    client = LSPClient()
    
    # Add diagnostics
    diagnostic = Diagnostic(
        range=Range(
            start=Position(line=1, character=0),
            end=Position(line=1, character=10)
        ),
        message="Test error"
    )
    
    client.diagnostics["file:///test.py"] = [diagnostic]
    
    diagnostics = client.get_diagnostics("file:///test.py")
    
    assert len(diagnostics) == 1, "1 diagnostic olmalı"
    assert diagnostics[0].message == "Test error", "Message eşleşmeli"
    
    print(f"  Diagnostics: {len(diagnostics)}")
    print(f"  Message: {diagnostics[0].message}")
    
    print("\n" + "=" * 70)
    print("PASS: LSP client diagnostics")
    print("=" * 70)


def test_text_edit_dataclass():
    """
    Test: TextEdit dataclass.
    """
    print("=" * 70)
    print("TEST: TextEdit Dataclass")
    print("=" * 70)
    
    text_edit = TextEdit(
        range=Range(
            start=Position(line=1, character=0),
            end=Position(line=1, character=10)
        ),
        newText="new text"
    )
    
    assert text_edit.newText == "new text", "New text eşleşmeli"
    assert text_edit.range.start.line == 1, "Range eşleşmeli"
    
    print(f"  New text: {text_edit.newText}")
    print(f"  Range: {text_edit.range.start.line}-{text_edit.range.end.line}")
    
    print("\n" + "=" * 70)
    print("PASS: TextEdit dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_lsp_message_type_enum()
        test2 = test_lsp_error_code_enum()
        test3 = test_lsp_method_enum()
        test4 = test_position_dataclass()
        test5 = test_range_dataclass()
        test6 = test_location_dataclass()
        test7 = test_text_document_item_dataclass()
        test8 = test_completion_item_dataclass()
        test9 = test_completion_list_dataclass()
        test10 = test_diagnostic_dataclass()
        test11 = test_lsp_client_config_dataclass()
        test12 = test_lsp_message_dataclass()
        test13 = test_lsp_client_initialization()
        test14 = test_lsp_client_config_update()
        test15 = test_lsp_client_get_config()
        test16 = test_lsp_client_diagnostics()
        test17 = test_text_edit_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"LSPMessageType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"LSPErrorCode Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"LSPMethod Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"Position Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"Range Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"Location Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"TextDocumentItem Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"CompletionItem Dataclass: {'PASS' if test8 else 'FAIL'}")
        print(f"CompletionList Dataclass: {'PASS' if test9 else 'FAIL'}")
        print(f"Diagnostic Dataclass: {'PASS' if test10 else 'FAIL'}")
        print(f"LSPClientConfig Dataclass: {'PASS' if test11 else 'FAIL'}")
        print(f"LSPMessage Dataclass: {'PASS' if test12 else 'FAIL'}")
        print(f"LSP Client Initialization: {'PASS' if test13 else 'FAIL'}")
        print(f"LSP Client Config Update: {'PASS' if test14 else 'FAIL'}")
        print(f"LSP Client Get Config: {'PASS' if test15 else 'FAIL'}")
        print(f"LSP Client Diagnostics: {'PASS' if test16 else 'FAIL'}")
        print(f"TextEdit Dataclass: {'PASS' if test17 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17])
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
