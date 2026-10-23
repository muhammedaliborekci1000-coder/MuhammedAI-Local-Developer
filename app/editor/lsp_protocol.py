"""
MuhammedAI Local Developer - LSP Protocol
Language Server Protocol implementation and utilities.
"""

import json
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from enum import Enum


class LSPVersion(Enum):
    """LSP protocol version."""
    V3_0 = "3.0"
    V3_1 = "3.1"
    V3_2 = "3.2"
    V3_3 = "3.3"
    V3_4 = "3.4"
    V3_5 = "3.5"
    V3_6 = "3.6"
    V3_7 = "3.7"
    V3_8 = "3.8"
    V3_9 = "3.9"
    V3_10 = "3.10"
    V3_11 = "3.11"
    V3_12 = "3.12"
    V3_13 = "3.13"
    V3_14 = "3.14"
    V3_15 = "3.15"
    V3_16 = "3.16"
    V3_17 = "3.17"
    LATEST = "3.17"


class JSONRPCVersion(Enum):
    """JSON-RPC version."""
    V2_0 = "2.0"


class LSPMessageType(Enum):
    """LSP message type."""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"


class LSPErrorCode(Enum):
    """LSP error codes."""
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603
    SERVER_ERROR_START = -32099
    SERVER_ERROR_END = -32000
    SERVER_NOT_INITIALIZED = -32002
    UNKNOWN_ERROR_CODE = -32001
    REQUEST_CANCELLED = -32800
    CONTENT_MODIFIED = -32801
    REQUEST_FAILED = -32803


class CompletionItemKind(Enum):
    """Completion item kind."""
    TEXT = 1
    METHOD = 2
    FUNCTION = 3
    CONSTRUCTOR = 4
    FIELD = 5
    VARIABLE = 6
    CLASS = 7
    INTERFACE = 8
    MODULE = 9
    PROPERTY = 10
    UNIT = 11
    VALUE = 12
    ENUM = 13
    KEYWORD = 14
    SNIPPET = 15
    COLOR = 16
    FILE = 17
    REFERENCE = 18
    FOLDER = 19
    ENUM_MEMBER = 20
    CONSTANT = 21
    STRUCT = 22
    EVENT = 23
    OPERATOR = 24
    TYPE_PARAMETER = 25


class DiagnosticSeverity(Enum):
    """Diagnostic severity."""
    ERROR = 1
    WARNING = 2
    INFORMATION = 3
    HINT = 4


class TextDocumentSyncKind(Enum):
    """Text document sync kind."""
    NONE = 0
    FULL = 1
    INCREMENTAL = 2


class InsertTextFormat(Enum):
    """Insert text format."""
    PLAIN_TEXT = 1
    SNIPPET = 2


class SymbolKind(Enum):
    """Symbol kind."""
    FILE = 1
    MODULE = 2
    NAMESPACE = 3
    PACKAGE = 4
    CLASS = 5
    METHOD = 6
    PROPERTY = 7
    FIELD = 8
    CONSTRUCTOR = 9
    ENUM = 10
    INTERFACE = 11
    FUNCTION = 12
    VARIABLE = 13
    CONSTANT = 14
    STRING = 15
    NUMBER = 16
    BOOLEAN = 17
    ARRAY = 18
    OBJECT = 19
    KEY = 20
    NULL = 21
    ENUM_MEMBER = 22
    STRUCT = 23
    EVENT = 24
    OPERATOR = 25
    TYPE_PARAMETER = 26


@dataclass
class LSPMessage:
    """LSP message."""
    jsonrpc: str = JSONRPCVersion.V2_0.value
    id: Optional[Union[int, str]] = None
    method: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


@dataclass
class LSPRequest(LSPMessage):
    """LSP request message."""
    method: str
    params: Optional[Dict[str, Any]] = None
    id: Union[int, str] = 0
    jsonrpc: str = JSONRPCVersion.V2_0.value
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


@dataclass
class LSPResponse(LSPMessage):
    """LSP response message."""
    id: Union[int, str]
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    jsonrpc: str = JSONRPCVersion.V2_0.value


@dataclass
class LSPNotification(LSPMessage):
    """LSP notification message."""
    method: str
    params: Optional[Dict[str, Any]] = None
    jsonrpc: str = JSONRPCVersion.V2_0.value
    id: Optional[Union[int, str]] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


@dataclass
class Position:
    """Position in text document."""
    line: int
    character: int


@dataclass
class Range:
    """Range in text document."""
    start: Position
    end: Position


@dataclass
class Location:
    """Location in workspace."""
    uri: str
    range: Range


@dataclass
class TextDocumentItem:
    """Text document item."""
    uri: str
    languageId: str
    version: int
    text: str


@dataclass
class TextDocumentIdentifier:
    """Text document identifier."""
    uri: str


@dataclass
class VersionedTextDocumentIdentifier:
    """Versioned text document identifier."""
    uri: str
    version: int


@dataclass
class CompletionItem:
    """Completion item."""
    label: str
    kind: Optional[int] = None
    detail: Optional[str] = None
    documentation: Optional[str] = None
    sortText: Optional[str] = None
    filterText: Optional[str] = None
    insertText: Optional[str] = None
    insertTextFormat: Optional[int] = None


@dataclass
class CompletionList:
    """Completion list."""
    isIncomplete: bool
    items: List[CompletionItem] = field(default_factory=list)


@dataclass
class Diagnostic:
    """Diagnostic."""
    range: Range
    severity: Optional[int] = None
    code: Optional[Union[str, int]] = None
    source: Optional[str] = None
    message: str = ""
    relatedInformation: Optional[List[Any]] = None


@dataclass
class TextEdit:
    """Text edit."""
    range: Range
    newText: str


@dataclass
class WorkspaceEdit:
    """Workspace edit."""
    changes: Optional[Dict[str, List[TextEdit]]] = None
    documentChanges: Optional[List[Any]] = None


@dataclass
class CodeAction:
    """Code action."""
    title: str
    kind: Optional[str] = None
    diagnostics: Optional[List[Diagnostic]] = None
    edit: Optional[WorkspaceEdit] = None


@dataclass
class SymbolInformation:
    """Symbol information."""
    name: str
    kind: int
    location: Location
    containerName: Optional[str] = None


@dataclass
class DocumentSymbol:
    """Document symbol."""
    name: str
    kind: int
    range: Range
    selectionRange: Range
    detail: Optional[str] = None
    children: Optional[List[Any]] = None


@dataclass
class ParameterInformation:
    """Parameter information."""
    label: Union[str, List[int]]
    documentation: Optional[str] = None


@dataclass
class SignatureInformation:
    """Signature information."""
    label: str
    documentation: Optional[str] = None
    parameters: List[ParameterInformation] = field(default_factory=list)


@dataclass
class SignatureHelp:
    """Signature help."""
    signatures: List[SignatureInformation]
    activeSignature: int = 0
    activeParameter: int = 0


class LSPProtocol:
    """
    LSP Protocol utilities.
    
    Özellikler:
    - Message encoding/decoding
    - Request/response creation
    - Notification creation
    - Error handling
    - JSON-RPC 2.0 compliance
    - LSP version management
    - Message validation
    """
    
    def __init__(self, version: LSPVersion = LSPVersion.LATEST):
        """
        Initialize LSP protocol.
        
        Args:
            version: LSP version
        """
        self.version = version
        self.jsonrpc_version = JSONRPCVersion.V2_0
    
    def encode_message(self, message: LSPMessage) -> bytes:
        """
        Encode LSP message to bytes.
        
        Args:
            message: LSP message
            
        Returns:
            bytes: Encoded message
        """
        content = json.dumps(self._message_to_dict(message), default=str)
        header = f"Content-Length: {len(content)}\r\n\r\n"
        return (header + content).encode('utf-8')
    
    def decode_message(self, data: bytes) -> Optional[LSPMessage]:
        """
        Decode LSP message from bytes.
        
        Args:
            data: Encoded message data
            
        Returns:
            Optional[LSPMessage]: Decoded message
        """
        try:
            # Find Content-Length header
            header_end = data.find(b"\r\n\r\n")
            if header_end == -1:
                return None
            
            header = data[:header_end].decode('utf-8')
            content_length = None
            
            for line in header.split('\r\n'):
                if line.startswith('Content-Length:'):
                    content_length = int(line.split(':')[1].strip())
            
            if content_length is None:
                return None
            
            # Extract content
            message_start = header_end + 4
            message_end = message_start + content_length
            
            if len(data) < message_end:
                return None
            
            content = data[message_start:message_end].decode('utf-8')
            message_dict = json.loads(content)
            
            return self._dict_to_message(message_dict)
        except (json.JSONDecodeError, ValueError):
            return None
    
    def create_request(self, method: str, params: Optional[Dict[str, Any]] = None, request_id: Union[int, str] = 0) -> LSPRequest:
        """
        Create LSP request.
        
        Args:
            method: LSP method
            params: Request parameters
            request_id: Request ID
            
        Returns:
            LSPRequest: Request message
        """
        return LSPRequest(
            jsonrpc=self.jsonrpc_version.value,
            id=request_id,
            method=method,
            params=params
        )
    
    def create_response(self, request_id: Union[int, str], result: Optional[Any] = None, error: Optional[Dict[str, Any]] = None) -> LSPResponse:
        """
        Create LSP response.
        
        Args:
            request_id: Request ID
            result: Response result
            error: Response error
            
        Returns:
            LSPResponse: Response message
        """
        return LSPResponse(
            jsonrpc=self.jsonrpc_version.value,
            id=request_id,
            result=result,
            error=error
        )
    
    def create_notification(self, method: str, params: Optional[Dict[str, Any]] = None) -> LSPNotification:
        """
        Create LSP notification.
        
        Args:
            method: LSP method
            params: Notification parameters
            
        Returns:
            LSPNotification: Notification message
        """
        return LSPNotification(
            jsonrpc=self.jsonrpc_version.value,
            method=method,
            params=params
        )
    
    def create_error(self, code: int, message: str, data: Optional[Any] = None) -> Dict[str, Any]:
        """
        Create LSP error.
        
        Args:
            code: Error code
            message: Error message
            data: Error data
            
        Returns:
            Dict[str, Any]: Error object
        """
        error = {
            "code": code,
            "message": message
        }
        if data is not None:
            error["data"] = data
        return error
    
    def validate_message(self, message: LSPMessage) -> bool:
        """
        Validate LSP message.
        
        Args:
            message: LSP message
            
        Returns:
            bool: Valid status
        """
        # Check jsonrpc version
        if message.jsonrpc != self.jsonrpc_version.value:
            return False
        
        # Check message type
        if isinstance(message, LSPRequest):
            return message.method is not None and message.id is not None
        elif isinstance(message, LSPResponse):
            return message.id is not None
        elif isinstance(message, LSPNotification):
            return message.method is not None
        
        return False
    
    def get_message_type(self, message: LSPMessage) -> Optional[LSPMessageType]:
        """
        Get message type.
        
        Args:
            message: LSP message
            
        Returns:
            Optional[LSPMessageType]: Message type
        """
        if isinstance(message, LSPRequest):
            return LSPMessageType.REQUEST
        elif isinstance(message, LSPResponse):
            return LSPMessageType.RESPONSE
        elif isinstance(message, LSPNotification):
            return LSPMessageType.NOTIFICATION
        return None
    
    def _message_to_dict(self, message: LSPMessage) -> Dict[str, Any]:
        """
        Convert message to dictionary.
        
        Args:
            message: LSP message
            
        Returns:
            Dict[str, Any]: Dictionary representation
        """
        result = {
            "jsonrpc": message.jsonrpc
        }
        
        if message.id is not None:
            result["id"] = message.id
        
        if message.method is not None:
            result["method"] = message.method
        
        if message.params is not None:
            result["params"] = message.params
        
        if message.result is not None:
            result["result"] = message.result
        
        if message.error is not None:
            result["error"] = message.error
        
        return result
    
    def _dict_to_message(self, data: Dict[str, Any]) -> Optional[LSPMessage]:
        """
        Convert dictionary to message.
        
        Args:
            data: Dictionary data
            
        Returns:
            Optional[LSPMessage]: Message object
        """
        jsonrpc = data.get("jsonrpc", self.jsonrpc_version.value)
        message_id = data.get("id")
        method = data.get("method")
        params = data.get("params")
        result = data.get("result")
        error = data.get("error")
        
        # Determine message type
        if message_id is not None and method is not None:
            return LSPRequest(
                jsonrpc=jsonrpc,
                id=message_id,
                method=method,
                params=params
            )
        elif message_id is not None:
            return LSPResponse(
                jsonrpc=jsonrpc,
                id=message_id,
                result=result,
                error=error
            )
        elif method is not None:
            return LSPNotification(
                jsonrpc=jsonrpc,
                method=method,
                params=params
            )
        
        return None
    
    def set_version(self, version: LSPVersion) -> None:
        """
        Set LSP version.
        
        Args:
            version: LSP version
        """
        self.version = version
    
    def get_version(self) -> LSPVersion:
        """
        Get LSP version.
        
        Returns:
            LSPVersion: Current version
        """
        return self.version


if __name__ == "__main__":
    # Basit test
    protocol = LSPProtocol()
    
    # Request oluştur
    request = protocol.create_request("initialize", {"processId": 12345}, 1)
    print(f"Request: {request.method}")
    
    # Encode
    encoded = protocol.encode_message(request)
    print(f"Encoded: {len(encoded)} bytes")
    
    # Decode
    decoded = protocol.decode_message(encoded)
    print(f"Decoded: {decoded.method if decoded else None}")
    
    # Response oluştur
    response = protocol.create_response(1, {"capabilities": {}})
    print(f"Response: {response.result}")
    
    # Notification oluştur
    notification = protocol.create_notification("initialized", {})
    print(f"Notification: {notification.method}")
