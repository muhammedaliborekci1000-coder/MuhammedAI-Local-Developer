"""
MuhammedAI Local Developer - LSP Client
Language Server Protocol client for code editor.
"""

import asyncio
import json
import os
import subprocess
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from enum import Enum


class LSPMessageType(Enum):
    """LSP message type."""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"


class LSPErrorCode(Enum):
    """LSP error codes."""
    ParseError = -32700
    InvalidRequest = -32600
    MethodNotFound = -32601
    InvalidParams = -32602
    InternalError = -32603
    ServerNotInitialized = -32002
    UnknownErrorCode = -32001
    RequestCancelled = -32800
    ContentModified = -32801


class LSPMethod(Enum):
    """LSP methods."""
    INITIALIZE = "initialize"
    INITIALIZED = "initialized"
    SHUTDOWN = "shutdown"
    EXIT = "exit"
    TEXT_DOCUMENT_DID_OPEN = "textDocument/didOpen"
    TEXT_DOCUMENT_DID_CHANGE = "textDocument/didChange"
    TEXT_DOCUMENT_DID_CLOSE = "textDocument/didClose"
    TEXT_DOCUMENT_DID_SAVE = "textDocument/didSave"
    TEXT_DOCUMENT_COMPLETION = "textDocument/completion"
    TEXT_DOCUMENT_HOVER = "textDocument/hover"
    TEXT_DOCUMENT_DEFINITION = "textDocument/definition"
    TEXT_DOCUMENT_REFERENCES = "textDocument/references"
    TEXT_DOCUMENT_DOCUMENT_SYMBOL = "textDocument/documentSymbol"
    TEXT_DOCUMENT_FORMATTING = "textDocument/formatting"
    TEXT_DOCUMENT_CODE_ACTION = "textDocument/codeAction"
    TEXT_DOCUMENT_RENAME = "textDocument/rename"
    TEXT_DOCUMENT_SIGNATURE_HELP = "textDocument/signatureHelp"
    WORKSPACE_SYMBOL = "workspace/symbol"


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
class PublishDiagnosticsParams:
    """Publish diagnostics parameters."""
    uri: str
    diagnostics: List[Diagnostic] = field(default_factory=list)


@dataclass
class LSPClientConfig:
    """LSP client configuration."""
    server_command: List[str] = field(default_factory=list)
    server_args: List[str] = field(default_factory=list)
    root_uri: str = ""
    initialization_options: Dict[str, Any] = field(default_factory=dict)
    capabilities: Dict[str, Any] = field(default_factory=dict)
    trace: str = "off"


@dataclass
class LSPMessage:
    """LSP message."""
    jsonrpc: str = "2.0"
    id: Optional[Union[int, str]] = None
    method: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


class LSPClient:
    """
    LSP Client implementation.
    
    Özellikler:
    - LSP Protocol implementation
    - Language server communication
    - Auto-completion
    - Diagnostics
    - Hover information
    - Go to definition
    - Find references
    - Document formatting
    - Document symbols
    - Code actions
    - Signature help
    - Rename symbol
    - Workspace symbols
    - Text document synchronization
    - Configuration management
    - Error handling
    """
    
    def __init__(self, config: Optional[LSPClientConfig] = None):
        """
        Initialize LSP client.
        
        Args:
            config: LSP client configuration
        """
        self.config = config or LSPClientConfig()
        self.server_process: Optional[subprocess.Popen] = None
        self.request_id: int = 0
        self.pending_requests: Dict[int, asyncio.Future] = {}
        self.diagnostics: Dict[str, List[Diagnostic]] = {}
        self.is_initialized: bool = False
        self.is_shutdown: bool = False
        self.documents: Dict[str, TextDocumentItem] = {}
    
    async def start_server(self) -> bool:
        """
        Start LSP server.
        
        Returns:
            bool: Success status
        """
        try:
            if not self.config.server_command:
                return False
            
            cmd = self.config.server_command + self.config.server_args
            self.server_process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=0
            )
            
            # Start message handler
            asyncio.create_task(self._read_messages())
            
            return True
        except Exception as e:
            print(f"Error starting server: {e}")
            return False
    
    async def initialize(self) -> Dict[str, Any]:
        """
        Initialize LSP server.
        
        Returns:
            Dict[str, Any]: Initialize result
        """
        params = {
            "processId": os.getpid(),
            "rootUri": self.config.root_uri,
            "initializationOptions": self.config.initialization_options,
            "capabilities": self.config.capabilities,
            "trace": self.config.trace
        }
        
        result = await self._send_request(LSPMethod.INITIALIZE.value, params)
        
        if result and not result.get("error"):
            self.is_initialized = True
            # Send initialized notification
            await self._send_notification(LSPMethod.INITIALIZED.value, {})
        
        return result or {}
    
    async def shutdown(self) -> Dict[str, Any]:
        """
        Shutdown LSP server.
        
        Returns:
            Dict[str, Any]: Shutdown result
        """
        result = await self._send_request(LSPMethod.SHUTDOWN.value, {})
        
        if result and not result.get("error"):
            self.is_shutdown = True
        
        return result or {}
    
    async def exit(self) -> None:
        """Exit LSP server."""
        await self._send_notification(LSPMethod.EXIT.value, {})
        
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            self.server_process = None
    
    async def open_document(self, uri: str, language_id: str, text: str) -> bool:
        """
        Open text document.
        
        Args:
            uri: Document URI
            language_id: Language identifier
            text: Document text
            
        Returns:
            bool: Success status
        """
        try:
            params = {
                "textDocument": {
                    "uri": uri,
                    "languageId": language_id,
                    "version": 1,
                    "text": text
                }
            }
            
            await self._send_notification(LSPMethod.TEXT_DOCUMENT_DID_OPEN.value, params)
            
            self.documents[uri] = TextDocumentItem(
                uri=uri,
                languageId=language_id,
                version=1,
                text=text
            )
            
            return True
        except Exception as e:
            print(f"Error opening document: {e}")
            return False
    
    async def change_document(self, uri: str, text: str) -> bool:
        """
        Change text document.
        
        Args:
            uri: Document URI
            text: New document text
            
        Returns:
            bool: Success status
        """
        try:
            if uri not in self.documents:
                return False
            
            doc = self.documents[uri]
            doc.version += 1
            doc.text = text
            
            params = {
                "textDocument": {
                    "uri": uri,
                    "version": doc.version
                },
                "contentChanges": [{"text": text}]
            }
            
            await self._send_notification(LSPMethod.TEXT_DOCUMENT_DID_CHANGE.value, params)
            
            return True
        except Exception as e:
            print(f"Error changing document: {e}")
            return False
    
    async def close_document(self, uri: str) -> bool:
        """
        Close text document.
        
        Args:
            uri: Document URI
            
        Returns:
            bool: Success status
        """
        try:
            params = {
                "textDocument": {"uri": uri}
            }
            
            await self._send_notification(LSPMethod.TEXT_DOCUMENT_DID_CLOSE.value, params)
            
            if uri in self.documents:
                del self.documents[uri]
            
            return True
        except Exception as e:
            print(f"Error closing document: {e}")
            return False
    
    async def get_completion(self, uri: str, line: int, character: int) -> Optional[CompletionList]:
        """
        Get completion items.
        
        Args:
            uri: Document URI
            line: Line number
            character: Character offset
            
        Returns:
            Optional[CompletionList]: Completion list
        """
        try:
            params = {
                "textDocument": {"uri": uri},
                "position": {"line": line, "character": character}
            }
            
            result = await self._send_request(LSPMethod.TEXT_DOCUMENT_COMPLETION.value, params)
            
            if result and not result.get("error"):
                if "items" in result:
                    items = [CompletionItem(**item) for item in result["items"]]
                    return CompletionList(
                        isIncomplete=result.get("isIncomplete", False),
                        items=items
                    )
                elif isinstance(result, list):
                    items = [CompletionItem(**item) for item in result]
                    return CompletionList(isIncomplete=False, items=items)
            
            return None
        except Exception as e:
            print(f"Error getting completion: {e}")
            return None
    
    async def get_hover(self, uri: str, line: int, character: int) -> Optional[str]:
        """
        Get hover information.
        
        Args:
            uri: Document URI
            line: Line number
            character: Character offset
            
        Returns:
            Optional[str]: Hover text
        """
        try:
            params = {
                "textDocument": {"uri": uri},
                "position": {"line": line, "character": character}
            }
            
            result = await self._send_request(LSPMethod.TEXT_DOCUMENT_HOVER.value, params)
            
            if result and not result.get("error"):
                contents = result.get("contents")
                if isinstance(contents, str):
                    return contents
                elif isinstance(contents, list) and len(contents) > 0:
                    return str(contents[0])
                elif isinstance(contents, dict):
                    return contents.get("value", str(contents))
            
            return None
        except Exception as e:
            print(f"Error getting hover: {e}")
            return None
    
    async def go_to_definition(self, uri: str, line: int, character: int) -> Optional[List[Location]]:
        """
        Go to definition.
        
        Args:
            uri: Document URI
            line: Line number
            character: Character offset
            
        Returns:
            Optional[List[Location]]: Locations
        """
        try:
            params = {
                "textDocument": {"uri": uri},
                "position": {"line": line, "character": character}
            }
            
            result = await self._send_request(LSPMethod.TEXT_DOCUMENT_DEFINITION.value, params)
            
            if result and not result.get("error"):
                if isinstance(result, list):
                    return [Location(**loc) for loc in result]
                elif isinstance(result, dict):
                    return [Location(**result)]
            
            return None
        except Exception as e:
            print(f"Error going to definition: {e}")
            return None
    
    async def find_references(self, uri: str, line: int, character: int) -> Optional[List[Location]]:
        """
        Find references.
        
        Args:
            uri: Document URI
            line: Line number
            character: Character offset
            
        Returns:
            Optional[List[Location]]: Locations
        """
        try:
            params = {
                "textDocument": {"uri": uri},
                "position": {"line": line, "character": character},
                "context": {"includeDeclaration": True}
            }
            
            result = await self._send_request(LSPMethod.TEXT_DOCUMENT_REFERENCES.value, params)
            
            if result and not result.get("error") and isinstance(result, list):
                return [Location(**loc) for loc in result]
            
            return None
        except Exception as e:
            print(f"Error finding references: {e}")
            return None
    
    async def format_document(self, uri: str) -> Optional[List[TextEdit]]:
        """
        Format document.
        
        Args:
            uri: Document URI
            
        Returns:
            Optional[List[TextEdit]]: Text edits
        """
        try:
            params = {
                "textDocument": {"uri": uri},
                "options": {"tabSize": 4, "insertSpaces": True}
            }
            
            result = await self._send_request(LSPMethod.TEXT_DOCUMENT_FORMATTING.value, params)
            
            if result and not result.get("error") and isinstance(result, list):
                return result
            
            return None
        except Exception as e:
            print(f"Error formatting document: {e}")
            return None
    
    async def get_document_symbols(self, uri: str) -> Optional[List[Any]]:
        """
        Get document symbols.
        
        Args:
            uri: Document URI
            
        Returns:
            Optional[List[Any]]: Symbols
        """
        try:
            params = {
                "textDocument": {"uri": uri}
            }
            
            result = await self._send_request(LSPMethod.TEXT_DOCUMENT_DOCUMENT_SYMBOL.value, params)
            
            if result and not result.get("error") and isinstance(result, list):
                return result
            
            return None
        except Exception as e:
            print(f"Error getting document symbols: {e}")
            return None
    
    async def get_workspace_symbols(self, query: str) -> Optional[List[Any]]:
        """
        Get workspace symbols.
        
        Args:
            query: Search query
            
        Returns:
            Optional[List[Any]]: Symbols
        """
        try:
            params = {"query": query}
            
            result = await self._send_request(LSPMethod.WORKSPACE_SYMBOL.value, params)
            
            if result and not result.get("error") and isinstance(result, list):
                return result
            
            return None
        except Exception as e:
            print(f"Error getting workspace symbols: {e}")
            return None
    
    async def get_code_actions(self, uri: str, range: Range) -> Optional[List[Any]]:
        """
        Get code actions.
        
        Args:
            uri: Document URI
            range: Range
            
        Returns:
            Optional[List[Any]]: Code actions
        """
        try:
            params = {
                "textDocument": {"uri": uri},
                "range": {
                    "start": {"line": range.start.line, "character": range.start.character},
                    "end": {"line": range.end.line, "character": range.end.character}
                }
            }
            
            result = await self._send_request(LSPMethod.TEXT_DOCUMENT_CODE_ACTION.value, params)
            
            if result and not result.get("error") and isinstance(result, list):
                return result
            
            return None
        except Exception as e:
            print(f"Error getting code actions: {e}")
            return None
    
    async def get_signature_help(self, uri: str, line: int, character: int) -> Optional[Any]:
        """
        Get signature help.
        
        Args:
            uri: Document URI
            line: Line number
            character: Character offset
            
        Returns:
            Optional[Any]: Signature help
        """
        try:
            params = {
                "textDocument": {"uri": uri},
                "position": {"line": line, "character": character}
            }
            
            result = await self._send_request(LSPMethod.TEXT_DOCUMENT_SIGNATURE_HELP.value, params)
            
            if result and not result.get("error"):
                return result
            
            return None
        except Exception as e:
            print(f"Error getting signature help: {e}")
            return None
    
    async def rename_symbol(self, uri: str, line: int, character: int, new_name: str) -> Optional[Dict[str, Any]]:
        """
        Rename symbol.
        
        Args:
            uri: Document URI
            line: Line number
            character: Character offset
            new_name: New symbol name
            
        Returns:
            Optional[Dict[str, Any]]: Workspace edit
        """
        try:
            params = {
                "textDocument": {"uri": uri},
                "position": {"line": line, "character": character},
                "newName": new_name
            }
            
            result = await self._send_request(LSPMethod.TEXT_DOCUMENT_RENAME.value, params)
            
            if result and not result.get("error"):
                return result
            
            return None
        except Exception as e:
            print(f"Error renaming symbol: {e}")
            return None
    
    def get_diagnostics(self, uri: str) -> List[Diagnostic]:
        """
        Get diagnostics for document.
        
        Args:
            uri: Document URI
            
        Returns:
            List[Diagnostic]: Diagnostics
        """
        return self.diagnostics.get(uri, [])
    
    def update_config(self, config: LSPClientConfig) -> None:
        """
        Update LSP client configuration.
        
        Args:
            config: New configuration
        """
        self.config = config
    
    def get_config(self) -> LSPClientConfig:
        """
        Get LSP client configuration.
        
        Returns:
            LSPClientConfig: Configuration
        """
        return self.config
    
    async def _send_request(self, method: str, params: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Send LSP request.
        
        Args:
            method: LSP method
            params: Request parameters
            
        Returns:
            Optional[Dict[str, Any]]: Response
        """
        if not self.server_process:
            return None
        
        self.request_id += 1
        request_id = self.request_id
        
        message = LSPMessage(
            id=request_id,
            method=method,
            params=params
        )
        
        future = asyncio.Future()
        self.pending_requests[request_id] = future
        
        await self._write_message(message)
        
        try:
            return await asyncio.wait_for(future, timeout=30.0)
        except asyncio.TimeoutError:
            self.pending_requests.pop(request_id, None)
            return None
    
    async def _send_notification(self, method: str, params: Optional[Dict[str, Any]]) -> None:
        """
        Send LSP notification.
        
        Args:
            method: LSP method
            params: Notification parameters
        """
        if not self.server_process:
            return
        
        message = LSPMessage(
            method=method,
            params=params
        )
        
        await self._write_message(message)
    
    async def _write_message(self, message: LSPMessage) -> None:
        """
        Write message to server.
        
        Args:
            message: LSP message
        """
        if not self.server_process:
            return
        
        content = json.dumps({
            "jsonrpc": message.jsonrpc,
            "id": message.id,
            "method": message.method,
            "params": message.params
        }, default=str)
        
        header = f"Content-Length: {len(content)}\r\n\r\n"
        
        self.server_process.stdin.write((header + content).encode('utf-8'))
        self.server_process.stdin.flush()
    
    async def _read_messages(self) -> None:
        """Read messages from server."""
        if not self.server_process:
            return
        
        buffer = b""
        
        while self.server_process and self.server_process.poll() is None:
            try:
                chunk = self.server_process.stdout.read(4096)
                if not chunk:
                    break
                
                buffer += chunk
                
                # Process messages
                while True:
                    # Find Content-Length header
                    header_end = buffer.find(b"\r\n\r\n")
                    if header_end == -1:
                        break
                    
                    header = buffer[:header_end].decode('utf-8')
                    content_length = None
                    
                    for line in header.split('\r\n'):
                        if line.startswith('Content-Length:'):
                            content_length = int(line.split(':')[1].strip())
                    
                    if content_length is None:
                        break
                    
                    # Check if we have the full message
                    message_start = header_end + 4
                    message_end = message_start + content_length
                    
                    if len(buffer) < message_end:
                        break
                    
                    # Extract message
                    message_content = buffer[message_start:message_end].decode('utf-8')
                    buffer = buffer[message_end:]
                    
                    # Parse message
                    try:
                        message = json.loads(message_content)
                        await self._handle_message(message)
                    except json.JSONDecodeError:
                        pass
            except Exception as e:
                print(f"Error reading messages: {e}")
                break
    
    async def _handle_message(self, message: Dict[str, Any]) -> None:
        """
        Handle incoming message.
        
        Args:
            message: LSP message
        """
        # Handle response
        if "id" in message and message["id"] in self.pending_requests:
            future = self.pending_requests.pop(message["id"])
            future.set_result(message)
        
        # Handle notification
        elif "method" in message:
            method = message["method"]
            params = message.get("params", {})
            
            if method == "textDocument/publishDiagnostics":
                uri = params.get("uri", "")
                diagnostics = params.get("diagnostics", [])
                self.diagnostics[uri] = [Diagnostic(**diag) for diag in diagnostics]


@dataclass
class TextEdit:
    """Text edit."""
    range: Range
    newText: str


if __name__ == "__main__":
    # Basit test
    async def test_lsp_client():
        config = LSPClientConfig(
            server_command=["python"],
            server_args=["-m", "pylsp"],
            root_uri="file:///path/to/project"
        )
        
        client = LSPClient(config)
        
        # Start server
        if await client.start_server():
            print("Server started")
            
            # Initialize
            result = await client.initialize()
            print(f"Initialized: {result}")
            
            # Shutdown
            await client.shutdown()
            await client.exit()
            print("Server stopped")
    
    asyncio.run(test_lsp_client())
