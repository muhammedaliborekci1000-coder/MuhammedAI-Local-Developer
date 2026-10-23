"""
MuhammedAI Local Developer - PyInstaller Paketleme Betiği
Windows masaüstü EXE oluşturma betiği.
"""

import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SPEC_FILE = PROJECT_ROOT / "muhammedai.spec"
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"

def build_exe():
    """PyInstaller ile EXE oluştur."""
    print("=" * 70)
    print("MuhammedAI Local Developer - EXE Paketleme")
    print("=" * 70)
    
    # Mutlak path'ler
    templates_path = PROJECT_ROOT / "app" / "ui" / "templates"
    static_path = PROJECT_ROOT / "app" / "ui" / "static"
    
    # PyInstaller komutu
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=MuhammedAI",
        "--onefile",
        "--windowed",
        "--clean",
        f"--specpath={BUILD_DIR}",
        f"--distpath={DIST_DIR}",
        f"--workpath={BUILD_DIR}",
        f"--add-data={templates_path};app/ui/templates",
        f"--add-data={static_path};app/ui/static",
        "--hidden-import=uvicorn.logging",
        "--hidden-import=uvicorn.loops",
        "--hidden-import=uvicorn.protocols",
        "--hidden-import=uvicorn.protocols.http",
        "--hidden-import=uvicorn.protocols.websockets",
        "--hidden-import=uvicorn.lifespan",
        "--hidden-import=webview",
        "--hidden-import=ollama",
        "--hidden-import=fastapi",
        "--hidden-import=jinja2",
        "--hidden-import=websockets",
        "desktop_app.py"
    ]
    
    print(f"\nKomut çalıştırılıyor:")
    print(" ".join(cmd))
    print()
    
    try:
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)
        print("\n" + "=" * 70)
        print("PAKETLEME BAŞARILI")
        print("=" * 70)
        print(f"EXE konumu: {DIST_DIR / 'MuhammedAI.exe'}")
        return True
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 70)
        print("PAKETLEME HATASI")
        print("=" * 70)
        print(f"Hata kodu: {e.returncode}")
        return False
    except FileNotFoundError:
        print("\n" + "=" * 70)
        print("HATA: PyInstaller bulunamadı")
        print("=" * 70)
        print("Lütfen önce PyInstaller kurun:")
        print("pip install pyinstaller")
        return False

def build_onedir():
    """PyInstaller ile onedir modunda oluştur (daha kolay debug)."""
    print("=" * 70)
    print("MuhammedAI Local Developer - OneDir Paketleme")
    print("=" * 70)
    
    # Mutlak path'ler
    templates_path = PROJECT_ROOT / "app" / "ui" / "templates"
    static_path = PROJECT_ROOT / "app" / "ui" / "static"
    
    # PyInstaller komutu - onedir
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=MuhammedAI",
        "--onedir",
        "--windowed",  # Windowed mod - konsol gösterme
        "--clean",
        f"--specpath={BUILD_DIR}",
        f"--distpath={DIST_DIR}",
        f"--workpath={BUILD_DIR}",
        f"--add-data={templates_path};app/ui/templates",
        f"--add-data={static_path};app/ui/static",
        "--hidden-import=uvicorn.logging",
        "--hidden-import=uvicorn.loops",
        "--hidden-import=uvicorn.protocols",
        "--hidden-import=uvicorn.protocols.http",
        "--hidden-import=uvicorn.protocols.websockets",
        "--hidden-import=uvicorn.lifespan",
        "--hidden-import=webview",
        "--hidden-import=ollama",
        "--hidden-import=fastapi",
        "--hidden-import=jinja2",
        "--hidden-import=websockets",
        "desktop_app.py"
    ]
    
    print(f"\nKomut çalıştırılıyor:")
    print(" ".join(cmd))
    print()
    
    try:
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)
        print("\n" + "=" * 70)
        print("PAKETLEME BAŞARILI (OneDir)")
        print("=" * 70)
        print(f"Dizin konumu: {DIST_DIR / 'MuhammedAI'}")
        print(f"EXE konumu: {DIST_DIR / 'MuhammedAI' / 'MuhammedAI.exe'}")
        return True
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 70)
        print("PAKETLEME HATASI")
        print("=" * 70)
        print(f"Hata kodu: {e.returncode}")
        return False
    except FileNotFoundError:
        print("\n" + "=" * 70)
        print("HATA: PyInstaller bulunamadı")
        print("=" * 70)
        print("Lütfen önce PyInstaller kurun:")
        print("pip install pyinstaller")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="MuhammedAI Local Developer EXE Paketleme")
    parser.add_argument("--onedir", action="store_true", help="OneDir modunda paketle (daha kolay debug)")
    parser.add_argument("--onefile", action="store_true", help="OneFile modunda paketle (tek EXE)")
    
    args = parser.parse_args()
    
    if args.onedir:
        success = build_onedir()
    elif args.onefile:
        success = build_exe()
    else:
        # Varsayılan: önce onedir dene
        print("Önce OneDir modunda paketleniyor (daha kolay debug)...")
        success = build_onedir()
        if success:
            print("\nOneDir başarılı. OneFile için --onefile kullanın.")
    
    sys.exit(0 if success else 1)
