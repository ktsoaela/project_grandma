"""
Flask server for the Steps Recorder backend.
Electron connects here to start/stop recording and add comments.
Run: python server.py [port]
"""
import sys
import os
import tempfile
from datetime import datetime

from flask import Flask, request, jsonify

# Add this directory so imports work when run from Electron resources
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from capture import StepCapture
from report import build_html, build_pdf, build_md
from video_capture import start_video_recording, stop_video_recording

app = Flask(__name__)
capture = None
step_count_callback = None
_video_path = None  # path where video will be saved (set when video recording starts)


def _step_callback(count):
    global step_count_callback
    if step_count_callback:
        step_count_callback(count)


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'ok': True})


@app.route('/state', methods=['GET'])
def state():
    global capture
    recording = capture is not None and capture._running
    count = capture.get_step_count() if capture else 0
    return jsonify({'recording': recording, 'step_count': count})


@app.route('/start', methods=['POST'])
def start():
    global capture, _video_path
    if capture and capture._running:
        return jsonify({'recording': True, 'step_count': capture.get_step_count()})
    data = request.get_json() or {}
    max_screenshots = data.get('max_screenshots', 25)
    record_video = data.get('record_video', False)
    video_fps = max(1, min(10, data.get('video_fps', 3)))
    capture_typed_text = data.get('capture_typed_text', False)
    capture = StepCapture(on_step=_step_callback, max_screenshots=max_screenshots,
                          capture_typed_text=capture_typed_text)
    capture.start()
    _video_path = None
    if record_video:
        _video_path = start_video_recording(fps=video_fps)
    return jsonify({'recording': True, 'step_count': 0})


@app.route('/stop', methods=['POST'])
def stop():
    global capture, _video_path
    paths = {'html': None, 'pdf': None, 'md': None, 'video': None}
    if capture:
        capture.stop()
        steps = capture.get_steps()
        session_start = capture.get_session_start() if capture else None
        session_end = datetime.now()
        base_name = f"StepsRecorder_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        out_dir = tempfile.gettempdir()
        data = request.get_json() or {}
        export_formats = data.get('export_formats') or ['html']

        if steps:
            if 'html' in export_formats:
                path_html = os.path.join(out_dir, base_name + '.html')
                build_html(steps, path_html, session_start=session_start, session_end=session_end)
                paths['html'] = path_html
            if 'pdf' in export_formats:
                path_pdf = os.path.join(out_dir, base_name + '.pdf')
                if build_pdf(steps, path_pdf, session_start=session_start, session_end=session_end):
                    paths['pdf'] = path_pdf
            if 'md' in export_formats:
                path_md = os.path.join(out_dir, base_name + '.md')
                build_md(steps, path_md, session_start=session_start, session_end=session_end)
                paths['md'] = path_md
        if _video_path:
            video_path = stop_video_recording()
            if video_path and os.path.isfile(video_path):
                paths['video'] = video_path
        _video_path = None
        capture = None
    return jsonify({'recording': False, 'path': paths.get('html'), 'paths': paths})


@app.route('/comment', methods=['POST'])
def comment():
    global capture
    if not capture or not capture._running:
        return jsonify({'error': 'Not recording'}), 400
    data = request.get_json() or {}
    text = data.get('text', '')
    capture.add_comment(text)
    return jsonify({'step_count': capture.get_step_count()})


def main():
    import threading
    import time
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 37482

    def run():
        app.run(host='127.0.0.1', port=port, threaded=True, use_reloader=False)

    t = threading.Thread(target=run, daemon=True)
    t.start()
    time.sleep(0.6)
    print('listening', flush=True)
    while True:
        time.sleep(3600)


if __name__ == '__main__':
    main()
