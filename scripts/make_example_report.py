"""Build the sample recorded-steps report shown on the site."""
import base64
import sys
from datetime import datetime
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "recorder"))
from report import build_html

SHOTS = ROOT / "scripts" / "_howto_work" / "report-shots"
OUT = ROOT / "docs" / "example-report.html"
BASE = "http://127.0.0.1:8766/"


def circle(path: Path, xy):
    im = Image.open(path).convert("RGB")
    d = ImageDraw.Draw(im)
    x, y = xy
    r = 18
    d.ellipse((x - r, y - r, x + r, y + r), outline="#4CAF50", width=4)
    buf = BytesIO()
    im.thumbnail((1000, 800))
    im.save(buf, format="PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def main():
    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1100, "height": 800})
        page.goto(BASE + "#steps", wait_until="domcontentloaded")
        page.locator("#steps").screenshot(path=str(SHOTS / "steps.png"))
        page.locator("#download").screenshot(path=str(SHOTS / "download.png"))
        page.goto(BASE + "grandma.html", wait_until="domcontentloaded")
        page.locator("#btn-stop").click()
        page.locator(".app").screenshot(path=str(SHOTS / "saved.png"))
        browser.close()

    start = datetime(2026, 11, 6, 21, 20, 4)
    steps = [
        {
            "description": 'User left click on "Steps" in Google Chrome',
            "time": start,
            "image_base64": circle(SHOTS / "steps.png", (180, 40)),
            "program": {"name": "Google Chrome", "version": "131", "company": "Google", "exe": "chrome.exe", "exe_path": ""},
            "ui_elements": ["Steps"],
        },
        {
            "description": 'User left click on "Download for Windows"',
            "time": datetime(2026, 11, 6, 21, 20, 18),
            "image_base64": circle(SHOTS / "download.png", (160, 150)),
            "program": {"name": "Google Chrome", "version": "131", "company": "Google", "exe": "chrome.exe", "exe_path": ""},
            "ui_elements": ["Download for Windows"],
        },
        {
            "description": 'User left click on "Open HTML" in Project Grandma',
            "time": datetime(2026, 11, 6, 21, 21, 2),
            "image_base64": circle(SHOTS / "saved.png", (90, 150)),
            "program": {"name": "Project Grandma", "version": "1.0.0", "company": "", "exe": "Project Grandma.exe", "exe_path": ""},
            "ui_elements": ["Open HTML"],
        },
    ]
    build_html(steps, str(OUT), session_start=start, session_end=steps[-1]["time"])
    print("wrote", OUT, OUT.stat().st_size)


if __name__ == "__main__":
    main()
