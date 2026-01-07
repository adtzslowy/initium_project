from dataclasses import dataclass
from typing import Dict, Optional

@dataclass(frozen=True)
class DevTool:
    key: str
    name: str
    description: str
    winget: Optional[str] = None
    choco: Optional[str] = None


DEV_TOOLS: Dict[str, DevTool] = {
    "git": DevTool(
        key="git",
        name="Git",
        description="Version control system",
        winget="Git.Git",
        choco="git"
    ),
    "nodejs": DevTool(
        key="nodejs",
        name="Node.js",
        description="Javascript runtime",
        winget="OpenJS.NodeJS",
        choco="nodejs"
    ),
    "vscode": DevTool(
        key="vscode",
        name="Visual Studio Code",
        description="Source code editor",
        winget="Microsoft.VisualStudioCode",
        choco="vscode"
    ),
    "xampp": DevTool(
        key="xampp",
        name="XAMPP",
        description="Free PHP development environment",
        winget="ApacheFriends.Xampp",
        choco="xampp"
    ),
    "laragon": DevTool(
        key="laragon",
        name="Laragon",
        description="Advanced PHP dev environment (with license required for latest version)",
        winget="LeNgocKhoa.Laragon",
        choco="laragon"
    )
}
