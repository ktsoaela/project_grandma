import { defineConfig } from 'astro/config';
import mermaid from 'astro-mermaid';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    // Mermaid must come before Starlight so markdown code blocks are transformed correctly
    mermaid(),
    starlight({
      title: 'Project Grandma',
      logo: {
        src: './src/assets/logo.png',
        alt: 'Project Grandma Logo'
      },
      description: 'Grandma-approved step recorder for Windows and macOS',
      favicon: '/src/assets/logo.png',
      titleDelimiter: ' - ',
      head: [],
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/ktsoaela/project_grandma'
        },
      ],
      editLink: {
        baseUrl: 'https://github.com/ktsoaela/project_grandma/edit/main/docs/',
      },
      sidebar: [
        {
          label: 'Getting Started',
          items: [
            { label: 'Welcome', slug: 'welcome' },
            { label: 'Installation', slug: 'installation' },
            { label: 'Quick Start', slug: 'quick-start' },
          ],
        },
        {
          label: 'User Guide',
          items: [
            { label: 'How to Record', slug: 'guide/recording' },
            { label: 'Add Comments', slug: 'guide/comments' },
            { label: 'Export Formats', slug: 'guide/export' },
            { label: 'Export Comparison (Chart)', slug: 'guide/export-chart' },
            { label: 'Tips & Tricks', slug: 'guide/tips' },
          ],
        },
        {
          label: 'Features',
          items: [
            { label: 'Windows Support', slug: 'features/windows' },
            { label: 'macOS Support', slug: 'features/macos' },
            { label: 'Export Options', slug: 'features/exports' },
            { label: 'Video Recording', slug: 'features/video' },
            {
              label: 'Click Circle',
              items: [
                { label: 'Overview', slug: 'features/click-circle' },
                { label: 'Quick Reference', slug: 'features/click-circle/quick-reference' },
                { label: 'Feature Guide', slug: 'features/click-circle/feature' },
                { label: 'Visual Guide', slug: 'features/click-circle/visual-guide' },
                { label: 'Implementation', slug: 'features/click-circle/implementation' },
              ],
            },
          ],
        },
        {
          label: 'Help',
          items: [
            { label: 'FAQ', slug: 'help/faq' },
            { label: 'Troubleshooting', slug: 'help/troubleshooting' },
            { label: 'Common Issues', slug: 'help/issues' },
          ],
        },
        {
          label: 'Development',
          items: [
            { label: 'Project Structure', slug: 'dev/structure' },
            { label: 'Building from Source', slug: 'dev/build' },
            { label: 'E2E Testing (Playwright)', slug: 'dev/playwright-e2e' },
            { label: 'Contributing', slug: 'dev/contributing' },
            { label: 'Architecture', slug: 'dev/architecture' },
          ],
        },
      ],
    }),
  ],
});
