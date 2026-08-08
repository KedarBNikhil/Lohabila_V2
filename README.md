# Lohabila BackupAgent Installer

A Windows installer wizard for **Lohabila BackupAgent**, the backup client used by [Lohabila Systems](https://github.com/KedarBNikhil) — a backup and storage managed service provider (MSP). This repo packages the agent's install, license/backend registration, and Windows service setup into a guided desktop wizard.

## What this does

- Provides a **GUI installer wizard** (built with PySide6/Qt) that walks a customer through installing the BackupAgent on Windows.
- Handles **backend registration** using a license key, connecting the agent to the Lohabila backend.
- Sets up the agent as a **Windows service** so backups run automatically in the background.
- Includes a lightweight local API layer (FastAPI + Uvicorn) for the agent to communicate with the installer/backend during setup.

## Tech stack

| Component        | Tech                          |
|-------------------|-------------------------------|
| Installer UI      | PySide6 (Qt for Python)       |
| Local API/service | FastAPI, Uvicorn              |
| Config validation | Pydantic                      |
| Backup engine     | PowerShell script (invoked by the agent) |

## Project structure

```
Lohabila_V2/
├── BackupAgent/         # Core backup agent
├── build/BackupAgent/   # Build output for the packaged agent
├── config/              # Configuration files
├── src/                 # Installer application source (wizard logic)
├── backup_page.ui       # Qt Designer UI file for the installer wizard
├── main.py              # Entry point — launches the InstallerWizard
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (not committed with real values)
```

## Getting started

### Prerequisites

- Windows 10/11
- Python 3.10+

### Installation

```bash
git clone https://github.com/KedarBNikhil/Lohabila_V2.git
cd Lohabila_V2
pip install -r requirements.txt
```

### Running the installer wizard

```bash
python main.py
```

This launches the `InstallerWizard`, which guides you through:
1. Accepting install location and prerequisites
2. Entering a license key to register the agent with the Lohabila backend
3. Installing the BackupAgent as a Windows service

## Configuration

Copy `.env.example` (create one if it doesn't exist yet) to `.env` and fill in the required values before running the installer. **Do not commit real credentials or license keys** — add `.env` to `.gitignore` if it isn't already.

## Status

This project is under active development as part of Lohabila Systems' core backup product. Expect breaking changes.

## License

Proprietary — © Lohabila Systems. All rights reserved.
