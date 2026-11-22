"""Event resolution for the 55 strategy cards (1st-edition texts, 2nd-edition rules)."""
from engine import (N, NAMES, IDX, ADJ, PROV, REGION, STYPE, PROVINCES, REG_PROVS, GAUL_REGIONS, PROVINCIA,
                    PORTS, OTHER, LEGATES, ROMAN_LEADERS, Leader, GERMAN_SH, GERMANIA_VP, PROV_ADJ, EDGE)


def influence_options(g, side, spaces, ignore_adj=False):
    opts = []
    for s in spaces:
        if g.can_place(side, s, ignore_adj=ignore_adj):
            opts.append(('place', s))
        elif g.can_convert(side, s):
            opts.append(('convert', s))
    return opts


def do_influence(g, side, act):
    if act is None:
        return
    kind, s = act
    if kind == 'place' and g.can_place(side, s, ignore_adj=True):
        g.place_im(side, s)
    elif kind == 'convert' and g.ctrl[s] == OTHER[side] and g.ctype[s] == 'IM':
        g.clear_ctrl(s); g.place_im(side, s)
    g.log(f'{side} influence {kind} {NAMES[s]}')


def prov_influence(g, side, provs, purpose):
    """One influence action in each listed province (policy picks the space)."""
    pol = g.pol[side]
    for p in provs:
        opts = influence_options(g, side, PROVINCES[p]['idx'])
        if opts:
            do_influence(g, side, pol.choose_influence(g, side, opts, purpose))


def gaul_provs():
    return [p for r in GAUL_REGIONS for p in REG_PROVS[r]]


def do_event(g, side, c):
    pol = g.pol[side]
    if c in (1, 2):   # Caesar (+ legate) activation, then AP
        cz = g.leaders.get('Caesar')
        if cz and isinstance(cz.loc, int):
            pol.activate_leader(g, side, cz, free=True)
        if c == 1:
            ls = [l for l in g.leaders.values() if l.name != 'Caesar' and isinstance(l.loc, int) and not l.moved]
            if ls:
                pol.activate_leader(g, side, pol.choose_leader(g, side, ls, 'legate'), free=True)
    elif c == 3:
        g.apply_replacements(2)
    elif c == 4:
        pol.spend_ap(g, side, 5)
    elif c == 5:
        stacks = [u for u in g.on_map('G') if REGION[u.loc] == 'Belgica' and not u.merc or (u.merc and u.ma and REGION[u.loc] == 'Belgica')]
        pol.mass_activation(g, side, stacks, 'belgic_confederation')
    elif c == 6:
        provs = [p for p in gaul_provs() if any(g.ctrl[s] == 'G' and g.ctype[s] == 'IM' for s in PROVINCES[p]['idx'])]
        prov_influence(g, side, provs, 'united_gaul')
    elif c == 7:
        provs = [p for p in REG_PROVS['Belgica'] if any(g.ctrl[s] == 'R' and g.ctype[s] == 'IM' for s in PROVINCES[p]['idx'])
                 or any(u.side == 'R' and PROV[u.loc] == p for u in g.on_map('R'))]
        prov_influence(g, side, provs, 'belgic_resentment')
    elif c == 8:
        provs = [p for p in gaul_provs() if not any(u.side == 'R' and PROV[u.loc] == p for u in g.on_map('R'))
                 and any(g.ctrl[s] == 'R' and g.ctype[s] == 'IM' for s in PROVINCES[p]['idx'])]
        if provs:
            p = pol.choose_province(g, side, provs, 'druidic')
            for s in PROVINCES[p]['idx']:
                if g.ctrl[s] == 'R' and g.ctype[s] == 'IM':
                    g.remove_im(s)
    elif c == 9:
        cz = g.leaders.get('Caesar')
        if cz and isinstance(cz.loc, int):
            for s in [cz.loc] + [t for t, k in ADJ[cz.loc]]:
                if g.ctrl[s] == 'G' and g.ctype[s] == 'IM' and not any(u.loc == s and u.side == 'G' for u in g.units.values()):
                    g.remove_im(s)
    elif c == 10:
        for _ in range(2):
            opts = [('place', s) for s in range(N) if g.can_place('R', s, ignore_adj=True)]
            if opts:
                do_influence(g, side, pol.choose_influence(g, side, opts, 'reach_of_rome'))
    elif c == 11:
        pol.mass_activation(g, side, None, 'glory_of_caesar')
    elif c == 12:
        reg = pol.choose_region(g, side, ['Celtica', 'Belgica'], 'roman_rule')
        provs = [p for p in REG_PROVS[reg] if any(g.ctrl[s] == 'R' and g.ctype[s] == 'IM' for s in PROVINCES[p]['idx'])]
        prov_influence(g, side, provs, 'roman_rule')
    elif c == 13:
        g.council_ims = min(6, g.council_ims + 2)
        red = [u for u in g.units.values() if u.kind == 'tribe' and u.steps == 1 and (isinstance(u.loc, int) or u.loc == 'submitted')]
        if red:
            u = pol.choose_unit(g, side, red, 'restore')
            u.steps = 2
    elif c == 14:
        provs = sorted({PROV[s] for s in range(N) if g.ctype[s] == 'FT'})
        prov_influence(g, side, provs, 'glory_liberty')
    elif c == 15:
        mt = next(u for u in g.units.values() if u.name == 'Minor Tribe')
        if mt.loc == 'hold':
            opts = [s for s in range(N) if REGION[s] in GAUL_REGIONS and g.ctrl[s] == 'G'
                    and not any(u.loc == s and u.side == 'R' for u in g.units.values())
                    and not any(l.loc == s for l in g.leaders.values())]
            if opts:
                mt.loc = pol.choose_space(g, side, opts, 'minor_tribe'); mt.moved = False
    elif c in (16, 53):
        pol.mass_activation(g, side, None, 'trumpets')
    elif c == 17:
        if 'Labienus' in g.legate_cup and any(True for _ in g.on_map('R', 'legion')):
            legs = [u.loc for u in g.on_map('R', 'legion')]
            s = pol.choose_space(g, side, sorted(set(legs)), 'labienus')
            g.legate_cup.remove('Labienus')
            b, cr, m = ROMAN_LEADERS['Labienus']
            g.leaders['Labienus'] = Leader('Labienus', 'R', b, cr, m, s)
            others = [l for l in g.leaders.values() if l.name not in ('Caesar', 'Labienus')]
            if others:
                ret = min(others, key=lambda l: l.br)
                g.legate_cup.append(ret.name); del g.leaders[ret.name]
        else:
            cz = g.leaders.get('Caesar')
            ls = [l for l in g.leaders.values() if l.name != 'Caesar' and isinstance(l.loc, int)
                  and not (cz and l.loc == cz.loc)]
            if ls:
                pol.activate_leader(g, side, pol.choose_leader(g, side, ls, 'lieutenant'), free=True)
    elif c == 18:
        pc = g.prov_control()
        opts = [s for s in range(N) if g.ctrl[s] == 'G' and g.ctype[s] == 'IM' and pc[PROV[s]] == 'R'
                and not any(u.loc == s and u.side == 'G' for u in g.units.values())]
        if opts:
            g.remove_im(pol.choose_space(g, side, opts, 'remove_enemy_im'))
    elif c == 19:
        pc = g.prov_control()
        rprov = [p for p, v in pc.items() if v == 'R']
        adjp = set()
        for p in rprov:
            adjp |= PROV_ADJ[p]
        opts = [s for s in range(N) if g.ctrl[s] == 'G' and g.ctype[s] == 'IM' and PROV[s] in adjp
                and not any(u.loc == s and u.side == 'G' for u in g.units.values())]
        if opts:
            g.remove_im(pol.choose_space(g, side, opts, 'remove_enemy_im'))
    elif c == 20:
        rome = g.path_to_rome()
        red = [u for u in g.on_map('R', 'legion') if u.steps == 1 and u.loc in rome and not g.unit_besieged(u)]
        if red:
            pol.choose_unit(g, side, red, 'restore').steps = 2
    elif c == 21:
        if g.pool:
            g.rng.shuffle(g.pool)
            u = g.units[g.pool.pop()]
            g.place_reinforcement(u, allow_council=True)
    elif c == 22:
        gs = {u.loc for u in g.on_map('G')}
        cand = set()
        for s in gs:
            cand.add(s)
            for t, k in ADJ[s]:
                cand.add(t)
        opts = [s for s in cand if not any(u.loc == s and u.side == 'R' for u in g.units.values())
                and g.ctype[s] not in ('WC', 'FT', 'SH') and REGION[s] not in ('Germania', 'Britannia')]
        if opts:
            s = pol.choose_space(g, side, opts, 'devastate')
            if s is not None:
                g.devast.add(s)
                if g.ctype[s] == 'IM':
                    g.remove_im(s)
    elif c == 23:
        near = set()
        for s in range(N):
            if g.ctrl[s] == 'G' and g.ctype[s] == 'SH':
                for t, k in ADJ[s]:
                    near.add(t)
        rem = [s for s in near if g.ctrl[s] == 'R' and g.ctype[s] == 'IM']
        if rem:
            g.remove_im(pol.choose_space(g, side, rem, 'remove_enemy_im'))
        else:
            opts = influence_options(g, side, sorted(near))
            if opts:
                do_influence(g, side, pol.choose_influence(g, side, opts, 'long_hairs'))
    elif c in (25, 26):
        mercs = [u for u in g.units.values() if u.name.startswith('Mercenaries') and u.loc == 'hold']
        if mercs:
            sup = g.supplied_spaces('G')
            opts = set(u.loc for u in g.on_map('G') if (u.kind in ('tribe', 'gleader')) and u.loc in sup and not g.unit_besieged(u))
            opts |= set(s for s in range(N) if g.ctype[s] == 'FT' and s in sup and not g.is_besieged(s))
            if opts:
                mercs[0].loc = pol.choose_space(g, side, sorted(opts), 'mercenary'); mercs[0].moved = False
    elif c == 27:
        done = set()
        for _ in range(2):
            opts = [s for s in range(N) if REGION[s] == 'Provincia' and g.ctrl[s] == 'R' and g.ctype[s] == 'IM' and PROV[s] not in done]
            if not opts:
                break
            s = pol.choose_space(g, side, opts, 'remove_enemy_im')
            done.add(PROV[s]); g.remove_im(s)
    elif c == 28:
        opts = [s for s in range(N) if g.ctype[s] == 'FT' and s not in g.ft_up and not g.is_besieged(s)]
        if opts:
            g.ft_up.add(pol.choose_space(g, side, opts, 'upgrade_ft'))
    elif c in (29, 30):
        cav = [u for u in g.units.values() if u.name.startswith('Germani Cav') and u.loc == 'hold']
        if cav:
            ok = german_supply_legions(g)
            if ok:
                cav[0].loc = pol.choose_space(g, side, sorted(ok), 'cavalry'); cav[0].moved = False
    elif c == 31:
        rs = {u.loc for u in g.on_map('R')}
        opts = [s for s in range(N) if g.ctrl[s] == 'G' and g.ctype[s] == 'IM' and any(t in rs for t, k in ADJ[s])]
        if opts:
            s = pol.choose_space(g, side, opts, 'convert'); g.clear_ctrl(s); g.place_im('R', s)
    elif c == 32:
        pol.mass_activation(g, side, None, 'caesars_legions')
    elif c in (33, 46):
        fr = {u.loc for u in g.on_map(side) if not g.unit_besieged(u)}
        opts = [s for s in range(N) if g.ctrl[s] == OTHER[side] and g.ctype[s] == 'IM'
                and any(t in fr for t, k in ADJ[s]) and not any(u.loc == s and u.side == OTHER[side] for u in g.units.values())]
        if opts:
            g.remove_im(pol.choose_space(g, side, opts, 'remove_enemy_im'))
    elif c in (34, 35):
        german_migration(g, side)
    elif c == 36:
        provs = sorted({PROV[u.loc] for u in g.on_map('G') if REGION[u.loc] in GAUL_REGIONS + ('Provincia',)})
        prov_influence(g, side, provs, 'encourage')
    elif c in (37, 38):
        pol.mass_activation(g, side, None, 'motus_ubique')
    elif c == 39:
        fp = {PROV[s] for s in range(N) if g.ctrl[s] == side and g.ctype[s] == 'IM'}
        opts = [s for s in range(N) if g.ctrl[s] == OTHER[side] and g.ctype[s] == 'IM' and PROV[s] in fp
                and not any(u.loc == s and u.side == OTHER[side] for u in g.units.values())]
        if opts:
            g.remove_im(pol.choose_space(g, side, opts, 'remove_enemy_im'))
    elif c == 40:
        vac = {p for p, v in PROVINCES.items() if any(g.ctrl[s] is None for s in v['idx'])}
        opts = [s for s in range(N) if g.ctrl[s] == OTHER[side] and g.ctype[s] == 'IM' and PROV[s] in vac
                and not any(u.loc == s for u in g.units.values())]
        if opts:
            g.remove_im(pol.choose_space(g, side, opts, 'remove_enemy_im'))
    elif c == 41:
        mil = next(u for u in g.units.values() if u.name == 'Militia')
        if mil.loc == 'hold':
            opts = set(u.loc for u in g.on_map('G', 'tribe') if REGION[u.loc] in ('Celtica', 'Belgica') and not g.unit_besieged(u))
            opts |= set(s for s in range(N) if g.ctype[s] == 'FT' and REGION[s] in ('Celtica', 'Belgica') and not g.is_besieged(s))
            if opts:
                s = pol.choose_space(g, side, sorted(opts), 'militia')
                reg = REGION[s]
                pc = g.prov_control()
                mil.cs = (sum(1 for p in REG_PROVS[reg] if pc[p] == 'G'),)
                mil.loc = s; mil.moved = False
    elif c == 42:
        rh = g.hands['R']
        if rh:
            took = g.rng.choice(rh)
            rh.remove(took); g.hands['G'].append(took)
            rh.append(42)
            if g.hands['G']:
                g.card_play('G')
    elif c == 43:
        aed = next(u for u in g.units.values() if u.name == 'Aedui')
        if aed.loc == 'aedui_box':
            opts = [s for s in PROVINCES['Aedui']['idx'] if g.ctrl[s] != 'R' and g.ctype[s] is None or g.ctrl[s] == 'G' and g.ctype[s] == 'IM']
            opts = [s for s in opts if not any(u.loc == s and u.side == 'R' for u in g.units.values()) and g.ctrl[s] != 'R']
            if opts:
                g.place_tribe(aed, pol.choose_space(g, side, opts, 'aedui'))
    elif c == 44:
        ls = [l for l in g.leaders.values() if l.name != 'Caesar' and isinstance(l.loc, int)]
        if ls and g.legate_cup:
            l = pol.choose_leader(g, side, ls, 'recall')
            g.rng.shuffle(g.legate_cup)
            nm = g.legate_cup.pop()
            b, cr, m = ROMAN_LEADERS[nm]
            g.leaders[nm] = Leader(nm, 'R', b, cr, m, l.loc)
            del g.leaders[l.name]; g.legate_cup.append(l.name)
    elif c == 45:
        opts = [s for s in range(N) if g.ctrl[s] == OTHER[side] and g.ctype[s] == 'IM' and REGION[s] in GAUL_REGIONS + ('Provincia',)
                and not any(u.loc == s and u.side == OTHER[side] for u in g.units.values())]
        if opts:
            s = pol.choose_space(g, side, opts, 'convert'); g.clear_ctrl(s); g.place_im(side, s)
    elif c == 47:
        pass  # only usable as the opening interrupt
    elif c == 48:
        opts = [s for s in range(N) if g.ctrl[s] == 'G' and g.ctype[s] == 'IM' and REGION[s] in GAUL_REGIONS + ('Provincia',)
                and not any(u.loc == s for u in g.units.values())]
        if opts:
            s = pol.choose_space(g, side, opts, 'convert'); g.clear_ctrl(s); g.place_im('R', s)
    elif c == 49:
        pol.mass_activation(g, side, None, 'three_days', ma=1)
    elif c == 50:
        opts = [s for s in range(N) if g.ctype[s] in ('FT', 'WC') and PORTS[s] and any(g.naval_supremacy(side, z) for z in PORTS[s])]
        opts = [s for s in opts if (g.fort_owner(s) != side and g.is_besieged(s)) or (g.fort_owner(s) == side and g.siege.get(s, 0) > 0)]
        if opts:
            siege_point_adjust(g, side, pol.choose_space(g, side, opts, 'siege_point'))
    elif c == 51:
        opts = [s for s in range(N) if g.ctype[s] in ('FT', 'WC') and g.is_besieged(s)]
        opts = [s for s in opts if g.fort_owner(s) != side or g.siege.get(s, 0) > 0]
        if opts:
            siege_point_adjust(g, side, pol.choose_space(g, side, opts, 'siege_point'))


def siege_point_adjust(g, side, s):
    if s is None:
        return
    if g.fort_owner(s) == side:
        g.siege[s] = max(0, g.siege.get(s, 0) - 1)
    else:
        g.siege[s] = g.siege.get(s, 0) + 1
        if g.siege[s] >= 3:
            g.fort_falls(side, s)


def german_supply_legions(g):
    """Spaces with a Legion that can trace a supply path to a German stronghold (via the entry arrows)."""
    from collections import deque
    starts = set()
    for sh, entries in GERMAN_SH.items():
        for e in entries:
            if g._passable(e, 'R'):
                starts.add(e)
    seen = set(starts)
    dq = deque(starts)
    while dq:
        s = dq.popleft()
        for t, k in ADJ[s]:
            if t not in seen and g._passable(t, 'R'):
                seen.add(t); dq.append(t)
    return {u.loc for u in g.on_map('R', 'legion') if u.loc in seen}


def german_migration(g, side):
    u = g.german_tribe()
    pol = g.pol[side]
    if u.loc == 'hold':
        sh = pol.choose_german_start(g, side, list(GERMAN_SH.keys()))
        if sh is None:
            return
        cur = None
        frontier = GERMAN_SH[sh]
        mp = 3
    else:
        cur = u.loc
        frontier = None
        mp = 3
    # choose a destination reachable within 3 MP avoiding CUs/FT/WC
    from collections import deque

    def ok(s):
        return (not any(x.loc == s and x.side in ('R', 'G') for x in g.units.values())
                and g.ctype[s] not in ('FT', 'WC') and REGION[s] not in ('Germania', 'Britannia'))
    dist = {}
    dq = deque()
    if cur is None:
        for e in frontier:
            if ok(e):
                dist[e] = 1; dq.append(e)
    else:
        dist[cur] = 0; dq.append(cur)
    while dq:
        s = dq.popleft()
        for t, k in ADJ[s]:
            c = dist[s] + (1 if k == 'path' else 2)
            if c <= mp and ok(t) and (t not in dist or dist[t] > c):
                dist[t] = c; dq.append(t)
    if not dist:
        return
    dest = pol.choose_german_dest(g, side, sorted(dist))
    if dest is None:
        return
    u.loc = dest
    if g.ctype[dest] == 'IM':
        g.remove_im(dest)
    g.log(f'German tribe to {NAMES[dest]}')
