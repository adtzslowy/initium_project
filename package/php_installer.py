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
from requests.adapters import HTTPAdapter, Retry
import tempfile
from tqdm import tqdm
import zipfile

LARAGON_PHP_DIR = None

VCREDIST_URLS = {
    "vs16": "https://aka.ms/vs/16/release/vc_redist.x64.exe",
    "VS17": "https://aka.ms/vs/17/release/vc_redist.x64.exe"
}

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def is_vcredist_installed_by_registry():
    try:
        uninstall_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        for base in uninstall_paths:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base) as root:
                for i in range(0, winreg.QueryInfoKey(root)[0]):
                    try:
                        subkey_name = winreg.EnumKey(root, i)
                        sub = winreg.OpenKey(root, subkey_name)
                        disp, _ = winreg.QueryValueEx(sub, "DisplayName")
                        if "Visual C++" in str(disp):
                            return True
                    except FileNotFoundError:
                        continue
                    except OSError:
                        continue
    except Exception:
        pass
    return False

def download_and_install_vcredist(version="vs17"):
    if not is_admin():
        print("❌ Memerlukan hak administrator untuk install VC++ Redistributable")
        print("💡 Jalankan program sebagai Administrator")
        return False

    url = VCREDIST_URLS.get(version)
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
            text=True
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
    url = "https://windows.php.net/downloads/releases/"
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))

    try:
        r = session.get(url, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"❌ Gagal mengakses situs PHP Windows: {e}")
        return {"8.4": ("8.4.14", "vs17")}

    soup = BeautifulSoup(r.text, "html.parser")
    versions = {}

    for a in soup.find_all("a", href=True):
      href = a["href"]
      name = os.path.basename(href)
      m = re.search(r"php-(\d+\.\d+\.\d+)-Win32-(vs\d+)-x64\.zip", name)
      if m:
          full_ver, vs_ver = m.groups()
          major = ".".join(full_ver.split(".")[:2])
          if major not in versions or full_ver > versions[major][0]:
              versions[major] = (full_ver, vs_ver)
    if not versions:
        print("⚠️ Tidak menemukan versi PHP di halaman release; gunakan fallback.")
        return {"8.4": ("8.4.1", "vs17")}
    return versions

def get_installed_php_version(laragon_path=None):
    if laragon_path is None:
        laragon_path = detect_laragon_path()
    if not laragon_path:
        return []

    php_dir = os.path.join(laragon_path, "bin", "php")
    if not os.path.exists(php_dir):
        return []

    dirs = [d for d in os.listdir(php_dir) if d.startswith('php')]
    return sorted(dirs, reverse=True)

def get_local_php_version(laragon_path=None):
    versions = get_installed_php_version(laragon_path)
    if not versions:
        return None
    latest_local = versions[0].replace("php-", "")
    print(f"[✓] Versi PHP Lokal: {latest_local}")
    return latest_local

def safe_extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for member in zf.namelist():
            member_path = os.path.normpath(os.path.join(extract_to, member))
            if not member_path.startswith(os.path.abspath(extract_to)):
                raise Exception("Attempted Path Traversal in Zip File")
        zf.extractall(extract_to)


def download_php(version, laragon_path):
    compiler = "vs17" if (int(version.split('.')[0]) > 8 or (int(version.split('.')[0]) == 8 and int(version.split('.')[1]) >= 4)) else "vs16"
    url = f"https://windows.php.net/downloads/releases/php-{version}-Win32-{compiler}-x64.zip"
    print(f"[*] Menggunakan build: {compiler.upper()} | URL: {url}")

    temp_dir = tempfile.gettempdir()
    filename = os.path.join(temp_dir, f"php-{version}.zip")

    try:
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            with open(filename, 'wb') as f, tqdm(total=total, unit='B', unit_scale=True, desc=f"Downloading PHP {version}") as pbar:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
    except Exception as e:
        print(f"[-] Gagal mengunduh: {e}")
        if os.path.exists(filename):
            os.remove(filename)
        return False

    php_dir = os.path.join(laragon_path, "bin", "php", f"php-{version}")
    os.makedirs(php_dir, exist_ok=True)

    try:
        safe_extract_zip(filename, php_dir)
    except Exception as e:
        print(f"[-] Gagal mengekstrak zip: {e}")
        if os.path.exists(filename):
            os.remove(filename)
        return False
    finally:
        if os.path.exists(filename):
            os.remove(filename)

    print(f"[✓] PHP {version} berhasil diinstal di: {php_dir}")
    return True


def is_laragon_installed():
    laragon_path = detect_laragon_path()
    if laragon_path:
        return True
    return False
