from .package_manager.resolver import PackageManagerResolver
from .package_manager.registry import DEV_TOOLS

class Installer:

    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.pm = PackageManagerResolver().resolve()

    def list_tools(self):
        return list(DEV_TOOLS.keys())

    def get_tool_info(self, key):
        tool = DEV_TOOLS[key]
        return {"name": tool.name, "description": tool.description}

    def _get_tool(self, key):
        return DEV_TOOLS[key]

    def _get_package_id(self, tool):
        if self.pm.name == "winget":
            return tool.winget
        return None

    def install(self, key):
        tool = self._get_tool(key)
        pid = self._get_package_id(tool)

        if self.pm.is_installed(pid):
            return True

        if self.dry_run:
            return True

        return self.pm.install(pid)

    def install_with_log(self, key, on_output):
        tool = self._get_tool(key)
        pid = self._get_package_id(tool)

        if self.pm.is_installed(pid):
            on_output("Already installed")
            return True

        if self.dry_run:
            on_output(f"[DRY-RUN] Would install {tool.name}")
            return True

        return self.pm.install_with_log(pid, on_output)

