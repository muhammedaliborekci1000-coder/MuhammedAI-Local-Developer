from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.tool_parser import ToolCall
from app.tools.tool_registry import ToolRegistry


class FakeWorkflow:
    def __init__(self, valid=True):
        self.create_calls = 0
        self.apply_calls = []
        self.valid = valid

    def create_plan(self, file_path, problem):
        self.create_calls += 1
        return {
            "plan": {
                "file": file_path,
                "old_code": "return 1",
                "new_code": "return 2",
            },
            "validation": {"valid": self.valid, "errors": []},
        }

    def apply_change(self, plan, test_file, approved=False):
        self.apply_calls.append((plan, test_file, approved))
        return {
            "success": True,
            "backup": "backup.py",
            "test": {"success": True},
        }


def make_agent(workflow, approval_callback):
    registry = ToolRegistry()
    registry.workflow = workflow
    registry.register(
        name="create_change_plan",
        description="test",
        handler=workflow.create_plan,
        category="coding",
    )
    return AgentLoop(
        ollama_client=None,
        tool_registry=registry,
        config=LoopConfig(enable_logging=False),
        approval_callback=approval_callback,
    )


def test_create_plan_reuses_one_plan_and_auto_discovers_relative_test_file(
    tmp_path, monkeypatch
):
    (tmp_path / "target.py").write_text("def value():\n    return 1\n", encoding="utf-8")
    (tmp_path / "test_target.py").write_text("# test\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("app.ai.agent_loop.PROJECT_ROOT", tmp_path)

    workflow = FakeWorkflow()
    approvals = []
    agent = make_agent(
        workflow,
        lambda tool_name, arguments: approvals.append((tool_name, arguments)) or True,
    )
    call = ToolCall(
        name="create_change_plan",
        arguments={"file_path": "target.py", "problem": "change return value"},
        raw_text="",
    )

    result = agent._execute_tool_call(call)

    expected_plan = {
        "file": "target.py",
        "old_code": "return 1",
        "new_code": "return 2",
    }
    assert workflow.create_calls == 1
    assert approvals[0][0] == "apply_change"
    assert approvals[0][1]["plan"] == expected_plan
    assert workflow.apply_calls == [(expected_plan, "test_target.py", True)]
    assert result["success"] is True
    assert result["orchestration"] == {
        "state": "COMPLETE",
        "approval": "approved",
        "test_file": "test_target.py",
        "apply_change": "completed",
    }


def test_rejected_plan_is_recorded_as_failure_and_never_applied():
    workflow = FakeWorkflow()
    approval_calls = []
    agent = make_agent(
        workflow,
        lambda tool_name, arguments: approval_calls.append(tool_name) or False,
    )
    call = ToolCall(
        name="create_change_plan",
        arguments={
            "file_path": "target.py",
            "problem": "change return value",
            "test_file": "test_target.py",
        },
        raw_text="",
    )

    first_result = agent._execute_tool_call(call)
    cached_result = agent._execute_tool_call(call)

    assert first_result["success"] is False
    assert first_result["orchestration"]["approval"] == "rejected"
    assert cached_result["success"] is False
    assert cached_result["cached"] is True
    assert len(approval_calls) == 1
    assert workflow.create_calls == 1
    assert workflow.apply_calls == []


def test_invalid_plan_does_not_request_approval_or_apply():
    workflow = FakeWorkflow(valid=False)
    approval_calls = []
    agent = make_agent(
        workflow,
        lambda tool_name, arguments: approval_calls.append(tool_name) or True,
    )
    call = ToolCall(
        name="create_change_plan",
        arguments={
            "file_path": "target.py",
            "problem": "change return value",
            "test_file": "test_target.py",
        },
        raw_text="",
    )

    result = agent._execute_tool_call(call)

    assert result["success"] is False
    assert "doğrulamadan" in result["error"]
    assert approval_calls == []
    assert workflow.apply_calls == []
