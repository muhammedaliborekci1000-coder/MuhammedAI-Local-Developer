"""
Web Project Detector
Web projelerini tespit etme ve analiz etme.
"""

import re
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class WebProjectInfo:
    """Web projesi bilgisi."""
    is_web_project: bool
    framework: str
    package_manager: str
    start_command: str
    likely_port: int
    entrypoint: str
    confidence: float


class WebProjectDetector:
    """
    Web projesi tespiti.
    
    Desteklenen framework'ler:
    - Python: Flask, FastAPI, Django, simple HTTP server
    - Node: npm, pnpm, yarn, vite, next, express
    - Frontend: React, Vue, Angular, Vite, static HTML
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Args:
            project_root: Proje kök dizini
        """
        self.project_root = project_root
    
    def detect(self, project_root: Optional[Path] = None) -> WebProjectInfo:
        """
        Web projesi tespit et.
        
        Args:
            project_root: Proje kök dizini
            
        Returns:
            WebProjectInfo: Web projesi bilgisi
        """
        root = project_root or self.project_root
        if root is None:
            return self._unknown_project()
        
        root = Path(root)
        
        # Python framework kontrolü
        python_info = self._detect_python_framework(root)
        if python_info["is_web_project"]:
            return WebProjectInfo(**python_info)
        
        # Node framework kontrolü
        node_info = self._detect_node_framework(root)
        if node_info["is_web_project"]:
            return WebProjectInfo(**node_info)
        
        # Static HTML kontrolü
        static_info = self._detect_static_html(root)
        if static_info["is_web_project"]:
            return WebProjectInfo(**static_info)
        
        return self._unknown_project()
    
    def _detect_python_framework(self, root: Path) -> Dict[str, Any]:
        """Python framework tespit et."""
        
        # Flask
        if self._has_file(root, "app.py") or self._has_file(root, "main.py"):
            content = self._read_file(root, "app.py") or self._read_file(root, "main.py")
            if content and "flask" in content.lower():
                return {
                    "is_web_project": True,
                    "framework": "flask",
                    "package_manager": "pip",
                    "start_command": "python app.py" if self._has_file(root, "app.py") else "python main.py",
                    "likely_port": 5000,
                    "entrypoint": "app.py" if self._has_file(root, "app.py") else "main.py",
                    "confidence": 0.9,
                }
        
        # FastAPI
        if self._has_file(root, "main.py"):
            content = self._read_file(root, "main.py")
            if content and "fastapi" in content.lower():
                return {
                    "is_web_project": True,
                    "framework": "fastapi",
                    "package_manager": "pip",
                    "start_command": "uvicorn main:app --reload",
                    "likely_port": 8000,
                    "entrypoint": "main.py",
                    "confidence": 0.9,
                }
        
        # Django
        if self._has_file(root, "manage.py"):
            return {
                "is_web_project": True,
                "framework": "django",
                "package_manager": "pip",
                "start_command": "python manage.py runserver",
                "likely_port": 8000,
                "entrypoint": "manage.py",
                "confidence": 0.95,
            }
        
        # Simple HTTP server
        if self._has_file(root, "server.py"):
            content = self._read_file(root, "server.py")
            if content and "http.server" in content:
                return {
                    "is_web_project": True,
                    "framework": "python-http",
                    "package_manager": "pip",
                    "start_command": "python server.py",
                    "likely_port": 8000,
                    "entrypoint": "server.py",
                    "confidence": 0.7,
                }
        
        return {"is_web_project": False, "framework": "unknown", "package_manager": "unknown", 
                "start_command": "", "likely_port": 0, "entrypoint": "", "confidence": 0.0}
    
    def _detect_node_framework(self, root: Path) -> Dict[str, Any]:
        """Node framework tespit et."""
        
        # package.json kontrolü
        package_json = root / "package.json"
        if not package_json.exists():
            return {"is_web_project": False, "framework": "unknown", "package_manager": "unknown", 
                    "start_command": "", "likely_port": 0, "entrypoint": "", "confidence": 0.0}
        
        content = self._read_file(root, "package.json")
        if not content:
            return {"is_web_project": False, "framework": "unknown", "package_manager": "unknown", 
                    "start_command": "", "likely_port": 0, "entrypoint": "", "confidence": 0.0}
        
        # Vite
        if "vite" in content.lower():
            return {
                "is_web_project": True,
                "framework": "vite",
                "package_manager": self._detect_package_manager(root),
                "start_command": "npm run dev",
                "likely_port": 5173,
                "entrypoint": "package.json",
                "confidence": 0.95,
            }
        
        # Next.js
        if "next" in content.lower():
            return {
                "is_web_project": True,
                "framework": "next",
                "package_manager": self._detect_package_manager(root),
                "start_command": "npm run dev",
                "likely_port": 3000,
                "entrypoint": "package.json",
                "confidence": 0.95,
            }
        
        # Express
        if "express" in content.lower():
            return {
                "is_web_project": True,
                "framework": "express",
                "package_manager": self._detect_package_manager(root),
                "start_command": "npm start",
                "likely_port": 3000,
                "entrypoint": "package.json",
                "confidence": 0.9,
            }
        
        # React
        if "react" in content.lower():
            return {
                "is_web_project": True,
                "framework": "react",
                "package_manager": self._detect_package_manager(root),
                "start_command": "npm start",
                "likely_port": 3000,
                "entrypoint": "package.json",
                "confidence": 0.85,
            }
        
        # Vue
        if "vue" in content.lower():
            return {
                "is_web_project": True,
                "framework": "vue",
                "package_manager": self._detect_package_manager(root),
                "start_command": "npm run dev",
                "likely_port": 5173,
                "entrypoint": "package.json",
                "confidence": 0.85,
            }
        
        # Angular
        if "angular" in content.lower():
            return {
                "is_web_project": True,
                "framework": "angular",
                "package_manager": self._detect_package_manager(root),
                "start_command": "ng serve",
                "likely_port": 4200,
                "entrypoint": "package.json",
                "confidence": 0.85,
            }
        
        return {"is_web_project": False, "framework": "unknown", "package_manager": "unknown", 
                "start_command": "", "likely_port": 0, "entrypoint": "", "confidence": 0.0}
    
    def _detect_static_html(self, root: Path) -> Dict[str, Any]:
        """Static HTML tespit et."""
        
        # index.html kontrolü
        if self._has_file(root, "index.html"):
            return {
                "is_web_project": True,
                "framework": "static-html",
                "package_manager": "none",
                "start_command": "python -m http.server 8000",
                "likely_port": 8000,
                "entrypoint": "index.html",
                "confidence": 0.6,
            }
        
        return {"is_web_project": False, "framework": "unknown", "package_manager": "unknown", 
                "start_command": "", "likely_port": 0, "entrypoint": "", "confidence": 0.0}
    
    def _detect_package_manager(self, root: Path) -> str:
        """Package manager tespit et."""
        
        # pnpm-lock.yaml
        if self._has_file(root, "pnpm-lock.yaml"):
            return "pnpm"
        
        # yarn.lock
        if self._has_file(root, "yarn.lock"):
            return "yarn"
        
        # package-lock.json
        if self._has_file(root, "package-lock.json"):
            return "npm"
        
        # Default: npm
        return "npm"
    
    def _has_file(self, root: Path, filename: str) -> bool:
        """Dosya var mı?"""
        return (root / filename).exists()
    
    def _read_file(self, root: Path, filename: str) -> Optional[str]:
        """Dosya oku."""
        try:
            return (root / filename).read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return None
    
    def _unknown_project(self) -> WebProjectInfo:
        """Bilinmeyen proje."""
        return WebProjectInfo(
            is_web_project=False,
            framework="unknown",
            package_manager="unknown",
            start_command="",
            likely_port=0,
            entrypoint="",
            confidence=0.0,
        )
