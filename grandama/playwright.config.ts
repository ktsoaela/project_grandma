import { defineConfig, devices } from '@playwright/test';
import path from 'path';

/**
 * One command from grandama: npm run test
 * Playwright starts the docs server, runs tests (Chrome → localhost:4321 → 3 pages), then exits.
 * Set BASE_URL to use an already-running server instead of auto-starting.
 */
export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:4321',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: process.env.BASE_URL
    ? undefined
    : {
        command: 'npm run build && npm run preview',
        cwd: path.join(__dirname, '..', 'docs'),
        url: 'http://localhost:4321',
        reuseExistingServer: true,
        timeout: 120_000,
      },
});
