---
title: E2E Testing with Playwright
description: Run end-to-end tests for the docs site and full Grandma recording flow
---

Project Grandma uses [Playwright](https://playwright.dev/) for end-to-end tests. Tests live in **grandama/e2e/** and cover both the documentation site and the full recording flow (Electron app + real OS clicks).

## Quick start

From the **grandama** directory:

```bash
npm run test
```

This will:

1. Build and start the docs server (if not already running).
2. Open Chromium, go to the docs at `http://localhost:4321/`, run all tests (including visiting key docs pages), then close the browser.
3. Exit (the docs server stops when Playwright exits).

If the docs are already running at `http://localhost:4321`, Playwright reuses that server.

**First-time:** install the browser:

```bash
npx playwright install chromium
```

## Test types

### Docs-only tests

- **What:** Playwright navigates to the docs site and runs tests (e.g. visiting Welcome, Installation, Quick start).
- **Where:** `grandama/e2e/docs.spec.ts`
- **Command:** `npm run test` (from grandama)

### Full flow (Grandma + docs + exports)

- **What:** Starts the Project Grandma Electron app, enables Record video + Export HTML/PDF/Markdown, starts recording, opens Chrome to the docs, then **clicks the Welcome, Installation, and Quick start links using real OS-level mouse events** (PowerShell + Python `pyautogui`) so the recorder captures each step. Then the test stops recording and opens the exported HTML, PDF, and Markdown.
- **Where:** `grandama/e2e/grandama-full.spec.ts`
- **Command:** `npm run test:full`

After a successful full run, a browser opens with three tabs:

1. **Playwright report** — test steps (same as `npx playwright show-report`)
2. **Grandma HTML export** — recorded steps as HTML
3. **Grandma Markdown export** — recorded steps as Markdown

**Requirements for full flow:**

- Recorder built: run `npm run build:recorder` from repo root (or have Python + `recorder/requirements.txt`).
- **Python with pyautogui:** `pip install pyautogui`
- **Windows** (for PowerShell window bounds). Keep the browser window in the foreground. Close the browser when done; press Ctrl+C in the terminal to stop the report server.

## Other commands

From **grandama**:

| Command | Description |
|--------|-------------|
| `npm run test` | Run all E2E tests (docs server started if needed) |
| `npm run test:full` | Full flow: Grandma + recording + real clicks + open exports |
| `npm run test:ui` | Playwright UI mode |
| `npm run test:headed` | See the browser while tests run |
| `npm run test:show` | Headed run of the “visits 3 docs pages” test only |

## Adding tests

Create `*.spec.ts` files in **grandama/e2e/**. Use `@playwright/test` and the existing specs as reference.

## Technical note: real clicks in full flow

In the full flow, Playwright **does not** perform clicks inside the browser. It is used to:

- Locate elements (e.g. sidebar links) and get their coordinates.
- Convert viewport coordinates to **screen** coordinates (browser window position + Chrome chrome offset).

A **Python script** (`grandama/scripts/real_click.py`) uses `pyautogui` to move the mouse and perform a real OS left-click at those screen coordinates. That way the recorder (pynput) sees real input and captures each step as a user would.

This keeps the E2E test representative of real usage while reusing Playwright for navigation and element lookup.
