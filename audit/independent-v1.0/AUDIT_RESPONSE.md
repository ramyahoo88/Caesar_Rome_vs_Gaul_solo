# Response to the independent v1.0 audit

The audit ([Caesar_Solo_v1.0_Independent_Audit.md](Caesar_Solo_v1.0_Independent_Audit.md)) reviewed commit `3e8dbac`. It found eight issues (one High, three Medium, four Low), raised one wording question and suggested several usability changes. All eight are fixed in **version 1.1**. The final study, the bot-vs-bot breakdown, the 1st-edition AP check and the latest-change comparisons were all re-run on the corrected engine. Section 6 of the Simulation Report still shows the development-time tuning tables as history, labelled as such, next to the new comparison. The regression tests are in `code/tests/test_audit_fixes.py`. They use the audit's own positions, with each assertion turned around to check the corrected behaviour.

| ID | Finding | Fix in v1.1 |
|---|---|---|
| C01 (High) | Reserve cards could be used before an Offer revealed them | The bot now tracks its face-down hand and its face-up Reserve separately. Reaction and Surprise cards are revealed one at a time during the Offer (rules 1.3, 2.2), and only revealed cards can trigger #24, #52, #54 or #55. The Reserve empties when the hands are discarded at the end of the Strategy Phase. Tests: no cancellation before the first Offer; cancellation after #24 is revealed; Reserve cleared on a new turn. |
| C02 (Medium) | Danger was judged before the move, so a route the army had been blocking was missed | Danger is now judged on the board after the move. The moving army is lifted from its old space; any enemy army whose reach touched that space is re-traced; the IMs the SWEEP removes are taken off before Local Support is counted. This covers both bots' SWEEPs (target and every extra step) and Imperator's REGROUP. The rules text (section 3) says so explicitly. Tests: the audit's Aduatuci–Eburones raid is refused, while the one-Legion control raid still goes; REGROUP no longer moves VII to Eburones. |
| C03 (Medium) | Siege contributors stayed available for another activation | Every CU that adds strength to a siege attempt is now marked as activated (14.3.2, Step 1). CUs that had already moved still contribute. Test: the audit's Gergovia position; XIII and XIV can no longer move afterwards. |
| C04 (Medium) | Card #42 vanished when played for AP | #42 is discarded like any other card unless its Event has actually moved it into the Roman hand. A follow-up check also caught a nested-play case: the Event makes Gaul play again at once, and #42 was then duplicated. The check now looks at where the card actually is. Tests: #42 for AP; #42 as an Event; 55-card conservation at the end of complete games. |
| C05 (Low) | The helper trusted damaged saved sessions | A saved session is checked in full before use: side, levels, turn, counters, deck indices and uniqueness, current card and history. A bad save is set aside under a separate key, a new game starts, and a notice explains this. Headless-Chrome tests covered invalid side, duplicate deck, non-JSON, reload, Undo and reshuffle. |
| C06 (Low) | The sample game said Concilium was at level 3 | It is now labelled "Imperator level 3 vs Concilium level 4 (standard rules)". The sample was regenerated on the corrected engine (seed 57) with a new narrative. |
| C07 (Low) | The Directive appendix left out REGROUP | Fixed. Every list of the bot's missions was re-checked: rules 2.5, the appendix, the reference sheet, the card footers and the helper. |
| C08 (Low) | The report's reproduction commands collapsed into one line and gave the wrong seed | Markdown `fenced_code` is enabled and code blocks are styled. The commands now use seed 57, with a note that the sample's introduction and narrative are editorial. |
| Q1 | Is #24 the "last card" when only Reserve cards are left? | Rules 1.3 now say: when every card left is in the Reserve, the bot plays #24 for AP if it holds it; otherwise (Surprises only) it discards them and draws replacements, then makes its Offer from the new cards. A worked example is included. |
| Fidelity | 1st-edition Siege Table with a −1 shift | Disclosed in the Simulation Report's summary and limitations. The printed bots use whatever table your copy of the game prints. |

**Usability suggestions adopted in the helper:**

* Undo now works across *Next turn*, and the button is disabled on Turn 6 instead of clearing the turn.
* Each bot has its own card-play counter, so the level 5 and Roman level 2 first-four bonus is counted per side.
* The deck shows "0 left · reshuffles on next draw".
* The first-four bonus reminders repeat the AP/Bonus-card qualifier and the #4 exception.
* The full lagging-region tie rule and the after-the-move danger rule are in the panels.
* A notice appears if the browser is not saving the session.

**Card sheets** now print face, back, face, back, so ordinary double-sided printing pairs them.

**Not adopted:**

* Session export/import. The helper is optional, and the paper deck is the reference.
* A worked danger example in the rules. The definition now states the after-the-move board, and the reference sheet and helper repeat it. It is on the playtest checklist.
