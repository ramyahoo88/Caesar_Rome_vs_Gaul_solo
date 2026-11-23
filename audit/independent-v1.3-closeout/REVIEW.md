# Caesar solo v1.3: review of the print-build closeout

Reviewed 23 November 2026. Release commit: `529c12b8c6e2bd645733f5e726561bf4b27e5f61`.
Compared with the previously audited game release, `7c0d65c41b36de4c5cad96d7227b056d494685ff`, and the preceding verification commit, `ceff30c`.

**Verdict: no new release blocker. The committed printables support the developer's claim that the pages are unchanged.** All 20 existing engine tests pass. The new evidence is correctly identified as developer checks. One Low test-coverage finding and one optional build-documentation improvement are recorded below; neither establishes a game or helper defect.

This is a review of the closeout, not a replacement full engine audit or a new clean-room bot implementation. It adds this report and its reproducible comparison evidence only. No product, rule, helper, card, result, or developer-check files are changed.

## Independently verified

| Check | Result |
|---|---|
| Commit scope | No changes to `code/`, `data/`, `results/`, rules Markdown, card data, reference/record-sheet HTML, or the standalone helper. Changes are confined to the print builder, seven PDFs, documentation and new developer evidence. |
| Actual old/new PDF blobs | All seven files, 55 pages, have identical extracted text, page rectangles and exact RGB pixels at 100 dpi. This compares the committed files directly, rather than accepting the developer JSON's equality flags. |
| Evidence provenance | Every old/new SHA-256 pair in `pdf-rebuild-fixed-dates.json` matches its corresponding committed PDF. Index 0 is the audited release; index 1 is the new fixed-date file. The JSON's `bytes_equal: 0` summary concerns that old/new comparison; its separate rebuild-versus-rebuild results report seven equal pairs. There is no contradiction. |
| Titles and dates | The cards and packet have the stated titles. All seven PDFs have fixed creation and modification dates. |
| PDF structure trees | Retained in the six individual PDFs that previously had them. The combined packet had no structure tree before this update and still has none. |
| Existing engine tests | `python3 tests/test_audit_fixes.py`: 15 passing functions. `python3 tests/test_smoke.py`: five passing functions. |
| Stored helper run | The JSON contains 37 checks, all marked passing, with an empty error list. Its script uses Playwright, real browser storage and persistent browser profiles, apart from the deliberate storage-write-failure injection. Its phone checks emulate a touch viewport in desktop Chrome; they are not a physical Android/iOS device test. |
| Visual spot checks | Fresh renders of Rules page 1, both reference pages and both nine-card face sheets were inspected, as was the developer's final phone screenshot. No new layout problem was observed. |

The pixel comparison uses RGB rather than the developer comparison's grayscale, so it also checks that this update introduced no rendered colour changes at that resolution. The 55 pages include the 18 packet pages; they are not 55 different source pages.

## V13C-01: keyboard check does not cover Undo as labelled

**Severity:** Low. Verification coverage only; no demonstrated helper malfunction.

**Expected:** a check labelled "Tab reaches side buttons, level, Draw, Undo, Next turn and Reset" should observe an enabled Undo button in the Tab order.

**Source:** [`helper_browser.py`, lines 129-138](../independent-v1.3/developer-checks/helper_browser.py#L129-L138). Line 136 checks `bR`, `bG`, `lvl`, `draw`, `next`, and `reset`, but omits `undo`.

**Exact reproduction:** inspect that assertion and the corresponding entry in `developer-checks/helper-browser.json`. The check begins immediately after `fresh(pg)`, which resets the session, so Undo is disabled. The recorded focus order contains no `undo`, yet the check passes. The following Enter/Space test exercises Draw only.

**Impact:** the reported 37/37 result is accurate for the assertions actually executed, but the label overstates keyboard coverage. It cannot establish that an enabled Undo is reachable by Tab or can be activated with the keyboard. The other mouse-based Undo checks remain useful.

**Smallest proposed fix:** draw once before collecting the Tab order, include `undo` in the required IDs, and activate the focused Undo with Enter or Space to verify the prior counter/deck state is restored. Adjust the subsequent Draw-count expectation or reset that scenario first. Keep the shipped helper unchanged unless this test exposes an actual defect.

## Optional: make the PDF reproduction environment explicit

[`README.md`, line 33](../../README.md#L33) promises byte identity with the same Chrome version. The response narrows this to the same Chrome build and identifies Chrome for Testing `153.0.8010.12`, but does not record the developer's Python-Markdown/pypdf versions or font-file hashes.

Fixed dates remove a known nondeterministic input, and the retained developer results support two equal builds in that environment. They do not establish a guarantee across arbitrary systems sharing only a Chrome version: `build.py` also uses Python-Markdown, pypdf, installed DejaVu fonts and the operating environment.

Record those versions and font hashes alongside the exact Chrome build, and qualify the promise as requiring the same build environment. This is a documentation/reproduction recommendation, not a reproduced failure of the shipped PDFs.

## Execution limits

An independent fresh Chrome build and helper run were attempted with the exact reported Chrome for Testing `153.0.8010.12`. Both local launches were stopped by the execution environment before loading the page: Chrome aborted at `process_singleton_posix.cc` because `socket()` returned `Operation not permitted`. The available cloud browser also disallowed local `file:` URLs. No browser policy workaround was attempted.

Consequently, this review does **not** certify a fresh independent Chrome reconstruction, independently rerun the 37 browser assertions, or turn the developer's two builds into independent executions. It independently verifies the committed PDF changes and their correspondence to the recorded hashes. The original developer-run provenance remains explicit.

## Remaining work

* **Exact second-edition components:** the Siege Table and revised card AP assignments/text remain unresolved model inputs. This closeout supplies no new component evidence and does not increase the certainty of the study's win rates. Physical play uses the actual components under the existing rules.
* **Current-rules clean-room reconstruction:** still outstanding. This is a separate software task that can be performed without component photos, provided its model assumptions remain explicit; it is not intrinsically blocked by missing physical materials. The current rules and helper are unchanged by this commit.
* **Physical tabletop testing:** still outstanding. Browser checks, simulation and print comparisons do not substitute for it.

## Reproduce this comparison

From the repository root, with PyMuPDF and pypdf installed:

```sh
python3 audit/independent-v1.3-closeout/check_closeout.py . audit/independent-v1.3-closeout/evidence/closeout-results.json
```

The script pins both reviewed commits, checks local printables against the new committed blobs, verifies the recorded hash pairs, and compares every page's text, geometry and RGB pixels. It does not invoke Chrome. Run the two existing engine-test commands from `code/` to repeat those checks separately.
