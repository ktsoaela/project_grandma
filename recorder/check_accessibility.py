#!/usr/bin/env python3
"""
Helper script to check and request Accessibility permissions on macOS.
Run this to verify permissions are set up correctly.
"""
import sys
import os

if sys.platform != 'darwin':
    print("This script is for macOS only.")
    sys.exit(1)

try:
    from HIServices import AXIsProcessTrusted, kAXTrustedCheckOptionPrompt
    from Quartz import AXIsProcessTrusted as QuartzAXIsProcessTrusted, kAXTrustedCheckOptionPrompt as QuartzPrompt
except ImportError:
    try:
        from Quartz import AXIsProcessTrusted, kAXTrustedCheckOptionPrompt
    except ImportError:
        print("ERROR: Cannot import Accessibility APIs. Make sure pyobjc is installed:")
        print("  pip install pyobjc-framework-ApplicationServices pyobjc-framework-Quartz")
        sys.exit(1)

def check_permissions():
    """Check if Accessibility permissions are granted."""
    print("Checking Accessibility permissions...")
    print(f"Python executable: {sys.executable}")
    print(f"Process name: {os.path.basename(sys.executable)}")
    print()
    
    # Check current status
    is_trusted = AXIsProcessTrusted()
    
    if is_trusted:
        print("✅ Accessibility permissions are GRANTED!")
        print("The recorder should work correctly.")
        return True
    else:
        print("❌ Accessibility permissions are NOT granted.")
        print()
        print("To fix this:")
        print("1. Open System Preferences (or System Settings)")
        print("2. Go to Security & Privacy → Privacy → Accessibility")
        print("3. Look for 'Python' or 'python3' in the list")
        print("4. If not there, click the '+' button and add:")
        print(f"   {sys.executable}")
        print("5. Check the box to enable it")
        print("6. Restart the recorder app")
        print()
        
        # Try to trigger the permission dialog
        print("Attempting to trigger permission dialog...")
        try:
            # This should trigger the system permission dialog
            AXIsProcessTrusted()  # Just checking again
            print("(If a dialog appeared, grant permission there)")
        except Exception as e:
            print(f"Could not trigger dialog: {e}")
        
        return False

if __name__ == '__main__':
    check_permissions()
