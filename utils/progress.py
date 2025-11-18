import time
import threading
import urllib
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
                percentage += 0.5
            elif percentage < 70:
                percentage += 0.1
            elif percentage < 95:
                percentage += 0.01
            else:
                percentage += 0.2

            if percentage > 99:
                percentage = 99

            progress.update(task, completed=percentage)

        progress.update(task, completed=100)
        time.sleep(0.3)

def download_file_with_progress(url, output, stop_event):
    response = urllib.request.urlopen(url)
    total_size = int(response.getheader("Content-Length").strip())
    downloaded = 0
    block_size = 8192

    with open(output, "wb") as f:
        while True:
            chunk = response.read(block_size)
            if not chunk:
                break

            f.write(chunk)
            downloaded += len(chunk)

    stop_event.set()
