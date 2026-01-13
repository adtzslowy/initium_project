import subprocess
from typing import Callable
from .base import BasePackageManager

class WingetPackageManager(BasePackageManager):

    @property
    def name(self):
        return "winget"

    def is_installed(self, package_id: str) -> bool:
        try:
            result = subprocess.run(
                ["winget", "list", "--id", package_id],
                capture_output=True,
                text=True
            )
            return package_id.lower() in result.stdout.lower()
        except:
            return False

    def install(self, package_id: str) -> bool:
        try:
            return subprocess.run(
                ["winget", "install", "--id", package_id, "-e",
                 "--accept-source-agreements", "--accept-package-agreements"],
                capture_output=True
            ).returncode == 0
        except:
            return False

    def install_with_log(self, package_id: str, on_output: Callable[[str], None]) -> bool:
        try:
            process = subprocess.Popen(
                ["winget", "install", "--id", package_id, "-e",
                 "--accept-source-agreements", "--accept-package-agreements"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            for line in process.stdout:
                if line.strip():
                    on_output(line.strip())

            process.wait()
            return process.returncode == 0
        except Exception as e:
            on_output(str(e))
            return False

