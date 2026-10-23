"""
MuhammedAI Local Developer - Masaüstü Kısayolu Oluşturma
Windows masaüstü kısayolu oluşturma betiği.
"""

import os
import sys
from pathlib import Path

def create_shortcut():
    """Masaüstü kısayolu oluştur."""
    import pythoncom
    from win32com.client import Dispatch
    
    project_root = Path(__file__).resolve().parent
    exe_path = project_root / "dist" / "MuhammedAI" / "MuhammedAI.exe"
    desktop = Path.home() / "Desktop"
    shortcut_path = desktop / "MuhammedAI.lnk"
    
    if not exe_path.exists():
        print(f"HATA: EXE bulunamadı: {exe_path}")
        return False
    
    print("=" * 70)
    print("Masaüstü Kısayolu Oluşturma")
    print("=" * 70)
    print(f"EXE yolu: {exe_path}")
    print(f"Kısayol yolu: {shortcut_path}")
    
    try:
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.Targetpath = str(exe_path)
        shortcut.WorkingDirectory = str(exe_path.parent)
        shortcut.Description = "MuhammedAI Local Developer - AI Kod Asistanı"
        shortcut.save()
        
        print("\n" + "=" * 70)
        print("KISAYOL BAŞARIYLA OLUŞTURULDU")
        print("=" * 70)
        print(f"Konum: {shortcut_path}")
        return True
    except Exception as e:
        print(f"\nHATA: {e}")
        print("Alternatif: pywin32 kurulu olmayabilir.")
        print("Kurulum: pip install pywin32")
        return False

if __name__ == "__main__":
    success = create_shortcut()
    sys.exit(0 if success else 1)
