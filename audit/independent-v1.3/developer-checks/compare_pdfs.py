"""Compare a fresh Chrome rebuild of the print PDFs with the shipped ones.

Usage: python3 compare_pdfs.py SHIPPED_DIR REBUILT_DIR [REBUILT2_DIR] OUT.json

For every PDF: SHA-256 of both files, page count, PDF metadata, page-by-page
extracted text (pdftotext -layout) and page-by-page rendered pixels
(pdftoppm, 100 dpi, greyscale). Pixel equality is exact; any differing page
also records how many pixels differ.
"""
import hashlib, json, os, subprocess, sys, tempfile
from pypdf import PdfReader

PDFS = ['Caesar_Solo_Rules.pdf', 'Caesar_Solo_Reference.pdf', 'Caesar_Solo_Cards.pdf',
        'Caesar_Solo_Record_Sheet.pdf', 'Caesar_Solo_Sim_Report.pdf', 'Caesar_Solo_Sample_Game.pdf',
        'Caesar_Solo_Print_and_Play.pdf']


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def meta(p):
    m = PdfReader(p).metadata or {}
    return {k: str(v) for k, v in m.items()}


def page_text(p, i):
    return subprocess.run(['pdftotext', '-layout', '-f', str(i), '-l', str(i), p, '-'],
                          capture_output=True, text=True, check=True).stdout


def page_pixels(p, i, tmp):
    base = os.path.join(tmp, 'pg')
    subprocess.run(['pdftoppm', '-r', '100', '-gray', '-f', str(i), '-l', str(i), '-singlefile', p, base], check=True)
    data = open(base + '.pgm', 'rb').read()
    os.unlink(base + '.pgm')
    return data


def pgm_diff(a, b):
    # P5 header: "P5\n<w> <h>\n255\n"
    def split(d):
        parts = d.split(b'\n', 3)
        return parts[1], parts[3]
    ha, pa = split(a)
    hb, pb = split(b)
    if ha != hb or len(pa) != len(pb):
        return None
    return sum(1 for x, y in zip(pa, pb) if x != y)


def compare(a, b, tmp):
    ra, rb = PdfReader(a), PdfReader(b)
    pages = []
    for i in range(1, len(ra.pages) + 1):
        ta, tb = page_text(a, i), page_text(b, i)
        xa, xb = page_pixels(a, i, tmp), page_pixels(b, i, tmp)
        d = 0 if xa == xb else pgm_diff(xa, xb)
        pages.append({'page': i, 'text_equal': ta == tb, 'pixels_equal': xa == xb, 'pixels_differing': d})
    return {
        'bytes_equal': sha(a) == sha(b), 'sha256': [sha(a), sha(b)],
        'pages': [len(ra.pages), len(rb.pages)],
        'metadata': [meta(a), meta(b)],
        'all_text_equal': all(p['text_equal'] for p in pages) and len(ra.pages) == len(rb.pages),
        'all_pixels_equal': all(p['pixels_equal'] for p in pages) and len(ra.pages) == len(rb.pages),
        'per_page': pages,
    }


def main():
    shipped, rebuilt = sys.argv[1], sys.argv[2]
    rebuilt2 = sys.argv[3] if len(sys.argv) > 4 else None
    out = sys.argv[-1]
    res = {'shipped_dir': shipped, 'rebuilt_dir': rebuilt, 'files': {}, 'rebuild_vs_rebuild': {}}
    with tempfile.TemporaryDirectory() as tmp:
        for f in PDFS:
            res['files'][f] = compare(os.path.join(shipped, f), os.path.join(rebuilt, f), tmp)
            if rebuilt2:
                r2 = compare(os.path.join(rebuilt, f), os.path.join(rebuilt2, f), tmp)
                res['rebuild_vs_rebuild'][f] = {k: r2[k] for k in ('bytes_equal', 'all_text_equal', 'all_pixels_equal')}
    res['summary'] = {
        'files': len(PDFS),
        'pages': sum(v['pages'][0] for v in res['files'].values()),
        'all_page_counts_equal': all(v['pages'][0] == v['pages'][1] for v in res['files'].values()),
        'all_text_equal': all(v['all_text_equal'] for v in res['files'].values()),
        'all_pixels_equal': all(v['all_pixels_equal'] for v in res['files'].values()),
        'bytes_equal': sum(v['bytes_equal'] for v in res['files'].values()),
    }
    json.dump(res, open(out, 'w'), indent=1)
    print(json.dumps(res['summary'], indent=1))
    for f, v in res['files'].items():
        bad = [p['page'] for p in v['per_page'] if not (p['text_equal'] and p['pixels_equal'])]
        print(f, 'bytes', v['bytes_equal'], 'text', v['all_text_equal'], 'pixels', v['all_pixels_equal'], 'diff pages', bad)
        if not v['bytes_equal']:
            print('   meta shipped', v['metadata'][0])
            print('   meta rebuilt', v['metadata'][1])
    if rebuilt2:
        print('rebuild vs rebuild', res['rebuild_vs_rebuild'])


if __name__ == '__main__':
    main()
