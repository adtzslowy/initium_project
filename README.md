# 🚀 Initium

**Initium** adalah CLI tool untuk menginstall dan men-setup *development environment* di Windows secara otomatis.

Dengan satu perintah, kamu bisa:
- Install Git, Node.js, Docker, VS Code, dll
- Setup environment sesuai role (Backend, Fullstack, Web)
- Melihat UI interaktif yang rapi
- Menjalankan simulasi tanpa mengubah sistem (dry-run)

> Initium = “Bootstrap environment developer dalam sekali jalan”

---

## ✨ Fitur

- 🔧 Install dev tools via **Winget** atau **Chocolatey**
- 📦 **Preset** untuk role developer
- 🧪 **Dry-run mode** (lihat rencana install tanpa benar-benar menginstall)
- 🎨 UI terminal modern (Rich)
- 🤖 CI-safe (Mock mode)

---

## 📦 Tools yang didukung

| Tool | Deskripsi |
|------|---------|
| Git | Version control |
| Node.js | JavaScript runtime |
| Visual Studio Code | Code editor |
| Docker Desktop | Container platform |
| Postman | API testing |
| XAMPP | PHP environment |
| Laragon | Advanced PHP environment |

---

## 🧩 Preset

| Preset | Tools |
|-------|------|
| **Backend Developer** | Git, Node.js, Docker, Postman |
| **Fullstack Developer** | Git, Node.js, Docker, VS Code |
| **Web Developer** | Git, Node.js, VS Code, Laragon |

Preset membuat Initium terasa seperti:
> “Setup environment sesuai pekerjaanmu”

---

## 🚀 Cara Menjalankan

### 1. Clone repository
```bash
git clone https://github.com/adtzslowy/initium_project
cd initium_project
```

### 2. Buat virtual environment
```bash
python -m venv venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Jalankan Initium
```bash
python -m src.initium.ui.cli
```

## 🧪 Dry Run (Simulasi)
```bash
python -m src.initium.ui.cli --dry-run
```

### Output
```bash
This will install:
- Git
- Node.js
- Docker
- Postman

No changes will be made.
```

## 🤖 CI Mode
Untuk melihat apa yang akan diinstall tanpa mengubah sistem:
```bash
INITIUM_MODE=ci python -m src.initium.ui.cli
```
Ini akan:
1. Tidak benar-benar menginstall apa pun
2. Tetap menampilkan alur dan UI

## ⚠ Catatan
1. Initium saat ini hanya mendukung Windows
2. Beberapa tool (Docker, VS, dll) bisa memakan waktu beberapa menit karena installer resmi Windows

## 📜 License
MIT License
