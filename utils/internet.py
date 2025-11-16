import subprocess

def is_winget_available():
    return (
        subprocess.call(
            ["where", "winget"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        == 0
    )
