import { test, expect } from '@playwright/test';

/**
 * Tests for the Project Grandma docs site.
 * Start the docs server yourself first (no Playwright auto-start):
 *   cd docs && npm run build && npm run preview
 * Then from grandama: npm run test
 */
test.describe('Docs site', () => {
  test('welcome page has title and main content', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Project Grandma|Grandma/i);
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  });

  test('docs navigation is present', async ({ page }) => {
    await page.goto('/');
    const nav = page.getByRole('navigation', { name: 'Main' });
    await expect(nav).toBeAttached();
    await expect(page.getByRole('link', { name: /welcome|installation/i }).first()).toBeAttached();
  });

  test('opens Chrome, visits 3 docs pages, then closes', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Project Grandma|Grandma/i);

    await page.goto('/welcome/');
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();

    await page.goto('/installation/');
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  });
});
