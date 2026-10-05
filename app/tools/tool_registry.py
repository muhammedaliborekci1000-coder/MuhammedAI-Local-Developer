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
        # CHANGE PLANNING
        # -----------------------------------------------------

        self.register(
            name="create_change_plan",
            description="Güvenli değişiklik planı oluştur; kullanıcı onayından sonra uygulama ve doğrulama orkestratör üzerinden yürütülür. ÖNEMLİ: file_path parametresinde mutlaka forward slash (/) kullanın, backslash kullanmayın. Dosya yollarında asla boşluk kullanmayın. Directory ve dosya isimlerini tam ve doğru yazın, kısaltma veya typo yapmayın. Örnek: 'quality_tests/e2e_workspace/agent_task.py'",
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
            "create_change_plan": {
                "parameters": [
                    {"name": "file_path", "type": "str", "required": True, "description": "Değiştirilecek dosya"},
                    {"name": "problem", "type": "str", "required": True, "description": "Sorun açıklaması"},
                    {"name": "test_file", "type": "str", "required": False, "description": "Test dosyası yolu (opsiyonel)"},
                ],
                "example_call": '{"tool": "create_change_plan", "arguments": {"file_path": "app/core/config.py", "problem": "Add new config", "test_file": "tests/test_config.py"}}',
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
