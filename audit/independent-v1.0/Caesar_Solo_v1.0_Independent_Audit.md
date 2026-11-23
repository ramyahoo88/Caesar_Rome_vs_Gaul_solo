# Caesar: Rome vs. Gaul — independent audit

**Imperator, Concilium and the offline Directive helper · 22 November 2026**

**Release reviewed:** version 1.0, repository `ramyahoo88/Caesar_Rome_vs_Gaul_solo`, main commit `3e8dbac8d2d0bc8bf4e4e8919574ff593d3ea406`.

**Verdict: hold the v1.0 release sign-off for a patch and corrected simulation runs.** Eight confirmed findings remain: one High, three Medium and four Low. Four affect the simulation's fidelity to the printed bot or native rules. The arithmetic behind the published results checks out; that does not establish that the simulated games represent the paper bots correctly. The direction and size of any win-rate changes are unmeasured.

The paper bots remain usable with the native game. Their main printed mission sequence and cards agree apart from one appendix omission, and the optional helper draws the correct Directive decks. This review does not recommend more strength tuning before correcting the simulation defects.

## Findings at a glance

| ID | Severity | Affected part | Confirmed issue |
|---|---|---|---|
| C01 | High | Simulation / evidence | Reactions and Surprises can be used before they are revealed into Reserve. |
| C02 | Medium | Simulation / latest bot changes | Danger uses the board before movement, missing routes opened by vacating the origin. |
| C03 | Medium | Native rules engine | Extra CUs contribute to a siege and remain available for another activation that card. |
| C04 | Medium | Native rules engine | Card #42 disappears from the game when played for AP. |
| C05 | Low | Offline helper | Syntactically valid but damaged saved sessions can crash startup or duplicate the Directive deck. |
| C06 | Low | Sample game | Concilium is labeled level 3 while using standard, level-4 settings. |
| C07 | Low | Printed rules | The Directive appendix omits the mandatory REGROUP mission. |
| C08 | Low | Simulation report / print build | Reproduction commands collapse in the PDF and specify the wrong sample seed. |

Severity describes impact within this release. C01 is High because the study compares a different Reserve policy from the published paper bot, undermining the strength evidence. It is not evidence that a bot reads the human player's hidden hand.

## What was checked

The review used the shipped rules, reference sheets, all 18 Directive faces, record sheet, sample, simulation report, helper, current simulation code and previous audit responses. Native timing expectations were checked against GMT's 2023 second-edition rulebook, including its original two-column layout. The latest danger, REGROUP, lagging-region and Caesar 2:1 siege changes received targeted independent cases. This is not a complete second implementation of both bots from prose.

| Check | Result and practical limit |
|---|---|
| Published final study | All 40 cells reconcile: 5,300 campaign runs, matching array lengths and independently recounted winners from terminal reason, VP and each level's target. This verifies archived totals, not every historical game. |
| Existing smoke suite | All four test functions pass. They do not test Reserve discovery, siege contributor activation or card conservation. |
| Fresh campaign sweep | 240 completed runs across all ten level configurations and both bot-versus-Heuristic directions; 60 distinct seed values, deliberately reused for matched level comparisons. Seeds: 710000–710019, 720000–720019 and 730000–730019. |
| Accounting during that sweep | 23,146 boundary checks. Every run recorded missing card #42. After recording that known exception, there were no other checked card, unit-location, shelter, eliminated-ID or VP-ledger failures, and no campaign exceptions. |
| Hidden-card dependency | 1,177 card-choice comparisons in 12 complete games, seeds 740000–740011. Replacing opponent card identities while preserving hand size, reversing the draw pile and changing the game RNG did not change the chosen card/mode. This covers `choose_play`, not all reaction hooks or all possible states. |
| Repeatability and VP targets | Four seeds, 740020–740023, each run three times. Identical target-12 runs matched, and changing the target to 10 left the complete play trace and VP unchanged. |
| Latest Control Table | Nine hand-derived Celtica/Belgica cases pass, including both regions lagging and tied lead margins. |
| Latest Caesar siege rule | A zero-Siege-Point, 2:1 Caesar siege is accepted, as the text requires. |
| Helper | Exact shipped JavaScript tested with DOM/storage doubles: 216 draws, reload after each draw, unique nine-card cycles, reshuffle Undo, and 80 bonus boundaries. Both nine-card arrays match the print data. This was not a real-browser test. |
| Rendered printables | All 36 unique PDF pages inspected, including both reference-sheet columns. All 18 packet pages have exactly the same extracted text as their individual PDFs. Each Directive's ID, name, compass and complete mission reminders were checked inside its own face rectangle. |
| Sample | Seed 47 reproduces the 13-VP Rome win, card/action log and winter states after whitespace normalization and excluding editorial introduction/result wording. It retains the simulation defects reported here. |

### Release build verification

The helper is authored standalone HTML, not generated output: the repository has no separate helper build to reproduce. Its local bytes equal the pinned Git blob. SHA-256: `5e6d37aa3478f60349d4fbac9dcd20a0eeb7fcdd50b4345c70417f5858ae7f96`.

The print builder regenerated its Markdown/card source HTML to a separate output directory and reproduced that HTML on a second call. The PDF content, packet assembly and card text checks passed subject to C06–C08. **A fresh Chrome PDF build and byte-for-byte PDF comparison were not completed:** this environment had no usable local Chrome, and obtaining the browser was blocked. No claim of byte-identical PDF rebuild or real-browser UI sign-off is made.

## C01 — Reserve cards are available before discovery

**Expected / player impact.** Bot rules 1.2–1.3 and 2.2 keep the bot's hand face down. A Reaction or Surprise enters its face-up Reserve when encountered while revealing an Offer. Unrevealed cards cannot supply the Reserve effects. Earlier cancellation and surprise availability can change both sides' results and the claimed agreement between paper and simulation.

**Reproduction.** `focused_rules.py`, seed 9, fixture `C01-unrevealed-reaction.json`: Rome holds #24 and #45; Gaul plays #6 as an Event. Rome has never drawn a Directive or revealed an Offer; `directive` is `None` and `reserve` is empty.

**Observed.** The log records `T1 R cancels #6 with #24`. No Roman Offer occurred. Source review confirms that the Reserve list is initialized but never populated or consulted. Card selection filters the whole hand to exclude Surprises and #24, and reaction/surprise hooks inspect eligibility without discovery state.

**Source.** `code/bots.py:96`, `:119`, `:124`, `:1343`; `code/engine.py:1720` and `:1276`; printed expectation at `print/Caesar_Solo_Rules.md:19`.

**Smallest fix.** Track the unrevealed hand and face-up Reserve separately in the policy. Encounter special cards while revealing the two-card Offer; only discovered Reserve cards may trigger their hooks. Preserve replacement and discard timing. Add a pre-first-Offer cancellation test and equivalent #52/#54 cases, then rerun the affected study. Do not infer a revised win rate from the current data.

## C02 — Danger misses paths opened by the move itself

**Expected / player impact.** Bot section 3 defines danger where an army would end its move, using the opponent's next activation. Sections 5.1 and 5.3 require a safe REGROUP destination and forbid a non-exempt SWEEP into danger. A move can remove the army that presently blocks an enemy path. The current implementation may raid or retreat into an attack the printed bot would reject.

**Reproduction A.** In `C02-danger-before-move.json`, put reduced Remi (CS 3) at Aduatuci, two full Roman Legions (CS 4 total) at Menapii and a Roman IM at Eburones; remove other units, leaders and markers. Concilium plans Aduatuci → Eburones and removes the IM. The static Roman threat at Eburones is 0. After Remi vacates Aduatuci, the legal Roman route Menapii → Aduatuci → Eburones costs 3 MP. Roman BS 4 is at least Gallic BS 3, so the destination is dangerous. Removing one Roman Legion gives the opposite, safe control case.

**Reproduction B.** In `C02-regroup-before-move.json`, put full Arverni (CS 7) at Menapii, Legion VII at Aduatuci and another full Legion at Eburones. Imperator REGROUPs VII to Eburones. The vacated route allows the Arverni to reach the joined Roman BS 4 at a ratio of 1.75, above the 1.5 danger threshold.

**Source.** Threat maps: `code/bots.py:501` and `:522`; REGROUP: `:582`; SWEEP: `:703` and `:706`. Expected wording: `print/Caesar_Solo_Rules.md:79`, `:120`, `:169`.

**Smallest fix.** Evaluate candidate safety on the prospective board: relocate the moving army, vacate its origin, apply the intended IM removals and recalculate enemy reach and local support. Preserve the mission's fixed initial RAID weights. Check both Roman and Gallic cases and multi-step SWEEPs. Re-run the danger/REGROUP comparisons after correction.

## C03 — Siege contributors can activate twice

**Expected / player impact.** Native rule 14.3.2, Step 1, printed page 13, includes all friendly CUs at the siege location in the attack strength, including previously activated CUs. Any previously unactivated contributor becomes unavailable for another activation that card. The simulation gains extra movement or attacks by counting those units for the siege without consuming their activation.

**Reproduction.** `focused_rules.py`, seed 11, `C03-siege-contributors.json`: Caesar and eight full Legions stand outside the Arverni Fortified Town at Gergovia; Arverni are inside. Activate Caesar with six Legions for one siege attempt. The fixture forces the dice to 2 to keep the position available for inspection.

**Observed.** All eight Legions contribute strength. Only the selected six become moved. XIII and XIV remain unmoved, and the engine accepts a second, leaderless activation taking both to Boii on the same card.

**Source.** `code/engine.py:1250` replaces the selected units with all outside friendly CUs; the valid siege paths at `:1257` and `:1267` do not consume the extra contributors. Activation eligibility is checked at `:719`. Native source: GMT 2023 second-edition rulebook, 14.3.2.

**Smallest fix.** When a legal siege attempt commits, mark every contributing CU as activated. Already activated CUs must remain eligible to contribute. Check consistent subjugation/surrender handling and test a same-card second activation of the extra contributors.

## C04 — Card #42 vanishes when spent for AP

**Expected / player impact.** A Strategy card spent for AP enters the discard pile. #42's special transfer to the Roman hand applies when its Gallic Event is actually executed. Losing a card changes later reshuffles and card availability.

**Reproduction.** `focused_rules.py`, seed 3, `C04-card42-for-AP.json`: Rome has only #42, Gaul has #6, and the remaining 53 cards are in the deck. Use an AP-only policy. A paired control spends #45 the same way.

**Observed.** After Rome plays #42, it is absent from both hands, the deck and the discard pile: only 54 cards remain. The #45 control has all 55 cards. The campaign checker recorded the #42 loss in all 240 sweep runs; it explicitly allows only this known exception before continuing the other invariants.

**Source.** `code/engine.py:1736` skips discard for every use of #42, regardless of mode. Card transfer belongs to the Event path in `code/events.py`.

**Smallest fix.** Skip discard only when the resolved Event actually transfers #42 to Rome. Cover Roman AP, Gallic AP, successful Event transfer and cancellation/nested-play paths without duplication. Add card-conservation checks at complete card-play boundaries and rerun the study.

## C05 — Damaged helper sessions are trusted

**Expected / player impact.** Reloading stored state should recover a usable helper or explain that the session cannot be restored. Invalid state should not silently change the Directive deck. This finding requires altered/damaged stored data; normal-session reload testing passed.

**Reproduction.** Store `C05-damaged-session.json` under localStorage key `caesarSoloDeck` and reload. It is a syntactically valid saved state with `side` changed to `invalid`. The runnable VM test also changes the Roman deck to nine copies of index 0.

**Observed.** Invalid side causes startup error `Cannot read properties of undefined (reading 'NaN')`. The duplicate deck is accepted and draws I-1 nine times. There is no recovery message. Confirmed by the exact shipped script with DOM/storage doubles; not reproduced in a real browser in this environment.

**Source.** `print/Caesar_Solo_Deck.html:129`–`:131`, consumed by `:138` onward.

**Smallest fix.** Validate side, level ranges, turn/play bounds, deck indices and uniqueness, current card and history before accepting a saved state. Retain a recoverable copy and offer a clear reset when invalid. Add startup recovery and duplicate-deck regressions.

## C06 — The sample's Concilium level is mislabeled

**Expected / player impact.** Bot section 7 gives Concilium level 3 a Roman target of 11 VP; standard 12 VP is level 4. Readers should be able to reproduce the stated sample settings.

**Reproduction / observed.** Run `sample_game.py 47` with an output path. The generator passes only `ap_bonus_R=1`, leaving the target at 12, while its title and the shipped sample say Concilium level 3. The resulting 13-VP Roman win reproduces, so the winner is unaffected by this labeling issue.

**Source.** `code/sample_game.py:32` and `:35`; `print/Caesar_Solo_Sample_Game.md:1`–`:3`, rendered PDF page 1. Ladder: `print/Caesar_Solo_Rules.md:336`–`:337`.

**Smallest fix.** Label the current sample “Imperator level 3 vs Concilium level 4 (standard rules)” and regenerate its PDF, or generate a new actual level-3 sample with `vp_target=11` and update its narration. A later regeneration must also incorporate C01–C04's corrected engine.

## C07 — REGROUP is missing from the appendix

**Expected / player impact.** Section 2.5, reference sheet, Roman card footers and helper require CONTINUE, PROTECT, SUBMIT, REGROUP before Directive missions. A player using the appendix alone can omit the new survival mission.

**Reproduction / observed.** Read the sentence immediately following the Imperator Directive table, rules PDF page 10. It ends the pre-mission list at SUBMIT.

**Source.** `print/Caesar_Solo_Rules.md:369`; correct main sequence at `:53`.

**Smallest fix.** Insert REGROUP after SUBMIT in the appendix and rebuild the Rules PDF and combined Print-and-Play PDF. Check all repeated mission lists, not merely whether REGROUP appears somewhere in each document.

## C08 — Printed reproduction instructions fail to reproduce the sample

**Expected / player impact.** Simulation-report section 10 should show separate executable commands and the seed of the shipped sample. A reviewer following it should regenerate the same example.

**Reproduction / observed.** Read simulation-report PDF page 7. The three command lines are collapsed into one paragraph. The generated HTML contains inline `<code>` rather than a `<pre>` block because fenced-code support is absent. The command also specifies seed 45, which produces a 9-VP Gaul win; the shipped example is seed 47, a 13-VP Rome win.

**Source.** `print/build.py:44`; `print/Caesar_Solo_Sim_Report.md:200`–`:204`; actual sample seed at `print/Caesar_Solo_Sample_Game.md:3`.

**Smallest fix.** Enable Markdown's `fenced_code` extension, preserve preformatted command lines, use seed 47 and regenerate the report PDF. Explain that the sample's introduction and narrative are editorial additions, so a raw generator output will not be byte-identical to the edited booklet.

## Unresolved fidelity limits and wording question

**Exact second-edition tables and deck are not certified.** The engine defaults to a first-edition Siege Table with `siege_shift=-1` for edition 2 (`code/engine.py:182`, `:1275`). The old engine audit acknowledges this approximation. The current simulation report prominently says it plays complete second-edition games, but its limitations do not plainly identify this siege-table approximation. The AP assignment and first-edition Event text assumptions are disclosed. AP sensitivity runs do not validate a different Siege Table. Obtain the actual revised table and card faces, transcribe them with provenance and compare every cell/card before presenting the figures as exact second-edition evidence. This is a known model limitation, not a newly proven incorrect table cell.

**Native-book inconsistencies need provenance.** The 2023 PDF contains stale siege-MP wording in section 14.3 while the second-edition movement/change material specifies 2 MP. The bots use 2 MP; no defect is assigned for that. The 2023 body/index disagreement about Fading Promises was already documented in the prior engine response; this audit does not silently resolve it. Retain an explicit rules-assumptions list.

**Q1 — last card versus last playable card.** Section 1.3 lets #24 be spent for AP only as the bot's “last card,” while Reserve Surprises still count as hand cards. It does not clearly resolve a Reserve containing #24 plus #52 or #54 and no ordinary card. The implementation instead says “last playable card.” Clarify whether #24 is playable when it is the only non-Surprise card, and exactly when the remaining Surprises are replaced. Add a worked case. This is a wording/sequence question, separate from C01's confirmed premature reaction.

## Optional quality-of-life improvements

These are recommendations, not additional release-blocking defects.

| Rank | Recommendation | Reason / observed behavior |
|---|---|---|
| 1 | Add session export/import and a visible autosave-failure notice. | Storage write failures are swallowed. In the blocked-storage test, no state is saved and no warning appears. |
| 1 | Preserve Undo across Next turn, or confirm and offer an immediate reversal. | Next turn clears all Undo history. An accidental advance is not recoverable through Undo. On Turn 6 it clears the current turn while leaving the display at 6. |
| 1 | Give each selected opponent a separate session counter, or explicitly reset when switching. | Decks and levels are separate but the card-play counter is shared. After four Roman draws, the first Gallic draw is numbered 5 and gets no level-5 first-four bonus. Midgame side switching is not documented, so this is classified as usability. |
| 2 | Show 0 cards remaining and “reshuffle on next draw.” | After the ninth card, the internal deck is empty but `length || 9` displays 9. Draw/reshuffle itself works. |
| 2 | Repeat the AP-only/Bonus-card and #4 exception on the first-four bonus reminders. | Levels R2/G5 omit the qualifier shown for permanent Roman bonus levels. |
| 2 | Include the full lagging-region tie rule and an offline rules/Event Guide view. | The short Control Table panel omits the both-lagging comparison. The helper works best when these decisions do not require another file. |
| 2 | Add a danger/REGROUP worked example showing the vacated origin. | Enemy reach and combined destination strength are the heaviest new tabletop calculations. |
| 3 | Explain duplex page pairing or reorder face/back sheets. | Current card PDF order is Roman faces, Gallic faces, Roman backs, Gallic backs. Ordinary sequential duplex printing does not pair the matching sides. No duplex compatibility claim was found. |

One logged tabletop game at level 3 against each bot remains valuable after patching and rerunning the evidence. It can measure decision burden, clarity and human challenge; computer win rates do not establish those properties.

## Evidence and rerun instructions

The accompanying evidence directory/ZIP contains the four executable audit scripts, helper VM tests, complete 240-run output, focused fixtures, archive reconciliation, repeatability hashes, print checks, rendered contact sheets and a source manifest. Fixtures are diagnostic state summaries; the Python script reconstructs them. They are not importable helper saves except for C05's localStorage fixture.

From a clean checkout of the reviewed commit, using the evidence scripts outside that checkout:

```sh
python3 EVIDENCE/focused_rules.py REPO OUTPUT
python3 EVIDENCE/campaign_audit.py REPO OUTPUT/campaigns.json 20
python3 EVIDENCE/release_checks.py REPO OUTPUT/release-checks.json
node EVIDENCE/helper_audit.cjs REPO OUTPUT
python3 EVIDENCE/print_audit.py REPO OUTPUT/rebuilt-html
python3 REPO/code/tests/test_smoke.py
python3 REPO/code/sample_game.py 47 OUTPUT/sample-seed47.md
```

Create `OUTPUT` first. See `evidence/README.md` for dependencies and expected results. Defect reproducers assert the defective baseline behavior; a corrected release should change those assertions rather than preserve them.

**Native source:** GMT Games, *Caesar: Rome vs. Gaul*, second-edition rules, 2023-1d, especially printed page 13, section 14.3.2. [Publisher-hosted PDF](https://gmtwebsiteassets.s3.us-west-2.amazonaws.com/CaesarRomeVSGaul/2nd+Edition/CAESAR-RULES-2023-1d.pdf). Downloaded PDF SHA-256: `2289f25a7c421dd27175c108609e9df6c19bd5fea757d0134c1af308987a9a70`. The original publisher PDF is not redistributed in the evidence archive.

**Repository baseline:** [pinned release](https://github.com/ramyahoo88/Caesar_Rome_vs_Gaul_solo/tree/3e8dbac8d2d0bc8bf4e4e8919574ff593d3ea406). All source line references in this report refer to that commit.

**Release decision:** patch C01–C08, resolve or clearly disclose the second-edition model assumptions, rerun the final study and latest-change comparisons, regenerate the affected PDFs, and complete a real-browser/offline smoke check. No production rule, bot, helper or published study was changed by this audit.
