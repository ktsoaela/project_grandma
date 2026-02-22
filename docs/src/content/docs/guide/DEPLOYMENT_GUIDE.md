# GitHub Actions & Documentation Setup Guide

## ✅ What We've Created

### 1. GitHub Actions Workflows
- **build.yml**: Builds the app for Windows & macOS
- **docs.yml**: Deploys documentation to GitHub Pages
- **release-template.md**: Template for release notes

### 2. Starlight Documentation
- Complete documentation site with 15+ pages
- Beautiful, searchable, mobile-friendly
- Auto-deploys to GitHub Pages

### 3. Project Structure
```
.github/
├── workflows/
│   ├── build.yml         ← Auto-build on tag
│   ├── docs.yml          ← Auto-deploy docs
│   └── release-template.md
docs/
├── astro.config.mjs      ← Starlight config
├── package.json
├── src/
│   ├── content/docs/     ← Documentation pages
│   ├── layouts/
│   └── assets/
```

## 🚀 Step-by-Step Deployment

### Step 1: Push All Files to GitHub

```bash
cd c:\Work\UTILITY\screen_recorder

# Add all new files
git add .

# Commit
git commit -m "Add GitHub Actions and Starlight documentation"

# Push
git push origin main
```

### Step 2: Enable GitHub Pages

1. Go to your repo settings
2. Click **"Pages"** (left sidebar)
3. Under "Build and deployment":
   - Source: **Deploy from a branch**
   - Branch: **gh-pages**
   - Folder: **/root**
4. Click **"Save"**

### Step 3: Install Docs Dependencies

First time only:

```bash
cd c:\Work\UTILITY\screen_recorder\docs
npm install

# This installs:
# - Astro
# - Starlight
# - Dependencies
```

### Step 4: Build Documentation Locally (Optional Testing)

```bash
cd docs

# Development server
npm run dev
# Visit http://localhost:3000

# Build for production
npm run build
# Output in docs/dist
```

### Step 5: Create Your First Release

```bash
cd c:\Work\UTILITY\screen_recorder

# Make sure everything is built
cd grandama
npm run build:win  # Run PowerShell as Admin

# Back to root
cd ..

# Create git tag
git tag -a v1.0.0 -m "Initial Release"

# Push to GitHub
git push origin main
git push origin v1.0.0
```

When you push the tag, GitHub Actions automatically:
1. ✅ Builds Windows executable
2. ✅ Builds macOS app
3. ✅ Creates GitHub Release
4. ✅ Uploads files to release
5. ✅ Deploys docs to GitHub Pages

### Step 6: Verify Everything Works

Check:
1. **GitHub Actions**: https://github.com/ktsoaela/project_grandma/actions
   - Should show successful build workflows
2. **Releases**: https://github.com/ktsoaela/project_grandma/releases
   - Should show your v1.0.0 with executable files
3. **Documentation**: https://ktsoaela.github.io/project_grandma/
   - Should display your Starlight docs

## 📝 Customizing Documentation

### Add New Page

Create file in `docs/src/content/docs/`:

```markdown
---
title: Page Title
description: Page description
---

# Page Content

Your markdown here...
```

Then add to `astro.config.mjs` sidebar:

```javascript
{
  label: 'Category Name',
  items: [
    { label: 'My Page', slug: 'my-page' },
  ],
}
```

### Update Sidebar

Edit `docs/astro.config.mjs`:

```javascript
sidebar: [
  {
    label: 'Getting Started',
    items: [
      { label: 'Welcome', slug: 'welcome' },
      { label: 'Installation', slug: 'installation' },
    ],
  },
]
```

### Customize Logo

Replace `docs/src/assets/logo.png` with your logo.

## 📋 Workflow: Releasing Updates

### For Bug Fixes & Minor Updates

```bash
# 1. Make changes
# ... edit files ...

# 2. Commit
git add .
git commit -m "Fix: issue description"

# 3. Bump version in grandama/package.json
# Change: "version": "1.0.0" → "1.0.1"

# 4. Build (Windows - must be admin terminal)
cd grandama
npm run build:win

# 5. Tag and push
cd ..
git add .
git commit -m "v1.0.1"
git tag -a v1.0.1 -m "Bug fixes"
git push origin main
git push origin v1.0.1

# ✅ Automatic:
# - Builds executables
# - Creates release
# - Deploys docs
```

### For Documentation Updates Only

```bash
# Edit docs in docs/src/content/docs/

git add docs/
git commit -m "Docs: update installation guide"
git push origin main

# ✅ Automatic: Deploys to GitHub Pages in 2-3 minutes
```

## 🔐 GitHub Secrets (Optional Advanced)

If you want to add auto-signing or deploy to other services, add secrets:

1. Go to repo **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**

Common secrets:
- `SIGNING_CERT_URL`: For code signing
- `YOUTUBE_API_KEY`: For auto-uploading videos
- `NPM_TOKEN`: For npm publishing

## ❓ Troubleshooting

### Build fails on Actions

**Check:**
1. Log into https://github.com/ktsoaela/project_grandma/actions
2. Click failed workflow
3. Click job → see error output
4. Fix issue locally first with `npm run build:win`

### Docs won't deploy

**Check:**
1. Pages settings (Settings → Pages)
2. gh-pages branch exists
3. Actions tab shows successful deployment

### Release not created

**Check:**
1. Tag pushed correctly: `git push origin v1.0.0`
2. No spaces in tag name
3. GitHub Actions completed successfully

## 📚 Documentation File Structure

```
docs/
├── src/
│   ├── content/docs/
│   │   ├── welcome.md           ← Home page
│   │   ├── installation.md
│   │   ├── quick-start.md
│   │   ├── guide/
│   │   │   ├── recording.md
│   │   │   ├── comments.md
│   │   │   └── export.md
│   │   ├── features/
│   │   │   ├── windows.md
│   │   │   ├── macos.md
│   │   │   └── video.md
│   │   ├── help/
│   │   │   ├── faq.md
│   │   │   ├── troubleshooting.md
│   │   │   └── issues.md
│   │   └── dev/
│   │       ├── build.md
│   │       ├── contributing.md
│   │       └── architecture.md
│   ├── assets/
│   │   └── logo.png        ← Your logo here
│   └── layouts/
│       └── Layout.astro
├── astro.config.mjs        ← Sidebar & theme
└── package.json
```

## 🎯 Next Steps

1. ✅ Push all files to GitHub
2. ✅ Enable GitHub Pages
3. ✅ Create v1.0.0 release/tag
4. ✅ Verify docs appear at GitHub Pages URL
5. ✅ Share documentation link with users

## 📖 Your Documentation Will be at:

- **Main Docs**: `https://ktsoaela.github.io/project_grandma/`
- **Installation**: `https://ktsoaela.github.io/project_grandma/installation/`
- **FAQ**: `https://ktsoaela.github.io/project_grandma/help/faq/`
- **All pages indexed and searchable**

## 🎉 What Happens Automatically

Every time you:
- **Push a tag** → Builds & creates release ✅
- **Update docs** → Deploys to GitHub Pages ✅
- **Open PR** → Runs build checks ✅
- **Merge to main** → Builds & updates ✅

You now have a complete CI/CD pipeline! 🚀
