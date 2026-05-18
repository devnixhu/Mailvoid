<div align="center">

# ✉ MAILVOID

**A sleek desktop email client for Resend.**  
*by: Devnixhu*
Send transactional emails, manage batches, track delivery — beautifully.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Resend](https://img.shields.io/badge/Made%20For-Resend-000000?style=flat-square)](https://resend.com)
[![License](https://img.shields.io/badge/License-MIT-7c3aed?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-38bdf8?style=flat-square)]()

</div>

---

## What is MAILVOID?

MAILVOID is a lightweight desktop app that lets you send and manage emails through the [Resend](https://resend.com) API — without writing a single line of code. It features drag & drop attachments, saved API keys, and full email management.

---

## Features

| | Feature | Description |
|---|---|---|
| ✉ | **Compose & Send** | Write emails in plain text or HTML with live preview |
| 🚀 | **Batch Sending** | Send to multiple recipients in one click via Resend Batch API |
| 📎 | **Attachments** | Drag & drop any file up to 25 MB |
| 🔑 | **Saved API Keys** | Store multiple keys locally by name — switch between them instantly |
| 📋 | **Email Tracking** | List all sent emails, see delivery status in real time |
| 🔍 | **Email Inspector** | View full details of any sent email (to, from, subject, status, timestamps) |

---

## Installation

### Windows — Executable (recommended)

1. Go to the [**Releases**](../../releases) page
2. Download the latest `Mailvoid.exe`
3. Run it — no installation needed

> ⚠️ Windows may show a SmartScreen warning since the app isn't code-signed. Click **More info → Run anyway** to proceed.

### macOS / Linux — Run from source

**Requirements:** Python 3.9+

```bash
# 1. Clone the repo
git clone https://github.com/devnixhu/mailvoid.git
cd mailvoid

# 2. Install dependencies
pip install pywebview resend

# 3. Run
python Mailvoid.py
```

---

## Getting Started

1. Launch the app — you'll be greeted by the welcome screen
2. Head to the **API Keys** tab and save your [Resend API key](https://resend.com/api-keys) with a name
3. Switch to **Compose**, pick your key from the dropdown
4. Fill in sender, recipients, subject and body — then hit **Send**

---

## Project Structure

```
mailvoid/
├── Mailvoid.py            # Python backend — pywebview + Resend API
├── Mailvoid.html        # Frontend — HTML / CSS / JS
├── saved_keys.json   # Auto-created — local API key storage
└── Wallpaper.mp4     # Background video (optional)
```

---

## Security & API Keys

- Keys are saved in `saved_keys.json` **locally on your device only**
- They are never transmitted anywhere except directly to Resend's API
- If you fork or modify this project, make sure to add `saved_keys.json` to `.gitignore`:

```
saved_keys.json
```

> The developer is not responsible for any misuse, data loss, or unauthorized access resulting from how you store or share your API keys.

---

## Building the Executable Yourself

```bash
pip install pyinstaller

pyinstaller --onefile --windowed \
  --add-data "Mailvoid.html;." \
  --add-data "Wallpaper.mp4;." \
  Mailvoid.py
```

Output will be in the `dist/` folder.

---

## License

[MIT](LICENSE) — free to use, modify, and distribute.

---

<div align="center">
  <sub>Built with ❤️ Devnixhu </sub>
</div>
