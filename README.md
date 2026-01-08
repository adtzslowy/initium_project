# Initium

Initium is a simple and transparent CLI tool for installing common development
dependencies on Windows using available package managers such as **winget**
and **Chocolatey**.

This project focuses on **clarity, safety, and maintainability** rather than
hidden automation or system magic.

---

## ✨ Features

- Install common dev tools from a single CLI
- Automatically selects available package manager (winget / choco)
- Clean and readable CLI interface (powered by Rich)
- CI-safe with mock mode
- Minimal and predictable behavior

---

## 🚧 Project Status

- **Early stage** (`v0.x`)
- **Windows only** (for real installations)
- Core architecture is stable
- Features and UX may evolve

Initium is currently intended for learning, experimentation, and internal use.

---

## 🖥 Supported Platform

| Platform | Status |
|--------|--------|
| Windows | ✅ Supported |
| macOS  | ⚠️ Dev / CI only |
| Linux  | ⚠️ Dev / CI only |

> On macOS and Linux, Initium runs in **mock mode** for development and CI.
> Actual system installation is Windows-only.

---

## 🚀 Usage

### Run locally

```bash
python -m src.initium.ui.cli

