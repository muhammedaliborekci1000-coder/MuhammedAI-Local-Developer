"""
MuhammedAI Local Developer - LSP Manager
LSP client lifecycle management using direct subprocess communication.
"""

import os
import json
import subprocess
import threading
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class LSPManagerConfig:
    """LSP manager configuration."""
    project_root: str
    pylsp_path: Optional[str] = None


class LSPManager:
    """
    LSP manager for handling LSP client lifecycle using direct JSON-RPC.
    
    Özellikler:
    - LSP client başlatma ve yönetme
    - pylsp entegrasyonu
    - Document tracking
    - Auto-restart on error
    - Resource cleanup
    """
    
    def __init__(self, config: LSPManagerConfig):
        """
        Initialize LSP manager.
        
        Args:
            config: LSP manager configuration
        """
        self.config = config
        self.process = None
        self.is_running: bool = False
        self.documents: Dict[str, str] = {}  # uri -> text
        self.request_id = 0
        self.responses = {}
        self.lock = threading.Lock()
    
    def _send_message(self, method: str, params: Any, is_notification: bool = False) -> Optional[Any]:
        """Send JSON-RPC message."""
        try:
            self.request_id += 1
            msg_id = self.request_id if not is_notification else None
            
            message = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "method": method,
                "params": params
            }
            
            content = json.dumps(message)
            header = f"Content-Length: {len(content)}\r\n\r\n"
            
            self.process.stdin.write((header + content).encode('utf-8'))
            self.process.stdin.flush()
            
            if is_notification:
                return None
            
            # Read response
            response = self._read_response()
            return response
        except Exception as e:
            print(f"Send message error: {e}")
            return None
    
    def _read_response(self) -> Optional[Dict]:
        """Read JSON-RPC response."""
        try:
            # Read Content-Length header
            header = b""
            while b"\r\n\r\n" not in header:
                char = self.process.stdout.read(1)
                if not char:
                    return None
                header += char
            
            # Parse Content-Length
            header_str = header.decode('utf-8')
            length = None
            for line in header_str.split('\r\n'):
                if line.startswith('Content-Length:'):
                    length = int(line.split(':')[1].strip())
                    break
            
            if length is None:
                return None
            
            # Read content
            content = self.process.stdout.read(length)
            response = json.loads(content.decode('utf-8'))
            
            return response
        except Exception as e:
            print(f"Read response error: {e}")
            return None
    
    def start(self) -> bool:
        """
        LSP client'ı başlat (sync).
        
        Returns:
            bool: Success status
        """
        try:
            import sys
            
            # pylsp'ı subprocess olarak başlat
            cmd = [str(sys.executable), "-m", "pylsp"]
            
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=0
            )
            
            self.is_running = True
            
            # Initialize
            self._initialize()
            
            return True
            
        except Exception as e:
            print(f"LSP start error: {e}")
            return False
    
    def _initialize(self) -> None:
        """LSP server'ı initialize et (sync)."""
        try:
            params = {
                "processId": os.getpid(),
                "rootUri": f"file://{self.config.project_root}",
                "capabilities": {
                    "textDocument": {
                        "completion": {
                            "completionItem": {
                                "snippetSupport": True
                            }
                        },
                        "hover": {
                            "contentFormat": ["markdown", "plaintext"]
                        }
                    }
                }
            }
            
            result = self._send_message("initialize", params)
            print(f"Initialize result: {result}")
            
            # initialized notification
            self._send_message("initialized", {}, is_notification=True)
        except Exception as e:
            print(f"Initialize error: {e}")
    
    def stop(self) -> None:
        """LSP client'ı durdur (sync)."""
        if self.process:
            try:
                self._send_message("shutdown", {})
                self._send_message("exit", {}, is_notification=True)
                self.process.terminate()
                self.process.wait(timeout=5)
            except Exception as e:
                print(f"LSP stop error: {e}")
                self.process.kill()
            finally:
                self.process = None
                self.is_running = False
    
    def open_document(self, uri: str, language_id: str, text: str) -> bool:
        """
        Dokümanı aç (sync).
        
        Args:
            uri: Document URI
            language_id: Language identifier
            text: Document text
            
        Returns:
            bool: Success status
        """
        if not self.is_running:
            return False
        
        try:
            params = {
                "textDocument": {
                    "uri": uri,
                    "languageId": language_id,
                    "version": 1,
                    "text": text
                }
            }
            self._send_message("textDocument/didOpen", params, is_notification=True)
            self.documents[uri] = text
            return True
        except Exception as e:
            print(f"Open document error: {e}")
            return False
    
    def get_completion(self, uri: str, line: int, character: int) -> Optional[Dict[str, Any]]:
        """
        Completion al (sync).
        
        Args:
            uri: Document URI
            line: Line number
            character: Character offset
            
        Returns:
            Optional[Dict[str, Any]]: Completion result
        """
        if not self.is_running:
            return None
        
        try:
            params = {
                "textDocument": {"uri": uri},
                "position": {"line": line, "character": character}
            }
            result = self._send_message("textDocument/completion", params)
            
            print(f"Completion raw result: {result}")
            
            if result is None:
                return None
            
            if "result" in result:
                result_data = result["result"]
                if result_data is None:
                    return {"isIncomplete": False, "items": []}
                
                return {
                    "isIncomplete": result_data.get("isIncomplete", False),
                    "items": [
                        {
                            "label": item.get("label", ""),
                            "kind": item.get("kind", 1),
                            "detail": item.get("detail", ""),
                            "documentation": item.get("documentation", ""),
                            "insertText": item.get("insertText", item.get("label", ""))
                        }
                        for item in result_data.get("items", [])
                    ]
                }
            elif "error" in result:
                print(f"Completion error: {result['error']}")
                return None
            
            return None
        except Exception as e:
            print(f"Get completion error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_hover(self, uri: str, line: int, character: int) -> Optional[str]:
        """
        Hover bilgisi al (sync).
        
        Args:
            uri: Document URI
            line: Line number
            character: Character offset
            
        Returns:
            Optional[str]: Hover text
        """
        if not self.is_running:
            return None
        
        try:
            params = {
                "textDocument": {"uri": uri},
                "position": {"line": line, "character": character}
            }
            result = self._send_message("textDocument/hover", params)
            
            if result and "result" in result:
                contents = result["result"].get("contents")
                if isinstance(contents, str):
                    return contents
                elif isinstance(contents, list) and len(contents) > 0:
                    return str(contents[0])
                elif isinstance(contents, dict):
                    return contents.get("value", str(contents))
            return None
        except Exception as e:
            print(f"Get hover error: {e}")
            return None
    
    def get_diagnostics(self, uri: str) -> List:
        """
        Diagnostics al (sync).
        
        Args:
            uri: Document URI
            
        Returns:
            List: Diagnostics
        """
        # Diagnostics genellikle notification olarak gelir
        return []
    
    def is_alive(self) -> bool:
        """
        Client'ın yaşayıp yaşamadığını kontrol et.
        
        Returns:
            bool: Alive status
        """
        return self.is_running and self.process is not None


if __name__ == "__main__":
    # Test
    def test_lsp_manager():
        from app.core.config import PROJECT_ROOT
        
        config = LSPManagerConfig(project_root=str(PROJECT_ROOT))
        manager = LSPManager(config)
        
        # Başlat
        if manager.start():
            print("LSP manager started")
            
            # Doküman aç
            code = "def hello():\n    print('world')"
            uri = "file:///test.py"
            if manager.open_document(uri, "python", code):
                print("Document opened")
                
                # Completion test
                completion = manager.get_completion(uri, 0, 5)
                print(f"Completion: {completion}")
                
                # Hover test
                hover = manager.get_hover(uri, 0, 4)
                print(f"Hover: {hover}")
            
            # Durdur
            manager.stop()
            print("LSP manager stopped")
    
    test_lsp_manager()
