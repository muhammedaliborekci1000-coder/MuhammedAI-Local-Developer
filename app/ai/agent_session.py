"""
MuhammedAI Local Developer - Agent Session
Agent çalışma oturumu ve state yönetimi.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, UTC
from enum import Enum
from pathlib import Path


class SessionStatus(Enum):
    """Session durumları."""
    IDLE = "IDLE"
    ANALYZING = "ANALYZING"
    PLANNING = "PLANNING"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    APPLYING = "APPLYING"
    TESTING = "TESTING"
    CORRECTING = "CORRECTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass
class ToolCallRecord:
    """Tool çağrısı kaydı."""
    tool: str
    arguments: Dict[str, Any]
    result: Dict[str, Any]
    success: bool
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class ApprovalRecord:
    """Approval kaydı."""
    action: str
    approved: bool
    attempt: int
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class TestResult:
    """Test sonucu kaydı."""
    success: bool
    returncode: Optional[int]
    stdout: str
    stderr: str
    error: Optional[str]
    command: Optional[str]
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class AgentSession:
    """
    Agent çalışma oturumu.
    
    Session boyunca:
    - State takibi
    - Tool history
    - Approval history
    - Changed files
    - Test results
    - Failure details
    - Web preview state
    """
    session_id: str
    user_request: str
    project_root: Path
    status: SessionStatus = SessionStatus.IDLE
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    
    # Task state
    current_task: Optional[str] = None
    iteration: int = 0
    correction_attempt: int = 0
    
    # Plan ve test
    last_plan: Optional[Dict[str, Any]] = None
    last_test_result: Optional[TestResult] = None
    last_failure_details: Optional[Dict[str, Any]] = None
    
    # History
    tool_history: List[ToolCallRecord] = field(default_factory=list)
    approval_history: List[ApprovalRecord] = field(default_factory=list)
    changed_files: List[str] = field(default_factory=list)
    tests_run: List[TestResult] = field(default_factory=list)
    
    # Web preview state
    web_framework: Optional[str] = None
    web_server_command: Optional[str] = None
    web_server_pid: Optional[int] = None
    web_port: Optional[int] = None
    web_preview_url: Optional[str] = None
    web_health_status: Optional[str] = None
    web_last_http_response: Optional[str] = None
    web_server_errors: List[str] = field(default_factory=list)
    web_restart_count: int = 0
    
    # Browser state
    browser_engine: Optional[str] = None
    browser_state: Optional[str] = None
    page_url: Optional[str] = None
    page_title: Optional[str] = None
    last_browser_action: Optional[str] = None
    last_browser_action_result: Optional[str] = None
    console_errors: List[str] = field(default_factory=list)
    network_errors: List[str] = field(default_factory=list)
    page_errors: List[str] = field(default_factory=list)
    screenshot_reference: Optional[str] = None
    browser_session_id: Optional[str] = None
    
    # Config limits
    max_tool_history: int = 30
    max_test_history: int = 10
    
    def update_status(self, new_status: SessionStatus) -> None:
        """Status güncelle."""
        self.status = new_status
        self.updated_at = datetime.now(UTC)
    
    def add_tool_call(self, tool: str, arguments: Dict[str, Any], 
                      result: Dict[str, Any], success: bool) -> None:
        """Tool çağrısı ekle."""
        record = ToolCallRecord(
            tool=tool,
            arguments=self._redact_secrets(arguments),
            result=self._redact_secrets(result),
            success=success
        )
        self.tool_history.append(record)
        
        # Limit uygula
        if len(self.tool_history) > self.max_tool_history:
            self.tool_history = self.tool_history[-self.max_tool_history:]
        
        self.updated_at = datetime.now(UTC)
    
    def add_approval(self, action: str, approved: bool, attempt: int = 0) -> None:
        """Approval kaydı ekle."""
        record = ApprovalRecord(
            action=action,
            approved=approved,
            attempt=attempt
        )
        self.approval_history.append(record)
        self.updated_at = datetime.now(UTC)
    
    def add_changed_file(self, file_path: str) -> None:
        """Değişen dosya ekle (duplicate yok)."""
        if file_path not in self.changed_files:
            self.changed_files.append(file_path)
            self.updated_at = datetime.now(UTC)
    
    def add_test_result(self, success: bool, returncode: Optional[int],
                       stdout: str, stderr: str, error: Optional[str],
                       command: Optional[str] = None) -> None:
        """Test sonucu ekle."""
        result = TestResult(
            success=success,
            returncode=returncode,
            stdout=stdout,
            stderr=stderr,
            error=error,
            command=command
        )
        self.tests_run.append(result)
        self.last_test_result = result
        
        # Limit uygula
        if len(self.tests_run) > self.max_test_history:
            self.tests_run = self.tests_run[-self.max_test_history:]
        
        self.updated_at = datetime.now(UTC)
    
    def set_failure_details(self, details: Dict[str, Any]) -> None:
        """Failure details set et."""
        self.last_failure_details = details
        self.updated_at = datetime.now(UTC)
    
    def increment_iteration(self) -> None:
        """Iteration artır."""
        self.iteration += 1
        self.updated_at = datetime.now(UTC)
    
    def increment_correction_attempt(self) -> None:
        """Correction attempt artır."""
        self.correction_attempt += 1
        self.updated_at = datetime.now(UTC)
    
    def set_web_preview_state(
        self,
        framework: Optional[str] = None,
        server_command: Optional[str] = None,
        server_pid: Optional[int] = None,
        port: Optional[int] = None,
        preview_url: Optional[str] = None,
        health_status: Optional[str] = None
    ) -> None:
        """Web preview state set et."""
        if framework is not None:
            self.web_framework = framework
        if server_command is not None:
            self.web_server_command = server_command
        if server_pid is not None:
            self.web_server_pid = server_pid
        if port is not None:
            self.web_port = port
        if preview_url is not None:
            self.web_preview_url = preview_url
        if health_status is not None:
            self.web_health_status = health_status
        self.updated_at = datetime.now(UTC)
    
    def add_web_server_error(self, error: str) -> None:
        """Web server hatası ekle."""
        self.web_server_errors.append(error)
        self.updated_at = datetime.now(UTC)
    
    def increment_web_restart_count(self) -> None:
        """Web restart count artır."""
        self.web_restart_count += 1
        self.updated_at = datetime.now(UTC)
    
    def set_browser_state(
        self,
        engine: Optional[str] = None,
        state: Optional[str] = None,
        page_url: Optional[str] = None,
        page_title: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> None:
        """Browser state set et."""
        if engine is not None:
            self.browser_engine = engine
        if state is not None:
            self.browser_state = state
        if page_url is not None:
            self.page_url = page_url
        if page_title is not None:
            self.page_title = page_title
        if session_id is not None:
            self.browser_session_id = session_id
        self.updated_at = datetime.now(UTC)
    
    def add_browser_action(self, action: str, result: str) -> None:
        """Browser action ekle."""
        self.last_browser_action = action
        self.last_browser_action_result = result
        self.updated_at = datetime.now(UTC)
    
    def add_console_error(self, error: str) -> None:
        """Console error ekle."""
        self.console_errors.append(error)
        self.updated_at = datetime.now(UTC)
    
    def add_network_error(self, error: str) -> None:
        """Network error ekle."""
        self.network_errors.append(error)
        self.updated_at = datetime.now(UTC)
    
    def add_page_error(self, error: str) -> None:
        """Page error ekle."""
        self.page_errors.append(error)
        self.updated_at = datetime.now(UTC)
    
    def set_screenshot_reference(self, path: str) -> None:
        """Screenshot reference set et."""
        self.screenshot_reference = path
        self.updated_at = datetime.now(UTC)
    
    def _redact_secrets(self, data: Any) -> Any:
        """
        Secret değerleri redact et.
        
        Redacts:
        - API_KEY
        - TOKEN
        - PASSWORD
        - SECRET
        """
        if isinstance(data, dict):
            return {k: self._redact_secrets(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._redact_secrets(item) for item in data]
        elif isinstance(data, str):
            redacted = data
            # Case-insensitive secret redaction for key=value format
            import re
            for secret_key in ['API_KEY', 'TOKEN', 'PASSWORD', 'SECRET']:
                # Match key=value pattern (case-insensitive key)
                pattern = re.compile(
                    rf'(?i){re.escape(secret_key)}\s*=\s*\S+',
                    re.IGNORECASE
                )
                redacted = pattern.sub(f'{secret_key}=***REDACTED***', redacted)
            return redacted
        else:
            return data
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Context özeti döndür."""
        return {
            "session_id": self.session_id,
            "status": self.status.value,
            "iteration": self.iteration,
            "correction_attempt": self.correction_attempt,
            "changed_files_count": len(self.changed_files),
            "tool_calls_count": len(self.tool_history),
            "approvals_count": len(self.approval_history),
            "tests_run_count": len(self.tests_run),
            "last_test_success": self.last_test_result.success if self.last_test_result else None,
            "has_failure": self.last_failure_details is not None,
        }
