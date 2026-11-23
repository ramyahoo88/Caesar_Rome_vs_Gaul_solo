"""Generate the narrated sample game (Imperator vs Concilium, both at level 3 = standard rules for
Concilium and +1 AP for Imperator)."""
import sys, re
from engine import Game, NAMES, REG_PROVS, PROVINCES, PROVINCIA
import engine
from bots import BotPolicy
from cards import CARDS

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 31
OUT = sys.argv[2] if len(sys.argv) > 2 else 'results/sample_game.md'

winter_notes = {}
_orig_gov = engine.Game.governance
_orig_wp = engine.Game.winter_phase


def wp(self):
    self._in_winter = True
    try:
        _orig_wp(self)
    finally:
        self._in_winter = False
        pc = self.prov_control()
        cel = (sum(1 for p in REG_PROVS['Celtica'] if pc[p] == 'R'), sum(1 for p in REG_PROVS['Celtica'] if pc[p] == 'G'))
        bel = (sum(1 for p in REG_PROVS['Belgica'] if pc[p] == 'R'), sum(1 for p in REG_PROVS['Belgica'] if pc[p] == 'G'))
        winter_notes[self.turn] = dict(cel=cel, bel=bel, ft=sum(1 for t in self.ctype if t == 'FT'),
                                       lost=[p for p in PROVINCIA if pc[p] != 'R'], vp=self.final_vp())


engine.Game.winter_phase = wp

g = Game({'R': BotPolicy('R', SEED), 'G': BotPolicy('G', SEED)}, seed=SEED, log=True, options={'ap_bonus_R': 1})
res = g.play()

lines = [f'# Sample game: Imperator (level 3) vs Concilium (level 4, standard rules)', '',
         f'Both sides are bots, so every decision below follows the printed rules. Seed {SEED}. '
         'Imperator gets +1 AP on every card play (its level 3); Concilium plays the standard rules (its level 4: Rome needs 12 VP). '
         'Lines starting with a Directive show the card turned over, the two cards of the Offer '
         '(* = Event Live for the bot) and the card chosen. "AP:" lines show the mission that spent each Action Point. '
         'Moves list the leader, the number of CUs, start and end space and the operations performed. '
         'Turns 1 and 2 are shown in full; later turns list only the cards played, combat, sieges, Tribes and VP.', '']
cur = None
for l in g.logs:
    m = re.match(r'T(\d+) (.*)', l)
    if not m:
        continue
    t, txt = int(m.group(1)), m.group(2)
    if t != cur:
        if cur is not None and cur in winter_notes:
            w = winter_notes[cur]
            lines.append('')
            lines.append(f'*End of Turn {cur}: Celtica provinces Rome {w["cel"][0]} / Gaul {w["cel"][1]}; Belgica Rome {w["bel"][0]} / Gaul {w["bel"][1]}; '
                         f'Fortified Towns {w["ft"]}; Provincia provinces lost: {", ".join(w["lost"]) or "none"}; Roman VP {w["vp"]}.*')
        cur = t
        lines += ['', f'## Turn {t}', '']
    keep_always = any(k in txt for k in ('battle', 'siege', 'surrender', 'falls', 'submit', 'eliminated', 'VP ', 'tribe ',
                                          'governance', 'displaced', 'intercepts', 'avoids', 'Caesar delayed', 'German tribe',
                                          'subjugated', 'cancels', 'native'))
    detailed = t <= 2
    if not detailed and not keep_always and not (txt.startswith('G plays') or txt.startswith('R plays')):
        continue
    if txt.startswith('G plays') or txt.startswith('R plays'):
        side = 'Concilium' if txt[0] == 'G' else 'Imperator'
        num = re.search(r'#(\d+)', txt).group(1)
        mode = txt.split(' as ')[-1]
        lines.append(f'- **{side}** plays #{num} {CARDS[int(num)]["title"]} as **{mode}**')
    elif txt.startswith('Imperator Directive') or txt.startswith('Concilium Directive'):
        lines.append(f'- {txt}')
    elif txt.startswith('  '):
        lines.append(f'    - {txt.strip()}')
    else:
        lines.append(f'    - {txt}')
if cur in winter_notes:
    w = winter_notes[cur]
    lines.append('')
    lines.append(f'*End of Turn {cur}: Celtica provinces Rome {w["cel"][0]} / Gaul {w["cel"][1]}; Belgica Rome {w["bel"][0]} / Gaul {w["bel"][1]}; '
                 f'Fortified Towns {w["ft"]}; Provincia provinces lost: {", ".join(w["lost"]) or "none"}; Roman VP {w["vp"]}.*')
lines += ['', f'**Result:** {"Rome" if res["winner"] == "R" else "Gaul"} wins ({res["reason"]}). '
          f'Battles {res["stats"]["battles"]}, siege rolls {res["stats"]["sieges"]}, Tribes eliminated {res["elim"]}, '
          f'Legions eliminated {res["elim_legions"]}.']
open(OUT, 'w').write('\n'.join(lines) + '\n')
print(res['winner'], res['reason'], len(lines), 'lines')
