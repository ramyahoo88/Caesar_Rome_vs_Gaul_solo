# Caesar solo v1.1 re-audit evidence

Reviewed release: `dcbfc228a71d054940d43fc9b71ab6d22defbba7`.
Review date: 22 November 2026.

Run the scripts outside a clean checkout of the reviewed release. Replace `REPO`,
`EVIDENCE` and `OUTPUT` with absolute paths. Create `OUTPUT` first. No production
source is edited by these tests.

```sh
python3 REPO/code/tests/test_audit_fixes.py
python3 REPO/code/tests/test_smoke.py
python3 EVIDENCE/targeted_reaudit.py REPO OUTPUT
node EVIDENCE/helper_reaudit.cjs REPO OUTPUT
python3 EVIDENCE/release_checks.py REPO OUTPUT/release-checks.json
python3 EVIDENCE/replay_archive.py REPO OUTPUT/archive-replays.json 3
python3 EVIDENCE/campaign_audit.py REPO OUTPUT/campaigns.json 20
python3 REPO/code/sample_game.py 57 OUTPUT/sample-seed57.md
python3 EVIDENCE/print_reaudit.py REPO OUTPUT/rebuilt-html
```

## Contents and interpretation

- `targeted_reaudit.py` / `targeted-results.json` reproduce R01, R02, R03 and R05.
  They deliberately assert remaining defective baseline behavior. After correction,
  change the affected assertions to the report's expected result.
- `helper_reaudit.cjs` / `helper-results.json` exercise the exact shipped script
  with DOM and storage doubles. Normal tests pass; R04 deliberately reproduces
  invalid Undo snapshots. This is not a real-browser test.
- `R04-damaged-undo.json` is a complete payload for localStorage key
  `caesarSoloDeck2`. Reload, then click Undo. The test also covers a valid-JSON
  snapshot with invalid side.
- `campaign_audit.py` imports `ObservedGame` from `replay_archive.py`; keep both
  in the same directory. `campaigns.json` contains 240 complete runs across ten
  level configurations and both bot/Heuristic directions. Seeds 810000–810019,
  820000–820019 and 830000–830019 are reused for matched comparisons. It checks
  strict 55-card accounting, units and VP and records Reserve lifecycle observations.
  There are 23,200 boundary checks, no exceptions or invariant failures, and 49 runs
  with partial replacement of a Surprise-only Reserve. These span 16 seed values;
  the levels are not independent samples. No immediate Reserve redraw was seen.
- `replay_archive.py` / `archive-replays.json` replay the first three games of all
  40 final-study cells: 120 configured runs using six distinct seed values. VP,
  ending reason, battles and sieges match in every case. They do not independently
  rerun all 5,300 games. Neither R01 nor R02 was observed in these prefix replays.
- `release_checks.py` / `release-checks.json` independently recount the 5,300 study
  outcomes, verify nine region-priority cases, run 1,165 opponent-hidden-identity
  perturbations of `choose_play` over 12 games, and compare complete traces for
  four seeds with repeat/changed VP targets. Hook behavior is not exhaustively
  covered by the hidden-identity check.
- `regression-results.txt` / `smoke-results.txt` contain the shipped suites' output:
  eight and five test functions, all passing. The scripts were run directly;
  pytest is not a dependency.
- `sample-seed57.md` exactly equals the archived raw sample. The edited booklet's
  play log/winter lines also match after whitespace normalization. Its editorial
  introduction and closing explanation are separate.
- `print_reaudit.py` / `print-results.json` check all 18 combined packet pages,
  all 18 individual card-face rectangles, face/back order, source-HTML generation,
  fixed appendix/reproduction wording and the helper's pinned Git bytes.
- `visual-review.json` and `rendered/` document visual inspection of all 37 unique
  product PDF pages. Both columns on both reference pages were inspected.
- `source-manifest.json` records the pinned source hashes and runtime versions.
  The publisher's rulebook is referenced by URL/hash, not redistributed.
- `render_report.py` generates the re-audit PDF from its Markdown source.

Python simulation tests use only the standard library. Print checks require
PyMuPDF, Markdown and pypdf; report generation additionally requires ReportLab,
Beautiful Soup and DejaVu fonts. Helper tests require Node.js, with no npm packages.
Exact versions are in the manifest.

The helper is authored standalone HTML, with no separate generator. Its bytes
match the reviewed Git blob. Regenerated print HTML contains a workspace-specific
base URL. PDF content checks and source HTML determinism do not certify a
byte-identical PDF rebuild. No local Chrome was usable, and this re-audit did not
complete an independent real-browser helper test.

No game-rule changes, production fixes or corrected win-rate estimates are
included. The full clean-room implementation and exact second-edition component
transcription remain outside this re-audit.
