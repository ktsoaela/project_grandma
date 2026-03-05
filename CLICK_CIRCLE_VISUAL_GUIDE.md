# Click Circle - Visual Customization Guide

## Overview

This guide provides visual examples of different click circle configurations and how to achieve them.

---

## 1. Circle Size Variations

### Size Parameters

| Size | Width/Height (UI) | Radius (Backend) | Use Case |
|------|---|---|---|
| **Tiny** | 20px | 10 | Subtle, minimal distraction |
| **Small** | 30px | 15 | Compact displays |
| **Medium** | 40px | 20 | Default, balanced |
| **Large** | 50px | 25 | Large displays, visibility |
| **XL** | 60px | 30 | Presentations, training |

### How to Change Size

**Frontend (UI):**
```css
/* grandama/renderer/style.css */
.click-circle {
  width: 40px;    /* ← Change this (40, 50, 60, etc.) */
  height: 40px;   /* ← Must match width for perfect circle */
  border: 3px solid #4CAF50;
}
```

**Backend (Screenshots):**
```python
# recorder/capture.py
circle_radius = 20  # ← Change this (10, 15, 20, 25, 30, etc.)
```

**Rule**: Backend `circle_radius` ≈ Frontend `width ÷ 2`
- UI 40px = Backend 20 radius ✅
- UI 50px = Backend 25 radius ✅
- UI 60px = Backend 30 radius ✅

---

## 2. Border Width Variations

### Border Strength Comparison

| Thickness | Frontend | Backend | Visual Impact |
|-----------|----------|---------|---|
| **Thin** | 1px | width=1 | Subtle, elegant |
| **Normal** | 2px | width=2 | Good balance |
| **Medium** | 3px | width=3 | Default, clear |
| **Bold** | 4px | width=4 | Prominent |
| **Thick** | 5px | width=5 | Very visible |

### How to Change Border Width

**Frontend:**
```css
border: 3px solid #4CAF50;
        ↑ Change this number
```

**Backend:**
```python
draw.ellipse([x1, y1, x2, y2], outline='#4CAF50', width=3)
                                                         ↑
```

---

## 3. Color Customization

### Popular Color Schemes

#### Green (Default)
```css
border: 3px solid #4CAF50;
```
```python
outline='#4CAF50'
```
Best for: Professional, tree/growth metaphor

#### Red
```css
border: 3px solid #FF5252;
```
```python
outline='#FF5252'
```
Best for: Warning, attention, action required

#### Blue
```css
border: 3px solid #2196F3;
```
```python
outline='#2196F3'
```
Best for: Cool tone, professional, tech

#### Yellow/Amber
```css
border: 3px solid #FFC107;
```
```python
outline='#FFC107'
```
Best for: Highlighting, warning, caution

#### Purple
```css
border: 3px solid #9C27B0;
```
```python
outline='#9C27B0'
```
Best for: Creative, premium feel

#### Cyan
```css
border: 3px solid #00BCD4;
```
```python
outline='#00BCD4'
```
Best for: Modern, eye-catching

---

## 4. Animation Speed Variations

### Frontend Animation Duration

**File**: `grandama/renderer/style.css`

```css
.click-circle {
  animation: clickRipple 0.6s ease-out forwards;
                         ↑ Change this (in seconds)
}
```

| Duration | Speed | Feel |
|----------|-------|------|
| 0.3s | Very Fast | Snappy, responsive |
| 0.5s | Fast | Quick, reactive |
| **0.6s** | **Normal** | **Default, balanced** |
| 0.8s | Slow | Smooth, gentle |
| 1.0s | Very Slow | Dramatic, flowing |

**Examples:**
```css
/* Snappy animation */
animation: clickRipple 0.3s ease-out forwards;

/* Smooth and slow */
animation: clickRipple 1s ease-out forwards;
```

---

## 5. Complete Configuration Examples

### Example 1: Minimal Profile
**Use Case**: Desktop applications, subtle feedback

**Frontend** (`style.css`):
```css
.click-circle {
  width: 30px;
  height: 30px;
  border: 1px solid #4CAF50;
  border-radius: 50%;
  pointer-events: none;
  z-index: 10000;
  animation: clickRipple 0.5s ease-out forwards;
}
```

**Backend** (`capture.py`):
```python
circle_radius = 15
draw.ellipse([x1, y1, x2, y2], outline='#4CAF50', width=1)
```

---

### Example 2: Bold Profile
**Use Case**: Presentations, training videos, large screens

**Frontend** (`style.css`):
```css
.click-circle {
  width: 60px;
  height: 60px;
  border: 5px solid #FF5252;
  border-radius: 50%;
  pointer-events: none;
  z-index: 10000;
  animation: clickRipple 0.8s ease-out forwards;
}
```

**Backend** (`capture.py`):
```python
circle_radius = 30
draw.ellipse([x1, y1, x2, y2], outline='#FF5252', width=5)
```

---

### Example 3: Blue Tech Profile
**Use Case**: Technical documentation, software tutorials

**Frontend** (`style.css`):
```css
.click-circle {
  width: 40px;
  height: 40px;
  border: 2px solid #2196F3;
  border-radius: 50%;
  pointer-events: none;
  z-index: 10000;
  animation: clickRipple 0.6s ease-out forwards;
}
```

**Backend** (`capture.py`):
```python
circle_radius = 20
draw.ellipse([x1, y1, x2, y2], outline='#2196F3', width=2)
```

---

### Example 4: Warning Profile
**Use Case**: Security, compliance, critical actions

**Frontend** (`style.css`):
```css
.click-circle {
  width: 45px;
  height: 45px;
  border: 4px solid #9C27B0;
  border-radius: 50%;
  pointer-events: none;
  z-index: 10000;
  animation: clickRipple 0.7s ease-out forwards;
}
```

**Backend** (`capture.py`):
```python
circle_radius = 22
draw.ellipse([x1, y1, x2, y2], outline='#9C27B0', width=4)
```

---

## 6. Responsive Design Considerations

### For Mobile/Tablet
- Use **larger circles** (50-60px) for touch targets
- Use **thicker borders** (4-5px) for visibility on small screens
- Use **slower animation** (0.8-1.0s) for clarity

```css
width: 55px;
height: 55px;
border: 4px solid #2196F3;
animation: clickRipple 0.9s ease-out forwards;
```

### For Desktop
- Use **medium circles** (40-45px) for balance
- Use **normal borders** (2-3px) for precision
- Use **normal animation** (0.5-0.7s) for responsiveness

```css
width: 42px;
height: 42px;
border: 3px solid #4CAF50;
animation: clickRipple 0.6s ease-out forwards;
```

### For Large Displays / Presentations
- Use **large circles** (50-70px) for visibility
- Use **bold borders** (4-5px) for clarity
- Use **slow animation** (0.8-1.2s) for drama

```css
width: 65px;
height: 65px;
border: 5px solid #FF5252;
animation: clickRipple 1s ease-out forwards;
```

---

## 7. Matching Frontend & Backend

**IMPORTANT**: Frontend and Backend must match for consistency!

### Verification Checklist

- [ ] Frontend `width` and Backend `radius` match proportionally
- [ ] Frontend `border` color matches Backend `outline` color
- [ ] Frontend `border` width matches Backend `width` parameter
- [ ] Both files saved before rebuild

### Automatic Sync Chart

| Component | Frontend (style.css) | Backend (capture.py) |
|-----------|---|---|
| Color | `#4CAF50` in `border` | `'#4CAF50'` in `outline` |
| Size (width) | `40px` | `20` (half of width) |
| Border | `3px` in `border` | `width=3` |

---

## 8. Troubleshooting Customization

### Issue: Circle looks different in exports than on screen

**Solution**: Ensure backend size calculation is correct
```python
# Frontend: width = 40px
# Backend: radius should be 20 (not 10 or 30)
circle_radius = 20  ✅
```

### Issue: Colors don't match between UI and screenshots

**Solution**: Update BOTH locations with same hex code
1. `style.css`: `border: 3px solid #FF5252;`
2. `capture.py`: `outline='#FF5252'`

### Issue: Animation too slow/fast

**Solution**: Adjust only in `style.css`
```css
animation: clickRipple 0.6s ease-out forwards;
                       ↑ Try 0.3s to 1.2s
```

### Issue: Circle too thin/thick

**Solution**: Adjust BOTH locations equally
- `style.css`: `border: 3px`
- `capture.py`: `width=3`

---

## 9. Color Psychology

Choose colors based on the message you want to convey:

- **🟢 Green**: Trust, success, growth, harmony
- **🔴 Red**: Danger, error, warning, attention
- **🔵 Blue**: Professional, calm, tech, trustworthy
- **🟡 Amber**: Caution, warning, highlight
- **🟣 Purple**: Creative, premium, mysterious
- **🩵 Cyan**: Modern, fresh, energetic
- **⚫ Black**: Bold, professional, neutral
- **⚪ White**: Clean, minimal, elegant (use on dark screenshots)

---

## 10. Quick Copy-Paste Customizations

### Blue & Bold
```css
/* style.css */
border: 4px solid #2196F3;
width: 48px;
height: 48px;
animation: clickRipple 0.7s ease-out forwards;
```

```python
# capture.py
circle_radius = 24
draw.ellipse([x1, y1, x2, y2], outline='#2196F3', width=4)
```

### Red & Thick
```css
/* style.css */
border: 5px solid #FF5252;
width: 50px;
height: 50px;
animation: clickRipple 0.8s ease-out forwards;
```

```python
# capture.py
circle_radius = 25
draw.ellipse([x1, y1, x2, y2], outline='#FF5252', width=5)
```

### Purple & Elegant
```css
/* style.css */
border: 2px solid #9C27B0;
width: 38px;
height: 38px;
animation: clickRipple 0.5s ease-out forwards;
```

```python
# capture.py
circle_radius = 19
draw.ellipse([x1, y1, x2, y2], outline='#9C27B0', width=2)
```

---

## Summary

| Parameter | Where to Change | Default | Range | Impact |
|-----------|---|---|---|---|
| **Color** | Both files | #4CAF50 (Green) | Any hex | Visual style |
| **Size (UI)** | style.css | 40px | 20-70px | Visibility |
| **Border Width** | Both files | 3px | 1-5px | Prominence |
| **Animation Speed** | style.css only | 0.6s | 0.3-1.2s | Feedback feel |

For most use cases, you only need to change **color** and **size**!
