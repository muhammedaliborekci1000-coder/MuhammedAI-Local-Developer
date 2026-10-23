"""
MuhammedAI Local Developer - Diff Exporter
Diff exporter engine for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
import json


class ExportFormat(Enum):
    """Export format."""
    TEXT = "text"
    HTML = "html"
    MARKDOWN = "markdown"
    JSON = "json"
    PDF = "pdf"
    PATCH = "patch"
    UNIFIED = "unified"
    SIDE_BY_SIDE = "side_by_side"


class ExportScope(Enum):
    """Export scope."""
    ALL_FILES = "all_files"
    CURRENT_FILE = "current_file"
    SELECTED_HUNKS = "selected_hunks"
    SELECTED_LINES = "selected_lines"
    VISIBLE_AREA = "visible_area"


class ExportAction(Enum):
    """Export action."""
    EXPORT = "export"
    EXPORT_AS = "export_as"
    EXPORT_TO_FILE = "export_to_file"
    EXPORT_TO_CLIPBOARD = "export_to_clipboard"
    EXPORT_TO_EMAIL = "export_to_email"
    PRINT = "print"


@dataclass
class ExportOptions:
    """Export options."""
    include_line_numbers: bool = True
    include_context: bool = True
    include_headers: bool = True
    include_statistics: bool = False
    include_timestamp: bool = True
    include_author: bool = False
    include_commit_info: bool = False
    colorize: bool = False
    wrap_lines: bool = False
    max_line_length: int = 120


@dataclass
class ExportResult:
    """Export result."""
    success: bool
    action: Optional[str] = None
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    exported_content: Optional[str] = None
    file_path: Optional[str] = None
    format: Optional[str] = None
    total_files: int = 0
    total_lines: int = 0


@dataclass
class ExportConfig:
    """Export configuration."""
    format: ExportFormat = ExportFormat.TEXT
    scope: ExportScope = ExportScope.ALL_FILES
    options: ExportOptions = field(default_factory=ExportOptions)
    output_path: Optional[str] = None


class DiffExporterEngine:
    """
    Diff exporter engine.
    
    Özellikler:
    - Export to text
    - Export to HTML
    - Export to Markdown
    - Export to JSON
    - Export to patch
    - Export to unified diff
    - Export to side-by-side diff
    - Export to file
    - Export to clipboard
    - Export options
    - Export scope
    - Line numbers
    - Context display
    - Headers
    - Statistics
    - Timestamp
    - Author info
    - Commit info
    - Colorization
    - Line wrapping
    - Export history
    - Configuration management
    """
    
    def __init__(self, config: Optional[ExportConfig] = None):
        """Initialize diff exporter engine."""
        self.config = config or ExportConfig()
        self.export_history: List[Tuple[str, str]] = []  # (action, target)
        self.diff_content: List[str] = []
        self.file_paths: List[str] = []
    
    def export(
        self,
        diff_content: Optional[List[str]] = None,
        file_paths: Optional[List[str]] = None
    ) -> ExportResult:
        """
        Dışa aktar.
        
        Args:
            diff_content: Diff içeriği
            file_paths: Dosya yolları
            
        Returns:
            ExportResult: Dışa aktarma sonucu
        """
        result = ExportResult(success=False)
        result.action = ExportAction.EXPORT.value
        
        try:
            if diff_content:
                self.diff_content = diff_content
            if file_paths:
                self.file_paths = file_paths
            
            if not self.diff_content:
                result.errors.append("No diff content to export")
                return result
            
            # Format'a göre dışa aktar
            if self.config.format == ExportFormat.TEXT:
                exported = self._export_text()
            elif self.config.format == ExportFormat.HTML:
                exported = self._export_html()
            elif self.config.format == ExportFormat.MARKDOWN:
                exported = self._export_markdown()
            elif self.config.format == ExportFormat.JSON:
                exported = self._export_json()
            elif self.config.format == ExportFormat.PATCH:
                exported = self._export_patch()
            elif self.config.format == ExportFormat.UNIFIED:
                exported = self._export_unified()
            elif self.config.format == ExportFormat.SIDE_BY_SIDE:
                exported = self._export_side_by_side()
            else:
                exported = "\n".join(self.diff_content)
            
            result.exported_content = exported
            result.format = self.config.format.value
            result.total_files = len(self.file_paths) if self.file_paths else 1
            result.total_lines = len(self.diff_content)
            result.success = True
            result.message = f"Exported to {self.config.format.value}"
            
            self.export_history.append(("export", self.config.format.value))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def export_as(
        self,
        format: ExportFormat,
        diff_content: Optional[List[str]] = None
    ) -> ExportResult:
        """
        Farklı formatta dışa aktar.
        
        Args:
            format: Dışa aktarma formatı
            diff_content: Diff içeriği
            
        Returns:
            ExportResult: Dışa aktarma sonucu
        """
        result = ExportResult(success=False)
        result.action = ExportAction.EXPORT_AS.value
        
        try:
            old_format = self.config.format
            self.config.format = format
            
            export_result = self.export(diff_content)
            
            if export_result.success:
                export_result.action = ExportAction.EXPORT_AS.value
            
            self.config.format = old_format
            return export_result
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def export_to_file(
        self,
        file_path: str,
        diff_content: Optional[List[str]] = None
    ) -> ExportResult:
        """
        Dosyaya dışa aktar.
        
        Args:
            file_path: Dosya yolu
            diff_content: Diff içeriği
            
        Returns:
            ExportResult: Dışa aktarma sonucu
        """
        result = ExportResult(success=False)
        result.action = ExportAction.EXPORT_TO_FILE.value
        
        try:
            export_result = self.export(diff_content)
            
            if not export_result.success:
                return export_result
            
            # Dosyaya yaz
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(export_result.exported_content)
            
            result.exported_content = export_result.exported_content
            result.file_path = file_path
            result.format = export_result.format
            result.total_files = export_result.total_files
            result.total_lines = export_result.total_lines
            result.success = True
            result.message = f"Exported to file: {file_path}"
            
            self.export_history.append(("export_to_file", file_path))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def export_to_clipboard(
        self,
        diff_content: Optional[List[str]] = None
    ) -> ExportResult:
        """
    Panoya dışa aktar.
        
        Args:
            diff_content: Diff içeriği
            
        Returns:
            ExportResult: Dışa aktarma sonucu
        """
        result = ExportResult(success=False)
        result.action = ExportAction.EXPORT_TO_CLIPBOARD.value
        
        try:
            export_result = self.export(diff_content)
            
            if not export_result.success:
                return export_result
            
            # Panoya kopyala (platform bağımsız)
            try:
                import pyperclip
                pyperclip.copy(export_result.exported_content)
                result.success = True
                result.message = "Exported to clipboard"
            except ImportError:
                result.errors.append("pyperclip not installed")
                return result
            
            result.exported_content = export_result.exported_content
            result.format = export_result.format
            result.total_files = export_result.total_files
            result.total_lines = export_result.total_lines
            
            self.export_history.append(("export_to_clipboard", "clipboard"))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_diff_content(self, diff_content: List[str], file_paths: Optional[List[str]] = None):
        """
        Diff içeriğini ayarla.
        
        Args:
            diff_content: Diff içeriği
            file_paths: Dosya yolları
        """
        self.diff_content = diff_content
        if file_paths:
            self.file_paths = file_paths
    
    def get_export_history(self) -> List[Tuple[str, str]]:
        """
        Dışa aktarma geçmişini al.
        
        Returns:
            List[Tuple[str, str]]: Geçmiş
        """
        return self.export_history
    
    def clear_history(self) -> ExportResult:
        """
        Geçmişi temizle.
        
        Returns:
            ExportResult: Temizleme sonucu
        """
        result = ExportResult(success=False)
        
        try:
            self.export_history.clear()
            result.success = True
            result.message = "Export history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        İstatistikleri al.
        
        Returns:
            Dict[str, Any]: İstatistikler
        """
        return {
            "total_lines": len(self.diff_content),
            "total_files": len(self.file_paths),
            "export_history_count": len(self.export_history),
            "current_format": self.config.format.value
        }
    
    def update_config(self, config: ExportConfig) -> ExportResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            ExportResult: Güncelleme sonucu
        """
        result = ExportResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> ExportConfig:
        """
        Konfigürasyon al.
        
        Returns:
            ExportConfig: Konfigürasyon
        """
        return self.config
    
    def _export_text(self) -> str:
        """Text formatında dışa aktar."""
        lines = []
        
        if self.config.options.include_headers:
            lines.append("=" * 70)
            lines.append("DIFF EXPORT")
            lines.append("=" * 70)
            if self.config.options.include_timestamp:
                from datetime import datetime
                lines.append(f"Generated: {datetime.now().isoformat()}")
            lines.append("")
        
        for i, line in enumerate(self.diff_content):
            if self.config.options.include_line_numbers:
                lines.append(f"{i + 1:4d}: {line}")
            else:
                lines.append(line)
        
        if self.config.options.include_statistics:
            lines.append("")
            lines.append("=" * 70)
            lines.append("STATISTICS")
            lines.append("=" * 70)
            lines.append(f"Total lines: {len(self.diff_content)}")
            lines.append(f"Total files: {len(self.file_paths)}")
        
        return "\n".join(lines)
    
    def _export_html(self) -> str:
        """HTML formatında dışa aktar."""
        html = ["<!DOCTYPE html>", "<html>", "<head>", "<meta charset='utf-8'>", "<title>Diff Export</title>", "<style>"]
        
        if self.config.options.colorize:
            html.append("""
                .added { background-color: #d4edda; color: #155724; }
                .removed { background-color: #f8d7da; color: #721c24; }
                .modified { background-color: #fff3cd; color: #856404; }
                .line-number { color: #6c757d; margin-right: 10px; }
            """)
        
        html.append("</style>")
        html.append("</head>")
        html.append("<body>")
        html.append("<pre>")
        
        for i, line in enumerate(self.diff_content):
            line_class = ""
            if line.startswith("+"):
                line_class = "added"
            elif line.startswith("-"):
                line_class = "removed"
            elif line.startswith("@@"):
                line_class = "modified"
            
            line_num = f"<span class='line-number'>{i + 1}</span>" if self.config.options.include_line_numbers else ""
            html.append(f"<div class='{line_class}'>{line_num}{line}</div>")
        
        html.append("</pre>")
        html.append("</body>")
        html.append("</html>")
        
        return "\n".join(html)
    
    def _export_markdown(self) -> str:
        """Markdown formatında dışa aktar."""
        lines = []
        
        if self.config.options.include_headers:
            lines.append("# Diff Export")
            if self.config.options.include_timestamp:
                from datetime import datetime
                lines.append(f"\n**Generated:** {datetime.now().isoformat()}\n")
        
        lines.append("```diff")
        lines.extend(self.diff_content)
        lines.append("```")
        
        if self.config.options.include_statistics:
            lines.append("\n## Statistics")
            lines.append(f"- Total lines: {len(self.diff_content)}")
            lines.append(f"- Total files: {len(self.file_paths)}")
        
        return "\n".join(lines)
    
    def _export_json(self) -> str:
        """JSON formatında dışa aktar."""
        data = {
            "format": self.config.format.value,
            "total_lines": len(self.diff_content),
            "total_files": len(self.file_paths),
            "content": self.diff_content,
            "file_paths": self.file_paths
        }
        
        if self.config.options.include_timestamp:
            from datetime import datetime
            data["generated_at"] = datetime.now().isoformat()
        
        return json.dumps(data, indent=2)
    
    def _export_patch(self) -> str:
        """Patch formatında dışa aktar."""
        lines = []
        
        if self.config.options.include_headers:
            lines.append("diff --git a/file b/file")
            lines.append("index 1234567..abcdefg 100644")
            lines.append("--- a/file")
            lines.append("+++ b/file")
        
        lines.extend(self.diff_content)
        
        return "\n".join(lines)
    
    def _export_unified(self) -> str:
        """Unified diff formatında dışa aktar."""
        lines = []
        
        if self.config.options.include_headers:
            lines.append("--- a/file")
            lines.append("+++ b/file")
        
        lines.extend(self.diff_content)
        
        return "\n".join(lines)
    
    def _export_side_by_side(self) -> str:
        """Side-by-side diff formatında dışa aktar."""
        lines = []
        
        if self.config.options.include_headers:
            lines.append("LEFT (ORIGINAL) | RIGHT (MODIFIED)")
            lines.append("=" * 70)
        
        # Basit side-by-side gösterim
        for line in self.diff_content:
            if line.startswith("+"):
                lines.append(f"                  | {line}")
            elif line.startswith("-"):
                lines.append(f"{line} |")
            else:
                lines.append(f"{line} | {line}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Basit test
    engine = DiffExporterEngine()
    
    diff_content = [
        "--- a/file.txt",
        "+++ b/file.txt",
        "@@ -1,3 +1,3 @@",
        " Line 1",
        "-Line 2 old",
        "+Line 2 new",
        " Line 3"
    ]
    
    result = engine.export(diff_content)
    print(f"Export: {result.success}")
    print(f"Format: {result.format}")
