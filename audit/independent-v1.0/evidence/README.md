# Caesar solo v1.0 independent-audit evidence

Baseline: `3e8dbac8d2d0bc8bf4e4e8919574ff593d3ea406`, reviewed 22 November 2026.

These scripts do not modify the bot, engine, helper or study. Run them against a
separate clean checkout of that baseline. Their diagnostic assertions deliberately
confirm defects in the baseline; they are not assertions that corrected code
should retain.

## Runtime

- Python 3.12.14; simulation/focused/release scripts use the standard library.
- Node.js for `helper_audit.cjs`; no npm dependencies. It uses the exact helper
  script in a VM with DOM and localStorage doubles, not a browser.
- Print checking: PyMuPDF 1.26.6, pypdf 6.21.4, Markdown 3.11.3.
- The audit PDF uses ReportLab 4.4.9. This is not the product's PDF build path.

## Run

Replace `REPO`, `EVIDENCE` and `OUTPUT` with absolute paths; create `OUTPUT` first.
Keep generated results outside `REPO`.

```sh
python3 EVIDENCE/focused_rules.py REPO OUTPUT
python3 EVIDENCE/campaign_audit.py REPO OUTPUT/campaigns.json 20
python3 EVIDENCE/release_checks.py REPO OUTPUT/release-checks.json
node EVIDENCE/helper_audit.cjs REPO OUTPUT
python3 EVIDENCE/print_audit.py REPO OUTPUT/rebuilt-html
python3 REPO/code/tests/test_smoke.py
python3 REPO/code/sample_game.py 47 OUTPUT/sample-seed47.md
```

The campaign sweep takes about one minute on four processes in this runtime.
Its 240 runs use 60 seed values, matched across level configurations. It records
missing #42 explicitly and permits **only** that known card-conservation exception
so later unit and score checks can finish. A zero exception count does not mean
card conservation passed. See each record's `card_issues` array.

The full published 5,300-game study was reconciled from archived data, not rerun.
`release_checks.py` also runs 12 games with opponent-hidden-identity perturbations
at every `choose_play` and 12 trace-comparison games (four seeds, three runs each).
Those checks do not reconstruct every decision independently from printed prose.

## Files

- `focused_rules.py`, `focused-rules-results.json`, `focused-console.txt`: C01–C04
  and the Caesar 2:1 siege eligibility control. C02 contains both SWEEP and REGROUP
  cases and an opposite safe control.
- `C01-*.json` through `C04-*.json`: diagnostic snapshots. They are not importable
  helper saves; `focused_rules.py` recreates the positions.
- `campaign_audit.py`, `campaigns.json`: full 240-run sweep and accounting.
- `release_checks.py`, `release-checks.json`: 5,300-run archive reconciliation,
  nine text-derived region cases, 1,177 hidden-identity comparisons and four
  repeated-seed/VP-target trace checks.
- `helper_audit.cjs`, `helper-results.json`: first launch, complete deck cycles,
  reload, Undo, bonus boundaries and damaged-session behavior.
- `C05-damaged-session.json`: payload for localStorage key `caesarSoloDeck`.
- `print_audit.py`, `print-results.json`: PDF inventory/hashes, all 18 packet-page
  text comparisons, per-face card checks, source HTML regeneration and C06–C08.
- `sample-seed47.md`: regenerated current sample. The shipped version has added
  editorial introduction and normalized list indentation; the play log and winter
  state lines agree after trimming whitespace. Result: Rome 13 VP, one battle,
  ten siege rolls, six Tribes eliminated, zero Legions still eliminated.
- `sample-seed45.md`: the seed incorrectly specified in the published report's
  reproduction instructions. Result: Gaul, Roman 9 VP.
- `smoke-results.txt`: existing release smoke-suite output.
- `rendered/`: contact sheets of all 36 unique product PDF pages, visually reviewed.
  Packet pages duplicate the Rules, Reference, Cards and Record Sheet.
- `source-manifest.json`: pinned source hashes, official rulebook URL/hash and
  runtime versions. The publisher's original rulebook is not redistributed.

The helper is authored standalone HTML; no independent helper generator exists.
Its bytes match the reviewed Git blob. Regenerated print HTML includes an absolute
base URL, so its hashes are workspace-specific. PDF text/content checks and source
HTML determinism do **not** certify a byte-identical PDF rebuild. No usable local
Chrome was available, and no real-browser UI test was completed.

No production fix or corrected win-rate estimate is included in these files.
