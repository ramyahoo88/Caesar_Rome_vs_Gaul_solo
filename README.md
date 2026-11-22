# Caesar: Rome vs. Gaul (2nd edition) — solo bots

Two card-driven paper bots for GMT Games' *Caesar: Rome vs. Gaul*, 2nd edition:

* **Imperator** plays Rome.
* **Concilium** plays Gaul.

You play the other side. The bot uses the same cards, units, dice and rules as a human player:

* its hand stays face down and it never looks at yours;
* it rolls only the dice the game rolls;
* it gets no free units.

Each decision comes from a **Directive card** (a mission order plus a compass point for tie-breaks) and a two-card **Offer** drawn from its hand. Five difficulty levels per bot change only Action Points or the VP target.

This is an unofficial fan variant, not a GMT publication. You need the game to play.

## Print and play

All files are in [`print/`](print):

| File | What it is |
|---|---|
| [Caesar_Solo_Print_and_Play.pdf](print/Caesar_Solo_Print_and_Play.pdf) | Everything below in one file |
| [Caesar_Solo_Rules.pdf](print/Caesar_Solo_Rules.pdf) | Bot rules, including the Event Guides and levels (9 pages) |
| [Caesar_Solo_Cards.pdf](print/Caesar_Solo_Cards.pdf) | 18 Directive cards: 9 Imperator and 9 Concilium, poker size, 9 per page |
| [Caesar_Solo_Reference.pdf](print/Caesar_Solo_Reference.pdf) | Two-page reference sheet: turn sequence, mission lists, Control and Agitate tables |
| [Caesar_Solo_Record_Sheet.pdf](print/Caesar_Solo_Record_Sheet.pdf) | Game record sheet for playtesting |
| [Caesar_Solo_Sample_Game.pdf](print/Caesar_Solo_Sample_Game.pdf) | A full bot-vs-bot game, card by card |
| [Caesar_Solo_Sim_Report.pdf](print/Caesar_Solo_Sim_Report.pdf) | How the bots were tested, and the results |

`Caesar_Solo_Rules.md` is the editable source. Run `python3 print/build.py` to rebuild the PDFs. It needs Python-Markdown, pypdf and Chrome or Chromium.

## Quick start

1. Set up the game normally. Pick the side you will play.
2. Cut out the bot's 9 Directive cards and shuffle them face down.
3. Deal the bot's hand face down. Each time it plays, turn over a Directive card, reveal two cards from its hand, and follow section 2 of the rules.
4. Start at **level 3** for either bot (section 7).

## Levels

| Level | Imperator (bot is Rome) | Concilium (bot is Gaul) |
|---|---|---|
| 1 | Rules only | Rome wins at 9 VP |
| 2 | +1 AP on its first 4 card plays each turn | Rome wins at 10 VP |
| 3 | +1 AP on every card play | Standard rules |
| 4 | +1 AP on every play, and wins at 10 VP | +1 AP on its first 4 card plays each turn |
| 5 | +1 AP on every play, and wins at 9 VP | +1 AP on every card play |

## How it was tested

The [`code/`](code) folder holds a Python engine for the full 2nd-edition rules (about 2,000 lines). It also has four computer opponents for each side:

* the paper bot itself;
* a heuristic player;
* an aggressive variant of the heuristic player;
* a one-ply lookahead player that searches each card play.

Thousands of games tuned the Directive decks and mission rules. The final study then ran every level against every opponent, on seeds never used during development. The details are in the [simulation report](print/Caesar_Solo_Sim_Report.md).

The engine was audited against the 2023 living rules by an independent reviewer. That report and the response are in [`audit/`](audit).

```
cd code
python3 -c "from harness import evaluate, line; print(line(evaluate(('bot',{}),('bot',{}),range(20)),'bot v bot'))"
python3 sample_game.py 33 sample.md        # a narrated bot-vs-bot game
python3 study.py                           # the full study (about an hour on 2 cores)
```

## Known assumptions

* The game data were extracted from the 1st-edition Vassal module and corrected to the 2nd-edition rules. That covers the map graph, counters and card texts.
* The 2nd edition changes the AP values of some cards: five cards are 3s, three are 1s and the rest are 2s. Which cards carry which value is assumed (`code/cards.py`). If a card's AP or text differs in your copy, play it as printed. The bots read the card in front of them.
* The engine does not model sorties from a siege and a few rare rules. The [audit response](audit/ENGINE_AUDIT_RESPONSE.md) lists them. They affect the simulation numbers, not the paper rules.

## Feedback

See [PLAYTEST.md](PLAYTEST.md). Table results are the most useful thing at this stage.
