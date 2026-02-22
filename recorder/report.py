"""
Generate PSR-style HTML report matching Recording_*.mht layout and CSS.
"""
import sys
from datetime import datetime

if sys.platform == 'win32':
    try:
        from win_info import get_os_version
    except ImportError:
        get_os_version = lambda: ''
else:
    get_os_version = lambda: ''


def _escape(s):
    if s is None:
        return ''
    s = str(s)
    return (s
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))


def _fmt_time(dt):
    if dt is None:
        return ''
    if hasattr(dt, 'strftime'):
        return dt.strftime('%Y/%m/%d %H:%M:%S')
    return str(dt)


# PSR main.css equivalent (inline for single-file output)
PSR_CSS = '''
body {
    font-family: "Segoe UI", "Verdana", "Arial";
    background-color: #FFFFFF;
    margin: 20px;
    color: #575757;
    width: 760px;
}
a {
    color: rgb(19,112,171);
    font-size: 1em;
    font-weight: normal;
    text-decoration: none;
    margin-left: 0px;
    vertical-align: top;
}
a:link, a:visited {
    color: rgb(19,112,171);
    text-decoration: none;
    vertical-align: top;
}
a:hover {
    color: rgb(7,74,229);
    text-decoration: underline;
    vertical-align: top;
}
h1 {
    color: #4465A2;
    font-size: 1.1em;
    font-weight: normal;
    vertical-align: bottom;
    margin-top: 7px;
    margin-bottom: 4px;
}
p {
    font-size: 0.9em;
    font-weight: normal;
    margin-top: 1px;
    margin-bottom: 1px;
}
ul, ol {
    font-size: 0.9em;
    list-style-position: outside;
    margin-top: 1px;
    margin-bottom: 1px;
    padding-top: 1px;
    padding-bottom: 1px;
    line-height: 1.3em;
}
img.screenshot-thumb {
    border: 2px solid rgb(19,112,171);
    width: 756px;
    max-width: 100%;
    margin-top: 5px;
    cursor: pointer;
}
img.screenshot {
    border: 2px solid rgb(19,112,171);
    margin-top: 5px;
    max-width: 100%;
}
.align-right {
    text-align: right;
}
span.accessible-text {
    height: 1px;
    width: 1px;
    position: absolute;
    overflow: hidden;
    clip: rect(0,0,0,0);
}
'''


def build_html(steps, output_path, session_start=None, session_end=None):
    session_start = session_start or (steps[0]['time'] if steps else None)
    session_end = session_end or (steps[-1]['time'] if steps else None)
    session_range = ''
    if session_start and session_end:
        session_range = _fmt_time(session_start) + ' - ' + _fmt_time(session_end)
    os_version = get_os_version()
    recorded = len(steps)
    missed = 0
    errors = 0

    parts = [
        '''<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title id="m1">Recorded Steps</title>
<style type="text/css">
''',
        PSR_CSS,
        '''
</style>
<script type="text/javascript">
function zoomToggle(num) {
  var img = document.getElementById("ss-" + num);
  if (img.className == "screenshot") {
    img.className = "screenshot-thumb";
  } else {
    img.className = "screenshot";
  }
  return false;
}
</script>
</head>
<body>
<div id="ReportTop" tabindex="0">
    <h1 id="m2" title="Recorded Steps">Recorded Steps</h1>
    <hr aria-hidden="true" />
    <p id="m3">
        This file contains all the steps and information that was recorded to
        help you describe the recorded steps to others.
    </p>
    <p id="m4">
        Before sharing this file, you should verify the following:
    </p>
    <ul>
        <li id="m5">
            The steps below accurately describe the recording.
        </li>
        <li id="m6">
            There is no information below or on any screenshots that you do
            not want others to see.
        </li>
    </ul>
    <p id="m7">
        Passwords or any other text you typed were not recorded, except for function
        and shortcut keys that you used.
    </p>
    <p id="m8">
        You can do the following:
    </p>
    <ul>
        <li id="m9" title="Review the recorded steps">
            <a href="#Steps">Review the recorded steps</a>
        </li>
        <li id="m10" title="Review the additional details">
            <a href="#AdditionalDetails">Review the additional details</a>
        </li>
    </ul>
    <hr aria-hidden="true" />
</div>

<div id="Steps" tabindex="0">
    <h1 id="m12" title="Steps">Steps</h1>
    <hr aria-hidden="true" />
'''
    ]

    for i, step in enumerate(steps):
        desc = _escape(step.get('description', ''))
        time_str = _fmt_time(step.get('time'))
        img_b64 = step.get('image_base64')
        step_num = i + 1
        step_id = f'Step{step_num}'
        title_attr = f'Step{step_num} {time_str} {desc}'[:200]

        # Previous / Next line (align-right)
        parts.append(f'    <div id="{step_id}" title="{title_attr}" tabindex="0">\n')
        parts.append('        <p class="align-right">\n')
        if i > 0:
            parts.append(f'            <a title="Previous" href="#Step{i}">Previous</a>\n            ')
        if i < len(steps) - 1:
            parts.append(f'            <a title="Next" href="#Step{step_num + 1}">Next</a>\n')
        parts.append('        </p>\n\n')

        # Step description: <p><b>Step N: (date time)</b> description</p>
        parts.append(f'        <p id="m13"><b>Step {step_num}: ({time_str})</b> {desc}</p>\n')

        # Screenshot (inline base64; PSR uses external JPEG)
        if img_b64:
            parts.append(f'        <a onclick="zoomToggle({step_num})"><img id="ss-{step_num}" class="screenshot-thumb" alt="Step {step_num} screenshot." title="Click to enlarge/shrink screenshot." src="data:image/png;base64,{img_b64}"><span class="accessible-text">Step {step_num} screenshot.</span></a>\n')
        else:
            parts.append(f'        <p>Step {step_num} screenshot.</p>\n')
        parts.append('        <hr aria-hidden="true" />\n    </div>\n\n')

    # Additional Details (same structure as PSR)
    parts.append('''<div id="AdditionalDetails" tabindex="0">
    <h1 title="Additional Details" id="m14">Additional Details</h1>
    <p id="m15">
        The following section contains the additional details that were
        recorded.
    </p>
    <p id="m16">
        These details help accurately identify the programmes and UI you
        used in this recording.
    </p>
    <p id="m17">
        This section may contain text that is internal to programmes that
        only very advanced users or programmers may understand.
    </p>
    <p id="m18">
        Please review these details to ensure that they do not contain
        any information that you would not like others to see.
    </p>

    <br />
    <p style="font-family:verdana">
''')

    # Single paragraph with <br /> like PSR: Recording Session, Recorded Steps, OS, then per-step
    if session_range:
        parts.append(f'            Recording Session: {_escape(session_range)}<br /><br />')
    parts.append(f'Recorded Steps: {recorded}, Missed Steps: {missed}, Other Errors: {errors}<br /><br />')
    if os_version:
        parts.append(f'Operating System: {_escape(os_version)}<br /><br />')

    for i, step in enumerate(steps):
        desc = _escape(step.get('description', ''))
        program = step.get('program')
        ui_elements = step.get('ui_elements') or []
        parts.append(f'Step {i+1}: {desc}<br />')
        if program and isinstance(program, dict):
            name = program.get('name', '')
            ver = program.get('version', '')
            company = program.get('company', '')
            exe = program.get('exe', '')
            parts.append(f'Program: {_escape(name)}, {_escape(ver)}, {_escape(company)}, {_escape(exe)}, {_escape(exe)}<br />')
        if ui_elements:
            parts.append(f'UI Elements: {", ".join(_escape(u) for u in ui_elements)}<br />')
        parts.append('<br />')

    parts.append('''    </p>
    <hr id="m19" aria-hidden="true" />
    <a href="#ReportTop" title="Return to top of page"> Return to top of page... </a>
</div>
<div style="height:500px;">&nbsp;</div>
</body>
</html>
''')

    html = ''.join(parts)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return output_path


def build_pdf(steps, output_path, session_start=None, session_end=None):
    """Generate a PDF report from steps. Requires reportlab."""
    import base64
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
        from reportlab.lib.enums import TA_LEFT
    except ImportError:
        return None
    session_start = session_start or (steps[0]['time'] if steps else None)
    session_end = session_end or (steps[-1]['time'] if steps else None)
    session_range = (_fmt_time(session_start) + ' - ' + _fmt_time(session_end)) if (session_start and session_end) else ''
    os_version = get_os_version()

    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        rightMargin=inch, leftMargin=inch, topMargin=inch, bottomMargin=inch,
    )
    styles = getSampleStyleSheet()
    style_heading = ParagraphStyle('StepHeading', parent=styles['Heading2'], fontSize=10, spaceAfter=6)
    style_body = ParagraphStyle('StepBody', parent=styles['Normal'], fontSize=9, spaceAfter=12)
    story = []

    story.append(Paragraph('Recorded Steps', styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        'This file contains all the steps and information that was recorded.'
        ' Recording Session: %s. Recorded Steps: %d. OS: %s' % (session_range, len(steps), _escape(os_version)),
        style_body,
    ))
    story.append(Spacer(1, 16))

    for i, step in enumerate(steps):
        desc = _escape(step.get('description', ''))
        time_str = _fmt_time(step.get('time'))
        story.append(Paragraph('Step %d: (%s) %s' % (i + 1, time_str, desc), style_heading))
        img_b64 = step.get('image_base64')
        if img_b64:
            try:
                from io import BytesIO
                from PIL import Image as PILImage
                buf = base64.b64decode(img_b64)
                stream = BytesIO(buf)
                pil_img = PILImage.open(stream)
                w_px, h_px = pil_img.size
                stream.seek(0)
                max_w = 5.5 * inch
                w_in = w_px * (inch / 96)
                h_in = h_px * (inch / 96)
                if w_in > max_w:
                    ratio = max_w / w_in
                    w_in, h_in = max_w, h_in * ratio
                story.append(Image(stream, width=w_in, height=h_in))
            except Exception:
                pass
        story.append(Spacer(1, 14))

    try:
        doc.build(story)
        return output_path
    except Exception:
        return None


def build_md(steps, output_md_path, session_start=None, session_end=None):
    """Generate a Markdown report and an images folder. Returns path to .md file."""
    import base64
    import os
    session_start = session_start or (steps[0]['time'] if steps else None)
    session_end = session_end or (steps[-1]['time'] if steps else None)
    session_range = (_fmt_time(session_start) + ' - ' + _fmt_time(session_end)) if (session_start and session_end) else ''
    os_version = get_os_version()
    base_name = os.path.splitext(os.path.basename(output_md_path))[0]
    out_dir = os.path.dirname(output_md_path)
    images_dir = os.path.join(out_dir, base_name + '_images')
    os.makedirs(images_dir, exist_ok=True)

    lines = [
        '# Recorded Steps',
        '',
        'This file contains all the steps and information that was recorded.',
        '',
        '- **Recording Session:** %s' % session_range,
        '- **Recorded Steps:** %d' % len(steps),
        '- **Operating System:** %s' % os_version,
        '',
        '---',
        '',
    ]
    for i, step in enumerate(steps):
        desc = step.get('description', '')
        time_str = _fmt_time(step.get('time'))
        lines.append('## Step %d: (%s)' % (i + 1, time_str))
        lines.append('')
        lines.append(desc)
        lines.append('')
        img_b64 = step.get('image_base64')
        if img_b64:
            img_name = 'step_%d.png' % (i + 1)
            img_path = os.path.join(images_dir, img_name)
            try:
                with open(img_path, 'wb') as f:
                    f.write(base64.b64decode(img_b64))
                rel = os.path.join(base_name + '_images', img_name)
                lines.append('![Step %d](%s)' % (i + 1, rel.replace('\\', '/')))
                lines.append('')
            except Exception:
                pass
        lines.append('---')
        lines.append('')

    with open(output_md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return output_md_path
