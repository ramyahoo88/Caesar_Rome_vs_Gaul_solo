"""Shared planning helpers: reachability, targets, influence valuation."""
import heapq
from engine import (N, NAMES, IDX, ADJ, EDGE, PROV, REGION, STYPE, PROVINCES, REG_PROVS, GAUL_REGIONS,
                    PROVINCIA, OTHER, Leader, Unit, GERMANIA_VP, BRITANNIA_VP, OCTODURUS, BRIGANTIUM)


def enemy_outside_at(g, s, side):
    return any(u.loc == s and u.side != side and not u.inside for u in g.units.values())


def reach(g, side, start, ma, cr, ncu, alone=False):
    """Dijkstra over movement costs. Returns (dist, parent). Spaces holding enemy CUs outside
    (or the German tribe) are terminal: they can be entered but not passed through."""
    dist = {start: 0}
    parent = {start: None}
    pq = [(0, start)]
    over = 1 if ncu > cr else 0
    gt = g.german_tribe()
    while pq:
        d, s = heapq.heappop(pq)
        if d > dist.get(s, 99):
            continue
        if s != start and (enemy_outside_at(g, s, side) or (gt is not None and gt.loc == s)):
            continue
        for t, k in ADJ[s]:
            if side == 'G' and REGION[t] in ('Germania', 'Britannia'):
                continue
            if alone:
                if enemy_outside_at(g, t, side) or g.ctype[t] in ('FT', 'SH') or (gt is not None and gt.loc == t):
                    continue
            c = d + (1 if k == 'path' else 2) + over
            if c <= ma and c < dist.get(t, 99):
                dist[t] = c; parent[t] = s
                heapq.heappush(pq, (c, t))
    return dist, parent


def path_to(parent, t):
    p = []
    while t is not None:
        p.append(t); t = parent[t]
    return list(reversed(p))[1:]


def stack_strength(units):
    return sum(u.strength() for u in units)


def gallic_army_at(g, s):
    return [u for u in g.units.values() if u.loc == s and u.side == 'G' and not u.inside]


def roman_army_at(g, s):
    return [u for u in g.units.values() if u.loc == s and u.side == 'R' and not u.inside]


# ---------------------------------------------------------------- influence valuation
def gov_and_provs(g):
    pc = g.prov_control()
    gov = g.governance()
    r = sum(1 for p, v in pc.items() if v == 'R' and PROVINCES[p]['region'] in GAUL_REGIONS)
    gl = sum(1 for p, v in pc.items() if v == 'G' and PROVINCES[p]['region'] in GAUL_REGIONS)
    return gov, r, gl


def prov_margin(g, p, side):
    """How many more spaces `side` needs for control (<=0 means it has majority)."""
    v = PROVINCES[p]
    have = sum(1 for s in v['idx'] if g.ctrl[s] == side)
    return v['need'] - have


def im_delta(g, side, act):
    """Value of an influence action for `side` (higher is better)."""
    kind, s = act
    before = gov_and_provs(g)
    old = (g.ctrl[s], g.ctype[s])
    g.ctrl[s] = side; g.ctype[s] = 'IM'; g._pc_cache = None
    after = gov_and_provs(g)
    p = PROV[s]
    margin_after = prov_margin(g, p, side)
    g.ctrl[s], g.ctype[s] = old; g._pc_cache = None
    margin_before = prov_margin(g, p, side)
    if side == 'R':
        v = (after[0] - before[0]) * 10 + (after[1] - before[1]) * 4 - (after[2] - before[2]) * 4
    else:
        v = -(after[0] - before[0]) * 10 + (after[2] - before[2]) * 4 - (after[1] - before[1]) * 4
        if REGION[s] == 'Provincia':
            v += 1
    # progress toward majority in that province
    if margin_after >= 0:
        v += max(0, 3 - margin_after) * 0.6
    if kind == 'convert':
        v += 1.0   # also denies the enemy
    if side == 'R':
        pend = {g.units[x].prov for x in g.pool}
        if p in pend:
            # Roman IMs in every open Town keep the province's Tribe from arriving
            open_t = sum(1 for t in PROVINCES[p]['idx'] if STYPE[t] == 'town' and g.ctype[t] is None
                         and not any(u.loc == t and u.side == 'R' for u in g.units.values()))
            v += 1.2 + (2.5 if open_t <= 1 else 0)
    if REGION[s] in ('Germania', 'Britannia'):
        v -= 2
    # safety: Roman IMs far from support are isolated in winter
    if side == 'R':
        sup = any(g.ctrl[t] == 'R' for t, k in ADJ[s]) or any(u.loc == s and u.side == 'R' for u in g.units.values())
        v += 0.5 if sup else -0.5
    return v


def best_influence(g, side, opts):
    if not opts:
        return None
    return max(opts, key=lambda a: (im_delta(g, side, a), -a[1]))


def all_influence_options(g, side):
    opts = []
    for s in range(N):
        if g.can_place(side, s):
            opts.append(('place', s))
        elif g.can_convert(side, s):
            opts.append(('convert', s))
    return opts
