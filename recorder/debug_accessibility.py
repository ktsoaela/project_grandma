"""
Diagnostic: Prints ALL accessibility attributes for the element under the mouse.
Usage: Run this, then within 4 seconds, hover your mouse over the element you want to inspect.
"""
import sys
import time

print(">>> Move your mouse to the element you want to inspect...")
print(">>> You have 4 seconds...")
for i in range(4, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

# Get current mouse position
from Quartz import CGEventCreate, CGEventGetLocation
event = CGEventCreate(None)
loc = CGEventGetLocation(event)
x, y = loc.x, loc.y
print(f"\n=== Mouse at screen coordinates: ({x:.0f}, {y:.0f}) ===\n")

# Get frontmost app
from AppKit import NSWorkspace, NSScreen
workspace = NSWorkspace.sharedWorkspace()
front_app = workspace.frontmostApplication()
print(f"Frontmost App: {front_app.localizedName()}")
print(f"Bundle ID: {front_app.bundleIdentifier()}")
print(f"PID: {front_app.processIdentifier()}")

# Screen info
main_f = NSScreen.mainScreen().frame()
print(f"Main Screen: {main_f.size.width}x{main_f.size.height} (points)")
backing = NSScreen.mainScreen().backingScaleFactor()
print(f"Backing Scale Factor (Retina): {backing}x")
print()

# Try importing accessibility functions
try:
    from HIServices import (
        AXIsProcessTrusted, AXUIElementCreateApplication, AXUIElementCreateSystemWide,
        AXUIElementCopyAttributeValue, AXUIElementCopyElementAtPosition,
        AXUIElementCopyAttributeNames
    )
    print("Imported from HIServices ✅")
except ImportError:
    try:
        from Quartz import (
            AXIsProcessTrusted, AXUIElementCreateApplication, AXUIElementCreateSystemWide,
            AXUIElementCopyAttributeValue, AXUIElementCopyElementAtPosition,
            AXUIElementCopyAttributeNames
        )
        print("Imported from Quartz ✅")
    except ImportError:
        print("❌ FATAL: Cannot import accessibility functions from HIServices or Quartz!")
        sys.exit(1)

trusted = AXIsProcessTrusted()
print(f"Accessibility Trusted: {'✅ YES' if trusted else '❌ NO'}")
if not trusted:
    print("   >>> You need to grant Accessibility permission to Python/Terminal.")
    print(f"   >>> Python executable: {sys.executable}")
    sys.exit(1)

print()

def dump_element(elem, label="Element"):
    """Print ALL attributes of an accessibility element."""
    print(f"--- {label} ---")
    res, attr_names = AXUIElementCopyAttributeNames(elem, None)
    if res != 0:
        print(f"  (Could not get attribute names, error={res})")
        return
    
    print(f"  Attributes ({len(attr_names)}):")
    for attr in sorted(attr_names):
        try:
            res, val = AXUIElementCopyAttributeValue(elem, attr, None)
            if res == 0 and val is not None:
                val_str = str(val)
                if len(val_str) > 120:
                    val_str = val_str[:120] + "..."
                print(f"    {attr} = {val_str}")
            else:
                print(f"    {attr} = (error={res})")
        except Exception as e:
            print(f"    {attr} = (exception: {e})")
    print()

# Strategy 1: System-wide element at position
print("=" * 60)
print("STRATEGY 1: AXUIElementCopyElementAtPosition (SystemWide)")
print("=" * 60)
try:
    sys_ref = AXUIElementCreateSystemWide()
    res, elem = AXUIElementCopyElementAtPosition(sys_ref, float(x), float(y))
    print(f"  Result code: {res}")
    if res == 0 and elem:
        print(f"  Found element: {elem}")
        dump_element(elem, "SystemWide Element")
        
        # Walk up parents
        curr = elem
        for i in range(5):
            res, parent = AXUIElementCopyAttributeValue(curr, "AXParent", None)
            if res == 0 and parent:
                dump_element(parent, f"Parent {i+1}")
                curr = parent
            else:
                print(f"  (No more parents at level {i+1})")
                break
    else:
        print("  ❌ No element found")
except Exception as e:
    print(f"  ❌ Exception: {e}")

print()

# Strategy 2: Application-specific element at position
print("=" * 60)
print("STRATEGY 2: AXUIElementCopyElementAtPosition (Application)")
print("=" * 60)
try:
    pid = front_app.processIdentifier()
    app_ref = AXUIElementCreateApplication(pid)
    res, elem = AXUIElementCopyElementAtPosition(app_ref, float(x), float(y))
    print(f"  Result code: {res}")
    if res == 0 and elem:
        print(f"  Found element: {elem}")
        dump_element(elem, "App Element")
    else:
        print("  ❌ No element found")
except Exception as e:
    print(f"  ❌ Exception: {e}")

print()
print("=" * 60)
print("Done! Share the output above so we can see what attributes are available.")
print("=" * 60)
