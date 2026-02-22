---
title: Troubleshooting
description: Solve common Project Grandma issues
---

## App Won't Start

### Windows

**Problem:** "Project Grandma won't open"

**Solutions:**
1. Try running as Administrator
2. Check if Python 3 is installed
3. Disable antivirus temporarily
4. Reinstall using the installer

**To reinstall:**
```
Settings → Apps → Project Grandma → Uninstall
Then download fresh installer from our website
```

### macOS

**Problem:** "Project Grandma is damaged" or "Can't be opened"

**Solution:** Grant permission
1. Right-click Project Grandma
2. Click "Open"
3. Click "Open" in security dialog
4. It should now work

**Problem:** "Apple can't verify the developer"

**Solution:**
```
System Preferences → Security & Privacy
Click "Open Anyway"
```

## Recording Won't Start

**Problem:** Click "Start Record" but nothing happens

**Checklist:**
- [ ] Enough disk space? (>1GB free)
- [ ] No other recording software running
- [ ] Try restarting the app
- [ ] Try restarting your computer
- [ ] Update to latest version

## Recording Stops

**Problem:** Recording stops mid-way

**Causes & Solutions:**

1. **Out of disk space**
   - Check: `C:\Disk Management` (Windows)
   - Free up space
   - Try again

2. **Antivirus interference**
   - Temporarily disable antivirus
   - Whitelist Project Grandma
   - Restart recording

3. **Running out of memory**
   - Close other apps
   - Lower number of stored screenshots
   - Try smaller recording

4. **Python server crashed** (Development mode)
   - Restart the app
   - Try production version instead

## File Issues

**Problem:** Exported file is empty or corrupted

**Try:**
1. Attempt recording again
2. Use simpler recording (fewer steps)
3. Export in different format
4. Restart computer and try again

**Problem:** Can't find exported file

**Location:**
- Windows: `C:\Users\[You]\AppData\Local\Temp\`
- macOS: `/tmp/`

**To open directly:**
- Windows: Press `Win + R`, type `%TEMP%`, press Enter
- macOS: Open Finder, press `Cmd + Shift + G`, type `/tmp`

**Problem:** Export button does nothing

**Solutions:**
- Click "Open" first, then button activates
- Wait 5 seconds after "Stop Record"
- Try different export format

## Export Issues

**Problem:** HTML file won't open in browser

**Try:**
1. Use different browser (Chrome, Firefox, Edge)
2. Try double-clicking the file
3. Drag file onto browser window
4. Right-click → "Open with" → Choose browser

**Problem:** PDF won't open

**Try:**
1. Install Adobe Reader (free)
2. Update your PDF reader
3. Try exporting again

**Problem:** Video won't play

**Try:**
1. Install VLC Media Player (free)
2. Update Windows Media Player
3. Try different video player
4. Check file isn't corrupted (re-export)

**Problem:** Markdown images not showing

**Reason:** Images folder got separated from .md file

**Fix:**
1. Keep image folder in same directory
2. Upload both folder and .md to hosting service
3. Use HTML export for single-file sharing

## Performance Issues

**Problem:** App is slow or laggy

**Solutions:**
1. Close other apps
2. Restart your computer
3. Reduce number of stored screenshots
4. Disable video recording
5. Update to latest version

**Problem:** High CPU/Memory usage

**Solutions:**
1. Record shorter sessions
2. Reduce screenshot storage
3. Disable video recording
4. Close background apps
5. Upgrade computer RAM (advanced)

## Windows-Specific

**Problem:** "Windows SmartScreen prevented an unrecognized app"

**This is normal** for unsigned apps

**Solution:**
1. Click "More info"
2. Click "Run anyway"
3. App will launch

**Problem:** Installer won't run

**Try:**
1. Download again (file may be corrupted)
2. Disable antivirus temporarily
3. Copy to Desktop first
4. Run as Administrator (right-click)

## macOS-Specific

**Problem:** "Missing dependencies" error

**Solution:**
1. Fully restart your Mac
2. Reinstall from DMG
3. Check macOS permissions
4. Update macOS if possible

**Problem:** Microphone/Screen recording denied

**Fix:**
1. System Preferences → Security & Privacy
2. Look for "Screen Recording" and "Microphone"
3. Add Project Grandma to both lists
4. Restart app

## Network Issues

**Problem:** Can't check for updates

This is OK - you don't need internet to use Project Grandma.

If needed:
1. Check your internet connection
2. Disable firewall temporarily
3. Check if your ISP blocks updates

## Still Not Working?

1. Check [FAQ](/help/faq/) for common questions
2. Search [GitHub Issues](https://github.com/ktsoaela/project_grandma/issues)
3. Create new issue with details:
   - Your OS and version
   - What you were doing
   - Error message
   - Steps to reproduce
