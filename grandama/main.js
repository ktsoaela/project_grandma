const { app, BrowserWindow, ipcMain, shell } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const http = require('http');

let mainWindow = null;
let pythonProcess = null;
const RECORDER_PORT = 37482;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 520,
    height: 500,
    minWidth: 500,
    minHeight: 480,
    title: 'Steps Recorder',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
    ...(fs.existsSync(path.join(__dirname, 'assets', 'icon.png'))
      ? { icon: path.join(__dirname, 'assets', 'icon.png') } : {}),
  });

  mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));
  mainWindow.setMenuBarVisibility(false);
}

function getRecorderPath() {
  const isDev = !app.isPackaged;
  if (isDev) {
    return path.join(__dirname, '..', 'recorder', 'server.py');
  }
  return path.join(process.resourcesPath, 'recorder', 'server.py');
}

function getPythonExecutable() {
  return process.platform === 'win32' ? 'python' : 'python3';
}

function requestRecorder(method, pathname, body) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : null;
    const req = http.request({
      hostname: '127.0.0.1',
      port: RECORDER_PORT,
      path: pathname,
      method,
      headers: data ? { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) } : {},
    }, (res) => {
      let chunks = '';
      res.on('data', (c) => chunks += c);
      res.on('end', () => {
        try {
          resolve(res.statusCode === 200 ? JSON.parse(chunks || '{}') : { error: chunks || 'Request failed' });
        } catch {
          resolve({ data: chunks });
        }
      });
    });
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

function startPythonRecorder() {
  if (pythonProcess) return Promise.resolve();
  // If server is already running (e.g. via npm run dev), use it
  return requestRecorder('GET', '/health')
    .then(() => Promise.resolve())
    .catch(() => {
      return new Promise((resolve, reject) => {
        const scriptPath = getRecorderPath();
        pythonProcess = spawn(getPythonExecutable(), [scriptPath, String(RECORDER_PORT)], {
          cwd: path.dirname(scriptPath),
          stdio: ['ignore', 'pipe', 'pipe'],
        });
        let stderr = '';
        pythonProcess.stderr.on('data', (d) => { stderr += d.toString(); });
        pythonProcess.stdout.on('data', (d) => {
          if (d.toString().includes('listening')) resolve();
        });
        const t = setTimeout(() => {
          requestRecorder('GET', '/health').then(() => resolve()).catch(reject);
        }, 2000);
        pythonProcess.once('error', (err) => {
          clearTimeout(t);
          reject(err);
        });
        pythonProcess.once('exit', (code) => {
          clearTimeout(t);
          if (code !== 0 && code !== null) reject(new Error(stderr || `Exit ${code}`));
        });
      });
    });
}

function stopPythonRecorder() {
  if (pythonProcess) {
    pythonProcess.kill();
    pythonProcess = null;
  }
}

app.whenReady().then(() => {
  createWindow();

  ipcMain.handle('recorder:start', async (_, options) => {
    await startPythonRecorder();
    const opts = typeof options === 'object' ? options : { maxScreenshots: options };
    return requestRecorder('POST', '/start', {
      max_screenshots: opts.maxScreenshots ?? 25,
      record_video: opts.recordVideo === true,
      video_fps: opts.videoFps ?? 3,
    });
  });

  ipcMain.handle('recorder:stop', async (_, exportFormats) => {
    const result = await requestRecorder('POST', '/stop', {
      export_formats: exportFormats || ['html'],
    }).catch(() => ({}));
    return result;
  });

  ipcMain.handle('recorder:addComment', async (_, text) => {
    return requestRecorder('POST', '/comment', { text: text || '' });
  });

  ipcMain.handle('recorder:getState', async () => {
    return requestRecorder('GET', '/state').catch(() => ({ recording: false, step_count: 0 }));
  });

  ipcMain.handle('recorder:openReport', async (_, filePath) => {
    if (filePath) shell.openPath(filePath).catch(() => {});
  });
});

app.on('window-all-closed', () => {
  stopPythonRecorder();
  app.quit();
});

app.on('before-quit', () => {
  stopPythonRecorder();
});
