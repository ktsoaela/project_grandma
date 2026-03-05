# Click Circle Feature Documentation

## Overview

The **Click Circle** feature provides visual feedback when users click on elements during recording. A green circle appears at the exact click location on all captured screenshots and exported files (HTML, PDF, video).

This makes it easy to see exactly where the user clicked in the recorded steps, improving clarity and understanding of the recording.

---

## How It Works

### Two-Part System

The click circle feature consists of two components:

1. **Frontend (Electron App)** - Displays an animated circle in the UI during recording
2. **Backend (Python Recorder)** - Draws a permanent circle on all captured screenshots

### Frontend Circle (UI Feedback)

- **Location**: `grandama/renderer/renderer.js` and `grandama/renderer/style.css`
- **Purpose**: Provides instant visual feedback to the user during recording
- **Behavior**: Appears and expands when user clicks, then fades out
- **Duration**: 0.6 seconds animation

### Backend Circle (Screenshot Overlay)

- **Location**: `recorder/capture.py`
- **Purpose**: Records the click location permanently on all screenshots
- **Output**: Visible in HTML, PDF, and video exports
- **Marker**: Green circle at exact click coordinates

---

## Customization Guide

### 1. Frontend Circle Colors

**File**: `grandama/renderer/style.css`

Find the `.click-circle` class:

```css
.click-circle {
  position: fixed;
  width: 40px;
  height: 40px;
  border: 3px solid #4CAF50;  /* Change this color */
  border-radius: 50%;
  pointer-events: none;
  z-index: 10000;
  animation: clickRipple 0.6s ease-out forwards;
}
```

**To change the border color:**
- Replace `#4CAF50` with any hex color code
- Examples:
  - `#FF5252` - Red
  - `#2196F3` - Blue
  - `#FFC107` - Amber
  - `#00BCD4` - Cyan

### 2. Frontend Circle Size

**File**: `grandama/renderer/style.css`

Modify the `width` and `height` properties in `.click-circle`:

```css
.click-circle {
  width: 40px;      /* Change starting size */
  height: 40px;     /* Should match width for circle */
  border: 3px solid #4CAF50;
}
```

**Examples:**
- Smaller (30px): `width: 30px; height: 30px;`
- Larger (60px): `width: 60px; height: 60px;`

### 3. Frontend Circle Border Width

**File**: `grandama/renderer/style.css`

Modify the `border` property:

```css
.click-circle {
  border: 3px solid #4CAF50;  /* 3px is the border width */
}
```

**Examples:**
- Thin (1px): `border: 1px solid #4CAF50;`
- Medium (2px): `border: 2px solid #4CAF50;`
- Thick (5px): `border: 5px solid #4CAF50;`

### 4. Frontend Circle Animation Speed

**File**: `grandama/renderer/style.css`

Modify the animation in `.click-circle`:

```css
.click-circle {
  animation: clickRipple 0.6s ease-out forwards;  /* 0.6s is duration */
}
```

**To change speed:**
- Faster (0.3s): `animation: clickRipple 0.3s ease-out forwards;`
- Slower (1s): `animation: clickRipple 1s ease-out forwards;`

### 5. Backend Circle Color (Screenshot Overlay)

**File**: `recorder/capture.py`

Find the `_take_screenshot()` method and locate this line:

```python
# Draw green circle (RGB: 76, 175, 80)
draw.ellipse([x1, y1, x2, y2], outline='#4CAF50', width=3)
```

**To change the color:**
- Replace `'#4CAF50'` with any hex color code
- Must match frontend color for consistency
- Examples:
  - `'#FF5252'` - Red
  - `'#2196F3'` - Blue
  - `'#FFC107'` - Amber

### 6. Backend Circle Size (Screenshot Overlay)

**File**: `recorder/capture.py`

Find the `_take_screenshot()` method and modify the radius:

```python
# Draw a green circle at the click location
circle_radius = 20  # Change this value
x1 = click_x - circle_radius
y1 = click_y - circle_radius
x2 = click_x + circle_radius
y2 = click_y + circle_radius
```

**Examples:**
- Small (10px): `circle_radius = 10`
- Medium (20px): `circle_radius = 20`
- Large (30px): `circle_radius = 30`

### 7. Backend Circle Border Width (Screenshot Overlay)

**File**: `recorder/capture.py`

Modify the `width` parameter in the `ellipse()` call:

```python
draw.ellipse([x1, y1, x2, y2], outline='#4CAF50', width=3)
                                                        ↑ Change this
```

**Examples:**
- Thin (1px): `width=1`
- Medium (3px): `width=3`
- Thick (5px): `width=5`

---

## Complete Customization Example

### Scenario: Make circles red and larger

**Step 1: Update Frontend Circle (UI)**

File: `grandama/renderer/style.css`

```css
.click-circle {
  position: fixed;
  width: 50px;                    /* ← Larger: 40px → 50px */
  height: 50px;                   /* ← Larger: 40px → 50px */
  border: 4px solid #FF5252;      /* ← Red, thicker: 3px → 4px */
  border-radius: 50%;
  pointer-events: none;
  z-index: 10000;
  animation: clickRipple 0.6s ease-out forwards;
}
```

**Step 2: Update Backend Circle (Screenshots)**

File: `recorder/capture.py`

Find the `_take_screenshot()` method and update:

```python
# Draw a red circle at the click location
circle_radius = 25              # ← Larger: 20 → 25
x1 = click_x - circle_radius
y1 = click_y - circle_radius
x2 = click_x + circle_radius
y2 = click_y + circle_radius

# Draw red circle
draw.ellipse([x1, y1, x2, y2], outline='#FF5252', width=4)
                                        ↑ Red      ↑ Thicker
```

---

## File Locations Reference

| Component | File | Location |
|-----------|------|----------|
| Frontend UI Circle | `style.css` | `grandama/renderer/style.css` |
| Frontend Click Handler | `renderer.js` | `grandama/renderer/renderer.js` |
| Backend Circle Drawer | `capture.py` | `recorder/capture.py` |
| Animation Definition | `style.css` | `grandama/renderer/style.css` |

---

## Code Snippets

### Frontend: Full Circle CSS

**File**: `grandama/renderer/style.css`

```css
.click-circle {
  position: fixed;
  width: 40px;
  height: 40px;
  border: 3px solid #4CAF50;
  border-radius: 50%;
  pointer-events: none;
  z-index: 10000;
  animation: clickRipple 0.6s ease-out forwards;
}

@keyframes clickRipple {
  0% {
    transform: translate(-50%, -50%) scale(0);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(1.5);
    opacity: 0;
  }
}
```

### Frontend: Click Handler JavaScript

**File**: `grandama/renderer/renderer.js`

```javascript
// Click circle effect during recording
document.addEventListener('click', (e) => {
  // Only show circle when recording
  if (recordingState.classList.contains('hidden')) return;
  
  const circle = document.createElement('div');
  circle.className = 'click-circle';
  circle.style.left = e.clientX + 'px';
  circle.style.top = e.clientY + 'px';
  
  document.body.appendChild(circle);
  
  // Remove circle after animation completes
  setTimeout(() => circle.remove(), 600);
});
```

### Backend: Screenshot Drawing Code

**File**: `recorder/capture.py`

```python
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
```

---

## Troubleshooting

### Circle not showing on screenshots
- **Check**: Make sure Pillow (`PIL`) is installed in requirements.txt
- **Solution**: Run `pip install -r recorder/requirements.txt`

### Circle showing in UI but not in exports
- **Check**: Backend circle code is properly drawing on screenshots
- **Solution**: Ensure `_take_screenshot()` is being called with `click_x` and `click_y` parameters

### Circle color doesn't match across platforms
- **Check**: Both frontend and backend colors match (same hex code)
- **Solution**: Update **both** `style.css` (frontend) and `capture.py` (backend) with same color

### Animation too fast/slow
- **Check**: Animation duration in CSS
- **Solution**: Modify the `0.6s` value in `clickRipple` animation

---

## Color Reference

| Color | Hex Code | RGB |
|-------|----------|-----|
| Green | #4CAF50 | 76, 175, 80 |
| Red | #FF5252 | 255, 82, 82 |
| Blue | #2196F3 | 33, 150, 243 |
| Amber | #FFC107 | 255, 193, 7 |
| Cyan | #00BCD4 | 0, 188, 212 |
| Purple | #9C27B0 | 156, 39, 176 |
| Orange | #FF9800 | 255, 152, 0 |

---

## Rebuilding After Changes

After customizing the circle feature, rebuild the application:

```bash
cd grandama
npm run build:mac    # For Mac
npm run build:win    # For Windows
npm run build:all    # For all platforms
```

Or for development/testing:

```bash
npm run dev          # Live reload with changes
```

---

## Performance Notes

- **Frontend circle**: Minimal performance impact (CSS animation only)
- **Backend circle**: Adds slight overhead to screenshot capture (PIL drawing)
- **Screenshot size**: Circle adds negligible data to screenshot file size
- **Memory**: Circles are cleaned up immediately after animation/screenshot

---

## Additional Resources

- [PIL/Pillow Documentation](https://pillow.readthedocs.io/)
- [CSS Animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations)
- [Hex Color Codes](https://www.color-hex.com/)
