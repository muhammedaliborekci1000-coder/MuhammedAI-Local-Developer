"""
MuhammedAI Local Developer - Masaüstü Başlatıcısı
PyInstaller ile paketlenmiş EXE için optimize edilmiş başlatıcı.
"""

import threading
import time
import socket
import sys
import os
from pathlib import Path
import logging

import uvicorn
import webview

# Log ayarları
log_file = Path.home() / ".muhammedai" / "desktop_app.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

HOST = "127.0.0.1"
PORT = 8000


def find_available_port(start_port=8000, max_attempts=10):
    """
    Kullanılabilir bir port bul.
    
    Args:
        start_port: Başlangıç portu
        max_attempts: Maksimum deneme sayısı
        
    Returns:
        int: Kullanılabilir port veya None
    """
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                pass  # Port kullanımda
        except OSError:
            return port  # Port boş
    return None


def wait_for_server(host, port, timeout=30):
    """
    Sunucunun başlamasını bekle.
    
    Args:
        host: Sunucu adresi
        port: Sunucu portu
        timeout: Maksimum bekleme süresi (saniye)
        
    Returns:
        bool: Sunucu başarılı mı başladı
    """
    deadline = time.time() + timeout
    logger.info(f"Sunucu başlaması bekleniyor: {host}:{port}")

    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=1):
                logger.info(f"Sunucu başarılı: {host}:{port}")
                return True
        except OSError:
            time.sleep(0.3)

    logger.error(f"Sunucu başlatılamadı: {host}:{port}")
    return False


def main():
    """Ana fonksiyon."""
    logger.info("MuhammedAI Local Developer başlatılıyor...")
    
    # Proje kökünü ayarla (PyInstaller için)
    if getattr(sys, 'frozen', False):
        # EXE çalıştırılıyor
        exe_dir = Path(sys.executable).parent
        os.environ["MUHAMMEDAI_PROJECT_ROOT"] = str(exe_dir)
        logger.info(f"EXE modu çalışıyor, PROJECT_ROOT: {exe_dir}")
    else:
        # Normal Python çalıştırması - desktop_app.py proje kökünde
        project_root = Path(__file__).resolve().parents[0]
        os.environ["MUHAMMEDAI_PROJECT_ROOT"] = str(project_root)
        logger.info(f"Normal mod çalışıyor, PROJECT_ROOT: {project_root}")
    
    # App'i import et (PROJECT_ROOT ayarlandıktan sonra)
    try:
        from app.ui.web_app import app
    except Exception as e:
        logger.error(f"App import hatası: {e}")
        import traceback
        traceback.print_exc()
        logger.error("Lütfen uygulama doğru paketlenmiş ve tüm bağımlılıklar yüklü.")
        sys.exit(1)
    
    # Port kontrolü
    available_port = find_available_port(PORT)
    if available_port is None:
        logger.error(f"Port {PORT}-{PORT+10} arası kullanımda.")
        logger.error("Lütfen başka bir uygulama kapatın veya portu değiştirin.")
        input("Çıkmak için Enter tuşuna basın...")
        sys.exit(1)
    
    actual_port = available_port
    if actual_port != PORT:
        logger.warning(f"Port {PORT} kullanımda, {actual_port} kullanılıyor.")
    
    # Sunucu başlat
    server = uvicorn.Server(
        uvicorn.Config(
            app,
            host=HOST,
            port=actual_port,
            log_level="info",
        )
    )
    
    server_thread = threading.Thread(
        target=server.run,
        daemon=False,  # Daemon değil, düzgün kapanması için
    )
    server_thread.start()
    
    try:
        # Sunucunun başlamasını bekle
        if not wait_for_server(HOST, actual_port):
            raise RuntimeError(
                f"Yerel sunucu 30 saniye içinde başlatılamadı: {HOST}:{actual_port}"
            )
        
        logger.info("Masaüstü penceresi açılıyor...")
        
        # Masaüstü penceresi
        webview.create_window(
            "MuhammedAI Local Developer",
            f"http://{HOST}:{actual_port}",
            width=1440,
            height=900,
            min_size=(1000, 650),
            background_color="#1a1a2e",
        )
        
        webview.start()
        
    except Exception as e:
        logger.error(f"Uygulama hatası: {e}")
        import traceback
        traceback.print_exc()
        input("Çıkmak için Enter tuşuna basın...")
    
    finally:
        logger.info("Sunucu kapatılıyor...")
        server.should_exit = True
        server_thread.join(timeout=5)
        logger.info("Uygulama kapandı.")


if __name__ == "__main__":
    main()
