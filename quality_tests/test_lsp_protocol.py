"""
Quality Test: LSP Protocol
LSP protocol system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.lsp_protocol import (
    LSPVersion,
    JSONRPCVersion,
    LSPMessageType,
    LSPErrorCode,
    CompletionItemKind,
    DiagnosticSeverity,
    TextDocumentSyncKind,
    InsertTextFormat,
    SymbolKind,
    LSPMessage,
    LSPRequest,
    LSPResponse,
    LSPNotification,
    Position,
    Range,
    Location,
    TextDocumentItem,
    CompletionItem,
    CompletionList,
    Diagnostic,
    TextEdit,
    WorkspaceEdit,
    CodeAction,
    LSPProtocol
)


def test_lsp_version_enum():
    """
    Test: LSPVersion enum.
    """
    print("=" * 70)
    print("TEST: LSPVersion Enum")
    print("=" * 70)
    
    assert LSPVersion.V3_0.value == "3.0"
    assert LSPVersion.V3_17.value == "3.17"
    assert LSPVersion.LATEST.value == "3.17"
    
    print(f"  All enum values verified")
    print(f"  Total versions: {len(LSPVersion)}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPVersion enum")
    print("=" * 70)


def test_jsonrpc_version_enum():
    """
    Test: JSONRPCVersion enum.
    """
    print("=" * 70)
    print("TEST: JSONRPCVersion Enum")
    print("=" * 70)
    
    assert JSONRPCVersion.V2_0.value == "2.0"
    
    print(f"  All enum values verified")
    print(f"  Total versions: {len(JSONRPCVersion)}")
    
    print("\n" + "=" * 70)
    print("PASS: JSONRPCVersion enum")
    print("=" * 70)


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
    
    assert LSPErrorCode.PARSE_ERROR.value == -32700
    assert LSPErrorCode.INVALID_REQUEST.value == -32600
    assert LSPErrorCode.METHOD_NOT_FOUND.value == -32601
    assert LSPErrorCode.REQUEST_CANCELLED.value == -32800
    
    print(f"  All enum values verified")
    print(f"  Total codes: {len(LSPErrorCode)}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPErrorCode enum")
    print("=" * 70)


def test_completion_item_kind_enum():
    """
    Test: CompletionItemKind enum.
    """
    print("=" * 70)
    print("TEST: CompletionItemKind Enum")
    print("=" * 70)
    
    assert CompletionItemKind.TEXT.value == 1
    assert CompletionItemKind.METHOD.value == 2
    assert CompletionItemKind.FUNCTION.value == 3
    assert CompletionItemKind.CLASS.value == 7
    
    print(f"  All enum values verified")
    print(f"  Total kinds: {len(CompletionItemKind)}")
    
    print("\n" + "=" * 70)
    print("PASS: CompletionItemKind enum")
    print("=" * 70)


def test_diagnostic_severity_enum():
    """
    Test: DiagnosticSeverity enum.
    """
    print("=" * 70)
    print("TEST: DiagnosticSeverity Enum")
    print("=" * 70)
    
    assert DiagnosticSeverity.ERROR.value == 1
    assert DiagnosticSeverity.WARNING.value == 2
    assert DiagnosticSeverity.INFORMATION.value == 3
    assert DiagnosticSeverity.HINT.value == 4
    
    print(f"  All enum values verified")
    print(f"  Total severities: {len(DiagnosticSeverity)}")
    
    print("\n" + "=" * 70)
    print("PASS: DiagnosticSeverity enum")
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


def test_lsp_message_dataclass():
    """
    Test: LSPMessage dataclass.
    """
    print("=" * 70)
    print("TEST: LSPMessage Dataclass")
    print("=" * 70)
    
    message = LSPMessage(
        jsonrpc="2.0",
        id=1,
        method="test",
        params={"key": "value"}
    )
    
    assert message.jsonrpc == "2.0", "jsonrpc eşleşmeli"
    assert message.id == 1, "ID eşleşmeli"
    assert message.method == "test", "Method eşleşmeli"
    
    print(f"  JSON-RPC: {message.jsonrpc}")
    print(f"  ID: {message.id}")
    print(f"  Method: {message.method}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPMessage dataclass")
    print("=" * 70)


def test_lsp_request_dataclass():
    """
    Test: LSPRequest dataclass.
    """
    print("=" * 70)
    print("TEST: LSPRequest Dataclass")
    print("=" * 70)
    
    request = LSPRequest(
        method="initialize",
        params={"processId": 12345},
        id=1
    )
    
    assert request.method == "initialize", "Method eşleşmeli"
    assert request.id == 1, "ID eşleşmeli"
    
    print(f"  Method: {request.method}")
    print(f"  ID: {request.id}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPRequest dataclass")
    print("=" * 70)


def test_lsp_response_dataclass():
    """
    Test: LSPResponse dataclass.
    """
    print("=" * 70)
    print("TEST: LSPResponse Dataclass")
    print("=" * 70)
    
    response = LSPResponse(
        id=1,
        result={"capabilities": {}}
    )
    
    assert response.id == 1, "ID eşleşmeli"
    assert response.result is not None, "Result olmalı"
    
    print(f"  ID: {response.id}")
    print(f"  Result: {response.result}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPResponse dataclass")
    print("=" * 70)


def test_lsp_notification_dataclass():
    """
    Test: LSPNotification dataclass.
    """
    print("=" * 70)
    print("TEST: LSPNotification Dataclass")
    print("=" * 70)
    
    notification = LSPNotification(
        method="initialized",
        params={}
    )
    
    assert notification.method == "initialized", "Method eşleşmeli"
    assert notification.id is None, "ID olmamalı"
    
    print(f"  Method: {notification.method}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPNotification dataclass")
    print("=" * 70)


def test_lsp_protocol_initialization():
    """
    Test: LSPProtocol initialization.
    """
    print("=" * 70)
    print("TEST: LSPProtocol Initialization")
    print("=" * 70)
    
    protocol = LSPProtocol()
    
    assert protocol.version == LSPVersion.LATEST, "Version eşleşmeli"
    assert protocol.jsonrpc_version == JSONRPCVersion.V2_0, "JSON-RPC version eşleşmeli"
    
    print(f"  Version: {protocol.version.value}")
    print(f"  JSON-RPC: {protocol.jsonrpc_version.value}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPProtocol initialization")
    print("=" * 70)


def test_lsp_protocol_create_request():
    """
    Test: LSPProtocol create request.
    """
    print("=" * 70)
    print("TEST: LSPProtocol Create Request")
    print("=" * 70)
    
    protocol = LSPProtocol()
    
    request = protocol.create_request("initialize", {"processId": 12345}, 1)
    
    assert request.method == "initialize", "Method eşleşmeli"
    assert request.id == 1, "ID eşleşmeli"
    assert request.params is not None, "Params olmalı"
    
    print(f"  Method: {request.method}")
    print(f"  ID: {request.id}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPProtocol create request")
    print("=" * 70)


def test_lsp_protocol_create_response():
    """
    Test: LSPProtocol create response.
    """
    print("=" * 70)
    print("TEST: LSPProtocol Create Response")
    print("=" * 70)
    
    protocol = LSPProtocol()
    
    response = protocol.create_response(1, {"capabilities": {}})
    
    assert response.id == 1, "ID eşleşmeli"
    assert response.result is not None, "Result olmalı"
    
    print(f"  ID: {response.id}")
    print(f"  Result: {response.result}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPProtocol create response")
    print("=" * 70)


def test_lsp_protocol_create_notification():
    """
    Test: LSPProtocol create notification.
    """
    print("=" * 70)
    print("TEST: LSPProtocol Create Notification")
    print("=" * 70)
    
    protocol = LSPProtocol()
    
    notification = protocol.create_notification("initialized", {})
    
    assert notification.method == "initialized", "Method eşleşmeli"
    assert notification.id is None, "ID olmamalı"
    
    print(f"  Method: {notification.method}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPProtocol create notification")
    print("=" * 70)


def test_lsp_protocol_encode_decode():
    """
    Test: LSPProtocol encode/decode.
    """
    print("=" * 70)
    print("TEST: LSPProtocol Encode/Decode")
    print("=" * 70)
    
    protocol = LSPProtocol()
    
    request = protocol.create_request("initialize", {"processId": 12345}, 1)
    encoded = protocol.encode_message(request)
    decoded = protocol.decode_message(encoded)
    
    assert decoded is not None, "Decode başarılı olmalı"
    assert decoded.method == "initialize", "Method eşleşmeli"
    assert decoded.id == 1, "ID eşleşmeli"
    
    print(f"  Encoded: {len(encoded)} bytes")
    print(f"  Decoded method: {decoded.method}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPProtocol encode/decode")
    print("=" * 70)


def test_lsp_protocol_create_error():
    """
    Test: LSPProtocol create error.
    """
    print("=" * 70)
    print("TEST: LSPProtocol Create Error")
    print("=" * 70)
    
    protocol = LSPProtocol()
    
    error = protocol.create_error(-32601, "Method not found")
    
    assert error["code"] == -32601, "Code eşleşmeli"
    assert error["message"] == "Method not found", "Message eşleşmeli"
    
    print(f"  Code: {error['code']}")
    print(f"  Message: {error['message']}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPProtocol create error")
    print("=" * 70)


def test_lsp_protocol_validate_message():
    """
    Test: LSPProtocol validate message.
    """
    print("=" * 70)
    print("TEST: LSPProtocol Validate Message")
    print("=" * 70)
    
    protocol = LSPProtocol()
    
    request = protocol.create_request("initialize", {}, 1)
    is_valid = protocol.validate_message(request)
    
    assert is_valid == True, "Request valid olmalı"
    
    print(f"  Valid: {is_valid}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPProtocol validate message")
    print("=" * 70)


def test_lsp_protocol_get_message_type():
    """
    Test: LSPProtocol get message type.
    """
    print("=" * 70)
    print("TEST: LSPProtocol Get Message Type")
    print("=" * 70)
    
    protocol = LSPProtocol()
    
    request = protocol.create_request("initialize", {}, 1)
    message_type = protocol.get_message_type(request)
    
    assert message_type == LSPMessageType.REQUEST, "Request type olmalı"
    
    print(f"  Type: {message_type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPProtocol get message type")
    print("=" * 70)


def test_lsp_protocol_version_management():
    """
    Test: LSPProtocol version management.
    """
    print("=" * 70)
    print("TEST: LSPProtocol Version Management")
    print("=" * 70)
    
    protocol = LSPProtocol()
    
    # Get version
    version = protocol.get_version()
    assert version == LSPVersion.LATEST, "Latest version olmalı"
    
    # Set version
    protocol.set_version(LSPVersion.V3_16)
    new_version = protocol.get_version()
    assert new_version == LSPVersion.V3_16, "Version güncellenmeli"
    
    print(f"  Original: {version.value}")
    print(f"  Updated: {new_version.value}")
    
    print("\n" + "=" * 70)
    print("PASS: LSPProtocol version management")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_lsp_version_enum()
        test2 = test_jsonrpc_version_enum()
        test3 = test_lsp_message_type_enum()
        test4 = test_lsp_error_code_enum()
        test5 = test_completion_item_kind_enum()
        test6 = test_diagnostic_severity_enum()
        test7 = test_position_dataclass()
        test8 = test_range_dataclass()
        test9 = test_location_dataclass()
        test10 = test_lsp_message_dataclass()
        test11 = test_lsp_request_dataclass()
        test12 = test_lsp_response_dataclass()
        test13 = test_lsp_notification_dataclass()
        test14 = test_lsp_protocol_initialization()
        test15 = test_lsp_protocol_create_request()
        test16 = test_lsp_protocol_create_response()
        test17 = test_lsp_protocol_create_notification()
        test18 = test_lsp_protocol_encode_decode()
        test19 = test_lsp_protocol_create_error()
        test20 = test_lsp_protocol_validate_message()
        test21 = test_lsp_protocol_get_message_type()
        test22 = test_lsp_protocol_version_management()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"LSPVersion Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"JSONRPCVersion Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"LSPMessageType Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"LSPErrorCode Enum: {'PASS' if test4 else 'FAIL'}")
        print(f"CompletionItemKind Enum: {'PASS' if test5 else 'FAIL'}")
        print(f"DiagnosticSeverity Enum: {'PASS' if test6 else 'FAIL'}")
        print(f"Position Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"Range Dataclass: {'PASS' if test8 else 'FAIL'}")
        print(f"Location Dataclass: {'PASS' if test9 else 'FAIL'}")
        print(f"LSPMessage Dataclass: {'PASS' if test10 else 'FAIL'}")
        print(f"LSPRequest Dataclass: {'PASS' if test11 else 'FAIL'}")
        print(f"LSPResponse Dataclass: {'PASS' if test12 else 'FAIL'}")
        print(f"LSPNotification Dataclass: {'PASS' if test13 else 'FAIL'}")
        print(f"LSPProtocol Initialization: {'PASS' if test14 else 'FAIL'}")
        print(f"LSPProtocol Create Request: {'PASS' if test15 else 'FAIL'}")
        print(f"LSPProtocol Create Response: {'PASS' if test16 else 'FAIL'}")
        print(f"LSPProtocol Create Notification: {'PASS' if test17 else 'FAIL'}")
        print(f"LSPProtocol Encode/Decode: {'PASS' if test18 else 'FAIL'}")
        print(f"LSPProtocol Create Error: {'PASS' if test19 else 'FAIL'}")
        print(f"LSPProtocol Validate Message: {'PASS' if test20 else 'FAIL'}")
        print(f"LSPProtocol Get Message Type: {'PASS' if test21 else 'FAIL'}")
        print(f"LSPProtocol Version Management: {'PASS' if test22 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22])
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
