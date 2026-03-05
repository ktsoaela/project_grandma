---
title: Click Circle - Documentation Index
description: Complete documentation index for the Click Circle feature
---

Welcome to the complete documentation for Project Grandma's **Click Circle Feature**. This documentation covers everything from quick customization to deep implementation details.

---

## 📚 Documentation Files

### 1. **[Quick Reference](/features/click-circle/quick-reference/)** ⚡
**Best for**: Quick lookups and fast changes

- TL;DR changes
- Popular customizations  
- Hex color codes
- Copy-paste examples

**Start here if**: You just want to change colors or sizes quickly.

---

### 2. **[Feature Guide](/features/click-circle/feature/)** 📖
**Best for**: Understanding how it all works

- Complete overview
- How it works  
- Feature breakdown
- Customization guide with examples
- Troubleshooting section

**Start here if**: You want a comprehensive understanding of the feature.

---

### 3. **[Visual Guide](/features/click-circle/visual-guide/)** 🎨
**Best for**: Visual learners and design decisions

- Size comparisons
- Border width variations
- Color psychology
- Complete configuration examples
- Responsive design guidelines

**Start here if**: You want to see visual examples before customizing.

---

### 4. **[Implementation Guide](/features/click-circle/implementation/)** 🔧
**Best for**: Developers and technical deep dives

- Architecture overview
- Frontend code walkthrough
- Backend code walkthrough
- Integration points
- Debugging tips
- Performance notes

**Start here if**: You're a developer who wants to understand the code.

---

## 🚀 Quick Start by Use Case

### "I want to change the color"
→ Go to [Quick Reference](/features/click-circle/quick-reference/) → Section "Change Circle Color"

### "I want to make the circle bigger"
→ Go to [Quick Reference](/features/click-circle/quick-reference/) → Section "Change Circle Size"

### "I want to see examples of different styles"
→ Go to [Visual Guide](/features/click-circle/visual-guide/) → Section "Complete Configuration Examples"

### "I want to understand how it works"
→ Go to [Feature Guide](/features/click-circle/feature/) → Section "How It Works"

### "I want to debug or modify the code"
→ Go to [Implementation Guide](/features/click-circle/implementation/) → Section "Frontend/Backend Implementation"

### "I'm creating documentation for others"
→ Go to [Feature Guide](/features/click-circle/feature/) → All sections

---

## 🎯 Feature Overview

The **Click Circle** feature adds visual indicators to Electron app clicks during screen recording.

### What It Does
- Shows an animated circle when users click
- Circles appear on all exported recordings (HTML, PDF, MP4)
- Helps viewers see exactly where clicks happened

### Architecture
```
User Click
    ↓
[Frontend UI] Shows animated circle (0.6s)
    ↓
[Python Backend] Draws circle on screenshot
    ↓
[Exports] All outputs include circles
```

### Key Files
- `grandama/renderer/style.css` - UI circle styling
- `grandama/renderer/renderer.js` - Click detection
- `recorder/capture.py` - Screenshot circle drawing

---

## 📋 Customization Cheat Sheet

### Most Common Changes

| What | File | Look For | Change |
|------|------|----------|--------|
| **Color** | Both files | `#4CAF50` | Replace with hex code |
| **Size** | Both files | `40px` (UI), `20` (Backend) | Increase/decrease |
| **Border** | Both files | `3px`, `width=3` | Thicker/thinner |
| **Speed** | style.css only | `0.6s` | Faster/slower |

### Example: Blue Circle
```css
/* style.css */
border: 3px solid #2196F3;
```
```python
# capture.py
outline='#2196F3'
```

### Example: Larger Circle
```css
/* style.css */
width: 50px;
height: 50px;
```
```python
# capture.py
circle_radius = 25
```

---

## 🔧 File Locations

```
project_grandma-DEV/
├── docs/
│   └── src/content/docs/features/click-circle/  (← Documentation)
│
├── grandama/
│   └── renderer/
│       ├── style.css             (← Circle CSS & animation)
│       ├── renderer.js           (← Click detection)
│       └── index.html
│
└── recorder/
    ├── capture.py                (← Circle drawing)
    ├── requirements.txt          (← Dependencies)
    └── server.py
```

---

## 🎨 Popular Customizations

### Professional (Green, Medium)
```
Color: #4CAF50 (Green)
Size: 40px (UI), 20 (Backend)
Border: 3px
Speed: 0.6s
```

### Bold (Red, Large)
```
Color: #FF5252 (Red)
Size: 50px (UI), 25 (Backend)
Border: 4px
Speed: 0.8s
```

### Tech (Blue, Slim)
```
Color: #2196F3 (Blue)
Size: 35px (UI), 17 (Backend)
Border: 2px
Speed: 0.5s
```

See [Visual Guide](/features/click-circle/visual-guide/) for more styles.

---

## ⚙️ Quick Reference

### Change Circle Color
1. Open `grandama/renderer/style.css`
2. Find `.click-circle { border: 3px solid #4CAF50; }`
3. Replace `#4CAF50` with your hex code
4. Open `recorder/capture.py`
5. Find `outline='#4CAF50'`
6. Replace with same hex code
7. Rebuild: `npm run build:mac`

### Change Circle Size
1. **Frontend**: Update `width` and `height` in `.click-circle` (style.css)
2. **Backend**: Update `circle_radius` in `_take_screenshot()` (capture.py)
3. Rule: Backend radius ≈ Frontend width ÷ 2
4. Rebuild: `npm run build:mac`

### Change Animation Speed
1. Open `grandama/renderer/style.css`
2. Find `animation: clickRipple 0.6s ease-out forwards;`
3. Change `0.6s` to desired duration (e.g., `0.3s` for fast, `1s` for slow)
4. Rebuild: `npm run build:mac`

---

## 🐛 Troubleshooting

### Circle not showing in exports
- Check: Is Pillow installed? `pip install -r recorder/requirements.txt`
- Check: Did you rebuild the app? `npm run build:mac`

### Circle position is wrong
- Check: Are frontend and backend coordinates matching?
- Debug: Add console logs to both files

### Colors don't match
- Check: Same hex code in **both** style.css and capture.py
- Check: Have you rebuilt? `npm run build:mac`

See [Feature Guide - Troubleshooting](/features/click-circle/feature/#troubleshooting) for more solutions.

---

## 📝 Frequently Asked Questions

### Q: Can I have different colors for different click types (left/right)?
A: Yes! Modify the backend `_on_click()` method to use different colors based on `button` parameter.

### Q: Can I have circles only on certain elements?
A: Yes! Add a filter in the frontend click handler to check `e.target`.

### Q: Does the circle affect performance?
A: Minimal. Frontend animation is GPU-accelerated. Backend adds ~5-10% screenshot overhead.

### Q: Can I remove circles after a certain time?
A: Yes! The frontend circle already removes itself after 0.6s. The backend circle is permanent (by design).

### Q: How do I match circle size between platforms?
A: Use proportional sizing: `radius = width ÷ 2`

See [Feature Guide](/features/click-circle/feature/) for complete FAQ.

---

## 🚀 Getting Started

### For Non-Developers (Just want to customize)
1. Read: [Quick Reference](/features/click-circle/quick-reference/)
2. Pick a customization from "Popular Customizations"
3. Copy the code examples
4. Paste into the appropriate files
5. Run: `npm run build:mac`

### For Developers (Want to understand/modify)
1. Read: [Feature Guide](/features/click-circle/feature/) overview
2. Review: [Implementation Guide](/features/click-circle/implementation/) architecture
3. Reference: [Visual Guide](/features/click-circle/visual-guide/) for design considerations
4. Debug: Use testing checklist in Implementation Guide

---

## 📚 Full Documentation Hierarchy

```
Click Circle Index (You are here)
├── Quick Reference
│   ├── TL;DR changes
│   ├── Popular styles
│   └── Quick copy-paste
├── Feature Guide
│   ├── Overview
│   ├── How it works
│   ├── Complete customization guide
│   └── Troubleshooting
├── Visual Guide
│   ├── Size variations
│   ├── Border variations
│   ├── Color psychology
│   ├── Configuration examples
│   └── Device-specific recommendations
└── Implementation Guide
    ├── Architecture
    ├── Frontend code walkthrough
    ├── Backend code walkthrough
    ├── Integration points
    └── Debugging guide
```

---

## 🔗 Related Files

- `grandama/renderer/index.html` - App UI structure
- `grandama/renderer/renderer.js` - App logic
- `grandama/main.js` - Electron main process
- `recorder/server.py` - Flask server
- `recorder/requirements.txt` - Python dependencies

---

Start with [Quick Reference](/features/click-circle/quick-reference/) for immediate customization, or [Feature Guide](/features/click-circle/feature/) for comprehensive understanding!
