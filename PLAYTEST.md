# Playtesting the Caesar solo bots

The bots have only been tested in simulation, so they still need games at the table. Use the [record sheet](print/Caesar_Solo_Record_Sheet.pdf), one per game. Each sheet takes about two minutes to fill in.

## What to record

1. **The level and the card edition.** The bots were simulated with an assumed 2nd-edition AP spread (five 3s, three 1s). If you play with the 2nd-edition cards, note any card whose AP value or text differs from the Event Guide summary.
2. **Governance points and VP each winter.** The final VP number alone can hide a game that was decided in Turn 2.
3. **Every time the bot looked wrong.** Write down the turn, the Directive, the Offer, the card and the rule section you applied. Most fixes in the Force 136 and Mincmistr bots came from notes like these.
4. **Rules you had to interpret.** Especially:
   - reach and MP counting with over-command (3);
   - the SWEEP target and army (5.3);
   - which Control Table or Agitate Table line applies (5.2, 6.2).
5. **Time per bot card.** The aim is under a minute. Note which missions are slow to resolve.

## Things to try first

- **Imperator, level 3 (you play Gaul).** Watch whether its armies get stranded out of supply, and whether PROTECT holds Provincia. Note how long the *danger* check (section 3) takes at the table: it drives REGROUP and the SWEEP limit. Note too whether the +1 AP bonus feels right.
- **Concilium, level 3 (you play Rome).** In simulation it beats every Roman computer player, including a lookahead player. A good human Rome may still find a pattern the computer players miss. Raiding Gallic bands leaving their Fortified Towns empty would be one such pattern. Note any you find.
- **One game of each bot at level 1.** This checks the unassisted rules.

## Sending results

Put your sheets, or a photo of them, in the repository's `playtests/` folder, or send them back in chat. Include the commit or version you played (v1.1).
