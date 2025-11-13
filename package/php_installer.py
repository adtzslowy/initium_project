import os
import urllib.request
import zipfile
import requests
import sys
from io import BytesIO
from bs4 import BeautifulSoup
import ctypes
import re

LARAGON_PHP_DIR = None

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAdmin()
    except:
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