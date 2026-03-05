"""
macOS: foreground window title, process info, UI element at point.
Used for PSR-style step descriptions and Additional Details.
"""
import sys
import os
import subprocess
import platform

if sys.platform != 'darwin':
    def get_window_title(): return ''
    def get_process_info(): return None
    def get_element_at_point(x, y): return ('', ' (unknown)', [], '', '')
    def get_os_version(): return ''
else:
    # --- Import AppKit (always available with pyobjc) ---
    try:
        from AppKit import NSWorkspace, NSScreen
    except ImportError:
        NSWorkspace = None
        NSScreen = None

    # --- Import Accessibility functions ---
    # These might come from HIServices or Quartz depending on pyobjc version/config
    _AXIsProcessTrusted = None
    _AXUIElementCreateApplication = None
    _AXUIElementCreateSystemWide = None
    _AXUIElementCopyAttributeValue = None
    _AXUIElementCopyElementAtPosition = None
    _AXUIElementCopyAttributeNames = None
    _ax_elem_at_pos_nargs = 3  # will detect below

    for _mod_name in ['HIServices', 'Quartz']:
        try:
            _mod = __import__(_mod_name)
            for _fn_name, _attr in [
                ('AXIsProcessTrusted', '_AXIsProcessTrusted'),
                ('AXUIElementCreateApplication', '_AXUIElementCreateApplication'),
                ('AXUIElementCreateSystemWide', '_AXUIElementCreateSystemWide'),
                ('AXUIElementCopyAttributeValue', '_AXUIElementCopyAttributeValue'),
                ('AXUIElementCopyElementAtPosition', '_AXUIElementCopyElementAtPosition'),
                ('AXUIElementCopyAttributeNames', '_AXUIElementCopyAttributeNames'),
            ]:
                if hasattr(_mod, _fn_name) and globals()[_attr] is None:
                    globals()[_attr] = getattr(_mod, _fn_name)
        except ImportError:
            pass

    # Detect AXUIElementCopyElementAtPosition argument count (3 or 4 depending on pyobjc)
    if _AXUIElementCopyElementAtPosition:
        try:
            import inspect
            sig = inspect.signature(_AXUIElementCopyElementAtPosition)
            _ax_elem_at_pos_nargs = len(sig.parameters)
        except:
            # Try calling with 4 args on a dummy to detect
            try:
                _sw = _AXUIElementCreateSystemWide()
                _AXUIElementCopyElementAtPosition(_sw, 0.0, 0.0, None)
                _ax_elem_at_pos_nargs = 4
            except TypeError:
                _ax_elem_at_pos_nargs = 3
            except:
                _ax_elem_at_pos_nargs = 4  # default to 4

    def _ax_copy_attr(elem, attr):
        """Safe wrapper for AXUIElementCopyAttributeValue. Returns (result, value)."""
        if not _AXUIElementCopyAttributeValue:
            return (-1, None)
        try:
            res, val = _AXUIElementCopyAttributeValue(elem, attr, None)
            return (res, val)
        except:
            return (-1, None)

    def _ax_element_at_position(ref, x, y):
        """Safe wrapper that handles 3-arg vs 4-arg pyobjc variants."""
        if not _AXUIElementCopyElementAtPosition:
            return (-1, None)
        try:
            if _ax_elem_at_pos_nargs >= 4:
                return _AXUIElementCopyElementAtPosition(ref, float(x), float(y), None)
            else:
                return _AXUIElementCopyElementAtPosition(ref, float(x), float(y))
        except:
            return (-1, None)

    def _ax_get_attr_names(elem):
        """Get list of attribute names for an element."""
        if not _AXUIElementCopyAttributeNames:
            return []
        try:
            res, names = _AXUIElementCopyAttributeNames(elem, None)
            return list(names) if (res == 0 and names) else []
        except:
            return []

    def get_os_version():
        try:
            return platform.platform()
        except:
            return 'macOS'

    def get_process_info():
        """Return dict with name, version, company, exe_path for foreground window."""
        if not NSWorkspace:
            return None
        try:
            workspace = NSWorkspace.sharedWorkspace()
            front_app = workspace.frontmostApplication()
            if not front_app:
                return None

            app_name = front_app.localizedName() or ''
            bundle_id = front_app.bundleIdentifier() or ''
            bundle_path = front_app.bundleURL()
            exe_path = ''
            exe_name = ''

            if bundle_path:
                exe_path = str(bundle_path.path())
                exe_name = os.path.basename(exe_path)
                if exe_name.endswith('.app'):
                    contents_path = os.path.join(exe_path, 'Contents', 'MacOS')
                    if os.path.exists(contents_path):
                        executables = [f for f in os.listdir(contents_path)
                                     if os.path.isfile(os.path.join(contents_path, f))]
                        if executables:
                            exe_name = executables[0]
                            exe_path = os.path.join(contents_path, exe_name)

            version = '0.0.0'
            try:
                if bundle_path:
                    info_plist = os.path.join(str(bundle_path.path()), 'Contents', 'Info.plist')
                    if os.path.exists(info_plist):
                        r = subprocess.run(['defaults', 'read', info_plist, 'CFBundleShortVersionString'],
                                         capture_output=True, text=True, timeout=1)
                        if r.returncode == 0:
                            version = r.stdout.strip() or '0.0.0'
            except:
                pass

            company = ''
            if bundle_id:
                parts = bundle_id.split('.')
                company = parts[-2] if len(parts) >= 2 else parts[0]
                if company == 'com' and len(parts) > 2:
                    company = parts[1]

            return {
                'name': app_name.replace('.app', ''),
                'version': version,
                'company': company or '',
                'exe': exe_name,
                'exe_path': exe_path,
            }
        except:
            return None

    def get_window_title():
        """Get the title of the frontmost window."""
        if not NSWorkspace:
            return ''
        try:
            workspace = NSWorkspace.sharedWorkspace()
            front_app = workspace.frontmostApplication()
            if not front_app:
                return ''

            pid = front_app.processIdentifier()

            # Accessibility - get exact window title
            if _AXUIElementCreateApplication and _AXUIElementCopyAttributeValue:
                try:
                    app_ref = _AXUIElementCreateApplication(pid)
                    res, children = _ax_copy_attr(app_ref, "AXChildren")
                    if res == 0 and children:
                        for win in children:
                            res, role = _ax_copy_attr(win, "AXRole")
                            if res == 0 and role == 'AXWindow':
                                res, title = _ax_copy_attr(win, "AXTitle")
                                if res == 0 and title:
                                    t = str(title).strip()
                                    if t:
                                        return t
                except:
                    pass

            # Fallback: app name
            return front_app.localizedName() or ''
        except:
            return ''

    def _get_element_info(elem):
        """Extract name, control type suffix, and parent chain from an AX element."""
        name = ''
        control_type = 'control'
        chain = []

        # Get available attributes for this element
        available = _ax_get_attr_names(elem)

        # Try to find a name from various attributes (only check ones that exist)
        name_attrs_to_try = ['AXTitle', 'AXDescription', 'AXLabel', 'AXValue', 'AXHelp',
                             'AXPlaceholderValue']
        for attr in name_attrs_to_try:
            if attr in available:
                res, val = _ax_copy_attr(elem, attr)
                if res == 0 and val:
                    s = str(val).strip()
                    if s and len(s) < 200:
                        name = s
                        break

        # Get role
        role = ''
        res, r_val = _ax_copy_attr(elem, "AXRole")
        if res == 0 and r_val:
            role = str(r_val).lower()

        subrole = ''
        if 'AXSubrole' in available:
            res, s_val = _ax_copy_attr(elem, "AXSubrole")
            if res == 0 and s_val:
                subrole = str(s_val).lower()

        # Map to PSR-style control types
        type_map = {
            'axbutton': 'button', 'axtextfield': 'edit', 'axstatictext': 'text',
            'axtextarea': 'edit', 'axcheckbox': 'check box', 'axradiobutton': 'radio button',
            'axpopupbutton': 'combo box', 'axmenu': 'menu', 'axmenuitem': 'menu item',
            'axmenubar': 'menu bar', 'axtoolbar': 'tool bar', 'axslider': 'slider',
            'axscrollbar': 'scroll bar', 'axtab': 'tab', 'axgroup': 'group',
            'aximage': 'image', 'axlink': 'hyperlink', 'axlist': 'list',
            'axtable': 'data grid', 'axrow': 'list item', 'axcell': 'data item',
            'axwindow': 'window', 'axscrollarea': 'pane', 'axwebarea': 'web page',
        }
        raw = subrole if (subrole and subrole != 'axunknown') else role
        control_type = type_map.get(raw, raw.replace('ax', ''))
        if not control_type or control_type == 'unknown':
            control_type = 'control'

        # Name fallback
        if not name:
            # Use RoleDescription if available
            if 'AXRoleDescription' in available:
                res, rd = _ax_copy_attr(elem, "AXRoleDescription")
                if res == 0 and rd:
                    rd_str = str(rd).strip()
                    if rd_str:
                        name = rd_str
            # Use control type
            if not name:
                if control_type and control_type not in ['control', 'group', 'pane']:
                    name = control_type
                else:
                    name = 'element'

        # Walk up parents to find owning AXWindow title and AXApplication name
        window_title = ''
        app_name = ''
        curr = elem
        for _ in range(30):
            try:
                r, rv = _ax_copy_attr(curr, "AXRole")
                if r == 0 and rv:
                    role_str = str(rv)
                    if role_str == 'AXWindow' and not window_title:
                        r2, t = _ax_copy_attr(curr, "AXTitle")
                        if r2 == 0 and t:
                            window_title = str(t).strip()
                    elif role_str == 'AXApplication' and not app_name:
                        r2, t = _ax_copy_attr(curr, "AXTitle")
                        if r2 == 0 and t:
                            app_name = str(t).strip()
                        # Once we have the app, we're done
                        if window_title:
                            break
                r, p = _ax_copy_attr(curr, "AXParent")
                if r == 0 and p:
                    curr = p
                else:
                    break
            except:
                break

        # Build parent chain (up to 10 levels)
        curr = elem
        for _ in range(10):
            try:
                c_name = ''
                for attr in ['AXTitle', 'AXDescription', 'AXLabel']:
                    r, v = _ax_copy_attr(curr, attr)
                    if r == 0 and v:
                        c_name = str(v).strip()
                        if c_name:
                            break
                r, rv = _ax_copy_attr(curr, "AXRole")
                c_role = str(rv).replace('AX', '') if (r == 0 and rv) else ''
                item = f"{c_role}: '{c_name}'" if c_name else c_role
                if item:
                    chain.append(item)
                r, p = _ax_copy_attr(curr, "AXParent")
                if r == 0 and p:
                    curr = p
                else:
                    break
            except:
                break

        # Return 5-tuple: (name, suffix, chain, window_title, app_name)
        return (name, f' ({control_type})', chain, window_title, app_name)

    def get_element_at_point(x, y):
        """Find the UI element at screen coordinates (x, y) from pynput (top-left origin, points)."""
        # Check accessibility permission
        if _AXIsProcessTrusted and not _AXIsProcessTrusted():
            proc = os.path.basename(sys.executable)
            return ('', f' (accessibility permission required for {proc})', [], '', '')

        if not _AXUIElementCopyElementAtPosition:
            return ('element', ' (control)', [], '', '')

        # Retina: pynput usually gives points, but sanity-check
        try:
            if NSScreen:
                main_f = NSScreen.mainScreen().frame()
                mw, mh = main_f.size.width, main_f.size.height
                if x > mw * 1.5 or y > mh * 1.5:
                    x /= 2.0
                    y /= 2.0
        except:
            pass

        # Strategy 1: System-wide hit test
        try:
            sw = _AXUIElementCreateSystemWide()
            res, elem = _ax_element_at_position(sw, x, y)
            if res == 0 and elem:
                info = _get_element_info(elem)
                # If we got a real name, return it
                if info[0] and info[0] != 'element':
                    return info
                # Even if name='element', still return if we got a real role
                if info[1] and info[1] != ' (control)':
                    return info
        except:
            pass

        # Strategy 2: App-specific hit test
        try:
            if NSWorkspace:
                workspace = NSWorkspace.sharedWorkspace()
                front_app = workspace.frontmostApplication()
                if front_app:
                    app_ref = _AXUIElementCreateApplication(front_app.processIdentifier())
                    res, elem = _ax_element_at_position(app_ref, x, y)
                    if res == 0 and elem:
                        return _get_element_info(elem)
        except:
            pass

        return ('element', ' (control)', [], '', '')
