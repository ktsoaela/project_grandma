# Project Grandma

<div align="center">
  <img src="./assets/old-woman-c.png" alt="Project Grandma" width="120" height="120">
</div>

A simple step recorder designed for explaining tasks clearly — like showing your grandma how to do something, one step at a time.

**[See Project Grandma →](https://ktsoaela.github.io/project_grandma/)**

**Project Grandma** captures screenshots on every click and lets you add helpful notes, so anyone can follow along easily. The page is [`site/index.html`](site/index.html). It is published from the `DEV` branch by GitHub Actions.

---

## What It Does

- Captures a screenshot on every mouse click and logs what was clicked (where supported)
- Lets you add comments between steps
- Exports to HTML, PDF, Markdown, and optional video (MP4)

Perfect for teaching someone how to use an app, documenting a process, or creating beginner-friendly tutorials.

---

## Documentation

Full documentation (installation, building, usage, macOS permissions, troubleshooting) is in the **[docs](./docs/)** site:

- [Welcome & getting started](./docs/src/content/docs/welcome.md)
- [Installation](./docs/src/content/docs/installation.md)
- [Quick start](./docs/src/content/docs/quick-start.md)
- [Recording guide](./docs/src/content/docs/guide/recording.md)
- [Export](./docs/src/content/docs/guide/export.md)
- [Export comparison (chart)](./docs/src/content/docs/guide/export-chart.mdx)
- [Building from source](./docs/src/content/docs/dev/build.md)
- [E2E testing (Playwright)](./docs/src/content/docs/dev/playwright-e2e.md)
- [macOS support & permissions](./docs/src/content/docs/features/macos.md)
- [Troubleshooting](./docs/src/content/docs/help/troubleshooting.md)

*(To serve the doc site locally: `cd docs && npm install && npm run build && npm run preview` or see the docs README.)*

---
