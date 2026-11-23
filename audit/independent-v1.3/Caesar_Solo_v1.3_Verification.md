# Caesar: Rome vs. Gaul — v1.3 verification

**Imperator, Concilium and the Directive helper · 22 November 2026**

**Reviewed release:** v1.3, commit `7c0d65c41b36de4c5cad96d7227b056d494685ff`, repository `ramyahoo88/Caesar_Rome_vs_Gaul_solo`. This review starts from the independent v1.2 report and the developer's response, then checks the release diff, the original failing positions, the refreshed evidence, the helper and the rendered printables.

**Verdict: R06 and R07 are closed. No new confirmed defects were found in this verification.** All 15 shipped audit regression functions and five smoke functions pass. The original extra-play positions now discard and replace revealed #55 before the next Offer. The AP experiment now retains enough data to recompute its win rates and paired statistics.

The reviewed fixes and the regenerated evidence pass within the existing model's documented scope. Exact second-edition components and a complete clean-room check of the latest bot text remain outstanding. This report adds verification artifacts only; it makes no game, rule or helper changes.

## R06 — Cleanup before every new card play

**Expected behavior.** Bot rule 1.3 requires a revealed Forced March (#55) to be discarded and replaced at the beginning of the bot's next card play. This includes the immediate play granted by #42 and the replacement play after an Event is canceled. Rule 6.5 gives #42's extra play a new Directive and Offer. A Surprise discard that retries the same play must not run a second start-of-play cleanup.

**Source review.** `code/engine.py:1709` now performs cleanup at the start of `card_play`. The outer strategy loop no longer performs it separately. Both `code/events.py:255` (#42) and the cancellation branch in `code/engine.py:1745` reach that same entry point. The Surprise retry at `code/engine.py:1728` passes `_retry=True` and skips the additional cleanup.

**Original position A — #42, seed 0.** Use the normal initial board, Rome's hand `[6, 45]`, Gaul's hand `[55, 42, 47]`, all other cards in ascending draw-pile order, and an empty discard pile. The first Gallic Offer reveals #55 and chooses #42 as an Event. After taking Rome's #45, the second Offer now begins with `[47, 45, 54]`: #55 has been discarded and replaced. In v1.2 that second Offer incorrectly still contained #55.

**Original position B — cancellation, seed 0.** Rome has `[24, 45]`, with #24 already in Reserve; Gaul has `[55, 21, 47]`. Use the same draw-pile convention. Gaul reveals #55 and plays #21 as an Event; Rome cancels it. The second Gallic Offer now begins with `[47, 53, 52]`, after #55 is discarded and replaced. Both fixtures conserve all 55 cards and call cleanup exactly twice across the two actual plays.

**Controls and campaign observation.** A normal strategy phase at seed 123 made 16 Offers and 16 cleanup calls. An intentionally forced Surprise-discard retry made two card choices, one cleanup and one counted card play; newly revealed #55 remained available within that same play. These controls verify both sides of the new timing boundary.

The 101 complete games used seeds 950000–950099 with Imperator's +1 AP, plus seed 200002 with the Roman lookahead opponent. None made a new Offer while a previously revealed #55 was still in hand. Observation happens at `choose_play`, after the new central cleanup; observing only entry to `card_play` would incorrectly flag the fixed implementation. The 120 archived study replays and the fresh 240-game sweep also recorded no missed cleanup.

**Evidence:** `evidence/cleanup_checks.py`, `cleanup-results.json`, `replay_archive.py`, `archive-replays.json` and `campaigns.json`. The new wording is present on rendered Rules page 1 and in the reference sheet's Reserve reminder.

## R07 — Saved AP experiment can be independently recounted

`code/ap_only.py:11` retains per-seed VP, winner and end reason for both AP settings. It also saves the half-open seed range, edition, options, policy configurations and AP override. At `code/ap_only.py:26`, serialization now preserves those rows instead of reducing them to win-rate summaries.

All 1,080 saved game outcomes have consistent counts, winners and terminal reasons. Recalculated win rates, paired Roman VP differences and standard errors match the artifact:

| Matchup | Pairs | AP1 minus AP2 Roman VP ± one SE |
|---|---|---|
| Imperator L3 vs Concilium | 300 | +0.1833 ± 0.1655 |
| Imperator L3 vs lookahead | 120 | +0.2500 ± 0.3545 |
| Concilium standard vs lookahead | 120 | +0.4417 ± 0.3919 |

An additional 18 full-game replays cover the first three seeds of all six matchup/AP combinations. VP, winner and end reason match every saved row checked. The AP-only option also retains the edition-2 initial board, deck, RNG state and all four native edition options; all 55 card AP lookups were checked. The exact second-edition AP assignments remain assumed, as the release discloses.

**Evidence:** `results/ap_only_check_v1.3.json`, `evidence/check_experiments.py`, `experiment-checks.json`, `replay_ap.py` and `ap-replays.json`.

## Broader regression and evidence checks

| Area | Result |
|---|---|
| Shipped tests | All 20 functions pass: 15 audit regressions and five smoke tests. Prior Reserve, danger, siege and card-conservation cases remain green. |
| Fresh games | 240 complete configured runs across every level and two purposeful heuristic matchups; 60 distinct seed values, reused for matched level comparisons. All 23,168 card-boundary/end checks pass for card conservation, unit state, shelter ownership, elimination IDs and the VP ledger. No stale Reserve redraw or partial all-Surprise replacement was observed. |
| Final study | All 40 cells and 5,300 archived outcomes reconcile to their saved win totals. Three seeds from every cell give 120 exact replays, matching VP, reason, battle count and siege count. These use six distinct seed values across the 40 configurations. |
| Latest changes | All 18 cells and 12 paired mean/SE comparisons recompute. Two seeds from every cell give 36 exact VP/win replays. |
| Decision checks | Nine independently specified lagging-region cases pass. Across 12 fresh games, 1,165 card-choice comparisons remain identical after hidden opposing-card identities and draw-pile order are changed. This checks the card-choice boundary, not a full proof of every policy method. |
| Determinism | Four fresh seeds reproduce complete log hashes. Changing only the VP target leaves the played trace and final VP unchanged in these cases. |
| Sample | Regenerating seed 57 matches `results/sample_game_seed57.md` byte for byte. The edited booklet's played log and winter lines agree. Gaul wins with Roman VP 11, correctly labelled Concilium level 4. |
| Helper | The exact shipped script passes 216 draw/reload checks, 80 level/bonus boundaries, reshuffle and turn Undo, Turn 6 stopping, separate side counters, corrupt-session recovery, corrupt-history filtering and the use-time Undo guard. These use DOM/storage doubles, not a real browser. |
| Printables | All 37 unique shipped PDF pages were inspected, including both columns of both reference pages. All 18 packet pages match the individual PDFs' extracted text. Each of the 18 card faces matches its own ID, name, compass, missions and full reminder text; faces and backs alternate correctly. |

The rendered simulation report includes the refreshed v1.3 tables, the paired SEs, the approximated Siege Table disclosure and readable reproduction commands using sample seed 57. The levels and win rates in the release summary agree with the archived study. The REGROUP tally code is present on the record sheet.

## Reproduction and limits

`evidence/README.md` lists commands for every check. Raw outputs, fixture logs, contact sheets, runtime information, source hashes and the report renderer are included. The evidence archive contains this report and the same supporting files. Existing game code was not modified during verification.

The complete 5,300-game study, complete 2,760-game latest-change experiment and complete 1,080-game AP experiment were not independently rerun. All their saved statistics were recounted; the explicitly numbered prefixes above were replayed against the pinned release. Matching these samples supports source/result consistency without proving every archived game was generated from this revision.

The helper is authored as a standalone HTML source, with no separate generator. Its SHA-256 is `c487dde93e4a46b5ad9478db6f9c204e975d6fefd25efd6a7dcd03e6fa65c5c3`, and its bytes match the pinned Git blob. Markdown-derived print HTML regenerates deterministically within this workspace. No fresh Chrome PDF rebuild or independent real-browser helper run was completed here, so byte-identical PDF reconstruction is not certified.

The simulation still approximates the second-edition Siege Table and assumes revised card AP assignments while using first-edition card text. The exact components and a full clean-room reconstruction of the latest rules have not been independently verified. No physical tabletop playtest was performed. These are existing scope limits; the reviewed R06/R07 fixes introduce no new unresolved finding.
