import os
import sys
import time
import socket
import threading
import webbrowser
from pathlib import Path
from wsgiref.simple_server import make_server

# Tentukan Environment Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

def get_wifi_ip():
    """Dapatkan IP WiFi / LAN lokal agar HP bisa terhubung"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        # Tidak perlu koneksi nyata keluar, hanya untuk mendeteksi interface default
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return '127.0.0.1'

def find_available_port(default_port=8000):
    """Cari port yang tersedia, mulai dari 8000"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('0.0.0.0', default_port))
        s.close()
        return default_port
    except OSError:
        # Port 8000 terpakai, cari port bebas acak
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', 0))
        port = s.getsockname()[1]
        s.close()
        return port

def run_db_migrations():
    """Jalankan migrasi database otomatis saat pertama kali dibuka"""
    try:
        call_command('migrate', interactive=False)
    except Exception as e:
        print(f"[Info Migrasi] {e}")

def main():
    print("=" * 65)
    print("      ✨ ARISAN DIGITAL - BY ALWARE PLATFORM ✨")
    print("           Solusi Arisan Warga Modern & Transparan")
    print("=" * 65)
    print("\n[1/3] Menyiapkan database lokal...")
    run_db_migrations()

    port = find_available_port(8000)
    wifi_ip = get_wifi_ip()

    print("[2/3] Memulai server aplikasi arisan...")
    # StaticFilesHandler memastikan file CSS, logo SVG, dan JS terlayani sempurna
    application = StaticFilesHandler(get_wsgi_application())
    httpd = make_server('0.0.0.0', port, application)

    local_url = f"http://127.0.0.1:{port}/"
    hp_url = f"http://{wifi_ip}:{port}/"

    print("[3/3] Server siap melayani!")
    print("-" * 65)
    print(f"  💻 Akses di Laptop (Browser) : {local_url}")
    print(f"  📱 Akses di HP (1 Jaringan)  : {hp_url}")
    print("-" * 65)
    print("\n🌐 Membuka aplikasi Arisan di browser laptop secara otomatis...")
    print("\n⚠️  PENTING: Jangan tutup jendela hitam ini selama menggunakan aplikasi.")
    print("    Tekan CTRL + C di jendela ini untuk mematikan aplikasi.\n")

    def open_browser():
        time.sleep(1.2)
        try:
            webbrowser.open(local_url)
        except Exception:
            pass

    threading.Thread(target=open_browser, daemon=True).start()

    try:
        httpd.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        print("\n\nTerima kasih! Server Arisan Digital telah dimatikan.")

if __name__ == '__main__':
    main()
