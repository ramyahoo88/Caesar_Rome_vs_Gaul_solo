"""SearchRome / SearchGaul: one-step lookahead players (test opponents).

For every Action Point they list candidate actions (influence, army moves, sweeps,
Gallic council actions), try each on a copy of the game, score the copy with a
position evaluation and keep the best.  Slow but much stronger than the heuristics.
"""
import copy
from engine import (N, NAMES, ADJ, PROV, REGION, PROVINCES, REG_PROVS, GAUL_REGIONS, PROVINCIA, OTHER, Leader,
                    CARDS, HOPS, STYPE)
from heur import im_delta, all_influence_options
from smart import SmartPolicy, removal_value
from bots import BotPolicy
import events as EV


def evaluate(g, side):
    """Position value from Rome's point of view (positive good for Rome)."""
    gov = g.governance()
    pc = g.prov_control()
    turns_left = 7 - g.turn
    v_gov = 0.5 * gov + (1.2 if gov >= 7 else 0) + (1.2 if gov >= 9 else 0) - (6 if gov <= 3 else 0) - (1.5 if gov == 4 else 0)
    v = v_gov * (0.6 + 0.25 * turns_left)
    v += 1.0 * (g.vp + len(g.elim_tribes) / 4.0 - len(g.elim_legions))
    v += 0.22 * sum(u.steps for u in g.on_map('R', 'legion'))
    v -= 0.12 * sum(u.steps for u in g.on_map('G', 'tribe'))
    for s in range(N):
        if g.ctype[s] == 'FT':
            v -= 0.45 if REGION[s] == 'Celtica' else 0.3
    for reg, w in (('Celtica', 0.7), ('Belgica', 0.45), ('Aquitania', 0.3)):
        v += w * sum(1 for p in REG_PROVS[reg] if pc[p] == 'R')
        v -= w * sum(1 for p in REG_PROVS[reg] if pc[p] == 'G')
    for p in PROVINCIA:
        if pc[p] != 'R':
            v -= 1.0 if p != 'Narbonensis' else 2.0
    rim = sum(1 for s in range(N) if g.ctrl[s] == 'R' and g.ctype[s] == 'IM')
    gim = sum(1 for s in range(N) if g.ctrl[s] == 'G' and g.ctype[s] == 'IM')
    v += 0.08 * rim - 0.08 * gim
    v -= 0.15 * len(g.submitted) * (-1)  # submitted tribes are good for Rome
    v += 0.12 * g.council_ims * -1
    v += 1.0 if g.caesars_pass else 0
    return v if side == 'R' else -v


class _Quiet:
    pass


class SearchPolicy(SmartPolicy):
    name = 'search'

    def __init__(self, side, seed=0, samples=1, k_infl=6, **params):
        super().__init__(side, seed, **params)
        self.samples = samples
        self.k_infl = k_infl
        self.bot = BotPolicy(side, seed)

    def clone(self, g):
        pol = g.pol
        g.pol = None
        h = copy.deepcopy(g)
        g.pol = pol
        # reaction hooks in the copy use cheap heuristics
        h.pol = {'R': SmartPolicy('R', 0, noise=0.0), 'G': SmartPolicy('G', 0, noise=0.0)}
        h.logging = False
        return h

    def candidates(self, g, side):
        cands = []
        opts = all_influence_options(g, side)
        opts.sort(key=lambda a: -im_delta(g, side, a))
        for a in opts[:self.k_infl]:
            cands.append(('infl', a, 1))
        for leader, units, start in self.commands(g, side):
            v, plan = self.best_plan(g, side, leader, units, start)
            if plan:
                cands.append(('move', (leader, units, start, plan), 1))
        # sweeps (multiple IM removals)
        armies = self.bot.roman_armies(g) if side == 'R' else self.bot.gallic_armies(g)
        self.bot.compass = 'N'
        for leader, units, start in armies:
            v, plan = self.bot.raid_plan(g, side, leader, units, start, lambda s: 1)
            if plan and v >= 2:
                cands.append(('move', (leader, units, start, plan), 1))
        if side == 'G':
            for v, kind, arg, cost in self.gallic_specials(g, 2):
                cands.append((kind, arg, cost))
        return cands

    def apply(self, h, side, cand):
        kind, arg, cost = cand
        if kind == 'infl':
            EV.do_influence(h, side, arg)
        elif kind == 'move':
            leader, units, start, plan = arg
            # map objects into the clone
            if leader is not None:
                if isinstance(leader, Leader):
                    leader = h.leaders.get(leader.name)
                else:
                    leader = h.units[leader.uid]
            units = [h.units[u.uid] for u in units]
            h.activate(side, leader, units, plan)
        elif kind == 'council_put':
            h.council_ims += 1
        elif kind == 'council_take':
            SmartPolicy.council_take(h.pol[side], h)
        elif kind == 'uprising':
            SmartPolicy.major_uprising(h.pol[side], h)
        elif kind == 'devastate':
            h.devast.add(arg)
            if h.ctype[arg] == 'IM':
                h.remove_im(arg)

    def spend_ap(self, g, side, ap):
        guard = 0
        while ap > 0 and guard < 10:
            guard += 1
            base = evaluate(g, side)
            best = None
            for cand in self.candidates(g, side):
                if cand[2] > ap:
                    continue
                tot = 0
                for k in range(self.samples):
                    h = self.clone(g)
                    h.rng.seed(self.rng.random())
                    try:
                        self.apply(h, side, cand)
                    except Exception:
                        tot = -1e9
                        break
                    if h.winner == side:
                        tot += 50
                    tot += evaluate(h, side)
                val = tot / self.samples - base
                if best is None or val > best[0]:
                    best = (val, cand)
            if best is None or best[0] < -0.5:
                break
            ap -= best[1][2]
            self.apply(g, side, best[1])
