from rich import table
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.status import Status
from rich.panel import Panel
from rich.align import Align

from src.initium.app import InitiumApp

console = Console()

def render_header():
    header = Panel(
        Align.center(
            "[bold cyan]Initium[/bold cyan]\n"
            "[white]DEV DEPENDENCIES INSTALLER[/white]\n",
            vertical="middle"
        ),
        border_style="cyan",
        padding=(1, 4)
    ),
    console.print(header)

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
    tools = render_tools(app)
    
    choice = Prompt.ask(
        "\n[bold]Select tool number to install[/bold]",
        choices=[str(i) for i in range(1, len(tools) + 1)]
    )

    tool_key = tools[int(choice) - 1]
    tool_info = app.get_tool_info(tool_key)

    console.print(
        Panel(
            f"[bold]Installing:[/bold] [cyan]{tool_info['name']}[/cyan]",
            border_style="green"
        )
    )

    with Status("[green]Working....[/green]", console=console):
        success = app.install_tool(tool_key)

    if success:
        console.print(
            Panel(
                f"[green]✔ {tool_info['name']} installed successfullty[/green]",
                border_style="green"
            )
        )
    else:
        console.print(
            Panel(
                f"[red]✖ Failed to install {tool_info['name']}[/red]",
                border_style="red"
            )
        )

    console.print(
        Align.center(
            "[dim]Tip: Run initium anytime to install more tools[/dim]",
            vertical="middle"
        )
    )

if __name__ == "__main__":
    main()
