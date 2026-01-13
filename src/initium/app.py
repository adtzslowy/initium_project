from .core.installer import Installer

class InitiumApp:

    def __init__(self, dry_run=False):
        self.installer = Installer(dry_run)

    def list_tools(self):
        return self.installer.list_tools()

    def get_tool_info(self, key):
        return self.installer.get_tool_info(key)

    def install_tool(self, key):
        return self.installer.install(key)

    def install_tool_with_log(self, key, on_output):
        return self.installer.install_with_log(key, on_output)

