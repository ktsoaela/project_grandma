# Project Grandma

<div align="center">
  <img src="./assets/old-woman-c.png" alt="Project Grandma" width="120" height="120">
</div>

A simple step recorder designed for explaining tasks clearly — like showing your grandma how to do something, one step at a time.

**Project Grandma** captures screenshots on every click and lets you add helpful notes, so anyone can follow along easily.

---

## What It Does

Project Grandma records step-by-step instructions by:

* Capturing a screenshot on every mouse click
* Logging what was clicked (on Windows)
* Letting you add comments between steps
* Generating a clean, easy-to-follow report

It’s perfect for:

* Teaching someone how to use an app
* Documenting a process
* Creating beginner-friendly tutorials

---

## Stack

* **UI**: Electron (Node.js)
* **Recording Engine**: Python (pynput + mss + Flask)
* **Exports**:

  * HTML (step-by-step guide)
  * Optional **PDF**
  * Optional **Markdown** (.md + images folder)
  * Optional **Video** (MP4)

On **Windows**, step descriptions include details like:

> “User left click on ‘element (type)’ in ‘window title’”

Additional info may include:

* Program name
* UI elements under cursor

(Uses `uiautomation` for Windows element detection.)

---

## Prerequisites

Before starting, make sure you have:

1. **Node.js**
2. **Python 3** (with pip)

---

## Setup

### Install Node dependencies (Electron)

```bash
cd project-grandma
npm install
```

### Install Python dependencies (Recorder)

```bash
cd recorder
pip install -r requirements.txt
```

Or from the root folder:

```bash
pip install -r recorder/requirements.txt
```

---

## Run Project Grandma

From the project root:

```bash
cd project-grandma
npm start
```

### PowerShell version:

```powershell
cd project-grandma; npm start
```

If you’re already inside the folder:

```bash
npm start
```

---

## Run Everything Together (Recommended for Development)

To run both the Electron interface and the Python recorder server at once:

```bash
cd project-grandma
npm run dev
```

PowerShell:

```powershell
cd project-grandma; npm run dev
```

### Available Scripts

* `npm start` → Starts Electron. Python launches automatically when you click **Start Record**.
* `npm run dev` → Starts Electron + Python server together.
* `npm run start:electron` → Electron only
* `npm run start:python` → Python server only

---

## How to Use (Grandma Style)

### Choose Options (Before Starting)

* **Number of recent screen captures to store** (default: 25)
* **Record video (MP4)** – optional
* **Export format(s)**:

  * HTML (always available)
  * PDF
  * Markdown

---

### Click “Start Record”

Recording begins.

* Every **mouse click** becomes a step.
* A screenshot is taken automatically.
* On Windows, it describes what you clicked.
* **Keyboard activity** is logged (but typed text is not saved — just like PSR).

---

### Add Comment (Optional)

Click **Add Comment** to explain something in plain language.
This creates a new step with a screenshot and your note.

Perfect for adding things like:

> “Now click here.”
> “Don’t forget to save before closing.”

---

### Click “Stop Record”

Project Grandma generates your guide in your temp folder:

Examples:

```
%TEMP%\ProjectGrandma_YYYYMMDD_HHMMSS.html
%TEMP%\ProjectGrandma_YYYYMMDD_HHMMSS.pdf
%TEMP%\ProjectGrandma_YYYYMMDD_HHMMSS.md
%TEMP%\ProjectGrandma_YYYYMMDD_HHMMSS.mp4
```

---

### Open and Share

Use the Open buttons to launch:

* HTML guide
* PDF
* Markdown
* Video

Now you can send it to anyone who needs step-by-step help

---

## Project Structure

* **project-grandma/** → Electron app (UI, main process, preload)
* **recorder/** → Python recording server

  * `server.py` → API (start, stop, comment, state)
  * `capture.py` → Mouse + keyboard listener, screenshots
  * `video_capture.py` → Optional MP4 recording
  * `win_info.py` → Windows UI + process info
  * `report.py` → Generates HTML, PDF, Markdown

---

## Inspiration

Inspired by Microsoft’s Problem Steps Recorder:

`C:\Windows\System32\psr.exe`


image:
https://www.flaticon.com/free-icon/old-woman_3544776?related_id=3544852&origin=search

But friendlier. Simpler. Grandma-approved.
