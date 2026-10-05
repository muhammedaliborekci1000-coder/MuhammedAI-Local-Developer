import pytest

from app.ai.agent_loop import AgentLoop, LoopConfig


class FakeAI:
    """Tool çağrısı yapmadan her seferinde normal metin döndüren sahte model."""

    def __init__(self):
        self.call_count = 0

    def chat(self, *args, **kwargs):
        self.call_count += 1
        return (
            "Dosyanın içeriğini okuyamadım. "
            "Herhangi bir tool çağrısı yapmadan cevap veriyorum."
        )


class FakeRegistry:
    """Gerçek tool çalıştırmamak için minimal sahte registry."""

    def __init__(self):
        self.calls = []
        # Mock workflow for AgentLoop initialization
        self.workflow = None

    def has(self, name):
        return name == "read_file"

    def get_detailed_tools_for_prompt(self):
        return """
- read_file:
  Açıklama: Dosya içeriğini okur.
  Parametreler:
    - relative_path: str, zorunlu
"""

    def get_tool_schema(self, name):
        if name != "read_file":
            return None

        return {
            "name": "read_file",
            "description": "Dosya okur.",
            "parameters": [
                {
                    "name": "relative_path",
                    "type": "str",
                    "required": True,
                }
            ],
        }

    def execute(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        raise AssertionError(
            "Bu testte hiçbir gerçek tool çalıştırılmamalı."
        )


def test_no_tool_retry_limit():
    """
    Model hiçbir tool çağrısı üretmezse AgentLoop'un
    max_no_tool_retries sınırını aşmamasını test eder.

    Beklenen:
    - İlk model çağrısı + en fazla 2 retry = en fazla 3 çağrı.
    - read_file gerçekte çalıştırılmamalı.
    - Gerçek dosya değiştirilmemeli.
    """

    fake_ai = FakeAI()
    fake_registry = FakeRegistry()

    config = LoopConfig(
        max_iterations=10,
        max_no_tool_retries=2,
        enable_logging=False,
    )

    loop = AgentLoop(
        ollama_client=fake_ai,
        tool_registry=fake_registry,
        config=config,
        approval_callback=None,
    )

    user_request = "app/tools/tool_registry.py dosyasını oku."

    # AgentLoop'un mevcut çalışma metodunu bul.
    run_method = getattr(loop, "run_task", None)

    if run_method is None:
        run_method = getattr(loop, "run", None)

    if run_method is None:
        pytest.fail(
            "AgentLoop üzerinde run_task veya run metodu bulunamadı."
        )

    # Mevcut imzaya göre çağırmayı dene.
    try:
        result = run_method(user_request)
    except TypeError:
        pytest.fail(
            "AgentLoop çalışma metodunun imzası beklenenden farklı. "
            "Mevcut run_task/run imzası incelenmeli."
        )

    # 1) İlk çağrı + en fazla 2 retry.
    assert fake_ai.call_count <= 3, (
        f"Model {fake_ai.call_count} kez çağrıldı. "
        "Beklenen maksimum: 3."
    )

    # 2) Gerçek tool çalıştırılmamalı.
    assert len(fake_registry.calls) == 0, (
        "Model tool çağırmamasına rağmen gerçek bir tool çalıştırıldı."
    )

    # 3) AgentLoop sonucu güvenli şekilde dönmeli.
    assert result is not None

    # 4) Modelin dosya içeriğini uydurmadığından emin ol.
    if hasattr(result, "final_response"):
        response = result.final_response.lower()

        assert "from pathlib import path" not in response
        assert "toolregistry" not in response or "dosya" in response