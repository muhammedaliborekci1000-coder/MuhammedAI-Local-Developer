from app.ai.ollama_client import OllamaClient
from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.tool_parser import ToolCall

from app.tools.file_reader import FileReader
from app.tools.code_search import CodeSearch
from app.tools.project_scanner import ProjectScanner
from app.tools.project_structure_analyzer import ProjectStructureAnalyzer
from app.tools.error_detector import ErrorDetector
from app.tools.python_runner import PythonRunner
from app.tools.change_workflow import ChangeWorkflow
from app.tools.tool_registry import ToolRegistry


class DeveloperAgent:

    def __init__(self, approval_callback=None):
        self.ai = OllamaClient()

        self.reader = FileReader()
        self.searcher = CodeSearch()
        self.scanner = ProjectScanner()
        self.structure_analyzer = ProjectStructureAnalyzer()
        self.error_detector = ErrorDetector()
        self.runner = PythonRunner()

        self.workflow = ChangeWorkflow()

        # AgentLoop için ToolRegistry
        self.registry = ToolRegistry()

        # AgentLoop (onay callback ile)
        self.loop_config = LoopConfig(max_iterations=10, enable_logging=True)
        self.agent_loop = AgentLoop(
            ollama_client=self.ai,
            tool_registry=self.registry,
            config=self.loop_config,
            approval_callback=approval_callback
        )

    def analyze_file(
        self,
        file_path: str,
    ) -> str:

        content = self.reader.read(file_path)

        prompt = (
            "Sen MuhammedAI Local Developer adlı yerel "
            "yazılım geliştirme asistanısın.\n\n"

            "Aşağıdaki Python dosyasını analiz et.\n\n"

            f"DOSYA: {file_path}\n\n"

            "DOSYA ICERIGI:\n"
            "```python\n"
            f"{content}\n"
            "```\n\n"

            "Şunları açıkla:\n"
            "1. Bu dosyanın amacı nedir?\n"
            "2. Hangi sınıflar ve fonksiyonlar var?\n"
            "3. Hangi modüllere bağımlı?\n"
            "4. Olası hata veya riskler var mı?\n"
            "5. Kodun genel yapısı nasıl?\n"
            "6. İyileştirme önerilerin neler?\n\n"

            "Kodda değişiklik yapma. "
            "Sadece analiz yap."
        )

        return self.ai.chat(prompt)

    def search_code(
        self,
        query: str,
    ) -> str:

        results = self.searcher.search(query)

        formatted = self.searcher.format_results(
            results
        )

        prompt = (
            "Sen MuhammedAI Local Developer'sın.\n\n"

            f"Kullanıcı şu ifadeyi arıyor: {query}\n\n"

            "Arama sonuçları:\n"
            f"{formatted}\n\n"

            "Sonuçları analiz et.\n"
            "Hangi dosyalarda bulunduğunu ve "
            "kullanım amacını açıkla.\n"

            "Sadece verilen sonuçlara dayan."
        )

        return self.ai.chat(prompt)

    def project_overview(self) -> str:

        tree = self.scanner.get_tree()

        structure_results = (
            self.structure_analyzer.analyze()
        )

        structure = (
            self.structure_analyzer.format_results(
                structure_results
            )
        )

        lines = []

        lines.append("=" * 60)
        lines.append("MUHAMMEDAI PROJE YAPISAL ANALİZİ")
        lines.append("=" * 60)
        lines.append("")

        lines.append("1. PROJE KÖKÜ")
        lines.append(
            str(self.scanner.project_root)
        )
        lines.append("")

        lines.append("2. TOPLAM DESTEKLENEN DOSYA")
        lines.append(
            str(len(self.scanner.scan()))
        )
        lines.append("")

        lines.append("3. PYTHON DOSYASI")
        lines.append(
            str(len(structure_results))
        )
        lines.append("")

        lines.append("4. DOSYA AĞACI")
        lines.append(tree)
        lines.append("")

        lines.append("5. GERÇEK PYTHON YAPISI")
        lines.append(structure)
        lines.append("")

        lines.append("6. ANALİZ NOTU")
        lines.append(
            "Yukarıdaki sınıf, fonksiyon ve import bilgileri "
            "Python AST analizi ile doğrudan kaynak kodundan "
            "çıkarılmıştır."
        )
        lines.append(
            "Bu nedenle dosya adından yapılan tahmin değildir."
        )

        return "\n".join(lines)

    def detect_errors(self) -> str:

        errors = (
            self.error_detector.scan_python_files()
        )

        formatted = (
            self.error_detector.format_errors(
                errors
            )
        )

        prompt = (
            "Sen MuhammedAI Local Developer'sın.\n\n"

            "Python projesinin syntax kontrol sonucu:\n\n"

            f"{formatted}\n\n"

            "Sonuçları analiz et.\n"
            "Hata yoksa açıkça belirt.\n"
            "Hata varsa dosya, satır, neden ve "
            "çözüm önerisini belirt.\n\n"

            "Dosyalarda değişiklik yapma."
        )

        return self.ai.chat(prompt)

    def run_and_analyze(
        self,
        file_path: str,
    ) -> str:

        result = self.runner.run_file(
            file_path
        )

        source_code = self.reader.read(
            file_path
        )

        prompt = (
            "Sen deneyimli bir Python debugging "
            "uzmanısın.\n\n"

            "Görevin, aşağıdaki Python programındaki "
            "gerçek problemi kaynak kodu ve çalışma "
            "sonucu üzerinden tespit etmektir.\n\n"

            f"DOSYA:\n{file_path}\n\n"

            "KAYNAK KODU:\n"
            "```python\n"
            f"{source_code}\n"
            "```\n\n"

            "PROGRAM ÇALIŞTIRMA SONUCU:\n"
            "```text\n"
            f"{result}\n"
            "```\n\n"

            "ANALİZ KURALLARI:\n"
            "1. Gerçek returncode değerini değerlendir.\n"
            "2. STDOUT ve STDERR sonuçlarını değerlendir.\n"
            "3. Kaynak kodundaki problemi bul.\n"
            "4. Sorunlu satırı açıkça belirt.\n"
            "5. Testlerin gerçekten başarılı olup "
            "olmadığını returncode değerine göre belirle.\n"
            "6. Tahmin yapma.\n"
            "7. Kanıtlanamayan bilgileri kesin gerçek "
            "olarak söyleme.\n\n"

            "SONUÇ FORMATı:\n"
            "GERÇEK DURUM:\n"
            "...\n\n"

            "SORUNLU SATIR:\n"
            "...\n\n"

            "SORUNUN NEDENİ:\n"
            "...\n\n"

            "ÖNERİLEN DÜZELTME:\n"
            "...\n\n"

            "Hiçbir dosyayı değiştirme."
        )

        return self.ai.chat(prompt)

    def create_change_plan(
        self,
        file_path: str,
        problem: str,
    ) -> dict:

        return self.workflow.create_plan(
            file_path,
            problem,
        )

    def apply_change(
        self,
        plan: dict,
        test_file: str,
        approved: bool = False,
    ) -> dict:

        return self.workflow.apply_change(
            plan=plan,
            test_file=test_file,
            approved=approved,
        )

    def run_task(self, task: str):
        """
        AgentLoop kullanarak çok adımlı görev çalıştırır.

        Args:
            task: Kullanıcı görevi
        
        Returns:
            LoopResult: Görev sonucu
        """
        return self.agent_loop.run(task)

    def get_tool_call_log(self):
        """Tool çağrı logunu döndürür."""
        return self.agent_loop.get_tool_call_log()

    def get_conversation_history(self):
        """Konuşma geçmişini döndürür."""
        return self.agent_loop.get_conversation_history()
