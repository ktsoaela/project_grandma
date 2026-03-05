"""Move mouse to the given screen coordinates and perform a real OS left-click.
Called from Playwright tests: Playwright selects the target and computes (x, y); this script
moves and clicks so the recorder (pynput) sees real input.
Usage: python real_click.py <screen_x> <screen_y>
Requires: pip install pyautogui"""
import sys
try:
    import pyautogui
except ImportError:
    print("Install pyautogui: pip install pyautogui", file=sys.stderr)
    sys.exit(1)
x = int(round(float(sys.argv[1])))
y = int(round(float(sys.argv[2])))
pyautogui.moveTo(x, y, duration=0.15)
pyautogui.click()
