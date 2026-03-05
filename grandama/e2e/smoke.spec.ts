import { test, expect } from '@playwright/test';

/**
 * Smoke tests. BASE_URL defaults to http://localhost:4321 (docs preview) in playwright.config.ts.
 */
test.describe('Smoke', () => {
  test('can load base URL', async ({ page }) => {
    const res = await page.goto('/');
    expect(res?.status()).toBeLessThan(500);
  });
});
