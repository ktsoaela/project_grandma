---
title: macOS Support
description: macOS-specific features and compatibility
---

Project Grandma supports macOS with DMG installers and universal binaries for Apple Silicon.

## macOS permissions for Project Grandma

In **System Settings → Privacy & Security**, enable these three:

1. **Input Monitoring** — needed to detect mouse clicks.
2. **Screen Recording** — needed to capture screenshots.
3. **Accessibility** — needed to detect window titles and UI element names (e.g. buttons).

### What to enable

- **During development (Terminal):** enable these for **Terminal**.
- **Using the built app:** enable these for **Project Grandma**.

### How to set them

1. Open **System Settings** (or **System Preferences** on older macOS).
2. Go to **Privacy & Security**.
3. Turn on each permission and allow the relevant app:
   - **Input Monitoring** → add/allow Terminal (or Project Grandma).
   - **Screen Recording** → add/allow Terminal (or Project Grandma).
   - **Accessibility** → add/allow Terminal (or Project Grandma).

You may need to restart Terminal or the app after enabling these.
