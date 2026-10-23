"""
MuhammedAI Local Developer - Directory Creation
Directory creation engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import os
from datetime import datetime


class CreateMode(Enum):
    """Create mode."""
    SINGLE = "single"
    NESTED = "nested"
    WITH_PARENTS = "with_parents"
    FORCE = "force"


class TemplateType(Enum):
    """Template type."""
    EMPTY = "empty"
    GIT = "git"
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    CUSTOM = "custom"


@dataclass
class CreateConfig:
    """Create configuration."""
    mode: CreateMode = CreateMode.WITH_PARENTS
    template: TemplateType = TemplateType.EMPTY
    create_gitignore: bool = False
    create_readme: bool = False
    permissions: str = "755"
    show_notification: bool = True


@dataclass
class CreateResult:
    """Create result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    created_path: Optional[str] = None
    created_count: int = 0


class DirectoryCreationEngine:
    """
    Directory creation engine.
    
    Özellikler:
    - Create directory
    - Create nested directories
    - Create with parents
    - Force creation
    - Template support
    - Gitignore support
    - README support
    - Permission support
    - Creation history
    - Undo support
    - Smart detection
    """
    
    def __init__(self, config: Optional[CreateConfig] = None):
        """Initialize directory creation engine."""
        self.config = config or CreateConfig()
        self.creation_history: List[Dict[str, Any]] = []
    
    def create_directory(self, path: str) -> CreateResult:
        """
        Dizin oluştur.
        
        Args:
            path: Dizin yolu
            
        Returns:
            CreateResult: Oluşturma sonucu
        """
        result = CreateResult(success=False)
        result.created_path = path
        
        try:
            # Check if already exists
            if os.path.exists(path):
                if self.config.mode == CreateMode.FORCE:
                    # Remove existing
                    if os.path.isdir(path):
                        import shutil
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                else:
                    result.errors.append(f"Path already exists: {path}")
                    return result
            
            # Create directory based on mode
            if self.config.mode == CreateMode.WITH_PARENTS:
                os.makedirs(path, exist_ok=True)
            elif self.config.mode == CreateMode.NESTED:
                os.makedirs(path, exist_ok=False)
            else:
                os.mkdir(path)
            
            # Apply template
            if self.config.template != TemplateType.EMPTY:
                self._apply_template(path)
            
            # Create gitignore
            if self.config.create_gitignore:
                self._create_gitignore(path)
            
            # Create readme
            if self.config.create_readme:
                self._create_readme(path)
            
            # Add to history
            self.creation_history.append({
                "path": path,
                "mode": self.config.mode.value,
                "template": self.config.template.value,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.created_count = 1
            result.message = f"Directory created: {path}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def create_multiple(self, paths: List[str]) -> CreateResult:
        """
        Birden fazla dizin oluştur.
        
        Args:
            paths: Dizin yolları
            
        Returns:
            CreateResult: Oluşturma sonucu
        """
        result = CreateResult(success=False)
        created_count = 0
        all_errors = []
        
        for path in paths:
            single_result = self.create_directory(path)
            if single_result.success:
                created_count += 1
            else:
                all_errors.extend(single_result.errors)
        
        result.success = created_count > 0
        result.created_count = created_count
        result.errors = all_errors
        result.message = f"Created {created_count} directories"
        
        return result
    
    def can_create(self, path: str) -> bool:
        """
        Oluşturulabilir mi?
        
        Args:
            path: Dizin yolu
            
        Returns:
            bool: Oluşturulabilir mi
        """
        try:
            if os.path.exists(path):
                return self.config.mode == CreateMode.FORCE
            
            # Check parent directory
            parent = os.path.dirname(path)
            if parent and not os.path.exists(parent):
                return self.config.mode == CreateMode.WITH_PARENTS
            
            return True
        except Exception:
            return False
    
    def undo_creation(self, path: str) -> CreateResult:
        """
        Oluşturmayı geri al.
        
        Args:
            path: Dizin yolu
            
        Returns:
            CreateResult: Geri alma sonucu
        """
        result = CreateResult(success=False)
        
        try:
            if not os.path.exists(path):
                result.errors.append(f"Path not found: {path}")
                return result
            
            if not os.path.isdir(path):
                result.errors.append(f"Path is not a directory: {path}")
                return result
            
            # Remove directory
            import shutil
            shutil.rmtree(path)
            
            # Remove from history
            self.creation_history = [
                h for h in self.creation_history
                if h["path"] != path
            ]
            
            result.success = True
            result.message = f"Directory removed: {path}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _apply_template(self, path: str) -> None:
        """
        Şablon uygula.
        
        Args:
            path: Dizin yolu
        """
        templates = {
            TemplateType.PYTHON: self._python_template,
            TemplateType.JAVASCRIPT: self._javascript_template,
            TemplateType.GIT: self._git_template,
        }
        
        template_func = templates.get(self.config.template)
        if template_func:
            template_func(path)
    
    def _python_template(self, path: str) -> None:
        """
        Python şablonu uygula.
        
        Args:
            path: Dizin yolu
        """
        # Create __init__.py
        init_file = os.path.join(path, "__init__.py")
        with open(init_file, 'w') as f:
            f.write('"""Python package."""\n')
        
        # Create src directory
        src_dir = os.path.join(path, "src")
        os.makedirs(src_dir, exist_ok=True)
    
    def _javascript_template(self, path: str) -> None:
        """
        JavaScript şablonu uygula.
        
        Args:
            path: Dizin yolu
        """
        # Create src directory
        src_dir = os.path.join(path, "src")
        os.makedirs(src_dir, exist_ok=True)
        
        # Create package.json
        package_file = os.path.join(path, "package.json")
        with open(package_file, 'w') as f:
            f.write('{\n  "name": "project",\n  "version": "1.0.0"\n}\n')
    
    def _git_template(self, path: str) -> None:
        """
        Git şablonu uygula.
        
        Args:
            path: Dizin yolu
        """
        # Create .git directory
        git_dir = os.path.join(path, ".git")
        os.makedirs(git_dir, exist_ok=True)
        
        # Create HEAD file
        head_file = os.path.join(git_dir, "HEAD")
        with open(head_file, 'w') as f:
            f.write('ref: refs/heads/master\n')
        
        # Create objects and refs directories
        os.makedirs(os.path.join(git_dir, "objects"), exist_ok=True)
        os.makedirs(os.path.join(git_dir, "refs", "heads"), exist_ok=True)
    
    def _create_gitignore(self, path: str) -> None:
        """
        .gitignore oluştur.
        
        Args:
            path: Dizin yolu
        """
        gitignore_file = os.path.join(path, ".gitignore")
        with open(gitignore_file, 'w') as f:
            f.write('# Python\n__pycache__/\n*.pyc\n\n# Node\nnode_modules/\n\n# IDE\n.vscode/\n.idea/\n')
    
    def _create_readme(self, path: str) -> None:
        """
        README oluştur.
        
        Args:
            path: Dizin yolu
        """
        readme_file = os.path.join(path, "README.md")
        with open(readme_file, 'w') as f:
            f.write('# Project\n\nDescription\n')
    
    def get_creation_history(self) -> List[Dict[str, Any]]:
        """
        Oluşturma geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.creation_history
    
    def clear_history(self) -> CreateResult:
        """
        Geçmişi temizle.
        
        Returns:
            CreateResult: Temizleme sonucu
        """
        result = CreateResult(success=False)
        
        try:
            self.creation_history.clear()
            result.success = True
            result.message = "Creation history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: CreateConfig) -> CreateResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            CreateResult: Güncelleme sonucu
        """
        result = CreateResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> CreateConfig:
        """
        Konfigürasyon al.
        
        Returns:
            CreateConfig: Konfigürasyon
        """
        return self.config
    
    def _get_timestamp(self) -> str:
        """
        Zaman damgası al.
        
        Returns:
            str: ISO format zaman damgası
        """
        return datetime.now().isoformat()


if __name__ == "__main__":
    # Basit test
    engine = DirectoryCreationEngine()
    
    print("Directory Creation Engine initialized")
    print(f"Mode: {engine.config.mode.value}")
