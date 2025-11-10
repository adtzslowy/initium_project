import os
import urllib.request
import zipfile
import requests
import sys
import glob
from bs4 import BeautifulSoup
import re

LARAGON_PHP_DIR = "C:\\laragon\\bin\\php"


def is_laragon_installed():
    return os.path.exists(LARAGON_PHP_DIR)

def detect_installed_php_versions():
    if not os.path.exists(LARAGON_PHP_DIR):
        print("❌ Laragon belum terpasang atau folder php tidak ditemukan")
        return []

    versions = [
        f for f in os.listdir(LARAGON_PHP_DIR)
        if os.path.isdir(os.path.join(LARAGON_PHP_DIR, f)) and f.startswith("php")
    ]
    print("\n📦 Versi PHP yang terdeteksi: ")
    for v in versions:
        print(f" - {v}")
    return versions

def get_latest_php_ver():
    url = "https://windows.php.net/download"
    r = requests.get(url)
    if r.status_code != 200:
        print("❌ Gagal mengakses situs PHP Windows")
        return {}

    soup = BeautifulSoup(r.text, "html.parser")
    versions = {}

    for a in soup.find_all("a", href=True):
        href = a['href']
        if "x64" in href and href.endswith("*.zip"):
            m = re.search(r"php-(\d+\.\d+\.\d+)-Win32-vs(\d+)-x64.zip")
            if m:
                full_ver, vs_ver = m.groups()
                major = ".".join(full_ver.split(".")[:2])
                if major not in versions or full_ver > versions[major][0]:
                    versions[major] = (full_ver, vs_ver)

    return versions

def download_and_install_php(major_version: str):
    latest_versions = get_latest_php_ver();
    if major_version not in latest_versions:
        print(f"⚠️ Versi {major_version} tidak ditemukan disitus resmi")
        return

    full_version, vs_version = latest_versions[major_version]
    install_dir = os.path.join(LARAGON_PHP_DIR, f"php-{full_version}")
    filename = f"php-{full_version}.zip"

    if os.path.exists(install_dir):
        print(f"! PHP {full_version} sudah terinstall di {install_dir}")
        return

    url = f"https://windows.php.net/downloads/releases/php-{full_version}-Win32-vs{vs_version}-x64.zip"
    print(f"⬇️ Mendownload PHP {full_version}")
    try:
        urllib.request.urlretrieve(url, filename)
    except Exception as e:
        print(f"Download Gagal: {e}")
        return

    print(f"📦 Mengekstrak file ke {install_dir}...")
    try:
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(install_dir);
        os.remove(filename)
    except Exception as e:
        print(f"❌ Gagal mengekstrak: {e}")

if __name__ == "__main__":
    if not is_laragon_installed():
        print('❌ Laragon tidak ter install!')
        sys.exit(1)

    installed_versions = detect_installed_php_versions()
    latest_version = get_latest_php_ver()

    print("\n🌐 Versi PHP terbaru di situs resmi:")
    for major, (full, vs) in latest_version.items():
        print(f" - {major}: {full} (VS{vs})")

    major_to_install = 8.4
    download_and_install_php(major_to_install)
