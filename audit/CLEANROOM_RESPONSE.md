# Response to the clean-room check

A separate agent wrote its own bot from the printed rules alone and compared it with the simulation bot, decision by decision ([CLEANROOM_REPORT.md](CLEANROOM_REPORT.md)). Before the fixes below, it agreed with the simulation bot on:

* 99.8% of card choices;
* 99.4% of mission choices;
* 90–96% of complete AP decisions (mission, army and target).

Every gap it found was settled in one of two ways: the printed rules now say what the code does, or the code now does what the rules say. Fixing the code meant the simulation had to be re-run, so all results in the Simulation Report come from the corrected code.

## Rules text clarified (the code was already right)

| # | Change |
|---|---|
| A1 | 5.3 SWEEP: target and army are chosen together. Ties go to the fewest MP, then the most MP left over, then the stronger army, then the compass. |
| A2 | Section 3: **Ties between armies** go to the stronger army, then army order. Concilium's leaders are listed Vercingetorix first. |
| A3 | Section 3 Odds: in a siege every Roman CU in the space counts (the code was changed to match). The defender is the Garrison plus every Gallic CU in the space, because the units inside may come out and fight. |
| A4 | SIEGE target order: "best Siege Table column". |
| A5 | SWEEP weights are judged at the start of the mission. |
| A6 | Agitate line 6: provinces Gaul does not control come first (the code was changed to match). |
| A7 | 4.3: units inside a fortification neither intercept nor count. |
| A8 | Winter camp: room counts only Legions already moved there this Winter. |
| A9 | 5.5 / 6.5: single-leader and multi-army activations are spelled out step by step. GATHER is the last activation mission. PROTECT never places an IM during an activation (the code was changed to match). |
| A10 | #50 Live test: a port location with Naval Supremacy (the code was changed to match the event). |
| A11 | One line each for: the kept-Legate tie, #1 and #17 Legate choice, #20, where a displaced Caesar goes, the displaced Gallic IM, Gaul's #50/#51, Labienus with no leaderless stack, and both Offer cards ★. |
| C1 | SUBMIT also rolls a siege when it ends at a Fortified Town (as STRIKE does). |
| C5 | Section 3: the Minor Tribe forms an army like a Tribe. |
| C6 | Control Table lines 3–5: "a province of Gaul". |

## Code changed to follow the rules

| # | Fix |
|---|---|
| C2 | SIEGE skips a location already rolled against this card. |
| C3 | CONTINUE acts only if a roll is possible (odds 1:2+, Stronghold CS 2+). |
| C4 | A Gallic leader's own CS counts in his army's BS. An engine bug was fixed at the same time: the leader himself counted toward the over-Command-Rating move penalty. |
| C7 | Agitate Deny: only provinces with no Fortified Town where one Roman IM would give Rome control. |
| C8 | PROTECT step 3 places directly by Control Table line 2. |
| C9 | #32 activates only Legions in spaces with no leader. |
| C10 | **Engine bug, important.** Two hits on two full-strength Legions eliminated one Legion instead of flipping both, which broke 4.6 for both sides. Fixed in `lose_steps`. |
| C11 | A Legate with no leaderless stack to join now goes to Caesar. |
| C12 | Caesar displaced: Provincia IMs are removed last. |
| C13 | Event IM weights match the RAID weights: Provincia 4, Germania and Britannia 1. |
| C14 | Live tests for #3, #20, #40, #45 and #50 match the event's own target rules. |
