# Caesar: Rome vs. Gaul — v1.1 re-audit

**Imperator, Concilium and the Directive helper · 22 November 2026**

**Reviewed commit:** `dcbfc228a71d054940d43fc9b71ab6d22defbba7` on `ramyahoo88/Caesar_Rome_vs_Gaul_solo`. Review began with `audit/independent-v1.0/AUDIT_RESPONSE.md`, `CHANGELOG.md` and the complete changes since the v1.0 audit.

**Verdict: the original regression cases pass, but full rules/simulation sign-off remains on hold.** Five additional findings remain: four Medium and one Low. Three concern simulation fidelity, one concerns saved Undo history, and one concerns the AP sensitivity experiment. None is a High finding. The new evidence reproduces the remaining problems without changing production code.

The main final-study data are consistent with the shipped v1.1 engine: all 5,300 archived outcomes reconcile, and three games from each of the 40 cells replay exactly on VP, termination reason, battles and siege rolls. That establishes reproducibility of the current model. The remaining rule mismatches still require correction before treating its percentages as verified paper-bot performance. Their effect on the win rates has not been measured.

## Status of the previous findings

| Item | Verified result | Remaining scope |
|---|---|---|
| C01 | An unrevealed #24 no longer cancels; a revealed one does; turn changes clear eligibility. | Additional Reserve lifecycle cases R01 and R02. |
| C02 | Both original Aduatuci–Eburones SWEEP and REGROUP cases now respect the vacated route; the safe one-Legion control passes. | New threat-eligibility case R03. |
| C03 | Closed. Siege contributors are marked activated; the extra Legions cannot move again. Already activated CUs are still included in strength. | No further defect confirmed in this fix. |
| C04 | Closed. AP use discards #42; Event transfer conserves it. Both the release tests and independent campaign checks conserve all 55 cards. | The extra Event-path repair is supported by the current tests. |
| C05 | Invalid side, duplicate deck and malformed JSON now recover with a notice and preserved damaged payload. | Serialized Undo snapshots remain unchecked: R04. |
| C06 | Closed. The sample is labeled Imperator level 3 versus Concilium level 4, standard rules. | Seed 57 reproduces the archived raw log byte for byte. |
| C07 | Closed. REGROUP is present in the appendix, rendered rules page 11, and the other checked mission sequences. | Optional record-sheet improvement below. |
| C08 | Closed. Commands are preformatted, visible on report page 8, and specify seed 57. | Report formatting now preserves separate command lines. |
| Q1 | The printed wording clearly specifies #24 before replacing remaining Reserve Surprises, with an example. | Engine replacement of multiple Surprises still differs: R01. |
| Table | The Siege Table approximation is now stated in the summary and limitations. | Exact second-edition table/card transcription remains an acknowledged model limit. |

## R01 — A Surprise-only Reserve is only partly replaced

**Severity: Medium · Simulation / Q1 implementation**

**Expected and impact.** Bot rules 1.3 say that when only Reserve Surprise cards remain, the bot discards them, draws replacements and forms an Offer from the new cards. Keeping one changes the draw count, future card availability and available Surprise effects.

**Exact reproduction.** Run `targeted_reaudit.py`, seed 9. Rome holds only #52 and #54, both already in Reserve. Gaul holds #45. The draw pile's top two cards are #6 then #7; all other cards are discarded. All 55 cards are accounted for.

**Observed.** `handle_surprises_start('R')` leaves Rome holding `[54, 6]`, with #7 still on the draw pile. The expected replacement hand is `[6, 7]`. Only the first Surprise was discarded. The single-Surprise control replaces its card correctly.

**Cause and source.** `code/engine.py:1686` correctly enters the all-Surprise branch, but `:1690` repeats `len(sur) == len(h)` inside the mutation loop. Removing the first card shrinks `h`; the condition becomes false for the second card. The ordinary #54 discard policy is false, so #54 stays.

**Smallest fix.** Compute an `all_surprises` Boolean before mutating the hand and use that fixed value throughout the loop. Preserve the separate rule for discarding a revealed #55 from a mixed hand. Test two- and three-Surprise Reserves, mixed hands, and replacement draws that themselves contain Surprises.

**Evidence.** `targeted-results.json`, R01. The script reconstructs the complete card distribution and includes the opposite one-card control.

The instrumented fresh sweep also observed this failure in **49 of 240 runs**, spanning 16 seed values. Levels deliberately share seeds, so this is a count of affected matched runs, not an independent estimate of general prevalence. For example, Imperator L1, seed 810013, reaches Turn 3 with Gaul's Reserve hand `[54, 52]` and draws only one replacement.

## R02 — An immediately redrawn Reserve card keeps its old reveal status

**Severity: Medium · Simulation / C01 lifecycle**

**Expected and impact.** Rules 1.3 require a newly drawn Surprise or Reaction to remain face down until an Offer reveals it. A card that was spent and then immediately redrawn after a reshuffle must lose its earlier Reserve eligibility. Otherwise it can supply another effect before discovery.

**Exact reproduction.** `targeted_reaudit.py`, seed 94. Rome holds #52 and #45; #52 is in Reserve. Gaul holds #6–#13. The draw pile is empty and every other card is in the discard pile. Caesar and six full Legions attempt a siege at Gergovia against Arverni inside its Town. The fixture forces the siege dice to 2 to keep the position nonterminal.

**Observed.** The engine spends #52, reshuffles the discards and immediately draws #52 back. Rome's hand becomes `[45, 52]`. No new Offer has occurred, but `use_vow_siege()` still returns `True`: the replacement #52 is still treated as revealed. Card conservation passes; this is an information-state error.

**Cause and source.** `code/bots.py:1427` synchronizes Reserve by intersecting card IDs with the current hand. `code/engine.py:1281` consumes #52 and draws its replacement without clearing the Reserve entry. When the same ID returns immediately, the policy never observes its absence. The reshuffle/draw code is at `code/engine.py:1362`.

**Smallest fix.** Remove a Reserve entry when the card is actually consumed, discarded or transferred, before drawing a replacement. A later Offer may reveal the new draw again. Apply the lifecycle consistently to #24, #52, #54 and #55. Do not clear an entry merely while querying whether it would be used: the discard policy is queried more than once before commitment.

**Evidence.** `targeted-results.json`, R02. The reproduction performs an actual siege and confirms all 55 cards remain present. No claim is made about its frequency or win-rate effect in the full study.

## R03 — A Gallic leader alone is omitted from danger

**Severity: Medium · Simulation / danger eligibility**

**Expected and impact.** Bot section 3 forms a Gallic army from each named leader with up to its Command Rating of other CUs and explicitly counts the leader's own CS. Native rule 9.5.2 makes Vercingetorix and Ambiorix CS-1 Combat Units as well as leaders. A leader alone can therefore reach a target and receive Local Support. Omitting that army can suppress REGROUP or admit an unsafe Roman SWEEP.

**Exact reproduction.** `targeted_reaudit.py`, seed 31, Turn 5. Put Vercingetorix alone at Alesia and one full Roman Legion, CS 2, at Bibracte. Put Gallic IMs in every other Aedui space, so Gaul controls Aedui; remove other units, leaders and markers. Alesia → Bibracte is a one-MP path.

**Observed.** `gallic_armies()` correctly forms `(Vercingetorix, [], Alesia)`, but `threat_armies()` drops it because the accompanying-unit list is empty. The danger result is false. Expected: Gallic BS 1 + 2 Local Support = 3, versus Roman BS 2, exactly the 1.5 danger threshold. Removing Gallic province control is the opposite safe control.

**Source.** `code/bots.py:522`–`:526`, especially `if not units: continue`. Printed expectation: bot section 3; native 2023 rules, printed page 7, section 9.5.2. The original vacated-origin fix itself passes its regression cases.

**Smallest fix.** Keep a Gallic army whose leader is itself a CU even if it has no accompanying units. Retain the distinction for Roman named leaders, which have no CS. Check other threat builders for the same filter. Add the supported and unsupported leader-only cases, then verify both SWEEP safety and REGROUP triggers.

**Evidence.** `targeted-results.json`, R03. The route, province control, strengths and expected threshold are derived from the printed definitions rather than the threat result.

## R04 — Saved Undo history can still crash Undo

**Severity: Low · Helper / remaining C05 coverage**

**Expected and impact.** Restored history should contain usable snapshots, or recovery should discard/reject the damaged history with a notice. The current top-level recovery works for the original bad-side/deck/JSON examples. A damaged history can still make Undo throw or corrupt the current in-memory side.

**Exact reproduction.** Load `R04-damaged-undo.json` into localStorage key `caesarSoloDeck2`, reload, and press Undo. It is otherwise a normal new-state object with `prev: ["not JSON"]`. The runnable VM test also supplies a valid-JSON snapshot whose side is `invalid`.

**Observed.** Startup accepts both sessions. Undo throws a JSON parse error for the first; the second sets the current side to `invalid` and throws `Cannot read properties of undefined (reading 'NaN')` during rendering. Normal generated Undo snapshots, including Next turn and reshuffle, passed.

**Source.** `print/Caesar_Solo_Deck.html:146` checks only that each history entry is a string. `:185` parses and assigns it without validation or an error handler.

**Smallest fix.** Parse and validate every restored snapshot against the snapshot schema before accepting it. Guard Undo itself, preserve recovery data and explain when unusable history is discarded. Validate before assigning fields to the live session.

**Evidence and limit.** `helper_reaudit.cjs`, `helper-results.json`, R04. This independently executes the exact shipped script with DOM/storage doubles. It is not a real-browser reproduction.

## R05 — The AP sensitivity check changes several other rules

**Severity: Medium · Evidence / experiment design**

**Expected and impact.** Simulation-report section 9 presents the edition comparison as changing the card AP values. To estimate that effect, every other rule must remain fixed. The current comparison cannot isolate whether the assumed AP assignment matters.

**Exact reproduction.** Run `targeted_reaudit.py`, R05. Inspect `code/ed1b.py:4`–`:7`: it passes `edition=ed` to all three matchups. `Game(..., edition=1)` and `edition=2` differ in these non-AP options:

| Rule parameter | Edition 1 → edition 2 |
|---|---|
| Siege Table shift | 0 → −1 |
| Siege-roll movement cost | 3 MP → 2 MP |
| Stronghold points required | 2 → 3 |
| Friendly Interception/Avoid modifier | +2 → +1 |

**Observed.** These four options change along with AP values. The report's numerical sensitivity results measure the combined settings. The main final study consistently uses edition 2; this finding concerns the interpretation of the sensitivity experiment.

**Source.** `code/ed1b.py:5`–`:7`; `code/engine.py:182`–`:183`; `print/Caesar_Solo_Sim_Report.md`, section 9.

**Smallest fix.** Either relabel the result as a combined edition-settings comparison, or rerun an AP-only comparison with siege cost, table shift, Stronghold points and the friendly modifier held at the edition-2 settings. A dedicated AP-value override would make the experimental boundary explicit. Update the report, generator text and affected PDF together.

**Evidence.** `targeted-results.json`, R05, records all four actual option differences. No new sensitivity percentages have been invented.

## Verification evidence and limits

| Check | Result |
|---|---|
| Release regressions and smoke tests | All 13 test functions pass: eight audit-fix regressions and five smoke checks. |
| Fresh campaign sweep | 240 runs across all ten level configurations and both bot/Heuristic directions. Sixty distinct seeds, matched across levels: 810000–810019, 820000–820019, 830000–830019. |
| Resource/accounting checks | 23,200 boundary checks; no failures. Strict card uniqueness/conservation while active, complete 55-card conservation after each campaign, valid units/shelter, unique eliminated IDs and balanced VP ledger. This accounting does not test whether Reserve replacement timing follows the rules. |
| Reserve observations in fresh sweep | R01 occurs in 49 runs, spanning 16 seed values. No immediate Reserve redraw was observed; the separate seed-94 fixture confirms R02. |
| Published study reconciliation | All 40 cells and 5,300 archived runs reconcile from terminal reason, VP and the level's target. |
| Archived-game replay | 120 runs: first three from every cell; six distinct seed values, 100000–100002 and 200000–200002, reused across configurations. VP, reason, battles and sieges match exactly in every replay. |
| Hidden-card dependency | 1,165 card-choice comparisons in 12 complete games, seeds 840000–840011, pass when opponent hidden identities, draw-pile order and game RNG are perturbed. Scope: `choose_play`, not all hooks/all possible states. |
| Determinism and targets | Seeds 840020–840023, three runs each. Identical target-12 runs match; changing to target 10 leaves the play trace and VP unchanged. |
| Lagging region | All nine hand-derived tie/lead cases pass. |
| Sample | Seed 57's raw file exactly matches `results/sample_game_seed57.md`. The edited booklet's play log and winter lines match after whitespace normalization. Rome wins with 12 VP, zero battles and 12 siege rolls. |
| Helper normal paths | 216 draws with reload after every draw, complete nine-card cycles, both sides, 80 bonus boundaries, independent counters, reshuffle Undo, Next-turn Undo, Turn-6 stop and storage-failure notice pass. |
| Printables | All 37 unique PDF pages visually inspected, including both columns on both reference pages. Each of 18 Directive faces checked in its own rectangle. All 18 combined-packet page texts equal their individual-PDF counterparts. |

The archive reconciliation and spot replays do not constitute an independent rerun of the entire final study. The latest-change comparison configuration and reported values were reviewed; its full aggregate experiment was not independently replayed. Remaining finding impact is unmeasured. The 120 archived-prefix replays did not trigger R01 or R02; targeted states do reproduce them.

The helper is authored standalone HTML; there is no separate generator to rebuild it. Its bytes match the pinned Git blob, SHA-256 `0f254e5654b0696ce384ad25d29e9a2dabc95ee30f8f6dddc1c5c9d27cd8be6b`. Print source HTML regenerates deterministically in this workspace. **A Chrome PDF rebuild, PDF byte-equality comparison and independent real-browser helper test were not completed:** no usable local Chrome was available. The author's headless-Chrome statement is not presented as this review's own browser test.

This remains a targeted independent re-audit, not a complete clean-room implementation. Exact second-edition Siege Table cells and card faces remain unverified; the new disclosure is accepted. Session export/import remains an optional enhancement, not a release defect.

## Optional usability and reporting improvements

* Add a REGROUP tally code to the record sheet so the new survival mission can be logged directly.
* Keep the sample's final result on the preceding page; current page 11 contains only that short result paragraph.
* Make section 6's introduction match its actual order: corrected comparison first, development tables afterward. Narrow the “every result in sections 6–8” statement to the rerun results, since the section deliberately retains older tables.
* Preserve per-seed outputs for future latest-change and AP sensitivity runs, and report uncertainty for paired differences. Aggregate means alone do not show how stable small gains are.

## Evidence and rerun instructions

The evidence archive contains the runnable cases, complete fresh-sweep results, archive replays, trace checks, helper tests, print checks, raw sample, PDF contact sheets and pinned source hashes. Output fixtures are diagnostic summaries except for the helper's localStorage payload. No production fixes are included.

Using a clean checkout of the reviewed commit, with the evidence scripts outside that checkout and `OUTPUT` created first:

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

The focused reproducers assert the remaining defective baseline behavior. After a fix, change the affected assertion to the printed expected outcome. See `evidence/README.md` for dependencies and exact scope.

Native source: GMT Games, *Caesar: Rome vs. Gaul*, second-edition rules, 2023-1d, printed page 7, section 9.5.2. [Publisher PDF](https://gmtwebsiteassets.s3.us-west-2.amazonaws.com/CaesarRomeVSGaul/2nd+Edition/CAESAR-RULES-2023-1d.pdf). SHA-256: `2289f25a7c421dd27175c108609e9df6c19bd5fea757d0134c1af308987a9a70`. The publisher PDF is not redistributed in the archive.

All source lines refer to [commit dcbfc22](https://github.com/ramyahoo88/Caesar_Rome_vs_Gaul_solo/tree/dcbfc228a71d054940d43fc9b71ab6d22defbba7). **Release decision:** patch R01–R04, correct or rerun the R05 experiment, update the audit response and regenerate affected evidence before full sign-off. No bot rules, gameplay code, helper or published study was modified by this review.
