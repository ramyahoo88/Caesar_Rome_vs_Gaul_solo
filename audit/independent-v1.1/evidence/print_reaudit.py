"""Check v1.1 print content, edited sample and helper source identity.
python3 print_reaudit.py REPO OUTPUT_DIR
Requires PyMuPDF, Markdown and pypdf. Does not rebuild the Chrome PDFs.
"""
import sys,json,re,hashlib,subprocess,importlib.util
from pathlib import Path
import fitz
repo=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(repo/'code'))
from bots import ROME_DIRECTIVES_V4,GAUL_DIRECTIVES
spec=importlib.util.spec_from_file_location('builder',repo/'print/build.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
norm=lambda s:re.sub(r'\W+','',s.casefold())
sha=lambda a:hashlib.sha256(a).hexdigest()
inventory=[]
for p in sorted((repo/'print').glob('*.pdf')):
    with fitz.open(p)as d:inventory.append({'file':p.name,'pages':len(d),'sha256':sha(p.read_bytes())})
packet=fitz.open(repo/'print/Caesar_Solo_Print_and_Play.pdf');i=0
for name in ['Rules','Reference','Cards','Record_Sheet']:
    with fitz.open(repo/f'print/Caesar_Solo_{name}.pdf')as d:
        for p in d:assert p.get_text()==packet[i].get_text(),(name,i);i+=1
assert i==len(packet)==18
cards=json.loads((repo/'print/cards.json').read_text())
with fitz.open(repo/'print/Caesar_Solo_Cards.pdf')as d:
    for pn,side,deck in [(0,'R',ROME_DIRECTIVES_V4),(2,'G',GAUL_DIRECTIVES)]:
        cs=[c for c in cards if c['side']==side];assert len(cs)==len(deck)==9
        for j,(c,code)in enumerate(zip(cs,deck)):
            assert (c['name'],c['missions'],c['compass'])==(code[0],list(code[1]),code[2])
            x=33.12+(j%3)*182.88;y=12.96+(j//3)*254.88
            t=norm(d[pn].get_text(clip=fitz.Rect(x,y,x+180,y+252)))
            for v in [c['id'],c['name'],c['compass']]:assert norm(v)in t,(c['id'],v)
            for m in c['missions']:
                desc=b.GAUL_RAID if side=='G'and m=='RAID'else b.MISSION_TEXT[m]
                assert norm(m+desc)in t,(c['id'],m)
            if side=='R':assert norm('Before: CONTINUE PROTECT SUBMIT REGROUP')in t
        assert norm('IMPERATOR'if side=='R'else'CONCILIUM')in norm(d[pn+1].get_text())

docs={}
for name,title in [('Rules','Caesar Solo Bots — Rules v1.1'),('Sim_Report','Caesar Solo Bots — Simulation Report'),('Sample_Game','Caesar Solo Bots — Sample Game')]:
    a=b.md_page(repo/f'print/Caesar_Solo_{name}.md',title);assert a==b.md_page(repo/f'print/Caesar_Solo_{name}.md',title)
    docs[name]=a;(out/f'Caesar_Solo_{name}.html').write_text(a)
assert '<pre><code>cd code\n' in docs['Sim_Report'] and 'sample_game.py 57' in docs['Sim_Report']
rules=(repo/'print/Caesar_Solo_Rules.md').read_text()
assert 'CONTINUE, PROTECT, SUBMIT and REGROUP' in rules
with fitz.open(repo/'print/Caesar_Solo_Rules.pdf')as d:
    t=norm(''.join(p.get_text()for p in d))
    for s in ['version 1.1','Only cards in the Reserve can be used','plays #24 for AP and keeps #52','CONTINUE, PROTECT, SUBMIT and REGROUP','after the move']:
        assert norm(s)in t,s

generated=(out.parent/'sample-seed57.md').read_text()
archived=(repo/'results/sample_game_seed57.md').read_text();assert generated==archived
edited=(repo/'print/Caesar_Solo_Sample_Game.md').read_text()
def log(s):return [x.strip()for x in s.split('## Turn 1',1)[1].splitlines()if x.strip()and not x.startswith('**Result:**')]
assert log(generated)==log(edited)
assert 'Concilium (level 4' in generated and 'end VP 12' in generated

helper=(repo/'print/Caesar_Solo_Deck.html').read_bytes()
assert helper==subprocess.check_output(['git','show','dcbfc22:print/Caesar_Solo_Deck.html'],cwd=repo)
r={'pdfInventory':inventory,'packetPagesMatchingIndividualText':18,'individuallyCheckedFaces':18,
   'cardOrder':'Roman faces / Roman backs / Gallic faces / Gallic backs','C06SampleByteMatchesArchivedLog':True,
   'editedSamplePlayLogMatches':True,'C07AppendixPresent':True,'C08FencedCommandsAndSeed57':True,
   'helperSHA256':sha(helper),'helperGitBlobByteMatch':True,
   'PDFRebuild':'Not completed: no usable local Chrome','helperBuild':'Authored standalone source, no separate generator'}
(out/'print-results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
