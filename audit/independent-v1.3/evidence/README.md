# Caesar solo v1.3 verification evidence

Reviewed commit: `7c0d65c41b36de4c5cad96d7227b056d494685ff`.

Run from the repository root. The scripts accept an explicit repository path and
write only to the chosen output path. To reproduce against the reviewed release,
use a checkout of the pinned commit and obtain these audit scripts separately,
or use the audit-only descendant containing this directory (game sources match).

```sh
REPO="$PWD"
EVIDENCE="$REPO/audit/independent-v1.3/evidence"
OUTPUT=/tmp/caesar-v13-check
mkdir -p "$OUTPUT"
python3 code/tests/test_audit_fixes.py
python3 code/tests/test_smoke.py
python3 "$EVIDENCE/cleanup_checks.py" "$REPO" "$OUTPUT"
python3 "$EVIDENCE/replay_archive.py" "$REPO" "$OUTPUT/archive-replays.json" 3
python3 "$EVIDENCE/campaign_audit.py" "$REPO" "$OUTPUT/campaigns.json" 20
python3 "$EVIDENCE/release_checks.py" "$REPO" "$OUTPUT/release-checks.json"
python3 "$EVIDENCE/check_experiments.py" "$REPO" "$OUTPUT/experiment-checks.json"
python3 "$EVIDENCE/replay_latest.py" "$REPO" "$OUTPUT/latest-replays.json"
python3 "$EVIDENCE/replay_ap.py" "$REPO" "$OUTPUT/ap-replays.json" 3
node "$EVIDENCE/helper_reaudit.cjs" "$REPO" "$OUTPUT"
python3 code/sample_game.py 57 "$OUTPUT/sample-seed57.md"
python3 "$EVIDENCE/print_reaudit.py" "$REPO" "$OUTPUT/print"
python3 "$EVIDENCE/render_prints.py" "$REPO" "$OUTPUT/rendered"
python3 "$EVIDENCE/render_report.py" \
  "$EVIDENCE/../Caesar_Solo_v1.3_Verification.md" "$OUTPUT/report.pdf"
```

`cleanup-results.json` contains both original R06 positions, the normal-path and
same-play retry controls, and all 101 complete-game observations. The observer is
at the pre-Offer boundary after central cleanup, rather than before cleanup.

`campaigns.json` covers seeds 1010000–1010019 across five Imperator levels,
1020000–1020019 across five Concilium levels, and 1030000–1030019 in each of two
bot/heuristic directions. These are 240 configured runs on 60 distinct seed values.
`release-checks.json` uses seeds 1040000–1040011 for hidden-identity checks and
1040020–1040023 for full-trace deterministic/target controls.

`archive-replays.json` checks the first three seeds of every final-study cell:
100000–100002 and 200000–200002. `latest-replays.json` checks seeds 20000–20001
across 18 configurations. `ap-replays.json` checks 14000–14002 for both AP settings
in each of three matchups, taking the saved metadata as the input configuration.
All are matched replays, not independent fresh statistical samples.

`experiment-checks.json` contains the recount of all latest-change means, win
rates, paired differences and SEs, plus all retained AP outcome checks and the
AP-only scope check. Per-seed source outcomes remain in the release's `results/`.

`helper-results.json` runs the exact helper script with DOM/storage doubles and
in-memory test exports. The shipped HTML is never modified. This is not a browser
layout, keyboard, mobile or real storage-implementation test.

`print/print-results.json` records product PDF hashes, packet text equality,
per-card rectangle comparisons, source-HTML regeneration, sample equality and
helper Git-blob identity. `rendered/` contains all 37 unique product pages in
labelled contact sheets; `visual-review.json` records their inspection. The
landscape record sheet is fitted to its contact-sheet cell without cropping.

Simulation tests use the Python standard library; helper tests use Node.js with
no npm dependencies. Print checking additionally needs PyMuPDF, Python-Markdown
and pypdf. Rendering uses Pillow, ReportLab, Beautiful Soup and DejaVu fonts.
`source-manifest.json` records exact runtime versions and baseline source hashes.

The full study and full comparison/AP experiments were not independently rerun.
There was no fresh Chrome PDF build, independent real-browser test, complete
clean-room bot implementation, exact second-edition component verification or
physical playtest. See the report for the release verdict within these bounds.
