"""
launcher.py — نقطة الدخول لملف بوصلة.exe
يشغّل Streamlit محلياً ويفتح المتصفح تلقائياً
"""
import os
import sys
import time
import socket
import threading
import webbrowser
import subprocess
from pathlib import Path


def get_base_path() -> Path:
    """مسار المشروع سواء كان .exe أو script عادي"""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


def find_free_port(start: int = 8501) -> int:
    for port in range(start, start + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", port)) != 0:
                return port
    return start


def wait_and_open(port: int, delay: float = 3.5):
    time.sleep(delay)
    webbrowser.open(f"http://localhost:{port}")


def main():
    base = get_base_path()
    app_path = base / "app.py"

    # تحميل .env إن وُجد (لمفتاح OpenAI)
    env_file = base / ".env"
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)

    port = find_free_port(8501)

    # فتح المتصفح بعد تأخير بسيط لإعطاء Streamlit وقت للإقلاع
    t = threading.Thread(target=wait_and_open, args=(port,), daemon=True)
    t.start()

    # تشغيل Streamlit
    streamlit_cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(app_path),
        f"--server.port={port}",
        "--server.headless=true",
        "--server.address=localhost",
        "--browser.gatherUsageStats=false",
    ]

    subprocess.run(streamlit_cmd, cwd=str(base))


if __name__ == "__main__":
    main()
