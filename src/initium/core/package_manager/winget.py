import subprocess
from .base import BasePackageManager

class WingetPackageManager(BasePackageManager):
    @property
    def name(self) -> str:
        return "winget"

    def is_available(self) -> bool:
        try:
            result = subprocess.run(
                ["winget", "--version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            return True
        except Exception:
            return False

    def install(self, package_id: str) -> bool:
        try:
            result = subprocess.run(
                [
                    "winget",
                    "install",
                    "--id",
                    package_id,
                    "-e",
                    "--accept-package-agreements",
                    "--accept-source-agreements",
                ],
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def is_installed(self, package_id: str) -> bool:
        try:
            result = subprocess.run(
                ["winget", "list", "--id", package_id],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                check=True
            )
            return package_id.lower() in result.stdout.lower()
        except Exception:
            return False
