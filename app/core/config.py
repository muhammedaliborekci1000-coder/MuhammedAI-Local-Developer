import os
import sys
from pathlib import Path

APP_NAME = "MuhammedAI Local Developer"

OLLAMA_HOST = "http://127.0.0.1:11434"

DEFAULT_MODEL = "qwen3:4b"

# PROJECT_ROOT çözümü - hem normal Python hem PyInstaller için
if getattr(sys, 'frozen', False):
    # EXE çalıştırılıyor - EXE'nin bulunduğu dizin
    PROJECT_ROOT = Path(sys.executable).parent.resolve()
else:
    # Normal Python çalıştırması
    # Önce ortam değişkenini kontrol et
    env_root = os.environ.get("MUHAMMEDAI_PROJECT_ROOT")
    if env_root:
        PROJECT_ROOT = Path(env_root).resolve()
    else:
        # Dosya yolundan hesapla (desktop_app.py veya web_app.py'den)
        try:
            PROJECT_ROOT = Path(__file__).resolve().parents[2]
        except:
            # Fallback: çalışma dizini
            PROJECT_ROOT = Path.cwd().resolve()

SUPPORTED_EXTENSIONS = {
    ".py",
    ".json",
    ".yaml",
    ".yml",
    ".txt",
    ".md",
    ".toml",
}

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode",
    ".muhammedai_backups",
}

