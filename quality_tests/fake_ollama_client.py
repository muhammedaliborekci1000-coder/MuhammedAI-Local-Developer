"""
Fake OllamaClient for testing AgentLoop without real AI
"""
import json


class FakeOllamaClient:
    """Deterministic fake model for testing AgentLoop"""
    
    def __init__(self, approval_mode=True):
        self.agent_loop_call_count = 0
        self.approval_mode = approval_mode
        
    def chat(self, message: str, response_format=None) -> str:
        """Return deterministic tool calls for AgentLoop"""
        
        # If response_format is dict, this is a request from ChangePlanner
        # Return a valid plan JSON for ChangePlanner
        if response_format == dict:
            return json.dumps({
                "file": "quality_tests/e2e_workspace/agent_task.py",
                "function": "greet",
                "problem": "greet fonksiyonunun mesajını değiştirmek",
                "change": "Merhaba mesajını Merhaba Muhammed olarak değiştirmek",
                "old_code": 'return "Merhaba"',
                "new_code": 'return "Merhaba Muhammed"',
                "reason": "E2E test"
            })
        
        # For AgentLoop calls
        self.agent_loop_call_count += 1
        
        if self.agent_loop_call_count == 1:
            # CALL 1: read_file
            return '{"tool": "read_file", "arguments": {"relative_path": "quality_tests/e2e_workspace/agent_task.py"}}'
        
        elif self.agent_loop_call_count == 2:
            # CALL 2: create_change_plan
            return '{"tool": "create_change_plan", "arguments": {"file_path": "quality_tests/e2e_workspace/agent_task.py", "problem": "greet fonksiyonunun mesajını değiştirmek", "test_file": "quality_tests/e2e_workspace/test_agent_task.py"}}'
        
        elif self.agent_loop_call_count == 3:
            # CALL 3: Done - return completion message (orkestratör apply_change'i halletti)
            return "Değişiklik başarıyla tamamlandı."
        
        else:
            # Any further calls
            return "Değişiklik tamamlandı."
