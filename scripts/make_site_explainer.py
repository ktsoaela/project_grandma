"""Still of a recording, and a short explainer of the guide it produces."""
from pathlib import Path

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs"
W, H = 960, 540
FPS = 8

FONT = Path(r"C:\Windows\Fonts\segoeui.ttf")
FONTB = Path(r"C:\Windows\Fonts\segoeuib.ttf")


def font(size, bold=False):
    path = FONTB if bold and FONTB.exists() else FONT
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default()


def text(draw, xy, s, size=16, fill="#1a1a1a", bold=False):
    draw.text(xy, s, font=font(size, bold), fill=fill)


def app_window(step_count):
    im = Image.new("RGB", (W, H), "#f4efe8")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((70, 50, 890, 490), 16, fill="#f0f0f0", outline="#ddd4c8")
    d.rectangle((70, 50, 890, 96), fill="#ffffff")
    text(d, (92, 62), "Grandma Steps", 18, bold=True)
    text(d, (250, 66), "Record steps to reproduce a problem", 13, "#666")
    d.line((92, 118, 868, 118), fill="#ccc")
    text(d, (92, 150), f"{step_count}", 28, "#0078d4", bold=True)
    text(d, (150, 160), "steps recorded", 16, "#555")
    d.rounded_rectangle((92, 230, 250, 268), 4, fill="#e5e5e5", outline="#ccc")
    text(d, (112, 238), "Add Comment", 14)
    d.rounded_rectangle((266, 230, 410, 268), 4, fill="#c42b1c")
    text(d, (292, 238), "Stop Record", 14, "#fff", bold=True)
    text(d, (92, 310), "Each click stores a screenshot and a green circle on the spot you clicked.", 14, "#555")
    text(d, (92, 360), "Record video (MP4) is on.", 14, "#555")
    return im


def guide_frame(highlight):
    im = Image.new("RGB", (W, H), "#ffffff")
    d = ImageDraw.Draw(im)
    text(d, (48, 28), "Recorded Steps", 26, bold=True)
    d.line((48, 70, 912, 70), fill="#ccc")
    text(d, (48, 86), "This file contains the steps that were recorded, ready to send.", 15, "#444")
    text(d, (48, 130), "Steps", 20, bold=True)
    d.line((48, 160, 912, 160), fill="#ccc")
    text(d, (48, 176), "Step 1: (10:14:02)  User left click on \"File\"", 15, bold=True)
    d.rounded_rectangle((48, 210, 430, 360), 6, fill="#e8eef5", outline="#c5d0dc")
    text(d, (70, 250), "File    Edit    View", 14, "#333")
    d.rectangle((64, 246, 108, 272), outline="#4CAF50", width=3)
    d.ellipse((78, 286, 118, 326), outline="#4CAF50", width=3)
    text(d, (150, 292), "click", 13, "#2e7d32")
    text(d, (48, 376), "Now we go to the File menu.", 15, "#333")
    d.line((48, 408, 912, 408), fill="#ccc")
    text(d, (48, 422), "Step 2: (10:14:06)  User left click on \"Open\"", 15, bold=True)
    if highlight:
        d.rounded_rectangle((620, 430, 900, 510), 8, fill="#3d291f")
        text(d, (640, 452), "Also saved as MP4", 16, "#fff", bold=True)
        text(d, (640, 476), "The same session, as video.", 13, "#f4efe8")
    return im


def caption(im, line):
    out = im.copy()
    d = ImageDraw.Draw(out)
    d.rectangle((0, H - 46, W, H), fill="#3d291f")
    text(d, (24, H - 34), line, 16, "#fbf7f2", bold=True)
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    recording = caption(app_window(3), "Recording. Every click becomes a step.")
    recording.save(OUT / "recording.png")
    frames = []
    frames += [caption(app_window(1), "1  Start the recording")] * (FPS * 2)
    frames += [caption(app_window(3), "2  Each click keeps a screenshot")] * (FPS * 2)
    frames += [caption(guide_frame(False), "3  The guide you send")] * (FPS * 3)
    frames += [caption(guide_frame(True), "4  The same session, as video")] * (FPS * 2)
    imageio.mimwrite(
        OUT / "explainer.mp4",
        [np.asarray(f) for f in frames],
        fps=FPS,
        codec="libx264",
        quality=8,
    )
    print("wrote", OUT / "recording.png")
    print("wrote", OUT / "explainer.mp4")


if __name__ == "__main__":
    main()
