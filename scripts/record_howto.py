"""Record a Windows Chrome walkthrough of the live page, with a spoken how-to."""
import asyncio
import shutil
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
GAP = 0.35

BEATS = [
    ("chrome", "On Windows, open Google Chrome."),
    ("address", "Select the address bar."),
    ("type", "Type ktsoaela.github.io, slash project underscore grandma, and press Enter."),
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
    done = subprocess.run(cmd, capture_output=True, text=True)
    if done.returncode != 0:
        raise SystemExit((done.stderr or done.stdout or "ffmpeg failed")[-2000:])


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
        if not dest.exists() or dest.stat().st_size < 1000:
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

    profile = WORK / "chrome-clean"
    subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "Get-CimInstance Win32_Process -Filter \"Name='chrome.exe'\" | "
         "Where-Object { $_.CommandLine -and $_.CommandLine.ToLower().Contains('chrome-clean') } | "
         "ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"],
        capture_output=True,
    )
    shutil.rmtree(profile, ignore_errors=True)
    profile.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen(
        [
            CHROME,
            "--remote-debugging-port=9341",
            f"--user-data-dir={profile}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-extensions",
            "--disable-popup-blocking",
            "--disable-session-crashed-bubble",
            "--hide-crash-restore-bubble",
            "--start-maximized",
            "https://www.google.com/ncr?hl=en",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    def profile_pids():
        ps = (
            "Get-CimInstance Win32_Process -Filter \"Name='chrome.exe'\" | "
            "Where-Object { $_.CommandLine -and $_.CommandLine.ToLower().Contains('chrome-clean') } | "
            "ForEach-Object { $_.ProcessId }"
        )
        out = subprocess.check_output(["powershell", "-NoProfile", "-Command", ps], text=True, errors="ignore")
        return {int(part) for part in out.split() if part.strip().isdigit()}

    def find_hwnd():
        pids = profile_pids()
        found = []

        @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        def cb(hwnd, _):
            if not user32.IsWindowVisible(hwnd):
                return True
            pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            if pid.value not in pids:
                return True
            length = user32.GetWindowTextLengthW(hwnd)
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            if buf.value:
                found.append(hwnd)
            return True

        user32.EnumWindows(cb, 0)
        return found[-1] if found else None

    def focus(hwnd):
        fg = user32.GetForegroundWindow()
        fg_thread = user32.GetWindowThreadProcessId(fg, None)
        this = ctypes.windll.kernel32.GetCurrentThreadId()
        user32.AttachThreadInput(this, fg_thread, True)
        user32.ShowWindow(hwnd, 3)
        user32.SetForegroundWindow(hwnd)
        user32.AttachThreadInput(this, fg_thread, False)

    hwnd = None
    for _ in range(40):
        hwnd = find_hwnd()
        if hwnd:
            break
        time.sleep(0.25)
    if not hwnd:
        proc.kill()
        raise SystemExit("Chrome window not found")

    focus(hwnd)
    user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0002 | 0x0001)
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

    ready = False
    for _ in range(8):
        focus(hwnd)
        user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0002 | 0x0001)
        time.sleep(0.4)
        if user32.GetForegroundWindow() == hwnd:
            ready = True
            break
    if not ready:
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
        raise SystemExit("Chrome was not in front, so nothing was recorded.")

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
    record_t0 = time.perf_counter()
    starts = []
    mouse_home = pyautogui.position()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9341")
        context = browser.contexts[0]
        page = context.pages[0]
        try:
            page.wait_for_load_state("domcontentloaded", timeout=20000)
        except Exception:
            pass

        def hold(index, action=None):
            starts.append(time.perf_counter())
            if action:
                action()
            remain = lengths[index] + GAP - (time.perf_counter() - starts[-1])
            if remain > 0:
                time.sleep(remain)

        def address_bar():
            focus(hwnd)
            pyautogui.moveTo(x + int(w * 0.45), y + 78, duration=0.35)
            pyautogui.click()
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
            "chrome": lambda: focus(hwnd),
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
        scroll_at = next(i for i, (key, _) in enumerate(BEATS) if key == "scroll")
        poster_at = starts[scroll_at] - record_t0
        try:
            ff.stdin.write(b"q")
            ff.stdin.flush()
        except Exception:
            pass
        try:
            ff.wait(timeout=8)
        except subprocess.TimeoutExpired:
            ff.kill()

    pyautogui.moveTo(mouse_home.x, mouse_home.y, duration=0.2)
    subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)

    voice = WORK / "voice.m4a"
    filters, labels = [], []
    mix = [FFMPEG, "-y"]
    for line in lines:
        mix += ["-i", str(line)]
    for i, start in enumerate(starts):
        ms = max(0, int((start - record_t0) * 1000))
        filters.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]")
        labels.append(f"[a{i}]")
    filters.append("".join(labels) + f"amix=inputs={len(starts)}:duration=longest:dropout_transition=0:normalize=0[a]")
    mix += ["-filter_complex", ";".join(filters), "-map", "[a]", "-c:a", "aac", "-b:a", "160k", str(voice)]
    run(mix)
    final = DOCS / "explainer.mp4"
    run([
        FFMPEG, "-y", "-i", str(raw), "-i", str(voice),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "23",
        "-c:a", "aac", "-shortest", str(final),
    ])
    poster = DOCS / "howto-poster.jpg"
    run([
        FFMPEG, "-y", "-ss", f"{max(0, poster_at):.2f}", "-i", str(final),
        "-frames:v", "1", "-update", "1", str(poster),
    ])
    print("wrote", final)


if __name__ == "__main__":
    main()
