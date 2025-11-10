import os
import sys
import subprocess
import platform

def activate_and_run():
    system = platform.system()
    python_bin = (
        ".venv\\Scripts\\python.exe" if system == "Windows"
        else "./.venv/bin/python"
    )

    if not os.path.exists(python_bin):
        print("❌ Virtual environment tidak ditemukan.")
        print("💡 Jalankan perintah berikut:")
        print("   python -m venv .venv")
        print("   pip install -r requirements.txt")
        return

    try:
        subprocess.run([python_bin, "main.py"])
    except KeyboardInterrupt:
        print("\n❌ Program dihentikan oleh user")

if __name__ == "__main__":
    activate_and_run()
