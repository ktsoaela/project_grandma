# E2E tests (Playwright)

### One command

From **grandama**:

```bash
npm run test
```

This will:

1. Build and start the docs server (if not already running).
2. Open Chromium, go to http://localhost:4321/, run all tests (including visiting 3 docs pages), then close the browser.
3. Exit (docs server stops when Playwright exits).

If the docs are already running at http://localhost:4321, Playwright reuses that server.

### Full flow (Grandma + docs + report)

Runs Project Grandma (Electron), checks Record video + Export HTML/PDF/Markdown, starts recording, opens Chrome to the docs, then **clicks the Welcome, Installation, and Quick start links using real OS-level mouse events** (PowerShell + Python pyautogui) so the recorder captures each step. Then the test stops recording and opens the exported HTML, PDF, and Markdown. **After a successful run**, a browser opens with three tabs:

1. **Playwright report** – test steps (same as `npx playwright show-report`)
2. **Grandma HTML export** – recorded steps as HTML
3. **Grandma Markdown export** – recorded steps as Markdown

```bash
npm run test:full
```

Requires: the recorder (run `npm run build:recorder` from repo root, or Python + `recorder/requirements.txt`), **Python with pyautogui** (`pip install pyautogui`), and **Windows** (for PowerShell window bounds). Keep the browser window in the foreground. Close the browser when done; press Ctrl+C in the terminal to stop the report server.

### Other commands

```bash
npm run test:ui      # Playwright UI mode
npm run test:headed # See the browser while tests run
npm run test:show   # Headed run of the “visits 3 docs pages” test only
```

**First-time:** `npx playwright install chromium`

To add more tests, create `*.spec.ts` files in this folder.
