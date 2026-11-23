# Changelog

## v1.2 (22 November 2026)

This release fixes everything found by the independent v1.1 re-audit. See [audit/independent-v1.1/AUDIT_RESPONSE.md](audit/independent-v1.1/AUDIT_RESPONSE.md).

* **Rules 1.3.** A Reserve card leaves the Reserve as soon as it is spent, discarded or given away, and a later copy starts face down.
* **Rules, section 3.** A Gallic leader on his own is an army, because he is a CU.
* **Engine: Surprise-only hands.** They are fully replaced. Owners are told when a card leaves the hand, before replacements are drawn.
* **Danger check.** It now includes a Gallic leader moving alone.
* **Helper.** Damaged Undo history is checked, dropped with a notice, and can no longer crash Undo.
* **AP sensitivity check.** It now changes only the AP values (new `ap_edition` option) and reports paired differences.
* **Re-runs.** The final study, the latest-change comparisons (now with per-seed results and paired standard errors) and the bot-vs-bot breakdown were re-run.
* **Sample game.** Regenerated: seed 57 is now a narrow Gaul win.
* **Record sheet.** It has a REGROUP tally code.

## v1.1 (22 November 2026)

This release fixes everything found by the independent v1.0 audit. See [audit/independent-v1.0/AUDIT_RESPONSE.md](audit/independent-v1.0/AUDIT_RESPONSE.md).

**Rules**

* **Reserve (1.3).** Only cards an Offer has revealed can be used. New rule for when only Reserve cards are left: #24 is played for AP, otherwise the Surprise cards are discarded and replaced. A worked example is included.
* **Danger (section 3).** Danger is judged on the board after the move: the army has left its old space, and any IM the move removes is gone.
* **REGROUP.** The destination must have no Gallic CUs outside.
* **Appendix.** The appendix now lists REGROUP among Imperator's fixed missions.

**Simulation engine and bots**

* **Reserve cards.** The bot reveals Reaction and Surprise cards into its Reserve during the Offer; unrevealed cards are never used.
* **Danger and REGROUP.** Both are evaluated on the board as it will be after the move.
* **Siege contributors.** Every CU that adds strength to a siege attempt now counts as activated (14.3.2).
* **Card #42.** It is discarded normally unless its Event moves it to the Roman hand. It is no longer lost or duplicated.
* **Re-run studies.** The final study, the bot-vs-bot breakdown, the 1st-edition AP check and the latest-change comparisons were all re-run.
* **Regression tests.** New tests in `code/tests/test_audit_fixes.py`, and a card-conservation check in the smoke tests.

**Print and helper**

* **Card sheets.** They now print face, back, face, back, so double-sided printing pairs them.
* **Sample game.** New sample game (seed 57), correctly labelled Imperator level 3 vs Concilium level 4 (standard rules).
* **Simulation report.** Proper code blocks and the right sample seed; the 1st-edition Siege Table approximation is now disclosed.
* **Helper.** It validates saved sessions and recovers from damaged ones with a notice. It keeps a card-play counter per bot, lets Undo cross *Next turn*, and stops at Turn 6. It shows when the deck will reshuffle, warns if the session is not being saved, and has fuller reminders.

## v1.0 (22 November 2026)

First release: Imperator and Concilium rules, 18 Directive cards, reference sheet, record sheet, sample game, simulation report, engine and study code.
