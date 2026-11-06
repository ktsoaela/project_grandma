"""Old wikiHow-style video, "How to use Project Grandma", and the report that matches it."""
import asyncio
import subprocess
import sys
import wave
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
import base64

import edge_tts
import imageio.v2 as imageio
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
WORK = ROOT / "scripts" / "_wikihow_work"
APP = ROOT / "grandama" / "renderer" / "index.html"
LOGO = DOCS / "logo.png"
SITE = "https://ktsoaela.github.io/project_grandma/"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

sys.path.insert(0, str(ROOT / "recorder"))
from report import build_html  # noqa: E402

W, H = 1280, 720
FPS = 12
GREEN = "#93b874"
DEEP_GREEN = "#5e7d43"
INK = "#333333"
CLICK = "#4CAF50"
VOICE = "en-ZA-LeahNeural"
FALLBACK_VOICE = "en-US-JennyNeural"
SR = 22050


def font(size, bold=False):
    name = "segoeuib.ttf" if bold else "segoeui.ttf"
    return ImageFont.truetype(rf"C:\Windows\Fonts\{name}", size)


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def ring(img, xy, r=28):
    d = ImageDraw.Draw(img)
    x, y = xy
    d.ellipse((x - r, y - r, x + r, y + r), outline=CLICK, width=6)
    return img


def center(box, dx=0, dy=0):
    return (box["x"] + box["width"] / 2 + dx, box["y"] + box["height"] / 2 + dy)


# ---------- pictures ----------

def desktop():
    top, bottom = np.array([20, 62, 112]), np.array([74, 140, 214])
    t = np.linspace(0, 1, H)[:, None, None]
    grad = (top * (1 - t) + bottom * t).astype(np.uint8)
    img = Image.fromarray(np.repeat(grad, W, axis=1), "RGB")
    d = ImageDraw.Draw(img)
    logo = Image.open(LOGO).convert("RGBA").resize((64, 64))
    img.paste(logo, (46, 36), logo)
    d.text((78, 108), "Project Grandma", font=font(15), fill="white", anchor="ma")
    d.rectangle((0, H - 56, W, H), fill=(32, 32, 32))
    cx, cy = W // 2, H - 28
    pts = {"desktop": (78, 72), "start": (cx - 96, cy), "chrome": (cx - 32, cy), "taskbar": (cx + 32, cy)}
    sx, sy = pts["start"]
    for ox, oy in ((-9, -9), (2, -9), (-9, 2), (2, 2)):
        d.rectangle((sx + ox, sy + oy, sx + ox + 8, sy + oy + 8), fill="#4cc2ff")
    gx, gy = pts["chrome"]
    for start, colour in ((-90, "#db4437"), (30, "#f4b400"), (150, "#0f9d58")):
        d.pieslice((gx - 16, gy - 16, gx + 16, gy + 16), start, start + 120, fill=colour)
    d.ellipse((gx - 7, gy - 7, gx + 7, gy + 7), fill="#4285f4", outline="white", width=2)
    small = Image.open(LOGO).convert("RGBA").resize((34, 34))
    tx, ty = pts["taskbar"]
    img.paste(small, (int(tx - 17), int(ty - 17)), small)
    return img, pts


def start_menu():
    img, pts = desktop()
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = W // 2 - 300, 150, W // 2 + 300, H - 70
    d.rounded_rectangle((x0, y0, x1, y1), 14, fill=(44, 44, 44))
    d.text((x0 + 30, y0 + 24), "Pinned", font=font(18, True), fill="white")
    names = ["Edge", "Mail", "Photos", "Project Grandma", "Settings", "Files"]
    tile = Image.open(LOGO).convert("RGBA").resize((48, 48))
    for i, name in enumerate(names):
        cx = x0 + 90 + (i % 3) * 210
        cy = y0 + 120 + (i // 3) * 140
        if name == "Project Grandma":
            img.paste(tile, (cx - 24, cy - 34), tile)
            pts["menu"] = (cx, cy - 10)
        else:
            d.rounded_rectangle((cx - 22, cy - 32, cx + 22, cy + 12), 8, fill=(90, 90, 90))
        d.text((cx, cy + 22), name, font=font(14), fill="white", anchor="ma")
    return img, pts


def window(app_png, on=None):
    base, pts = on if on else desktop()
    app = Image.open(app_png).convert("RGB")
    bar = 32
    win = Image.new("RGB", (app.width, app.height + bar), "#f3f3f3")
    win.paste(app, (0, bar))
    d = ImageDraw.Draw(win)
    icon = Image.open(LOGO).convert("RGBA").resize((18, 18))
    win.paste(icon, (10, 7), icon)
    d.text((36, 7), "Steps Recorder", font=font(13), fill="#222")
    for i, glyph in enumerate(("✕", "□", "–")):
        bx = app.width - 46 * (i + 1)
        d.text((bx + 23, 16), glyph, font=font(14), fill="#222", anchor="mm")
    ox, oy = W // 2 - app.width // 2, 70
    base = base.copy()
    ImageDraw.Draw(base).rectangle((ox - 1, oy - 1, ox + win.width, oy + win.height), outline="#888")
    base.paste(win, (ox, oy))
    out = dict(pts)
    out["offset"] = (ox, oy + bar)
    out["close"] = (ox + app.width - 23, oy + 16)
    return base, out


def browser(content, url):
    chrome = 84
    img = Image.new("RGB", (W, chrome + content.height), "#ffffff")
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 40), fill="#dee1e6")
    d.rounded_rectangle((12, 8, 270, 40), 8, fill="#ffffff")
    d.text((30, 15), "Project Grandma", font=font(13), fill="#222")
    d.rounded_rectangle((120, 48, W - 100, 78), 15, fill="#f1f3f4")
    d.text((140, 53), url, font=font(15), fill="#202124")
    for i, glyph in enumerate(("←", "→", "⟳")):
        d.text((24 + i * 32, 63), glyph, font=font(16), fill="#5f6368", anchor="mm")
    img.paste(content, (0, chrome))
    return img, {"omnibox": (420, 63), "offset": (0, chrome)}


def new_tab():
    page = Image.new("RGB", (W, 720), "#ffffff")
    d = ImageDraw.Draw(page)
    d.text((W // 2, 250), "Google", font=font(72), fill="#4285f4", anchor="mm")
    d.rounded_rectangle((W // 2 - 280, 320, W // 2 + 280, 368), 24, outline="#dfe1e5", width=2)
    return page


def share_picture(report_png):
    img = Image.new("RGB", (W, H), "#f7f7f5")
    d = ImageDraw.Draw(img)
    rep = Image.open(report_png).convert("RGB")
    rep.thumbnail((430, 330))
    img.paste(rep, (90, 150))
    d.rectangle((90, 150, 90 + rep.width, 150 + rep.height), outline="#c9c9c9", width=2)
    d.text((90, 500), "Recorded Steps.html", font=font(20, True), fill=INK)
    d.rounded_rectangle((90, 550, 520, 640), 10, fill="#222")
    d.polygon([(285, 575), (285, 615), (320, 595)], fill="white")
    d.text((340, 584), "StepsRecorder.mp4", font=font(18), fill="white")
    d.line((600, 395, 820, 395), fill=DEEP_GREEN, width=10)
    d.polygon([(820, 370), (870, 395), (820, 420)], fill=DEEP_GREEN)
    d.ellipse((960, 230, 1080, 350), fill="#d9a77c")
    d.pieslice((900, 360, 1140, 600), 180, 360, fill="#5e7d43")
    d.text((1020, 520), "Your friend", font=font(24, True), fill=INK, anchor="ma")
    return img


# ---------- capture ----------

MOCK = """
window.recorderAPI = {
  getState: async () => ({ recording: false, step_count: 0 }),
  start: async () => ({ recording: true }),
  stop: async () => ({ paths: { html: 'Recorded Steps.html', video: 'StepsRecorder.mp4' } }),
  addComment: async () => {},
  openReport: async () => {},
};
"""


def capture():
    WORK.mkdir(parents=True, exist_ok=True)
    boxes = {}
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        app = b.new_page(viewport={"width": 520, "height": 500})
        app.add_init_script(MOCK)
        app.goto(APP.as_uri())
        app.wait_for_selector("#btn-start")
        app.screenshot(path=str(WORK / "app-idle.png"))
        boxes["start"] = app.locator("#btn-start").bounding_box()
        app.click("#btn-start")
        app.wait_for_selector("#recording-state:not(.hidden)")
        app.screenshot(path=str(WORK / "app-rec0.png"))
        app.evaluate("document.getElementById('step-count').textContent = '6'")
        app.screenshot(path=str(WORK / "app-rec6.png"))
        boxes["stop"] = app.locator("#btn-stop").bounding_box()
        app.click("#btn-stop")
        app.wait_for_selector("#save-dialog:not(.hidden) .save-btn")
        app.screenshot(path=str(WORK / "app-saved.png"))
        boxes["open_html"] = app.locator('.save-btn[data-format="html"]').bounding_box()

        site = b.new_page(viewport={"width": W, "height": 720})
        site.goto(SITE, wait_until="networkidle")
        site.screenshot(path=str(WORK / "site-top.png"))
        boxes["nav_download"] = site.locator("header a.btn:not(.ghost)").bounding_box()
        site.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        site.wait_for_timeout(800)
        site.screenshot(path=str(WORK / "site-download.png"))
        boxes["dl_win"] = site.locator("#dl-win").bounding_box()
        b.close()
    return boxes


def shoot_report():
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        page = b.new_page(viewport={"width": W, "height": 720})
        page.goto((DOCS / "example-report.html").as_uri())
        page.screenshot(path=str(WORK / "report.png"))
        b.close()


# ---------- pictures for each step ----------

def pictures(bx):
    def app_on_desktop(png, click=None):
        img, pts = window(WORK / png)
        if click:
            ox, oy = pts["offset"]
            x, y = center(bx[click])
            ring(img, (ox + x, oy + y))
        return img, pts

    def site_shot(png, click=None, omnibox=False):
        img, pts = browser(Image.open(WORK / png).convert("RGB"), "ktsoaela.github.io/project_grandma/")
        if click:
            x, y = center(bx[click])
            ring(img, (x, y + pts["offset"][1]))
        if omnibox:
            ring(img, pts["omnibox"], r=34)
        return img

    pics = {}
    img, pts = start_menu()
    for key in ("desktop", "menu", "taskbar"):
        ring(img, pts[key], r=40)
    pics["find"] = img
    img, pts = start_menu()
    pics["open"] = ring(img, pts["menu"], r=40)
    pics["start"], _ = app_on_desktop("app-idle.png", "start")
    pics["perform"], _ = app_on_desktop("app-rec0.png")
    img, pts = desktop()
    pics["browser"] = ring(img, pts["chrome"], r=30)
    pics["address"] = site_shot("site-top.png", omnibox=True)
    pics["download"] = site_shot("site-top.png", "nav_download")
    pics["choose"] = site_shot("site-download.png", "dl_win")
    pics["stop"], _ = app_on_desktop("app-rec6.png", "stop")
    pics["saved"], _ = app_on_desktop("app-saved.png", "open_html")
    img, pts = window(WORK / "app-saved.png")
    pics["close"] = ring(img, pts["close"], r=24)
    return pics


def b64(img):
    im = img.copy()
    im.thumbnail((1000, 760))
    buf = BytesIO()
    im.save(buf, format="PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def write_report(pics):
    explorer = {"name": "Windows Explorer", "version": "10.0", "company": "Microsoft", "exe": "explorer.exe", "exe_path": ""}
    grandma = {"name": "Project Grandma", "version": "1.0.0", "company": "", "exe": "Project Grandma.exe", "exe_path": ""}
    chrome = {"name": "Google Chrome", "version": "131", "company": "Google", "exe": "chrome.exe", "exe_path": ""}
    rows = [
        ('User left click on "Project Grandma" in Start', "open", explorer, ["Project Grandma"]),
        ('User left click on "Start Record" in Project Grandma', "start", grandma, ["Start Record"]),
        ('User left click on "Google Chrome" in Taskbar', "browser", explorer, ["Google Chrome"]),
        ('User left click on "Address and search bar" in Google Chrome', "address", chrome, ["Address and search bar"]),
        ('User Comment: "Go to https://ktsoaela.github.io/project_grandma/"', "address", chrome, []),
        ('User left click on "Download" in Google Chrome', "download", chrome, ["Download"]),
        ('User left click on "Download for Windows" in Google Chrome', "choose", chrome, ["Download for Windows"]),
        ('User left click on "Stop Record" in Project Grandma', "stop", grandma, ["Stop Record"]),
    ]
    t = datetime(2026, 11, 6, 22, 30, 4)
    steps = []
    for i, (desc, key, prog, ui) in enumerate(rows):
        steps.append({
            "description": desc,
            "time": t + timedelta(seconds=9 * i),
            "image_base64": b64(pics[key]),
            "program": prog,
            "ui_elements": ui,
        })
    build_html(steps, str(DOCS / "example-report.html"), session_start=steps[0]["time"], session_end=steps[-1]["time"])


# ---------- slides ----------

def title_slide():
    img = Image.new("RGB", (W, H), GREEN)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((140, 150, W - 140, H - 150), 24, fill="white")
    logo = Image.open(LOGO).convert("RGBA").resize((120, 120))
    img.paste(logo, (220, H // 2 - 60), logo)
    d.text((380, 250), "How to use", font=font(40), fill=DEEP_GREEN)
    d.text((380, 300), "Project Grandma", font=font(78, True), fill=INK)
    d.text((384, 410), "A step recorder that writes the guide for you", font=font(24), fill="#666")
    return img


def intro_slide():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 12), fill=GREEN)
    d.text((110, 110), "In this video", font=font(52, True), fill=INK)
    for i, line in enumerate(("How to use Project Grandma", "How to install Project Grandma", "How to generate a report")):
        y = 240 + i * 110
        d.ellipse((110, y, 170, y + 60), fill=GREEN)
        d.text((140, y + 30), "✓", font=font(32, True), fill="white", anchor="mm")
        d.text((200, y + 6), line, font=font(38), fill=INK)
    return img


def step_slide(number, text, picture):
    img = Image.new("RGB", (W, H), "#f4f4f2")
    d = ImageDraw.Draw(img)
    pic = picture.copy()
    pic.thumbnail((W - 120, H - 190))
    px, py = (W - pic.width) // 2, 24 + (H - 190 - pic.height) // 2
    d.rectangle((px - 2, py - 2, px + pic.width + 1, py + pic.height + 1), fill="#d8d8d4")
    img.paste(pic, (px, py))
    d.rectangle((0, H - 150, W, H), fill="white")
    d.rectangle((0, H - 150, W, H - 144), fill=GREEN)
    d.ellipse((40, H - 118, 116, H - 42), fill=GREEN)
    d.text((78, H - 80), str(number), font=font(36, True), fill="white", anchor="mm")
    fnt = font(32, True)
    lines = wrap(d, text, fnt, W - 190)[:2]
    y = H - 80 - 21 * len(lines)
    for line in lines:
        d.text((140, y), line, font=fnt, fill=INK)
        y += 44
    return img


SCRIPT = [
    (None, "title", "How to use Project Grandma.", None),
    (None, "intro", "In this video, we are going to show you how to use Project Grandma, how to install Project Grandma, and how to generate a report.", None),
    (1, "find", "Find where you installed it: on the Start menu, the desktop, or the taskbar.", "Find Project Grandma on the Start menu, the desktop, or the taskbar."),
    (2, "open", "Open the Project Grandma app.", "Open the Project Grandma app."),
    (3, "start", "Click Start Record.", "Click Start Record."),
    (4, "perform", "Perform your actions. In this example, we will be installing Project Grandma.", "Perform your actions. Here, we install Project Grandma."),
    (5, "browser", "Open your browser.", "Open your browser."),
    (6, "address", "Go to ktsoaela dot github dot io, slash project underscore grandma.", "Go to ktsoaela.github.io/project_grandma/"),
    (7, "download", "Click Download at the top right of the screen, or scroll down to the Download section at the bottom.", "Click Download at the top right, or scroll down to the Download section."),
    (8, "choose", "Choose your operating system, and download it.", "Choose your operating system and download it."),
    (9, "stop", "End the recording. Click Stop Record.", "End the recording: click Stop Record."),
    (10, "report", "View the report. Every step has the time, what you clicked, and a screenshot.", "View the report."),
    (11, "share", "Save the recording, and hand it over to a friend who needs to follow the instructions.", "Save the recording and hand it to a friend who needs to follow it."),
    (12, "close", "Close Project Grandma. That's it.", "Close Project Grandma."),
]


# ---------- audio ----------

async def speak(i, text):
    dest = WORK / f"voice-{i:02d}.mp3"
    if dest.exists() and dest.stat().st_size > 1000:
        return dest
    for voice in (VOICE, FALLBACK_VOICE):
        try:
            await edge_tts.Communicate(text, voice, rate="-5%").save(str(dest))
            if dest.stat().st_size > 1000:
                return dest
        except Exception:
            continue
    raise SystemExit(f"could not speak line {i}")


def duration(path):
    out = subprocess.run([FFMPEG, "-i", str(path), "-f", "null", "-"], capture_output=True, text=True).stderr
    for line in out.splitlines():
        if "Duration:" in line:
            h, m, s = line.split("Duration:", 1)[1].split(",", 1)[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise RuntimeError(path)


def pluck(freq, seconds=1.8):
    n = int(SR * seconds)
    period = max(2, int(SR / freq))
    out = np.zeros(n + period)
    out[:period] = np.random.default_rng(int(freq * 10)).uniform(-1, 1, period)
    k, step = period, period - 1
    while k < len(out):
        end = min(k + step, len(out))
        out[k:end] = 0.994 * 0.5 * (out[k - period:end - period] + out[k - period + 1:end - period + 1])
        k = end
    return out[:n]


def ukulele(total):
    chords = [
        [261.63, 329.63, 392.00, 523.25],
        [196.00, 246.94, 293.66, 392.00],
        [220.00, 261.63, 329.63, 440.00],
        [174.61, 220.00, 261.63, 349.23],
    ]
    pattern = [0, 1, 2, 3, 2, 1, 2, 3]
    eighth = 60 / 96 / 2
    cache = {}
    track = np.zeros(int(SR * (total + 3)))
    t, bar = 0.0, 0
    while t < total:
        chord = chords[bar % 4]
        for j, idx in enumerate(pattern):
            f = chord[idx]
            note = cache.setdefault(f, pluck(f))
            s = int((t + j * eighth) * SR)
            e = min(len(track), s + len(note))
            if s < len(track):
                track[s:e] += note[: e - s] * (0.9 if j == 0 else 0.6)
        root = chord[0] / 2
        tt = np.arange(int(SR * 1.6)) / SR
        bass = np.sin(2 * np.pi * root * tt) * np.exp(-tt * 2.2) * 0.5
        s = int(t * SR)
        e = min(len(track), s + len(bass))
        track[s:e] += bass[: e - s]
        t += eighth * 8
        bar += 1
    track = track[: int(SR * total)]
    fade = int(SR * 2)
    track[:fade] *= np.linspace(0, 1, fade)
    track[-fade:] *= np.linspace(1, 0, fade)
    track /= np.max(np.abs(track)) + 1e-9
    pcm = (track * 0.8 * 32767).astype(np.int16)
    dest = WORK / "music.wav"
    with wave.open(str(dest), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())
    return dest


def run(cmd):
    done = subprocess.run(cmd, capture_output=True, text=True)
    if done.returncode != 0:
        raise SystemExit(done.stderr[-2000:])


# ---------- main ----------

def main():
    boxes = capture()
    pics = pictures(boxes)
    write_report(pics)
    shoot_report()
    report = Image.open(WORK / "report.png").convert("RGB")
    pics["report"], _ = browser(report, "file:///C:/Users/you/Documents/Recorded Steps.html")
    pics["share"] = share_picture(WORK / "report.png")

    slides = []
    for number, key, _, caption in SCRIPT:
        if key == "title":
            slides.append(title_slide())
        elif key == "intro":
            slides.append(intro_slide())
        else:
            slides.append(step_slide(number, caption, pics[key]))
    slides[0].save(DOCS / "howto-poster.jpg", quality=90)

    async def all_voices():
        return [await speak(i, line[2]) for i, line in enumerate(SCRIPT)]
    voices = asyncio.run(all_voices())
    lengths = [duration(v) for v in voices]
    spans = [max(3.2, l + 1.3) for l in lengths]
    starts = np.concatenate([[0], np.cumsum(spans)[:-1]])
    total = float(sum(spans))

    silent = WORK / "video.mp4"
    writer = imageio.get_writer(str(silent), fps=FPS, codec="libx264", quality=8, macro_block_size=16)
    fade = int(0.4 * FPS)
    for i, slide in enumerate(slides):
        frames = int(round(spans[i] * FPS))
        cur = np.asarray(slide)
        prev = np.asarray(slides[i - 1]) if i else None
        for f in range(frames):
            if prev is not None and f < fade:
                a = (f + 1) / (fade + 1)
                writer.append_data((prev * (1 - a) + cur * a).astype(np.uint8))
            else:
                writer.append_data(cur)
    writer.close()

    voice_track = WORK / "voice.m4a"
    cmd, filters, labels = [FFMPEG, "-y"], [], []
    for v in voices:
        cmd += ["-i", str(v)]
    for i, s in enumerate(starts):
        ms = int((s + 0.45) * 1000)
        filters.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]")
        labels.append(f"[a{i}]")
    filters.append("".join(labels) + f"amix=inputs={len(voices)}:duration=longest:dropout_transition=0:normalize=0[a]")
    run(cmd + ["-filter_complex", ";".join(filters), "-map", "[a]", "-c:a", "aac", "-b:a", "160k", str(voice_track)])

    music = ukulele(total)
    run([
        FFMPEG, "-y", "-i", str(silent), "-i", str(voice_track), "-i", str(music),
        "-filter_complex",
        "[1:a]aresample=24000,volume=1.0[v];[2:a]aresample=24000,volume=0.14[m];[v][m]amix=inputs=2:duration=longest:normalize=0[a]",
        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
        "-t", f"{total:.2f}", "-movflags", "+faststart", str(DOCS / "explainer.mp4"),
    ])
    print(f"wrote explainer.mp4 ({total:.1f}s) and example-report.html")


if __name__ == "__main__":
    main()
