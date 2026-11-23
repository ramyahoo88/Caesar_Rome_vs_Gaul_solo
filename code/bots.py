"""The paper bots, as code.  Imperator (Rome) and Concilium (Gaul).

Everything here must be executable by a person at the table: decisions use counts of
spaces, battle strengths, siege odds and simple priority lists.  The printed rules
(print/Caesar_Solo_Rules.md) are written from this file.
"""
import random
from engine import (N, NAMES, IDX, ADJ, EDGE, PROV, REGION, STYPE, PROVINCES, REG_PROVS, GAUL_REGIONS,
                    PROVINCIA, OTHER, Leader, Unit, GERMANIA_VP, BRITANNIA_VP, OCTODURUS, BRIGANTIUM,
                    battle_result, odds_col, CARDS, SEA, GERMAN_SH, WC_GARRISON, HOPS, PORTS)
from heur import reach, path_to, stack_strength, enemy_outside_at, prov_margin
from policies import BasePolicy
import events as EV

PORTUS_ITIUS = IDX['Portus Itius']
DUBRIS = IDX['Dubris']; DUROVERNON = IDX['Durovernon']
GERM_A = IDX['Germania A']; GERM_B = IDX['Germania B']

# ------------------------------------------------------------------ directive decks
# Each directive: mission order + compass tie-break.
ROME_DIRECTIVES_V2 = [
    ('Pacify',    ['RAID', 'CONTROL', 'SIEGE', 'STRIKE'], 'N'),
    ('Pacify',    ['RAID', 'CONTROL', 'SIEGE', 'STRIKE'], 'S'),
    ('Pacify',    ['RAID', 'CONTROL', 'STRIKE', 'SIEGE'], 'E'),
    ('Pacify',    ['RAID', 'CONTROL', 'STRIKE', 'SIEGE'], 'W'),
    ('Rule',      ['CONTROL', 'RAID', 'SIEGE', 'STRIKE'], 'N'),
    ('Rule',      ['CONTROL', 'RAID', 'SIEGE', 'STRIKE'], 'W'),
    ('Rule',      ['CONTROL', 'RAID', 'STRIKE', 'SIEGE'], 'E'),
    ('Campaign',  ['CONTINUE', 'SIEGE', 'RAID', 'CONTROL', 'STRIKE'], 'S'),
    ('Glory',     ['INVADE', 'CONTINUE', 'SIEGE', 'RAID', 'CONTROL'], 'N'),
]
ROME_DIRECTIVES_V3 = [
    ('Pacify',    ['RULE', 'RAID', 'SETTLE', 'SIEGE', 'STRIKE'], 'N'),
    ('Pacify',    ['RULE', 'RAID', 'SETTLE', 'SIEGE', 'STRIKE'], 'S'),
    ('Pacify',    ['RULE', 'RAID', 'SETTLE', 'STRIKE', 'SIEGE'], 'E'),
    ('Pacify',    ['RULE', 'RAID', 'SETTLE', 'STRIKE', 'SIEGE'], 'W'),
    ('Rule',      ['RULE', 'SETTLE', 'RAID', 'SIEGE', 'STRIKE'], 'N'),
    ('Rule',      ['RULE', 'RAID', 'SIEGE', 'SETTLE', 'STRIKE'], 'W'),
    ('Raid',      ['RAID', 'RULE', 'SETTLE', 'SIEGE', 'STRIKE'], 'E'),
    ('Campaign',  ['RULE', 'CONTINUE', 'SIEGE', 'RAID', 'SETTLE', 'STRIKE'], 'S'),
    ('Glory',     ['RULE', 'INVADE', 'RAID', 'SETTLE', 'SIEGE'], 'N'),
]
ROME_DIRECTIVES_V4 = [
    ('Pacify',    ['RULE', 'SIEGE', 'RAID', 'SETTLE', 'STRIKE'], 'N'),
    ('Pacify',    ['RULE', 'SIEGE', 'RAID', 'SETTLE', 'STRIKE'], 'S'),
    ('Pacify',    ['RULE', 'SIEGE', 'RAID', 'SETTLE', 'STRIKE'], 'E'),
    ('Pacify',    ['RULE', 'SIEGE', 'RAID', 'SETTLE', 'STRIKE'], 'W'),
    ('Rule',      ['RULE', 'RAID', 'SIEGE', 'SETTLE', 'STRIKE'], 'N'),
    ('Rule',      ['RULE', 'RAID', 'SIEGE', 'SETTLE', 'STRIKE'], 'W'),
    ('Raid',      ['RAID', 'RULE', 'SIEGE', 'SETTLE', 'STRIKE'], 'E'),
    ('Campaign',  ['RULE', 'SIEGE', 'STRIKE', 'RAID', 'SETTLE'], 'S'),
    ('Glory',     ['RULE', 'INVADE', 'SIEGE', 'RAID', 'SETTLE'], 'N'),
]
ROME_DIRECTIVES_V1 = [
    ('Campaign',  ['SIEGE', 'STRIKE', 'CONTROL', 'MARCH'], 'N'),
    ('Campaign',  ['SIEGE', 'STRIKE', 'CONTROL', 'MARCH'], 'W'),
    ('Conquest',  ['STRIKE', 'SIEGE', 'MARCH', 'CONTROL'], 'N'),
    ('Conquest',  ['STRIKE', 'SIEGE', 'MARCH', 'CONTROL'], 'S'),
    ('Rule',      ['CONTROL', 'SIEGE', 'STRIKE', 'MARCH'], 'E'),
    ('Rule',      ['CONTROL', 'STRIKE', 'SIEGE', 'MARCH'], 'W'),
    ('Glory',     ['INVADE', 'SIEGE', 'STRIKE', 'CONTROL', 'MARCH'], 'N'),
    ('Pacify',    ['RAID', 'CONTROL', 'SIEGE', 'STRIKE', 'MARCH'], 'S'),
    ('Pacify',    ['RAID', 'SIEGE', 'CONTROL', 'STRIKE', 'MARCH'], 'E'),
]
GAUL_DIRECTIVES = [
    ('Revolt',    ['RISE', 'AMBUSH', 'RAID', 'AGITATE'], 'N'),
    ('Revolt',    ['RISE', 'RAID', 'AMBUSH', 'AGITATE'], 'S'),
    ('Agitate',   ['AGITATE', 'RAID', 'AMBUSH', 'BANK'], 'E'),
    ('Agitate',   ['AGITATE', 'AMBUSH', 'RAID', 'BANK'], 'W'),
    ('Raid',      ['RAID', 'AGITATE', 'AMBUSH', 'BANK'], 'S'),
    ('Raid',      ['RAID', 'AMBUSH', 'AGITATE', 'BANK'], 'N'),
    ('Ambush',    ['AMBUSH', 'RAID', 'AGITATE', 'BANK'], 'E'),
    ('Council',   ['BANK', 'AGITATE', 'RAID', 'AMBUSH'], 'W'),
    ('Council',   ['RISE', 'BANK', 'AGITATE', 'RAID'], 'N'),
]


def compass_key(s, c):
    # map coordinates: x grows east, y grows south
    from engine import _sp
    x, y = _sp[s]['x'], _sp[s]['y']
    return {'N': y, 'S': -y, 'E': -x, 'W': x}[c]


class BotPolicy(BasePolicy):
    name = 'bot'

    def __init__(self, side, seed=0, level=2, look=2, directives=None, **params):
        super().__init__(side, seed, **params)
        self.level = level
        self.look = look
        self.deck = list(directives or (ROME_DIRECTIVES_V4 if side == 'R' else GAUL_DIRECTIVES))
        self.dpile = []
        self.directive = None
        self.compass = 'N'
        self.reserve = set()
        self.expedition = False
        self.p.update(dict(noise=0.0))
        self.cfg = dict(
            r_siege_min_col=2, r_siege_min_col_caesar=1, r_strike_ratio=2.0, r_strike_ratio_caesar=1.5,
            g_ambush_ratio=1.5, g_avoid_ratio=1.5, r_avoid_ratio=1.5, g_inside_ratio=1.0,
            r_invade_turn=3, bank_turn_max=5, rise_min=3, deny=True, block=False, block_first=False, celtica_first=True, dominance_race=True, protect=True, r_pre=('CONTINUE', 'PROTECT', 'SUBMIT', 'REGROUP'), siege_strict=True, strike_submit_only=False, winter_neutral=True,
            regroup=True, r_post=('GATHER', 'CONTROL'), expedition=False, invade_cs=12, safe_raid=True, g_safe_raid=1.0, g_regroup=0, g_pre=(), r_danger=1.5, caesar_siege_col=3, extra_star=(), live_first=False,
        )
        self.cfg.update({k: v for k, v in params.items() if k in self.cfg})

    # ============================================================ directive deck
    def draw_directive(self):
        if not self.dpile:
            self.dpile = list(self.deck)
            self.rng.shuffle(self.dpile)
        self.directive = self.dpile.pop()
        return self.directive

    # ============================================================ card choice
    def choose_play(self, g, side):
        d = self.draw_directive()
        self.compass = d[2]
        self.sync_reserve(g, side)
        hand = list(g.hands[side])
        # 2.2 Offer: shuffle the face-down hand (not the Reserve) and reveal cards one at a time;
        # a Surprise card or #24 goes face up into the Reserve and another card is revealed (1.3)
        hidden = [c for c in hand if c not in self.reserve]
        self.rng.shuffle(hidden)
        look = self.look if self.look > 0 else len(hidden)
        shown = []
        for c in hidden:
            if CARDS[c]['kind'] == 'surprise' or c == 24:
                self.reserve.add(c)
                continue
            shown.append(c)
            if len(shown) >= look:
                break
        if not shown:
            # 1.3: only Reserve cards are left.  #24 is then played for AP; with only Surprise
            # cards left the bot discards them and draws replacements (7.5.4).
            if 24 in hand:
                return 24, 'ap'
            return hand[0], 'ap'
        best = None
        for c in shown:
            live = self.event_live(g, side, c)
            star = live and self.priority_event(g, side, c)
            key = (1 if star else 0, g.ap(c), 1 if live else 0) if not self.cfg.get('live_first') else \
                (1 if star else 0, 1 if live else 0, g.ap(c))
            if best is None or key > best[0]:
                best = (key, c, live)
        c, live = best[1], best[2]
        if g.logging:
            nm = 'Imperator' if side == 'R' else 'Concilium'
            g.log(f'{nm} Directive {d[0]} ({d[2]}): ' + ' > '.join(d[1]) +
                  f'; Offer ' + ', '.join(f'#{x}{"*" if self.event_live(g, side, x) else ""}' for x in shown) + f' -> #{c}')
        if live:
            return c, ('bonus' if CARDS[c]['kind'] == 'bonus' else 'event')
        return c, 'ap'

    # ------------------------------------------------------------ event guide
    def priority_event(self, g, side, c):
        if side == 'R':
            return c in (1, 2, 4, 11, 3, 10) + tuple(self.cfg.get('extra_star', ()))
        return c in (5, 16, 53, 21, 43, 6, 14, 27) + tuple(self.cfg.get('extra_star', ()))

    def event_live(self, g, side, c):
        if not g.event_allowed(side, c):
            return False
        k = CARDS[c]['kind']
        pc = g.prov_control()
        cz = g.leaders.get('Caesar')
        cz_on = cz is not None and isinstance(cz.loc, int)
        R, G = 'R', 'G'
        def n_targets_remove(pred):
            return sum(1 for s in range(N) if g.ctrl[s] == OTHER[side] and g.ctype[s] == 'IM' and pred(s))
        if side == 'R':
            if c in (1, 2):
                return cz_on and not g.caesar_delayed
            if c == 3:
                rome = g.path_to_rome()
                return sum(1 for u in g.on_map('R', 'legion') if u.steps == 1 and u.loc in rome and not g.unit_besieged(u)) \
                    + 2 * min(1, len(g.elim_legions)) >= 2
            if c == 4:
                return g.turn <= 4
            if c == 9:
                if not cz_on:
                    return False
                return sum(1 for s in [cz.loc] + [t for t, kk in ADJ[cz.loc]] if g.ctrl[s] == 'G' and g.ctype[s] == 'IM'
                           and not any(u.loc == s and u.side == 'G' for u in g.units.values())) >= 2
            if c == 10:
                return True
            if c == 11:
                return True
            if c == 12:
                return max(sum(1 for p in REG_PROVS[r] if any(g.ctrl[s] == 'R' and g.ctype[s] == 'IM' for s in PROVINCES[p]['idx']))
                           for r in ('Celtica', 'Belgica')) >= 3
            if c == 17:
                return True
            if c == 18:
                return n_targets_remove(lambda s: pc[PROV[s]] == 'R' and not any(u.loc == s and u.side == 'G' for u in g.units.values())) > 0
            if c == 19:
                rp = [p for p, v in pc.items() if v == 'R']
                adj = set()
                for p in rp:
                    from engine import PROV_ADJ
                    adj |= PROV_ADJ[p]
                return n_targets_remove(lambda s: PROV[s] in adj and not any(u.loc == s and u.side == 'G' for u in g.units.values())) > 0
            if c == 20:
                rome = g.path_to_rome()
                return any(u.steps == 1 and u.loc in rome and not g.unit_besieged(u) for u in g.on_map('R', 'legion'))
            if c in (29, 30):
                return any(u.loc == 'hold' and u.name.startswith('Germani Cav') for u in g.units.values()) and bool(EV.german_supply_legions(g))
            if c == 31:
                rs = {u.loc for u in g.on_map('R')}
                return n_targets_remove(lambda s: any(t in rs for t, kk in ADJ[s])) > 0
            if c == 32:
                return any(not any(l.loc == u.loc for l in g.leaders.values()) for u in g.on_map('R', 'legion'))
            if c in (37, 38):
                return len({REGION[u.loc] for u in g.on_map('R')}) >= 3
            if c == 45:
                return n_targets_remove(lambda s: REGION[s] in GAUL_REGIONS + ('Provincia',) and not any(u.loc == s and u.side == 'G' for u in g.units.values())) > 0
            if c == 48:
                return n_targets_remove(lambda s: REGION[s] in GAUL_REGIONS + ('Provincia',) and not any(u.loc == s for u in g.units.values())) > 0
            if c == 44:
                return any(l.br == 0 for l in g.leaders.values() if l.name != 'Caesar' and isinstance(l.loc, int))
        else:
            if c == 5:
                return sum(1 for u in g.on_map('G') if REGION[u.loc] == 'Belgica' and u.kind in ('tribe', 'gleader')) >= 2
            if c in (16, 53):
                return sum(1 for u in g.on_map('G') if u.kind in ('tribe', 'gleader')) >= 3
            if c == 6:
                return sum(1 for p in REG_PROVS['Celtica'] + REG_PROVS['Belgica'] + REG_PROVS['Aquitania']
                           if any(g.ctrl[s] == 'G' and g.ctype[s] == 'IM' for s in PROVINCES[p]['idx'])) >= 3
            if c == 7:
                return sum(1 for p in REG_PROVS['Belgica'] if any(g.ctrl[s] == 'R' and g.ctype[s] == 'IM' for s in PROVINCES[p]['idx'])
                           or any(PROV[u.loc] == p for u in g.on_map('R'))) >= 2
            if c == 8:
                for p in REG_PROVS['Celtica'] + REG_PROVS['Belgica'] + REG_PROVS['Aquitania']:
                    if any(PROV[u.loc] == p for u in g.on_map('R')):
                        continue
                    if sum(1 for s in PROVINCES[p]['idx'] if g.ctrl[s] == 'R' and g.ctype[s] == 'IM') >= 2:
                        return True
                return False
            if c == 13:
                return True
            if c == 14:
                return len({PROV[s] for s in range(N) if g.ctype[s] == 'FT'}) >= 3
            if c == 15:
                return any(u.name == 'Minor Tribe' and u.loc == 'hold' for u in g.units.values())
            if c == 21:
                return bool(g.pool)
            if c in (22, 23, 28):
                return True
            if c in (25, 26):
                return any(u.name.startswith('Mercenaries') and u.loc == 'hold' for u in g.units.values())
            if c == 27:
                return sum(1 for s in range(N) if REGION[s] == 'Provincia' and g.ctrl[s] == 'R' and g.ctype[s] == 'IM') > 0
            if c == 36:
                return len({PROV[u.loc] for u in g.on_map('G')}) >= 3
            if c == 41:
                return any(u.name == 'Militia' and u.loc == 'hold' for u in g.units.values()) and \
                    sum(1 for p in REG_PROVS['Celtica'] if pc[p] == 'G') >= 2
            if c == 42:
                return len(g.hands['R']) >= 2
            if c == 43:
                return any(u.name == 'Aedui' and u.loc == 'aedui_box' for u in g.units.values()) and \
                    any(g.ctrl[s] != 'R' and not any(u.loc == s and u.side == 'R' for u in g.units.values()) for s in PROVINCES['Aedui']['idx'])
            if c in (37, 38):
                return len({REGION[u.loc] for u in g.on_map('G')}) >= 3
            if c == 45:
                return n_targets_remove(lambda s: REGION[s] in GAUL_REGIONS + ('Provincia',) and not any(u.loc == s and u.side == 'R' for u in g.units.values())) > 0
            if c == 44:
                return any(l.br >= 2 for l in g.leaders.values() if l.name != 'Caesar' and isinstance(l.loc, int))
        if c in (33, 46):
            fr = {u.loc for u in g.on_map(side) if not g.unit_besieged(u)}
            return n_targets_remove(lambda s: any(t in fr for t, kk in ADJ[s]) and not any(u.loc == s and u.side == OTHER[side] for u in g.units.values())) > 0
        if c == 39:
            fp = {PROV[s] for s in range(N) if g.ctrl[s] == side and g.ctype[s] == 'IM'}
            return n_targets_remove(lambda s: PROV[s] in fp and not any(u.loc == s and u.side == OTHER[side] for u in g.units.values())) > 0
        if c == 40:
            vac = {p for p, v in PROVINCES.items() if any(g.ctrl[x] is None for x in v['idx'])}
            return n_targets_remove(lambda s: PROV[s] in vac and not any(u.loc == s for u in g.units.values())) > 0
        if c in (34, 35):
            return True
        if c == 50:
            return any(g.ctype[s] in ('FT', 'WC') and PORTS[s] and any(g.naval_supremacy(side, z) for z in PORTS[s])
                       and g.is_besieged(s) and g.fort_owner(s) != side for s in range(N))
        if c == 51:
            return any(g.is_besieged(s) and g.fort_owner(s) != side for s in range(N))
        return False

    # ============================================================ AP spending
    def spend_ap(self, g, side, ap):
        d = self.directive or self.draw_directive()
        order = d[1]
        self.compass = d[2]
        guard = 0
        while ap > 0 and guard < 12:
            guard += 1
            done = False
            pre = list(self.cfg['r_pre']) if side == 'R' else list(self.cfg['g_pre'])
            for m in pre + order + (list(self.cfg['r_post']) if side == 'R' else ['AGITATE']):
                cost = self.try_mission(g, side, m, ap)
                if cost:
                    if g.logging:
                        g.log(f'  {"Imperator" if side == "R" else "Concilium"} AP: {m}')
                    ap -= cost
                    done = True
                    break
            if not done:
                break

    def try_mission(self, g, side, m, ap):
        fn = getattr(self, 'm_' + m.lower(), None)
        if fn is None:
            return 0
        return fn(g, ap)

    # ------------------------------------------------------------ armies
    def roman_armies(self, g):
        """(leader, units, space) for unmoved Roman armies: leader-led first (Caesar, then by BR)."""
        out = []
        used = set()
        for l in sorted(g.leaders.values(), key=lambda l: (l.name != 'Caesar', -l.br)):
            if not isinstance(l.loc, int) or l.moved:
                continue
            us = [u for u in g.units.values() if u.loc == l.loc and u.side == 'R' and not u.moved and not g.unit_besieged(u)
                  and u.uid not in used]
            us.sort(key=lambda u: (-u.strength(), u.merc))
            us = us[:l.cr]
            if us:
                out.append((l, us, l.loc)); used |= {u.uid for u in us}
        stacks = {}
        for u in g.on_map('R', 'legion'):
            if u.moved or u.uid in used or g.unit_besieged(u):
                continue
            stacks.setdefault(u.loc, []).append(u)
        for s, us in stacks.items():
            us.sort(key=lambda u: -u.strength())
            out.append((None, us[:2], s))
        return out

    def gallic_armies(self, g):
        out = []
        used = set()
        for u in sorted(g.on_map('G', 'gleader'), key=lambda x: x.name != 'Vercingetorix'):
            if u.moved or g.unit_besieged(u):
                continue
            us = [x for x in g.units.values() if x.loc == u.loc and x.side == 'G' and x is not u and not x.moved
                  and not g.unit_besieged(x) and x.kind != 'gleader' and (u.name != 'Ambiorix' or x.region == 'Belgic' or x.merc)]
            us.sort(key=lambda x: -x.strength())
            out.append((u, us[:u.cr], u.loc)); used |= {x.uid for x in us[:u.cr]} | {u.uid}
        for u in g.on_map('G'):
            if u.uid in used or u.moved or g.unit_besieged(u) or u.kind not in ('tribe', 'merc'):
                continue
            if u.merc and u.ma == 0:
                continue
            others = [x for x in g.units.values() if x.loc == u.loc and x.side == 'G' and x is not u and not x.moved
                      and x.uid not in used and x.kind in ('tribe', 'merc') and not g.unit_besieged(x)]
            others.sort(key=lambda x: -x.strength())
            take = [u] + others[:1]
            used |= {x.uid for x in take}
            out.append((None, take, u.loc))
        return out

    def army_reach(self, g, side, leader, units, start):
        if leader is not None:
            ma = leader.ma
        else:
            movers = [u for u in units if u.ma > 0]
            ma = min(u.ma for u in movers) if movers else 0
        cr = leader.cr if leader is not None else 2
        dist, parent = reach(g, side, start, ma, cr, len(units))
        return ma, dist, parent

    def pick(self, cands):
        """cands: list of (priority tuple, space, payload). Lower tuple wins; compass breaks ties;
        if several armies tie for the same space, the strongest army goes (then army order)."""
        if not cands:
            return None
        def army_str(c):
            try:
                return -stack_strength(c[2][1])
            except Exception:
                return 0
        return min(cands, key=lambda c: (c[0], compass_key(c[1], self.compass), army_str(c)))

    # ============================================================ ROMAN missions
    def bs(self, g, side, units, s):
        return stack_strength(units) + g.local_support(side, s)

    def rsup(self, g):
        self.g_ref = g
        return None

    def m_siege(self, g, ap):
        cands = []
        sup = self.rsup(g)
        smp = g.opt['siege_mp']
        armies = list(self.roman_armies(g))
        # leaderless stacks may take a third Legion (over command) to force a surrender
        extra = []
        for leader, units, start in armies:
            if leader is None:
                more = [u for u in g.units.values() if u.loc == start and u.kind == 'legion' and not u.moved
                        and u not in units and not g.unit_besieged(u)]
                if more:
                    extra.append((None, units + more[:1], start))
        for leader, units, start in armies + extra:
            caesar = leader is not None and leader.name == 'Caesar'
            ma, dist, parent = self.army_reach(g, 'R', leader, units, start)
            cs0 = stack_strength(units)
            for t, d in dist.items():
                if ma - d < smp or t in g.sieged_this_card:
                    continue
                cs = cs0 + stack_strength([u for u in g.units.values() if u.loc == t and u.side == 'R' and u not in units
                                           and not u.inside])
                if g.ctype[t] == 'FT':
                    # defenders inside may come out, so every Gallic CU in the space counts
                    dfn = g.fort_defense(t)[0] + stack_strength([u for u in g.units.values() if u.loc == t and u.side == 'G'
                                                                 and not u.inside])
                    col = odds_col(cs, dfn)
                    pts = g.siege.get(t, 0)
                    need = self.cfg['r_siege_min_col_caesar'] if caesar else self.cfg['r_siege_min_col']
                    if leader is None and col != 4:
                        continue
                    if self.cfg.get('siege_strict'):
                        ok = col == 4 or (pts >= 2 and col >= 1) or (pts >= 1 and caesar and col >= 3) \
                            or (caesar and self.cfg.get('caesar_siege_col') is not None and col >= self.cfg['caesar_siege_col'])
                    else:
                        ok = col == 4 or col >= need or (pts >= 1 and col >= 1)
                    if ok:
                        if g.ctype[t] == 'FT' and enemy_outside_at(g, t, 'R') and col < 4:
                            # must beat the army outside first: leave to STRIKE
                            continue
                        reg = 0 if REGION[t] == 'Celtica' else 1
                        cands.append(((0 if col == 4 else 1, 0 if self.near_sup(t, sup) else 1, -pts, reg if self.cfg.get('celtica_first') else 0, -col, d), t, (leader, units, parent)))
                elif g.ctype[t] == 'SH' and t == OCTODURUS and not g.caesars_pass and cs >= 2 and leader is not None:
                    cands.append(((2, 0, -g.siege.get(t, 0), 0, 0, d), t, (leader, units, parent)))
        c = self.pick(cands)
        if not c:
            return 0
        leader, units, parent = c[2]
        g.activate('R', leader, units, [('to', x) for x in path_to(parent, c[1])] + [('siege',)])
        return 1

    def m_continue(self, g, ap):
        if self.cfg.get('expedition') and self.expedition:
            r = self.m_invade(g, ap, force=True)
            if r:
                return r
        """An army already besieging a Fortified Town (or Stronghold) rolls again."""
        for leader, units, start in self.roman_armies(g):
            if leader is None:
                continue
            t = start
            if t in g.sieged_this_card:
                continue
            here = stack_strength([u for u in g.units.values() if u.loc == t and u.side == 'R' and not u.inside])
            if g.ctype[t] == 'FT' and g.siege.get(t, 0) >= 1 and not enemy_outside_at(g, t, 'R') \
                    and odds_col(here, g.fort_defense(t)[0]) >= 0:
                g.activate('R', leader, units, [('siege',)])
                return 1
            if g.ctype[t] == 'SH' and g.ctrl[t] == 'G' and g.siege.get(t, 0) >= 1 and here >= 2:
                g.activate('R', leader, units, [('siege',)])
                return 1
        return 0

    def m_protect(self, g, ap):
        """Provincia first: attack Gallic CUs in Provincia, or sweep Gallic IMs there, when a
        Provincia province is not Roman-controlled or Gallic CUs stand in Provincia."""
        if not self.cfg.get('protect', True):
            return 0
        pc = g.prov_control()
        lost = [p for p in PROVINCIA if pc[p] != 'R']
        gcus = [u for u in g.on_map('G') if REGION[u.loc] == 'Provincia' and not u.inside]
        if not lost and not gcus:
            return 0
        # attack Gallic units in Provincia at 1:1 or better
        cands = []
        for leader, units, start in self.roman_armies(g):
            ma, dist, parent = self.army_reach(g, 'R', leader, units, start)
            for t, d in dist.items():
                if REGION[t] != 'Provincia' or t == start:
                    continue
                ga = [u for u in g.units.values() if u.loc == t and u.side == 'G' and not u.inside]
                if not ga:
                    continue
                # units inside a fortification may come out and fight: count them all
                mine = self.bs(g, 'R', units, t); theirs = self.bs(g, 'G', [u for u in g.units.values() if u.loc == t and u.side == 'G'], t)
                if theirs > 0 and mine >= theirs:
                    cands.append(((0 if mine >= 3 * theirs else 1, -theirs, d), t, (leader, units, parent)))
        c = self.pick(cands)
        if c:
            leader, units, parent = c[2]
            g.activate('R', leader, units, [('to', x) for x in path_to(parent, c[1])])
            return 1
        if lost:
            # sweep Gallic IMs in the lost provinces
            def weight(t):
                return 3 if PROV[t] in lost else 0
            r = self.sweep(g, 'R', weight)
            if r:
                g.activate('R', r[0], r[1], r[2])
                return 1
            if getattr(self, '_activating', False):
                return 0
            places = [s for s in range(N) if g.can_place('R', s) and REGION[s] == 'Provincia' and pc[PROV[s]] != 'R']
            if places:
                s = min(places, key=lambda s: (0 if PROV[s] == 'Narbonensis' else 1, compass_key(s, self.compass)))
                EV.do_influence(g, 'R', ('place', s))
                return 1
        return 0

    # ------------------------------------------------------------ danger (section 3)
    def threat_armies(self, g, enemy):
        """Every army the enemy could activate next (moved flags ignored): (cs, dist, leader, units, start)."""
        moved = [u for u in g.units.values() if u.side == enemy and u.moved]
        if enemy == 'R':
            moved += [l for l in g.leaders.values() if l.moved]
        for u in moved:
            u.moved = False
        out = []
        try:
            for leader, units, start in (self.gallic_armies(g) if enemy == 'G' else self.roman_armies(g)):
                if not units:
                    continue
                ma, dist, parent = self.army_reach(g, enemy, leader, units, start)
                cs = stack_strength(units + ([leader] if enemy == 'G' and leader is not None else []))
                out.append((cs, dist, leader, units, start))
        finally:
            for u in moved:
                u.moved = True
        return out

    def threat_after_move(self, g, enemy, base, movers, origin):
        """Largest enemy CS that can reach each space once `movers` have left `origin`.
        Vacating the origin can open a route that the movers were blocking (C02)."""
        friend = OTHER[enemy]
        others = [u for u in g.units.values() if u.loc == origin and u.side == friend and not u.inside
                  and u not in movers]
        m = {}
        if others or not any(origin in a[1] for a in base):
            for cs, dist, *_ in base:
                for t in dist:
                    if cs > m.get(t, 0):
                        m[t] = cs
            return m
        saved = [(u, u.loc) for u in movers]
        for u in movers:
            u.loc = 'lifted'
        try:
            for cs, dist, leader, units, start in base:
                if origin in dist:
                    dist = self.army_reach(g, enemy, leader, units, start)[1]
                for t in dist:
                    if cs > m.get(t, 0):
                        m[t] = cs
        finally:
            for u, l in saved:
                u.loc = l
        return m

    def in_danger(self, g, side, t, movers, tmap, removed=()):
        """Would `movers` (side's army) be in danger at t on the board after the move,
        with the enemy IMs in `removed` already taken off?"""
        enemy = OTHER[side]
        if side == 'R' and g.ctrl[t] == 'R' and g.ctype[t] == 'WC':
            return False
        if side == 'G' and g.ctrl[t] == 'G' and g.ctype[t] == 'FT':
            return False
        if t not in tmap:
            return False
        saved = [(s, g.ctrl[s], g.ctype[s]) for s in removed if g.ctype[s] == 'IM']
        for s, c, k in saved:
            g.ctrl[s] = None; g.ctype[s] = None
        try:
            els = g.local_support(enemy, t); ols = g.local_support(side, t)
        finally:
            for s, c, k in saved:
                g.ctrl[s] = c; g.ctype[s] = k
        own = stack_strength([u for u in g.units.values() if u.loc == t and u.side == side and u not in movers]
                             + list(movers)) + ols
        ratio = self.cfg['r_danger'] if side == 'R' else self.cfg['g_safe_raid']
        return tmap[t] + els >= ratio * own

    def gallic_threat(self, g):
        """Largest Gallic BS one Gallic army could bring into each space (moved flags ignored)."""
        thr = {}
        moved = [u for u in g.units.values() if u.side == 'G' and u.moved]
        for u in moved:
            u.moved = False
        try:
            for leader, units, start in self.gallic_armies(g):
                if not units:
                    continue
                ma, dist, parent = self.army_reach(g, 'G', leader, units, start)
                cs = stack_strength(units + ([leader] if leader is not None else []))
                for t in dist:
                    v = cs + g.local_support('G', t)
                    if v > thr.get(t, 0):
                        thr[t] = v
        finally:
            for u in moved:
                u.moved = True
        return thr

    def roman_threat(self, g):
        """Largest Roman BS one Roman army could bring into each space (moved flags ignored)."""
        thr = {}
        moved = [u for u in g.units.values() if u.side == 'R' and u.moved] + [l for l in g.leaders.values() if l.moved]
        for u in moved:
            u.moved = False
        try:
            for leader, units, start in self.roman_armies(g):
                if not units:
                    continue
                ma, dist, parent = self.army_reach(g, 'R', leader, units, start)
                cs = stack_strength(units)
                for t in dist:
                    v = cs + g.local_support('R', t)
                    if v > thr.get(t, 0):
                        thr[t] = v
        finally:
            for u in moved:
                u.moved = True
        return thr

    def gallic_unsafe(self, g, thr, t, extra=()):
        if g.ctrl[t] == 'G' and g.ctype[t] == 'FT':
            return False
        us = [u for u in g.units.values() if u.loc == t and u.side == 'G' and u not in extra] + list(extra)
        return thr.get(t, 0) >= self.cfg['g_regroup' if self.cfg['g_regroup'] else 'g_safe_raid'] * (stack_strength(us) + g.local_support('G', t))

    def m_regroup_g(self, g, ap):
        """A Gallic army Rome could attack at the danger ratio moves to safety (its own Fortified Town first)."""
        ratio = self.cfg.get('g_regroup')
        if not ratio:
            return 0
        thr = self.roman_threat(g)
        cz = g.leaders.get('Caesar')
        cands = []
        for leader, units, start in self.gallic_armies(g):
            allu = units + ([leader] if leader is not None else [])
            if not self.gallic_unsafe(g, thr, start):
                continue
            ma, dist, parent = self.army_reach(g, 'G', leader, units, start)
            for t, d in dist.items():
                if t == start or enemy_outside_at(g, t, 'G'):
                    continue
                if self.gallic_unsafe(g, thr, t, allu):
                    continue
                ft = g.ctrl[t] == 'G' and g.ctype[t] == 'FT'
                far = HOPS[cz.loc][t] if cz is not None and isinstance(cz.loc, int) else 0
                cands.append(((0 if ft else 1, -far, d), t, (leader, units, parent)))
        c = self.pick(cands)
        if not c:
            return 0
        leader, units, parent = c[2]
        g.activate('G', leader, units, [('to', x) for x in path_to(parent, c[1])])
        return 1

    def m_regroup(self, g, ap):
        """A Roman army (not Caesar's) that a Gallic army could attack at 1.5:1 joins a stronger
        Roman force or a Roman Walled City it can reach where it would be safe."""
        if not self.cfg.get('regroup'):
            return 0
        base = self.threat_armies(g, 'G')
        here = self.threat_after_move(g, 'G', base, [], None)   # the board as it stands

        def rbs(t):
            us = [u for u in g.units.values() if u.loc == t and u.side == 'R']
            return stack_strength(us) + g.local_support('R', t) if us else 0
        cands = []
        for leader, units, start in self.roman_armies(g):
            if leader is not None and leader.name == 'Caesar':
                continue
            if not self.in_danger(g, 'R', start, [], here):
                continue
            after = self.threat_after_move(g, 'G', base, units, start)
            ma, dist, parent = self.army_reach(g, 'R', leader, units, start)
            for t, d in dist.items():
                if t == start or enemy_outside_at(g, t, 'R'):
                    continue
                if self.in_danger(g, 'R', t, units, after):
                    continue
                cz = any(l.loc == t and l.name == 'Caesar' for l in g.leaders.values())
                cands.append(((-(here.get(start, 0) + g.local_support('G', start)) / max(1, rbs(start)),
                               0 if cz else 1, -rbs(t), d), t, (leader, units, parent)))
        c = self.pick(cands)
        if not c:
            return 0
        leader, units, parent = c[2]
        g.activate('R', leader, units, [('to', x) for x in path_to(parent, c[1])])
        return 1

    def m_submit(self, g, ap):
        """STRIKE restricted to targets that must Submit (3:1)."""
        saved = self.cfg.get('strike_submit_only')
        self.cfg['strike_submit_only'] = True
        try:
            return self.m_strike(g, ap)
        finally:
            self.cfg['strike_submit_only'] = saved

    def m_strike(self, g, ap):
        cands = []
        for leader, units, start in self.roman_armies(g):
            ma, dist, parent = self.army_reach(g, 'R', leader, units, start)
            caesar = leader is not None and leader.name == 'Caesar'
            ratio_need = self.cfg['r_strike_ratio_caesar'] if caesar else self.cfg['r_strike_ratio']
            for t, d in dist.items():
                if t == start:
                    continue
                ga = [u for u in g.units.values() if u.loc == t and u.side == 'G' and not u.inside]
                if not ga:
                    continue
                # units inside a fortification may come out and fight: count them all
                mine = self.bs(g, 'R', units, t); theirs = self.bs(g, 'G', [u for u in g.units.values() if u.loc == t and u.side == 'G'], t)
                if theirs <= 0:
                    continue
                r = mine / theirs
                if r >= 3:
                    cands.append(((0, -theirs, d), t, (leader, units, parent)))
                elif r >= ratio_need and not self.cfg.get('strike_submit_only'):
                    cands.append(((1, -theirs, d), t, (leader, units, parent)))
        c = self.pick(cands)
        if not c:
            return 0
        leader, units, parent = c[2]
        plan = [('to', x) for x in path_to(parent, c[1])]
        if g.ctype[c[1]] == 'FT':
            plan.append(('siege',))
        g.activate('R', leader, units, plan)
        return 1

    def raid_plan(self, g, side, leader, units, start, weight):
        """Best sequence of (move, remove) for one activation: remove enemy IMs along the way.
        weight(s) -> value of removing the IM at s (<=0: not wanted)."""
        ma, _, _ = self.army_reach(g, side, leader, units, start)
        cr = leader.cr if leader is not None else 2
        over = 1 if len(units) > cr else 0
        enemy = OTHER[side]
        best = (0, None)
        def ok_enter(t):
            if side == 'G' and REGION[t] in ('Germania', 'Britannia'):
                return False
            if enemy_outside_at(g, t, side):
                return False
            gt = g.german_tribe()
            return not (gt is not None and gt.loc == t)
        def removable(s, done):
            return (s not in done and g.ctrl[s] == enemy and g.ctype[s] == 'IM'
                    and not any(u.loc == s and u.side == enemy for u in g.units.values()))
        def dfs(s, mp, done, plan, val, depth):
            nonlocal best
            if val > best[0]:
                best = (val, list(plan))
            if depth > 5:
                return
            if mp >= 2 and removable(s, done) and weight(s) > 0:
                done.add(s); plan.append(('remove_im',))
                dfs(s, mp - 2, done, plan, val + weight(s), depth + 1)
                plan.pop(); done.discard(s)
                return
            for t, k in ADJ[s]:
                c = (1 if k == 'path' else 2) + over
                if c + 2 <= mp and ok_enter(t) and removable(t, done) and weight(t) > 0:
                    plan.append(('to', t))
                    dfs(t, mp - c, done, plan, val, depth + 1)
                    plan.pop()
        dfs(start, ma, set(), [], 0, 0)
        return best

    def sweep(self, g, side, weight, avoid=None):
        """Paper SWEEP: pick the target (highest weight enemy IM, no enemy CU, that some army reaches
        with 2+ MP left; then nearest; then compass).  The army that reaches it with the most MP
        left goes (ties: strongest), removes it, then keeps stepping to adjacent IMs while MP allow.
        Returns (leader, units, plan, total weight) or None."""
        enemy = OTHER[side]
        armies = self.roman_armies(g) if side == 'R' else self.gallic_armies(g)
        def removable(t, done=()):
            return (t not in done and g.ctrl[t] == enemy and g.ctype[t] == 'IM' and weight(t) > 0
                    and not any(u.loc == t and u.side == enemy for u in g.units.values())
                    and not (avoid and avoid(t)))
        use = (side == 'R' and self.cfg.get('safe_raid')) or (side == 'G' and self.cfg.get('g_safe_raid'))
        base = self.threat_armies(g, OTHER[side]) if use else None
        tcache = {}

        def unsafe(t, leader, units, removed=()):
            if base is None or (side == 'R' and leader is not None and leader.name == 'Caesar'):
                return False
            movers = list(units) + ([leader] if side == 'G' and leader is not None and isinstance(leader, Unit) else [])
            if not movers:
                return False
            origin = movers[0].loc
            key = (origin, frozenset(u.uid for u in movers))
            if key not in tcache:
                tcache[key] = self.threat_after_move(g, OTHER[side], base, movers, origin)
            return self.in_danger(g, side, t, movers, tcache[key], tuple(removed) + (t,))
        cands = []
        for leader, units, start in armies:
            ma, dist, parent = self.army_reach(g, side, leader, units, start)
            for t, d in dist.items():
                if ma - d >= 2 and removable(t) and not unsafe(t, leader, units):
                    cands.append(((-weight(t), d, -(ma - d), -stack_strength(units)), t, (leader, units, start, parent, ma - d)))
        c = self.pick(cands)
        if not c:
            return None
        leader, units, start, parent, left = c[2]
        t = c[1]
        plan = [('to', x) for x in path_to(parent, t)] + [('remove_im',)]
        total = weight(t)
        left -= 2
        cr = leader.cr if leader is not None else 2
        over = 1 if len(units) > cr else 0
        cur = t; done = {t}
        while True:
            nxt = []
            for x, k in ADJ[cur]:
                cost = (1 if k == 'path' else 2) + over
                if cost + 2 <= left and removable(x, done) and not enemy_outside_at(g, x, side) \
                        and not (side == 'G' and REGION[x] in ('Germania', 'Britannia')) and not unsafe(x, leader, units, done):
                    nxt.append(((-weight(x),), x, cost))
            if not nxt:
                break
            pick = min(nxt, key=lambda n: (n[0], compass_key(n[1], self.compass)))
            plan += [('to', pick[1]), ('remove_im',)]
            left -= pick[2] + 2
            total += weight(pick[1])
            cur = pick[1]; done.add(cur)
        return (leader, units, plan, total)

    def m_raid(self, g, ap):
        """Rome RAID: sweep Gallic IMs worth 2+ (see weights)."""
        pc = g.prov_control()
        def weight(t):
            p = PROV[t]
            if REGION[t] in ('Germania', 'Britannia'):
                return 0
            if REGION[t] == 'Provincia':
                return 4
            if pc[p] == 'G':
                return 4 if REGION[t] == 'Celtica' else 3
            if prov_margin(g, p, 'R') <= 1 and not any(g.ctype[x] == 'FT' for x in PROVINCES[p]['idx']):
                return 2
            return 0
        r = self.sweep(g, 'R', weight)
        if not r:
            return 0
        g.activate('R', r[0], r[1], r[2])
        return 1

    def m_invade(self, g, ap, force=False):
        if g.turn < self.cfg['r_invade_turn'] and not force:
            return 0
        self.expedition = False
        cz = g.leaders.get('Caesar')
        if not cz or not isinstance(cz.loc, int) or cz.moved:
            return 0
        units = [u for u in g.units.values() if u.loc == cz.loc and u.side == 'R' and not u.moved and not g.unit_besieged(u)]
        units.sort(key=lambda u: -u.strength())
        units = units[:6]
        if stack_strength(units) < self.cfg['invade_cs']:
            return 0
        targets = []
        if not g.britannia_done:
            targets += [s for s in BRITANNIA_VP if g.ctrl[s] == 'G']
        if not g.germania_done:
            targets += [s for s in GERMANIA_VP if g.ctrl[s] == 'G']
        if not targets:
            return 0
        ma, dist, parent = self.army_reach(g, 'R', cz, units, cz.loc)
        # in reach with 2 MP to remove?
        best = None
        for t in targets:
            if t in dist and ma - dist[t] >= 2:
                if best is None or dist[t] < best[0]:
                    best = (dist[t], t)
        if best:
            g.activate('R', cz, units, [('to', x) for x in path_to(parent, best[1])] + [('remove_im',)])
            # more targets left in the same land: keep going
            self.expedition = any(g.ctrl[t] == 'G' for t in (BRITANNIA_VP if best[1] in BRITANNIA_VP else GERMANIA_VP))
            return 1
        # march toward the nearest target
        goal = min(targets, key=lambda t: HOPS[cz.loc][t])
        stops = [t for t in dist if t != cz.loc and not enemy_outside_at(g, t, 'R')]
        if not stops:
            return 0
        t = min(stops, key=lambda x: (HOPS[x][goal], dist[x]))
        if HOPS[t][goal] >= HOPS[cz.loc][goal]:
            return 0
        g.activate('R', cz, units, [('to', x) for x in path_to(parent, t)])
        self.expedition = True
        return 1

    def near_sup(self, t, sup=None):
        """Paper test: the space, or a space next to it, holds a Roman control marker."""
        return self.g_ref.ctrl[t] == 'R' or any(self.g_ref.ctrl[x] == 'R' for x, k in ADJ[t])

    def m_march(self, g, ap):
        """Move the strongest unmoved leader-led army toward the nearest Gallic Fortified Town
        that lies in or next to Roman supply."""
        armies = [a for a in self.roman_armies(g) if a[0] is not None]
        if not armies:
            return 0
        sup = self.rsup(g)
        fts = [s for s in range(N) if g.ctype[s] == 'FT' and self.near_sup(s, sup)] or \
            [s for s in range(N) if g.ctype[s] == 'FT']
        if not fts:
            return 0
        for leader, units, start in armies:
            cs = stack_strength(units)
            if cs < 6:
                continue
            ma, dist, parent = self.army_reach(g, 'R', leader, units, start)
            goal = min(fts, key=lambda t: (HOPS[start][t], compass_key(t, self.compass)))
            if HOPS[start][goal] <= 1:
                continue
            stops = [t for t in dist if t != start and not enemy_outside_at(g, t, 'R') and g.ctype[t] != 'FT'
                     and self.near_sup(t)]
            if not stops:
                continue
            t = min(stops, key=lambda x: (HOPS[x][goal], -dist[x], compass_key(x, self.compass)))
            if HOPS[t][goal] >= HOPS[start][goal]:
                continue
            g.activate('R', leader, units, [('to', x) for x in path_to(parent, t)])
            return 1
        return 0

    def m_gather(self, g, ap):
        """A leaderless Legion stack joins the nearest Roman leader it can reach."""
        lead_spaces = {l.loc for l in g.leaders.values() if isinstance(l.loc, int)}
        for leader, units, start in self.roman_armies(g):
            if leader is not None or not units:
                continue
            ma, dist, parent = self.army_reach(g, 'R', None, units, start)
            opts = [t for t in dist if t in lead_spaces]
            if opts:
                t = min(opts, key=lambda x: dist[x])
                g.activate('R', None, units, [('to', x) for x in path_to(parent, t)])
                return 1
        return 0

    def m_control(self, g, ap):
        act = self.roman_control_choice(g)
        if act is None:
            return 0
        EV.do_influence(g, 'R', act)
        return 1

    def m_rule(self, g, ap):
        """Control Table lines 0-3 only (presence, convert, Provincia, gain control)."""
        act = self.roman_control_choice(g, strong_only=True)
        if act is None:
            return 0
        EV.do_influence(g, 'R', act)
        return 1

    def m_settle(self, g, ap):
        return self.m_control(g, ap)

    def pending_provinces(self, g):
        """Provinces whose Tribe is still in the Pool (it would arrive with a Fortified Town)."""
        return {g.units[x].prov for x in g.pool}

    def open_towns(self, g, p):
        n = 0
        for s in PROVINCES[p]['idx']:
            if STYPE[s] != 'town' or g.ctype[s] in ('FT', 'SH', 'WC'):
                continue
            if g.ctrl[s] == 'R' or any(u.loc == s and u.side == 'R' for u in g.units.values()):
                continue
            n += 1
        return n

    def roman_control_choice(self, g, allowed=None, strong_only=False):
        """Roman Control Table (first line that applies; Celtica before Belgica before others)."""
        pc = g.prov_control()
        if allowed is None:
            conv = [s for s in range(N) if g.can_convert('R', s)]
            places = [s for s in range(N) if g.can_place('R', s)]
        else:
            conv = [s for k, s in allowed if k == 'convert']
            places = [s for k, s in allowed if k == 'place']
        regord = {'Celtica': 0, 'Belgica': 1, 'Aquitania': 2, 'Provincia': 3, 'Germania': 4, 'Britannia': 4}
        if self.cfg.get('dominance_race'):
            # the region where Rome lacks Dominance (and is closest to it) comes first
            # the region where Rome lacks Dominance comes first (if both, the one Gaul leads by less);
            # if Rome has Dominance in both, Celtica first
            gap = {}
            for reg in ('Celtica', 'Belgica'):
                r = sum(1 for p in REG_PROVS[reg] if pc[p] == 'R'); gl = sum(1 for p in REG_PROVS[reg] if pc[p] == 'G')
                gap[reg] = (0, gl - r) if r <= gl else (1, 0)
            first, second = sorted(('Celtica', 'Belgica'), key=lambda r: (gap[r], r != 'Celtica'))
            regord = {first: 0, second: 1, 'Aquitania': 2, 'Provincia': 3, 'Germania': 4, 'Britannia': 4}
        def ft_in(p):
            return any(g.ctype[s] == 'FT' for s in PROVINCES[p]['idx'])
        def key(s, *extra):
            return extra + (regord[REGION[s]], compass_key(s, self.compass))
        # 0 safety: presence in every region of Gaul
        for reg in ('Aquitania', 'Belgica', 'Celtica'):
            if not any(g.ctrl[s] == 'R' for p in REG_PROVS[reg] for s in PROVINCES[p]['idx']):
                opts = [s for s in places if REGION[s] == reg]
                cv = [s for s in conv if REGION[s] == reg]
                if cv:
                    return ('convert', min(cv, key=key))
                if opts:
                    return ('place', min(opts, key=key))
        # 1 convert
        if conv:
            return ('convert', min(conv, key=lambda s: key(s, 0 if pc[PROV[s]] == 'G' else 1)))
        # 2 restore Provincia
        prov = [s for s in places if REGION[s] == 'Provincia' and pc[PROV[s]] != 'R']
        if prov:
            return ('place', min(prov, key=lambda s: key(s, 0 if PROV[s] == 'Narbonensis' else 1)))
        pending = self.pending_provinces(g)
        if self.cfg.get('block_first'):
            blk = [s for s in places if PROV[s] in pending and REGION[s] in GAUL_REGIONS]
            if blk:
                return ('place', min(blk, key=lambda s: key(s, self.open_towns(g, PROV[s]))))
        # 3 gain control (one IM short, no Fortified Town)
        gain = [s for s in places if prov_margin(g, PROV[s], 'R') == 1 and not ft_in(PROV[s]) and pc[PROV[s]] != 'R'
                and REGION[s] in GAUL_REGIONS]
        if gain:
            return ('place', min(gain, key=key))
        if strong_only:
            return None
        # 4 deny: Gaul one short of control and no Roman marker there yet
        deny = [s for s in places if REGION[s] in GAUL_REGIONS and pc[PROV[s]] is None and prov_margin(g, PROV[s], 'G') == 1]
        if deny and self.cfg.get('deny', True):
            return ('place', min(deny, key=key))
        # 5 block: fill the open Towns of a province whose Tribe has not yet arrived
        pending = self.pending_provinces(g)
        blk = [s for s in places if PROV[s] in pending]
        if blk and self.cfg.get('block', True):
            return ('place', min(blk, key=lambda s: key(s, self.open_towns(g, PROV[s]))))
        # 6 presence in a region with none
        for reg in ('Celtica', 'Belgica', 'Aquitania'):
            if not any(g.ctrl[s] == 'R' for p in REG_PROVS[reg] for s in PROVINCES[p]['idx']):
                opts = [s for s in places if REGION[s] == reg]
                if opts:
                    return ('place', min(opts, key=key))
        # 7 province (no FT, not yet Roman) closest to control
        opts = [s for s in places if REGION[s] in GAUL_REGIONS and not ft_in(PROV[s]) and pc[PROV[s]] != 'R']
        if opts:
            return ('place', min(opts, key=lambda s: key(s, prov_margin(g, PROV[s], 'R'))))
        opts = [s for s in places if REGION[s] in GAUL_REGIONS]
        if opts:
            return ('place', min(opts, key=lambda s: key(s, -sum(1 for t, k in ADJ[s] if g.ctrl[t] == 'R'))))
        if places:
            return ('place', min(places, key=key))
        return None

    # ============================================================ GALLIC missions
    def m_rise(self, g, ap):
        free_tribes = [x for x in g.council_tribes if not (g.units[x].name == 'Arverni' and not g.arverni_free())
                       and g.legal_tribe_spaces(g.units[x])]
        sub = [g.units[x] for x in g.submitted if g.units[x].loc == 'submitted' and g.legal_tribe_spaces(g.units[x])]
        if g.turn >= 4 and ap >= 2 and len(sub) >= 2:
            self.major_uprising(g)
            return 2
        if free_tribes or g.council_ims >= self.cfg['rise_min'] or (g.council_ims and len(g.hands['G']) == 0):
            self.council_take(g)
            return 1
        return 0

    def m_bank(self, g, ap):
        if g.turn > self.cfg['bank_turn_max'] or g.council_ims >= 6:
            return 0
        g.council_ims += 1
        return 1

    def m_ambush(self, g, ap):
        cands = []
        for leader, units, start in self.gallic_armies(g):
            ma, dist, parent = self.army_reach(g, 'G', leader, units, start)
            for t, d in dist.items():
                if t == start:
                    continue
                ra = [u for u in g.units.values() if u.loc == t and u.side == 'R' and not u.inside]
                if not ra:
                    continue
                caesar = any(l.loc == t and l.name == 'Caesar' for l in g.leaders.values())
                mine = self.bs(g, 'G', units + ([leader] if leader is not None else []), t)
                theirs = self.bs(g, 'R', [u for u in g.units.values() if u.loc == t and u.side == 'R'], t)
                need = self.cfg['g_ambush_ratio'] * (1.4 if caesar else 1.0)
                if theirs > 0 and mine >= need * theirs:
                    cands.append(((0 if caesar else 1, -theirs, d), t, (leader, units, parent)))
        c = self.pick(cands)
        if not c:
            return 0
        leader, units, parent = c[2]
        g.activate('G', leader, units, [('to', x) for x in path_to(parent, c[1])])
        return 1

    def m_raid_g(self, g, ap):
        """Gaul RAID: sweep Roman IMs (Narbonensis 4, other Provincia 2, Roman-controlled province 3,
        else 1); never a target in or next to Caesar's space."""
        pc = g.prov_control()
        cz = g.leaders.get('Caesar')
        def weight(t):
            p = PROV[t]
            if p == 'Narbonensis':
                return 4
            if pc[p] == 'R':
                return 3
            if REGION[t] == 'Provincia':
                return 2
            return 1
        def avoid(t):
            return cz is not None and isinstance(cz.loc, int) and HOPS[cz.loc][t] <= 1
        r = self.sweep(g, 'G', weight, avoid)
        if not r:
            return 0
        g.activate('G', r[0], r[1], r[2])
        return 1

    def m_agitate(self, g, ap):
        act = self.gallic_agitate_choice(g)
        if act is None:
            return 0
        EV.do_influence(g, 'G', act)
        return 1

    def gallic_agitate_choice(self, g, allowed=None):
        pc = g.prov_control()
        if allowed is None:
            conv = [s for s in range(N) if g.can_convert('G', s)]
            places = [s for s in range(N) if g.can_place('G', s)]
        else:
            conv = [s for k, s in allowed if k == 'convert']
            places = [s for k, s in allowed if k == 'place']
        if conv:
            return ('convert', min(conv, key=lambda s: (0 if pc[PROV[s]] == 'R' else 1, compass_key(s, self.compass))))
        prov = [s for s in places if REGION[s] == 'Provincia']
        if prov:
            return ('place', min(prov, key=lambda s: (0 if PROV[s] == 'Narbonensis' else 1, compass_key(s, self.compass))))
        gain = [s for s in places if prov_margin(g, PROV[s], 'G') == 1 and pc[PROV[s]] != 'G' and REGION[s] in GAUL_REGIONS]
        if gain:
            return ('place', min(gain, key=lambda s: (0 if REGION[s] == 'Celtica' else 1, compass_key(s, self.compass))))
        deny = [s for s in places if REGION[s] in GAUL_REGIONS and pc[PROV[s]] != 'R' and prov_margin(g, PROV[s], 'R') == 1
                and not any(g.ctype[x] == 'FT' for x in PROVINCES[PROV[s]]['idx'])]
        if deny:
            return ('place', min(deny, key=lambda s: compass_key(s, self.compass)))
        cut = [s for s in places if REGION[s] in GAUL_REGIONS and sum(1 for t, k in ADJ[s] if g.ctrl[t] == 'R' and g.ctype[t] == 'IM') >= 2]
        if cut:
            return ('place', min(cut, key=lambda s: (-sum(1 for t, k in ADJ[s] if g.ctrl[t] == 'R'), compass_key(s, self.compass))))
        opts = [s for s in places if REGION[s] in GAUL_REGIONS]
        if opts:
            return ('place', min(opts, key=lambda s: (pc[PROV[s]] == 'G', prov_margin(g, PROV[s], 'G'), compass_key(s, self.compass))))
        if places:
            return ('place', min(places, key=lambda s: compass_key(s, self.compass)))
        return None

    def try_mission(self, g, side, m, ap):
        if side == 'G' and m == 'RAID':
            return self.m_raid_g(g, ap)
        if side == 'G' and m == 'REGROUP':
            return self.m_regroup_g(g, ap)
        fn = getattr(self, 'm_' + m.lower(), None)
        if fn is None:
            return 0
        return fn(g, ap)

    def council_take(self, g):
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
            act = self.gallic_agitate_choice(g)
            if act is None or act[0] != 'place':
                opts = [s for s in range(N) if g.can_place('G', s)]
                if not opts:
                    break
                act = ('place', opts[0])
            EV.do_influence(g, 'G', act)

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
        n = g.council_ims
        g.council_ims = 0
        pc = g.prov_control()
        for _ in range(n):
            rem = [s for s in range(N) if g.ctrl[s] == 'R' and g.ctype[s] == 'IM' and REGION[s] in GAUL_REGIONS]
            if rem:
                s = min(rem, key=lambda s: (0 if g.prov_control()[PROV[s]] == 'R' else 1, compass_key(s, self.compass)))
                g.remove_im(s)
        for x in list(g.council_tribes):
            u = g.units[x]
            if u.name == 'Arverni' and not g.arverni_free():
                continue
            sp = g.legal_tribe_spaces(u)
            if sp:
                g.council_tribes.remove(x)
                g.place_tribe(u, self.place_tribe_choice(g, u, sp, False))

    # ============================================================ activation events
    ACT_R = ('PROTECT', 'SUBMIT', 'CONTINUE', 'SIEGE', 'STRIKE', 'INVADE', 'RAID', 'GATHER')
    ACT_G = ('AMBUSH', 'RAID')

    def activate_leader(self, g, side, leader, free=True):
        """Event activation of one named leader: his army does the first Activation Mission
        (Imperator: PROTECT, SUBMIT, CONTINUE, SIEGE, STRIKE, INVADE, RAID) it can."""
        self._activating = True
        try:
            for m in (self.ACT_R if side == 'R' else self.ACT_G):
                if m == 'GATHER':
                    continue
                if self.try_filtered(g, side, m, lambda a: a[0] is leader):
                    return
        finally:
            self._activating = False

    def try_filtered(self, g, side, m, keep):
        """Run mission m with the bot's armies limited to those for which keep(army) is true."""
        base = BotPolicy.roman_armies if side == 'R' else BotPolicy.gallic_armies
        def only(gg, _base=base):
            return [a for a in _base(self, gg) if keep(a)]
        attr = 'roman_armies' if side == 'R' else 'gallic_armies'
        setattr(self, attr, only)
        try:
            if m == 'INVADE':
                return self.m_invade(g, 1) if any(keep(a) and a[0] is not None and getattr(a[0], 'name', '') == 'Caesar'
                                                  for a in base(self, g)) else 0
            return self.try_mission(g, side, m, 1)
        finally:
            delattr(self, attr)

    def mass_activation(self, g, side, units, purpose, ma=None):
        """Activation events: armies act one at a time, each doing the first Activation Mission
        it can, until no eligible army can do anything.
        Belgic Confederation: armies in Belgica only.  Caesar's Legions: Legion stacks without a
        leader only.  Motus Ubique: at most one army per Region."""
        if self.directive is None:
            self.draw_directive()
        self.compass = self.directive[2]
        missions = self.ACT_R if side == 'R' else self.ACT_G
        regions_done = set()
        def keep(a):
            leader, units_, start = a
            if purpose == 'belgic_confederation' and REGION[start] != 'Belgica':
                return False
            if purpose == 'caesars_legions' and (leader is not None or any(l.loc == start for l in g.leaders.values())):
                return False
            if purpose == 'motus_ubique' and REGION[start] in regions_done:
                return False
            return True
        self._activating = True
        try:
            self._mass(g, side, missions, keep, purpose, regions_done)
        finally:
            self._activating = False

    def _mass(self, g, side, missions, keep, purpose, regions_done):
        for _ in range(20):
            acted = False
            for m in missions:
                before = {id(u): u.loc for u in g.units.values()}
                starts = {}
                for a in (BotPolicy.roman_armies(self, g) if side == 'R' else BotPolicy.gallic_armies(self, g)):
                    if keep(a):
                        for u in a[1]:
                            starts[u.uid] = a[2]
                if self.try_filtered(g, side, m, keep):
                    acted = True
                    if purpose == 'motus_ubique':
                        moved = [starts[u.uid] for u in g.units.values() if u.uid in starts and u.moved]
                        if moved:
                            regions_done.add(REGION[moved[0]])
                    break
            if not acted:
                break

    def choose_ims_to_remove(self, g, ims, n):
        """Caesar displaced: Roman IMs outside Roman-controlled provinces first, Provincia last."""
        pc = g.prov_control()
        return sorted(ims, key=lambda s: (REGION[s] == 'Provincia', pc[PROV[s]] == 'R', compass_key(s, self.compass)))[:n]

    def choose_unit(self, g, side, units, purpose):
        if purpose == 'restore' and side == 'R':
            return self.choose_replacement(g, units)
        return super().choose_unit(g, side, units, purpose)

    def choose_replacement(self, g, red):
        cz = g.leaders.get('Caesar')
        def key(u):
            with_c = cz is not None and u.loc == cz.loc
            n = sum(1 for x in g.units.values() if x.loc == u.loc and x.kind == 'legion')
            return (with_c, n)
        return max(red, key=key)

    # ============================================================ event targets (paper rules)
    def choose_influence(self, g, side, opts, purpose):
        act = self.roman_control_choice(g, opts) if side == 'R' else self.gallic_agitate_choice(g, opts)
        return act if act is not None else opts[0]

    def im_weight(self, g, side, t):
        """Weight of removing / converting the enemy IM at t (the RAID weights)."""
        pc = g.prov_control()
        p = PROV[t]
        if side == 'R':
            if REGION[t] in ('Germania', 'Britannia'):
                return 1
            if REGION[t] == 'Provincia':
                return 4
            if pc[p] == 'G':
                return 4 if REGION[t] == 'Celtica' else 3
            if prov_margin(g, p, 'R') <= 1 and not any(g.ctype[x] == 'FT' for x in PROVINCES[p]['idx']):
                return 2
            return 1
        if p == 'Narbonensis':
            return 4
        if pc[p] == 'R':
            return 3
        if REGION[t] == 'Provincia':
            return 2
        return 1

    def choose_space(self, g, side, opts, purpose):
        if not opts:
            return None
        if purpose in ('remove_enemy_im', 'convert'):
            return min(opts, key=lambda t: (-self.im_weight(g, side, t), compass_key(t, self.compass)))
        if purpose == 'devastate':
            rim = [t for t in opts if g.ctrl[t] == 'R' and g.ctype[t] == 'IM']
            if not rim:
                return None
            return min(rim, key=lambda t: (-sum(1 for u in g.units.values() if u.kind == 'legion' and isinstance(u.loc, int)
                                                and HOPS[u.loc][t] <= 1), compass_key(t, self.compass)))
        if purpose in ('mercenary', 'militia', 'minor_tribe'):
            def near_leg(t):
                return min([HOPS[u.loc][t] for u in g.units.values() if u.kind == 'legion' and isinstance(u.loc, int)] + [99])
            return min(opts, key=lambda t: (near_leg(t), compass_key(t, self.compass)))
        if purpose == 'upgrade_ft':
            def near_leg(t):
                return min([HOPS[u.loc][t] for u in g.units.values() if u.kind == 'legion' and isinstance(u.loc, int)] + [99])
            return min(opts, key=lambda t: (near_leg(t), compass_key(t, self.compass)))
        if purpose == 'cavalry':
            cz = g.leaders.get('Caesar')
            if cz is not None and cz.loc in opts:
                return cz.loc
            return max(opts, key=lambda t: (sum(1 for u in g.units.values() if u.loc == t and u.kind == 'legion'),
                                            -compass_key(t, self.compass)))
        if purpose == 'siege_point':
            return max(opts, key=lambda t: (g.siege.get(t, 0), -compass_key(t, self.compass)))
        if purpose == 'aedui':
            return min(opts, key=lambda t: compass_key(t, self.compass))
        if purpose.startswith('leader_arrival') or purpose == 'winter_leader':
            return max(opts, key=lambda t: (sum(u.strength() for u in g.units.values() if u.loc == t and u.side == 'G'),
                                            g.ctype[t] == 'FT', -compass_key(t, self.compass)))
        if purpose == 'im_relocate':
            return min(opts, key=lambda t: compass_key(t, self.compass))
        if purpose in ('caesar', 'reinforce', 'replace') or purpose.startswith('legate') or purpose == 'labienus':
            def legs(t):
                return sum(1 for u in g.units.values() if u.loc == t and u.kind == 'legion')
            def has_leader(t):
                return any(l.loc == t for l in g.leaders.values())
            if purpose == 'caesar':
                return max(opts, key=lambda t: (legs(t), -compass_key(t, self.compass)))
            if purpose in ('reinforce', 'replace'):
                cz = g.leaders.get('Caesar')
                if cz and cz.loc in opts:
                    return cz.loc
                return max(opts, key=lambda t: (legs(t), -compass_key(t, self.compass)))
            # legates / Labienus: the largest Legion stack without a leader, else with Caesar
            free = [t for t in opts if legs(t) > 0 and not has_leader(t)]
            if free:
                return max(free, key=lambda t: (legs(t), -compass_key(t, self.compass)))
            cz = g.leaders.get('Caesar')
            if cz is not None and cz.loc in opts:
                return cz.loc
            return max(opts, key=lambda t: (legs(t), -compass_key(t, self.compass)))
        return super().choose_space(g, side, opts, purpose)

    def avoid_dest(self, g, side, s, units, dests):
        return min(dests, key=lambda t: (g.ctrl[t] != side, not any(u.loc == t and u.side == side for u in g.units.values()),
                                         compass_key(t, self.compass)))

    def choose_retreat(self, g, side, units, s, dests):
        return min(dests, key=lambda t: (any(u.loc == t and u.side == OTHER[side] for u in g.units.values()),
                                         g.ctrl[t] != side,
                                         not any(u.loc == t and u.side == side for u in g.units.values()),
                                         EDGE.get((s, t)) == 'channel',
                                         compass_key(t, self.compass)))

    def choose_province(self, g, side, provs, purpose):
        pc = g.prov_control()
        return max(provs, key=lambda p: (pc[p] == 'R', sum(1 for x in PROVINCES[p]['idx'] if g.ctrl[x] == 'R' and g.ctype[x] == 'IM'),
                                         -compass_key(PROVINCES[p]['idx'][0], self.compass)))

    def choose_german_start(self, g, side, shs):
        for sh in sorted(shs, key=lambda x: compass_key(GERMAN_SH[x][0], self.compass)):
            if any(g.ctrl[e] == OTHER[side] and g.ctype[e] == 'IM' for e in GERMAN_SH[sh]):
                return sh
        return None

    def choose_german_dest(self, g, side, dests):
        tg = [t for t in dests if g.ctrl[t] == OTHER[side] and g.ctype[t] == 'IM']
        if tg:
            return min(tg, key=lambda t: (-self.im_weight(g, side, t), compass_key(t, self.compass)))
        return None

    # ============================================================ reserve cards
    CANCEL = {'R': (5, 16, 53, 6, 14, 36, 21, 43, 27, 8),   # Imperator cancels these Gallic events
              'G': (1, 2, 4, 11, 3, 10, 12)}               # Concilium cancels these Roman events

    # ------------------------------------------------------------ Reserve (1.3)
    def sync_reserve(self, g, side):
        """The Reserve holds only cards revealed face up this turn that are still in the hand."""
        if getattr(self, '_reserve_turn', None) != g.turn:
            self.reserve = set()
            self._reserve_turn = g.turn
        self.reserve = set(c for c in self.reserve if c in g.hands[side])
        return self.reserve

    def in_reserve(self, g, side, c):
        return c in self.sync_reserve(g, side)

    def react(self, g, side, c):
        return self.in_reserve(g, side, 24) and c in self.CANCEL[side]

    def use_vow_battle(self, g, side, s, a_bs, d_bs, attacker):
        return self.in_reserve(g, side, 52) and abs(a_bs - d_bs) <= 3

    def use_vow_siege(self, g, s):
        return self.in_reserve(g, 'R', 52)

    def use_remedies(self, g, side, roller, drm):
        # +2 to the bot's own Avoid Battle / Interception roll
        return self.in_reserve(g, side, 54) and roller == side

    def discard_surprise(self, g, side, sur):
        # Forced March in the Reserve is discarded at the start of the bot's next card play
        return any(c == 55 and self.in_reserve(g, side, 55) for c in sur)

    # ============================================================ reactions & phases
    def avoid(self, g, side, s, units, movers, prev):
        mine = stack_strength(units) + g.local_support(side, s)
        theirs = stack_strength(movers) + g.local_support(OTHER[side], s)
        if side == 'G' and theirs >= 3 * mine:
            return True
        ratio = self.cfg['g_avoid_ratio'] if side == 'G' else self.cfg['r_avoid_ratio']
        return theirs >= ratio * mine

    def inside_outside(self, g, side, s, defenders, movers):
        mine = stack_strength(defenders) + g.local_support(side, s)
        theirs = stack_strength(movers) + g.local_support(OTHER[side], s)
        if theirs >= self.cfg['g_inside_ratio'] * mine:
            return list(defenders)
        return []

    def intercept(self, g, side, to, frm, movers, mleader, candidates):
        mstr = stack_strength(movers) + g.local_support(OTHER[side], to)
        caesar_moving = isinstance(mleader, Leader) and mleader.name == 'Caesar'
        best = None
        for t, (us, ls, k) in candidates.items():
            us = [u for u in us if not u.inside]
            if not us:
                continue
            here = [u for u in g.units.values() if u.loc == to and u.side == side and not u.inside]
            mine = stack_strength(us) + stack_strength(here) + g.local_support(side, to)
            need = 2.0 if side == 'R' else (2.0 if caesar_moving else 1.5)
            if mine >= need * mstr:
                lead = max(ls, key=lambda l: l.br) if (side == 'R' and ls) else None
                if best is None or mine > best[0]:
                    best = (mine, t, us, lead)
        if best:
            return {best[1]: (best[2], best[3])}
        return None

    def reroll_choice(self, g, side, my_bs, opp_bs, mine, theirs, side_is_attacker, opp_side):
        lo = min(range(2), key=lambda i: mine[i])
        hi = max(range(2), key=lambda i: theirs[i])
        if (max(3, mine[lo]) if side == 'R' else mine[lo]) <= 3:
            return ('own', lo)
        oval = theirs[hi]
        if oval >= 5 and not (opp_side == 'R' and oval <= 3):
            return ('opp', hi)
        return None

    def choose_reinforcements(self, g, drawn):
        drawn = sorted(drawn, key=lambda u: (len(g.legal_tribe_spaces(u)) > 0, u.cs[-1]), reverse=True)
        return drawn[:3], drawn[3:]

    def place_tribe_choice(self, g, u, spaces, council_ok):
        if not spaces:
            return 'council'
        def danger(s):
            return min([HOPS[x.loc][s] for x in g.units.values() if x.side == 'R' and isinstance(x.loc, int) and x.kind == 'legion'] + [99])
        far = max(spaces, key=lambda s: (min(danger(s), 4), -sum(1 for t, k in ADJ[s] if g.ctrl[t] == 'R'), -compass_key(s, 'N')))
        return far

    def winter_camp(self, g):
        legs = sorted(g.on_map('R', 'legion'), key=lambda u: -u.steps)
        load = {}
        for u in legs:
            load[u.loc] = load.get(u.loc, 0)
        load = {}
        for u in legs:
            dist, parent = reach(g, 'R', u.loc, 3, 99, 1)
            cap_here = g.forage(u.loc)
            best = None
            for t, d in dist.items():
                gt = g.german_tribe()
                if gt is not None and gt.loc == t:
                    continue
                if load.get(t, 0) >= g.forage(t):
                    continue
                # pairs of legions into neutral Gallic spaces next to Roman influence (they become Roman IMs)
                pc = g.prov_control()
                pri = 4
                if self.cfg.get('winter_neutral') and g.ctrl[t] is None and REGION[t] in GAUL_REGIONS \
                        and any(g.ctrl[x] == 'R' for x, k in ADJ[t]):
                    pri = -1
                elif g.ctrl[t] == 'R' and g.ctype[t] == 'IM' and pc[PROV[t]] == 'R':
                    pri = 0
                elif g.ctype[t] == 'WC' and g.ctrl[t] == 'R':
                    pri = 1
                elif g.ctrl[t] == 'R' and g.ctype[t] == 'IM':
                    pri = 2
                elif g.ctrl[t] is None and REGION[t] in GAUL_REGIONS:
                    pri = 3
                key = (pri, d, compass_key(t, 'N'))
                if best is None or key < best[0]:
                    best = (key, t)
            if best is None:
                continue
            t = best[1]
            load[t] = load.get(t, 0) + 1
            if t != u.loc:
                g.winter_camp_move(u, path_to(parent, t))

    def spring_muster(self, g):
        return
