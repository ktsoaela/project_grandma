"""Record a Windows Chrome walkthrough of the live page, with a spoken how-to."""
import asyncio
import subprocess
import time
from pathlib import Path

import edge_tts
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
WORK = ROOT / "scripts" / "_howto_work"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
URL = "https://ktsoaela.github.io/project_grandma/"
VOICE = "en-US-JennyNeural"
GAP = 0.45

BEATS = [
    ("ready", "In this video, you will open the Project Grandma page on Windows, and follow each direction."),
    ("chrome", "First, open Google Chrome."),
    ("address", "Select the address bar."),
    ("type", "Go to ktsoaela.github.io, slash project underscore grandma. Then press Enter."),
    ("loaded", "The page opens. The heading reads: Show the steps. Not just the result."),
    ("idea", "This is a step recorder. Every click becomes a screenshot, a note, and a guide someone else can follow."),
    ("scroll", "Scroll to What it records. These are the directions."),
    ("c0", "A step per click. Each click is a new step, in the order you did it."),
    ("c1", "A screenshot. The screen is captured, so the next person can see what you saw."),
    ("c2", "A click circle. A circle marks where you clicked, in the app, and on the export."),
    ("c3", "What was clicked. On Windows, the recorder names the control when it can."),
    ("c4", "A comment. Add a sentence between steps, when the click is not obvious."),
    ("c5", "A guide to share. Hand someone the result, instead of walking them through it again."),
    ("export", "Scroll to Take it with you. The same recording can leave in more than one form."),
    ("e0", "HTML. An interactive step by step page."),
    ("e1", "PDF. A printable copy of the steps."),
    ("e2", "Markdown. Text, with the screenshots embedded."),
    ("e3", "Video. An optional MP4 of the actions."),
    ("e4", "Windows. Windows 10 and later."),
    ("e5", "macOS. macOS 10.12 and later. Screen recording permission is required."),
    ("end", "That is the direction. Open the page, read one step at a time, and follow it."),
]


def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def duration(path: Path) -> float:
    out = subprocess.run(
        [FFMPEG, "-i", str(path), "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    for line in out.splitlines():
        if "Duration:" in line:
            h, m, s = line.split("Duration:", 1)[1].split(",", 1)[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise RuntimeError(f"no duration for {path}")


async def speak_all():
    WORK.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, (_, text) in enumerate(BEATS):
        dest = WORK / f"line-{i:02d}.mp3"
        if not dest.exists():
            await edge_tts.Communicate(text, VOICE, rate="-6%").save(str(dest))
        paths.append(dest)
    return paths


def main():
    import ctypes
    from ctypes import wintypes

    from playwright.sync_api import sync_playwright
    import pyautogui

    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.05
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass

    user32 = ctypes.windll.user32
    lines = asyncio.run(speak_all())
    lengths = [duration(p) for p in lines]

    profile = WORK / "chrome-profile"
    profile.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen(
        [
            CHROME,
            "--remote-debugging-port=9333",
            f"--user-data-dir={profile}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-extensions",
            "--disable-popup-blocking",
            "--start-maximized",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    def find_hwnd():
        found = []

        @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        def cb(hwnd, _):
            if not user32.IsWindowVisible(hwnd):
                return True
            length = user32.GetWindowTextLengthW(hwnd)
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            title = buf.value
            if "Google Chrome" in title or title == "about:blank":
                found.append(hwnd)
            return True

        user32.EnumWindows(cb, 0)
        return found[-1] if found else None

    hwnd = None
    for _ in range(40):
        hwnd = find_hwnd()
        if hwnd:
            break
        time.sleep(0.25)
    if not hwnd:
        proc.kill()
        raise SystemExit("Chrome window not found")

    user32.ShowWindow(hwnd, 3)
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.8)

    class RECT(ctypes.Structure):
        _fields_ = [("l", ctypes.c_long), ("t", ctypes.c_long), ("r", ctypes.c_long), ("b", ctypes.c_long)]

    rect = RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    # Record the Chrome window only, so the rest of the desktop stays off camera.
    x, y = max(0, rect.l), max(0, rect.t)
    sw, sh = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    w, h = min(rect.r, sw) - x, min(rect.b, sh) - y
    w -= w % 2
    h -= h % 2

    raw = WORK / "capture.mp4"
    ff = subprocess.Popen(
        [
            FFMPEG, "-y",
            "-f", "gdigrab",
            "-framerate", "15",
            "-offset_x", str(x),
            "-offset_y", str(y),
            "-video_size", f"{w}x{h}",
            "-draw_mouse", "1",
            "-i", "desktop",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "veryfast",
            str(raw),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(0.6)

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9333")
        context = browser.contexts[0]
        page = context.pages[0]

        def focus():
            user32.ShowWindow(hwnd, 3)
            user32.SetForegroundWindow(hwnd)

        def hold(index, action=None):
            start = time.perf_counter()
            if action:
                action()
            remain = lengths[index] + GAP - (time.perf_counter() - start)
            if remain > 0:
                time.sleep(remain)

        def address_bar():
            focus()
            pyautogui.hotkey("ctrl", "l")
            time.sleep(0.2)

        def go():
            address_bar()
            pyautogui.write(URL, interval=0.035)
            time.sleep(0.2)
            pyautogui.press("enter")
            page.wait_for_load_state("domcontentloaded", timeout=30000)
            page.wait_for_selector("#steps article", timeout=30000)

        def highlight(selector, nth):
            page.evaluate(
                """([selector, nth]) => {
                    document.querySelectorAll('.howto-hot').forEach(el => el.classList.remove('howto-hot'));
                    const el = document.querySelectorAll(selector)[nth];
                    if (!el) return;
                    el.classList.add('howto-hot');
                    el.scrollIntoView({behavior: 'smooth', block: 'center'});
                }""",
                [selector, nth],
            )
            page.add_style_tag(content=".howto-hot{outline:3px solid #8d4a32;outline-offset:4px;border-radius:16px}")

        actions = {
            "ready": lambda: focus(),
            "chrome": lambda: focus(),
            "address": address_bar,
            "type": go,
            "loaded": lambda: page.evaluate("window.scrollTo({top:0,behavior:'smooth'})"),
            "idea": lambda: None,
            "scroll": lambda: highlight("#steps article", 0),
            "c0": lambda: highlight("#steps article", 0),
            "c1": lambda: highlight("#steps article", 1),
            "c2": lambda: highlight("#steps article", 2),
            "c3": lambda: highlight("#steps article", 3),
            "c4": lambda: highlight("#steps article", 4),
            "c5": lambda: highlight("#steps article", 5),
            "export": lambda: highlight("#export article", 0),
            "e0": lambda: highlight("#export article", 0),
            "e1": lambda: highlight("#export article", 1),
            "e2": lambda: highlight("#export article", 2),
            "e3": lambda: highlight("#export article", 3),
            "e4": lambda: highlight("#export article", 4),
            "e5": lambda: highlight("#export article", 5),
            "end": lambda: page.evaluate("document.querySelector('#steps').scrollIntoView({behavior:'smooth'})"),
        }
        for i, (key, _) in enumerate(BEATS):
            hold(i, actions[key])
        browser.close()

    time.sleep(0.4)
    try:
        ff.stdin.write(b"q")
        ff.stdin.flush()
    except Exception:
        pass
    try:
        ff.wait(timeout=8)
    except subprocess.TimeoutExpired:
        ff.kill()
    proc.terminate()

    concat = WORK / "list.txt"
    silence = WORK / "gap.mp3"
    run([
        FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
        "-t", str(GAP), "-c:a", "libmp3lame", "-q:a", "6", str(silence),
    ])
    parts = []
    for line in lines:
        parts.append(f"file '{line.as_posix()}'")
        parts.append(f"file '{silence.as_posix()}'")
    concat.write_text("\n".join(parts), encoding="utf-8")
    voice = WORK / "voice.m4a"
    run([
        FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-c:a", "aac", "-b:a", "160k", str(voice),
    ])
    final = DOCS / "explainer.mp4"
    run([
        FFMPEG, "-y", "-i", str(raw), "-i", str(voice),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "23",
        "-c:a", "aac", "-shortest", str(final),
    ])
    poster = DOCS / "howto-poster.jpg"
    run([
        FFMPEG, "-y", "-ss", "18", "-i", str(final), "-frames:v", "1", "-update", "1", str(poster),
    ])
    print("wrote", final)


if __name__ == "__main__":
    main()
