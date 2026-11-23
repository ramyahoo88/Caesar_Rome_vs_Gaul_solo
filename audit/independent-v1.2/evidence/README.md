# Caesar solo v1.2 verification evidence

Reviewed release: `a52079a`. Date: 22 November 2026.

The requested R01–R03 regression tests are already in the release's
`code/tests/test_audit_fixes.py`. All 12 regression functions and five smoke
functions pass. No duplicate production tests or gameplay fixes were added.

Run the following against a clean checkout of the reviewed release. Replace
`REPO`, `EVIDENCE` and `OUTPUT` with absolute paths. Create `OUTPUT` first. Keep
all evidence scripts in one directory outside the release checkout.

```sh
python3 REPO/code/tests/test_audit_fixes.py
python3 REPO/code/tests/test_smoke.py
python3 EVIDENCE/campaign_audit.py REPO OUTPUT/campaigns.json 20
python3 EVIDENCE/nested_reserve.py REPO OUTPUT 100
python3 EVIDENCE/replay_archive.py REPO OUTPUT/archive-replays.json 3
python3 EVIDENCE/replay_latest.py REPO OUTPUT/latest-replays.json
python3 EVIDENCE/check_experiments.py REPO OUTPUT/experiment-checks.json
python3 EVIDENCE/release_checks.py REPO OUTPUT/release-checks.json
node EVIDENCE/helper_reaudit.cjs REPO OUTPUT
python3 REPO/code/sample_game.py 57 OUTPUT/sample-seed57.md
python3 EVIDENCE/print_reaudit.py REPO OUTPUT/rebuilt-html
```

## What each file establishes

- `regression-results.txt`, `smoke-results.txt`: all 17 shipped test functions pass.
- `campaign_audit.py`, `campaigns.json`: 240 configured full games, 60 matched seed
  values, 23,221 invariant boundaries and final 55-card accounting. No partial
  all-Reserve replacement or stale redraw was observed. This sweep did not record
  R06; that observation was added to the separate probe and archive replays below.
- `replay_archive.py`: exports `ObservedGame`, imported by `campaign_audit.py` and
  `nested_reserve.py`. Keep these files together. Its diagnostics do not change
  the policy's choices, Events, AP or RNG.
- `archive-replays.json`: first three games from every final-study cell (120
  configured runs, six distinct seed values); all archived summary results match.
  Four configured runs record R06, all the same Concilium-vs-Lookahead seed 200002
  trajectory repeated across levels 1–4. They are not independent occurrences.
- `nested_reserve.py`, `nested-reserve-fixtures.json`: seed-0 R06 reproductions
  for #42's extra play and a #24-canceled Event, plus a normal-entry control.
  The assertions confirm the defective baseline behavior; change them after a fix.
- `nested-reserve-results.json`: the fixtures and 100 additional full games on
  distinct seeds 950000–950099. R06 occurs at seeds 950034 and 950097. Full outcomes
  are retained; no win-rate correction or population prevalence is inferred.
- `replay_latest.py`, `latest-replays.json`: first two seeds of every latest-change
  cell (36 runs, two seed values), matching every stored VP and win result. The
  script extracts literal variant configurations with AST; it never imports and
  inadvertently executes the full experiment in `code/latest.py`.
- `check_experiments.py`, `experiment-checks.json`: all 18 latest-change cell
  statistics and 12 paired mean/SE comparisons recompute. The AP-only option keeps
  native edition settings and initial state identical while changing all 55 AP
  lookups correctly. R07 records that AP per-seed VP arrays are omitted on save;
  change its saved-key assertions if the raw arrays are retained after this review.
- `release_checks.py`, `release-checks.json`: 5,300-run archive reconciliation,
  nine region-priority cases, 1,172 hidden-identity comparisons of `choose_play`
  across 12 games, and four repeated-seed/VP-target full-trace checks.
- `helper_reaudit.cjs`, `helper-results.json`: exact shipped helper script with
  DOM/storage doubles. Tests 216 draw/reloads, 80 bonus boundaries, Undo and recovery,
  including mixed history and a corrupt step introduced after loading. Only test
  exports are injected into the in-memory script. The HTML file is not modified.
- `sample-seed57.md`: byte-identical to the archived raw sample. Gaul wins with
  Roman VP 11. The edited booklet's log and winter lines also match.
- `print_reaudit.py`, `print-results.json`: all 18 packet pages, all 18 card-face
  rectangles, face/back order, current rules text, sample equality and helper Git
  blob identity. Source HTML is regenerated, not Chrome PDFs.
- `visual-review.json`, `rendered/`: all 37 unique product PDF pages inspected;
  both reference-sheet columns on both pages included.
- `source-manifest.json`: pinned source hashes and runtime versions.
- `render_report.py`: renders the accompanying Markdown verification report to PDF.

Python simulation tests need only the standard library. Helper tests use Node.js
without npm dependencies. Print checks need PyMuPDF, Markdown and pypdf. Report
generation additionally needs ReportLab, Beautiful Soup and DejaVu fonts.

No fresh Chrome PDF build or independent real-browser helper test was completed.
PDF content checks do not certify byte-identical PDF reconstruction. The helper
is authored standalone HTML; its bytes match the reviewed Git blob. Source HTML
hashes may depend on the workspace's absolute base URL.

The complete 5,300-game study and full latest-change/AP experiments were not
independently rerun. Exact second-edition components and a complete clean-room
implementation remain outside this verification. No physical playtest was done.
