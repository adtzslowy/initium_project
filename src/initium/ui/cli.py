from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.prompt import Prompt
from initium.app import InitiumApp

console = Console()

def main(app):
    tools = app.list_tools()

    for i, t in enumerate(tools, 1):
        info = app.get_tool_info(t)
        console.print(f"{i}. {info['name']}")

    choice = Prompt.ask("Choose tool", choices=[str(i) for i in range(1, len(tools)+1)])
    key = tools[int(choice)-1]
    tool = app.get_tool_info(key)

    logs = []

    def on_log(line):
        logs.append(line)
        if len(logs) > 15:
            logs.pop(0)

    with Live(Panel("", title=f"Installing {tool['name']}", border_style="cyan"), refresh_per_second=4) as live:
        success = app.install_tool_with_log(key, on_log)
        live.update(Panel("\n".join(logs), title="Done", border_style="green" if success else "red"))


