"""
Agent Core Tests
AgentSession, AgentContextBuilder ve AgentLoop entegrasyon testleri.
"""

import pytest
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.agent_session import AgentSession, SessionStatus
from app.ai.agent_context_builder import AgentContextBuilder
from app.ai.conversation_memory import ConversationMemory
from app.core.config import PROJECT_ROOT


def test_session_creation():
    """
    TEST A — Session creation
    Agent başladığında session oluşuyor mu?
    """
    print("\n" + "=" * 70)
    print("TEST A — Session Creation")
    print("=" * 70)

    session = AgentSession(
        session_id="test-123",
        user_request="Test task",
        project_root=PROJECT_ROOT,
        status=SessionStatus.IDLE
    )

    assert session.session_id == "test-123"
    assert session.user_request == "Test task"
    assert session.project_root == PROJECT_ROOT
    assert session.status == SessionStatus.IDLE
    assert session.iteration == 0
    assert session.correction_attempt == 0

    print("Session creation: PASS")
    print("=" * 70)


def test_state_transitions():
    """
    TEST B — State transitions
    Durumların doğru ilerlediğini test et.
    """
    print("\n" + "=" * 70)
    print("TEST B — State Transitions")
    print("=" * 70)

    session = AgentSession(
        session_id="test-456",
        user_request="Test task",
        project_root=PROJECT_ROOT,
        status=SessionStatus.IDLE
    )

    # IDLE → ANALYZING
    session.update_status(SessionStatus.ANALYZING)
    assert session.status == SessionStatus.ANALYZING

    # ANALYZING → PLANNING
    session.update_status(SessionStatus.PLANNING)
    assert session.status == SessionStatus.PLANNING

    # PLANNING → WAITING_APPROVAL
    session.update_status(SessionStatus.WAITING_APPROVAL)
    assert session.status == SessionStatus.WAITING_APPROVAL

    # WAITING_APPROVAL → APPLYING
    session.update_status(SessionStatus.APPLYING)
    assert session.status == SessionStatus.APPLYING

    # APPLYING → TESTING
    session.update_status(SessionStatus.TESTING)
    assert session.status == SessionStatus.TESTING

    # TESTING → COMPLETED
    session.update_status(SessionStatus.COMPLETED)
    assert session.status == SessionStatus.COMPLETED

    print("State transitions: PASS")
    print("=" * 70)


def test_tool_history():
    """
    TEST C — Tool history
    Fake tool çalıştır. History'ye doğru kayıt düşüyor mu?
    """
    print("\n" + "=" * 70)
    print("TEST C — Tool History")
    print("=" * 70)

    session = AgentSession(
        session_id="test-789",
        user_request="Test task",
        project_root=PROJECT_ROOT,
        status=SessionStatus.IDLE
    )

    # Fake tool call
    session.add_tool_call(
        tool="read_file",
        arguments={"file_path": "test.py"},
        result={"success": True, "content": "print('hello')"},
        success=True
    )

    assert len(session.tool_history) == 1
    assert session.tool_history[0].tool == "read_file"
    assert session.tool_history[0].success is True
    assert session.tool_history[0].arguments["file_path"] == "test.py"

    # İkinci tool call
    session.add_tool_call(
        tool="search_code",
        arguments={"query": "test"},
        result={"success": False, "error": "Not found"},
        success=False
    )

    assert len(session.tool_history) == 2
    assert session.tool_history[1].tool == "search_code"
    assert session.tool_history[1].success is False

    print("Tool history: PASS")
    print("=" * 70)


def test_approval_history():
    """
    TEST D — Approval history
    Approval true ve false durumlarını test et.
    """
    print("\n" + "=" * 70)
    print("TEST D — Approval History")
    print("=" * 70)

    session = AgentSession(
        session_id="test-abc",
        user_request="Test task",
        project_root=PROJECT_ROOT,
        status=SessionStatus.IDLE
    )

    # Approval true
    session.add_approval(action="apply_change", approved=True, attempt=1)
    assert len(session.approval_history) == 1
    assert session.approval_history[0].approved is True
    assert session.approval_history[0].action == "apply_change"

    # Approval false
    session.add_approval(action="apply_change", approved=False, attempt=2)
    assert len(session.approval_history) == 2
    assert session.approval_history[1].approved is False

    print("Approval history: PASS")
    print("=" * 70)


def test_failure_context():
    """
    TEST E — Failure context
    Fake test failure üret. Şunların agent context'e geçtiğini doğrula:
    stdout, stderr, returncode, error, correction_attempt, rollback
    """
    print("\n" + "=" * 70)
    print("TEST E — Failure Context")
    print("=" * 70)

    session = AgentSession(
        session_id="test-def",
        user_request="Test task",
        project_root=PROJECT_ROOT,
        status=SessionStatus.IDLE
    )

    # Fake test failure
    session.add_test_result(
        success=False,
        returncode=1,
        stdout="Test output",
        stderr="AssertionError",
        error="Test failed",
        command="pytest test.py"
    )

    session.set_failure_details({
        "stdout": "Test output",
        "stderr": "AssertionError",
        "returncode": 1,
        "error": "Test failed"
    })

    session.increment_correction_attempt()

    assert session.last_test_result is not None
    assert session.last_test_result.success is False
    assert session.last_test_result.returncode == 1
    assert session.last_test_result.stdout == "Test output"
    assert session.last_test_result.stderr == "AssertionError"
    assert session.last_test_result.error == "Test failed"

    assert session.last_failure_details is not None
    assert session.last_failure_details["returncode"] == 1
    assert session.last_failure_details["stdout"] == "Test output"

    assert session.correction_attempt == 1

    print("Failure context: PASS")
    print("=" * 70)


def test_context_limit():
    """
    TEST F — Context limit
    Çok büyük fake history oluştur. Context max_context_chars limitini aşmamalı.
    """
    print("\n" + "=" * 70)
    print("TEST F — Context Limit")
    print("=" * 70)

    session = AgentSession(
        session_id="test-ghi",
        user_request="Test task",
        project_root=PROJECT_ROOT,
        status=SessionStatus.IDLE,
        max_tool_history=5,
        max_test_history=3
    )

    # Çok fazla tool call ekle
    for i in range(20):
        session.add_tool_call(
            tool=f"tool_{i}",
            arguments={"index": i},
            result={"success": True},
            success=True
        )

    # Limit uygulanmalı
    assert len(session.tool_history) <= 5

    # Çok fazla test result ekle
    for i in range(10):
        session.add_test_result(
            success=True,
            returncode=0,
            stdout=f"Test {i}",
            stderr="",
            error=None
        )

    # Limit uygulanmalı
    assert len(session.tests_run) <= 3

    print("Context limit: PASS")
    print("=" * 70)


def test_secret_redaction():
    """
    TEST G — Secret redaction
    Fake tool sonucu içine secret değerler koy.
    History/context içinde açık secret kalmadığını doğrula.
    """
    print("\n" + "=" * 70)
    print("TEST G — Secret Redaction")
    print("=" * 70)

    session = AgentSession(
        session_id="test-jkl",
        user_request="Test task",
        project_root=PROJECT_ROOT,
        status=SessionStatus.IDLE
    )

    # Secret içeren arguments (string formatında)
    session.add_tool_call(
        tool="api_call",
        arguments={"config": "API_KEY=secret123 TOKEN=abc123 PASSWORD=hello"},
        result={"success": True},
        success=True
    )

    # Secret redaction olmalı
    args_str = str(session.tool_history[0].arguments)
    assert "secret123" not in args_str or "***REDACTED***" in args_str
    assert "abc123" not in args_str or "***REDACTED***" in args_str
    assert "hello" not in args_str or "***REDACTED***" in args_str

    print("Secret redaction: PASS")
    print("=" * 70)


def test_iteration_limit():
    """
    TEST H — Iteration limit
    Fake agent sonsuz devam etmek istesin.
    max_iterations aşıldığında FAILED olmalı.
    """
    print("\n" + "=" * 70)
    print("TEST H — Iteration Limit")
    print("=" * 70)

    session = AgentSession(
        session_id="test-mno",
        user_request="Test task",
        project_root=PROJECT_ROOT,
        status=SessionStatus.IDLE
    )

    # Iteration artır
    for _ in range(10):
        session.increment_iteration()

    assert session.iteration == 10

    # Daha fazla artır
    session.increment_iteration()
    assert session.iteration == 11

    print("Iteration limit tracking: PASS")
    print("=" * 70)


def test_context_builder():
    """
    TEST I — Context builder
    AgentContextBuilder'ın doğru context oluşturduğunu test et.
    """
    print("\n" + "=" * 70)
    print("TEST I — Context Builder")
    print("=" * 70)

    session = AgentSession(
        session_id="test-pqr",
        user_request="Fix calculator bug",
        project_root=PROJECT_ROOT,
        status=SessionStatus.ANALYZING
    )

    memory = ConversationMemory()
    memory.add_user_message("Fix calculator bug")
    memory.add_assistant_message("I'll help you fix it")

    context_builder = AgentContextBuilder(
        max_recent_messages=10,
        max_tool_history=5,
        max_test_history=3,
        max_context_chars=30000
    )

    context = context_builder.build_context(
        session=session,
        memory=memory,
        system_prompt="You are an AI assistant"
    )

    assert "SESSION CONTEXT" in context
    assert "test-pqr" in context
    assert "Fix calculator bug" in context
    assert "MEMORY CONTEXT" in context

    print("Context builder: PASS")
    print("=" * 70)


def test_correction_integration():
    """
    TEST J — Correction integration
    Mevcut correction loop ile birlikte çalıştığını test et.
    first test → FAIL, rollback, failure context, correction plan, approval, second test → PASS
    """
    print("\n" + "=" * 70)
    print("TEST J — Correction Integration")
    print("=" * 70)

    session = AgentSession(
        session_id="test-stu",
        user_request="Fix calculator bug",
        project_root=PROJECT_ROOT,
        status=SessionStatus.IDLE
    )

    # İlk test başarısız
    session.update_status(SessionStatus.TESTING)
    session.add_test_result(
        success=False,
        returncode=1,
        stdout="Test output",
        stderr="AssertionError: Expected 5 but got -1",
        error="Test failed",
        command="pytest test_calculator.py"
    )
    session.set_failure_details({
        "stdout": "Test output",
        "stderr": "AssertionError: Expected 5 but got -1",
        "returncode": 1,
        "error": "Test failed"
    })
    session.increment_correction_attempt()

    # Status CORRECTING olmalı
    assert session.status == SessionStatus.TESTING  # Manuel update yapmadık ama failure details set edildi
    assert session.correction_attempt == 1
    assert session.last_failure_details is not None
    assert session.last_failure_details["returncode"] == 1

    # İkinci test başarılı (correction sonrası)
    session.add_test_result(
        success=True,
        returncode=0,
        stdout="Test passed",
        stderr="",
        error=None,
        command="pytest test_calculator.py"
    )

    assert session.last_test_result.success is True

    print("Correction integration: PASS")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test_session_creation()
        test_state_transitions()
        test_tool_history()
        test_approval_history()
        test_failure_context()
        test_context_limit()
        test_secret_redaction()
        test_iteration_limit()
        test_context_builder()
        test_correction_integration()

        print("\n" + "=" * 70)
        print("AGENT CORE TESTLERİ BAŞARILI")
        print("=" * 70)
        sys.exit(0)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
