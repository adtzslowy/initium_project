from typing import List

from .core.installer import Installer
from .core.package_manager.registry import DEV_TOOLS

class InitiumApp:
    """
    High-level application interface untuk Initium.
    UI / CLI hanya boleh berinteraksi lewat class ini.
    """

    def __init__(self):
        self.installer = Installer()

    def list_tools(self) -> List[str]:
        """
        Mengembalikan list key dev tools yang tersedia.
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
