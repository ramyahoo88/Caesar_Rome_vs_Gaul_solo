# Caesar: Rome vs. Gaul — v1.2 verification

**Imperator, Concilium and the Directive helper · 22 November 2026**

**Reviewed release:** v1.2, commit `a52079aceab888e1f44cf6a8099337b5fbc7f243`, repository `ramyahoo88/Caesar_Rome_vs_Gaul_solo`. Sources: the v1.1 audit response, v1.2 changelog, source diff, current rules/cards/helper, regenerated PDFs and archived experiments.

**Verdict: R01–R05 are fixed; one additional Medium simulation finding and one Low evidence-retention finding remain.** The R01–R03 regression tests requested in the update are already present in `code/tests/test_audit_fixes.py`. All 12 regression functions and five smoke functions pass, so no duplicate production tests were added.

The printed bot and helper changes pass the checks described here. Full simulation-to-paper fidelity sign-off remains pending R06. R07 limits independent checking of the AP experiment's saved summary; the AP-only engine option itself is correct. The effects of R06 on published win rates have not been measured. No production fixes or rule changes are included in this review.

## Closure of the previous re-audit

| Item | Verified behavior in v1.2 |
|---|---|
| R01 | Two- and three-Surprise hands are fully replaced. A mixed hand retains unrevealed #55 and discards revealed #55. The fresh 240-run sweep recorded zero partial all-Reserve replacements. |
| R02 | The seed-94 Gergovia case spends, reshuffles and redraws #52; the new draw is no longer in Reserve. Card-leaving notifications precede replacement draws at the reviewed Reaction, battle, siege, discard and transfer paths. Rules 1.3 state the lifecycle. |
| R03 | Vercingetorix alone with Local Support puts the Bibracte Legion in danger; removing that support makes it safe. The printed army definition now includes a leader alone. |
| R04 | Both damaged Undo examples are dropped at load. Mixed history retains its valid step. An additional use-time corruption test is safely skipped with a notice. Normal Undo still passes. |
| R05 | `ap_edition=1` changes card AP values while the game remains edition 2. All four native edition options and the initial board/deck/RNG state remain identical. All 55 cards' AP mappings were checked. |

The REGROUP tally code is visible on the record sheet. The sample's result now shares page 11 with the closing log, rather than occupying a page alone. The report presents its corrected comparison first and labels its older tables. Latest-change per-seed VP/win arrays are retained, and their paired statistics recount correctly. AP per-seed retention is the remaining exception, R07.

## R06 — Immediate extra card plays skip the #55 cleanup

**Severity: Medium · Simulation timing**

**Expected / player impact.** Bot rule 1.3 says a revealed #55 is discarded at the start of the bot's next card play and replaced. Rule 6.5 explicitly gives Concilium a new Directive and Offer when #42 grants an immediate play. The same start-of-play rule applies when an Event is canceled and the bot plays again. Delaying the discard changes replacement timing, the next Offer and available Reserve effects.

**Exact reproduction A — #42.** Run `nested_reserve.py`, fixture seed 0, using the normal seeded initial board. Replace the card distribution with Rome `[6, 45]`, Gaul `[55, 42, 47]`, all other cards in the draw pile in ascending order and no discards. #55 initially is face down. The test calls the regular Surprise-start handler before the first play, then uses the actual BotPolicy choices and Event implementation.

1. Gaul's first Offer reveals #55 into Reserve and chooses #42 as an Event.
2. #42 takes Roman #45 and immediately calls the next Gallic card play.
3. The second Offer starts with `[55, 47, 45]`, chooses #45, and leaves #55 in Reserve.

**Observed.** #55 is neither discarded nor replaced before that second Offer. It remains in the Gallic hand after both plays. Expected: discard #55 and draw its replacement before forming the second Offer. All 55 cards remain conserved, so a resource-count check does not catch this timing difference.

**Exact reproduction B — cancellation.** The second seed-0 fixture uses Gaul `[55, 21, 47]`, Rome `[24, 45]`, with Roman #24 already in Reserve. Gaul reveals #55 and plays #21; Rome cancels it. The immediate replacement play begins with Gallic `[55, 47, 53]` and again skips the #55 discard. A control through the ordinary strategy-loop start correctly discards a revealed #55.

**Full-game evidence.** The observer recorded the same missing cleanup in two of 100 fresh full games, seeds **950034** (Turn 6) and **950097** (Turn 4), with Imperator +1 AP against standard Concilium. It also appears in the archived final-study replay at **seed 200002**, Concilium versus Lookahead, Turn 4. That one trajectory repeats across Concilium levels 1–4, producing four affected configured replays; these are not four independent occurrences. This is descriptive evidence of occurrence, not a measured win-rate effect.

**Source.** The ordinary strategy loop calls `handle_surprises_start` at `code/engine.py:1665`. `card_play` at `:1710` proceeds directly to choosing the Offer. Both the #42 path at `code/events.py:255` and cancellation path at `code/engine.py:1740` call `card_play` directly. Expected printed wording: `print/Caesar_Solo_Rules.md:26` and `:322`.

**Smallest fix.** Ensure start-of-play Surprise processing runs exactly once before every actual new Offer, including immediate #42 plays and canceled-Event replacements. Centralizing that entry step would avoid callers bypassing it; remove or guard the ordinary-loop call so cleanup is not duplicated. Preserve the new Reserve-leaving notifications. Add both trigger cases, the normal-path control, and replacement-draw boundaries to the regression suite, then rerun affected evidence.

**Evidence.** `nested_reserve.py`, `nested-reserve-fixtures.json`, `nested-reserve-results.json`, and `archive-replays.json`. The fixture observer records hands and Reserve state around the real decisions; it does not override the card selection, Events or AP behavior.

## R07 — AP per-seed VP arrays are calculated, then omitted from the saved file

**Severity: Low · Evidence retention**

**Expected / impact.** The audit response says the latest-change and AP-only runs retain their per-seed results; that statement should accurately describe the saved artifacts. Retaining both AP-setting VP arrays permits independent recalculation of the paired mean and standard error without repeating the full experiment. The latest-change artifact retains them; the AP artifact does not.

**Exact reproduction / observed.** Run `check_experiments.py`, or read `code/ap_only.py:22` and `results/ap_only_check_v1.2.json`. The script builds `row['ap1']['vp']` and `row['ap2']['vp']`, computes the paired statistics, then deliberately replaces each AP-setting object with only `{'win': ...}` when saving. All three saved matchups contain win-rate summaries, the paired mean, SE and sample size, but no per-seed VP arrays.

**Source.** `code/ap_only.py:22`–`:23`; `results/ap_only_check_v1.2.json`; optional-suggestions statement in `audit/independent-v1.1/AUDIT_RESPONSE.md`.

**Smallest fix.** Correct the response's retention claim if the AP output is intentionally summary-only. To complete the suggested retention improvement, serialize the full `OUT` rows rather than stripping `vp`, record the seed range/settings, and regenerate the artifact. Per-seed winners/reasons would also support independent win-rate checking. This finding does not dispute the reported AP effect sizes. The corrected AP-only option closes the original R05 confounding issue.

**Evidence.** `check_experiments.py` and `experiment-checks.json` identify the saved keys for all three AP matchups and independently verify that the engine option leaves the other edition settings unchanged.

## Verification performed

| Check | Result and scope |
|---|---|
| Shipped suites | 17/17 functions pass: 12 regression, five smoke. R01–R03 are covered by four existing regression functions, including controls. |
| Fresh campaign sweep | 240 completed runs across all ten level configurations and both bot/Heuristic directions. Sixty seed values, matched across levels: 910000–910019, 920000–920019 and 930000–930019. |
| Accounting | 23,221 boundary checks pass; complete 55-card conservation after every campaign; no checked card, unit, shelter, eliminated-ID or VP-ledger failures. Zero observed partial Reserve replacements or immediate stale Reserve redraws. |
| Additional timing probe | 100 distinct seeds, 950000–950099, all full bot-versus-bot games. Two record R06. Card conservation passes. |
| Final-study archive | All 40 cells and 5,300 archived runs reconcile from VP, termination reason and each level's victory target. |
| Final-study spot replays | 120 configured runs, first three per cell. All stored VP, termination reasons, battles and siege counts match. Six distinct seed values, 100000–100002 and 200000–200002, are reused across configurations. |
| Latest-change evidence | All 18 cells' sample sizes, per-seed VP means and win rates recount. All 12 paired mean differences and standard errors recompute exactly within floating-point tolerance. |
| Latest-change spot replays | First two seeds of each of 18 cells: 36 configured runs on seeds 20000–20001. Every stored VP and win result matches the shipped engine/configuration. |
| Hidden-card dependency | 1,172 `choose_play` comparisons across 12 games, seeds 940000–940011, pass when opponent hidden identities, draw-pile order and game RNG are perturbed. This is not an exhaustive test of all hooks/states. |
| Determinism and VP target | Four seeds, 940020–940023, each run three times. Repeat runs match; changing the target leaves the full play trace and VP unchanged. All nine lagging-region cases also pass. |
| Helper | 216 draws with reload, unique nine-card cycles on both sides, 80 bonus boundaries, side counters, reshuffle/turn Undo, Turn-6 stop, storage notices and the expanded R04 recovery checks pass using DOM/storage doubles. |
| Sample | Seed 57 reproduces `results/sample_game_seed57.md` byte for byte. Edited booklet log/winter states also match after whitespace normalization. Gaul wins: Roman 11 VP, one battle, 13 siege rolls. |
| Printables | All 37 unique PDF pages visually inspected, including both columns on both reference pages. All 18 individual Directive faces match their source reminders inside each face's rectangle. All 18 packet pages' extracted text equals the corresponding individual PDF pages. Duplex order is R faces/backs, G faces/backs. |

The complete final study and full latest-change experiments were not independently rerun; the reconciliation and replays above state exactly what was checked. The 240-run sweep preceded the additional timing instrumentation; R06 frequency was measured in the separate 100-run probe and archived-prefix replays. No aggregate win-rate correction is claimed.

## Release identity and remaining limits

The helper is authored standalone HTML, with no separate generator. Its bytes match the pinned Git blob. SHA-256: `47d88bb1df00bf044d07824121495c8c924eaa9d703bdb909acaab9f65cb12f2`. Print source HTML regenerates deterministically in this workspace. A fresh Chrome PDF build, PDF byte-for-byte comparison and independent real-browser helper test were not completed because no usable local Chrome was available. The author's browser tests are not presented as this review's own tests.

This is a targeted release/fix verification, not a complete clean-room reconstruction. The disclosed second-edition Siege Table approximation and untranscribed exact card faces remain outside the verified model. No physical tabletop playtest was performed. No additional paper-rule or helper logic defect was confirmed in this review.

## Evidence and reproduction

Use a clean checkout of `a52079a`, keep the evidence scripts together outside it, and create `OUTPUT` first:

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

The R06 fixture assertions deliberately confirm the current defect; after repair they should assert cleanup before the second Offer. The R07 saved-key assertions describe the current summary-only format and should change if raw arrays are retained. The evidence includes full probe results, fixtures, source hashes, screenshots/contact sheets and runtime versions. See `evidence/README.md` for dependencies and interpretation.

**Release decision:** accept the R01–R05 repairs and retain their regression tests. Correct R06 before final simulation-fidelity sign-off and regenerate affected evidence. Resolve R07 by retaining the AP raw arrays or accurately documenting its summary-only output. The review does not require a change to the paper bot's intended rules or difficulty ladder.

All source line references use the [pinned release](https://github.com/ramyahoo88/Caesar_Rome_vs_Gaul_solo/tree/a52079aceab888e1f44cf6a8099337b5fbc7f243).
