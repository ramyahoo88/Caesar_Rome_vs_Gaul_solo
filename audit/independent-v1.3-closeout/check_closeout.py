"""Independently check the committed v1.3 print-build closeout.

Usage: python3 check_closeout.py REPO OUTPUT.json
Needs PyMuPDF and pypdf. No browser, network, or product modifications.
Compares the actual committed old/new PDFs, not the developer's JSON flags.
"""
import hashlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys

import fitz
from pypdf import PdfReader
from io import BytesIO

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
old = "7c0d65c41b36de4c5cad96d7227b056d494685ff"
new = "529c12b8c6e2bd645733f5e726561bf4b27e5f61"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=repo)


def blob(ref, path):
    return git("show", f"{ref}:{path}")


def sha(data):
    return hashlib.sha256(data).hexdigest()


paths = git("diff", "--name-only", old, new).decode().splitlines()
product = [p for p in paths if p.startswith(("code/", "results/", "data/"))
           or (p.startswith("print/") and not p.endswith(".pdf") and p != "print/build.py")]
assert not product, product
report = {
    "oldCommit": old,
    "reviewedCommit": new,
    "changedFiles": paths,
    "changedGameRuleHelperCardOrResultFiles": product,
    "runtime": {"python": sys.version, "PyMuPDF": importlib.metadata.version("PyMuPDF"),
                "pypdf": importlib.metadata.version("pypdf")},
    "pdfComparisonMethod": "Committed blobs; PyMuPDF extracted text and exact RGB samples at 100 dpi",
    "pdfs": {},
}

evidence_path = "audit/independent-v1.3/developer-checks/pdf-rebuild-fixed-dates.json"
developer = json.loads(blob(new, evidence_path))
for path in sorted(p for p in paths if p.startswith("print/") and p.endswith(".pdf")):
    a, b = blob(old, path), blob(new, path)
    ar, br = PdfReader(BytesIO(a)), PdfReader(BytesIO(b))
    pages = []
    with fitz.open(stream=a, filetype="pdf") as ad, fitz.open(stream=b, filetype="pdf") as bd:
        assert len(ad) == len(bd), path
        for i, (ap, bp) in enumerate(zip(ad, bd), 1):
            ax = ap.get_pixmap(dpi=100, colorspace=fitz.csRGB, alpha=False)
            bx = bp.get_pixmap(dpi=100, colorspace=fitz.csRGB, alpha=False)
            row = {"page": i, "textEqual": ap.get_text() == bp.get_text(),
                   "geometryEqual": ap.rect == bp.rect,
                   "rgbPixelsEqual": (ax.width, ax.height, ax.samples) == (bx.width, bx.height, bx.samples),
                   "rgbSHA256": [sha(ax.samples), sha(bx.samples)]}
            assert row["textEqual"] and row["geometryEqual"] and row["rgbPixelsEqual"], (path, i)
            pages.append(row)
    stored = developer["files"][Path(path).name]
    # Index 0 is the original audited release; index 1 is the fixed-date build.
    assert stored["sha256"] == [sha(a), sha(b)], path
    assert b == (repo / path).read_bytes(), path
    am = {k: str(v) for k, v in (ar.metadata or {}).items()}
    bm = {k: str(v) for k, v in (br.metadata or {}).items()}
    assert bm["/CreationDate"] == bm["/ModDate"] == "D:20261122000000+00'00'", path
    before_tags = bool(ar.trailer["/Root"].get("/StructTreeRoot"))
    after_tags = bool(br.trailer["/Root"].get("/StructTreeRoot"))
    assert before_tags == after_tags, path
    report["pdfs"][Path(path).name] = {
        "sha256": [sha(a), sha(b)], "developerRecordedHashesMatchCommittedBlobs": True,
        "metadataBefore": am, "metadataAfter": bm,
        "structureTreePresent": [before_tags, after_tags], "pages": pages,
    }

helper_path = "audit/independent-v1.3/developer-checks/helper-browser.json"
helper = json.loads(blob(new, helper_path))
assert helper["total"] == len(helper["checks"]) == 37
assert helper["passed"] == sum(bool(c["pass"]) for c in helper["checks"]) == 37
assert not helper["errors"]
keyboard = next(c for c in helper["checks"] if c["check"].startswith("Tab reaches"))
report["developerHelperResults"] = {
    "passed": helper["passed"], "total": helper["total"], "errors": helper["errors"],
    "executionStatus": "Reviewed stored developer run; not independently rerun",
    "keyboardCheckLabel": keyboard["check"], "keyboardRecordedOrder": keyboard["detail"],
    "undoAppearsInRecordedTabOrder": "'undo'" in keyboard["detail"],
}
report["rebuildPairsRecordedByDeveloper"] = developer["rebuild_vs_rebuild"]
report["summary"] = {
    "files": len(report["pdfs"]), "pages": sum(len(v["pages"]) for v in report["pdfs"].values()),
    "allTextGeometryAndRGBPixelsEqual": True, "developerPDFHashesMatchCommittedBlobs": True,
    "freshBrowserRun": "Blocked by execution-environment/browser file-access policy",
    "freshChromePDFRebuild": "Blocked by execution environment; not certified by this run",
}
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report["summary"], indent=2))
