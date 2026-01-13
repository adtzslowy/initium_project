from typing import Optional
import platform
import os

from .package_manager.registry import DEV_TOOLS, DevTool
from .package_manager.resolver import PackageManagerResolver
from .package_manager.base import BasePackageManager

class Installer:
    """
    Orchestrator untuk proses installasi dev dependencies.
    """
    def __init__(self, package_manager=None, dry_run: bool = False):
        self.dry_run = dry_run


        if os.getenv("INITIUM_MODE") == "ci":
            from .package_manager.mock import MockPackageManager
            self.pm = MockPackageManager()
            self.dry_run = True
            return

        current_os = platform.system()
        if current_os != "Windows":
            raise RuntimeError(
                f"Initium currently supports Windows only (detected: {current_os})"
            )

        if package_manager:
            self.pm = package_manager
        else:
            resolver = PackageManagerResolver()
            self.pm = resolver.resolve()

        if not self.pm:
            raise RuntimeError("No supported package manager found on this system")

    def install(self, tool_key: str) -> bool :
        """
        Install dev tool berdasarkan key registry.
        Return true jika sukses, False jika gagal.
        """
        tool = self._get_tool(tool_key)

        if self.pm.name == "mock":
            return self.pm.install(tool_key)

        package_id = self._get_package_id(tool)

        if not package_id:
            raise RuntimeError(
                f"{tool.name} is not supported by {self.pm.name}"
            )

        if self.pm.is_installed(package_id):
            return True

        return self.pm.install(package_id)

    def _get_tool(self, tool_key: str) -> DevTool :
        try:
            return DEV_TOOLS[tool_key]
        except KeyError:
            raise ValueError(f"Unknown dev tool: {tool_key}")

    def _get_package_id(self, tool: DevTool) ->  Optional[str]:
        """
        Ambil package ID sesuai dengan package manager aktif
        """

        if self.pm.name == "winget":
            return tool.winget
        if self.pm.name == "choco":
            return tool.choco
        return None
