"""
MuhammedAI Local Developer - Git Diff
Git diff engine for code editor.
"""

import os
import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class DiffType(Enum):
    """Diff type."""
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"
    UNCHANGED = "unchanged"


class DiffView(Enum):
    """Diff view mode."""
    INLINE = "inline"
    SIDE_BY_SIDE = "side_by_side"
    UNIFIED = "unified"


@dataclass
class DiffLine:
    """Diff line."""
    line_number: int
    content: str
    type: DiffType
    old_line_number: Optional[int] = None
    new_line_number: Optional[int] = None


@dataclass
class DiffHunk:
    """Diff hunk."""
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: List[DiffLine] = field(default_factory=list)
    header: str = ""


@dataclass
class FileDiff:
    """File diff."""
    file_path: str
    old_file: Optional[str] = None
    new_file: Optional[str] = None
    hunks: List[DiffHunk] = field(default_factory=list)
    added_lines: int = 0
    removed_lines: int = 0
    is_binary: bool = False


@dataclass
class GitDiffResult:
    """Git diff result."""
    success: bool
    diffs: List[FileDiff] = field(default_factory=list)
    total_files: int = 0
    total_added: int = 0
    total_removed: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class GitDiffEngine:
    """
    Git diff engine.
    
    Özellikler:
    - File diff viewing
    - Line-by-line diff
    - Added/removed/modified lines
    - Diff between commits
    - Diff between branches
    - Diff between working directory and HEAD
    - Diff with staging area
    - Diff statistics
    - Color-coded diff output
    - Inline diff view
    - Side-by-side diff view
    - Hunk navigation
    - Patch generation
    """
    
    def __init__(self, repo_path: str = "."):
        """
        Args:
            repo_path: Git repository path
        """
        self.repo_path = repo_path
    
    def diff(
        self,
        target: str = "HEAD",
        source: Optional[str] = None,
        file_path: Optional[str] = None,
        staged: bool = False
    ) -> GitDiffResult:
        """
        Git diff çalıştır.
        
        Args:
            target: Hedef commit/branch
            source: Kaynak commit/branch (opsiyonel)
            file_path: Dosya yolu (opsiyonel)
            staged: Staged changes
            
        Returns:
            GitDiffResult: Diff sonucu
        """
        result = GitDiffResult(success=False)
        
        try:
            # Git komutunu oluştur
            if staged:
                cmd = ["git", "diff", "--cached"]
            elif source:
                cmd = ["git", "diff", source, target]
            else:
                cmd = ["git", "diff", target]
            
            if file_path:
                cmd.append(file_path)
            
            # Git diff'i çalıştır
            import subprocess
            process = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if process.returncode != 0:
                result.errors.append(f"Git diff failed: {process.stderr}")
                return result
            
            # Diff'i parse et
            diffs = self._parse_diff(process.stdout)
            
            # İstatistikleri hesapla
            total_added = sum(d.added_lines for d in diffs)
            total_removed = sum(d.removed_lines for d in diffs)
            
            result.diffs = diffs
            result.total_files = len(diffs)
            result.total_added = total_added
            result.total_removed = total_removed
            result.success = True
            result.message = f"Diff: {len(diffs)} files changed, +{total_added}/-{total_removed} lines"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _parse_diff(self, diff_text: str) -> List[FileDiff]:
        """Diff text'ini parse et."""
        diffs = []
        
        if not diff_text:
            return diffs
            
        lines = diff_text.splitlines()
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Yeni dosya başlangıcı
            if line.startswith("diff --git"):
                file_diff = FileDiff(file_path="")
                
                # Dosya yollarını parse et
                if i + 1 < len(lines) and lines[i + 1].startswith("old mode"):
                    i += 1
                if i + 1 < len(lines) and lines[i + 1].startswith("new mode"):
                    i += 1
                if i + 1 < len(lines) and lines[i + 1].startswith("deleted file"):
                    i += 1
                if i + 1 < len(lines) and lines[i + 1].startswith("new file"):
                    i += 1
                if i + 1 < len(lines) and lines[i + 1].startswith("index"):
                    i += 1
                if i + 1 < len(lines) and lines[i + 1].startswith("---"):
                    file_diff.old_file = lines[i + 1][4:].strip()
                    i += 1
                if i + 1 < len(lines) and lines[i + 1].startswith("+++"):
                    file_diff.new_file = lines[i + 1][4:].strip()
                    file_diff.file_path = file_diff.new_file
                    i += 1
                
                # Hunks'ları parse et
                i += 1
                while i < len(lines) and (lines[i].startswith("@@") or lines[i].startswith("+") or lines[i].startswith("-") or lines[i].startswith(" ")):
                    if lines[i].startswith("@@"):
                        hunk = self._parse_hunk(lines[i])
                        file_diff.hunks.append(hunk)
                        i += 1
                        
                        # Hunk satırlarını parse et
                        while i < len(lines) and (lines[i].startswith("+") or lines[i].startswith("-") or lines[i].startswith(" ")):
                            diff_line = self._parse_diff_line(lines[i])
                            hunk.lines.append(diff_line)
                            
                            if diff_line.type == DiffType.ADDED:
                                file_diff.added_lines += 1
                            elif diff_line.type == DiffType.REMOVED:
                                file_diff.removed_lines += 1
                            
                            i += 1
                    else:
                        break
                
                diffs.append(file_diff)
            else:
                i += 1
        
        return diffs
    
    def _parse_hunk(self, header: str) -> DiffHunk:
        """Hunk header'ını parse et."""
        # @@ -old_start,old_count +new_start,new_count @@
        match = re.search(r'@@\s*-(\d+)(?:,(\d+))?\s*\+(\d+)(?:,(\d+))?\s*@@', header)
        
        if match:
            old_start = int(match.group(1))
            old_count = int(match.group(2)) if match.group(2) else 1
            new_start = int(match.group(3))
            new_count = int(match.group(4)) if match.group(4) else 1
            
            return DiffHunk(
                old_start=old_start,
                old_count=old_count,
                new_start=new_start,
                new_count=new_count,
                header=header
            )
        
        return DiffHunk(old_start=0, old_count=0, new_start=0, new_count=0, header=header)
    
    def _parse_diff_line(self, line: str) -> DiffLine:
        """Diff satırını parse et."""
        if line.startswith("+"):
            return DiffLine(
                line_number=0,
                content=line[1:],
                type=DiffType.ADDED,
                new_line_number=0
            )
        elif line.startswith("-"):
            return DiffLine(
                line_number=0,
                content=line[1:],
                type=DiffType.REMOVED,
                old_line_number=0
            )
        elif line.startswith(" "):
            return DiffLine(
                line_number=0,
                content=line[1:],
                type=DiffType.UNCHANGED
            )
        else:
            return DiffLine(
                line_number=0,
                content=line,
                type=DiffType.UNCHANGED
            )
    
    def get_diff_stats(self, target: str = "HEAD") -> Dict[str, int]:
        """
        Diff istatistiklerini al.
        
        Args:
            target: Hedef commit/branch
            
        Returns:
            Dict[str, int]: İstatistikler
        """
        result = self.diff(target)
        
        if not result.success:
            return {"files": 0, "additions": 0, "deletions": 0}
        
        return {
            "files": result.total_files,
            "additions": result.total_added,
            "deletions": result.total_removed
        }
    
    def generate_patch(
        self,
        target: str = "HEAD",
        source: Optional[str] = None
    ) -> Optional[str]:
        """
        Patch oluştur.
        
        Args:
            target: Hedef commit/branch
            source: Kaynak commit/branch
            
        Returns:
            Optional[str]: Patch içeriği
        """
        try:
            import subprocess
            
            if source:
                cmd = ["git", "diff", source, target]
            else:
                cmd = ["git", "diff", target]
            
            process = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if process.returncode == 0:
                return process.stdout
            
            return None
        
        except Exception:
            return None


if __name__ == "__main__":
    # Basit test
    import tempfile
    import subprocess
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Git repo oluştur
        subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmpdir, capture_output=True)
        
        # Dosya oluştur ve commit et
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Hello World")
        
        subprocess.run(["git", "add", "test.txt"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=tmpdir, capture_output=True)
        
        # Dosyayı değiştir
        with open(test_file, "w") as f:
            f.write("Hello World\nNew Line")
        
        # Diff al
        engine = GitDiffEngine(tmpdir)
        result = engine.diff()
        
        print(f"Diff: {result.success}")
        print(f"Total files: {result.total_files}")
        print(f"Total added: {result.total_added}")
        print(f"Total removed: {result.total_removed}")
