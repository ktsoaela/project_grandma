#!/bin/bash
# Helper script to fix Accessibility permissions on macOS

echo "=========================================="
echo "macOS Accessibility Permission Fixer"
echo "=========================================="
echo ""

# Find Python executable
if [ -d "../venv" ]; then
    PYTHON_EXEC="../venv/bin/python3"
    echo "Using virtual environment Python: $PYTHON_EXEC"
else
    PYTHON_EXEC=$(which python3)
    echo "Using system Python: $PYTHON_EXEC"
fi

if [ ! -f "$PYTHON_EXEC" ]; then
    PYTHON_EXEC=$(which python3)
fi

echo "Python path: $PYTHON_EXEC"
echo ""

# Check permissions
echo "Checking current permissions..."
cd "$(dirname "$0")"
if [ -d "../venv" ]; then
    source ../venv/bin/activate
fi

python3 << 'EOF'
import sys
import os

try:
    from HIServices import AXIsProcessTrusted
except ImportError:
    try:
        from Quartz import AXIsProcessTrusted
    except ImportError:
        print("ERROR: Cannot check permissions - pyobjc not installed")
        sys.exit(1)

is_trusted = AXIsProcessTrusted()
print(f"Accessibility permissions: {'✅ GRANTED' if is_trusted else '❌ NOT GRANTED'}")
print(f"Python executable: {sys.executable}")
print(f"Process name: {os.path.basename(sys.executable)}")
print()

if not is_trusted:
    print("=" * 50)
    print("TO FIX:")
    print("=" * 50)
    print("1. Open System Preferences (or System Settings)")
    print("2. Go to: Security & Privacy → Privacy → Accessibility")
    print("3. Click the lock icon (bottom left) to make changes")
    print("4. Look for one of these in the list:")
    print(f"   - Python")
    print(f"   - python3")
    print(f"   - {os.path.basename(sys.executable)}")
    print(f"   - {sys.executable}")
    print("5. If not found, click '+' and add:")
    print(f"   {sys.executable}")
    print("6. Check the box to enable it")
    print("7. Restart the recorder app")
    print()
    print("Opening System Preferences...")
    # Try different methods to open System Preferences
    import subprocess
    try:
        # macOS Ventura+ (System Settings)
        subprocess.run(["open", "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"], check=False)
    except:
        try:
            # Older macOS (System Preferences)
            subprocess.run(["open", "/System/Library/PreferencePanes/Security.prefPane"], check=False)
        except:
            print("Please manually open System Preferences → Security & Privacy → Privacy → Accessibility")
EOF

echo ""
echo "After granting permissions, restart the recorder app."
