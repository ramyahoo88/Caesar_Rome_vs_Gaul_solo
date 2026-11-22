# Clean-room check of the Imperator / Concilium solo rules

A separate agent wrote `CleanBot` from `Caesar_Solo_Rules.md` and the engine API only, without seeing `bots.py`. It then compared CleanBot with `bots.BotPolicy`:

1. **Full games** (seeds 0–99). Each game was played twice: once with bots.py on both sides, once with CleanBot on both sides. The random streams were aligned.
2. **Decisions** (100 games, bots.py on both sides). At every card play, every AP and every other engine hook, the game was copied and both implementations were asked what they would do.

## Agreement

| Measure | Rome | Gaul |
|---|---|---|
| Card and mode | 4803/4814 (99.8%) | 4842/4842 (100%) |
| AP mission | 8736/8784 (99.5%) | 7159/7208 (99.3%) |
| Whole AP decision (mission, army, target, ops or space) | 8423/8784 (95.9%) | 6505/7208 (90.2%) |
| Other hooks (both sides) | 24400/25859 (94.4%) | |

Every full game diverged by Turn 3: 68 games in Turn 1, 30 in Turn 2 and 2 in Turn 3. The most common first divergences were C2, A8, C1, A9 and A1.

## (b) Bugs in the clean-room code (fixed, then re-run)

* **B1, 5.3 SWEEP.** The clean-room bot read the army choice as "most MP left first".
* **B2, 4.5 Rerolls.** It compared the effective value of the "lower die" instead of the number shown.
* **B3, 4.4 Backing up.** It counted only the units already in the target space.

## (a) Gaps and ambiguities in the rules text

| # | Rule | Finding | Suggested fix |
|---|---|---|---|
| A1 | 5.3 SWEEP tie order | 539 Gaul and 61 Rome RAID cases | Among equal weights: fewest MP, then most MP left, then the strongest army, then the compass |
| A2 | Several armies tie for one target | AMBUSH 75, SUBMIT 18, other missions 4 | Ties between armies follow the army order in section 3. Define an army order for Concilium |
| A3 | 3 Odds for a siege | Roman CUs already in the space | Say whether they count. The engine counts them |
| A4 | SIEGE "best odds" | 2 cases | "best Siege Table column" |
| A5 | SWEEP weights during the extra steps | 1 case | Judge the weights at the start of the mission |
| A6 | 6.2 Agitate line 6 | Some of the 38 Agitate mismatches | Say whether provinces Gaul already controls count |
| A7 | 4.3 Interception | 589 of 2480 cases | Units inside a fortification neither intercept nor count |
| A8 | 5.6 Winter camp "room" | 184 of 593 cases | Room counts only Legions already moved there this Winter |
| A9 | 5.5 / 6.5 Activation Events | Motus Ubique 19/88 and Trumpets of War 93/165 agree | Spell out the order, and whether PROTECT step 3 applies in activations |
| A10 | #50 Live test | 6 card-mode mismatches | Say whether the port and naval-supremacy target is required |
| A11 | Unspecified choices | Kept-Legate tie; #1 "largest stack"; #17 which Legate; displaced Caesar; Gallic IM relocation; #20 which Legion; Gaul's #50/51 point; Labienus with no leaderless stack; both Offer cards ★ and Live | One line each |

## (c) bots.py does things the text does not say

| # | Behaviour | Cases |
|---|---|---|
| C1 | SUBMIT also rolls a siege at a Fortified Town (it reuses STRIKE) | 208 |
| C2 | SIEGE ignores "one siege roll per card": Caesar marches to a location already rolled against this card | 28 |
| C3 | CONTINUE fires when no roll is possible, wasting the AP | 12 |
| C4 | A Gallic leader's own CS is left out of his army's BS | 37 |
| C5 | The Minor Tribe forms an army on its own | 14 |
| C6 | Control Table lines 3–5 consider only Gaul | 16 |
| C7 | Agitate Deny includes provinces where a Fortified Town blocks Roman control | 5 of 6 sampled |
| C8 | PROTECT step 3 takes the first line of the whole Control Table, and acts only if that line lands in Provincia | 6 |
| C9 | Mass activations also run GATHER, and #32 includes Legions stacked with a leader | most #32 / #11 mismatches |
| C10 | Losses: two hits on two full Legions eliminate one instead of flipping both (breaks 4.6) | Rome 197/1033, Gaul 49/720 |
| C11 | When every Legion stack has a leader, a Legate goes to an empty Walled City rather than to Caesar | 26/986 |
| C12 | Caesar displaced: Provincia IMs are not removed last | 17/22 |
| C13 | Event IM weights: Germania/Britannia 3 instead of 1; Gallic-controlled Provincia 3 instead of 4 | 6/456 |
| C14 | Live tests: #40 ignores the vacant-space condition; #3/#20 count besieged Legions; Rome's #45 requires no CUs at all | 5 |

What was done about each item is in [CLEANROOM_RESPONSE.md](CLEANROOM_RESPONSE.md).
