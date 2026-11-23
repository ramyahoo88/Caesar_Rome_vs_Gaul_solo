"""Verify shipped print content and regenerate source HTML without editing the release.
Requires PyMuPDF, Python-Markdown and pypdf.
python3 print_audit.py REPO OUTPUT_DIR
This does not rebuild PDFs or claim PDF byte reproducibility.
"""
import sys, json, re, hashlib, importlib.util, subprocess
from pathlib import Path
import fitz

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(repo / 'code'))
from bots import ROME_DIRECTIVES_V4, GAUL_DIRECTIVES

spec = importlib.util.spec_from_file_location('print_builder', repo / 'print/build.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
norm = lambda s: re.sub(r'\W+', '', s.casefold())
sha = lambda data: hashlib.sha256(data).hexdigest()
inventory = []
for p in sorted((repo / 'print').glob('*.pdf')):
    with fitz.open(p) as doc:
        inventory.append({'file': p.name, 'pages': len(doc), 'sha256': sha(p.read_bytes())})

packet = fitz.open(repo / 'print/Caesar_Solo_Print_and_Play.pdf')
parts = ['Rules', 'Reference', 'Cards', 'Record_Sheet']
i = 0
for part in parts:
    with fitz.open(repo / f'print/Caesar_Solo_{part}.pdf') as doc:
        for page in doc:
            assert page.get_text() == packet[i].get_text(), (part, i)
            i += 1
assert i == len(packet) == 18

cards = json.loads((repo / 'print/cards.json').read_text())
with fitz.open(repo / 'print/Caesar_Solo_Cards.pdf') as doc:
    for page_number, (side, deck) in enumerate([('R', ROME_DIRECTIVES_V4), ('G', GAUL_DIRECTIVES)]):
        cs = [c for c in cards if c['side'] == side]
        assert len(cs) == len(deck) == 9
        for j, (card, code) in enumerate(zip(cs, deck)):
            assert (card['name'], card['missions'], card['compass']) == (code[0], list(code[1]), code[2])
            # Each face is checked in its own rectangle, not by searching the whole PDF.
            x = 33.12 + (j % 3) * 182.88
            y = 12.96 + (j // 3) * 254.88
            text = norm(doc[page_number].get_text(clip=fitz.Rect(x, y, x + 180, y + 252)))
            for value in [card['id'], card['name'], card['compass']]:
                assert norm(value) in text, (card['id'], value)
            for mission in card['missions']:
                desc = b.GAUL_RAID if side == 'G' and mission == 'RAID' else b.MISSION_TEXT[mission]
                assert norm(mission + desc) in text, (card['id'], mission)
            if side == 'R':
                assert norm('Before: CONTINUE PROTECT SUBMIT REGROUP') in text

generated = []
for name, title in [('Rules', 'Caesar Solo Bots — Rules v1.0'),
                    ('Sim_Report', 'Caesar Solo Bots — Simulation Report'),
                    ('Sample_Game', 'Caesar Solo Bots — Sample Game')]:
    path = repo / f'print/Caesar_Solo_{name}.md'
    a = b.md_page(path, title)
    assert a == b.md_page(path, title)
    dest = out / f'Caesar_Solo_{name}.html'
    dest.write_text(a)
    generated.append({'file': dest.name, 'sha256': sha(a.encode())})
card_html = b.cards_html(cards)
assert card_html == b.cards_html(cards)
(out / 'Caesar_Solo_Cards.html').write_text(card_html)
generated.append({'file': 'Caesar_Solo_Cards.html', 'sha256': sha(card_html.encode())})

# C08: the rendered code fence is an inline code element, not a preformatted block.
report_html = (out / 'Caesar_Solo_Sim_Report.html').read_text()
assert '<pre>' not in report_html
assert '<code>cd code\npython3 study.py' in report_html

# C06/C07: retained source inconsistencies, also visible in shipped PDFs.
rules = (repo / 'print/Caesar_Solo_Rules.md').read_text()
assert 'CONTINUE, PROTECT, SUBMIT, REGROUP' in rules
stale = "Before the card's missions Imperator always tries CONTINUE, PROTECT and SUBMIT"
assert stale in rules
with fitz.open(repo / 'print/Caesar_Solo_Rules.pdf') as doc:
    assert norm(stale) in norm(''.join(p.get_text() for p in doc))
sample = (repo / 'print/Caesar_Solo_Sample_Game.md').read_text()
assert 'Seed 47' in sample and 'Concilium (level 3)' in sample
assert "options={'ap_bonus_R': 1}" in (repo / 'code/sample_game.py').read_text()

helper = repo / 'print/Caesar_Solo_Deck.html'
blob = subprocess.check_output(['git', 'show', '3e8dbac:print/Caesar_Solo_Deck.html'], cwd=repo)
assert helper.read_bytes() == blob
result = {'pdfInventory': inventory, 'combinedPagesMatchingIndividualText': i,
          'cardsCheckedWithinIndividualFace': 18, 'printDataMatchesSimulationDecks': True,
          'helperGitBlobByteMatch': True, 'helperSHA256': sha(blob),
          'regeneratedHTML': generated, 'PDFRebuild': 'Not performed: no usable local Chrome',
          'helperRebuild': 'Authored standalone HTML; no separate build generator exists',
          'C08': {'PDFPage': 7, 'codeFenceRenderedAsInlineCode': True,
                  'documentedSampleSeed': 45, 'shippedSampleSeed': 47}}
(out / 'print-results.json').write_text(json.dumps(result, indent=2))
print(json.dumps({k: v for k, v in result.items() if k not in ['regeneratedHTML', 'pdfInventory']}))
