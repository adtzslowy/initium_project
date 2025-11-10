import os
import urllib.request
import zipfile
import shutil
import glob

LARAGON_PHP_DIR = "C:\\laragon\\bin\\php"


def is_laragon_installed():
    return os.path.exists(LARAGON_PHP_DIR)


SUPPORTED_PHP_VERSIONS = {
    "8.1": "8.1.33",
    "8.2": "8.2.29",
    "8.3": "8.3.25",
    "8.4": "8.4.12",
}


def detect_installed_php_versions():
    if not os.path.exists(LARAGON_PHP_DIR):
        print("❌ Laragon belum terpasang atau folder php tidak ditemukan")
        return []

    versions = [
        f
        for f in os.listdir(LARAGON_PHP_DIR)
        if os.path.isdir(os.path.join(LARAGON_PHP_DIR, f)) and f.startswith("php")
    ]
    print("\n📦 Versi PHP yang terdeteksi: ")
    for v in versions:
        print(f" - {v}")
    return versions


def download_and_install_php(major_version: str):
    full_version = SUPPORTED_PHP_VERSIONS.get(major_version)
    if not full_version:
        print("⚠️ Versi tidak tersedia")
        return

    vs_version = "vs17" if full_version.startswith("8.4") else "vs16"

    url = f"https://windows.php.net/downloads/releases/php-{full_version}-Win32-{vs_version}-x64.zip"
    filename = f"php-{full_version}.zip"
    install_dir = os.path.join("C:\\laragon\\bin\\php", f"php-{full_version}")

    if os.path.exists(install_dir):
        print(f"﹗ PHP {full_version} sudah terinstall di {install_dir}")
        return

    print(f"⬇️ Mendownload PHP {full_version}...")
    try:
        urllib.request.urlretrieve(url, filename)
    except Exception as e:
        print(f"❌ Download gagal: {e}")
        return

    print("📦 Mengekstrak file: ", install_dir)
    try:
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(install_dir)
        os.remove(filename)
        print(f"✅ PHP {full_version} berhasil di install")
    except Exception as e:
        print(f"❌ Gagal mengekstrak: {e}")
