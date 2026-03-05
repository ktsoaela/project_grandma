#!/bin/bash
# Build standalone Python executable for the recorder using PyInstaller
# This bundles Python with the server code so it doesn't require Python installed

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Installing PyInstaller..."
pip3 install pyinstaller > /dev/null 2>&1 || {
  echo "❌ Failed to install PyInstaller. Make sure Python 3 and pip are installed."
  exit 1
}

echo "Installing recorder requirements..."
pip3 install -r requirements.txt > /dev/null 2>&1 || {
  echo "❌ Failed to install recorder requirements."
  exit 1
}

echo "Building standalone executable..."
# Create a standalone, one-file executable
# --onefile: Single executable file
# --windowed: No console window (macOS)
# --collect-all: Collect all data files from dependencies
python3 -m PyInstaller \
  --onefile \
  --name recorder-server \
  --distpath ./dist/executable \
  --workpath ./build \
  --specpath ./specs \
  --collect-all flask \
  --collect-all imageio \
  server.py 2>&1 | grep -v "^WARNING:" || true

if [ -f "./dist/executable/recorder-server" ] || [ -f "./dist/executable/recorder-server.exe" ]; then
  echo "✓ Executable built successfully"
else
  echo "❌ Failed to build executable"
  exit 1
fi

