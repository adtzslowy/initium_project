from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.status import Status
from rich.panel import Panel
from rich.align import Align

import os

from src.initium.app import InitiumApp

console = Console()

def render_header():
    header = Panel(
        Align.center(
            "[bold cyan]Initium[/bold cyan]\n",
            "[white]DEV DEPENDENCIES INSTALLER[/white]\n",
            vertical="middle"
        ),
        border_style="cyan",
        padding=(1, 4)
    ),
    console.print(header)

def render_presets(app: InitiumApp):
    presets = app.list_presets()

    table = Table(
        title="Available presets",
        header_style="bold magenta",
        box=None
    )

    table.add_column("No", justify="right", style="bold")
    table.add_column("Preset", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")

    for i, key in enumerate(presets, start=1):
        info = app.get_preset_info(key)
        table.add_row(
            str(i),
            info["name"],
            info["description"]
        )
    console.print(table)
    return presets

def render_tools(app: InitiumApp):
    tools = app.list_tools()

    table = Table(
        title="Available tools",
        header_style="bold magenta",
        box=None
    )

    table.add_column("No", justify="right", style="bold")
    table.add_column("Tool", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")

    for i, key in enumerate(tools, start=1):
        info = app.get_tool_info(key)
        table.add_row(str(i), info["name"], info["description"])

    console.print(table)
    return tools


def main():
    render_header()
    app = InitiumApp()

    # Choose mode
    if os.getenv("INITIUM_MODE") == "ci":
        mode = "tools"
    else:
        mode = Prompt.ask(
            "[bold]Mau pilih installasi yang mana?[/bold]",
            choices=["tool", "preset"],
            default="tool"
        )

    if mode == "tool":
        tools = render_tools(app)

        if os.getenv("INITIUM_MODE") == "ci":
            tool_key = tools[0]
        else:
            choice = Prompt.ask(
                "[bold]Pilih tool yang ingin di install.[/bold]",
                choices=[str(i) for i in range(1, len(tools) + 1)]
            )
            tool_key = tools[int(choice) - 1]

        tool_info = app.get_tool_info(tool_key)
        console.print(f"\n[bold]Installing:[/bold] {tool_info['name']}\n")

        success = app.install_tool(tool_key)
        return

    if mode == "preset":
        presets = render_presets(app)

        if os.getenv("INITIUM_MODE") == "ci":
            preset_key = presets[0]
        else:
            choice = Prompt.ask(
                "[bold]Pilih tool yang ingin di install.[/bold]",
                choices=[str(i) for i in range(1, len(presets) + 1)]
            )
            preset_key = presets[int(choice) - 1]

        console.print(f"\n[bold]Installing preset:[/bold] {preset_key}\n")
        results = app.install_preset(preset_key)

        for tool, ok in results.items():
            if ok:
                console.print(f"[green]✔ {tool}[/green]")
            else:
                console.print(f"[red]✖ {tool}[/red]")

        return
if __name__ == "__main__":
    main()
