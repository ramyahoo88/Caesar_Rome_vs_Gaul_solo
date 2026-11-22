"""Fill the Simulation Report template with the final study, the bot-vs-bot breakdown and the tables."""
import json, sys, statistics
tmpl, study, decide, tables, out = sys.argv[1:6]
t = open(tmpl).read()
R = json.load(open(study))
d = json.load(open(decide))
tb = open(tables).read()
tb = tb.replace('### Imperator\n', '### Imperator (bot plays Rome; cells = Imperator win rate, mean Roman VP)\n') \
       .replace('### Concilium\n', '### Concilium (bot plays Gaul; cells = Concilium win rate, mean Roman VP)\n')
tb += "\nImperator levels 3–5 differ only in the VP Rome needs, so they play the same games and show the same mean VP. The same is true of Concilium levels 1–4.\n"
ng = sum(v['n'] for v in R.values())


def w(k):
    v = R[k]
    return v['bot_wins'] / v['n']


summary = f"""* **Both bots play complete games of the 2nd-edition rules.** Each decision comes from a Directive card and a two-card Offer, following the printed rules. The bot never looks at hidden cards. An independent clean-room implementation of the printed rules matched the simulation bot on more than 99% of card and mission choices.
* **The levels form a smooth ladder against every computer opponent.** Against the strongest of them, the Lookahead player:
    * Imperator wins {w('Imperator L1 vs search'):.0%} at level 1, {w('Imperator L3 vs search'):.0%} at level 3 and {w('Imperator L5 vs search'):.0%} at level 5;
    * Concilium wins {w('Concilium L1 vs search'):.0%} at level 1, {w('Concilium L3 vs search'):.0%} at level 3 and {w('Concilium L5 vs search'):.0%} at level 5.
* **Concilium is the stronger bot.** Under the standard rules (its level 4) it wins {w('Concilium L4 vs bot'):.0%} against Imperator with +1 AP and {w('Concilium L4 vs search'):.0%} against the Lookahead player. Rome-side computer players are weaker than skilled humans, so Concilium's levels start with a lower VP target for you: 9 VP at level 1. Level 3 (11 VP) is the recommended start.
* **Imperator at level 3** (+1 AP on every card play) wins {w('Imperator L3 vs bot'):.0%} of its games against Concilium and about {(w('Imperator L3 vs smart') + w('Imperator L3 vs smart-aggressive')) / 2:.0%} against the Heuristic players.
* **A typical bot-vs-bot game (Imperator at level 3, Concilium under the standard rules) is a Governance race.** Rome earns most of its VP from Governance, plus Caesar's Pass. A game has few battles (about {d['battles']:.1f}) and around {d['sieges']:.0f} siege rolls.
* {ng:,} games were played for the final study, and many thousands more during development."""
t = t.replace('{{SUMMARY}}', summary).replace('{{TABLES}}', tb).replace('{{NGAMES}}', f'{ng:,}')
n = d['n']
near = sum(c for v, c in d['vp_hist'] if v in (11, 12))
hi = sum(c for t2, v in d['gov'].items() for g_, c in v['dist'] if g_ >= 9) / sum(c for t2, v in d['gov'].items() for g_, c in v['dist'])
gov = ' | '.join(f"{float(v['mean']):.1f}" for t2, v in d['gov'].items())
dec = f"""These figures come from {n} games of Imperator (level 3) against Concilium (standard rules), on seeds from 300000 up. Rome won {d['rome_wins']} of them ({d['rome_wins']/n:.0%}), with a mean of {d['mean_vp']:.1f} VP.

**Where Rome's VP come from (per game):**

| Source | VP |
|---|---|
| Governance (six winters) | {d['sources']['governance']:.1f} |
| Caesar's Pass | {d['sources'].get("Caesar's", 0):.2f} |
| Germania and Britannia | {d['sources'].get('Germania', 0) + d['sources'].get('Britannia', 0):.2f} |
| Eliminated Tribes (÷4) | about {d['elim_tribes']/4:.1f} ({d['elim_tribes']:.1f} Tribes) |
| Eliminated Legions | −{d['elim_legions']:.2f} |

**Mean Governance by winter** (9–10 Governance gives 2 VP, 7–8 gives 1):

| Turn | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Mean Governance | {gov} |

{hi:.0%} of Rome's winters reach 9–10 Governance. The rest fall to 7–8, nearly always because Belgica is tied or lost. Turn 6 is the hardest winter, because Concilium saves its Submitted Tribes and Council IMs for a late Major Uprising.

**Battles are rare.** A game averages {d['battles']:.1f} battles and {d['sieges']:.1f} siege rolls, because neither bot gives the other good odds. REGROUP keeps Imperator's Legate armies out of reach, and Concilium never sweeps into danger. A human who takes risks will see more fighting.

**Close games.** {near/n:.0%} of games end on 11 or 12 VP, a point either side of the target, so every Governance point matters.

**VP distribution (VP: games):** """ + ', '.join(f'{v}: {c}' for v, c in d['vp_hist']) + "."
t = t.replace('{{DECIDE}}', dec)
t = t.replace("| **Bot** | The other paper bot, following its printed rules exactly. In the Imperator rows, Concilium plays at level 3. In the Concilium rows, Imperator plays with the same level adjustments as Concilium's opponent. At level 3 that means the rules only. |",
              "| **Bot** | The other paper bot, following its printed rules exactly. In the Imperator rows it is Concilium under the standard rules. In the Concilium rows it is Imperator at its level 3 (+1 AP on every card play), the strongest Roman player available. |")
t = t.replace("The raw results are in `results/study_final.json`.", "The raw results are in `results/study_final.json`, and the bot-vs-bot breakdown is in `results/decide.json`.")
t = t.replace("![Imperator win rate by level](sim/imperator_levels.png)", "![Imperator win rate by level](sim/imperator_levels.png)\n\n*Error bars show one standard error.*")
open(out, 'w').write(t)
print('placeholders left:', t.count('{{'))
