# Caesar: Rome vs. Gaul — Solo Bots: Simulation Report

*Imperator and Concilium, version 1.3. These are model results from computer play, not tabletop results.*

## 1. Summary

* **Both bots play complete games of the 2nd-edition rules** in the simulation, with one approximation: the Siege Table is the 1st-edition table shifted one row. Each decision comes from a Directive card and a two-card Offer, following the printed rules. The bot never looks at hidden cards, and its Reaction and Surprise cards work only once an Offer has revealed them. An independent clean-room implementation of the printed rules matched the simulation bot on more than 99% of card and mission choices. Three independent audits (of v1.0, v1.1 and v1.2) found fifteen issues between them, all fixed in v1.3, and every study result here comes from the corrected v1.3 engine.
* **The levels form a smooth ladder against every computer opponent.** Against the strongest of them, the Lookahead player:
    * Imperator wins 0% at level 1, 30% at level 3 and 65% at level 5;
    * Concilium wins 64% at level 1, 84% at level 3 and 98% at level 5.
* **Concilium is the stronger bot.** Under the standard rules (its level 4) it wins 63% against Imperator with +1 AP and 91% against the Lookahead player. Rome-side computer players are weaker than skilled humans, so Concilium's levels start with a lower VP target for you: 9 VP at level 1. Level 3 (11 VP) is the recommended start.
* **Imperator at level 3** (+1 AP on every card play) wins 36% of its games against Concilium and about 51% against the Heuristic players.
* **A typical bot-vs-bot game (Imperator at level 3, Concilium under the standard rules) is a Governance race.** Rome earns most of its VP from Governance, plus Caesar's Pass. A game has few battles (about 1.6) and around 9 siege rolls.
* 5,300 games were played for the final study, and many thousands more during development.

## 2. The simulation engine

The engine (`code/engine.py`, `events.py`, `cards.py`, `map.json`) plays complete games of the 2nd-edition rules:

* **Map:** 117 spaces and 275 connections (path, rough, Channel); 26 provinces in 6 regions. Extracted from the Vassal module's map and checked against the printed province values.
* **Turns:** six turns of reinforcements (3 Tribes per turn, Turn-5 Legions, Ambiorix, Vercingetorix) and card play with Reactions and Surprise cards. Each turn ends with Winter: Supply, Isolation, Governance, Winter Camps, Fading Promises and Spring Muster.
* **Cards:** all 55, each played as an Event, a Bonus card or AP.
* **Movement and combat:** Command Ratings and over-command, Interception, Avoid Battle and Back Up, battles with leader and elite rerolls, retreats, and Submission at 3:1.
* **Sieges:** Siege Points, surrender at 3:1 and Strongholds, including Caesar's Pass.
* **Influence:** Place, Convert and Remove, Local Support, the Council Box and the Major Uprising.
* **The edges of the map:** Germania and Britannia with native attacks, and Storms at Sea.
* **Victory:** both automatic victories and the Turn 6 VP total.

## 3. Opponents

Each bot was tested against four computer players of the other side.

| Opponent | How it plays |
|---|---|
| **Bot** | The other paper bot, following its printed rules exactly. In the Imperator rows it is Concilium under the standard rules. In the Concilium rows it is Imperator at its level 3 (+1 AP on every card play), the strongest Roman player available. |
| **Heuristic** | Sees its whole hand and scores every Event and AP use with hand-tuned values. |
| **Heuristic (aggressive)** | The same player with 1.5× weight on attacks and 0.7× on influence. |
| **Lookahead** | For each card, tries the candidate plays on a copy of the game with fresh dice (so it cannot see the future) and keeps the one its position evaluation likes best. |

None of them plays as well as a strong human. Read the tables as a comparison between levels and between opponents, not as a forecast of your own win rate. The Lookahead player is the strongest of them, so its column is the best guide to a skilled opponent.

## 4. How the bots were developed

**Concilium** beat every Roman computer player from its first version. Its rules are short:

* **RAID** where the Legions are not.
* **AMBUSH** only at good odds.
* **AGITATE**.
* **BANK** IMs in the Council Box early.
* **RISE** to spend them.

Most of the tuning went into three things: the RAID weights (Narbonensis first, never next to Caesar), when to BANK and RISE, and the *danger* rule (section 6).

**Imperator** was much harder, because Rome must *earn* 12 VP while Gaul only has to stop it. The first Imperator decks were built around sieges and battles, and they scored about 3 VP a game. The fixes came from four kinds of test:

* **A passive opponent.** Against a Gaul that did nothing, Imperator scored 14–15 VP. So the engine and the scoring were sound, and the weakness was in the decisions.
* **A lookahead hybrid.** One version of Imperator tried every mission on a copy of the game with fresh dice and logged which ones paid. Removing Gallic IMs (RAID) and completing provinces (RULE) were worth far more per AP than sieges. A siege paid only when the Town was about to fall. That finding produced RULE (Control Table lines 0–3), the SWEEP procedure and the strict SIEGE targets.
* **Ablations.** Each mission was switched off in turn, and so were the block and deny lines and the size of the Offer. A change was kept only if it held up on fresh seeds. An Offer of two cards played as well as seeing three cards or the whole hand, so the bot keeps the simpler Offer.
* **Loss analysis.** Legions were dying to Gallic ambushes, about 2.9 per game, mostly in two-Legion Legate armies in Belgica. This produced the *danger* rule and the REGROUP mission.

Ideas that did not help, and were dropped:

* An expedition to Britannia or Germania from Turn 3. The 2 VP rarely made up for Caesar's absence.
* More sieges.
* Looser siege rules for every army. They helped against Concilium but cost VP against the Heuristic and Lookahead players. Only Caesar's army was given the looser rule (section 6).
* Blocking provinces before their Tribe arrives.
* A danger ratio other than 1.5 for Imperator. Ratios of 1.0, 1.25 and 2.0 were all tried.
* Putting RAID first on more Directive cards.
* A lower STRIKE ratio for Caesar's army.
* Putting SIEGE first on more Directive cards.
* A different winter-camp priority order, preferring a Live Event over a higher-AP card, and more ★ Events (#9, #12).

**Is the printed mission order good enough?** As a final check, we built an Imperator that keeps the Offer and the Directive but picks each AP's mission by lookahead. It tries every mission on a copy of the game, with fresh dice, and keeps the one the position evaluation likes best. Over 120 games against Concilium with +1 AP (Imperator's level 3) it won 44%, with a mean of 10.7 VP. The printed Imperator won 43% with the same mean. Both figures come from the v1.0 engine, before the audit fixes. The lookahead and the printed order agreed on 70% of the 14,000 decisions. Most of the disagreements were cases where the lookahead skipped REGROUP or SIEGE to place an IM instead, and the earlier tests showed that REGROUP pays off over the following cards, which the one-step lookahead cannot see. Within the reach of a one-card lookahead, then, the printed mission order loses nothing.

The last checks on Concilium varied its AMBUSH ratio (1.25× and 2×), the RISE threshold and the last BANK turn. None of these moved the result by more than about 0.2 VP, which is within the noise, so Concilium's rules were left unchanged.

## 5. Independent checks

Three independent reviews checked the work. None of the reviewers had written the code.

* **Engine audit.** Compared the engine with the 2023 living rules and reported 23 findings. The important ones were fixed: Submission is now checked before Avoid Battle, legion attrition was corrected, and Roman supply sources now trace correctly. One item was kept on purpose (Fading Promises), and one simplification remains (Sorties). See `audit/ENGINE_AUDIT_RESPONSE.md`.
* **Clean-room test.** Wrote a second implementation of both bots from the printed rules only, then compared it with the simulation bot decision by decision. Before fixes, the two agreed on:
    * 99.8% of card choices;
    * 99.4% of mission choices;
    * 90–96% of full AP decisions (mission, army and target).

    Every gap it found was closed, either by clarifying the text or by fixing the code. One of the code fixes was an engine bug in how losses were applied, which affected both sides. See `audit/CLEANROOM_RESPONSE.md`.

    This check covered the rules text as it stood before the last round of changes in section 6: the danger rule, REGROUP, the lagging-region order and Caesar's 2:1 sieges.

* **Independent v1.0 audit.** Reviewed the whole v1.0 release: rules, cards, reference, helper, sample game, report, code and the archived study. It reproduced every one of the 40 study totals and ran its own 240-game sweep. It also tested the latest changes with hand-built positions. It found eight issues. The most important was that Reaction and Surprise cards could be used before an Offer had revealed them. Two others: danger was judged before the move, missing routes the moving army had been blocking; and units that added strength to a siege could still activate again. All eight are fixed in v1.1. A re-audit of v1.1 then found five more issues. Three were in the simulation: Surprise-only hands were only partly replaced; a spent Reserve card that was immediately redrawn stayed face up; and a Gallic leader alone was left out of the danger check. The other two were a helper Undo crash and an AP-sensitivity check that also changed four other rules. All five are fixed in v1.2. A third review, of v1.2, found that the immediate extra plays after #42 or after a cancelled Event skipped the Forced March cleanup, and that the AP check did not keep its per-seed results. Both are fixed in v1.3. The final study (section 7), the corrected-engine comparison (section 6) and the breakdown (section 8) all come from the v1.3 engine. See the `AUDIT_RESPONSE.md` files under `audit/independent-v1.0`, `-v1.1` and `-v1.2`.

## 6. The final changes and what they were worth

These changes were made after the clean-room fixes. The first table below measures them on the current, corrected engine. The three tables after it are **development-time numbers**: they were measured on the engine before the audit corrections and are kept as a record of how the decisions were made.

**On the corrected v1.3 engine** (seeds 20000 and up; 200 games against the Bot, 160 against the Heuristic player, 100 against the Lookahead player). Each cell is the bot's win rate, with the mean Roman VP in brackets. For each "without" row, the change in mean Roman VP against the final version is given on the same seeds, ± one standard error of the paired difference.

| Version | vs Bot | vs Heuristic | vs Lookahead |
|---|---|---|---|
| Imperator v1.3 (level 3) | 38% (10.4 VP) | 52% (11.4 VP) | 40% (10.3 VP) |
| … without REGROUP and the danger limit on SWEEP | 44% (10.7 VP); +0.28 ± 0.18 | 46% (10.9 VP); -0.46 ± 0.26 | 29% (9.3 VP); -1.04 ± 0.37 |
| … without the lagging-region order | 35% (10.0 VP); -0.40 ± 0.19 | 54% (11.3 VP); -0.10 ± 0.21 | 23% (9.8 VP); -0.54 ± 0.30 |
| … without Caesar's 2:1 sieges | 30% (9.7 VP); -0.71 ± 0.20 | 57% (11.5 VP); +0.13 ± 0.25 | 33% (10.2 VP); -0.19 ± 0.33 |
| Concilium v1.3 (standard rules) | 62% (10.4 VP) | 94% (5.0 VP) | 88% (7.1 VP) |
| … without its danger rule | 40% (11.7 VP); +1.32 ± 0.21 | 92% (6.0 VP); +1.04 ± 0.37 | 85% (8.2 VP); +1.10 ± 0.35 |

For Imperator, the Bot is Concilium under the standard rules. For Concilium, the Bot is Imperator with +1 AP on every card play.

On the corrected engine every change still pays overall, though not against every opponent. A minus sign means Rome scores less without the change:

* **REGROUP and the danger limit.** Without them Imperator scores about 0.3 VP more against Concilium, but about 0.5 VP less against the Heuristic player and 1.0 VP less against the Lookahead player. They pay against the stronger, more flexible opponents.
* **The lagging-region order.** Without it Imperator scores about 0.4 VP less against Concilium and 0.5 VP less against the Lookahead player.
* **Caesar's 2:1 sieges.** These gain about 0.7 VP against Concilium. Against the other opponents the difference is within the noise.
* **Concilium's danger rule.** It takes 1.0–1.3 VP off every Roman opponent.

The development-time tables follow. Each row compares the same seeds with and without the change, and the Imperator rows are at level 3.

**Imperator** at level 3. Seeds 9000+: 200 games each against the Bot and Heuristic players, 100 against the Lookahead player. The Bot here is the Concilium of that time, before its own danger rule was added. Each cell gives Imperator's win rate and its mean VP.

| Version | vs Bot | vs Heuristic | vs Lookahead | Legions lost per game |
|---|---|---|---|---|
| Before | 38.5% (10.7 VP) | 36.0% (10.2 VP) | 17% (8.5 VP) | 2.3 |
| + REGROUP | 40.0% (10.4 VP) | 42.5% (10.7 VP) | 17% (9.1 VP) | 1.5 |
| + REGROUP + danger limit on SWEEP (adopted) | 43.0% (10.8 VP) | 46.0% (10.9 VP) | 18% (9.0 VP) | 1.3 |

**Concilium's danger ratio**, the Roman BS (as a multiple of the Gallic BS) at which a space counts as dangerous for its SWEEPs. Seeds 9500+: 160 games against Imperator with +1 AP and against the Heuristic player, 80 against the Lookahead player. Each cell gives Concilium's win rate, then the mean Roman VP (lower is better for Gaul).

| Danger ratio | vs Imperator (+1 AP) | vs Heuristic | vs Lookahead |
|---|---|---|---|
| none | 53% (11.1) | 95% (6.0) | 75% (8.6) |
| 2× | 68% (10.2) | 97% (5.5) | 85% (7.6) |
| 1.5× | 71% (9.8) | 96% (5.5) | 94% (7.3) |
| **1× (adopted)** | 75% (9.5) | 96% (4.6) | 98% (6.5) |
| 0.5× | 78% (9.4) | 96% (4.4) | 94% (6.9) |

Below 1× the gains level off, and 1× ("a Roman army could reach it with at least equal strength") is the simplest rule to apply at the table.

**Two last Imperator changes**, tested against the final Concilium. Each cell is the change in Imperator's mean VP at level 3 on the same seeds, one figure per seed set: 200 games against Concilium and against the Heuristic player, and 120 against the Lookahead player.

| Change | vs Concilium | vs Heuristic | vs Lookahead |
|---|---|---|---|
| Control Table: **lagging region first** (Celtica or Belgica, whichever Rome is not winning) | +0.35, +0.42 | +0.32, +0.52 | +0.84, +0.08 |
| SIEGE: **Caesar's army at 2:1** may siege any Town (before: only a Town with a Siege Point already on it) | +0.61, +0.24 | −0.35, −0.21 | +0.19, +0.30 |

Both were adopted. The second costs a little against the Heuristic player but gains against the two stronger opponents.


## 7. Final study

**Method.**

* Every level of each bot played every opponent: 150 games against the Bot and Heuristic players and 80 against the Lookahead player, 5,300 games in all.
* The study used seed ranges 100000+ (Imperator) and 200000+ (Concilium), which were never used during development.
* All cards used the assumed 2nd-edition AP values.
* The cells below give the bot's win rate and the mean Roman VP. With 150 games the margin of error is about ±7 points; with 80 games, about ±9.

![Imperator win rate by level](sim/imperator_levels.png)

*Error bars show one standard error.*

![Concilium win rate by level](sim/concilium_levels.png)

### Imperator (bot plays Rome; cells = Imperator win rate, mean Roman VP)

| Level | Bot | Heuristic | Heuristic (aggressive) | Lookahead |
|---|---|---|---|---|
| 1 | 4% (6.9 VP) | 6% (6.1 VP) | 6% (7.0 VP) | 0% (3.6 VP) |
| 2 | 18% (9.0 VP) | 17% (8.8 VP) | 26% (9.2 VP) | 8% (6.8 VP) |
| 3 | 36% (10.3 VP) | 44% (10.9 VP) | 59% (11.8 VP) | 30% (9.7 VP) |
| 4 | 63% (10.3 VP) | 67% (10.9 VP) | 77% (11.8 VP) | 60% (9.7 VP) |
| 5 | 74% (10.3 VP) | 81% (10.9 VP) | 87% (11.8 VP) | 65% (9.7 VP) |

### Concilium (bot plays Gaul; cells = Concilium win rate, mean Roman VP)

| Level | Bot | Heuristic | Heuristic (aggressive) | Lookahead |
|---|---|---|---|---|
| 1 | 23% (10.3 VP) | 85% (4.9 VP) | 83% (4.3 VP) | 64% (7.3 VP) |
| 2 | 37% (10.3 VP) | 89% (4.9 VP) | 90% (4.3 VP) | 74% (7.3 VP) |
| 3 | 53% (10.3 VP) | 95% (4.9 VP) | 95% (4.3 VP) | 84% (7.3 VP) |
| 4 | 63% (10.3 VP) | 98% (4.9 VP) | 97% (4.3 VP) | 91% (7.3 VP) |
| 5 | 83% (8.9 VP) | 100% (1.7 VP) | 100% (1.4 VP) | 98% (4.7 VP) |

Imperator levels 3–5 differ only in the VP Rome needs, so they play the same games and show the same mean VP. The same is true of Concilium levels 1–4.


## 8. How the games are decided

These figures come from 300 games of Imperator (level 3) against Concilium (standard rules), on seeds from 300000 up. Rome won 104 of them (35%), with a mean of 10.3 VP.

**Where Rome's VP come from (per game):**

| Source | VP |
|---|---|
| Governance (six winters) | 9.4 |
| Caesar's Pass | 0.83 |
| Germania and Britannia | 0.07 |
| Eliminated Tribes (÷4) | about 0.9 (3.6 Tribes) |
| Eliminated Legions | −0.53 |

**Mean Governance by winter** (9–10 Governance gives 2 VP, 7–8 gives 1):

| Turn | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Mean Governance | 9.3 | 9.2 | 9.1 | 9.0 | 8.9 | 8.7 |

64% of Rome's winters reach 9–10 Governance. The rest fall to 7–8, nearly always because Belgica is tied or lost. Turn 6 is the hardest winter, because Concilium saves its Submitted Tribes and Council IMs for a late Major Uprising.

**Battles are rare.** A game averages 1.6 battles and 9.1 siege rolls, because neither bot gives the other good odds. REGROUP keeps Imperator's Legate armies out of reach, and Concilium never sweeps into danger. A human who takes risks will see more fighting.

**Close games.** 33% of games end on 11 or 12 VP, a point either side of the target, so every Governance point matters.

**VP distribution (VP: games):** 2: 1, 4: 2, 5: 6, 6: 7, 7: 22, 8: 28, 9: 38, 10: 42, 11: 50, 12: 50, 13: 38, 14: 13, 15: 3.

## 9. Limitations

* **These are computer opponents.** A strong human will beat the Heuristic and Lookahead players. Expect your results against Imperator to be better than theirs, and against Concilium perhaps much better.
* **The 2nd-edition card values are assumed.** The 2nd edition gives five cards 3 AP, three cards 1 AP and makes the rest 2 AP. Which cards carry which value is assumed. The card texts are 1st edition, and the 2nd edition changes some text. To check how much this matters, the main matchups were re-run on the same seeds with only the AP values changed. Only the card AP values were switched to their 1st-edition numbers; every other rule stayed at the 2nd-edition settings, on the same seeds. Imperator (level 3) beat Concilium in 41% of 300 games (38% with the assumed 2nd-edition values; Roman VP +0.18 ± 0.17), Imperator beat the Lookahead player in 34% of 120 (27%; +0.25 ± 0.35 VP), and Concilium under the standard rules beat the Lookahead player in 89% of 120 (94%; Roman VP +0.44 ± 0.39). The bots' rules work with either deck.
* **The Siege Table is the 1st-edition table shifted one row (−1).** It approximates the 2nd-edition table. The exact revised table has not been transcribed cell by cell, so siege results in the simulation are approximate. The printed bots use whatever table your copy of the game prints.
* **Rulebook ambiguities.** The 2023 rulebook still says 3 MP for a siege in section 14.3, while the 2nd-edition change notes say 2 MP; the bots use 2. Fading Promises appears in the index and the 2020 rules but not in the 2023 body; the engine applies it, as the engine audit response explains. The independent v1.0 audit raised the siege-MP point.
* **Simplifications in the engine.** Sorties and a few rare rules are simplified (see the audit response). They change the numbers a little but not the bots' rules.
* **Tuning targets.** Imperator was tuned against the Concilium, Heuristic and Lookahead players, so it may be tuned to their habits. Concilium was tuned against Imperator and the Heuristic player.

## 10. Reproducing the results

```
cd code
python3 tests/test_smoke.py           # smoke tests
python3 tests/test_audit_fixes.py     # regression tests for the v1.0 audit findings
python3 study.py                      # full study, about an hour on 2 cores
python3 decide.py 300                 # bot-vs-bot breakdown (section 8)
python3 sample_game.py 57 out.md      # the sample game's log
```

The sample game's introduction and narrative were written by hand, so the generated file reproduces the log but not those notes.

The raw results are in `results/study_final.json`, and the bot-vs-bot breakdown is in `results/decide.json`.
