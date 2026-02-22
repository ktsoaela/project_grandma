/**
 * Start the Python recorder server (for use with concurrently).
 * Keeps running until Ctrl+C. Uses RECORDER_PORT from main.js (37482).
 */
const path = require('path');
const { spawn } = require('child_process');

const RECORDER_PORT = 37482;
const recorderDir = path.join(__dirname, '..', '..', 'recorder');
const serverPath = path.join(recorderDir, 'server.py');
const python = process.platform === 'win32' ? 'python' : 'python3';

const child = spawn(python, [serverPath, String(RECORDER_PORT)], {
  cwd: recorderDir,
  stdio: 'inherit',
});

child.on('error', (err) => {
  console.error('Failed to start Python recorder:', err.message);
  process.exit(1);
});

child.on('exit', (code, signal) => {
  if (code !== 0 && code !== null) process.exit(code || 1);
  if (signal) process.exit(1);
});
