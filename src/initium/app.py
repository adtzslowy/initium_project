from typing import List

from .core.installer import Installer
from .core.package_manager.registry import DEV_TOOLS
from .core.preset import PRESETS

class InitiumApp:
    """
    High-level application interface untuk Initium.
    UI / CLI hanya boleh berinteraksi lewat class ini.
    """

    def __init__(self, dry_run: bool = False):
        self.installer = Installer(dry_run=dry_run)

    def list_tools(self) -> List[str]:
        """
        Mengembalikan list key dev tools yang tersedia.
	Code by adit
        """

        return list(DEV_TOOLS.keys())

    def get_tool_info(self, tool_key: str) -> dict:
        """
        Mengembalikan info tool untuk UI
        """

        tool = DEV_TOOLS.get(tool_key)
        if not tool:
            raise ValueError(f"Unknown dev tool: {tool_key}")

        return {
            "key": tool.key,
            "name": tool.name,
            "description": tool.description,
        }

    def install_tool(self, tool_key: str)-> bool:
        """
        Install satu dev tool
        """
        return self.installer.install(tool_key)

    def install_many(self, tool_keys: List[str])-> dict:
        """
        Install banyak dev tools.
        Return hasil per tool.
        """
        results = {}

        for key in tool_keys:
            try:
                results[key] = self.install_tool(key)
            except Exception as e:
                results[key] = False

        return results

    def list_presets(self) -> list[str]:
        return list(PRESETS.keys())

    def get_preset_info(self, preset_key: str) -> dict:
        preset = PRESETS.get(preset_key)
        if not preset:
            raise ValueError(f"Unknown preset: {preset_key}")
        return preset

    def install_preset(self, preset_key: str) -> dict:
        preset = self.get_preset_info(preset_key)

        result = {}
        for tool_key in preset["tools"]:
            try:
                result[tool_key] = self.install_tool(tool_key)
            except Exception:
                result[tool_key] = False
        return result
