import subprocess
from .base import BasePackageManager

class ChocoPackageManager(BasePackageManager):
    @property
    def name(self) -> str:
        return "choco"

    def is_available(self) -> bool:
        try:
            subprocess.run(
                ["choco", "-v"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            return True
        except Exception:
            return False

    def install(self, package_id: str) -> bool:
        try:
            subprocess.run(
                [
                    "choco",
                    "install",
                    package_id,
                    "-y"
                ],
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def is_installed(self, pacakge_id: str) -> bool:
        try:
            result = subprocess.run(
                [
                    "choco",
                    "list",
                    "--local-only",
                    "--exact",
                    pacakge_id
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                check=True
            )
            return pacakge_id.lower() in result.stdout.lower()
        except Exception:
            return False
