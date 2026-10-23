import sys
sys.path.insert(0, '.')

from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.ollama_client import OllamaClient
from app.tools.tool_registry import ToolRegistry

ollama_client = OllamaClient()
tool_registry = ToolRegistry()
config = LoopConfig(max_iterations=1)
agent_loop = AgentLoop(ollama_client=ollama_client, tool_registry=tool_registry, config=config)

user_task = 'git status'

# Memory'ye user message ekle
agent_loop.memory.add_user_message(user_task)

# Messages'ı kontrol et
messages = agent_loop.memory.get_messages()
print(f'Message count: {len(messages)}')
for i, msg in enumerate(messages):
    print(f'{i}: role={msg.get("role")}, content_len={len(msg.get("content", ""))}')
