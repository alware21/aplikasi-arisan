import os
import sys
import subprocess
import webbrowser
from pathlib import Path

CLOUD_PORTAL_URL = "https://alware21.pythonanywhere.com/portal/"

# Pastikan stdout/stderr aman saat dijalankan dalam mode GUI windowed (tanpa terminal console)
if sys.stdout is None:
    try:
        sys.stdout = open(os.devnull, "w", encoding="utf-8")
    except Exception:
        pass
if sys.stderr is None:
    try:
        sys.stderr = open(os.devnull, "w", encoding="utf-8")
    except Exception:
        pass


def find_browser_executable():
    """Mencari browser berbasis Chromium (Edge / Chrome) untuk mode jendela aplikasi mandiri."""
    candidates = [
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    return None


def main():
    """Membuka Arisan Digital Cloud (Full Online) dalam mode aplikasi desktop mandiri."""
    browser_exe = find_browser_executable()
    if browser_exe:
        try:
            profile_dir = Path(os.environ.get("TEMP", ".")) / "arisan_desktop_profile"
            subprocess.Popen([
                browser_exe,
                f"--app={CLOUD_PORTAL_URL}",
                f"--user-data-dir={profile_dir}",
                "--no-first-run",
                "--no-default-browser-check",
            ])
            return
        except Exception:
            pass

    webbrowser.open(CLOUD_PORTAL_URL)


if __name__ == "__main__":
    main()
