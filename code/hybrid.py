from bots import BotPolicy
from heur import im_delta, all_influence_options
from smart import SmartPolicy

class BotSmartControl(BotPolicy):
    """Imperator with the heuristic (im_delta) influence choice instead of the Control Table."""
    def roman_control_choice(self, g, allowed=None):
        opts = allowed if allowed is not None else all_influence_options(g, 'R')
        if not opts:
            return None
        return max(opts, key=lambda a: im_delta(g, 'R', a))

class BotCardsSmart(BotPolicy):
    """Imperator but card choice by the Smart heuristic (sees whole hand)."""
    def choose_play(self, g, side):
        d = self.draw_directive(); self.compass = d[2]
        return SmartPolicy.choose_play(self._sm(g, side), g, side)
    def _sm(self, g, side):
        if not hasattr(self, '_smart'):
            self._smart = SmartPolicy(side, 0, noise=0.0)
        return self._smart

import copy
from search import evaluate as sev
from collections import Counter

class BotSearchMissions(BotPolicy):
    """Each AP: try every Imperator mission on a copy, keep the one the evaluation likes best."""
    MISSIONS = ['CONTINUE', 'PROTECT', 'SIEGE', 'STRIKE', 'RAID', 'INVADE', 'MARCH', 'GATHER', 'CONTROL']
    stats = Counter()

    def spend_ap(self, g, side, ap):
        d = self.directive or self.draw_directive()
        self.compass = d[2]
        guard = 0
        while ap > 0 and guard < 12:
            guard += 1
            base = sev(g, side)
            best = None
            for m in (self.MISSIONS if side == 'R' else ['RISE', 'AMBUSH', 'RAID', 'AGITATE', 'BANK']):
                h = self.clone(g)
                me = h.pol[side]
                try:
                    cost = me.try_mission(h, side, m, ap)
                except Exception:
                    cost = 0
                if not cost:
                    continue
                v = sev(h, side) + (50 if h.winner == side else 0) - base
                if best is None or v > best[0]:
                    best = (v, m)
            if best is None:
                break
            BotSearchMissions.stats[best[1]] += 1
            cost = self.try_mission(g, side, best[1], ap)
            if not cost:
                break
            ap -= cost

    def clone(self, g):
        pol = g.pol
        g.pol = None
        h = copy.deepcopy(g)
        g.pol = pol
        from smart import SmartPolicy
        me = BotPolicy(self.side, 0)
        me.directive = self.directive; me.compass = self.compass
        h.pol = {self.side: me, ('G' if self.side == 'R' else 'R'): SmartPolicy('G' if self.side == 'R' else 'R', 0, noise=0.0)}
        h.logging = False
        h.rng.seed(self.rng.random())   # no peeking at future dice
        return h
