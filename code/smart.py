"""SmartPolicy: flexible heuristic computer player (test opponent and building block for the bots)."""
from engine import (N, NAMES, IDX, ADJ, EDGE, PROV, REGION, STYPE, PROVINCES, REG_PROVS, GAUL_REGIONS,
                    PROVINCIA, OTHER, Leader, Unit, GERMANIA_VP, BRITANNIA_VP, OCTODURUS, BRIGANTIUM,
                    battle_result, odds_col, CARDS, SEA, GERMAN_SH, WC_GARRISON, HOPS)
from heur import (reach, path_to, stack_strength, gallic_army_at, roman_army_at, im_delta, best_influence,
                  all_influence_options, enemy_outside_at, gov_and_provs, prov_margin)
from policies import BasePolicy, win_prob, p_success
import events as EV

VP_SPACES = set(GERMANIA_VP + BRITANNIA_VP)
_SEV = {}


def removal_value(g, side, s):
    """Value for `side` of removing the enemy IM at s."""
    old = (g.ctrl[s], g.ctype[s])
    gov0, r0, gl0 = gov_and_provs(g)
    g.ctrl[s] = None; g.ctype[s] = None; g._pc_cache = None
    gov, r, gl = gov_and_provs(g)
    g.ctrl[s], g.ctype[s] = old; g._pc_cache = None
    if side == 'R':
        v = (gov - gov0) * 10 + (gl0 - gl) * 4 + 1.0
        if s in VP_SPACES:
            others = [t for t in (GERMANIA_VP if s in GERMANIA_VP else BRITANNIA_VP) if t != s]
            v += 8 if all(g.ctrl[t] != 'G' for t in others) else 4
    else:
        v = (gov0 - gov) * 10 + (r0 - r) * 4 + 1.0 + (2 if REGION[s] == 'Provincia' else 0)
    return v


class SmartPolicy(BasePolicy):
    name = 'smart'

    # ============================================================ commands
    def commands(self, g, side, only=None):
        """Possible activations: list of (leader or None, units list, start)."""
        cmds = []
        used = set()
        if side == 'R':
            for l in sorted(g.leaders.values(), key=lambda l: -l.br):
                if not isinstance(l.loc, int) or l.moved:
                    continue
                if only is not None and l not in only:
                    continue
                us = [u for u in g.units.values() if u.loc == l.loc and u.side == 'R' and not u.moved and not g.unit_besieged(u)]
                us.sort(key=lambda u: (-u.strength(), u.merc))
                take = us[:l.cr] if len(us) > l.cr else us
                if l.name == 'Caesar' and len(us) > l.cr and len(us) <= l.cr + 3:
                    take = us   # big army, accept the slower pace
                cmds.append((l, take, l.loc))
                used |= {u.uid for u in take}
            stacks = {}
            for u in g.on_map('R', 'legion'):
                if u.moved or u.uid in used or g.unit_besieged(u):
                    continue
                if only is not None and u not in only:
                    continue
                if any(l.loc == u.loc for l in g.leaders.values()) and only is None:
                    continue
                stacks.setdefault(u.loc, []).append(u)
            for s, us in stacks.items():
                us.sort(key=lambda u: -u.strength())
                merc = [u for u in g.units.values() if u.loc == s and u.side == 'R' and u.merc and not u.moved]
                cmds.append((None, (us + merc)[:2], s))
        else:
            for u in g.on_map('G', 'gleader'):
                if u.moved or g.unit_besieged(u) or (only is not None and u not in only):
                    continue
                us = [x for x in g.units.values() if x.loc == u.loc and x.side == 'G' and not x.moved and x is not u
                      and not g.unit_besieged(x) and x.kind != 'gleader']
                if u.name == 'Ambiorix':
                    us = [x for x in us if x.region == 'Belgic' or x.merc]
                us.sort(key=lambda x: -x.strength())
                take = us[:u.cr]
                cmds.append((u, take, u.loc))
                used |= {x.uid for x in take} | {u.uid}
            for u in g.on_map('G'):
                if u.uid in used or u.moved or u.kind not in ('tribe', 'merc') or g.unit_besieged(u):
                    continue
                if u.merc and u.ma == 0:
                    continue
                if only is not None and u not in only:
                    continue
                others = [x for x in g.units.values() if x.loc == u.loc and x.side == 'G' and x is not u and not x.moved
                          and x.uid not in used and x.kind in ('tribe', 'merc') and not g.unit_besieged(x)]
                others.sort(key=lambda x: -x.strength())
                take = [u] + others[:1]
                used |= {x.uid for x in take}
                cmds.append((None, take, u.loc))
        return cmds

    def command_ma(self, g, side, leader, units, ma_override=None):
        if ma_override is not None:
            return ma_override
        if leader is not None:
            if isinstance(leader, Leader) and not units:
                return 7
            return leader.ma
        movers = [u for u in units if u.ma > 0]
        return min(u.ma for u in movers) if movers else 0

    def threat(self, g, side):
        """Enemy combat strength able to strike each space (within 2 hops)."""
        enemy = OTHER[side]
        th = [0.0] * N
        for u in g.units.values():
            if u.side != enemy or not isinstance(u.loc, int):
                continue
            st = u.strength()
            for t in range(N):
                h = HOPS[u.loc][t]
                if h <= 2:
                    th[t] += st if h <= 1 else st * 0.6
        if enemy == 'R':
            for l in g.leaders.values():
                if l.name == 'Caesar' and isinstance(l.loc, int):
                    for t in range(N):
                        if HOPS[l.loc][t] <= 2:
                            th[t] *= 1.3
        return th

    def approach_targets(self, g, side, my_cs, is_caesar):
        tg = []
        if side == 'R':
            for s in range(N):
                if g.ctype[s] == 'FT':
                    inside = sum(u.strength() for u in g.units.values() if u.loc == s and u.side == 'G')
                    if my_cs >= 4:
                        tg.append((s, 3.0 + (1.0 if is_caesar else 0) - 0.15 * inside))
                elif g.ctype[s] == 'SH' and s == OCTODURUS and not g.caesars_pass and my_cs >= 2:
                    tg.append((s, 3.0))
                ga = [u for u in g.units.values() if u.loc == s and u.side == 'G' and not u.inside]
                if ga and my_cs >= 1.5 * stack_strength(ga):
                    tg.append((s, 1.5 + 0.5 * sum(u.steps for u in ga)))
            if is_caesar and my_cs >= 12 and g.turn >= 2:
                if not g.britannia_done:
                    tg.append((IDX['Dubris'], 4.0))
                if not g.germania_done:
                    tg.append((IDX['Germania A'], 4.0))
        else:
            pc = g.prov_control()
            for s in range(N):
                if g.ctrl[s] == 'R' and g.ctype[s] == 'IM':
                    v = 1.0 + (1.5 if pc[PROV[s]] == 'R' else 0) + (1.5 if PROV[s] == 'Narbonensis' else 0)
                    tg.append((s, v))
        return tg

    def best_plan(self, g, side, leader, units, start, ma_override=None):
        v1 = self._best_plan(g, side, leader, units, start, ma_override)
        return v1

    def _best_plan(self, g, side, leader, units, start, ma_override=None):
        """Return (value, plan) for one activation."""
        ma = self.command_ma(g, side, leader, units, ma_override)
        if ma <= 0 or (not units and not (isinstance(leader, Leader))):
            return (-99, None)
        cr = leader.cr if leader is not None else 2
        ncu = len(units)
        alone = side == 'R' and isinstance(leader, Leader) and not units
        dist, parent = reach(g, side, start, ma, cr, ncu, alone=alone)
        my_cs = stack_strength(units)
        is_caesar = isinstance(leader, Leader) and leader.name == 'Caesar'
        br = leader.br if leader is not None else (1 if any(u.full() for u in units if u.kind in ('legion', 'tribe')) else 0)
        best = (-99, None)
        smp = g.opt['siege_mp']
        aggr = self.p['aggr']
        for t, d in dist.items():
            left = ma - d
            vals = []
            if side == 'R':
                if alone:
                    # leader alone: go join a leaderless legion stack
                    if t != start and any(u.loc == t and u.kind == 'legion' for u in g.units.values()) and \
                            not any(l.loc == t for l in g.leaders.values()):
                        n = sum(1 for u in g.units.values() if u.loc == t and u.kind == 'legion')
                        vals.append((1.0 + 0.4 * n + leader.br * 0.5, [('to', x) for x in path_to(parent, t)]))
                    continue
                vals += self.roman_targets(g, t, d, left, units, my_cs, is_caesar, br, parent, start)
            else:
                vals += self.gallic_targets(g, t, d, left, units, my_cs, leader, br, parent, start)
            if vals and not alone:
                th = self._threat if getattr(self, '_threat', None) is not None else self.threat(g, side)
                risk_t = max(0.0, th[t] - my_cs * (1.4 if side == 'R' else 1.0)) * 0.35
            else:
                risk_t = 0
            for v, plan in vals:
                v = v * (aggr if v > 0 else 1) - d * 0.05 - risk_t + self.noise()
                if v > best[0]:
                    best = (v, plan)
        # approach moves toward distant targets, with a safety check
        if not alone and units:
            th = self._threat if getattr(self, '_threat', None) is not None else self.threat(g, side)
            tg = self.approach_targets(g, side, my_cs, is_caesar)
            if tg:
                def pot(x):
                    return max(v - 0.7 * HOPS[x][s0] for s0, v in tg)
                p0 = pot(start)
                for t, d in dist.items():
                    if t == start or enemy_outside_at(g, t, side):
                        continue
                    if side == 'G' and g.ctrl[t] == 'R' and False:
                        continue
                    risk = max(0.0, th[t] - my_cs * (1.4 if side == 'R' else 1.0)) * 0.35
                    risk0 = max(0.0, th[start] - my_cs * (1.4 if side == 'R' else 1.0)) * 0.35
                    v = (pot(t) - p0) * 0.6 - (risk - risk0) - 0.3 + self.noise()
                    if v > best[0]:
                        best = (v, [('to', x) for x in path_to(parent, t)])
        return best

    # ------------------------------------------------------------ Roman targets
    def roman_targets(self, g, t, d, left, units, my_cs, is_caesar, br, parent, start):
        out = []
        path = [('to', x) for x in path_to(parent, t)]
        smp = g.opt['siege_mp']
        if my_cs <= 0:
            return out
        ga = [u for u in g.units.values() if u.loc == t and u.side == 'G' and not u.inside]
        gt = g.german_tribe()
        if gt is not None and gt.loc == t:
            if my_cs >= 10:
                out.append((1.0, path))
            return out
        if ga and t != start:
            their = stack_strength(ga) + g.local_support('G', t)
            mine = my_cs + g.local_support('R', t)
            steps = sum(u.steps for u in ga)
            if their > 0 and mine >= 3 * their:
                v = 3.0 + 1.5 * steps + (2 * sum(1 for u in ga if u.kind == 'tribe'))
                out.append((v, path + ([('siege',)] if left >= smp else [])))
            else:
                p = win_prob(mine, their, True, False, br, 1)
                pav = 0.25 if their < mine else 0.05
                v = (p * (1.2 * steps + 2) - (1 - p) * (0.8 * len(units) + 1.5)) * (1 - pav)
                if p >= 0.55:
                    out.append((v, path))
        # sieges / subjugation
        def sev(col, drm):
            from itertools import product
            from engine import siege_result
            key = (col, drm)
            if key not in _SEV:
                sp = loss = 0
                for a, b in product(range(1, 7), repeat=2):
                    r = siege_result(col, a + b + drm)
                    if r == 'S':
                        sp += 3
                    else:
                        loss += r[0]; sp += r[1]
                _SEV[key] = (sp / 36, loss / 36)
            return _SEV[key]
        if g.ctype[t] == 'FT' and left >= smp:
            gar = 3 if t in g.ft_up else 2
            inside = [u for u in g.units.values() if u.loc == t and u.side == 'G' and u.inside]
            outside_g = [u for u in g.units.values() if u.loc == t and u.side == 'G' and not u.inside]
            dfn = gar + stack_strength(inside)
            if outside_g:
                dfn += stack_strength(outside_g)   # they may go inside
            col = odds_col(my_cs, dfn)
            if col == 4:
                out.append((6.0 + 1.5 * sum(u.steps for u in inside), path + [('siege',)]))
            elif col >= 1:
                pts = g.siege.get(t, 0)
                drm = g.siege_drm(t, 'R', is_caesar) + g.opt['siege_shift']
                sp, loss = sev(col, drm)
                v = 6.5 * min(1.0, sp / max(0.5, 3 - pts)) * 0.8 - 1.6 * loss + 0.3
                out.append((v, path + [('siege',)]))
        if g.ctype[t] == 'SH' and g.ctrl[t] == 'G' and left >= smp and my_cs >= 2:
            pts = g.siege.get(t, 0)
            drm = (1 if is_caesar else 0) + g.opt['siege_shift']
            sp, loss = sev(2, drm)
            need = g.opt['sh_points']
            worth = 3.5 if (t == OCTODURUS and not g.caesars_pass) else 1.2
            v = worth * min(1.0, sp / max(0.5, need - pts)) - 1.6 * loss
            out.append((v, path + [('siege',)]))
        if g.ctrl[t] == 'G' and g.ctype[t] == 'IM' and left >= 2 and not ga:
            v = removal_value(g, 'R', t) * 0.35
            if t in VP_SPACES and my_cs < 7:
                v -= 3
            out.append((v, path + [('remove_im',)]))
        return out

    # ------------------------------------------------------------ Gallic targets
    def gallic_targets(self, g, t, d, left, units, my_cs, leader, br, parent, start):
        out = []
        path = [('to', x) for x in path_to(parent, t)]
        if my_cs <= 0:
            return out
        ra = [u for u in g.units.values() if u.loc == t and u.side == 'R' and not u.inside]
        if ra and t != start:
            their = stack_strength(ra) + g.local_support('R', t)
            mine = my_cs + g.local_support('G', t)
            rbr = 0
            ls = [l for l in g.leaders.values() if l.loc == t]
            if ls:
                rbr = max(l.br for l in ls)
            p = win_prob(mine, their, False, True, br, rbr)
            steps = sum(u.steps for u in ra)
            caesar_bonus = 3 if any(l.name == 'Caesar' for l in ls) else 0
            v = p * (1.4 * steps + 2 + caesar_bonus) - (1 - p) * (1.2 * len(units) + 2)
            if p >= 0.6:
                out.append((v, path))
        if g.ctrl[t] == 'R' and g.ctype[t] == 'IM' and left >= 2 and not ra:
            v = removal_value(g, 'G', t) * 0.35
            out.append((v, path + [('remove_im',)]))
        if g.ctype[t] == 'WC' and g.ctrl[t] == 'R' and left >= g.opt['siege_mp'] and not ra:
            dfn = WC_GARRISON[t][0] + stack_strength([u for u in g.units.values() if u.loc == t and u.side == 'R'])
            col = odds_col(my_cs, dfn)
            if col >= 1:
                out.append((2.0 + col + g.siege.get(t, 0) * 1.5, path + [('siege',)]))
        # go home to safety if threatened (stay inside fort)
        return out

    # ============================================================ influence & AP loop
    def influence_choice(self, g, side):
        opts = all_influence_options(g, side)
        if not opts:
            return (-99, None)
        best = max(opts, key=lambda a: im_delta(g, side, a))
        return (im_delta(g, side, best) * self.p['infl'] * 0.35 + self.noise(), best)

    def spend_ap(self, g, side, ap):
        guard = 0
        while ap > 0 and guard < 12:
            guard += 1
            options = []
            iv, ia = self.influence_choice(g, side)
            if ia:
                options.append((iv, 'infl', ia, 1))
            self._threat = self.threat(g, side)
            for leader, units, start in self.commands(g, side):
                v, plan = self.best_plan(g, side, leader, units, start)
                if plan:
                    options.append((v, 'move', (leader, units, plan), 1))
            self._threat = None
            if side == 'G':
                options += self.gallic_specials(g, ap)
            if not options:
                break
            options.sort(key=lambda o: -o[0])
            v, kind, arg, cost = options[0]
            if cost > ap:
                options = [o for o in options if o[3] <= ap]
                if not options:
                    break
                v, kind, arg, cost = options[0]
            if v < -1 and kind != 'infl':
                break
            ap -= cost
            if kind == 'infl':
                EV.do_influence(g, side, arg)
            elif kind == 'move':
                leader, units, plan = arg
                g.activate(side, leader, units, plan)
            elif kind == 'council_put':
                g.council_ims += 1
            elif kind == 'council_take':
                self.council_take(g)
            elif kind == 'uprising':
                self.major_uprising(g)
            elif kind == 'devastate':
                g.devast.add(arg)
                if g.ctype[arg] == 'IM':
                    g.remove_im(arg)

    # ------------------------------------------------------------ Gallic special actions
    def gallic_specials(self, g, ap):
        out = []
        iv = 0
        opts = all_influence_options(g, 'G')
        good = sorted((im_delta(g, 'G', a) for a in opts), reverse=True)
        n_out = len(good)
        if g.council_ims < 6 and g.turn <= 5:
            # banking an IM is worth roughly a fraction of a later placement
            out.append((0.55 + (0.3 if g.turn >= 3 else 0), 'council_put', None, 1))
        avail_tribes = [x for x in g.council_tribes if not (g.units[x].name == 'Arverni' and not g.arverni_free())]
        if g.council_ims or avail_tribes:
            k = min(g.council_ims, n_out)
            v = sum(max(0, x) for x in good[:k]) * 0.35 + 2.5 * len([x for x in avail_tribes if g.legal_tribe_spaces(g.units[x])])
            urgency = 1.0 if (g.turn >= 4 or len(g.hands['G']) <= 2) else 0.6
            out.append((v * urgency - 0.5, 'council_take', None, 1))
        if g.turn >= 4 and ap >= 2:
            sub = [g.units[x] for x in g.submitted if g.units[x].loc == 'submitted']
            ok = [u for u in sub if g.legal_tribe_spaces(u)]
            if ok:
                v = 2.2 * len(ok) + g.council_ims * 0.8
                out.append((v, 'uprising', None, 2))
        v = next((u for u in g.on_map('G', 'gleader') if u.name == 'Vercingetorix'), None)
        if v is not None:
            for t in [v.loc] + [x for x, k in ADJ[v.loc]]:
                if g.ctrl[t] == 'R' and g.ctype[t] == 'IM' and t != v.loc and g.ctype[t] != 'WC':
                    pass
            cands = [t for t, k in ADJ[v.loc] if g.ctrl[t] != 'R' and g.ctype[t] not in ('FT', 'WC', 'SH')
                     and not any(u.loc == t and u.side == 'R' for u in g.units.values())]
            # devastation near Roman legions denies supply / winter forage
            for t in cands:
                rl = sum(1 for u in g.units.values() if u.side == 'R' and isinstance(u.loc, int) and (u.loc == t or (u.loc, t) in EDGE))
                if rl >= 2 and g.ctrl[t] != 'G':
                    out.append((0.4 + 0.2 * rl, 'devastate', t, 1))
        return out

    def council_take(self, g):
        # tribes
        for x in list(g.council_tribes):
            u = g.units[x]
            if u.name == 'Arverni' and not g.arverni_free():
                continue
            sp = g.legal_tribe_spaces(u)
            if sp:
                g.council_tribes.remove(x)
                g.place_tribe(u, self.place_tribe_choice(g, u, sp, False))
                u.moved = False
        n = g.council_ims
        g.council_ims = 0
        for _ in range(n):
            opts = [a for a in all_influence_options(g, 'G') if a[0] == 'place']
            if not opts:
                break
            EV.do_influence(g, 'G', max(opts, key=lambda a: im_delta(g, 'G', a)))

    def major_uprising(self, g):
        for x in list(g.submitted):
            u = g.units[x]
            if u.loc != 'submitted':
                continue
            sp = g.legal_tribe_spaces(u)
            if sp:
                g.submitted.remove(x)
                g.place_tribe(u, self.place_tribe_choice(g, u, sp, False))
                u.moved = False
        # council IMs may each remove a Roman IM in Gaul
        n = g.council_ims
        g.council_ims = 0
        for _ in range(n):
            rem = [s for s in range(N) if g.ctrl[s] == 'R' and g.ctype[s] == 'IM' and REGION[s] in GAUL_REGIONS]
            opts = [a for a in all_influence_options(g, 'G') if a[0] == 'place']
            best_rem = max(rem, key=lambda s: removal_value(g, 'G', s)) if rem else None
            best_pl = max(opts, key=lambda a: im_delta(g, 'G', a)) if opts else None
            if best_rem is not None and (best_pl is None or removal_value(g, 'G', best_rem) >= im_delta(g, 'G', best_pl)):
                g.remove_im(best_rem)
            elif best_pl:
                EV.do_influence(g, 'G', best_pl)
        for x in list(g.council_tribes):
            u = g.units[x]
            if u.name == 'Arverni' and not g.arverni_free():
                continue
            sp = g.legal_tribe_spaces(u)
            if sp:
                g.council_tribes.remove(x)
                g.place_tribe(u, self.place_tribe_choice(g, u, sp, False))

    # ============================================================ activations
    def activate_leader(self, g, side, leader, free=True):
        us = [u for u in g.units.values() if u.loc == leader.loc and u.side == side and not u.moved and not g.unit_besieged(u)]
        us.sort(key=lambda u: -u.strength())
        if isinstance(leader, Leader) and len(us) > leader.cr + (3 if leader.name == 'Caesar' else 0):
            us = us[:leader.cr]
        v, plan = self.best_plan(g, side, leader, us, leader.loc)
        if plan and v > -0.5:
            g.activate(side, leader, us, plan)

    def mass_activation(self, g, side, units, purpose, ma=None):
        if purpose == 'motus_ubique':
            done_regions = set()
            for _ in range(6):
                best = None
                for leader, us, start in self.commands(g, side):
                    if REGION[start] in done_regions:
                        continue
                    v, plan = self.best_plan(g, side, leader, us, start)
                    if plan and (best is None or v > best[0]):
                        best = (v, leader, us, plan, start)
                if not best or best[0] < 0.2:
                    break
                done_regions.add(REGION[best[4]])
                g.activate(side, best[1], best[2], best[3])
            return
        only = None
        if purpose == 'belgic_confederation':
            only = [u for u in g.on_map('G') if REGION[u.loc] == 'Belgica']
        guard = 0
        while guard < 20:
            guard += 1
            cmds = self.commands(g, side, only=only)
            if purpose == 'caesars_legions':
                cmds = [c for c in cmds if c[0] is None]
            best = None
            for leader, us, start in cmds:
                v, plan = self.best_plan(g, side, leader, us, start, ma_override=ma)
                if plan and (best is None or v > best[0]):
                    best = (v, leader, us, plan)
            if not best or best[0] < 0.3:
                break
            g.activate(side, best[1], best[2], best[3], ma_override=ma)

    # ============================================================ card choice
    def event_value(self, g, side, c):
        info = CARDS[c]
        if not g.event_allowed(side, c):
            return None
        ap = g.ap(c)
        cz = g.leaders.get('Caesar')
        cz_on = cz is not None and isinstance(cz.loc, int)
        pc = g.prov_control()
        def count(pred):
            return sum(1 for s in range(N) if pred(s))
        v = None
        if c in (1, 2):
            v = ap + (1.5 if cz_on else 0) + (0.8 if c == 1 else 0)
        elif c == 3:
            rome = g.path_to_rome()
            red = sum(1 for u in g.on_map('R', 'legion') if u.steps == 1 and u.loc in rome) + len(g.elim_legions)
            v = min(2, red) * 1.6
        elif c == 4:
            v = 5.0 if g.turn <= 4 else None
        elif c == 5:
            n = len([1 for cmd in self.commands(g, 'G', only=[u for u in g.on_map('G') if REGION[u.loc] == 'Belgica'])])
            v = n * 0.9
        elif c == 6:
            n = sum(1 for p in REG_PROVS['Celtica'] + REG_PROVS['Belgica'] + REG_PROVS['Aquitania']
                    if any(g.ctrl[s] == 'G' and g.ctype[s] == 'IM' for s in PROVINCES[p]['idx']))
            v = n * 0.6
        elif c == 7:
            n = sum(1 for p in REG_PROVS['Belgica'] if any(g.ctrl[s] == 'R' for s in PROVINCES[p]['idx'])
                    or any(u.side == 'R' and PROV[u.loc] == p for u in g.on_map('R')))
            v = n * 0.7
        elif c == 8:
            best = 0
            for p in REG_PROVS['Celtica'] + REG_PROVS['Belgica'] + REG_PROVS['Aquitania']:
                if any(u.side == 'R' and PROV[u.loc] == p for u in g.on_map('R')):
                    continue
                k = sum(1 for s in PROVINCES[p]['idx'] if g.ctrl[s] == 'R' and g.ctype[s] == 'IM')
                k += 2 if pc[p] == 'R' else 0
                best = max(best, k)
            v = best * 0.9
        elif c == 9:
            if cz_on:
                k = sum(1 for s in [cz.loc] + [t for t, kk in ADJ[cz.loc]] if g.ctrl[s] == 'G' and g.ctype[s] == 'IM'
                        and not any(u.loc == s and u.side == 'G' for u in g.units.values()))
                v = k * 0.9
        elif c == 10:
            v = 2.4
        elif c == 11:
            v = len(self.commands(g, 'R')) * 0.9
        elif c == 12:
            v = max(sum(1 for p in REG_PROVS[r] if any(g.ctrl[s] == 'R' and g.ctype[s] == 'IM' for s in PROVINCES[p]['idx']))
                    for r in ('Celtica', 'Belgica')) * 0.65
        elif c == 13:
            red = any(u.kind == 'tribe' and u.steps == 1 and (isinstance(u.loc, int) or u.loc == 'submitted') for u in g.units.values())
            v = 1.2 + (1.2 if red else 0)
        elif c == 14:
            v = len({PROV[s] for s in range(N) if g.ctype[s] == 'FT'}) * 0.55
        elif c == 15:
            mt = next(u for u in g.units.values() if u.name == 'Minor Tribe')
            v = ap + (0.9 if mt.loc == 'hold' else 0)
        elif c in (16, 53):
            v = len(self.commands(g, 'G')) * 0.6
        elif c == 17:
            v = ap + 1.0
        elif c in (18, 19, 31, 33, 39, 40, 46, 23, 22):
            v = ap + 0.8
        elif c == 20:
            v = ap + (1.0 if any(u.steps == 1 for u in g.on_map('R', 'legion')) else 0)
        elif c == 21:
            v = 2.6 if g.pool else None
        elif c in (25, 26):
            v = ap + 0.9
        elif c == 27:
            k = len({PROV[s] for s in range(N) if REGION[s] == 'Provincia' and g.ctrl[s] == 'R' and g.ctype[s] == 'IM'})
            v = min(2, k) * 1.5
        elif c == 28:
            v = ap + 0.4
        elif c in (29, 30):
            v = ap + 0.8
        elif c == 32:
            v = ap + 0.5 * len([1 for cmd in self.commands(g, 'R') if cmd[0] is None])
        elif c in (34, 35):
            v = ap + 0.3
        elif c == 36:
            v = len({PROV[u.loc] for u in g.on_map('G')}) * 0.55
        elif c in (37, 38):
            v = min(6, len({REGION[cmd[2]] for cmd in self.commands(g, side)})) * 0.8
        elif c == 41:
            v = 1.0 + 0.3 * sum(1 for p, x in pc.items() if x == 'G')
        elif c == 42:
            v = 1.8
        elif c == 43:
            aed = next(u for u in g.units.values() if u.name == 'Aedui')
            ok = aed.loc == 'aedui_box' and any(g.ctrl[s] != 'R' and not any(u.loc == s and u.side == 'R' for u in g.units.values())
                                               for s in PROVINCES['Aedui']['idx'])
            v = ap + (3.5 if ok else 0)
        elif c == 44:
            v = ap + 0.2
        elif c in (45, 48):
            v = 1.6
        elif c == 47:
            v = None
        elif c == 49:
            v = len(self.commands(g, side)) * 0.35
        elif c in (50, 51):
            v = ap + (1.0 if any(g.is_besieged(s) for s in range(N)) else 0)
        if v is None:
            return None
        return v + self.p['event_bias']

    def choose_play(self, g, side):
        hand = [c for c in g.hands[side] if CARDS[c]['kind'] != 'surprise']
        best = None
        for c in hand:
            ap = g.ap(c)
            ev = self.event_value(g, side, c)
            opts = [(ap * 1.0, 'ap')]
            if ev is not None:
                mode = 'bonus' if CARDS[c]['kind'] == 'bonus' else 'event'
                opts.append((ev, mode))
            for v, mode in opts:
                key = v + self.noise() * 2
                if best is None or key > best[0]:
                    best = (key, c, mode)
        if best is None:
            c = g.hands[side][0]
            return c, 'ap'
        return best[1], best[2]

    # ============================================================ Gallic spring muster
    def spring_muster(self, g):
        # move tribes toward Roman IMs they can raid later, staying safe
        for u in list(g.on_map('G', 'tribe')):
            if g.unit_besieged(u):
                continue
            dist, parent = reach(g, 'G', u.loc, 3, 2, 1)
            best = None
            for t, d in dist.items():
                if t == u.loc or not g.muster_ok(t) or g.ctrl[t] == 'R':
                    continue
                adj_r = sum(1 for x, k in ADJ[t] if g.ctrl[x] == 'R' and g.ctype[x] == 'IM')
                v = adj_r * 0.5 - d * 0.1
                if g.ctype[u.loc] == 'FT' and g.ft_tribe.get(u.loc) == u.uid:
                    v -= 0.6
                if best is None or v > best[0]:
                    best = (v, t)
            if best and best[0] > 0.3:
                g.muster_move([u], path_to(parent, best[1]))
