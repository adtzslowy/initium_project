from typing import Dict, List

PRESETS: Dict[str, dict] = {
    "backend-dev": {
        "name": "Backend Developer",
        "description": "Git, Node.Js, Docker, and Postman",
        "tools": ["git", "docker", "postman", "nodejs"],
    },

    "fullstack-dev": {
        "name": "Fullstack Developer",
        "description": "Git, Node.js, Docker, and Visual Studio Code",
        "tools": ["git", "nodejs", "docker", "vscode"],
    },

    "web-dev": {
        "name": "Web Developer",
        "description": "Git, Visual Studio Code, Node.js, Laragon",
        "tools": ["git", "vscode", "nodejs", "laragon"]
    },
}
