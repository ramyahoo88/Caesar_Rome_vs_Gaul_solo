"""Heuristic decision makers.

BasePolicy  -- defaults for every engine hook (reaction rolls, losses, retreats, rerolls...).
SmartPolicy -- a flexible computer player used as the test opponent (sees its whole hand,
               scores every option).  Parameters create a family of styles.
"""
import random
from engine import (N, NAMES, IDX, ADJ, EDGE, PROV, REGION, STYPE, PROVINCES, REG_PROVS, GAUL_REGIONS,
                    PROVINCIA, OTHER, Leader, Unit, GERMANIA_VP, BRITANNIA_VP, OCTODURUS, BRIGANTIUM,
                    battle_result, odds_col, CARDS, SEA, GERMAN_SH, WC_GARRISON)
from heur import (reach, path_to, stack_strength, gallic_army_at, roman_army_at, im_delta, best_influence,
                  all_influence_options, enemy_outside_at, gov_and_provs, prov_margin)

# probability that 2d6 + drm >= 9
P9 = {}
for drm in range(-6, 10):
    c = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b + drm >= 9)
    P9[drm] = c / 36


def p_success(drm):
    return P9[max(-6, min(9, drm))]


def expected_hits(strength, roman=False):
    tot = 0
    for a in range(1, 7):
        for b in range(1, 7):
            r = (max(3, a) + max(3, b)) if roman else a + b
            tot += battle_result(strength, r)[0]
    return tot / 36


def win_prob(att_bs, dfn_bs, att_roman, dfn_roman, rr_a=0, rr_d=0):
    """Rough probability attacker wins (more hits) ignoring rerolls except as a bonus."""
    win = 0
    da = [(max(3, a) + max(3, b)) if att_roman else a + b for a in range(1, 7) for b in range(1, 7)]
    dd = [(max(3, a) + max(3, b)) if dfn_roman else a + b for a in range(1, 7) for b in range(1, 7)]
    ra = [battle_result(att_bs, x) for x in da]
    rd = [battle_result(dfn_bs, x) for x in dd]
    for x in ra:
        for y in rd:
            if x > y:
                win += 1
            elif x == y:
                win += 0.3
    p = win / (36 * 36)
    p += 0.04 * (rr_a - rr_d)
    return max(0.0, min(1.0, p))


class BasePolicy:
    name = 'base'

    def __init__(self, side, seed=0, **params):
        self.side = side
        self.rng = random.Random(seed * 7 + (1 if side == 'R' else 2))
        self.p = dict(aggr=1.0, infl=1.0, noise=0.15, event_bias=0.0, avoid_ratio=0.85, intercept_ratio=1.3)
        self.p.update(params)

    # -------------------------------------------------------------- generic choices
    def noise(self):
        return self.rng.random() * self.p['noise']

    def choose_space(self, g, side, opts, purpose):
        if not opts:
            return None
        if purpose == 'im_relocate':
            return max(opts, key=lambda s: im_delta(g, side, ('place', s)))
        if purpose in ('remove_enemy_im', 'convert'):
            def val(s):
                old = (g.ctrl[s], g.ctype[s])
                g.ctrl[s] = None; g.ctype[s] = None; g._pc_cache = None
                gov, r, gl = gov_and_provs(g)
                g.ctrl[s], g.ctype[s] = old; g._pc_cache = None
                gov0, r0, gl0 = gov_and_provs(g)
                if side == 'R':
                    v = (gov - gov0) * 10 + (gl0 - gl) * 4
                else:
                    v = (gov0 - gov) * 10 + (r0 - r) * 4 + (2 if REGION[s] == 'Provincia' else 0)
                if purpose == 'convert':
                    v += im_delta(g, side, ('place', s)) if True else 0
                return v + self.noise()
            return max(opts, key=val)
        if purpose == 'caesar':
            return max(opts, key=lambda s: (sum(u.steps for u in g.units.values() if u.loc == s and u.kind == 'legion'),
                                            -abs(REGION[s] == 'Provincia')))
        if purpose.startswith('legate'):
            def lv(s):
                leg = sum(1 for u in g.units.values() if u.loc == s and u.kind == 'legion')
                has = any(l.loc == s for l in g.leaders.values())
                return (leg if not has else leg * 0.1, -s)
            return max(opts, key=lv)
        if purpose in ('reinforce', 'replace'):
            cz = g.leaders.get('Caesar')
            if cz and isinstance(cz.loc, int) and cz.loc in opts:
                return cz.loc
            return opts[0]
        if purpose.startswith('leader_arrival') or purpose == 'winter_leader':
            # with the biggest Gallic group, else in a fortified space
            return max(opts, key=lambda s: (sum(u.strength() for u in g.units.values() if u.loc == s and u.side == 'G'),
                                            g.ctype[s] == 'FT', -s))
        if purpose == 'devastate':
            def dv(s):
                v = 0
                if g.ctrl[s] == 'R' and g.ctype[s] == 'IM':
                    v += 3
                if g.ctrl[s] == 'G':
                    v -= 3
                if any(t for t, k in ADJ[s] if any(u.loc == t and u.side == 'R' and u.kind == 'legion' for u in g.units.values())):
                    v += 1
                return v + self.noise()
            best = max(opts, key=dv)
            return best if dv(best) > 0.5 else None
        if purpose in ('mercenary', 'militia', 'minor_tribe'):
            def mv(s):
                rs = [u for u in g.units.values() if u.side == 'R' and isinstance(u.loc, int) and
                      (u.loc == s or (s, u.loc) in EDGE)]
                return (len(rs), sum(u.strength() for u in g.units.values() if u.loc == s and u.side == 'G'))
            return max(opts, key=mv)
        if purpose == 'cavalry':
            cz = g.leaders.get('Caesar')
            if cz and cz.loc in opts:
                return cz.loc
            return opts[0]
        if purpose == 'upgrade_ft':
            def fv(s):
                return sum(1 for u in g.units.values() if u.side == 'R' and isinstance(u.loc, int) and
                           (u.loc == s or (s, u.loc) in EDGE))
            return max(opts, key=fv)
        if purpose == 'siege_point':
            return max(opts, key=lambda s: g.siege.get(s, 0))
        if purpose == 'labienus':
            cz = g.leaders.get('Caesar')
            def lab(s):
                has = any(l.loc == s for l in g.leaders.values())
                return (not has, sum(1 for u in g.units.values() if u.loc == s and u.kind == 'legion'))
            return max(opts, key=lab)
        if purpose == 'aedui':
            return opts[0]
        return opts[0]

    def choose_influence(self, g, side, opts, purpose):
        return max(opts, key=lambda a: im_delta(g, side, a) + self.noise())

    def choose_province(self, g, side, provs, purpose):
        def v(p):
            return sum(1 for s in PROVINCES[p]['idx'] if g.ctrl[s] == 'R' and g.ctype[s] == 'IM') + \
                (3 if g.prov_control()[p] == 'R' else 0)
        return max(provs, key=v)

    def choose_region(self, g, side, regs, purpose):
        def v(r):
            return sum(1 for p in REG_PROVS[r] for s in PROVINCES[p]['idx'] if g.ctrl[s] == 'R' and g.ctype[s] == 'IM')
        return max(regs, key=v)

    def choose_unit(self, g, side, units, purpose):
        return max(units, key=lambda u: u.cs[-1])

    def choose_leader(self, g, side, leaders, purpose):
        if purpose == 'recall':
            if side == 'R':
                return min(leaders, key=lambda l: l.br)
            return max(leaders, key=lambda l: l.br)
        return max(leaders, key=lambda l: (sum(1 for u in g.units.values() if u.loc == l.loc and u.kind == 'legion'), l.br))

    def choose_german_start(self, g, side, shs):
        # enter next to the enemy's influence
        best, bv = None, 0
        for sh in shs:
            for e in GERMAN_SH[sh]:
                v = 1 if g.ctrl[e] == OTHER[side] else 0
                if v > bv:
                    best, bv = sh, v
        return best if best else (shs[0] if self.rng.random() < 0.5 else None)

    def choose_german_dest(self, g, side, dests):
        def v(s):
            val = 0
            if g.ctrl[s] == OTHER[side] and g.ctype[s] == 'IM':
                val += 3
            if g.ctrl[s] == side:
                val -= 3
            # block enemy supply/province
            return val + self.noise()
        best = max(dests, key=v)
        return best

    # -------------------------------------------------------------- battle hooks
    def choose_losses(self, g, side, units, hits, reason='battle'):
        units = [u for u in units if u.steps > 0]
        regular = [u for u in units if u.kind in ('legion', 'tribe')]
        mercs = [u for u in units if u.merc]
        leaders = [u for u in units if u.is_leader]
        order = []
        # 1) flip full-strength regulars (non-elite first, weakest first)
        full = sorted([u for u in regular if u.full()], key=lambda u: (u.elite, u.cs[-1]))
        order += full
        # 2) then mercenaries (allowed once all regulars are reduced)
        order += mercs
        # 3) then reduced regulars (weakest first)
        order += sorted([u for u in regular], key=lambda u: u.cs[0])
        order += leaders
        return order

    def reroll_choice(self, g, side, my_bs, opp_bs, mine, theirs, side_is_attacker, opp_side):
        roman = side == 'R'; oroman = opp_side == 'R'
        def val(m, t):
            a = (max(3, m[0]) + max(3, m[1])) if roman else m[0] + m[1]
            b = (max(3, t[0]) + max(3, t[1])) if oroman else t[0] + t[1]
            x = battle_result(my_bs, a); y = battle_result(opp_bs, b)
            return (x[0] - y[0]) + (0.6 if x > y else (-0.6 if y > x else 0))
        base = val(mine, theirs)
        best, bv = None, base + 0.05
        for i in range(2):
            ev = sum(val([v if j == i else mine[j] for j in range(2)], theirs) for v in range(1, 7)) / 6
            if ev > bv:
                best, bv = ('own', i), ev
            ev2 = sum(val(mine, [v if j == i else theirs[j] for j in range(2)]) for v in range(1, 7)) / 6
            if ev2 > bv:
                best, bv = ('opp', i), ev2
        return best

    def retreat_inside(self, g, side, s, units):
        return True

    def choose_retreat(self, g, side, units, s, dests):
        def v(t):
            val = 0
            if any(u.loc == t and u.side == OTHER[side] for u in g.units.values()):
                val -= 10
            if g.ctrl[t] == side:
                val += 2
            elif g.ctrl[t] == OTHER[side]:
                val -= 3
            if any(u.loc == t and u.side == side for u in g.units.values()):
                val += 2
            if EDGE.get((s, t)) == 'channel':
                val -= 3
            return val
        return max(dests, key=v)

    def inside_outside(self, g, side, s, defenders, movers):
        mine = stack_strength([u for u in defenders]) + g.local_support(side, s)
        theirs = stack_strength(movers) + g.local_support(OTHER[side], s)
        if side == 'G' and theirs >= 3 * mine:
            return list(defenders)
        if mine >= theirs * 1.1:
            return []
        return list(defenders)

    def avoid(self, g, side, s, units, movers, prev):
        mine = stack_strength(units) + g.local_support(side, s)
        theirs = stack_strength(movers) + g.local_support(OTHER[side], s)
        if side == 'G' and theirs >= 3 * mine:
            return True
        return mine < theirs * self.p['avoid_ratio']

    def avoid_dest(self, g, side, s, units, dests):
        return max(dests, key=lambda t: (g.ctrl[t] == side, any(u.loc == t and u.side == side for u in g.units.values()), -t))

    def intercept(self, g, side, to, frm, movers, mleader, candidates):
        mstr = stack_strength(movers) + g.local_support(OTHER[side], to)
        best = None
        for t, (us, ls, k) in candidates.items():
            us = [u for u in us if not u.inside]
            if not us:
                continue
            here = [u for u in g.units.values() if u.loc == to and u.side == side and not u.inside]
            mine = stack_strength(us) + stack_strength(here) + g.local_support(side, to)
            if side == 'G' and mstr >= 3 * mine:
                continue
            if mine >= mstr * self.p['intercept_ratio']:
                lead = None
                if side == 'R' and ls:
                    lead = max(ls, key=lambda l: l.br)
                if best is None or mine > best[0]:
                    best = (mine, t, us, lead)
        if best:
            return {best[1]: (best[2], best[3])}
        return None

    def back_up(self, g, side, units, leader, to, frm):
        mine = stack_strength(units)
        theirs = stack_strength([u for u in g.units.values() if u.loc == to and u.side == OTHER[side]])
        return mine < theirs

    def use_remedies(self, g, side, roller, drm):
        return False

    def use_vow_battle(self, g, side, s, a_bs, d_bs, attacker):
        return abs(a_bs - d_bs) <= 3

    def use_vow_siege(self, g, s):
        return True

    def discard_surprise(self, g, side, sur):
        return False

    def react(self, g, side, c):
        return CARDS[c]['kind'] == 'event' and c in (4, 11, 16, 53, 5, 6, 14, 36, 12, 8, 21, 27)

    def choose_ims_to_remove(self, g, ims, n):
        # remove the least valuable Roman IMs (outside controlled provinces)
        pc = g.prov_control()
        return sorted(ims, key=lambda s: (pc[PROV[s]] == 'R', REGION[s] == 'Provincia'))[:n]

    def choose_caesar_relocation(self, g, opts):
        return max(opts, key=lambda s: sum(1 for u in g.units.values() if u.loc == s and u.kind == 'legion'))

    def emergency_replacements(self, g, prov_ims):
        return []

    def choose_replacement(self, g, red):
        return red[0]

    def keep_legate(self, g):
        ls = [l for l in g.leaders.values() if l.name != 'Caesar']
        if not ls:
            return None
        best = max(ls, key=lambda l: (l.br, l.cr))
        return best.name if best.br >= 2 else None

    def play_winter_campaign(self, g):
        return False

    def winter_campaign_move(self, g):
        pass

    # -------------------------------------------------------------- reinforcements
    def choose_reinforcements(self, g, drawn):
        # keep the three strongest that have a legal space; return the weakest
        drawn = sorted(drawn, key=lambda u: (len(g.legal_tribe_spaces(u)) > 0, u.cs[-1]), reverse=True)
        return drawn[:3], drawn[3:]

    def place_tribe_choice(self, g, u, spaces, council_ok):
        if not spaces:
            return 'council'
        def v(s):
            val = 0
            # fortified towns far from Roman legions survive longer
            close = sum(u2.strength() for u2 in g.units.values() if u2.side == 'R' and isinstance(u2.loc, int)
                        and (u2.loc, s) in EDGE)
            val -= close
            if g.ctrl[s] == 'G':
                val -= 0.5
            return val + self.noise()
        return max(spaces, key=v)

    def spring_muster(self, g):
        return

    # -------------------------------------------------------------- winter
    def winter_camp(self, g):
        # spread legions so that each space holds at most its forage level
        legs = sorted(g.on_map('R', 'legion'), key=lambda u: -u.steps)
        load = {}
        for u in legs:
            dist, parent = reach(g, 'R', u.loc, 3, 99, 1)
            best = None
            for t, d in dist.items():
                if g.german_tribe() and g.german_tribe().loc == t:
                    continue
                cap = g.forage(t)
                if load.get(t, 0) >= cap:
                    continue
                # prefer neutral Gallic spaces near Roman IMs (they gain an IM at end of winter)
                val = 0
                pc = g.prov_control()
                if g.ctrl[t] == 'R' and pc[PROV[t]] == 'R':
                    val += 3
                elif g.ctrl[t] == 'R':
                    val += 2
                elif g.ctrl[t] is None and REGION[t] in GAUL_REGIONS:
                    val += 1
                val -= d * 0.2
                if best is None or val > best[0]:
                    best = (val, t)
            if best is None:
                continue
            t = best[1]
            load[t] = load.get(t, 0) + 1
            if t != u.loc:
                g.winter_camp_move(u, path_to(parent, t))
