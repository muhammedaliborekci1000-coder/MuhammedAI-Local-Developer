"""
MuhammedAI Local Developer - Tool Registry
Aktif proje araçlarının merkezi kayıt ve çalıştırma katmanı.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

from app.tools.project_scanner import ProjectScanner
from app.tools.project_structure_analyzer import ProjectStructureAnalyzer
from app.tools.code_search import CodeSearch
from app.tools.file_reader import FileReader
from app.tools.error_detector import ErrorDetector
from app.tools.python_runner import PythonRunner
from app.tools.change_workflow import ChangeWorkflow
from app.ai.codebase_index import CodebaseIndex
from app.tools.web_project_detector import WebProjectDetector
from app.tools.dev_server_manager import DevServerManager
from app.tools.http_inspector import HttpInspector
from app.tools.web_preview import WebPreview
from app.tools.browser_engine import BrowserEngine
from app.tools.browser_manager import BrowserManager
from app.tools.browser_inspector import BrowserInspector
from app.tools.browser_actions import BrowserActions
from app.tools.terminal_executor import TerminalExecutor


@dataclass
class ToolDefinition:
    """AI tarafından kullanılabilen araç tanımı."""

    name: str
    description: str
    handler: Callable[..., Any]
    requires_approval: bool = False
    category: str = "general"


class ToolRegistry:
    """
    MuhammedAI Local Developer araç kayıt sistemi.

    Araçları:
    - keşfeder
    - AI'ya tanıtır
    - çalıştırır
    - onay gerektiren işlemleri engeller
    """

    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}

        self.scanner = ProjectScanner()
        self.structure_analyzer = ProjectStructureAnalyzer()
        self.searcher = CodeSearch()
        self.reader = FileReader()
        self.error_detector = ErrorDetector()
        self.python_runner = PythonRunner()
        self.workflow = ChangeWorkflow()
        self.codebase_index = CodebaseIndex()
        self.web_detector = WebProjectDetector()
        self.dev_server_manager = DevServerManager()
        self.http_inspector = HttpInspector()
        self.web_preview = WebPreview()
        self.browser_engine = BrowserEngine()
        self.browser_manager = BrowserManager()
        self.browser_inspector = BrowserInspector(self.browser_manager)
        self.browser_actions = BrowserActions(self.browser_manager)
        self.terminal_executor = TerminalExecutor()

        self._register_default_tools()

    # ---------------------------------------------------------
    # Registry
    # ---------------------------------------------------------

    def register(
        self,
        name: str,
        description: str,
        handler: Callable[..., Any],
        requires_approval: bool = False,
        category: str = "general",
    ) -> None:

        if not name:
            raise ValueError("Araç adı boş olamaz.")

        if not callable(handler):
            raise TypeError(
                f"'{name}' aracı için handler callable olmalıdır."
            )

        self.tools[name] = ToolDefinition(
            name=name,
            description=description,
            handler=handler,
            requires_approval=requires_approval,
            category=category,
        )

    # ---------------------------------------------------------
    # Tool kayıtları
    # ---------------------------------------------------------

    def _register_default_tools(self) -> None:

        # -----------------------------------------------------
        # PROJECT
        # -----------------------------------------------------

        self.register(
            name="project_scan",
            description="Projeyi tara ve desteklenen dosyaları listele.",
            handler=self.scanner.scan,
            requires_approval=False,
            category="project",
        )

        self.register(
            name="project_tree",
            description="Projenin dosya ağacını oluştur.",
            handler=self.scanner.get_tree,
            requires_approval=False,
            category="project",
        )

        self.register(
            name="project_structure",
            description="Python dosyalarının gerçek sınıf, fonksiyon ve import yapısını analiz et.",
            handler=self._project_structure,
            requires_approval=False,
            category="project",
        )

        # -----------------------------------------------------
        # SEARCH
        # -----------------------------------------------------

        self.register(
            name="search_code",
            description="Proje içerisindeki kodlarda metin ara.",
            handler=self.search_code,
            requires_approval=False,
            category="search",
        )

        # -----------------------------------------------------
        # FILE
        # -----------------------------------------------------

        self.register(
            name="read_file",
            description="Proje içerisindeki güvenli bir metin dosyasını oku.",
            handler=self.reader.read,
            requires_approval=False,
            category="file",
        )

        # -----------------------------------------------------
        # ANALYSIS
        # -----------------------------------------------------

        self.register(
            name="detect_errors",
            description="Python dosyalarında syntax hatalarını tespit et.",
            handler=self._detect_errors,
            requires_approval=False,
            category="analysis",
        )

        # -----------------------------------------------------
        # PYTHON
        # -----------------------------------------------------

        self.register(
            name="run_python_file",
            description="Proje içerisindeki Python dosyasını çalıştır.",
            handler=self.python_runner.run_file,
            requires_approval=True,
            category="python",
        )

        # -----------------------------------------------------
        # TERMINAL
        # -----------------------------------------------------

        self.register(
            name="execute_terminal_command",
            description="Terminal komutu çalıştır. Parametre: 'command' (komut string'i). Örnek: command='git status'. [KULLANICI ONAYI GEREKLİ]",
            handler=self._execute_terminal_command,
            requires_approval=True,
            category="terminal",
        )

        # -----------------------------------------------------
        # CHANGE PLANNING
        # -----------------------------------------------------

        self.register(
            name="create_change_plan",
            description="Güvenli değişiklik planı oluştur. İki parametre: 'file_path' (değiştirilecek dosya yolu, forward slash kullanın) ve 'problem' (sorun açıklaması). Örnek: file_path='quality_tests/test_workspace/file.py', problem='Change function return value'.",
            handler=self.workflow.create_plan,
            requires_approval=False,
            category="coding",
        )

        # -----------------------------------------------------
        # CHANGE APPLICATION
        # -----------------------------------------------------

        self.register(
            name="apply_change",
            description="Onaylanmış değişiklik planını uygula, syntax kontrolü ve testi çalıştır.",
            handler=self.workflow.apply_change,
            requires_approval=True,
            category="coding",
        )

        # -----------------------------------------------------
        # CODEBASE INTELLIGENCE
        # -----------------------------------------------------

        self.register(
            name="search_code_symbols",
            description="Proje içinde class, function, method gibi sembolleri ara.",
            handler=self._search_code_symbols,
            requires_approval=False,
            category="codebase",
        )

        self.register(
            name="get_symbol_details",
            description="Bir sembolün detaylı bilgilerini al (dosya, satır, signature, decorators).",
            handler=self._get_symbol_details,
            requires_approval=False,
            category="codebase",
        )

        self.register(
            name="find_related_files",
            description="Bir dosyaya ilişkili dosyaları bul (import, reverse import, test dosyaları).",
            handler=self._find_related_files,
            requires_approval=False,
            category="codebase",
        )

        self.register(
            name="get_file_dependencies",
            description="Bir dosyanın import ettiği modülleri/dosyaları listele.",
            handler=self._get_file_dependencies,
            requires_approval=False,
            category="codebase",
        )

        self.register(
            name="find_dependents",
            description="Bir dosyayı hangi dosyaların import ettiğini bul.",
            handler=self._find_dependents,
            requires_approval=False,
            category="codebase",
        )

        # -----------------------------------------------------
        # WEB DEVELOPMENT
        # -----------------------------------------------------

        self.register(
            name="detect_web_project",
            description="Projenin web projesi olup olmadığını tespit et (framework, package manager, start command).",
            handler=self._detect_web_project,
            requires_approval=False,
            category="web",
        )

        self.register(
            name="start_web_preview",
            description="Web development server'ı başlat ve health check yap. [KULLANICI ONAYI GEREKLİ]",
            handler=self._start_web_preview,
            requires_approval=True,
            category="web",
        )

        self.register(
            name="stop_web_preview",
            description="Web development server'ı durdur. [KULLANICI ONAYI GEREKLİ]",
            handler=self._stop_web_preview,
            requires_approval=True,
            category="web",
        )

        self.register(
            name="inspect_http",
            description="HTTP isteği yap ve response analiz et (status, headers, body).",
            handler=self._inspect_http,
            requires_approval=False,
            category="web",
        )

        self.register(
            name="check_web_health",
            description="Web server health check yap.",
            handler=self._check_web_health,
            requires_approval=False,
            category="web",
        )

        # -----------------------------------------------------
        # BROWSER AUTOMATION
        # -----------------------------------------------------

        self.register(
            name="browser_status",
            description="Browser engine status ve hazır olup olmadığını kontrol et.",
            handler=self._browser_status,
            requires_approval=False,
            category="browser",
        )

        self.register(
            name="browser_open",
            description="Browser başlat. [KULLANICI ONAYI GEREKLİ]",
            handler=self._browser_open,
            requires_approval=True,
            category="browser",
        )

        self.register(
            name="browser_close",
            description="Browser kapat. [KULLANICI ONAYI GEREKLİ]",
            handler=self._browser_close,
            requires_approval=True,
            category="browser",
        )

        self.register(
            name="browser_navigate",
            description="Browser ile URL'e git (localhost only). [KULLANICI ONAYI GEREKLİ]",
            handler=self._browser_navigate,
            requires_approval=True,
            category="browser",
        )

        self.register(
            name="browser_inspect",
            description="Sayfa DOM bilgilerini incele (title, buttons, links, inputs vb.).",
            handler=self._browser_inspect,
            requires_approval=False,
            category="browser",
        )

        self.register(
            name="browser_screenshot",
            description="Sayfa screenshot al.",
            handler=self._browser_screenshot,
            requires_approval=False,
            category="browser",
        )

        self.register(
            name="browser_click",
            description="Elemente tıkla. [KULLANICI ONAYI GEREKLİ]",
            handler=self._browser_click,
            requires_approval=True,
            category="browser",
        )

        self.register(
            name="browser_type",
            description="Elemente metin yaz. [KULLANICI ONAYI GEREKLİ]",
            handler=self._browser_type,
            requires_approval=True,
            category="browser",
        )

        self.register(
            name="browser_fill",
            description="Elementi doldur. [KULLANICI ONAYI GEREKLİ]",
            handler=self._browser_fill,
            requires_approval=True,
            category="browser",
        )

        self.register(
            name="browser_select",
            description="Select option seç. [KULLANICI ONAYI GEREKLİ]",
            handler=self._browser_select,
            requires_approval=True,
            category="browser",
        )

        self.register(
            name="browser_scroll",
            description="Sayfayı scroll et.",
            handler=self._browser_scroll,
            requires_approval=False,
            category="browser",
        )

        self.register(
            name="browser_reload",
            description="Sayfayı yenile.",
            handler=self._browser_reload,
            requires_approval=False,
            category="browser",
        )

        self.register(
            name="browser_get_errors",
            description="Console, page ve network hatalarını al.",
            handler=self._browser_get_errors,
            requires_approval=False,
            category="browser",
        )

    # ---------------------------------------------------------
    # Wrapper methods
    # ---------------------------------------------------------

    def search_code(
        self,
        query: str,
        max_results: int = 30,
    ) -> Dict[str, Any]:

        results = self.searcher.search(
            query=query,
            max_results=max_results,
        )

        return {
            "results": results,
            "formatted": self.searcher.format_results(results),
        }

    def _project_structure(self) -> Dict[str, Any]:

        results = self.structure_analyzer.analyze()

        return {
            "results": results,
            "formatted": self.structure_analyzer.format_results(results),
        }

    def _detect_errors(self) -> Dict[str, Any]:

        errors = self.error_detector.scan_python_files()

        return {
            "errors": errors,
            "formatted": self.error_detector.format_errors(errors),
        }

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def get(self, name: str) -> Optional[ToolDefinition]:
        return self.tools.get(name)

    def has(self, name: str) -> bool:
        return name in self.tools

    def list_tools(self) -> list:
        return list(self.tools.keys())

    # ---------------------------------------------------------
    # Tool information
    # ---------------------------------------------------------

    def get_tool_info(
        self,
        name: str,
    ) -> Optional[Dict[str, Any]]:

        tool = self.get(name)

        if tool is None:
            return None

        return {
            "name": tool.name,
            "description": tool.description,
            "requires_approval": tool.requires_approval,
            "category": tool.category,
        }

    def get_tool_schema(
        self,
        name: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Tool için detaylı şema bilgisi döndürür.
        AI'nın doğru parametreleri kullanması için.

        Returns:
            Dict with: name, description, parameters, example_call, requires_approval
        """

        tool = self.get(name)

        if tool is None:
            return None

        # Tool handler'ın gerçek parametrelerini belirle
        schemas = {
            "project_scan": {
                "parameters": [],
                "example_call": '{"tool": "project_scan", "arguments": {}}',
            },
            "project_tree": {
                "parameters": [],
                "example_call": '{"tool": "project_tree", "arguments": {}}',
            },
            "project_structure": {
                "parameters": [],
                "example_call": '{"tool": "project_structure", "arguments": {}}',
            },
            "search_code": {
                "parameters": [
                    {"name": "query", "type": "str", "required": True, "description": "Aranacak metin"},
                    {"name": "max_results", "type": "int", "required": False, "default": 30, "description": "Maksimum sonuç sayısı"},
                ],
                "example_call": '{"tool": "search_code", "arguments": {"query": "AgentExecutor"}}',
            },
            "read_file": {
                "parameters": [
                    {"name": "relative_path", "type": "str", "required": True, "description": "Dosya yolu (proje köküne göre)"},
                    {"name": "offset", "type": "int", "required": False, "default": 0, "description": "Başlangıç satırı (0-indexed)"},
                    {"name": "limit", "type": "int", "required": False, "default": None, "description": "Maksimum satır sayısı (None = tüm dosya)"},
                ],
                "example_call": '{"tool": "read_file", "arguments": {"relative_path": "app/core/config.py"}}',
            },
            "detect_errors": {
                "parameters": [],
                "example_call": '{"tool": "detect_errors", "arguments": {}}',
            },
            "run_python_file": {
                "parameters": [
                    {"name": "file_path", "type": "str", "required": True, "description": "Çalıştırılacak dosya yolu"},
                    {"name": "timeout", "type": "int", "required": False, "default": 30, "description": "Maksimum çalışma süresi (saniye)"},
                ],
                "example_call": '{"tool": "run_python_file", "arguments": {"file_path": "app/tools/tool_registry.py"}}',
            },
            "execute_terminal_command": {
                "parameters": [
                    {"name": "command", "type": "str", "required": True, "description": "Terminal komutu (örn: git status)"},
                    {"name": "timeout", "type": "int", "required": False, "default": 30, "description": "Maksimum çalışma süresi (saniye)"},
                ],
                "example_call": '{"tool": "execute_terminal_command", "arguments": {"command": "git status"}}',
            },
            "create_change_plan": {
                "parameters": [
                    {"name": "file_path", "type": "str", "required": True, "description": "Değiştirilecek dosya (proje köküne göre relative path, forward slash kullanın)"},
                    {"name": "problem", "type": "str", "required": True, "description": "Sorun açıklaması"},
                ],
                "example_call": '{"tool": "create_change_plan", "arguments": {"file_path": "quality_tests/test_workspace/agent_task.py", "problem": "Change return value to Merhaba Muhammed"}}',
            },
            "apply_change": {
                "parameters": [
                    {"name": "plan", "type": "dict", "required": True, "description": "Değişiklik planı (create_change_plan'dan gelen)"},
                    {"name": "test_file", "type": "str", "required": True, "description": "Test dosyası yolu"},
                    {"name": "approved", "type": "bool", "required": False, "default": False, "description": "Kullanıcı onayı"},
                ],
                "example_call": '{"tool": "apply_change", "arguments": {"plan": {...}, "test_file": "tests/test_config.py", "approved": true}}',
            },
        }

        schema = schemas.get(name, {"parameters": [], "example_call": f'{{"tool": "{name}", "arguments": {{}}}}'})

        return {
            "name": tool.name,
            "description": tool.description,
            "requires_approval": tool.requires_approval,
            "category": tool.category,
            "parameters": schema["parameters"],
            "example_call": schema["example_call"],
        }

    def get_all_tool_info(self) -> list:

        return [
            self.get_tool_info(name)
            for name in self.tools
        ]

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def _search_code_symbols(
        self,
        query: str,
        max_results: int = 30,
    ) -> Dict[str, Any]:
        """Sembol ara."""
        self.codebase_index.index_project()
        symbols = self.codebase_index.search_symbols(query)

        results = []
        for symbol in symbols[:max_results]:
            results.append({
                "name": symbol.name,
                "type": symbol.type,
                "file": symbol.file,
                "line_start": symbol.line_start,
                "line_end": symbol.line_end,
                "signature": symbol.signature,
                "parent_class": symbol.parent_class,
            })

        return {
            "query": query,
            "count": len(results),
            "symbols": results,
        }

    def _get_symbol_details(
        self,
        symbol_name: str,
        file_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Sembol detaylarını al."""
        self.codebase_index.index_project()
        symbol = self.codebase_index.get_symbol_details(symbol_name, file_path)

        if not symbol:
            return {
                "error": f"Symbol not found: {symbol_name}",
                "symbol_name": symbol_name,
                "file_path": file_path,
            }

        return {
            "name": symbol.name,
            "type": symbol.type,
            "file": symbol.file,
            "line_start": symbol.line_start,
            "line_end": symbol.line_end,
            "signature": symbol.signature,
            "parent_class": symbol.parent_class,
            "decorators": symbol.decorators,
            "docstring": symbol.docstring,
        }

    def _find_related_files(
        self,
        file_path: str,
        max_results: int = 10,
    ) -> Dict[str, Any]:
        """İlgili dosyaları bul."""
        self.codebase_index.index_project()
        related = self.codebase_index.find_related_files(file_path, max_results)

        return {
            "file_path": file_path,
            "related_files": related,
        }

    def _get_file_dependencies(
        self,
        file_path: str,
    ) -> Dict[str, Any]:
        """Dosya bağımlılıklarını al."""
        self.codebase_index.index_project()
        deps = self.codebase_index.get_file_dependencies(file_path)

        return {
            "file_path": file_path,
            "dependencies": list(deps),
        }

    def _find_dependents(
        self,
        file_path: str,
    ) -> Dict[str, Any]:
        """Dependents'ı bul."""
        self.codebase_index.index_project()
        dependents = self.codebase_index.get_dependents(file_path)

        return {
            "file_path": file_path,
            "imported_by": list(dependents),
        }

    def _detect_web_project(self) -> Dict[str, Any]:
        """Web projesi tespit et."""
        info = self.web_detector.detect()

        return {
            "is_web_project": info.is_web_project,
            "framework": info.framework,
            "package_manager": info.package_manager,
            "start_command": info.start_command,
            "likely_port": info.likely_port,
            "entrypoint": info.entrypoint,
            "confidence": info.confidence,
        }

    def _start_web_preview(self, dry_run: bool = False) -> Dict[str, Any]:
        """Web preview başlat."""
        result = self.web_preview.start_preview(dry_run=dry_run)

        return {
            "status": result.status,
            "url": result.url,
            "port": result.port,
            "framework": result.framework,
            "health": result.health,
            "server_pid": result.server_pid,
            "error": result.error,
        }

    def _stop_web_preview(self) -> Dict[str, Any]:
        """Web preview durdur."""
        success = self.web_preview.stop_preview()

        return {
            "success": success,
        }

    def _inspect_http(self, url: str, method: str = "GET") -> Dict[str, Any]:
        """HTTP inspection."""
        if method.upper() == "GET":
            response = self.http_inspector.get(url)
        elif method.upper() == "HEAD":
            response = self.http_inspector.head(url)
        else:
            return {
                "error": f"Unsupported method: {method}",
            }

        return {
            "status_code": response.status_code,
            "headers": response.headers,
            "content_type": response.content_type,
            "content_length": response.content_length,
            "body": response.body,
            "response_time": response.response_time,
            "final_url": response.final_url,
            "success": response.success,
            "error": response.error,
        }

    def _check_web_health(self, url: str) -> Dict[str, Any]:
        """Web health check."""
        return self.web_preview.health_check()

    def _browser_status(self) -> Dict[str, Any]:
        """Browser status."""
        return self.browser_manager.get_status()

    def _browser_open(self, headless: bool = True) -> Dict[str, Any]:
        """Browser aç."""
        info = self.browser_manager.launch(headless)

        return {
            "state": info.state.value,
            "error": info.error,
        }

    def _browser_close(self) -> Dict[str, Any]:
        """Browser kapat."""
        success = self.browser_manager.close()

        return {
            "success": success,
        }

    def _browser_navigate(self, url: str, allow_external: bool = False) -> Dict[str, Any]:
        """Browser navigate."""
        info = self.browser_manager.navigate(url, allow_external)

        return {
            "state": info.state.value,
            "url": info.url,
            "title": info.title,
            "error": info.error,
        }

    def _browser_inspect(self) -> Dict[str, Any]:
        """Browser inspect."""
        page_info = self.browser_inspector.inspect_page()

        return {
            "url": page_info.url,
            "title": page_info.title,
            "headings_count": len(page_info.headings),
            "links_count": len(page_info.links),
            "buttons_count": len(page_info.buttons),
            "inputs_count": len(page_info.inputs),
            "forms_count": len(page_info.forms),
            "error": page_info.error,
        }

    def _browser_screenshot(self, path: Optional[str] = None) -> Dict[str, Any]:
        """Browser screenshot."""
        info = self.browser_manager.screenshot(path)

        return {
            "success": info.error is None,
            "path": info.screenshot_path,
            "error": info.error,
        }

    def _browser_click(self, selector: str) -> Dict[str, Any]:
        """Browser click."""
        result = self.browser_actions.click(selector)

        return {
            "success": result.success,
            "selector": result.selector,
            "error": result.error,
            "url_changed": result.url_changed,
            "new_url": result.new_url,
        }

    def _browser_type(self, selector: str, text: str, sensitive: bool = False) -> Dict[str, Any]:
        """Browser type."""
        result = self.browser_actions.type(selector, text, sensitive)

        return {
            "success": result.success,
            "selector": result.selector,
            "error": result.error,
        }

    def _browser_fill(self, selector: str, value: str, sensitive: bool = False) -> Dict[str, Any]:
        """Browser fill."""
        result = self.browser_actions.fill(selector, value, sensitive)

        return {
            "success": result.success,
            "selector": result.selector,
            "error": result.error,
        }

    def _browser_select(self, selector: str, value: str) -> Dict[str, Any]:
        """Browser select."""
        result = self.browser_actions.select(selector, value)

        return {
            "success": result.success,
            "selector": result.selector,
            "error": result.error,
        }

    def _browser_scroll(self, direction: str = "down", amount: int = 500) -> Dict[str, Any]:
        """Browser scroll."""
        result = self.browser_actions.scroll(direction, amount)

        return {
            "success": result.success,
            "direction": result.selector,
            "error": result.error,
        }

    def _browser_reload(self) -> Dict[str, Any]:
        """Browser reload."""
        info = self.browser_manager.reload()

        return {
            "state": info.state.value,
            "url": info.url,
            "title": info.title,
            "error": info.error,
        }

    def _browser_get_errors(self) -> Dict[str, Any]:
        """Browser errors."""
        status = self.browser_manager.get_status()

        return {
            "console_errors_count": status["console_errors_count"],
            "page_errors_count": status["page_errors_count"],
            "network_errors_count": status["network_errors_count"],
        }

    def _execute_terminal_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Terminal komutu çalıştır."""
        from app.tools.terminal_executor import TerminalCommand
        
        cmd = TerminalCommand(
            command=command,
            shell="powershell",
            timeout=timeout
        )
        
        result = self.terminal_executor.execute(cmd)
        
        return {
            "command": result.command,
            "exit_code": result.exit_code,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration": result.duration,
            "success": result.success,
            "error": result.error,
            "risk_level": result.risk_level.value if result.risk_level else None,
            "approval_required": result.approval_required,
        }

    def execute(
        self,
        name: str,
        arguments: Optional[Dict[str, Any]] = None,
        approved: bool = False,
    ) -> Dict[str, Any]:

        arguments = arguments or {}

        tool = self.get(name)

        if tool is None:
            return {
                "success": False,
                "tool": name,
                "error": f"Bilinmeyen araç: {name}",
            }

        if tool.requires_approval and not approved:
            return {
                "success": False,
                "tool": name,
                "requires_approval": True,
                "error": (
                    "Bu araç için kullanıcı onayı gerekiyor."
                ),
            }

        try:
            result = tool.handler(**arguments)

            return {
                "success": True,
                "tool": name,
                "result": result,
            }

        except Exception as exc:

            return {
                "success": False,
                "tool": name,
                "error": str(exc),
            }

    # ---------------------------------------------------------
    # AI prompt
    # ---------------------------------------------------------

    def get_tools_for_prompt(self) -> str:

        lines = [
            "KULLANILABİLİR ARAÇLAR:",
            "",
        ]

        for tool in self.tools.values():

            approval = (
                " [KULLANICI ONAYI GEREKLİ]"
                if tool.requires_approval
                else ""
            )

            lines.append(
                f"- {tool.name}: "
                f"{tool.description}"
                f"{approval}"
            )

        return "\n".join(lines)

    def get_detailed_tools_for_prompt(self) -> str:
        """
        AI için detaylı tool şema bilgisi döndürür.
        Her tool için parametre bilgisi ve örnek çağrı içerir.
        """

        lines = [
            "KULLANILABİLİR ARAÇLAR VE PARAMETRELER:",
            "",
        ]

        for tool_name in sorted(self.tools.keys()):
            schema = self.get_tool_schema(tool_name)

            if schema is None:
                continue

            approval = (
                " [KULLANICI ONAYI GEREKLİ]"
                if schema["requires_approval"]
                else ""
            )

            lines.append(f"## {schema['name']}{approval}")
            lines.append(f"Açıklama: {schema['description']}")

            if schema["parameters"]:
                lines.append("Parametreler:")
                for param in schema["parameters"]:
                    required_str = "ZORUNLU" if param["required"] else "OPSİYONEL"
                    default_str = f" (varsayılan: {param['default']})" if "default" in param else ""
                    lines.append(
                        f"  - {param['name']} ({param['type']}) [{required_str}]{default_str}: {param['description']}"
                    )
            else:
                lines.append("Parametreler: Yok (boş arguments kullanın)")

            lines.append(f"Örnek çağrı: {schema['example_call']}")
            lines.append("")

        return "\n".join(lines)

    def get_ollama_tools(self) -> list:
        """
        Ollama API için tool tanımlarını döndürür.
        
        Returns:
            list: Ollama formatında tool tanımları
        """
        ollama_tools = []
        
        for tool_name, tool in self.tools.items():
            schema = self.get_tool_schema(tool_name)
            if schema is None:
                continue
            
            # Ollama formatına çevir
            properties = {}
            required = []
            
            for param in schema.get("parameters", []):
                param_name = param["name"]
                param_type = param["type"]
                
                # Type mapping
                type_map = {
                    "str": "string",
                    "int": "integer",
                    "bool": "boolean",
                    "dict": "object",
                    "list": "array"
                }
                
                json_type = type_map.get(param_type, "string")
                
                properties[param_name] = {
                    "type": json_type,
                    "description": param.get("description", "")
                }
                
                if param.get("required", False):
                    required.append(param_name)
            
            ollama_tool = {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": schema.get("description", ""),
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": required
                    }
                }
            }
            
            ollama_tools.append(ollama_tool)
        
        return ollama_tools


if __name__ == "__main__":

    registry = ToolRegistry()

    print("=" * 60)
    print("MuhammedAI Local Developer - Tool Registry")
    print("=" * 60)

    print("\nKayıtlı araçlar:")

    for tool in registry.get_all_tool_info():

        print(
            f"- {tool['name']} "
            f"[{tool['category']}] "
            f"approval={tool['requires_approval']}"
        )

    print("\nToplam araç:", len(registry.tools))

    print("\nAI araç listesi:")
    print(registry.get_tools_for_prompt())
