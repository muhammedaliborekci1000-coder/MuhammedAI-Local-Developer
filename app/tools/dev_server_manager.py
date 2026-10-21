"""
Dev Server Manager
Development server başlatma, yönetme ve kontrol etme.
"""

import subprocess
import re
import time
import socket
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Callable
from enum import Enum

from app.core.config import PROJECT_ROOT
from app.tools.terminal_executor import TerminalExecutor, TerminalCommand
from app.tools.terminal_security import RiskLevel
from app.tools.http_inspector import HttpInspector


class ServerState(Enum):
    """Server durumları."""
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    TIMEOUT = "TIMEOUT"


@dataclass
class ServerInfo:
    """Server bilgisi."""
    pid: Optional[int]
    command: str
    working_directory: str
    port: Optional[int]
    state: ServerState
    startup_time: float
    last_check_time: float
    stdout: str
    stderr: str
    error: Optional[str]
    health_check_passed: bool


class DevServerManager:
    """
    Development server yöneticisi.
    
    Özellikler:
    - Server başlatma
    - Process ID takip etme
    - stdout/stderr yakalama
    - Port tespiti
    - Process durdurma
    - Timeout
    - Startup timeout
    - Health check
    - Server state takibi
    """
    
    def __init__(
        self,
        project_root: Path = PROJECT_ROOT,
        startup_timeout: int = 30,
        health_check_timeout: int = 10
    ):
        """
        Args:
            project_root: Proje kök dizini
            startup_timeout: Startup timeout (saniye)
            health_check_timeout: Health check timeout (saniye)
        """
        self.project_root = Path(project_root)
        self.startup_timeout = startup_timeout
        self.health_check_timeout = health_check_timeout
        
        self.terminal_executor = TerminalExecutor(project_root)
        self.http_inspector = HttpInspector()
        
        self.active_servers: dict[int, ServerInfo] = {}
    
    def start_server(
        self,
        command: str,
        working_directory: Optional[str] = None,
        expected_port: Optional[int] = None,
        shell: str = "powershell",
        dry_run: bool = False
    ) -> ServerInfo:
        """
        Server başlat.
        
        Args:
            command: Start command
            working_directory: Working directory
            expected_port: Beklenen port
            shell: Shell tipi
            dry_run: Dry-run
            
        Returns:
            ServerInfo: Server bilgisi
        """
        startup_time = time.time()
        
        # Dry-run
        if dry_run:
            return ServerInfo(
                pid=None,
                command=command,
                working_directory=working_directory or str(self.project_root),
                port=expected_port,
                state=ServerState.STARTING,
                startup_time=startup_time,
                last_check_time=time.time(),
                stdout="[DRY-RUN: Server not started]",
                stderr="[DRY-RUN: Server not started]",
                error=None,
                health_check_passed=False
            )
        
        # Terminal command oluştur
        cmd = TerminalCommand(
            command=command,
            shell=shell,
            working_directory=working_directory,
            timeout=self.startup_timeout,
            dry_run=False
        )
        
        # Komutu çalıştır (background'da)
        try:
            # Background process başlat
            process = subprocess.Popen(
                self.terminal_executor._build_shell_command(cmd),
                cwd=working_directory or str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            
            # Server info oluştur
            server_info = ServerInfo(
                pid=process.pid,
                command=command,
                working_directory=working_directory or str(self.project_root),
                port=expected_port,
                state=ServerState.STARTING,
                startup_time=startup_time,
                last_check_time=time.time(),
                stdout="",
                stderr="",
                error=None,
                health_check_passed=False
            )
            
            # Active servers'a ekle
            self.active_servers[process.pid] = server_info
            
            # Startup için bekle
            time.sleep(2)
            
            # Port tespit et
            detected_port = self._detect_port(process.pid)
            if detected_port:
                server_info.port = detected_port
            
            # Health check
            if server_info.port:
                health_result = self.http_inspector.health_check(
                    f"http://127.0.0.1:{server_info.port}",
                    timeout=self.health_check_timeout
                )
                server_info.health_check_passed = health_result["healthy"]
                
                if health_result["healthy"]:
                    server_info.state = ServerState.RUNNING
                else:
                    server_info.state = ServerState.FAILED
                    server_info.error = "Health check failed"
            else:
                server_info.state = ServerState.FAILED
                server_info.error = "Could not detect port"
            
            # stdout/stderr oku
            try:
                stdout, stderr = process.communicate(timeout=1)
                server_info.stdout = stdout
                server_info.stderr = stderr
            except subprocess.TimeoutExpired:
                pass
            
            server_info.last_check_time = time.time()
            
            return server_info
            
        except Exception as exc:
            return ServerInfo(
                pid=None,
                command=command,
                working_directory=working_directory or str(self.project_root),
                port=expected_port,
                state=ServerState.FAILED,
                startup_time=startup_time,
                last_check_time=time.time(),
                stdout="",
                stderr="",
                error=f"Failed to start server: {exc}",
                health_check_passed=False
            )
    
    def stop_server(self, pid: int) -> bool:
        """
        Server durdur.
        
        Args:
            pid: Process ID
            
        Returns:
            bool: Başarılı mı
        """
        if pid not in self.active_servers:
            return False
        
        server_info = self.active_servers[pid]
        server_info.state = ServerState.STOPPING
        
        try:
            # Process terminate
            subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True)
            
            server_info.state = ServerState.STOPPED
            del self.active_servers[pid]
            return True
            
        except Exception as exc:
            server_info.error = f"Failed to stop server: {exc}"
            server_info.state = ServerState.FAILED
            return False
    
    def get_server_info(self, pid: int) -> Optional[ServerInfo]:
        """
        Server bilgisi al.
        
        Args:
            pid: Process ID
            
        Returns:
            Optional[ServerInfo]: Server bilgisi
        """
        return self.active_servers.get(pid)
    
    def check_port(self, port: int) -> bool:
        """
        Port kullanımda mı?
        
        Args:
            port: Port
            
        Returns:
            bool: Kullanımda mı
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(("127.0.0.1", port))
                return result == 0
        except Exception:
            return False
    
    def _detect_port(self, pid: int) -> Optional[int]:
        """
        Process'in kullandığı portu tespit et.
        
        Args:
            pid: Process ID
            
        Returns:
            Optional[int]: Port
        """
        # psutil olmadığı için port tespiti yapılamıyor
        # Expected port'u kullan
        return None
    
    def cleanup(self) -> None:
        """Tüm active server'ları temizle."""
        for pid in list(self.active_servers.keys()):
            self.stop_server(pid)
