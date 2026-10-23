"""
Real Git Integration
Gerçek Git subprocess çağrıları (commit, push, pull, branch yönetimi).
"""

import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class GitStatus(Enum):
    """Git status."""
    UNTRACKED = "untracked"
    MODIFIED = "modified"
    STAGED = "staged"
    COMMITTED = "committed"
    IGNORED = "ignored"


@dataclass
class GitFile:
    """Git file status."""
    path: str
    status: GitStatus
    staged: bool = False


@dataclass
class GitBranch:
    """Git branch information."""
    name: str
    is_current: bool = False
    is_remote: bool = False


class RealGit:
    """
    Real Git integration using subprocess.
    
    Özellikler:
    - Gerçek Git subprocess çağrıları
    - Commit, push, pull işlemleri
    - Branch yönetimi (create, switch, delete)
    - Status, diff, log
    - Merge, rebase
    """
    
    def __init__(self, repo_path: str):
        """
        Initialize Git client.
        
        Args:
            repo_path: Git repository path
        """
        self.repo_path = Path(repo_path)
    
    def _run_git(self, args: List[str]) -> subprocess.CompletedProcess:
        """
        Git komutu çalıştır.
        
        Args:
            args: Git komut argümanları
            
        Returns:
            subprocess.CompletedProcess
        """
        return subprocess.run(
            ["git"] + args,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
    
    def status(self) -> Dict[str, Any]:
        """
        Git status al.
        
        Returns:
            Dict: Status bilgisi
        """
        result = self._run_git(["status", "--porcelain"])
        
        files = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            
            status_code = line[:2]
            path = line[3:]
            
            if status_code == "??":
                status = GitStatus.UNTRACKED
            elif status_code.startswith("M"):
                status = GitStatus.MODIFIED
            elif status_code.startswith("A"):
                status = GitStatus.STAGED
            else:
                status = GitStatus.MODIFIED
            
            files.append(GitFile(path=path, status=status))
        
        # Branch bilgisi
        branch_result = self._run_git(["branch", "--show-current"])
        branch = branch_result.stdout.strip()
        
        return {
            "success": True,
            "branch": branch,
            "files": [
                {"path": f.path, "status": f.status.value}
                for f in files
            ],
            "modified": len([f for f in files if f.status == GitStatus.MODIFIED]),
            "staged": len([f for f in files if f.status == GitStatus.STAGED]),
            "untracked": len([f for f in files if f.status == GitStatus.UNTRACKED])
        }
    
    def add(self, files: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Dosyaları stage'e ekle.
        
        Args:
            files: Dosya listesi (None = tüm değişiklikler)
            
        Returns:
            Dict: Sonuç
        """
        args = ["add"]
        if files:
            args.extend(files)
        else:
            args.append(".")
        
        result = self._run_git(args)
        
        return {
            "success": result.returncode == 0,
            "message": result.stdout if result.returncode == 0 else result.stderr
        }
    
    def commit(self, message: str) -> Dict[str, Any]:
        """
        Commit yap.
        
        Args:
            message: Commit mesajı
            
        Returns:
            Dict: Sonuç
        """
        result = self._run_git(["commit", "-m", message])
        
        return {
            "success": result.returncode == 0,
            "message": result.stdout if result.returncode == 0 else result.stderr
        }
    
    def push(self, remote: str = "origin", branch: Optional[str] = None) -> Dict[str, Any]:
        """
        Push yap.
        
        Args:
            remote: Remote adı
            branch: Branch adı (None = current branch)
            
        Returns:
            Dict: Sonuç
        """
        args = ["push", remote]
        if branch:
            args.append(branch)
        
        result = self._run_git(args)
        
        return {
            "success": result.returncode == 0,
            "message": result.stdout if result.returncode == 0 else result.stderr
        }
    
    def pull(self, remote: str = "origin", branch: Optional[str] = None) -> Dict[str, Any]:
        """
        Pull yap.
        
        Args:
            remote: Remote adı
            branch: Branch adı (None = current branch)
            
        Returns:
            Dict: Sonuç
        """
        args = ["pull", remote]
        if branch:
            args.append(branch)
        
        result = self._run_git(args)
        
        return {
            "success": result.returncode == 0,
            "message": result.stdout if result.returncode == 0 else result.stderr
        }
    
    def branches(self) -> Dict[str, Any]:
        """
        Branch listesini al.
        
        Returns:
            Dict: Branch bilgisi
        """
        result = self._run_git(["branch", "-a"])
        
        branches = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            
            is_current = line.startswith("*")
            name = line[2:].strip()
            is_remote = "/" in name
            
            if is_remote:
                name = name.split("/")[-1]
            
            branches.append(GitBranch(
                name=name,
                is_current=is_current,
                is_remote=is_remote
            ))
        
        return {
            "success": True,
            "branches": [
                {"name": b.name, "is_current": b.is_current, "is_remote": b.is_remote}
                for b in branches
            ]
        }
    
    def create_branch(self, name: str, checkout: bool = True) -> Dict[str, Any]:
        """
        Yeni branch oluştur.
        
        Args:
            name: Branch adı
            checkout: Branch'e geçiş yap
            
        Returns:
            Dict: Sonuç
        """
        args = ["branch"]
        if checkout:
            args.append("-b")
        args.append(name)
        
        result = self._run_git(args)
        
        return {
            "success": result.returncode == 0,
            "message": result.stdout if result.returncode == 0 else result.stderr
        }
    
    def switch_branch(self, name: str) -> Dict[str, Any]:
        """
        Branch'e geçiş yap.
        
        Args:
            name: Branch adı
            
        Returns:
            Dict: Sonuç
        """
        result = self._run_git(["checkout", name])
        
        return {
            "success": result.returncode == 0,
            "message": result.stdout if result.returncode == 0 else result.stderr
        }
    
    def delete_branch(self, name: str, force: bool = False) -> Dict[str, Any]:
        """
        Branch sil.
        
        Args:
            name: Branch adı
            force: Zorla sil
            
        Returns:
            Dict: Sonuç
        """
        args = ["branch"]
        if force:
            args.append("-D")
        else:
            args.append("-d")
        args.append(name)
        
        result = self._run_git(args)
        
        return {
            "success": result.returncode == 0,
            "message": result.stdout if result.returncode == 0 else result.stderr
        }
    
    def log(self, limit: int = 10) -> Dict[str, Any]:
        """
        Commit log'u al.
        
        Args:
            limit: Commit sayısı
            
        Returns:
            Dict: Log bilgisi
        """
        result = self._run_git(["log", "--oneline", f"-{limit}"])
        
        commits = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            
            parts = line.split(" ", 1)
            if len(parts) == 2:
                hash_short, message = parts
                commits.append({"hash": hash_short, "message": message})
        
        return {
            "success": True,
            "commits": commits
        }
    
    def diff(self, file: Optional[str] = None) -> Dict[str, Any]:
        """
        Diff al.
        
        Args:
            file: Dosya yolu (None = tüm değişiklikler)
            
        Returns:
            Dict: Diff bilgisi
        """
        args = ["diff"]
        if file:
            args.append(file)
        
        result = self._run_git(args)
        
        return {
            "success": True,
            "diff": result.stdout
        }
