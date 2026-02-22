"""
Video recording: capture screen at fixed FPS and write to MP4.
Uses mss for frames and imageio + imageio-ffmpeg for encoding.
"""
import threading
import time
import os
import tempfile
from datetime import datetime

_writer = None
_stop = threading.Event()
_thread = None
_output_path = None


def _capture_loop(fps, output_path):
    global _writer, _stop, _output_path
    try:
        import mss
        import numpy as np
        import imageio
    except ImportError:
        return
    try:
        with mss.mss() as sct:
            mon = sct.monitors[0]
            interval = 1.0 / fps
            # imageio v2: get_writer with FFMPEG for .mp4
            w = imageio.get_writer(output_path, format="FFMPEG", mode="I", fps=fps, codec="libx264", output_params=["-pix_fmt", "yuv420p"])
            _writer = w
            while not _stop.is_set():
                t0 = time.monotonic()
                shot = sct.grab(mon)
                frame = np.array(shot)
                frame = frame[:, :, [2, 1, 0]]  # BGRA -> RGB
                w.append_data(frame)
                elapsed = time.monotonic() - t0
                sleep = interval - elapsed
                if sleep > 0:
                    _stop.wait(sleep)
            w.close()
    except Exception:
        if _writer is not None:
            try:
                _writer.close()
            except Exception:
                pass
    finally:
        _writer = None
        _output_path = output_path


def start_video_recording(fps=3, output_dir=None):
    """Start recording video. Returns path where file will be written."""
    global _thread, _stop, _output_path
    if _thread is not None and _thread.is_alive():
        return None
    _output_path = None
    _stop.clear()
    output_dir = output_dir or tempfile.gettempdir()
    name = "StepsRecorder_%s.mp4" % datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(output_dir, name)
    _thread = threading.Thread(target=_capture_loop, args=(fps, path), daemon=True)
    _thread.start()
    time.sleep(0.3)
    return path


def stop_video_recording():
    """Stop recording and return the path to the video file (if known)."""
    global _stop, _thread, _writer, _output_path
    _stop.set()
    if _thread is not None:
        _thread.join(timeout=8.0)
        _thread = None
    path = _output_path
    _output_path = None
    return path
