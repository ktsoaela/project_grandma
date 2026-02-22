"""
Windows-only: foreground window title, process info (exe, name), UI element at point.
Used for PSR-style step descriptions and Additional Details.
"""
import sys
import os

if sys.platform != 'win32':
    def get_window_title(): return ''
    def get_process_info(): return None
    def get_element_at_point(x, y): return ('', ' (unknown)', [])
    def get_os_version(): return ''
else:
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    psapi = ctypes.windll.psapi

    def get_window_title():
        try:
            hwnd = user32.GetForegroundWindow()
            if not hwnd:
                return ''
            length = user32.GetWindowTextLengthW(hwnd)
            if length <= 0:
                return ''
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            return buf.value or ''
        except Exception:
            return ''

    def get_process_info():
        """Return dict with name, version, company, exe_path for foreground window."""
        try:
            hwnd = user32.GetForegroundWindow()
            if not hwnd:
                return None
            pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            if not pid.value:
                return None
            # PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            h = kernel32.OpenProcess(0x1000, False, pid.value)
            if not h:
                return None
            try:
                path_buf = ctypes.create_unicode_buffer(512)
                size = wintypes.DWORD(512)
                if kernel32.QueryFullProcessImageNameW(h, 0, path_buf, ctypes.byref(size)):
                    exe_path = path_buf.value
                    exe_name = os.path.basename(exe_path)
                else:
                    exe_path = exe_name = ''
                version = ''
                company = ''
                # Version/company optional; can be filled by file properties later
                return {
                    'name': exe_name.replace('.exe', '') if exe_name else '',
                    'version': version or '0.0.0.0',
                    'company': company or '',
                    'exe': exe_name or '',
                    'exe_path': exe_path or '',
                }
            finally:
                kernel32.CloseHandle(h)
        except Exception:
            return None

    def get_element_at_point(x, y):
        """Return (element_label, control_type_suffix, ui_elements_chain) for PSR-style text.
        Matches PSR format: element Name + (LocalizedControlType) in window title.
        """
        try:
            import uiautomation as auto
        except ImportError:
            return ('', '', [])
        try:
            elem = auto.ControlFromPoint(x, y)
            if elem is None:
                return ('', '', [])
            name = (elem.Name or '').strip()
            # Try to get LocalizedControlType (PSR uses this, e.g. "region", "button", "text")
            ctrl_type = ''
            try:
                # uiautomation might expose LocalizedControlType directly
                localized = getattr(elem, 'LocalizedControlType', None)
                if localized:
                    ctrl_type = str(localized).strip()
                else:
                    # Fallback: try to get via UIA property or map ControlType
                    ct = getattr(elem, 'ControlType', None)
                    if ct is not None:
                        # Map common ControlType IDs to PSR-style names
                        type_map = {
                            50000: 'button',
                            50001: 'calendar',
                            50002: 'check box',
                            50003: 'combo box',
                            50004: 'edit',
                            50005: 'hyperlink',
                            50006: 'image',
                            50007: 'list item',
                            50008: 'list',
                            50009: 'menu',
                            50010: 'menu bar',
                            50011: 'menu item',
                            50012: 'pane',
                            50013: 'progress bar',
                            50014: 'radio button',
                            50015: 'scroll bar',
                            50016: 'slider',
                            50017: 'spinner',
                            50018: 'status bar',
                            50019: 'tab',
                            50020: 'tab item',
                            50021: 'text',
                            50022: 'tool bar',
                            50023: 'tool tip',
                            50024: 'tree',
                            50025: 'tree item',
                            50026: 'custom',
                            50027: 'group',
                            50028: 'thumbnail',
                            50029: 'data grid',
                            50030: 'data item',
                            50031: 'document',
                            50032: 'split button',
                            50033: 'window',
                        }
                        ctrl_type = type_map.get(ct, 'control')
            except Exception:
                pass
            if not ctrl_type:
                ctrl_type = 'control'
            suffix = ' (' + ctrl_type + ')' if ctrl_type else ''
            # Build UI elements chain (for Additional Details) - walk up parents
            chain = []
            current = elem
            seen = set()
            for _ in range(100):
                if current is None or id(current) in seen:
                    break
                seen.add(id(current))
                n = (current.Name or getattr(current, 'AutomationId', None) or getattr(current, 'ClassName', None) or '')
                if isinstance(n, str) and n.strip():
                    chain.append(n.strip())
                try:
                    current = current.GetParentControl()
                except Exception:
                    break
            return (name or '(unknown)', suffix, chain)
        except Exception:
            return ('', '', [])

    def get_os_version():
        try:
            import platform
            v = platform.platform()
            if v:
                return v
            return os.environ.get('OS', '') + ' "Windows"'
        except Exception:
            return ''
