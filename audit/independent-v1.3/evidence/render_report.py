"""Render the accompanying audit Markdown as a standalone PDF.
python3 render_report.py REPORT.md REPORT.pdf
Requires reportlab, markdown and beautifulsoup4; DejaVu fonts.
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape
import markdown
from bs4 import BeautifulSoup
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, PageBreak, CondPageBreak
from reportlab.pdfgen import canvas

fontroot = Path('/usr/share/fonts/truetype/dejavu')
for name, file in [('Audit', 'DejaVuSans.ttf'), ('Audit-Bold', 'DejaVuSans-Bold.ttf'),
                   ('Audit-Italic', 'DejaVuSans-Oblique.ttf'), ('AuditMono', 'DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(fontroot / file)))
pdfmetrics.registerFontFamily('Audit', normal='Audit', bold='Audit-Bold', italic='Audit-Italic', boldItalic='Audit-Bold')

styles = getSampleStyleSheet()
body = ParagraphStyle('AuditBody', fontName='Audit', fontSize=9.15, leading=13.2,
                      spaceAfter=6, splitLongWords=True, textColor=colors.HexColor('#24303c'))
title = ParagraphStyle('AuditTitle', parent=body, fontName='Audit-Bold', fontSize=20, leading=24,
                       spaceAfter=12, textColor=colors.HexColor('#701d24'), keepWithNext=True)
h2 = ParagraphStyle('AuditH2', parent=body, fontName='Audit-Bold', fontSize=12.4, leading=16,
                    spaceBefore=13, spaceAfter=6, textColor=colors.HexColor('#701d24'), keepWithNext=True)
h3 = ParagraphStyle('AuditH3', parent=h2, fontSize=10.3, leading=14, spaceBefore=9)
tablehead = ParagraphStyle('TableHead', parent=h2, keepWithNext=False)
severity = ParagraphStyle('Severity', parent=body, keepWithNext=True)
cellstyle = ParagraphStyle('AuditCell', parent=body, fontSize=8, leading=11.2, spaceAfter=0)
codestyle = ParagraphStyle('AuditCode', parent=body, fontName='AuditMono', fontSize=7.2, leading=10,
                          backColor=colors.HexColor('#f2f4f5'), borderPadding=8, spaceAfter=9)

def inline(tag):
    cp = BeautifulSoup(str(tag), 'html.parser')
    for code in cp.find_all('code'):
        code.name = 'font'
        code.attrs = {'name': 'AuditMono', 'size': '8'}
    for st in cp.find_all('strong'):
        st.name = 'b'
    for em in cp.find_all('em'):
        em.name = 'i'
    root = cp.find()
    return ''.join(str(x) for x in root.contents) if root else escape(str(tag))

source = Path(sys.argv[1])
soup = BeautifulSoup(markdown.markdown(source.read_text(), extensions=['tables', 'fenced_code']), 'html.parser')
flow = []
width = 526
for el in soup.children:
    name = getattr(el, 'name', None)
    if name in ('h1', 'h2', 'h3'):
        if name == 'h2' and el.get_text() == 'Optional usability and reporting improvements':
            flow.append(PageBreak())
        next_el=el.find_next_sibling()
        style={'h1': title, 'h2': h2, 'h3': h3}[name]
        if name=='h2' and next_el is not None and next_el.name=='table':
            flow.append(CondPageBreak(95));style=tablehead
        flow.append(Paragraph(inline(el), style))
    elif name == 'p':
        flow.append(Paragraph(inline(el), severity if el.get_text().startswith('Severity:') else body))
    elif name in ('ul', 'ol'):
        for i, li in enumerate(el.find_all('li', recursive=False), 1):
            text = inline(li)
            bullet = f'{i}.' if name == 'ol' else '•'
            flow.append(Paragraph(escape(bullet) + ' ' + text, body))
    elif name == 'pre':
        flow.append(Preformatted(el.get_text().rstrip(), codestyle, maxLineLength=110))
    elif name == 'table':
        rows = []
        for tr in el.find_all('tr'):
            rows.append([Paragraph(inline(td), cellstyle) for td in tr.find_all(['th', 'td'])])
        count = len(rows[0])
        widths = {2: [145, 381], 3: [210, 45, 271], 4: [33, 51, 129, 313]}[count]
        table = Table(rows, colWidths=widths, repeatRows=1, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e9e0d3')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), .35, colors.HexColor('#bcc3c8')),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f6f7f7')]),
        ]))
        flow.extend([table, Spacer(1, 8)])

def footer(c, doc):
    c.saveState()
    c.setStrokeColor(colors.HexColor('#bbc2c7'))
    c.line(43, 37, 569, 37)
    c.setFont('Audit', 7)
    c.setFillColor(colors.HexColor('#65717a'))
    c.drawString(43, 25, 'Caesar solo bots · v1.3 verification · 7c0d65c · 22 November 2026')
    c.drawRightString(569, 25, str(doc.page))
    c.restoreState()

class FixedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        kwargs['invariant'] = 1
        super().__init__(*args, **kwargs)

doc = SimpleDocTemplate(sys.argv[2], pagesize=letter, rightMargin=43, leftMargin=43,
                        topMargin=42, bottomMargin=48,
                        title='Caesar Solo v1.3 — Verification', author='Codex',
                        subject='Rules, simulation, helper and printables audit of commit 7c0d65c')
doc.build(flow, onFirstPage=footer, onLaterPages=footer, canvasmaker=FixedCanvas)
print(sys.argv[2])
