# Response to the independent v1.2 re-audit

The re-audit ([Caesar_Solo_v1.2_Reaudit.md](Caesar_Solo_v1.2_Reaudit.md)) reviewed commit `a52079a`. It confirmed that R01–R05 are fixed, and its 120 study replays and 36 comparison replays matched the archive. It found two more issues; both are fixed in **version 1.3**. Because R06 changes the simulation, the final study, the latest-change comparisons, the AP-only check and the bot-vs-bot breakdown were all re-run on the v1.3 engine.

| ID | Finding | Fix in v1.3 |
|---|---|---|
| R06 (Medium) | The extra plays right after #42 or after a #24 cancellation skipped the Forced March cleanup | Surprise cleanup has moved into `card_play` and runs once at the start of every new card play, wherever the call comes from. That includes the immediate play after #42 and the replacement play after a cancelled Event. The strategy loop no longer calls it separately, so it never runs twice. The retry after discarding a Surprise card is the same card play, so it is flagged and skips the step. Rules 1.3 now say that #55 is also discarded before such an extra play. New tests use the re-audit's #42 and cancellation positions, plus the normal-path control. A 101-game observation, seeds 950000–950099 plus 200002, found no Offer made while a revealed #55 was still in hand. |
| R07 (Low) | The AP check computed per-seed VP but did not save it | `code/ap_only.py` now saves the full rows: per-seed VP, winner and end reason for both AP settings, plus the seed range and settings. The re-run artifact is `results/ap_only_check_v1.3.json`. The v1.1 response's statement that the per-seed results are kept is now true. |

**Still open, unchanged:**

* The exact 2nd-edition Siege Table and card faces are not transcribed.
* No complete clean-room implementation of the latest text exists.
