"""Builds every SVG in assets/ for the profile README.

    python3 scripts/generate.py      (needs Pillow)

All copy lives in the CONTENT section below. Edit it, re-run, commit the assets.
GitHub renders these through <img>, so everything is self-contained: no JS, no external
fonts or images, animations are SMIL, and links live on the <a> wrapping each image.
"""
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

from portrait import portrait

ASSETS = Path(__file__).resolve().parent.parent / 'assets'

# ─────────────────────────────── CONTENT ───────────────────────────────

USER, HOST = 'ali', 'north-vancouver'

NEOFETCH = [
    ('OS', 'Computer Engineering @ SFU'),
    ('Uptime', '4th year · grad May 2027'),
    ('Host', 'North Vancouver, BC'),
    ('Kernel', 'prev. SWE co-op @ TELUS'),
    ('Firmware', 'C on ARM · SFU Robot Soccer'),
    ('Shell', 'Python · TypeScript · C++ · Rust'),
    ('Frameworks', 'React Native · Next.js · FastAPI · OpenCV'),
    ('Packages', '14 public repos'),
    ('Now', 'shipping a personal RAG chatbot'),
    ('Fuel', 'coffee, refilled per commit'),
    ('Offline', 'mountain biking · skiing'),
    ('Web', 'ali-shamsi-dev.netlify.app'),
]

PROJECTS = [
    dict(slug='paddlepal', name='PaddlePal', badge='capstone · A',
         desc='Smart pickleball paddle. RP2040 firmware reads impact sensors and streams '
              'over BLE to a native iOS app for swing and hit-zone analytics.',
         stack=['react-native', 'expo', 'ble', 'firebase', 'c++']),
    dict(slug='steadyscript', name='SteadyScript', badge='★ nwHacks 2026 ×2',
         desc='Tremor-therapy biofeedback. OpenCV tracks a pen over webcam, a custom '
              'jitter algorithm scores steadiness, Arduino LEDs react live.',
         stack=['react', 'fastapi', 'opencv', 'arduino']),
    dict(slug='portfolio-v3', name='Portfolio + RAG', badge='● live',
         desc='My site, plus a chatbot that answers questions about my work: Cloudflare '
              'Worker API, Qdrant vector search, Gemini embeddings and LLM fallback chain.',
         stack=['react', 'vite', 'cf-workers', 'qdrant', 'gemini']),
    dict(slug='phishnet', name='PhishNet.AI', badge='AI/ML hackathon',
         desc='Paste an email, get a phishing verdict. SVC + TF-IDF classifier behind a '
              'Flask API, plus a Learning Mode that trains you to spot phish yourself.',
         stack=['scikit-learn', 'flask', 'nltk', 'pandas', 'js']),
]

STACK = [
    ('languages', ['python', 'typescript', 'javascript', 'c', 'c++', 'rust', 'java', 'sql', 'cuda']),
    ('ai-ml', ['pytorch', 'tensorflow', 'langchain', 'hugging-face', 'opencv', 'scikit-learn', 'whisper']),
    ('web', ['react', 'next.js', 'react-native', 'expo', 'fastapi', 'flask', 'node.js', 'tailwind']),
    ('cloud', ['gcp', 'cloudflare-workers', 'firebase', 'qdrant', 'docker', 'terraform']),
    ('hardware', ['arm-cortex', 'rp2040', 'arduino', 'zynq-fpga', 'vivado', 'i2c', 'spi', 'uart', 'ble']),
    ('tools', ['git', 'linux', 'gitlab-ci', 'pytest', 'claude-code']),
]

CONTACT = [('email', 'pink'), ('linkedin', 'cyan'), ('website', 'green'), ('resume', 'yellow')]

# ─────────────────────────────── THEME ───────────────────────────────

C = dict(bg='#0f1117', bar='#1a1d27', border='#2d3140', fg='#f8f8f2', dim='#6272a4',
         pink='#ff79c6', purple='#bd93f9', green='#50fa7b', cyan='#8be9fd', yellow='#f1fa8c',
         orange='#ffb86c', red='#ff5555')
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
CH = 0.602  # monospace advance per 1px of font-size (Menlo/SF Mono); narrower fonts just leave slack


def save(name, w, h, body):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
           f'font-family="{MONO}">{body}</svg>')
    (ASSETS / name).write_text(svg)


def window(w, h, title):
    return (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="{C["bg"]}" stroke="{C["border"]}" stroke-width="1.5"/>'
            f'<path d="M1 13a12 12 0 0 1 12-12h{w-26}a12 12 0 0 1 12 12v23H1z" fill="{C["bar"]}"/>'
            f'<line x1="1" y1="36" x2="{w-1}" y2="36" stroke="{C["border"]}"/>'
            f'<circle cx="22" cy="18.5" r="6" fill="#ff5f57"/><circle cx="42" cy="18.5" r="6" fill="#febc2e"/>'
            f'<circle cx="62" cy="18.5" r="6" fill="#28c840"/>'
            f'<text x="{w/2}" y="23" text-anchor="middle" font-size="13" fill="{C["dim"]}">{escape(title)}</text>')


def prompt(x, y, path='~', cmd=''):
    return (f'<text x="{x}" y="{y}" font-size="15" xml:space="preserve">'
            f'<tspan fill="{C["green"]}" font-weight="700">{USER}@sfu</tspan>'
            f'<tspan fill="{C["fg"]}">:</tspan><tspan fill="{C["purple"]}" font-weight="700">{path}</tspan>'
            f'<tspan fill="{C["fg"]}">$ {escape(cmd)}</tspan></text>')


def prompt_width(path):
    return len(f'{USER}@sfu:{path}$ ') * 15 * CH


def typed(text, x, y, start, step=0.08, size=15):
    """Reveals one character at a time; independent of the viewer's font width."""
    spans = ''.join(f'<tspan visibility="hidden">{"&#160;" if ch == " " else escape(ch)}'
                    f'<set attributeName="visibility" to="visible" begin="{start + i*step:.2f}s" fill="freeze"/></tspan>'
                    for i, ch in enumerate(text))
    return f'<text x="{x:.0f}" y="{y}" font-size="{size}" fill="{C["fg"]}" xml:space="preserve">{spans}</text>'


def appear(inner, t, dur=0.25):
    return (f'<g opacity="0">{inner}<animate attributeName="opacity" from="0" to="1" '
            f'begin="{t:.2f}s" dur="{dur}s" fill="freeze"/></g>')


def cursor(x, y, begin=0.0):
    return (f'<rect x="{x:.0f}" y="{y-13}" width="9" height="17" fill="{C["fg"]}" opacity="0">'
            f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" '
            f'begin="{begin:.2f}s" repeatCount="indefinite"/></rect>')


# ─────────────────────────────── ASSETS ───────────────────────────────

def header():
    W, H = 900, 540
    p = [window(W, H, f'{USER}@{HOST}: ~'), prompt(24, 66)]
    p.append(typed('neofetch', 24 + prompt_width('~'), 66, 0.4, 0.09))
    t0 = 0.4 + 8 * 0.09 + 0.3

    fs, lh, top = 8.6, 9.8, 112
    for r, row in enumerate(portrait()):
        spans, run, col = [], '', None
        for ch, c in row + [(None, 'END')]:
            if c != col and run:
                spans.append(f'<tspan fill="{col}">{escape(run)}</tspan>' if col else escape(run))
                run = ''
            if ch is None:
                break
            col = c
            run += ch
        p.append(appear(f'<text x="26" y="{top + r*lh:.1f}" font-size="{fs}" xml:space="preserve">{"".join(spans)}</text>',
                        t0 + r * 0.03, 0.2))

    X, Y, step = 340, 104, 25
    t = t0 + 0.4
    lines = [(f'<text x="{X}" y="{Y}" font-size="16" font-weight="700" xml:space="preserve">'
              f'<tspan fill="{C["green"]}">{USER}</tspan><tspan fill="{C["fg"]}">@</tspan>'
              f'<tspan fill="{C["purple"]}">{HOST}</tspan></text>'),
             f'<text x="{X}" y="{Y + step}" font-size="15" fill="{C["dim"]}">{"─" * len(USER + HOST + "@")}</text>']
    for i, (k, v) in enumerate(NEOFETCH, start=2):
        lines.append(f'<text x="{X}" y="{Y + i*step}" font-size="15" xml:space="preserve">'
                     f'<tspan fill="{C["pink"]}" font-weight="700">{escape(k)}</tspan>'
                     f'<tspan fill="{C["fg"]}">: {escape(v)}</tspan></text>')
    for i, s in enumerate(lines):
        p.append(appear(s, t + i * 0.1))
    y = Y + len(lines) * step - 8
    swatches = ['#21222c', C['red'], C['green'], C['yellow'], C['purple'], C['pink'], C['cyan'], C['fg']]
    p.append(appear(''.join(f'<rect x="{X + i*30}" y="{y}" width="30" height="16" fill="{c}"/>'
                            for i, c in enumerate(swatches)), t + len(lines) * 0.1))

    tend = t + len(lines) * 0.1 + 0.4
    p.append(appear(prompt(24, H - 22), tend))
    p.append(cursor(24 + prompt_width('~'), H - 22, tend))
    save('header.svg', W, H, ''.join(p))


def divider(name, cmd):
    body = (f'<text x="0" y="28" font-size="16" xml:space="preserve"><tspan fill="{C["dim"]}">──── </tspan>'
            f'<tspan fill="{C["green"]}" font-weight="700">$ </tspan><tspan fill="{C["purple"]}" font-weight="700">{escape(cmd)}</tspan>'
            f'<tspan fill="{C["dim"]}"> {"─" * 90}</tspan></text>')
    save(f'divider-{name}.svg', 900, 44, body)


def card(proj, n_lines):
    W = 440
    slug = proj['slug']
    path = f'~/{slug}'
    desc = textwrap.wrap(proj['desc'], 46)
    H = 206 + n_lines * 20
    p = [window(W, H, f'~/projects/{slug}'), prompt(18, 64, path, 'cat README.md')]

    title = f'# {proj["name"]}'
    p.append(f'<text x="18" y="96" font-size="19" font-weight="700" fill="{C["purple"]}">{escape(title)}</text>')
    if proj.get('badge'):
        bx = 18 + len(title) * 19 * CH + 12
        bw = len(proj['badge']) * 12 * CH + 18
        p.append(f'<rect x="{bx:.0f}" y="80" width="{bw:.0f}" height="21" rx="10" fill="none" stroke="{C["yellow"]}"/>'
                 f'<text x="{bx + 9:.0f}" y="95" font-size="12" fill="{C["yellow"]}">{escape(proj["badge"])}</text>')
    for i, line in enumerate(desc):
        p.append(f'<text x="18" y="{124 + i*20}" font-size="13.5" fill="{C["fg"]}" opacity=".85">{escape(line)}</text>')

    y = 124 + n_lines * 20 + 12
    p.append(prompt(18, y, path, 'ls stack/'))
    cols = [C['cyan'], C['green'], C['orange'], C['pink'], C['yellow']]
    spans = ''.join(f'<tspan fill="{cols[i % len(cols)]}" font-weight="700">{escape(s)}/</tspan><tspan>  </tspan>'
                    for i, s in enumerate(proj['stack']))
    assert sum(len(s) + 3 for s in proj['stack']) * 14 * CH < W - 30, f'{slug}: stack line too long'
    p.append(f'<text x="18" y="{y + 24}" font-size="14" xml:space="preserve">{spans}</text>')
    p.append(prompt(18, y + 50, path))
    p.append(cursor(18 + prompt_width(path), y + 50))
    save(f'card-{slug}.svg', W, H, ''.join(p))


def stack():
    W = 900
    label_w = max(len(k) for k, _ in STACK) + 3
    H = 124 + len(STACK) * 30
    p = [window(W, H, '~/stack'), prompt(24, 66)]
    p.append(typed('ls ~/stack/*', 24 + prompt_width('~'), 66, 0.3, 0.07))
    colors = [C['pink'], C['purple'], C['cyan'], C['orange'], C['green'], C['yellow']]
    for i, (cat, items) in enumerate(STACK):
        row = f'{cat}/'.ljust(label_w)
        assert (label_w + sum(len(s) + 2 for s in items)) * 14 * CH < W - 48, f'{cat}: row too long'
        s = (f'<text x="24" y="{100 + i*30}" font-size="14" xml:space="preserve">'
             f'<tspan fill="{colors[i]}" font-weight="700">{escape(row)}</tspan>'
             f'<tspan fill="{C["fg"]}">{escape("  ".join(items))}</tspan></text>')
        p.append(appear(s, 1.4 + i * 0.15))
    p.append(appear(prompt(24, H - 20), 1.4 + len(STACK) * 0.15))
    p.append(cursor(24 + prompt_width('~'), H - 20, 1.4 + len(STACK) * 0.15))
    save('stack.svg', W, H, ''.join(p))


ICONS = {
    'email': lambda c: (f'<rect x="18" y="16" width="22" height="16" rx="2" fill="none" stroke="{c}" stroke-width="2"/>'
                        f'<path d="M19 18l10 8 10-8" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>'),
    'linkedin': lambda c: (f'<rect x="18" y="13" width="22" height="22" rx="4" fill="{c}"/>'
                           f'<text x="29" y="30" text-anchor="middle" font-size="14" font-weight="800" '
                           f'font-family="Helvetica,Arial,sans-serif" fill="{C["bg"]}">in</text>'),
    'website': lambda c: (f'<circle cx="29" cy="24" r="11" fill="none" stroke="{c}" stroke-width="2"/>'
                          f'<ellipse cx="29" cy="24" rx="4.5" ry="11" fill="none" stroke="{c}" stroke-width="1.6"/>'
                          f'<path d="M18 24h22M20 18h18M20 30h18" stroke="{c}" stroke-width="1.4"/>'),
    'resume': lambda c: (f'<path d="M20 12h13l6 6v18H20z" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>'
                         f'<path d="M33 12v6h6M24 24h11M24 28h11M24 32h7" fill="none" stroke="{c}" stroke-width="1.6"/>'),
}


def contact_button(name, color):
    W, H = 200, 48
    c = C[color]
    body = (f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{C["bg"]}" stroke="{c}" stroke-width="1.5"/>'
            f'{ICONS[name](c)}'
            f'<text x="54" y="29" font-size="15" xml:space="preserve"><tspan fill="{C["green"]}" font-weight="700">./</tspan>'
            f'<tspan fill="{c}" font-weight="700">{name}</tspan></text>'
            f'<text x="{W-18}" y="29" text-anchor="end" font-size="15" fill="{C["dim"]}">↗</text>')
    save(f'btn-{name}.svg', W, H, body)


def coffee():
    """Easter egg: `brew install coffee` with a progress bar and a steaming ASCII mug."""
    W, H = 640, 420
    p = [window(W, H, 'caffeine.sh'), prompt(24, 66)]
    p.append(typed('brew install coffee', 24 + prompt_width('~'), 66, 0.3, 0.06))
    t = 0.3 + 19 * 0.06 + 0.3
    out = [(C['cyan'], '==> Grinding beans...'), (C['cyan'], '==> Brewing at 94°C...')]
    for i, (col, s) in enumerate(out):
        p.append(appear(f'<text x="24" y="{96 + i*24}" font-size="14" fill="{col}">{escape(s)}</text>', t + i * 0.5))
    # progress bar fills after the brew line
    bar_t = t + 1.1
    p.append(appear(f'<text x="24" y="148" font-size="14" fill="{C["fg"]}" xml:space="preserve">[                              ]</text>', bar_t, 0.1))
    p.append(f'<rect x="34" y="137" width="0" height="13" fill="{C["green"]}">'
             f'<animate attributeName="width" from="0" to="252" begin="{bar_t:.2f}s" dur="1.8s" fill="freeze"/></rect>')
    done = bar_t + 1.9
    p.append(appear(f'<text x="310" y="148" font-size="14" fill="{C["green"]}">100%</text>', done, 0.1))

    mug = ['.-----------.',
           '|           |--.',
           '|  ALI.EXE  |  |',
           '|           |--\'',
           '\\           /',
           " `---------'"]
    mx, my = 250, 226
    for i, line in enumerate(mug):
        p.append(appear(f'<text x="{mx}" y="{my + i*18}" font-size="15" fill="{C["orange"]}" xml:space="preserve">{escape(line)}</text>',
                        done + 0.3 + i * 0.08))
    # steam: three wisps rising off the rim and fading, on a loop
    for j, d in enumerate([0.0, 0.6, 1.2]):
        x = mx + (3 + j * 3) * 15 * CH
        p.append(f'<text x="{x:.0f}" y="{my - 14}" font-size="16" fill="{C["dim"]}" opacity="0">{"(" if j % 2 else ")"}'
                 f'<animate attributeName="y" values="{my - 14};{my - 50}" dur="1.8s" begin="{done + 1 + d:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;.9;0" dur="1.8s" begin="{done + 1 + d:.2f}s" repeatCount="indefinite"/></text>')
    fin = done + 1.2
    p.append(appear(f'<text x="24" y="{H - 48}" font-size="14" fill="{C["green"]}">✔ coffee installed. resuming: shipping code.</text>', fin))
    p.append(appear(prompt(24, H - 20), fin + 0.3))
    p.append(cursor(24 + prompt_width('~'), H - 20, fin + 0.3))
    save('coffee.svg', W, H, ''.join(p))


if __name__ == '__main__':
    ASSETS.mkdir(exist_ok=True)
    header()
    for name, cmd in [('projects', 'cd ~/projects'), ('stack', 'ls ~/stack'),
                      ('activity', 'git log --graph'), ('contact', './contact.sh')]:
        divider(name, cmd)
    n_lines = max(len(textwrap.wrap(p['desc'], 46)) for p in PROJECTS)
    for proj in PROJECTS:
        card(proj, n_lines)
    stack()
    for name, color in CONTACT:
        contact_button(name, color)
    coffee()
    print('wrote', ', '.join(sorted(f.name for f in ASSETS.glob('*.svg'))))
