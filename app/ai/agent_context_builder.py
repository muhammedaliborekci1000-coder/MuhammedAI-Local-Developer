"""
MuhammedAI Local Developer - Agent Context Builder
Agent için kontrollü context oluşturma.
"""

from typing import Dict, Any, Optional, List
from app.ai.agent_session import AgentSession, SessionStatus
from app.ai.conversation_memory import ConversationMemory
from app.ai.codebase_index import CodebaseIndex
from app.ai.memory import MemorySystem, MemoryScope
from app.ai.project_rules import ProjectRules


class AgentContextBuilder:
    """
    Agent için context oluşturur.
    
    Context bölümleri:
    - SYSTEM CONTEXT
    - PROJECT CONTEXT
    - SESSION CONTEXT
    - TASK CONTEXT
    - MEMORY CONTEXT
    - RECENT TOOL HISTORY
    - RECENT TEST RESULT
    - FAILURE DETAILS
    - CURRENT PLAN
    """
    
    def __init__(
        self,
        max_recent_messages: int = 20,
        max_tool_history: int = 30,
        max_test_history: int = 10,
        max_context_chars: int = 30000,
        codebase_index: Optional[CodebaseIndex] = None,
        memory_system: Optional[MemorySystem] = None,
        project_rules: Optional[ProjectRules] = None
    ):
        """
        Args:
            max_recent_messages: Maksimum recent message sayısı
            max_tool_history: Maksimum tool history kaydı
            max_test_history: Maksimum test history kaydı
            max_context_chars: Maksimum toplam context karakter
            codebase_index: Codebase index (opsiyonel)
            memory_system: Memory system (opsiyonel)
            project_rules: Project rules (opsiyonel)
        """
        self.max_recent_messages = max_recent_messages
        self.max_tool_history = max_tool_history
        self.max_test_history = max_test_history
        self.max_context_chars = max_context_chars
        self.codebase_index = codebase_index
        self.memory_system = memory_system
        self.project_rules = project_rules
    
    def build_context(
        self,
        session: AgentSession,
        memory: ConversationMemory,
        system_prompt: Optional[str] = None,
        relevant_files: Optional[List[str]] = None,
        task: Optional[str] = None
    ) -> str:
        """
        Tam context string'i oluşturur.
        
        Args:
            session: Agent session
            memory: Conversation memory
            system_prompt: Sistem prompt (opsiyonel)
            relevant_files: İlgili dosyalar (opsiyonel)
            task: Görev açıklaması (rules relevance için)
            
        Returns:
            str: Tam context
        """
        parts = []
        
        # System Context
        if system_prompt:
            parts.append(self._build_system_context(system_prompt))
        
        # Project Rules (öncelikli)
        if self.project_rules:
            parts.append(self._build_rules_context(task))
        
        # Session Context
        parts.append(self._build_session_context(session))
        
        # Project Context (basit - session'dan)
        parts.append(self._build_project_context(session))
        
        # Codebase Context (varsa)
        if self.codebase_index and relevant_files:
            parts.append(self._build_codebase_context(relevant_files))
        
        # Memory Context (varsa)
        if self.memory_system and session.session_id:
            parts.append(self._build_memory_system_context(session))
        
        # Task Context
        parts.append(self._build_task_context(session))
        
        # Conversation Memory (recent messages)
        parts.append(self._build_memory_context(memory))
        
        # Tool History (recent)
        parts.append(self._build_tool_history_context(session))
        
        # Test Result (recent)
        parts.append(self._build_test_result_context(session))
        
        # Failure Details (varsa)
        if session.last_failure_details:
            parts.append(self._build_failure_context(session))
        
        # Current Plan (varsa)
        if session.last_plan:
            parts.append(self._build_current_plan_context(session))
        
        # Birleştir ve limit uygula
        full_context = "\n\n".join(parts)
        
        if len(full_context) > self.max_context_chars:
            # Basit truncation - baştan kesme
            full_context = full_context[-self.max_context_chars:]
            full_context = "...[CONTEXT TRUNCATED]...\n\n" + full_context
        
        return full_context
    
    def _build_system_context(self, system_prompt: str) -> str:
        """System context."""
        return f"=== SYSTEM CONTEXT ===\n{system_prompt}"
    
    def _build_session_context(self, session: AgentSession) -> str:
        """Session context."""
        return (
            f"=== SESSION CONTEXT ===\n"
            f"Session ID: {session.session_id}\n"
            f"Status: {session.status.value}\n"
            f"Iteration: {session.iteration}\n"
            f"Correction Attempt: {session.correction_attempt}\n"
            f"Changed Files: {len(session.changed_files)}\n"
        )
    
    def _build_project_context(self, session: AgentSession) -> str:
        """Project context."""
        return (
            f"=== PROJECT CONTEXT ===\n"
            f"Project Root: {session.project_root}\n"
        )
    
    def _build_task_context(self, session: AgentSession) -> str:
        """Task context."""
        return (
            f"=== TASK CONTEXT ===\n"
            f"User Request: {session.user_request}\n"
            f"Current Task: {session.current_task or 'None'}\n"
        )
    
    def _build_memory_context(self, memory: ConversationMemory) -> str:
        """Memory context (recent messages)."""
        messages = memory.messages
        
        # Recent messages limit
        recent_messages = messages[-self.max_recent_messages:] if len(messages) > self.max_recent_messages else messages
        
        if not recent_messages:
            return "=== MEMORY CONTEXT ===\nNo recent messages."
        
        lines = ["=== MEMORY CONTEXT ==="]
        for msg in recent_messages:
            lines.append(f"[{msg.role.upper()}]")
            lines.append(msg.content)
            lines.append("")
        
        return "\n".join(lines)
    
    def _build_tool_history_context(self, session: AgentSession) -> str:
        """Tool history context (recent)."""
        if not session.tool_history:
            return "=== TOOL HISTORY ===\nNo tool calls."
        
        # Recent tool history limit
        recent_tools = session.tool_history[-self.max_tool_history:] if len(session.tool_history) > self.max_tool_history else session.tool_history
        
        lines = ["=== TOOL HISTORY ==="]
        for record in recent_tools:
            lines.append(f"Tool: {record.tool}")
            lines.append(f"Success: {record.success}")
            lines.append(f"Arguments: {record.arguments}")
            lines.append(f"Result: {record.result}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _build_test_result_context(self, session: AgentSession) -> str:
        """Test result context (recent)."""
        if not session.tests_run:
            return "=== TEST RESULTS ===\nNo tests run."
        
        # Recent test history limit
        recent_tests = session.tests_run[-self.max_test_history:] if len(session.tests_run) > self.max_test_history else session.tests_run
        
        lines = ["=== TEST RESULTS ==="]
        for result in recent_tests:
            lines.append(f"Success: {result.success}")
            lines.append(f"Returncode: {result.returncode}")
            lines.append(f"Stdout: {result.stdout}")
            lines.append(f"Stderr: {result.stderr}")
            lines.append(f"Error: {result.error}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _build_failure_context(self, session: AgentSession) -> str:
        """Failure details context."""
        if not session.last_failure_details:
            return ""
        
        details = session.last_failure_details
        return (
            f"=== FAILURE DETAILS ===\n"
            f"Previous change failed and was rolled back.\n"
            f"Real test result:\n"
            f"returncode: {details.get('returncode')}\n"
            f"stdout: {details.get('stdout', '')}\n"
            f"stderr: {details.get('stderr', '')}\n"
            f"error: {details.get('error', '')}\n"
            f"Correction attempt: {session.correction_attempt}\n"
        )
    
    def _build_current_plan_context(self, session: AgentSession) -> str:
        """Current plan context."""
        if not session.last_plan:
            return ""
        
        plan = session.last_plan
        return (
            f"=== CURRENT PLAN ===\n"
            f"File: {plan.get('file')}\n"
            f"Function: {plan.get('function')}\n"
            f"Problem: {plan.get('problem')}\n"
            f"Change: {plan.get('change')}\n"
            f"Reason: {plan.get('reason')}\n"
        )
    
    def _build_codebase_context(self, relevant_files: List[str]) -> str:
        """Codebase context (relevant files)."""
        if not self.codebase_index:
            return ""
        
        lines = ["=== CODEBASE CONTEXT ==="]
        
        for file_path in relevant_files:
            if file_path not in self.codebase_index.files:
                continue
            
            file_index = self.codebase_index.files[file_path]
            
            if file_index.parse_error:
                lines.append(f"\nFile: {file_path}")
                lines.append(f"  Parse error: {file_index.parse_error}")
                continue
            
            lines.append(f"\nFile: {file_path}")
            
            # Symbols
            if file_index.symbols:
                lines.append("  Symbols:")
                for symbol in file_index.symbols[:10]:  # Max 10 symbols
                    lines.append(f"    - {symbol.type} {symbol.name} (line {symbol.line_start})")
            
            # Imports
            if file_index.imports:
                lines.append("  Imports:")
                for imp in file_index.imports[:10]:  # Max 10 imports
                    if imp.is_from:
                        lines.append(f"    - from {imp.from_module} import {imp.name}")
                    else:
                        lines.append(f"    - import {imp.module}")
        
        return "\n".join(lines)
    
    def _build_rules_context(self, task: Optional[str] = None) -> str:
        """Project rules context."""
        if not self.project_rules:
            return ""
        
        rules = self.project_rules.get_relevant_rules(task=task, max_rules=15)
        
        if not rules:
            return "=== PROJECT RULES ===\nNo rules found."
        
        lines = ["=== PROJECT RULES ==="]
        for rule in rules:
            lines.append(f"- {rule.content}")
        
        return "\n".join(lines)
    
    def _build_memory_system_context(self, session: AgentSession) -> str:
        """Memory system context."""
        if not self.memory_system:
            return ""
        
        # Session ve project scope memory'leri al
        memories = []
        
        # Session memory
        session_memories = self.memory_system.search(
            query="",
            scope=MemoryScope.SESSION,
            session_id=session.session_id,
            min_importance=3,
            limit=5
        )
        memories.extend(session_memories)
        
        # Project memory
        project_memories = self.memory_system.search(
            query="",
            scope=MemoryScope.PROJECT,
            project_id=str(session.project_root),
            min_importance=4,
            limit=5
        )
        memories.extend(project_memories)
        
        if not memories:
            return "=== MEMORY ===\nNo relevant memories."
        
        lines = ["=== MEMORY ==="]
        for mem in memories[:10]:  # Max 10 memories
            lines.append(f"[{mem.category.value}] {mem.content}")
        
        return "\n".join(lines)
