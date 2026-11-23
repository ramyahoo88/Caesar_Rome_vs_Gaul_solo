"""Lookahead hybrid: Imperator whose every AP is chosen by trying each mission on a copy of the game
(fresh dice) and keeping the best by the position evaluation.  Records the paper bot's choice next to
the lookahead's choice, to see where the printed mission order disagrees with lookahead."""
import sys, copy, statistics, json
from collections import Counter
from multiprocessing import Pool
from engine import Game
from bots import BotPolicy
from search import evaluate as sev

MISSIONS = ['CONTINUE', 'PROTECT', 'SUBMIT', 'REGROUP', 'SIEGE', 'STRIKE', 'RAID', 'RULE', 'SETTLE', 'INVADE', 'GATHER']


class HS(BotPolicy):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.pairs = Counter()

    def clone(self, g):
        pol = g.pol
        g.pol = None
        h = copy.deepcopy(g)
        g.pol = pol
        me = BotPolicy('R', 0); me.directive = self.directive; me.compass = self.compass
        h.pol = {'R': me, 'G': BotPolicy('G', 0)}
        h.logging = False
        h.rng.seed(self.rng.random())
        return h

    def spend_ap(self, g, side, ap):
        if side != 'R':
            return super().spend_ap(g, side, ap)
        d = self.directive or self.draw_directive()
        self.compass = d[2]
        paper = list(self.cfg['r_pre']) + list(d[1]) + list(self.cfg['r_post'])
        guard = 0
        while ap > 0 and guard < 12:
            guard += 1
            base = sev(g, side)
            vals = {}
            for m in MISSIONS:
                h = self.clone(g)
                try:
                    cost = h.pol['R'].try_mission(h, 'R', m, ap)
                except Exception:
                    cost = 0
                if cost:
                    vals[m] = sev(h, 'R') + (50 if h.winner == 'R' else 0) - base
            if not vals:
                break
            best = max(vals, key=vals.get)
            pc = next((m for m in paper if m in vals or (m == 'CONTROL' and 'SETTLE' in vals)), None)
            pc = 'SETTLE' if pc == 'CONTROL' else pc
            self.pairs[(pc, best, d[0])] += 1
            cost = self.try_mission(g, side, best, ap)
            if not cost:
                break
            ap -= cost


def one(seed):
    r = HS('R', seed)
    g = Game({'R': r, 'G': BotPolicy('G', seed)}, seed=seed, options={'ap_bonus_R': 1})
    res = g.play()
    return res['winner'], res['vp'], {f'{a}|{b}|{c}': n for (a, b, c), n in r.pairs.items()}


if __name__ == '__main__':
    n = int(sys.argv[1])
    with Pool(2) as p:
        out = p.map(one, range(18000, 18000 + n), chunksize=1)
    pairs = Counter()
    for w, vp, pr in out:
        pairs.update(pr)
    print('Rome wins', sum(w == 'R' for w, _, _ in out), '/', n, 'meanVP', statistics.mean(vp for _, vp, _ in out))
    agg = Counter()
    for k, v in pairs.items():
        a, b, c = k.split('|'); agg[(a, b)] += v
    tot = sum(agg.values())
    print('agreement', sum(v for (a, b), v in agg.items() if a == b) / tot, 'decisions', tot)
    for (a, b), v in agg.most_common(30):
        print(f'{a:9s} -> {b:9s} {v}')
    json.dump({k: v for k, v in pairs.items()}, open('hsearch_pairs.json', 'w'))
