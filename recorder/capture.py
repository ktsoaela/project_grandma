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

try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

if sys.platform == 'win32':
    try:
        from win_info import get_window_title, get_process_info, get_element_at_point, get_os_version
    except ImportError:
        get_window_title = lambda: ''
        get_process_info = lambda: None
        get_element_at_point = lambda x, y: ('', '', [])
        get_os_version = lambda: ''
elif sys.platform == 'darwin':
    try:
        from mac_info import get_window_title, get_process_info, get_element_at_point, get_os_version
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
    def __init__(self, on_step, max_screenshots=25, capture_typed_text=False):
        self.on_step = on_step
        self.max_screenshots = max(1, max_screenshots)
        self.capture_typed_text = capture_typed_text
        self._steps = []
        self._lock = threading.Lock()
        self._mouse_listener = None
        self._keyboard_listener = None
        self._running = False
        self._session_start = None
        self._last_keyboard_step = 0
        self._keyboard_throttle_sec = 2.0
        self._typed_buffer = []  # accumulates typed characters when capture_typed_text is True
        self._typed_lock = threading.Lock()

    def _take_screenshot(self, click_x=None, click_y=None):
        """Take a screenshot and optionally draw a circle at click location."""
        if not mss:
            return None
        try:
            with mss.mss() as sct:
                mon = sct.monitors[0]
                shot = sct.grab(mon)
                
                # Draw circle at click location if provided
                if click_x is not None and click_y is not None and PIL_AVAILABLE:
                    # Convert MSS screenshot to PIL Image
                    img = Image.frombytes('RGB', shot.size, shot.rgb)
                    draw = ImageDraw.Draw(img)
                    
                    # Draw a green circle at the click location
                    circle_radius = 20
                    x1 = click_x - circle_radius
                    y1 = click_y - circle_radius
                    x2 = click_x + circle_radius
                    y2 = click_y + circle_radius
                    
                    # Draw green circle (RGB: 76, 175, 80)
                    draw.ellipse([x1, y1, x2, y2], outline='#4CAF50', width=3)
                    
                    # Convert back to PNG bytes
                    from io import BytesIO
                    buf = BytesIO()
                    img.save(buf, format='PNG')
                    img_bytes = buf.getvalue()
                else:
                    img_bytes = mss.tools.to_png(shot.rgb, shot.size)
                
                return base64.b64encode(img_bytes).decode('ascii')
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
        elem_result = get_element_at_point(x, y)
        # Handle both 3-tuple (win_info) and 5-tuple (mac_info) return
        elem_name = elem_result[0]
        suffix = elem_result[1]
        chain = elem_result[2] if len(elem_result) > 2 else []
        # On macOS, the 4th element is the window title from the clicked element's AX hierarchy
        elem_window_title = elem_result[3] if len(elem_result) > 3 else ''
        # On macOS, the 5th element is the application name
        elem_app_name = elem_result[4] if len(elem_result) > 4 else ''

        # Use the window title from the element hierarchy (accurate even when recorder is foreground)
        # For menu/dock items that don't have a window, use the app name
        # Fall back to get_window_title() only as last resort
        window_title = elem_window_title or elem_app_name or get_window_title()

        label = self._element_label(elem_name, suffix)
        btn = str(button).replace('Button.', '')
        if btn == 'left':
            action = 'User left click'
        elif btn == 'right':
            action = 'User right click'
        else:
            action = f'User {btn} click'
        desc = f'{action} on "{label}" in "{window_title}"'
        img = self._take_screenshot(click_x=x, click_y=y)
        prog = get_process_info()
        self._add_step(desc, img, window_title=window_title, program=prog, ui_elements=chain)

    def _key_to_text(self, key):
        """Convert a pynput key to printable text."""
        try:
            if hasattr(key, 'char') and key.char:
                return key.char
        except AttributeError:
            pass
        # Special keys
        try:
            name = key.name if hasattr(key, 'name') else str(key)
            special_map = {
                'space': ' ', 'enter': '↵', 'return': '↵',
                'tab': '⇥', 'backspace': '⌫',
                'shift': '', 'shift_l': '', 'shift_r': '',
                'ctrl': '', 'ctrl_l': '', 'ctrl_r': '',
                'alt': '', 'alt_l': '', 'alt_r': '',
                'cmd': '', 'cmd_l': '', 'cmd_r': '',
                'caps_lock': '', 'esc': '⎋',
            }
            if name.lower() in special_map:
                return special_map[name.lower()]
            # F-keys, arrows, etc.
            if name.startswith('f') and name[1:].isdigit():
                return f'[{name.upper()}]'
            if name in ('up', 'down', 'left', 'right'):
                return f'[{name}]'
            if name in ('delete', 'home', 'end', 'page_up', 'page_down'):
                return f'[{name}]'
        except:
            pass
        return ''

    def _on_key(self, key):
        try:
            import time

            # If capturing typed text, accumulate into buffer
            if self.capture_typed_text:
                char = self._key_to_text(key)
                if char:
                    with self._typed_lock:
                        self._typed_buffer.append(char)

            now = time.monotonic()
            if now - self._last_keyboard_step < self._keyboard_throttle_sec:
                return
            self._last_keyboard_step = now

            # Get window title
            window_title = get_window_title()

            # Build description
            if self.capture_typed_text:
                with self._typed_lock:
                    typed = ''.join(self._typed_buffer)
                    self._typed_buffer.clear()
                if typed.strip():
                    desc = f'User typed "{typed}" in "{window_title} (window)"'
                else:
                    desc = f'User keyboard input on "{window_title} (window)" in "{window_title}" [...]'
            else:
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
