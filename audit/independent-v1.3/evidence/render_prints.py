"""Render all unique shipped PDF pages as labelled four-page contact sheets.
python3 render_prints.py REPO OUTPUT_DIR
"""
import sys, json
from pathlib import Path
import fitz
from PIL import Image, ImageDraw

r = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
inventory = []
for name in ['Rules', 'Reference', 'Cards', 'Record_Sheet', 'Sample_Game', 'Sim_Report']:
    d = fitz.open(r / f'print/Caesar_Solo_{name}.pdf')
    inventory.append({'name': name, 'pages': len(d)})
    for start in range(0, len(d), 4):
        sheet = Image.new('RGB', (1360, 1810), '#dcdcdc')
        dr = ImageDraw.Draw(sheet)
        for j, p in enumerate(list(d)[start:start + 4]):
            scale = min(660 / p.rect.width, 860 / p.rect.height)
            px = p.get_pixmap(matrix=fitz.Matrix(scale, scale))
            im = Image.frombytes('RGB', (px.width, px.height), px.samples)
            x, y = (j % 2) * 680 + (680 - im.width) // 2, (j // 2) * 905 + 28
            sheet.paste(im, (x, y))
            dr.text((x, y - 20), f'{name} / page {start + j + 1}', fill='black')
        sheet.save(out / f'{name}-{start + 1}.jpg', quality=88)
print(json.dumps(inventory))
