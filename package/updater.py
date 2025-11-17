import asyncio
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import SpinnerColumn, BarColumn, TextColumn, Progress
from gh_auto_updater import update

console = Console()

def get_current_version():
    version_file = Path(__file__).parent / "VERSION"
    if version_file.exists():
        return version_file.read_text().strip()
    return "0.0.0"

async def self_update():
    console.print(Panel.fit("[bold green]Memeriksa pembaharuan...[/bold green]", title="Initium Updater"))

    try:
        install_dir = Path(__file__).parent
        current_version = get_current_version()
        with Progress(
            SpinnerColumn(),
            "[progress.description]{task.description}",
            BarColumn(),
            TextColumn("{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            task = progress.add_task("Downloading...", total=None)

            await update(
                repository_name="adtzslowy/initium_project",
                current_version=current_version,
                install_dir=install_dir
            )

            progress.update(task, advance=100)

        console.print(Panel(
            f"[green][✓] Update selesai![/green]\n[white]Versi terbaru sudah terpasang[/white]",
            title="Update Complate"
        ))

    except Exception as e:
        console.print(Panel(f"[red]Gagal updaet: {e}[/red]", title="Error"))
