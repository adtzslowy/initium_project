from re import sub
import subprocess
from typing import Callable

from .base import BasePackageManager

class WingetPackageManager(BasePackageManager):
    @property
    def name(self) -> str:
        return "winget"
    
    def is_installed(self, pacakge_id: str) -> bool:
        try:
            result = subprocess.run(
                ["winget", "list", "--id", pacakge_id],
                capture_output=True,
                text=True
            )
            return pacakge_id.lower() in result.stdout.lower()
        except Exception:
            return False

    
    # ------------------------------------------
    # Silent Install (used by CI or Dry-run)
    # ------------------------------------------
    def install(self, pacakge_id: str) -> bool:
        try:
            result = subprocess.run(
                ["winget", "install", "--id", pacakge_id, "-e", "--silent", "--accept-source-agreements", "--accept-package-agreements"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False

    # ------------------------------------------
    # Streaming install for UI
    # ------------------------------------------
    def install_with_log(self, package_id: str, on_output: Callable[[str], None]) -> bool:
        try:
            cmd = [
                "winget", "install", "--id", package_id, "-e", "--accept-source-agreements", "--accept-package-agreements"
            ]

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            for line in process.stdout:
                clean = line.strip()
                if clean:
                    on_output(clean)

            process.wait()
            return process.returncode == 0

        except Exception as e:
            on_output(str(e))
            return False
