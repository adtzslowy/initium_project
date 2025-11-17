import time
import threading
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

def run_progress_bar(stop_event, title="Processing"):
    with Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        TextColumn("{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        expand=True
    ) as progress:
        task = progress.add_task(title, total=100)
        percentage = 0

        while not stop_event.is_set():
            time.sleep(0.05)

            if percentage < 40:
                percentage += 2
            elif percentage < 70:
                percentage +=1
            elif percentage < 95:
                percentage += 0.5
            else:
                percentage += 0.2

            if percentage > 99:
                percentage = 99

            progress.update(task, completed=percentage)

        progress.update(task, completed=100)
        time.sleep(0.3)
