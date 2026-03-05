# Building Project Grandma - Mac Binary Setup

## Problem
The built Mac application requires Python to be installed on users' machines. This guide bundles Python with the app using PyInstaller, so users don't need Python installed.

## Solution: Automatic Standalone Executable Build

The build process is now **automated**. Just run:

```bash
cd grandama
npm run build:mac
```

This will:
1. Automatically build the standalone Python executable
2. Bundle it with the app
3. Create the Mac DMG installer

Users won't need Python installed to run the app.

## What Changed

- `npm run build:mac` now automatically runs `npm run build:recorder` first
- `npm run build:win` and `npm run build:all` also build the recorder executable automatically
- Error messages show helpful instructions if something goes wrong

## Development Setup (Optional)

If you want to test the Python server manually:

```bash
# Install dependencies
cd recorder
pip3 install -r requirements.txt

# Run the server
python3 server.py 37482

# In another terminal
cd grandama
npm run start:electron
```

Or use concurrently:
```bash
cd grandama
npm run dev
```

## Troubleshooting

**"Could not start recorder" after building:**
- This means the executable wasn't built. Run again:
  ```bash
  npm run build:mac
  ```

**"ENOENT" or "not found" error:**
- PyInstaller failed to build. Check that Python 3 and pip are installed:
  ```bash
  python3 --version
  pip3 --version
  ```

**Python fallback still required:**
- The app will fall back to using the system Python if the executable can't be found
- For production builds, ensure `npm run build:mac` completes successfully

