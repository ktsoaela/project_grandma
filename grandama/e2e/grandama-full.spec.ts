import { test, expect } from '@playwright/test';
import path from 'path';
import fs from 'fs';
import { execSync } from 'child_process';

const grandamaDir = path.join(__dirname, '..');
const exportPathsFile = path.join(grandamaDir, '.playwright-export-paths.json');
const docsUrl = process.env.BASE_URL || 'http://localhost:4321';

/** Chrome content area offset from window top-left (title bar + tabs + address bar). */
const CHROME_OFFSET_X = 10;
const CHROME_OFFSET_Y = 100;

/** Get (Left, Top) of a window. Pass title substring (e.g. "localhost") to get browser window; omit for foreground. */
function getWindowBounds(titlePart?: string): { x: number; y: number } {
  const scriptPath = path.join(grandamaDir, 'scripts', 'get-window-bounds.ps1');
  const arg = titlePart ? ` "${titlePart.replace(/"/g, '""')}"` : '';
  const out = execSync(`powershell -ExecutionPolicy Bypass -File "${scriptPath}"${arg}`, {
    encoding: 'utf8',
    windowsHide: true,
  });
  const [x, y] = out.trim().split(/\s+/).map(Number);
  if (Number.isNaN(x) || Number.isNaN(y)) throw new Error('Could not get window bounds (PowerShell script failed)');
  return { x, y };
}

/**
 * Python: move mouse to (screenX, screenY) and perform a real OS left-click.
 * Used so the recorder (pynput) sees real input; Playwright never clicks in the browser.
 */
function pythonMoveAndClick(screenX: number, screenY: number): void {
  const pyScript = path.join(grandamaDir, 'scripts', 'real_click.py');
  const py = process.platform === 'win32' ? 'python' : 'python3';
  execSync(`"${py}" "${pyScript}" ${screenX} ${screenY}`, { cwd: grandamaDir, stdio: 'inherit' });
}

/**
 * For a browser target: use Playwright to get the button/link coordinates, then Python to move and click.
 * Playwright only locates the element and returns screen coordinates; Python does the actual move + click
 * so the recorder captures real OS input.
 */
async function realClickAtElement(page: import('@playwright/test').Page, selector: string): Promise<void> {
  await page.bringToFront();
  await new Promise((r) => setTimeout(r, 500));
  // 1) Playwright: get target position (viewport-relative bounding box)
  const box = await page.locator(selector).first().boundingBox();
  if (!box) throw new Error(`Element not found or not visible: ${selector}`);
  // 2) Convert to screen coordinates (browser window by current page title so we get Chromium, not Electron)
  const pageTitle = await page.title();
  const windowBounds = getWindowBounds(pageTitle);
  const screenX = Math.round(windowBounds.x + CHROME_OFFSET_X + box.x + box.width / 2);
  const screenY = Math.round(windowBounds.y + CHROME_OFFSET_Y + box.y + box.height / 2);
  // 3) Python: move to target and click (real OS events for the recorder)
  pythonMoveAndClick(screenX, screenY);
  await new Promise((r) => setTimeout(r, 1500));
}

/**
 * Full flow: start Project Grandma, set options, start recording, open Chrome to docs,
 * then real OS-level clicks on 3 sidebar links (Welcome, Installation, Quick start)
 * so the recorder captures steps. Then stop recording and open exports.
 */
test.describe('Grandma full flow', () => {
  test('start Grandma, check options, record, browse 3 docs pages, stop, open HTML/PDF/MD', async ({
    page: browserPage,
  }) => {
    test.setTimeout(120_000);
    const { _electron: electron } = require('playwright-core');

    const electronApp = await test.step('Launch Project Grandma (Electron)', async () => {
      const app = await electron.launch({
        cwd: grandamaDir,
        args: ['.'],
      });
      const win = await app.firstWindow();
      await win.waitForLoadState('domcontentloaded');
      return { app, win };
    });

    const { app: electronAppInstance, win: appWindow } = electronApp;

    await test.step('Check Record video, Export HTML, PDF, Markdown', async () => {
      await appWindow.getByRole('checkbox', { name: /record video/i }).check();
      await appWindow.getByRole('checkbox', { name: /export as html/i }).check();
      await appWindow.getByRole('checkbox', { name: /export as pdf/i }).check();
      await appWindow.getByRole('checkbox', { name: /export as markdown/i }).check();
    });

    await test.step('Start recording', async () => {
      await appWindow.getByRole('button', { name: /start record/i }).click();
      await expect(appWindow.getByRole('button', { name: /stop record/i })).toBeVisible({
        timeout: 15000,
      });
    });

    await test.step('Open Chrome and go to docs at ' + docsUrl, async () => {
      await browserPage.setViewportSize({ width: 1280, height: 720 });
      await browserPage.goto(docsUrl + '/');
      await expect(browserPage).toHaveTitle(/Project Grandma|Grandma/i);
    });

    await test.step('Click Welcome link (real OS click so recorder captures it)', async () => {
      await realClickAtElement(browserPage, 'a[href*="/welcome/"]');
    });
    await test.step('Click Installation link (real OS click)', async () => {
      await realClickAtElement(browserPage, 'a[href*="/installation/"]');
    });
    await test.step('Click Quick start link (real OS click)', async () => {
      await realClickAtElement(browserPage, 'a[href*="/quick-start/"]');
    });

    await test.step('Close Chrome (browser)', async () => {
      await browserPage.close();
    });

    await test.step('Stop recording in Grandma', async () => {
      await appWindow.getByRole('button', { name: /stop record/i }).click();
      await expect(appWindow.locator('#save-dialog:not(.hidden)')).toBeVisible({ timeout: 30000 });
    });

    await test.step('Save export paths for report script', async () => {
      const htmlPath = await appWindow.locator('.save-btn[data-format="html"]').getAttribute('data-path');
      const mdPath = await appWindow.locator('.save-btn[data-format="md"]').getAttribute('data-path');
      if (htmlPath || mdPath) {
        fs.writeFileSync(exportPathsFile, JSON.stringify({ htmlPath: htmlPath || null, mdPath: mdPath || null }, null, 2));
      }
    });

    await test.step('Open HTML, Open Markdown, Open PDF in save dialog', async () => {
      for (const name of [/open html/i, /open markdown/i, /open pdf/i]) {
        const btn = appWindow.getByRole('button', { name });
        if (await btn.isVisible()) await btn.click();
      }
    });

    await test.step('Click Done and close Grandma', async () => {
      await appWindow.getByRole('button', { name: /done/i }).click();
      await electronAppInstance.close();
    });
  });
});
