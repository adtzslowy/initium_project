from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.status import Status
from rich.panel import Panel
from rich.align import Align

import os

from ..app import InitiumApp

console = Console()


# =========================
# UI HELPERS
# =========================

def render_header():
    header = Panel(
        Align.center(
            "[bold cyan]Initium[/bold cyan]\n"
            "[white]DEV DEPENDENCIES INSTALLER[/white]\n",
            vertical="middle"
        ),
        border_style="cyan",
        padding=(1, 4)
    )
    console.print(header)


def run_with_ui(label: str, action):
    """
    Run an action with Rich UI.
    In CI mode, UI is disabled automatically.
    """
    if os.getenv("INITIUM_MODE") == "ci":
        return action()

    with Status(f"[bold cyan]{label}[/bold cyan]", spinner="dots"):
        return action()


# =========================
# RENDERERS
# =========================

def render_tools(app: InitiumApp):
    tools = app.list_tools()

    table = Table(
        title="Available Tools",
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


def render_presets(app: InitiumApp):
    presets = app.list_presets()

    table = Table(
        title="Available Presets",
        header_style="bold magenta",
        box=None
    )

    table.add_column("No", justify="right", style="bold")
    table.add_column("Preset", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")

    for i, key in enumerate(presets, start=1):
        info = app.get_preset_info(key)
        table.add_row(str(i), info["name"], info["description"])

    console.print(table)
    return presets


# =========================
# MAIN
# =========================

def main():
    render_header()
    app = InitiumApp()

    # -------------------------
    # Choose mode
    # -------------------------
    if os.getenv("INITIUM_MODE") == "ci":
        mode = "tool"
    else:
        mode = Prompt.ask(
            "[bold]Mau pilih instalasi yang mana?[/bold]",
            choices=["tool", "preset"],
            default="tool"
        )

    # =========================
    # TOOL MODE
    # =========================
    if mode == "tool":
        tools = render_tools(app)

        if os.getenv("INITIUM_MODE") == "ci":
            tool_key = tools[0]
        else:
            choice = Prompt.ask(
                "[bold]Pilih tool yang ingin di install[/bold]",
                choices=[str(i) for i in range(1, len(tools) + 1)]
            )
            tool_key = tools[int(choice) - 1]

        tool_info = app.get_tool_info(tool_key)

        console.print(
            Panel(
                f"[bold]Installing:[/bold] {tool_info['name']}",
                border_style="cyan"
            )
        )

        success = run_with_ui(
            f"Installing {tool_info['name']}",
            lambda: app.install_tool(tool_key)
        )

        if success:
            console.print(f"[green]✔ {tool_info['name']} installed[/green]")
        else:
            console.print(f"[red]✖ Failed to install {tool_info['name']}[/red]")

        return

    # =========================
    # PRESET MODE
    # =========================
    if mode == "preset":
        presets = render_presets(app)

        if os.getenv("INITIUM_MODE") == "ci":
            preset_key = presets[0]
        else:
            choice = Prompt.ask(
                "[bold]Pilih preset yang ingin di install[/bold]",
                choices=[str(i) for i in range(1, len(presets) + 1)]
            )
            preset_key = presets[int(choice) - 1]

        preset_info = app.get_preset_info(preset_key)

        console.print(
            Panel(
                f"[bold]Installing preset:[/bold] {preset_info['name']}\n"
                f"[white]{preset_info['description']}[/white]",
                border_style="cyan"
            )
        )

        results = {}

        for tool_key in preset_info["tools"]:
            tool_info = app.get_tool_info(tool_key)

            ok = run_with_ui(
                f"Installing {tool_info['name']}",
                lambda k=tool_key: app.install_tool(k)
            )

            results[tool_key] = ok

        success_count = sum(1 for ok in results.values() if ok)
        total = len(results)

        console.print(
            Panel(
                f"[green]{success_count}/{total} tools installed successfully[/green]",
                title="Done",
                border_style="green"
            )
        )

        return


if __name__ == "__main__":
    main()

