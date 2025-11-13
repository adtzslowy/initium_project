import subprocess
import sys
import os
import webbrowser
import platform
from .php_installer import (
    get_latest_php_version,
    get_local_php_version,
    is_laragon_installed,
    download_php,
    detect_laragon_path,
)

# Silent install
def silent_install_windows(installer_path, silent_args=None):
    """
    Menjalankan installer windows secara silent tanpa GUI
    """
    if not os.path.exists(installer_path):
        print(f"❌ File installer tidak ditemukan: {installer_path}")
        return False

    try:
        cmd = [installer_path]
        if silent_args:
            cmd.extend(silent_args.split())
        print(f"🚀 Menjalankan installer silent: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        print("✅ Installasi selesai")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Gagal menjalankan installer silent: {e}")
        return False

def handle_choice(choice, os_type):
    tools = {
        1: {"name": "Node.js", "install": install_node},
        2: {"name": "Visual Studio Code", "install": install_vscode},
        3: {"name": "Git", "install": install_git},
        4: {"name": "Python", "install": install_python},
        5: {"name": "XAMPP", "install": install_xampp},
        6: {"name": "Laragon", "install": install_laragon},
        7: {"name": "Postman", "install": install_postman},
        8: {"name": "Docker Desktop", "install": install_docker},
        9: {"name": "PHP untuk laragon", "install": install_php_laragon},
        10: {"name": "Composer", "install": install_composer},
        11: {"name": "Install Semua", "install": None},
        12: {"name": "Keluar", "install": None},
    }

    try:
        choice = int(choice)

        if os_type == "Windows" and not is_winget_available():
            print("❌ Winget tidak tersedia disistem, akan menggunakan fallback URL")
            return

        if choice == 12:
            print("👋🏻 Keluar dari program!")
            sys.exit(1)

        if choice == 11:
            for i in range(1, 10):
                print(f"🔧 Menginstall {tools[i]['name']}...")
                tools[i]["install"](os_type)
            print("\n✅ Semua tools berhasil diproses")
            return

        selected = tools.get(choice)
        if not selected:
            print("⚠️ Pilihan tidak valid!")
            return

        print(f"🛠 Menginstall {selected['name']}...\n")
        selected["install"](os_type)

    except Exception as e:
        print(f"⚠️ Error: {e}")


# === DETEKSI WINGET HELPER ===
def is_winget_available():
    return (
        subprocess.call(
            ["where", "winget"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        == 0
    )


def winget_install(package_id, fallback_url=None):
    if not is_winget_available():
        if fallback_url:
            print(f"🔗 Membuka Fallback URL untuk {package_id}")
            open_url(fallback_url)
        else:
            print("❌ Winget dan fallback URL tidak tersedia untuk {package_id}")
        return

    try:
        subprocess.run(
            [
                "winget",
                "install",
                "--id",
                package_id,
                "--source",
                "winget",
                "--silent",
                "--accept-package-agreements",
                "--accept-source-agreements",
                "-e",
            ],
            check=True,
        )
    except subprocess.CalledProcessError:
        print(f"⚠️ Winget gagal menemukan atau menginstall {package_id}")
        if fallback_url:
            open_url(fallback_url)


# === FUNGSI PEMBANTU ===
def open_url(url):
    try:
        system = platform.system()
        if system == "Windows":
            os.startfile(url)
        elif system == "Darwin":
            subprocess.run(["open", url])
        elif system == "Linux":
            subprocess.run(["xdg-open", url])
        else:
            webbrowser.open(url)
    except Exception as e:
        print(f"❌ Gagal membuka URL: {e}")


# === INSTALLER FUNCTION ===
def install_node(os_type):
    if os_type == "macOS":
        subprocess.run(["brew", "install", "nodejs"])
    elif os_type == "Linux":
        subprocess.run(["sudo", "apt", "install", "-y", "nodejs"])
    elif os_type == "Windows":
        winget_install("OpenJS.NodeJS", "https://nodejs.org/en/download/")


def install_vscode(os_type):
    if os_type == "Windows":
        winget_install(
            "Microsoft.VisualStudioCode", "https://code.visualstudio.com/Download"
        )
    elif os_type == "macOS":
        subprocess.run(["brew", "install", "--cask", "visual-studio-code"])
    elif os_type == "Linux":
        subprocess.run(["sudo", "snap", "install", "--classic", "code"])


def install_git(os_type):
    if os_type == "Windows":
        winget_install("Git.Git", "https://git-scm.com/download/win")
    elif os_type == "macOS":
        subprocess.run(["brew", "install", "git"])
    elif os_type == "Linux":
        subprocess.run(["sudo", "apt", "install", "-y", "git"])


def install_python(os_type):
    if os_type == "Windows":
        winget_install("Python.Python3.13", "https://www.python.org/downloads/windows")
    elif os_type == "macOS":
        subprocess.run(["brew", "install", "python@3.14"])
    elif os_type == "Linux":
        subprocess.run(["sudo", "apt", "install", "-y", "python3", "python3-pip"])


def install_xampp(os_type):
    open_url("https://www.apachefriends.org/index.html")


def install_laragon(os_type):
    if os_type != "Windows":
        print("❌ Laragon hanya tersedia di Windows")
        return

    installer_url = (
        "https://github.com/leokhoa/laragon/releases/download/6.0.0/laragon-wamp.exe"
    )
    installer_name = "laragon-wamp.exe"

    try:
        import urllib.request
        print("⬇️ Mengunduh Laragon...")
        urllib.request.urlretrieve(installer_url, installer_name)
        print("✅ Laragon berhasil di unduh")

        print("🚀 Menginstall laragon...")
        silent_install_windows(installer_name, "/S")

    except Exception as e:
        print(f"❌ Gagal menginstall Laragon: {e}")


def install_postman(os_type):
    if os_type == "Windows":
        winget_install("Postman.Postman", "https://www.postman.com/downloads")
    else:
        open_url("https://www.postman.com/downloads")


def install_docker(os_type):
    if os_type == "Windows":
        winget_install(
            "Docker.DockerDesktop", "https://www.docker.com/products/docker-dekstop/"
        )
    elif os_type == "macOS":
        open_url("https://www.docker.com/products/docker-desktop/")
    elif os_type == "Linux":
        subprocess.run(["sudo", "apt", "install", "-y", "docker.io"])


def install_php_laragon(os_type):
    if os_type != "Windows":
        print("❌ Fitur ini hanya tersedia di Windows.")
        return

    if not is_laragon_installed():
        print("❌ Laragon tidak ditemukan di sistem, harap install terlebih dahulu.")

    print("\n--- PHP Installer Untuk Laragon ---")
    laragon_path = detect_laragon_path()
    installed_versions = get_local_php_version(laragon_path)
    latest_versions = get_latest_php_version()
    
    for major, (full, vs) in latest_versions.items():
        print(f"{major} ͢ PHP {full} ({vs})")
    
    latest_major = max(latest_versions.keys())
    latest_full, _ = latest_versions[latest_major]

    print(f"\n🌐 Versi PHP terbaru untuk {latest_major} adalah {latest_full}")

    if installed_versions and latest_full in installed_versions:
        print(f"✅ PHP {latest_full} sudah terpasang.")
        return
    
    print(f"⬇️ Mengunduh dan memasang PHP {latest_full} ...")
    success = download_php(latest_full, laragon_path)
    if success:
         print(f"🎉 PHP {latest_full} berhasil diinstal ke {laragon_path}\\bin\\php")
    else:
        print(f"❌ Gagal menginstal PHP {latest_full}.")


def install_composer(os_type):
    if os_type != "Windows":
        print("❌ Composer installer .exe hanya tersedia di Windows")
        return

    print("⬇️ Mengunduh installer composer.")
    composer_url = "https://getcomposer.org/Composer-Setup.exe"
    installer_path = "Composer-Setup.exe"

    try:
        import urllib.request

        urllib.request.urlretrieve(composer_url, installer_path)
        print("✅ Composer installer berhasil di unduh")

        print("🚀 Menjalankan installer Composer...")
        os.startfile(installer_path)
    except Exception as e:
        print(f"❌ Gagal menginstall Composer: {e}")
