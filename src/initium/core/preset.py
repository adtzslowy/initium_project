from typing import Dict, List

PRESETS: Dict[str, dict] = {
    "web-dev": {
        "name": "Web Development",
        "description": "Git, Node.js, and Visual Studio Code",
        "tools": ["git", "nodejs", "vscode"]
    },
    "python-dev": {
        "name": "Python Development",
        "description": "Git and Python",
        "tools": ["git", "python"],
    },
    "php-dev": {
        "name": "PHP Development",
        "description": "Git, Laragon and XAMPP",
        "tools": ["git", "laragon", "xampp"]
    }
}
