/**
 * After test:full, opens a browser with 3 tabs:
 * 1. Playwright HTML report (steps from the test run)
 * 2. Grandma exported HTML (recorded steps)
 * 3. Grandma exported Markdown (recorded steps)
 * Run from grandama: node scripts/open-full-report.js
 */
const http = require('http');
const fs = require('fs');
const path = require('path');

const grandamaDir = path.join(__dirname, '..');
const reportDir = path.join(grandamaDir, 'playwright-report');
const pathsFile = path.join(grandamaDir, '.playwright-export-paths.json');
function pathToFileURL(filePath) {
  if (!filePath) return null;
  const normalized = path.resolve(filePath).replace(/\\/g, '/');
  return 'file:///' + (normalized.startsWith('/') ? normalized.slice(1) : normalized);
}

async function main() {
  let htmlPath = null;
  let mdPath = null;
  if (fs.existsSync(pathsFile)) {
    try {
      const data = JSON.parse(fs.readFileSync(pathsFile, 'utf8'));
      htmlPath = data.htmlPath || null;
      mdPath = data.mdPath || null;
    } catch (_) {}
  }

  const server = http.createServer((req, res) => {
    const subPath = req.url === '/' ? 'index.html' : path.normalize(req.url.split('?')[0]).replace(/^(\.\.(\/|\\|$))+/, '');
    const filePath = path.join(reportDir, subPath);
    const resolved = path.resolve(filePath);
    if (!resolved.startsWith(path.resolve(reportDir)) || resolved === path.resolve(reportDir)) {
      res.statusCode = 404;
      res.end();
      return;
    }
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.statusCode = 404;
        res.end();
        return;
      }
      const ext = path.extname(filePath);
      const types = { '.html': 'text/html', '.js': 'application/javascript', '.json': 'application/json', '.css': 'text/css' };
      res.setHeader('Content-Type', types[ext] || 'application/octet-stream');
      res.end(data);
    });
  });

  server.listen(0, '127.0.0.1', async () => {
    const port = server.address().port;
    const reportUrl = `http://127.0.0.1:${port}/`;
    const { chromium } = require('playwright-core');
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();

    const reportPage = await context.newPage();
    await reportPage.goto(reportUrl);

    if (htmlPath && fs.existsSync(htmlPath)) {
      const p2 = await context.newPage();
      await p2.goto(pathToFileURL(htmlPath));
    }
    if (mdPath && fs.existsSync(mdPath)) {
      const p3 = await context.newPage();
      await p3.goto(pathToFileURL(mdPath));
    }

    console.log('Browser opened with Playwright report + recorded steps (HTML/MD). Close the browser when done.');
  });
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
