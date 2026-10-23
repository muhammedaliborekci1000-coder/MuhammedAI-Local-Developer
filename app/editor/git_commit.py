"""
MuhammedAI Local Developer - Git Commit
Git commit engine for code editor.
"""

import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class CommitAction(Enum):
    """Commit action."""
    CREATE = "create"
    AMEND = "amend"
    CHERRY_PICK = "cherry_pick"
    REVERT = "revert"


@dataclass
class CommitAuthor:
    """Commit author."""
    name: str
    email: str


@dataclass
class Commit:
    """Commit."""
    hash: str
    author: CommitAuthor
    date: datetime
    message: str
    files_changed: int = 0
    insertions: int = 0
    deletions: int = 0
    short_hash: str = ""


@dataclass
class GitCommitResult:
    """Git commit result."""
    success: bool
    commit_hash: Optional[str] = None
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    staged_files: List[str] = field(default_factory=list)
    unstaged_files: List[str] = field(default_factory=list)


class GitCommitEngine:
    """
    Git commit engine.
    
    Özellikler:
    - Commit creation
    - Commit message editing
    - Commit history viewing
    - Commit staging
    - Commit amend
    - Commit cherry-pick
    - Commit revert
    - Commit statistics
    - Commit author management
    - Commit date management
    - Commit sign-off
    - Commit verification
    """
    
    def __init__(self, repo_path: str = "."):
        """
        Args:
            repo_path: Git repository path
        """
        self.repo_path = repo_path
    
    def commit(
        self,
        message: str,
        amend: bool = False,
        sign_off: bool = False,
        allow_empty: bool = False
    ) -> GitCommitResult:
        """
        Git commit çalıştır.
        
        Args:
            message: Commit mesajı
            amend: Son commit'i değiştir
            sign_off: Sign-off ekle
            allow_empty: Boş commit'e izin ver
            
        Returns:
            GitCommitResult: Commit sonucu
        """
        result = GitCommitResult(success=False)
        result.message = message
        
        try:
            import subprocess
            
            cmd = ["git", "commit"]
            
            if amend:
                cmd.append("--amend")
            if sign_off:
                cmd.append("--signoff")
            if allow_empty:
                cmd.append("--allow-empty")
            
            cmd.extend(["-m", message])
            
            process = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if process.returncode != 0:
                result.errors.append(f"Git commit failed: {process.stderr}")
                return result
            
            # Commit hash'i al
            hash_result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if hash_result.returncode == 0:
                result.commit_hash = hash_result.stdout.strip()
            
            result.success = True
            result.message = f"Commit successful: {result.commit_hash[:7] if result.commit_hash else 'unknown'}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def stage_files(self, files: List[str]) -> GitCommitResult:
        """
        Dosyaları stage et.
        
        Args:
            files: Dosya yolları listesi
            
        Returns:
            GitCommitResult: Staging sonucu
        """
        result = GitCommitResult(success=False)
        
        try:
            import subprocess
            
            cmd = ["git", "add"] + files
            
            process = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if process.returncode != 0:
                result.errors.append(f"Git add failed: {process.stderr}")
                return result
            
            result.staged_files = files
            result.success = True
            result.message = f"Staged {len(files)} files"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def unstage_files(self, files: List[str]) -> GitCommitResult:
        """
        Dosyaları unstaged yap.
        
        Args:
            files: Dosya yolları listesi
            
        Returns:
            GitCommitResult: Unstaging sonucu
        """
        result = GitCommitResult(success=False)
        
        try:
            import subprocess
            
            cmd = ["git", "reset"] + files
            
            process = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if process.returncode != 0:
                result.errors.append(f"Git reset failed: {process.stderr}")
                return result
            
            result.unstaged_files = files
            result.success = True
            result.message = f"Unstaged {len(files)} files"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_commit_history(self, max_count: int = 10) -> List[Commit]:
        """
        Commit geçmişini al.
        
        Args:
            max_count: Maksimum commit sayısı
            
        Returns:
            List[Commit]: Commit listesi
        """
        commits = []
        
        try:
            import subprocess
            
            cmd = ["git", "log", f"-{max_count}", "--pretty=format:%H|%an|%ae|%ai|%s"]
            
            process = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if process.returncode == 0:
                for line in process.stdout.splitlines():
                    parts = line.split("|", 4)
                    if len(parts) >= 5:
                        commit = Commit(
                            hash=parts[0],
                            short_hash=parts[0][:7],
                            author=CommitAuthor(name=parts[1], email=parts[2]),
                            date=datetime.fromisoformat(parts[3]),
                            message=parts[4]
                        )
                        commits.append(commit)
        
        except Exception:
            pass
        
        return commits
    
    def get_staged_files(self) -> List[str]:
        """
        Staged dosyaları al.
        
        Returns:
            List[str]: Staged dosya listesi
        """
        files = []
        
        try:
            import subprocess
            
            process = subprocess.run(
                ["git", "diff", "--name-only", "--cached"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if process.returncode == 0:
                files = process.stdout.splitlines()
        
        except Exception:
            pass
        
        return files
    
    def get_unstaged_files(self) -> List[str]:
        """
        Unstaged dosyaları al.
        
        Returns:
            List[str]: Unstaged dosya listesi
        """
        files = []
        
        try:
            import subprocess
            
            process = subprocess.run(
                ["git", "diff", "--name-only"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if process.returncode == 0:
                files = process.stdout.splitlines()
        
        except Exception:
            pass
        
        return files
    
    def amend_commit(self, new_message: Optional[str] = None) -> GitCommitResult:
        """
        Commit'i değiştir.
        
        Args:
            new_message: Yeni commit mesajı (opsiyonel)
            
        Returns:
            GitCommitResult: Amend sonucu
        """
        result = GitCommitResult(success=False)
        
        try:
            import subprocess
            
            cmd = ["git", "commit", "--amend"]
            
            if new_message:
                cmd.extend(["-m", new_message])
            else:
                cmd.append("--no-edit")
            
            process = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if process.returncode != 0:
                result.errors.append(f"Git amend failed: {process.stderr}")
                return result
            
            # Commit hash'i al
            hash_result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if hash_result.returncode == 0:
                result.commit_hash = hash_result.stdout.strip()
            
            result.success = True
            result.message = f"Commit amended: {result.commit_hash[:7] if result.commit_hash else 'unknown'}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def revert_commit(self, commit_hash: str) -> GitCommitResult:
        """
        Commit'i revert et.
        
        Args:
            commit_hash: Commit hash
            
        Returns:
            GitCommitResult: Revert sonucu
        """
        result = GitCommitResult(success=False)
        
        try:
            import subprocess
            
            cmd = ["git", "revert", commit_hash, "--no-edit"]
            
            process = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if process.returncode != 0:
                result.errors.append(f"Git revert failed: {process.stderr}")
                return result
            
            # Commit hash'i al
            hash_result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if hash_result.returncode == 0:
                result.commit_hash = hash_result.stdout.strip()
            
            result.success = True
            result.message = f"Commit reverted: {result.commit_hash[:7] if result.commit_hash else 'unknown'}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result


if __name__ == "__main__":
    # Basit test
    import tempfile
    import subprocess
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Git repo oluştur
        subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmpdir, capture_output=True)
        
        # Dosya oluştur ve stage et
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Hello World")
        
        engine = GitCommitEngine(tmpdir)
        stage_result = engine.stage_files(["test.txt"])
        
        if stage_result.success:
            # Commit et
            commit_result = engine.commit("Initial commit")
            print(f"Commit: {commit_result.success}")
            print(f"Hash: {commit_result.commit_hash}")
