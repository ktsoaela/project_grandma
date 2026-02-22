"""
Step capture: global mouse + keyboard listener, screenshot on each step.
PSR-style step text: "User left click on \"element (type)\" in \"window title\"."
"""
import sys
import threading
import base64
from datetime import datetime

try:
    from pynput import mouse, keyboard
except ImportError:
    mouse = None
    keyboard = None
try:
    import mss
    import mss.tools
except ImportError:
    mss = None

if sys.platform == 'win32':
    try:
        from win_info import get_window_title, get_process_info, get_element_at_point, get_os_version
    except ImportError:
        get_window_title = lambda: ''
        get_process_info = lambda: None
        get_element_at_point = lambda x, y: ('', '', [])
        get_os_version = lambda: ''
else:
    get_window_title = lambda: ''
    get_process_info = lambda: None
    get_element_at_point = lambda x, y: ('', '', [])
    get_os_version = lambda: ''


class StepCapture:
    def __init__(self, on_step, max_screenshots=25):
        self.on_step = on_step
        self.max_screenshots = max(1, max_screenshots)
        self._steps = []
        self._lock = threading.Lock()
        self._mouse_listener = None
        self._keyboard_listener = None
        self._running = False
        self._session_start = None
        self._last_keyboard_step = 0
        self._keyboard_throttle_sec = 2.0

    def _take_screenshot(self):
        if not mss:
            return None
        try:
            with mss.mss() as sct:
                mon = sct.monitors[0]
                shot = sct.grab(mon)
                img = mss.tools.to_png(shot.rgb, shot.size)
                return base64.b64encode(img).decode('ascii')
        except Exception:
            return None

    def _element_label(self, elem_name, suffix):
        s = (elem_name or '').strip()
        if suffix and not s.endswith(suffix):
            s = s + suffix
        return s if s else 'unknown'

    def _add_step(self, description, image_b64=None, window_title=None, program=None, ui_elements=None):
        with self._lock:
            self._steps.append({
                'description': description,
                'image_base64': image_b64,
                'time': datetime.now(),
                'window_title': window_title or get_window_title(),
                'program': program or get_process_info(),
                'ui_elements': ui_elements if ui_elements is not None else [],
            })
            if len(self._steps) > self.max_screenshots:
                self._steps = self._steps[-self.max_screenshots:]
            count = len(self._steps)
        if self.on_step:
            self.on_step(count)

    def _on_click(self, x, y, button, pressed):
        if not pressed:
            return
        window_title = get_window_title()
        elem_name, suffix, chain = get_element_at_point(x, y)
        label = self._element_label(elem_name, suffix)
        btn = str(button).replace('Button.', '')
        if btn == 'left':
            action = 'User left click'
        elif btn == 'right':
            action = 'User right click'
        else:
            action = f'User {btn} click'
        desc = f'{action} on "{label}" in "{window_title}"'
        img = self._take_screenshot()
        prog = get_process_info()
        self._add_step(desc, img, window_title=window_title, program=prog, ui_elements=chain)

    def _on_key(self, key):
        try:
            import time
            now = time.monotonic()
            if now - self._last_keyboard_step < self._keyboard_throttle_sec:
                return
            self._last_keyboard_step = now
            window_title = get_window_title()
            desc = f'User keyboard input on "{window_title} (window)" in "{window_title}" [...]'
            img = self._take_screenshot()
            prog = get_process_info()
            self._add_step(desc, img, window_title=window_title, program=prog, ui_elements=[])
        except Exception:
            pass

    def add_comment(self, text):
        text = (text or '').strip()
        if not text:
            return
        window_title = get_window_title()
        desc = f'User comment: {text}'
        img = self._take_screenshot()
        prog = get_process_info()
        self._add_step(desc, img, window_title=window_title, program=prog, ui_elements=[])

    def start(self):
        if self._running:
            return
        if not mouse:
            raise RuntimeError("pynput not installed: pip install pynput")
        self._session_start = datetime.now()
        self._running = True
        self._mouse_listener = mouse.Listener(on_click=self._on_click)
        self._mouse_listener.start()
        if keyboard:
            self._keyboard_listener = keyboard.Listener(on_press=self._on_key)
            self._keyboard_listener.start()

    def stop(self):
        self._running = False
        for lst in (self._mouse_listener, self._keyboard_listener):
            if lst:
                try:
                    lst.stop()
                except Exception:
                    pass
        self._mouse_listener = None
        self._keyboard_listener = None

    def get_steps(self):
        with self._lock:
            return list(self._steps)

    def get_step_count(self):
        with self._lock:
            return len(self._steps)

    def get_session_start(self):
        return self._session_start
