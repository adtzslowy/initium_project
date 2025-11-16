import os
import urllib.request
import zipfile
import requests
import sys
from io import BytesIO
from bs4 import BeautifulSoup
import ctypes
import re
import winreg
import subprocess

LARAGON_PHP_DIR = None

VCREDITS_URLS = {
    "vs16": "https://aka.ms/vs/16/release/vc_redist.x64.exe",
    "VS17": "https://aka.ms/vs/17/release/vc_redist.x64.exe"
}

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAdmin()
    except:
        return False


def check_vcredist_installed(version="vs17"):
    try:
        registry_path = [
            r"SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64",
            r"SOFTWARE\WOW6432Node\Microsoft\VisualStudio\14.0\VC\Runtimes\x64"
        ]

        for path in registry_path:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
                installed, _ = winreg.QueryValueEx(key, "Installed")
                major, _ = winreg.QueryValueEx(key, "Major")
                minor, _ = winreg.QueryValueEx(key, "Minor")
                winreg.CloseKey(key)

                if installed == 1:
                    if version == "vs17" and major >= 14 and minor >= 30:
                        return True
                    elif version == "vs16" and major >= 14 and minor >= 20:
                        return True
            except FileNotFoundError:
                continue
        return False
    except Exception as e:
        print(f"[-] Gagal memeriksa installasi vcredist: {e}")
        return False

def download_and_install_vcredist(version="vs17"):
    if not is_admin():
        print("❌ Memerlukan hak administrator untuk install VC++ Redistributable")
        print("💡 Jalankan program sebagai Administrator")
        return False

    url = VCREDITS_URLS.get(version)
    if not url:
        print(f"[-] Versi vcredist {version} tidak ditemukan/dikenali")
        return False
    print(f"[*] Mengunduh dan menginstall VC++ Redistributable version {version}...")

    try:
        temp_file = os.path.join(os.environ['TEMP'], f"vs_redist_{version}.exe")

        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        with open(temp_file, 'wb') as f:
            if total_size:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent = (downloaded / total_size) * 100
                    print(f"\r[+] Mengunduh... {percent:.2f}%", end='')
            else:
                f.write(response.content)

        print(f"✅ Download selesai.")
        print(f"[*] Menginstall VC++ Redistributable...")

        result = subprocess.run(
            [temp_file, '/install', "/quiet", '/norestart'],
            capture_output=True,
            text=tuple
        )

        if result.returncode == 0 or result.returncode == 3010:
            print(f"[✓] VC++ Redistributable version {version} berhasil diinstall.")
            if result.returncode == 3010:
                print("⚠️ Restart komputer mungkin diperlukan")
            os.remove(temp_file)
            return True
        else:
            print(f"[-] Gagal menginstall VC++ Redistributable. Kode keluar: {result.returncode}")
            return False
    except Exception as e:
        print(f"❌ Error saat install VC++ Redistributable: {e}")
        return False

def detect_laragon_path():
    possible_paths = [
        r"C:\laragon",
        r"D:\laragon"
    ]

    for path in possible_paths:
        if os.path.exists(path):
            print(f"Laragon ditemukan di: {path}")
            return path
    print("[-] Laragon tidak ditemukan di Disk C: dan D:")
    return None

def get_latest_php_version():
    # print("[*] Mengecek versi PHP terbaru dari windows.php.net")
    # url = "https://www.windows.php.net/downloads/release/"
    # r = requests.get(url)
    # soup = BeautifulSoup(r.text, "html.parser")

    # match = re.search(r"PHP (\d+\.\d+\.\d+)", soup.text)
    # if match:
    #     latest_version = match.group(1)
    #     print(f"[✓] Versi PHP terbaru: {latest_version}")
    #     return latest_version
    # print("[-] Gagal mendapatkan versi PHP terbaru")
    # return None

    url = "https://windows.php.net/downloads/releases/"
    r = requests.get(url)
    if r.status_code != 200:
        print("❌ Gagal mengakses situs PHP Windows")
        return {}

    soup = BeautifulSoup(r.text, "html.parser")
    versions = {}

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "x64" in href and href.endswith(".zip"):
            m = re.search(r"php-(\d+\.\d+\.\d+)-Win32-(vs\d+)-x64\.zip", href)
            if m:
                full_ver, vs_ver = m.groups()
                major = ".".join(full_ver.split(".")[:2])
                if major not in versions or full_ver > versions[major][0]:
                    versions[major] = (full_ver, vs_ver)

    return versions

def get_local_php_version(laragon_path=None):
    if laragon_path is None:
        laragon_path = detect_laragon_path()
    if not laragon_path:
        print("[-] Laragon tidak bisa ditemukan")
        return None

    php_dir = os.path.join(laragon_path, "bin", "php")
    if not os.path.exists(php_dir):
        return None

    dirs = [d for d in os.listdir(php_dir) if d.startswith("php")]
    if not dirs:
        return None

    versions = sorted(dirs, reverse=True)
    latest_local = versions[0].replace("php-", "")
    print(f"[✓] Versi PHP Lokal: {latest_local}")
    return latest_local

def download_php(version, laragon_path):
    print(f"[*] Mengunduh PHP {version} untuk windows")
    major, minor, *_ = version.split(".")
    major = int(major)
    minor = int(minor)

    if major > 8 or (major == 8 and minor >= 4):
        compiler = "vs17"
    else:
        compiler = "vs16"


    base_url = f"https://windows.php.net/downloads/releases/php-{version}-Win32-{compiler}-x64.zip"
    print(f"[*] Menggunakan build: {compiler.upper()}")

    r = requests.get(base_url, stream=True)

    if r.status_code != 200:
        print("[-] Gagal mengunduh file dari php.net, mungkin versi belum tersedia.")
        print(f"[-] Coba cek URL manual: {base_url}")
        return False

    php_dir = os.path.join(laragon_path, "bin", "php", f"php-{version}")
    os.makedirs(php_dir, exist_ok=True)

    with zipfile.ZipFile(BytesIO(r.content)) as zf:
        zf.extractall(php_dir)

    print(f"[✓] PHP {version} berhasil diinstal di: {php_dir}")
    return True

def is_laragon_installed():
    laragon_path = detect_laragon_path()
    if laragon_path:
        return True
    return False
