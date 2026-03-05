# Click Circle - Quick Reference Guide

## TL;DR - Quick Changes

### Change Circle Color (All Occurrences)

1. **Frontend UI**: `grandama/renderer/style.css` - Line with `#4CAF50`
   ```css
   border: 3px solid #FF5252;  /* Change #4CAF50 to your color */
   ```

2. **Backend Screenshots**: `recorder/capture.py` - Line with `#4CAF50`
   ```python
   draw.ellipse([x1, y1, x2, y2], outline='#FF5252', width=3)  /* Change #4CAF50 to your color */
   ```

---

### Change Circle Size

**Frontend**: `grandama/renderer/style.css`
```css
.click-circle {
  width: 50px;    /* Default: 40px */
  height: 50px;   /* Default: 40px */
}
```

**Backend**: `recorder/capture.py`
```python
circle_radius = 25  # Default: 20
```

---

### Change Circle Border Width

**Frontend**: `grandama/renderer/style.css`
```css
border: 5px solid #4CAF50;  /* Default: 3px */
```

**Backend**: `recorder/capture.py`
```python
draw.ellipse([x1, y1, x2, y2], outline='#4CAF50', width=5)  /* Default: width=3 */
```

---

### Change Animation Speed

**Frontend**: `grandama/renderer/style.css`
```css
animation: clickRipple 1s ease-out forwards;  /* Default: 0.6s */
```

---

## Popular Customizations

### Blue Circle (Smaller)
```css
/* style.css */
border: 2px solid #2196F3;
width: 30px;
height: 30px;
```
```python
# capture.py
circle_radius = 15
draw.ellipse([x1, y1, x2, y2], outline='#2196F3', width=2)
```

### Red Circle (Larger & Thicker)
```css
/* style.css */
border: 4px solid #FF5252;
width: 50px;
height: 50px;
```
```python
# capture.py
circle_radius = 25
draw.ellipse([x1, y1, x2, y2], outline='#FF5252', width=4)
```

### Subtle Yellow Circle
```css
/* style.css */
border: 1px solid #FFC107;
width: 35px;
height: 35px;
```
```python
# capture.py
circle_radius = 15
draw.ellipse([x1, y1, x2, y2], outline='#FFC107', width=1)
```

---

## File Lookup Table

| What to Change | File | Search For |
|---|---|---|
| UI Circle Color | `grandama/renderer/style.css` | `.click-circle` class, `#4CAF50` |
| UI Circle Size | `grandama/renderer/style.css` | `.click-circle` class, `width:`, `height:` |
| UI Border Width | `grandama/renderer/style.css` | `.click-circle` class, `border:` |
| UI Animation Speed | `grandama/renderer/style.css` | `clickRipple`, `0.6s` |
| Screenshot Circle Color | `recorder/capture.py` | `draw.ellipse`, `#4CAF50` |
| Screenshot Circle Size | `recorder/capture.py` | `circle_radius = 20` |
| Screenshot Border Width | `recorder/capture.py` | `draw.ellipse`, `width=3` |

---

## Hex Color Codes

```
🟢 Green:  #4CAF50  (Current)
🔴 Red:    #FF5252
🔵 Blue:   #2196F3
🟡 Yellow: #FFC107
🟠 Orange: #FF9800
🟣 Purple: #9C27B0
🩵 Cyan:   #00BCD4
```

---

## Rebuild Command

After making changes:
```bash
cd grandama
npm run build:mac    # Mac
npm run dev          # Development/Testing
```

---

## Example: Change to Purple with Custom Size

**Step 1**: Edit `grandama/renderer/style.css`
```css
.click-circle {
  width: 45px;                     /* increased from 40 */
  height: 45px;                    /* increased from 40 */
  border: 3px solid #9C27B0;       /* changed to purple */
}
```

**Step 2**: Edit `recorder/capture.py`
```python
circle_radius = 22                 /* increased from 20 */
draw.ellipse([x1, y1, x2, y2], outline='#9C27B0', width=3)  /* changed to purple */
```

Done! Both UI and screenshots will now show purple circles.

---

## Revert to Defaults

If you want to restore the original green circles:

**style.css:**
```css
border: 3px solid #4CAF50;
width: 40px;
height: 40px;
animation: clickRipple 0.6s ease-out forwards;
```

**capture.py:**
```python
circle_radius = 20
draw.ellipse([x1, y1, x2, y2], outline='#4CAF50', width=3)
```
