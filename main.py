import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from package.installer import handle_choice
from ui.interface import show_ui
from package.checker import is_connected


def main():
    if not is_connected():
        print("❌ tidak ada koneksi internet. harap sambungkan dan coba lagi.")
        return

    while True:
        os_type, choice = show_ui()
        handle_choice(choice, os_type)
        input("\n tekan enter untuk kembali ke menu....")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ program dihentikan oleh user")
