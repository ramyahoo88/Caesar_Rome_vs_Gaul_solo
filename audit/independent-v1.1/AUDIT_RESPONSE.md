# Response to the independent v1.1 re-audit

The re-audit ([Caesar_Solo_v1.1_Reaudit.md](Caesar_Solo_v1.1_Reaudit.md)) reviewed commit `dcbfc22` and confirmed that the v1.0 fixes hold. It found five more issues (four Medium, one Low) and made four optional suggestions. Everything listed below is fixed in **version 1.2**. The final study, the bot-vs-bot breakdown, the latest-change comparisons and the AP-only check were all re-run on the corrected engine. The latest-change comparisons now keep their per-seed results and report the paired difference with its standard error. The regression tests are in `code/tests/test_audit_fixes.py`. They reuse the re-audit's positions, with each assertion turned around to check the corrected behaviour.

| ID | Finding | Fix in v1.2 |
|---|---|---|
| R01 (Medium) | A hand of only Surprise cards was only partly replaced | `handle_surprises_start` now decides "all Surprises" before changing the hand, then discards every one of them and draws the same number. A revealed #55 in a mixed hand is still discarded on its own. Tests: two- and three-Surprise Reserves are fully replaced; in a mixed hand an unrevealed #55 stays and a revealed one goes. |
| R02 (Medium) | A spent Reserve card that was immediately redrawn kept its old reveal status | The engine now tells the card's owner whenever a card leaves a hand, before any replacement is drawn. This covers spent Reaction and Surprise cards, Surprise discards, played cards, the cards #42 takes away, and the end-of-phase discard. The bot then drops the card from its Reserve, so a later copy starts face down. Rules 1.3 now say so. Test: the re-audit's Gergovia siege, where #52 is spent, reshuffled and redrawn at once and then cannot be used. |
| R03 (Medium) | Danger left out a Gallic leader moving alone | A Gallic leader is a CU (9.5.2), so an army that is just the leader now counts in the danger check (a Roman leader alone still does not). The rules' army definition now says a leader on his own is an army. Test: Vercingetorix alone with Local Support puts the Legion at Bibracte in danger; without Local Support it is safe. |
| R04 (Low) | Damaged Undo history could still crash Undo | Each saved Undo step is parsed and checked against the full state schema when the session is loaded; damaged steps are dropped with a notice. Undo checks the step again before using it. Tested in headless Chrome with a non-JSON step, a step with an invalid side, and a mix of good and bad steps; normal Undo is unchanged. |
| R05 (Medium) | The "AP" sensitivity check also changed four other rules | New engine option `ap_edition`. The check now keeps every 2nd-edition rule (siege cost, table shift, Stronghold points, friendly modifier) and changes only the card AP values. Results are on the same seeds, with the paired VP difference and its standard error. The report text is regenerated from that run. |

**Optional suggestions, all adopted:**

* The record sheet has a tally code for REGROUP (RG).
* The sample game was regenerated on v1.2. Seed 57 now ends in a narrow Gaul win, and the narrative was rewritten.
* Section 6 of the report introduces its tables in the order they appear (the corrected-engine comparison first), and its claim is narrowed to the re-run results.
* The latest-change and AP-only runs keep their per-seed results and report the uncertainty of the paired differences.

**Still open (as the re-audit notes):**

* The exact 2nd-edition Siege Table and card faces are not transcribed; the simulation uses the disclosed approximation.
* No complete clean-room implementation of the v1.2 text exists.
