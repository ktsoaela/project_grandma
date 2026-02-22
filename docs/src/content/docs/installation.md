---
title: Installation
description: Install Project Grandma on Windows or macOS
---

import { Tabs, TabItem } from '@astrojs/starlight/components';

## System Requirements

<Tabs>
<TabItem label="Windows">
    <ul>
        <li><strong>OS</strong>: Windows 10 or later</li>
        <li><strong>Processor</strong>: Any modern processor</li>
        <li><strong>Memory</strong>: 4GB RAM (8GB recommended)</li>
        <li><strong>Disk Space</strong>: 500MB for installation</li>
        <li><strong>Network</strong>: Internet connection (optional, for updates)</li>
    </ul>
</TabItem>
<TabItem label="macOS">
    <ul>
        <li><strong>OS</strong>: macOS 10.12 or later</li>
        <li><strong>Processor</strong>: Intel or Apple Silicon</li>
        <li><strong>Memory</strong>: 4GB RAM (8GB recommended)</li>
        <li><strong>Disk Space</strong>: 500MB for installation</li>
        <li><strong>Network</strong>: Internet connection (optional, for updates)</li>
    </ul>
</TabItem>
</Tabs>

## Installation Methods

<Tabs>
<TabItem label="Windows Installer">
### Step 1: Download
Go to [Releases](https://github.com/ktsoaela/project_grandma/releases) and download the latest `Project-Grandma-X.X.X.exe`

### Step 2: Run Installer
Double-click the downloaded `.exe` file

### Step 3: Follow Prompts
- Accept the license
- Choose installation directory
- Click "Install"

### Step 4: Launch
- Click "Finish" and Project Grandma will launch
- Or find it in your Start Menu

**Desktop Shortcut**: Created automatically
</TabItem>
<TabItem label="Windows Portable">
### Portable (No Installation Required)

1. Download `Project Grandma.exe` from [Releases](https://github.com/ktsoaela/project_grandma/releases)
2. Save anywhere on your computer
3. Double-click to run
4. No installation needed!

**Perfect for**: USB drives, quick testing, no admin rights
</TabItem>
<TabItem label="macOS">
### Step 1: Download
Go to [Releases](https://github.com/ktsoaela/project_grandma/releases) and download the latest `Project-Grandma-X.X.X.dmg`

### Step 2: Open DMG
Double-click the downloaded `.dmg` file

### Step 3: Drag to Applications
Drag "Project Grandma" to the Applications folder

### Step 4: Launch
Open Applications folder and double-click "Project Grandma"

**First Time?**: macOS may ask for permission - click "Open"

### For M1/M2 Macs
The universal binary works on both Intel and Apple Silicon Macs
</TabItem>
</Tabs>

## Development Installation

To build from source:

```bash
# Install Node.js
# https://nodejs.org/

# Install Python 3
# https://www.python.org/

# Clone the repository
git clone https://github.com/ktsoaela/project_grandma.git
cd project_grandma

# Install Electron dependencies
cd grandama
npm install

# Install Python dependencies
cd ../recorder
pip install -r requirements.txt

# Run in development mode
npm run dev
```

## Troubleshooting Installation

### "App can't be opened" (macOS)
1. Right-click Project Grandma
2. Click "Open"
3. Click "Open" on the security prompt

### "SmartScreen warning" (Windows)
- This is normal for unsigned apps
- Click "More info" → "Run anyway"

### "Admin rights required"
- Use portable version instead of installer
- Or run the installer as Administrator

Can't install? See [Troubleshooting Guide](/help/troubleshooting/) for more help.
