---
title: How to Record
description: Complete guide to recording steps with Project Grandma
---

## Recording a Guide

### Before You Start

Choose your settings:

| Setting | Purpose | Default |
|---------|---------|---------|
| **Screenshots** | How many recent captures to keep in memory | 25 |
| **Record Video** | Create MP4 video alongside guide | Off |
| **Export Format** | Output types (HTML, PDF, Markdown) | HTML |

Tip: Start with HTML only, add video later if needed.

## Recording Process

### 1. Click "Start Record"
The app waits for your actions. Everything is ready.

### 2. Perform Actions
Each action creates a step:

- **Mouse Click** → Screenshot taken + UI element detected
- **Keyboard Activity** → Logged but text not captured (privacy)
- **Movement** → Not recorded (only clicks matter)

### 3. Add Comments
Between steps, explain what's happening:

```
1. Click File → [screenshot]
   "Now we go to File menu"
2. Click Open → [screenshot]
   "Select Open to browse files"
```

**To add a comment:**
1. Click **"Add Comment"**
2. Type explanation in dialog
3. Click **"OK"**
4. Continue recording

### 4. Complex Steps
For multi-step actions:

**❌ Wrong way:**
```
Click Preferences
Close this dialog first
Then open Settings
```

**✅ Right way:**
- Click Preferences **[Comment: "Step 1"]**
- Close dialog **[Comment: "Step 2"]**
- Open Settings **[Comment: "Step 3"]**

Each action gets its own screenshot!

## What Gets Recorded

### ✅ Recorded
- Mouse clicks with coordinates
- Application windows and titles
- UI elements (buttons, fields, menus)
- Screenshot of each click
- Your custom comments

### ❌ Not Recorded
- Typed text (for privacy)
- Passwords (even if typed)
- System background processes
- File contents

## Tips for Better Guides

### 1. Go Slowly
- One action per step (don't rapid-click)
- Pause between actions
- Let screenshots load

### 2. Be Clear
- Use meaningful comments
- Explain why, not just what
- Point out important buttons

### 3. Test Your Guide
- Open the generated HTML
- Does it make sense to someone new?
- Is anything confusing?

### 4. Retake If Needed
- Recording a new guide is easy
- Polish your guide step by step
- Share only your best work

## Time Limits

- **Minimum**: 1 click (creates 1-step guide)
- **Maximum**: No limit! Record hour-long guides if needed
- **Optimal**: 5-15 steps per guide (easier to follow)

## Window Switching

You can switch between windows during recording:
1. Click on different windows
2. Each gets its own step
3. Comments explain the context

Example guide:
```
Step 1: Open Email App
Step 2: Click Inbox
Step 3: Select First Email
Step 4: Click Reply
Step 5: Open Word Document
Step 6: Paste in template
```

## Example Guide Structure

### Good Tutorial (7 steps)
1. Open Application
2. Click New
3. Fill in name field
4. Fill in email field
5. Choose options
6. Click Save
7. Confirm success

Each step is clear, focused, and logical.

### Common Mistakes

❌ **Don't:** Rapid multi-clicking
❌ **Don't:** Forget to add comments on confusing steps
❌ **Don't:** Record entire applications opening

✅ **Do:** Slow down your actions
✅ **Do:** Add comments liberally
✅ **Do:** Focus on the specific task

Next: [Export Your Guide](/guide/export/) to share with others!
