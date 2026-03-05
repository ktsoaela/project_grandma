const idleState = document.getElementById('idle-state');
const recordingState = document.getElementById('recording-state');
const saveDialog = document.getElementById('save-dialog');
const saveButtons = document.getElementById('save-buttons');
const btnStart = document.getElementById('btn-start');
const btnStop = document.getElementById('btn-stop');
const btnAddComment = document.getElementById('btn-add-comment');
const stepCountEl = document.getElementById('step-count');
const maxScreenshotsInput = document.getElementById('max-screenshots');
const recordVideoCheck = document.getElementById('record-video');
const videoFpsInput = document.getElementById('video-fps');
const exportHtmlCheck = document.getElementById('export-html');
const exportPdfCheck = document.getElementById('export-pdf');
const exportMdCheck = document.getElementById('export-md');
const captureTypedTextCheck = document.getElementById('capture-typed-text');
const privacyWarning = document.getElementById('privacy-warning');

let pollInterval = null;

// Privacy toggle: show/hide warning when "Show typed text" is toggled
captureTypedTextCheck.addEventListener('change', () => {
  privacyWarning.classList.toggle('visible', captureTypedTextCheck.checked);
});

function showState(idle, recording, showSave) {
  idleState.classList.toggle('hidden', !idle);
  recordingState.classList.toggle('hidden', !recording);
  saveDialog.classList.toggle('hidden', !showSave);
}

function updateStepCount(n) {
  stepCountEl.textContent = String(n);
}

async function pollState() {
  try {
    const state = await window.recorderAPI.getState();
    if (state.recording) updateStepCount(state.step_count || 0);
  } catch (_) { }
}

btnStart.addEventListener('click', async () => {
  const max = parseInt(maxScreenshotsInput.value, 10) || 25;
  const recordVideo = recordVideoCheck.checked;
  const videoFps = parseInt(videoFpsInput.value, 10) || 3;
  const captureTypedText = captureTypedTextCheck.checked;
  btnStart.disabled = true;
  try {
    const result = await window.recorderAPI.start({
      maxScreenshots: max,
      recordVideo,
      videoFps,
      captureTypedText,
    });
    if (result && result.error) {
      throw new Error(typeof result.error === 'string' ? result.error : result.error.message || 'Request failed');
    }
    if (result && result.video_error) {
      alert('Recording started, but video could not be recorded:\n\n' + result.video_error);
    }
    showState(false, true, false);
    updateStepCount(0);
    pollInterval = setInterval(pollState, 800);
  } catch (e) {
    const errorMsg = e?.message || e?.toString() || '';
    let alertMsg = 'Could not start recorder.';
    
    if (errorMsg.includes('ENOENT') || errorMsg.includes('not found')) {
      alertMsg += '\n\nMake sure the app was built correctly:\n1. Run: npm run build:recorder\n2. Run: npm run build:mac';
    } else if (errorMsg.includes('Python')) {
      alertMsg += '\n\nPython is not installed or recorder dependencies are missing:\nRun: pip install -r recorder/requirements.txt';
    } else {
      alertMsg += '\n\nError: ' + errorMsg;
    }
    
    alert(alertMsg);
    btnStart.disabled = false;
    return;
  }
  btnStart.disabled = false;
});

btnStop.addEventListener('click', async () => {
  if (pollInterval) {
    clearInterval(pollInterval);
    pollInterval = null;
  }
  const exportFormats = [];
  if (exportHtmlCheck.checked) exportFormats.push('html');
  if (exportPdfCheck.checked) exportFormats.push('pdf');
  if (exportMdCheck.checked) exportFormats.push('md');
  if (exportFormats.length === 0) exportFormats.push('html');
  btnStop.disabled = true;
  try {
    const result = await window.recorderAPI.stop(exportFormats);
    showState(false, false, true);
    const paths = result && result.paths ? result.paths : (result && result.path ? { html: result.path } : {});
    const videoErrorEl = document.getElementById('video-error-msg');
    if (paths.video_error) {
      videoErrorEl.textContent = 'Video: ' + paths.video_error;
      videoErrorEl.classList.remove('hidden');
    } else {
      videoErrorEl.textContent = '';
      videoErrorEl.classList.add('hidden');
    }
    saveButtons.innerHTML = '';
    const labels = { html: 'Open HTML', pdf: 'Open PDF', md: 'Open Markdown', video: 'Open video' };
    for (const [key, path] of Object.entries(paths)) {
      if (path && key !== 'video_error') {
        const btn = document.createElement('button');
        btn.className = 'btn btn-secondary save-btn';
        btn.setAttribute('data-format', key);
        btn.setAttribute('data-path', path);
        btn.textContent = labels[key] || key;
        btn.onclick = () => window.recorderAPI.openReport(path);
        saveButtons.appendChild(btn);
      }
    }
  } catch (_) { }
  btnStop.disabled = false;
});

btnAddComment.addEventListener('click', () => {
  const text = prompt('Add a comment (e.g. typed text or note):');
  if (text != null) window.recorderAPI.addComment(text);
});

document.querySelector('.btn-done').addEventListener('click', () => {
  showState(true, false, false);
});

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

(async () => {
  try {
    const state = await window.recorderAPI.getState();
    if (state.recording) {
      showState(false, true, false);
      updateStepCount(state.step_count || 0);
      pollInterval = setInterval(pollState, 800);
    } else {
      showState(true, false, false);
    }
  } catch (_) {
    showState(true, false, false);
  }
})();
