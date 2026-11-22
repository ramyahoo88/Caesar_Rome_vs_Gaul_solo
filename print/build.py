"""Build the print-and-play PDFs.

Requires: Python-Markdown, pypdf, and headless Google Chrome (google-chrome on PATH).
Run from this folder:  python3 build.py
"""
import json, os, subprocess, sys, tempfile, html
import markdown
from pypdf import PdfWriter, PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE
CHROME = os.environ.get('CHROME', 'google-chrome')

BASE_CSS = """
@page { size: Letter; margin: 0.55in 0.6in 0.6in 0.6in; }
body { font-family: 'DejaVu Serif', Georgia, serif; font-size: 10.5pt; line-height: 1.32; color: #1d1d1d; }
h1 { font-size: 20pt; margin: 0 0 4pt 0; color: #7a1010; }
h2 { font-size: 14pt; margin: 14pt 0 4pt 0; color: #7a1010; border-bottom: 1px solid #c9b18a; padding-bottom: 2pt; break-after: avoid; }
h3 { font-size: 11.5pt; margin: 10pt 0 3pt 0; color: #3b2a10; break-after: avoid; }
p { margin: 4pt 0; }
ul, ol { margin: 3pt 0 3pt 0; padding-left: 18pt; }
li { margin: 1.5pt 0; }
table { border-collapse: collapse; width: 100%; margin: 5pt 0; font-size: 9.5pt; break-inside: auto; }
th, td { border: 1px solid #b9a27a; padding: 2.5pt 4pt; vertical-align: top; text-align: left; }
th { background: #efe4cf; }
tr { break-inside: avoid; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 9pt; }
hr { border: none; border-top: 1px solid #c9b18a; margin: 10pt 0; }
"""


def chrome_pdf(html_text, pdf_path):
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(html_text)
        tmp = f.name
    cmd = [CHROME, '--headless', '--disable-gpu', '--no-sandbox', '--no-pdf-header-footer',
           f'--print-to-pdf={pdf_path}', 'file://' + tmp]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.unlink(tmp)


def md_page(md_path, title, extra_css=''):
    text = open(md_path, encoding='utf-8').read()
    body = markdown.markdown(text, extensions=['tables', 'sane_lists'])
    foot = (title + ' · unofficial fan variant for Caesar: Rome vs. Gaul (GMT Games) · page ').replace('"', "'")
    page_css = ('@page { @bottom-center { content: "' + foot + '" counter(page); font-family: \'DejaVu Serif\', serif; '
                'font-size: 8pt; color: #777; } }')
    base = 'file://' + HERE + '/'
    return f"""<!doctype html><html><head><meta charset="utf-8"><base href="{base}"><title>{html.escape(title)}</title>
<style>{BASE_CSS}{page_css}img {{ width: 5.4in; max-width: 100%; display: block; margin: 4pt auto; }}{extra_css}</style></head><body>{body}</body></html>"""


# ------------------------------------------------------------------ Directive cards
MISSION_TEXT = {
    'RULE': 'Control Table lines 0–3: presence, convert, Provincia, gain a province.',
    'SIEGE': 'March and roll vs a Town that surrenders (3:1), has 2+ Siege Points (1:1), or where Caesar has 2:1. Octodurus last.',
    'RAID': 'SWEEP Gallic IMs: 4 Gallic province in Celtica / Provincia; 3 other Gallic province; 2 near Roman control. Not into danger (Caesar may).',
    'SETTLE': 'Whole Control Table (0–6).',
    'STRIKE': 'Attack Gallic CUs at 2:1 BS (Caesar 1.5:1). 3:1 first, then largest, then nearest.',
    'INVADE': 'Turn 3+, Caesar unmoved, 6 strongest CUs CS 12+: Britannia / Germania IMs.',
    'RISE': 'Major Uprising (Turn 4+, 2 AP, 2+ Submitted Tribes) — or empty the Council Box (free Tribe, or 3+ IMs).',
    'AMBUSH': 'Attack Roman CUs at 1.5:1 BS (Caesar’s army 2.1:1). Caesar first, then largest, then nearest.',
    'AGITATE': 'One Agitate Table action.',
    'BANK': 'Turns 1–5: one IM into the Council Box (max 6).',
}
GAUL_RAID = 'SWEEP Roman IMs: 4 Narbonensis; 3 Roman province; 2 other Provincia; 1 else. Never at/next to Caesar or into danger.'


def cards_html(cards):
    css = """
@page { size: Letter; margin: 0.18in 0.3in; }
body { margin: 0; font-family: 'DejaVu Sans', Arial, sans-serif; }
.sheet { display: grid; grid-template-columns: repeat(3, 2.5in); grid-auto-rows: 3.5in; gap: 0.04in; justify-content: center; page-break-after: always; }
.card { box-sizing: border-box; border: 1px dashed #999; padding: 0.11in; position: relative; overflow: hidden; }
.card .band { color: #fff; font-weight: bold; font-size: 9pt; letter-spacing: 1.5pt; padding: 3pt 6pt; margin: -0.11in -0.11in 6pt -0.11in; display: flex; justify-content: space-between; }
.R .band { background: #8a1414; } .G .band { background: #1d4f86; }
.head { display: flex; justify-content: space-between; align-items: center; height: 0.5in; border-bottom: 1px solid #ccc; margin-bottom: 4pt; }
.title { font-family: 'DejaVu Serif', Georgia, serif; font-size: 16pt; font-weight: bold; }
.compass { width: 0.44in; height: 0.44in; border-radius: 50%; border: 2px solid #333; box-sizing: border-box;
           font-size: 18pt; font-weight: bold; text-align: center; line-height: 0.4in; }
ol { margin: 6pt 0 0 0; padding-left: 14pt; font-size: 7.6pt; line-height: 1.22; }
li { margin: 0 0 3pt 0; } li b { font-size: 8.6pt; }
.foot { position: absolute; bottom: 0.08in; left: 0.11in; right: 0.11in; font-size: 6.8pt; color: #444; border-top: 1px solid #bbb; padding-top: 2pt; }
.back { display: flex; align-items: center; justify-content: center; flex-direction: column; color: #fff; }
.back.R { background: #8a1414; } .back.G { background: #1d4f86; }
.back .big { font-family: 'DejaVu Serif', Georgia, serif; font-size: 22pt; font-weight: bold; letter-spacing: 2pt; }
.back .small { font-size: 9pt; margin-top: 6pt; }
"""
    pages = []
    for side in ('R', 'G'):
        cs = [c for c in cards if c['side'] == side]
        cells = []
        for c in cs:
            items = []
            for m in c['missions']:
                t = GAUL_RAID if (side == 'G' and m == 'RAID') else MISSION_TEXT[m]
                items.append(f'<li><b>{m}</b> — {html.escape(t)}</li>')
            if side == 'R':
                foot = 'Before: CONTINUE · PROTECT · SUBMIT · REGROUP &nbsp;|&nbsp; After: GATHER · CONTROL'
            else:
                foot = 'After: AGITATE &nbsp;|&nbsp; Reveal 2 · ★ Live event · higher AP'
            cells.append(f"""<div class="card {side}"><div class="band"><span>{'IMPERATOR' if side == 'R' else 'CONCILIUM'}</span><span>{c['id']}</span></div>
<div class="head"><div class="title">{html.escape(c['name'])}</div><div class="compass">{c['compass']}</div></div>
<ol>{''.join(items)}</ol><div class="foot">{foot}</div></div>""")
        pages.append('<div class="sheet">' + ''.join(cells) + '</div>')
    backs = []
    for side in ('R', 'G'):
        name = 'IMPERATOR' if side == 'R' else 'CONCILIUM'
        sub = 'Rome · Directive' if side == 'R' else 'Gaul · Directive'
        backs.append('<div class="sheet">' + ''.join(
            f'<div class="card back {side}"><div class="big">{name}</div><div class="small">{sub}</div></div>' for _ in range(9)) + '</div>')
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(pages + backs)}</body></html>'


def main():
    cards = json.load(open(os.path.join(HERE, 'cards.json')))
    chrome_pdf(md_page(os.path.join(HERE, 'Caesar_Solo_Rules.md'), 'Caesar Solo Bots — Rules v1.0'),
               os.path.join(OUT, 'Caesar_Solo_Rules.pdf'))
    chrome_pdf(cards_html(cards), os.path.join(OUT, 'Caesar_Solo_Cards.pdf'))
    chrome_pdf(open(os.path.join(HERE, 'reference.html'), encoding='utf-8').read(), os.path.join(OUT, 'Caesar_Solo_Reference.pdf'))
    chrome_pdf(open(os.path.join(HERE, 'record_sheet.html'), encoding='utf-8').read(), os.path.join(OUT, 'Caesar_Solo_Record_Sheet.pdf'))
    for md, title in (('Caesar_Solo_Sim_Report.md', 'Caesar Solo Bots — Simulation Report'),
                      ('Caesar_Solo_Sample_Game.md', 'Caesar Solo Bots — Sample Game')):
        p = os.path.join(HERE, md)
        if os.path.exists(p):
            chrome_pdf(md_page(p, title), os.path.join(OUT, md.replace('.md', '.pdf')))
    w = PdfWriter()
    for f in ('Caesar_Solo_Rules.pdf', 'Caesar_Solo_Reference.pdf', 'Caesar_Solo_Cards.pdf', 'Caesar_Solo_Record_Sheet.pdf'):
        for pg in PdfReader(os.path.join(OUT, f)).pages:
            w.add_page(pg)
    with open(os.path.join(OUT, 'Caesar_Solo_Print_and_Play.pdf'), 'wb') as f:
        w.write(f)
    for f in sorted(os.listdir(OUT)):
        if f.endswith('.pdf'):
            print(f, len(PdfReader(os.path.join(OUT, f)).pages), 'pages')


if __name__ == '__main__':
    main()
