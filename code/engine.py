"""Caesar: Rome vs Gaul (GMT, 2nd edition rules) -- simulation engine.

Written for bot development: it executes the published rules and asks a
Policy object for every decision.  Simplifications are listed in
ENGINE_NOTES.md.  Pure standard library.
"""
import json, os, random
from collections import deque
from cards import CARDS, ap_value

HERE = os.path.dirname(os.path.abspath(__file__))
_M = json.load(open(os.path.join(HERE, 'map.json')))

# ---------------------------------------------------------------- map data
_sp = sorted(_M['spaces'].values(), key=lambda s: s['id'])
NAMES = [s['name'] for s in _sp]
IDX = {n: i for i, n in enumerate(NAMES)}
N = len(NAMES)
STYPE = [s['type'] for s in _sp]                 # town / stronghold / walled / vp
PROV = [s['province'] for s in _sp]
REGION = [s['region'] for s in _sp]
SECTION = [s.get('section') for s in _sp]
PORTS = [tuple(s.get('ports', [])) for s in _sp]
WC_GARRISON = {IDX[s['name']]: (s['garrison_roman'], s['garrison_gallic']) for s in _sp if s['type'] == 'walled'}
ADJ = [[] for _ in range(N)]                     # (neighbour, kind)
for a, b, k in _M['edges']:
    ADJ[IDX[a]].append((IDX[b], k)); ADJ[IDX[b]].append((IDX[a], k))
EDGE = {}
for i in range(N):
    for j, k in ADJ[i]:
        EDGE[(i, j)] = k
PROVINCES = {p: dict(v, idx=[IDX[s] for s in v['spaces']]) for p, v in _M['provinces'].items()}
GAUL_REGIONS = ('Celtica', 'Belgica', 'Aquitania')
PROVINCIA = ('Volcae', 'Allobroges', 'Narbonensis')
REG_PROVS = {}
for p, v in PROVINCES.items():
    REG_PROVS.setdefault(v['region'], []).append(p)
PROV_NUM = {v['num']: p for p, v in PROVINCES.items()}
BRIGANTIUM = IDX['Brigantium']
OCTODURUS = IDX['Octodurus']
GERMANIA_VP = [IDX['Germania A'], IDX['Germania B']]
BRITANNIA_VP = [IDX['Durovernon'], IDX['Dubris']]
GERMAN_SH = {'Usipetes': [IDX['Eburones']], 'Ubii': [IDX['Vangiones']], 'Suebi': [IDX['Nemetes'], IDX['Triboci']]}
GERMAN_ENTRY = sorted({s for v in GERMAN_SH.values() for s in v})
STRONGHOLD_SPACES = [i for i in range(N) if STYPE[i] == 'stronghold']
SEA = {z: [IDX[s] for s in v] for z, v in _M['sea_zones'].items()}
VENETI_SPACE = IDX['Veneti']
GERGOVIA = IDX['Gergovia']
# province adjacency (some space of P adjacent to some space of Q)
PROV_ADJ = {p: set() for p in PROVINCES}
for (i, j), k in EDGE.items():
    if PROV[i] != PROV[j]:
        PROV_ADJ[PROV[i]].add(PROV[j])

HOPS = []
for _i in range(N):
    _d = [99] * N; _d[_i] = 0; _q = deque([_i])
    while _q:
        _s = _q.popleft()
        for _t, _k in ADJ[_s]:
            if _d[_t] == 99:
                _d[_t] = _d[_s] + 1; _q.append(_t)
    HOPS.append(_d)

BATTLE_COLS = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 6), (7, 8), (9, 10), (11, 12), (13, 15), (16, 18), (19, 22), (23, 27), (28, 999)]
_BT = """
0 0 0 0 0 0 0 1 1* 1** 2 2* 2**
0 0 0 0 0* 0** 1 1* 1** 2 2* 2** 3
0 0 0 0* 0** 1 1* 1** 2 2* 2** 3 3*
0 0 0* 0** 1 1* 1** 2 2* 2** 3 3* 3**
0 0* 0** 1 1* 1** 2 2* 2** 3 3* 3** 4
0* 0** 1 1* 1** 2 2* 2** 3 3* 3** 4 4*
0** 1 1* 1** 2 2* 2** 3 3* 3** 4 4* 4**
1 1* 1** 2 2* 2** 3 3* 3** 4 4* 4** 5
1* 1** 2 2* 2** 3 3* 3** 4 4* 4** 5 5*
1* 2 2* 2** 3 3* 3** 4 4* 4** 5 5* 5**
1** 2* 2** 3 3* 3** 4 4* 4** 5 5* 5** 6
"""
BATTLE_TABLE = {}
for r, line in zip(range(2, 13), _BT.strip().splitlines()):
    BATTLE_TABLE[r] = [(int(t.rstrip('*')), t.count('*')) for t in line.split()]


def battle_result(strength, roll):
    if strength <= 0:
        return (0, -1)
    for ci, (lo, hi) in enumerate(BATTLE_COLS):
        if lo <= strength <= hi:
            return BATTLE_TABLE[roll][ci]
    return BATTLE_TABLE[roll][-1]

# Siege table (1st-edition PAC).  Entry = (attacker step loss, siege points) or 'S'.
_ST = {  # roll: [1-2, 1-1, 1.5-1, 2-1]
    2: [(1, 0), (1, 0), (1, 0), (0, 0)], 3: [(1, 0), (1, 0), (0, 0), (0, 0)],
    4: [(1, 0), (0, 0), (0, 0), (1, 1)], 5: [(0, 0), (0, 0), (1, 1), (0, 1)],
    6: [(0, 0), (1, 1), (0, 1), (0, 1)], 7: [(1, 1), (0, 1), (0, 1), (1, 2)],
    8: [(0, 1), (0, 1), (1, 2), (0, 2)], 9: [(0, 1), (1, 2), (0, 2), (0, 2)],
    10: [(1, 2), (0, 2), (0, 2), (1, 3)], 11: [(0, 2), (0, 2), (1, 3), 'S'],
    12: [(0, 2), (1, 3), 'S', 'S'],
}


def siege_result(col, roll):
    roll = max(2, min(12, roll))
    return _ST[roll][col]


def odds_col(att, dfn):
    """Siege column: -1 none (<1:2), 0 '1-2', 1 '1-1', 2 '1.5-1', 3 '2-1', 4 submit (3-1)."""
    if dfn <= 0:
        return 4
    r = att / dfn
    if r >= 3: return 4
    if r >= 2: return 3
    if r >= 1.5: return 2
    if r >= 1: return 1
    if r >= 0.5: return 0
    return -1

OTHER = {'R': 'G', 'G': 'R'}

ROMAN_LEADERS = {  # name: (battle rating, command, MA)
    'Caesar': (3, 6, 5), 'Labienus': (2, 4, 4), 'P. Crassus': (1, 2, 4), 'Cicero': (1, 4, 3),
    'Galba': (1, 4, 3), 'Antonius': (2, 2, 4), 'D. Brutus': (1, 3, 3), 'Sabinus': (0, 4, 3)}
LEGATES = [k for k in ROMAN_LEADERS if k != 'Caesar']
TRIBES = {  # name: (province, full CS, reduced CS, region tag)
    'Aedui': ('Aedui', 6, 3), 'Aquitani': ('Aquitania', 4, 2), 'Armorici': ('Armorici', 4, 2),
    'Atrebates': ('Atrebates', 5, 3), 'Aulerci': ('Aulerci', 5, 3), 'Arverni': ('Arverni', 7, 4),
    'Bellovaci': ('Bellovaci', 6, 4), 'Bituriges': ('Bituriges', 5, 3), 'Cadurci': ('Cadurci', 5, 3),
    'Carnutes': ('Carnutes', 4, 2), 'Eburones': ('Eburones', 4, 2), 'Leuci': ('Leuci', 4, 2),
    'Lingones': ('Senones/Lingones', 4, 2), 'Nervii': ('Nervii', 5, 3), 'Parisii': ('Parisii', 4, 2),
    'Pictones': ('Pictones/Santones', 4, 2), 'Remi': ('Remi', 5, 3), 'Santones': ('Pictones/Santones', 4, 2),
    'Senones': ('Senones/Lingones', 5, 3), 'Sequani': ('Sequani', 5, 3), 'Suessiones': ('Suessiones', 4, 2),
    'Treveri': ('Treveri', 5, 3), 'Veneti': ('Veneti', 5, 3)}
SECTION_TRIBE = {'Pictones': 'Pictones', 'Santones': 'Santones', 'Senones': 'Senones', 'Lingones': 'Lingones'}


class Unit:
    __slots__ = ('uid', 'side', 'kind', 'name', 'cs', 'steps', 'maxsteps', 'ma', 'loc', 'inside',
                 'prov', 'region', 'elite', 'merc', 'moved', 'br', 'cr', 'is_leader')

    def __init__(self, uid, side, kind, name, cs, steps, ma, loc, prov=None, region=None, elite=False,
                 merc=False, br=None, cr=2, is_leader=False):
        self.uid = uid; self.side = side; self.kind = kind; self.name = name
        self.cs = cs                  # tuple (reduced CS, full CS) indexed by steps-1
        self.steps = steps; self.maxsteps = steps; self.ma = ma; self.loc = loc; self.inside = False
        self.prov = prov; self.region = region; self.elite = elite; self.merc = merc; self.moved = False
        self.br = br; self.cr = cr; self.is_leader = is_leader

    def strength(self):
        if self.steps <= 0:
            return 0
        return self.cs[self.steps - 1]

    def full(self):
        return self.steps == self.maxsteps

    def __repr__(self):
        return f'{self.name}[{self.steps}]@{self.loc}'


class Leader:
    __slots__ = ('name', 'side', 'br', 'cr', 'ma', 'loc', 'moved')

    def __init__(self, name, side, br, cr, ma, loc):
        self.name = name; self.side = side; self.br = br; self.cr = cr; self.ma = ma; self.loc = loc; self.moved = False

    def __repr__(self):
        return f'{self.name}@{self.loc}'


class GameOver(Exception):
    pass


class Game:
    def __init__(self, policies, seed=0, edition=2, log=False, options=None):
        self.rng = random.Random(seed)
        self.seed = seed
        self.edition = edition
        self.pol = policies            # {'R': policy, 'G': policy}
        self.opt = dict(siege_shift=-1 if edition == 2 else 0, siege_mp=2 if edition == 2 else 3,
                        sh_points=3 if edition == 2 else 2, ia_friendly=1 if edition == 2 else 2)
        if options:
            self.opt.update(options)
        self.logging = log
        self.logs = []
        self.turn = 1
        self.ctrl = [None] * N          # 'R'/'G'/None
        self.ctype = [None] * N         # 'IM','WC','FT','SH'
        self.ft_tribe = {}              # space -> tribe uid
        self.ft_up = set()
        self.siege = {}                 # space -> points
        self.sieged_this_card = set()
        self.devast = set()
        self.units = {}
        self.leaders = {}
        self.legate_cup = list(LEGATES)
        self.kept_legate = None
        self.council_tribes = []
        self.council_ims = 0
        self.pool = []
        self.submitted = []
        self.elim_tribes = []           # tribe/leader names
        self.elim_legions = []
        self.vp = 0
        self.vp_log = []
        self.caesars_pass = False
        self.germania_done = False
        self.britannia_done = False
        self.caesar_delay_used = False
        self.caesar_delayed = False
        self.deck = []
        self.discard = []
        self.hands = {'R': [], 'G': []}
        self.active = None
        self.winner = None
        self.win_reason = None
        self.stats = dict(battles=0, sieges=0, events={'R': 0, 'G': 0}, plays={'R': 0, 'G': 0},
                          submits=0, tribes_elim=0, legion_steps_lost=0, intercepts=0, avoids=0)
        self._pc_cache = None
        self.uid_counter = 0
        self.turn_plays = {'R': 0, 'G': 0}
        self.setup()

    # ------------------------------------------------------------ logging
    def log(self, msg):
        if self.logging:
            self.logs.append(f'T{self.turn} {msg}')

    def d6(self):
        return self.rng.randint(1, 6)

    # ------------------------------------------------------------ setup
    def new_unit(self, *a, **k):
        self.uid_counter += 1
        u = Unit(self.uid_counter, *a, **k)
        self.units[u.uid] = u
        return u

    def setup(self):
        R = 'R'; G = 'G'
        aedui_towns = PROVINCES['Aedui']['idx']
        for s in aedui_towns + PROVINCES['Sequani']['idx']:
            self.set_ctrl(s, 'R', 'IM')
        for p in PROVINCIA:
            for s in PROVINCES[p]['idx']:
                if STYPE[s] == 'town':
                    self.set_ctrl(s, 'R', 'IM')
                elif STYPE[s] == 'walled':
                    self.set_ctrl(s, 'R', 'WC')
        self.set_ctrl(IDX['Burdigala'], 'R', 'IM')
        self.set_ctrl(IDX['Bibrax'], 'R', 'IM')
        for s in STRONGHOLD_SPACES:
            self.set_ctrl(s, 'G', 'SH')
        for s in GERMANIA_VP + BRITANNIA_VP:
            self.set_ctrl(s, 'G', 'IM')
        # Roman army
        bib = IDX['Bibracte']
        for name in ['VII', 'VIII', 'IX', 'XI', 'XII']:
            self.new_unit(R, 'legion', name, (1, 2), 2, 3, bib, br=1)
        self.new_unit(R, 'legion', 'X', (1, 2), 2, 3, bib, elite=True, br=1)
        vie = IDX['Vienne']
        for name in ['XIII', 'XIV']:
            self.new_unit(R, 'legion', name, (1, 2), 2, 3, vie, br=1)
        for name in ['V', 'VI']:
            self.new_unit(R, 'legion', name, (1, 2), 2, 3, 'turn5', br=1)
        self.leaders['Caesar'] = Leader('Caesar', R, 3, 6, 5, bib)
        self.rng.shuffle(self.legate_cup)
        l1 = self.legate_cup.pop(); l2 = self.legate_cup.pop()
        b, c, m = ROMAN_LEADERS[l1]; self.leaders[l1] = Leader(l1, R, b, c, m, bib)
        b, c, m = ROMAN_LEADERS[l2]; self.leaders[l2] = Leader(l2, R, b, c, m, vie)
        # Gauls
        for t, (prov, f, r) in TRIBES.items():
            reg = PROVINCES[prov]['region']
            tag = 'Belgic' if reg == 'Belgica' else ('Celtic' if reg == 'Celtica' else 'Aquitani')
            u = self.new_unit(G, 'tribe', t, (r, f), 2, 3, 'pool', prov=prov, region=tag, elite=(t == 'Nervii'), br=1)
            if t == 'Aedui':
                u.loc = 'aedui_box'
            elif t == 'Sequani':
                u.loc = 'submitted'; u.steps = 1; self.submitted.append(u.uid)
            elif t == 'Arverni':
                u.loc = 'council'; self.council_tribes.append(u.uid)
            else:
                self.pool.append(u.uid)
        self.new_unit(G, 'gleader', 'Ambiorix', (1,), 1, 4, 'turn4', region='Belgic', br=1, cr=3, is_leader=True)
        self.new_unit(G, 'gleader', 'Vercingetorix', (1,), 1, 4, 'turn5', region='Celtic', br=1, cr=4, is_leader=True)
        # mercenaries (holding boxes)
        self.new_unit(G, 'merc', 'Minor Tribe', (2,), 1, 3, 'hold', merc=True, br=1)
        self.new_unit(G, 'merc', 'Militia', (0,), 1, 0, 'hold', merc=True, br=0)
        self.new_unit(G, 'merc', 'Mercenaries 1', (2,), 1, 0, 'hold', merc=True, br=0, cr=0)
        self.new_unit(G, 'merc', 'Mercenaries 2', (2,), 1, 0, 'hold', merc=True, br=0, cr=0)
        self.new_unit(R, 'merc', 'Germani Cav 1', (2,), 1, 0, 'hold', merc=True, br=0, cr=0)
        self.new_unit(R, 'merc', 'Germani Cav 2', (2,), 1, 0, 'hold', merc=True, br=0, cr=0)
        self.new_unit('X', 'german', 'Germani', (5, 8), 2, 3, 'hold', br=0)
        self.deck = list(CARDS.keys())
        self.rng.shuffle(self.deck)

    # ------------------------------------------------------------ queries
    def set_ctrl(self, s, side, kind, tribe=None):
        self.ctrl[s] = side; self.ctype[s] = kind
        if kind == 'FT':
            self.ft_tribe[s] = tribe
        self._pc_cache = None

    def clear_ctrl(self, s):
        if self.ctype[s] in ('FT', 'WC'):
            if self.ctype[s] == 'FT':
                self.ft_tribe.pop(s, None); self.ft_up.discard(s)
            # units that sheltered inside are now in the open (11.2.4)
            for u in self.units.values():
                if u.loc == s and u.inside:
                    u.inside = False
        self.ctrl[s] = None; self.ctype[s] = None
        self.siege.pop(s, None)
        self._pc_cache = None

    def on_map(self, side=None, kind=None):
        for u in self.units.values():
            if isinstance(u.loc, int) and (side is None or u.side == side) and (kind is None or u.kind == kind):
                yield u

    def cus_at(self, s, side=None):
        return [u for u in self.units.values() if u.loc == s and (side is None or u.side == side)]

    def leaders_at(self, s, side='R'):
        if side == 'R':
            return [l for l in self.leaders.values() if l.loc == s]
        return [u for u in self.units.values() if u.loc == s and u.is_leader]

    def outside(self, s, side):
        return [u for u in self.units.values() if u.loc == s and u.side == side and not u.inside]

    def fort_owner(self, s):
        if self.ctype[s] == 'FT':
            return 'G'
        if self.ctype[s] == 'WC':
            return self.ctrl[s]
        return None

    def is_besieged(self, s):
        o = self.fort_owner(s)
        if o is None:
            return False
        return any(u.loc == s and not u.inside and u.side == OTHER[o] for u in self.units.values())

    def unit_besieged(self, u):
        return u.inside and self.is_besieged(u.loc)

    def prov_control(self):
        if self._pc_cache is not None:
            return self._pc_cache
        res = {}
        for p, v in PROVINCES.items():
            rc = gc = 0; wc_r = wc_g = True; ft = False
            for s in v['idx']:
                c = self.ctrl[s]
                if c == 'R': rc += 1
                elif c == 'G': gc += 1
                if self.ctype[s] == 'WC':
                    if c != 'R': wc_r = False
                    if c != 'G': wc_g = False
                if self.ctype[s] == 'FT':
                    ft = True
            need = v['need']
            if rc >= need and wc_r and not ft:
                res[p] = 'R'
            elif gc >= need and wc_g:
                res[p] = 'G'
            else:
                res[p] = None
        self._pc_cache = res
        return res

    def controls_prov(self, side, p):
        return self.prov_control()[p] == side

    def local_support(self, side, s):
        if REGION[s] in ('Germania', 'Britannia'):
            return 0
        return 2 if self.prov_control()[PROV[s]] == side else 0

    def naval_supremacy(self, side, zone):
        if zone == 'Sinus Gallicus':
            return side == 'R'
        r = sum(1 for s in SEA[zone] if self.ctrl[s] == 'R')
        g = sum(1 for s in SEA[zone] if self.ctrl[s] == 'G')
        rome = r > g
        return rome if side == 'R' else not rome

    def caesar(self):
        return self.leaders.get('Caesar')

    def german_tribe(self):
        for u in self.units.values():
            if u.kind == 'german':
                return u

    # ------------------------------------------------------------ supply
    def _passable(self, s, side):
        """For supply / isolation paths."""
        if any(u.loc == s and u.side not in (side,) and not u.inside for u in self.units.values()):
            # unbesieged enemy CU present (outside) blocks; German tribe blocks both
            return False
        hostile = (self.ctrl[s] is not None and self.ctrl[s] != side) or s in self.devast
        if hostile:
            return any(u.loc == s and u.side == side for u in self.units.values())
        return True

    def supply_sources(self, side):
        pc = self.prov_control()
        src = set()
        if side == 'R':
            # WCs are sources; a Roman marker in a Roman province is a source only if it can trace
            # a path to (a space of) a different Roman-controlled province.
            for s in range(N):
                if self.ctrl[s] == 'R' and self.ctype[s] == 'WC' and not self.is_besieged(s):
                    src.add(s)
            cand = [s for s in range(N) if self.ctrl[s] == 'R' and pc[PROV[s]] == 'R' and self.ctype[s] != 'WC']
            comp = {}
            for s0 in cand:
                if s0 in comp:
                    continue
                seen = {s0}; dq = deque([s0])
                while dq:
                    x = dq.popleft()
                    for t, k in ADJ[x]:
                        if t not in seen and self._passable(t, 'R'):
                            seen.add(t); dq.append(t)
                provs = {PROV[x] for x in seen if self.ctrl[x] == 'R' and pc[PROV[x]] == 'R'}
                for x in seen:
                    if x in cand:
                        comp[x] = len(provs) >= 2
            src |= {s for s in cand if comp.get(s)}
            return src
        g = self.german_tribe()
        for s in range(N):
            if self.ctrl[s] != side:
                continue
            if side == 'R':
                if self.ctype[s] == 'WC' or pc[PROV[s]] == 'R':
                    src.add(s)
            else:
                if self.ctype[s] in ('SH', 'FT'):
                    if self.ctype[s] == 'SH' and g is not None and g.loc == s:
                        continue
                    if self.ctype[s] == 'FT' and self.is_besieged(s):
                        continue
                    src.add(s)
                elif pc[PROV[s]] == 'G' and REGION[s] in GAUL_REGIONS:
                    src.add(s)
        return src

    def supplied_spaces(self, side):
        src = self.supply_sources(side)
        seen = set(s for s in src)
        dq = deque(seen)
        while dq:
            s = dq.popleft()
            for t, k in ADJ[s]:
                if t not in seen and self._passable(t, side):
                    seen.add(t); dq.append(t)
        return seen

    def path_to_rome(self, side='R'):
        """Spaces that can trace a supply path to Rome (via the Alps at Brigantium or a Roman WC)."""
        targets = [BRIGANTIUM] + [s for s in range(N) if self.ctype[s] == 'WC' and self.ctrl[s] == 'R']
        seen = set(t for t in targets if self._passable(t, 'R'))
        dq = deque(seen)
        while dq:
            s = dq.popleft()
            for t, k in ADJ[s]:
                if t not in seen and self._passable(t, 'R'):
                    seen.add(t); dq.append(t)
        return seen

    def supply_phase(self, side):
        if self.opt.get('no_supply_' + side):
            return
        sup = self.supplied_spaces(side)
        stacks = {}
        for u in list(self.on_map(side)):
            if u.kind == 'german':
                continue
            if u.inside and self.is_besieged(u.loc):
                # a besieged location supplies the units inside
                continue
            if u.loc in sup:
                continue
            if u.merc:
                self.to_holding(u)
                continue
            stacks.setdefault(u.loc, []).append(u)
        for s, us in stacks.items():
            us = [u for u in us if u.loc == s]
            if sum(u.steps for u in us) >= 3:
                victim = self.pol[side].choose_losses(self, side, us, 1, reason='attrition')
                self.lose_steps(side, victim[:1], 1, s)
                self.log(f'attrition {NAMES[s]} {side}')

    # ------------------------------------------------------------ boxes
    def to_holding(self, u):
        u.loc = 'hold'; u.inside = False; u.steps = u.maxsteps

    def eliminate(self, u, cause=''):
        side = u.side
        if u.kind == 'legion':
            u.loc = 'elim'; u.steps = 0; u.inside = False
            self.elim_legions.append(u.uid)
        elif u.kind in ('tribe', 'gleader'):
            # remove its fortified town
            if u.kind == 'tribe':
                for s, t in list(self.ft_tribe.items()):
                    if t == u.uid:
                        self.clear_ctrl(s)
            u.loc = 'elim'; u.steps = 0; u.inside = False
            self.elim_tribes.append(u.name)
            self.stats['tribes_elim'] += 1
        elif u.kind == 'german':
            u.loc = 'hold'; u.steps = u.maxsteps
        else:
            self.to_holding(u)
        self.log(f'eliminated {u.name} {cause}')

    def submit_tribe(self, u):
        """Tribe loses a step and goes to the Submitted box (or is eliminated)."""
        for s, t in list(self.ft_tribe.items()):
            if t == u.uid:
                self.clear_ctrl(s)
        if u.kind == 'tribe':
            if u.steps <= 1:
                self.eliminate(u, 'submit')
            else:
                u.steps -= 1; u.loc = 'submitted'; u.inside = False
                self.submitted.append(u.uid)
            self.stats['submits'] += 1
        elif u.kind == 'gleader':
            self.eliminate(u, 'submit')
        elif u.merc:
            self.to_holding(u)

    def lose_steps(self, side, order, hits, space):
        """Apply hits in the given unit order (owner's choice). Returns steps actually lost."""
        lost = 0
        i = 0
        while hits > 0:
            # each entry of the owner's order takes one hit (a 2-step unit appears twice: full, then reduced)
            u = None
            while i < len(order):
                c = order[i]; i += 1
                if c.steps > 0 and c.loc == space:
                    u = c
                    break
            if u is None:
                cands = [x for x in order if x.steps > 0 and x.loc == space]
                if not cands:
                    break
                u = cands[0]
            u.steps -= 1; hits -= 1; lost += 1
            if u.kind == 'legion':
                self.stats['legion_steps_lost'] += 1
            if u.steps <= 0 or u.kind == 'gleader':
                self.eliminate(u, 'loss')
        self.check_displacement(space)
        return lost

    def check_displacement(self, s):
        if not isinstance(s, int):
            return
        if any(u.loc == s and u.side == 'R' for u in self.units.values()):
            return
        for l in [l for l in self.leaders.values() if l.loc == s]:
            self.displace(l)

    def displace(self, l):
        self.log(f'{l.name} displaced')
        if l.name == 'Caesar':
            ims = [s for s in range(N) if self.ctrl[s] == 'R' and self.ctype[s] == 'IM']
            for s in self.pol['R'].choose_ims_to_remove(self, ims, 3):
                self.clear_ctrl(s)
            opts = [u.loc for u in self.on_map('R', 'legion') if not self.unit_besieged(u)]
            opts += [s for s in range(N) if self.ctype[s] == 'WC' and self.ctrl[s] == 'R' and not self.is_besieged(s)]
            if opts:
                l.loc = self.pol['R'].choose_caesar_relocation(self, opts)
            else:
                l.loc = 'rome'
        else:
            l.loc = 'cup'
            del self.leaders[l.name]
            self.legate_cup.append(l.name)

    # ------------------------------------------------------------ influence
    def can_place(self, side, s, ignore_adj=False):
        if self.ctrl[s] is not None or s in self.devast:
            return False
        if STYPE[s] == 'walled':
            return False
        if any(u.loc == s and u.side == OTHER[side] for u in self.units.values()):
            return False
        g = self.german_tribe()
        if g and g.loc == s:
            return False
        reg = REGION[s]
        if reg in ('Germania', 'Britannia') and side == 'G':
            return False
        if ignore_adj:
            return True
        if side == 'R' and reg != 'Provincia':
            if any(u.loc == s and u.side == 'R' for u in self.units.values()):
                return True
            return any(self.ctrl[t] == 'R' and self.ctype[t] == 'IM' for t, k in ADJ[s])
        if side == 'G' and reg == 'Provincia':
            if any(u.loc == s and u.side == 'G' for u in self.units.values()):
                return True
            return any(self.ctrl[t] == 'G' for t, k in ADJ[s])
        return True

    def can_convert(self, side, s):
        return (self.ctrl[s] == OTHER[side] and self.ctype[s] == 'IM'
                and any(u.loc == s and u.side == side for u in self.units.values()))

    def place_im(self, side, s):
        self.set_ctrl(s, side, 'IM')
        self.after_im_change(s)

    def remove_im(self, s):
        if self.logging:
            self.log(f'IM removed: {NAMES[s]} ({self.ctrl[s]})')
        self.clear_ctrl(s)
        self.after_im_change(s)

    def after_im_change(self, s):
        # Germania / Britannia VP
        if not self.germania_done and all(self.ctrl[t] != 'G' for t in GERMANIA_VP):
            self.germania_done = True; self.add_vp(2, 'Germania')
        if not self.britannia_done and all(self.ctrl[t] != 'G' for t in BRITANNIA_VP):
            self.britannia_done = True; self.add_vp(2, 'Britannia')

    def add_vp(self, n, why):
        self.vp += n
        self.vp_log.append((self.turn, n, why))
        self.log(f'VP {n:+d} {why} -> {self.vp}')

    # ------------------------------------------------------------ dice helpers
    def roll2(self):
        return self.d6() + self.d6()

    # ------------------------------------------------------------ reaction rolls
    def ia_roll(self, side, leader_br, dest, rough, surprise_hook=None):
        drm = leader_br
        if self.ctrl[dest] == side or any(u.loc == dest and u.side == side for u in self.units.values()):
            drm += self.opt['ia_friendly']
        if rough:
            drm -= 2
        extra = 0
        if surprise_hook:
            extra = surprise_hook(drm)
        roll = self.roll2()
        return roll + drm + extra >= 9

    def army_br(self, side, s, units, leaders=None):
        """Commanding leader's battle rating for an army."""
        if side == 'R':
            ls = leaders if leaders is not None else self.leaders_at(s, 'R')
            if ls:
                return max(l.br for l in ls) if not any(l.name == 'Caesar' for l in ls) else 3
        else:
            gl = [u for u in units if u.is_leader]
            if gl:
                v = [u for u in gl if u.name == 'Vercingetorix']
                return (v or gl)[0].br
        best = 0
        for u in units:
            if u.br and u.full() and u.kind in ('legion', 'tribe') or (u.kind == 'merc' and u.name == 'Minor Tribe'):
                best = max(best, 1 if u.full() else 0)
        return best

    # ================================================================ movement
    def stack_cr(self, side, leader, units):
        if leader is None:
            return 2
        if isinstance(leader, Leader):
            return leader.cr
        return leader.cr

    def step_cost(self, a, b, ncu, cr):
        k = EDGE[(a, b)]
        c = 1 if k == 'path' else 2
        if ncu > cr:
            c += 1
        return c

    def can_enter(self, side, s, alone_roman_leader=False, german=False):
        if REGION[s] in ('Germania', 'Britannia') and side == 'G':
            return False
        if alone_roman_leader:
            g = self.german_tribe()
            if g and g.loc == s:
                return False
            if any(u.loc == s and u.side == 'G' and not u.inside for u in self.units.values()):
                return False
            if self.ctype[s] in ('FT', 'SH'):
                return False
        return True

    def activate(self, side, leader, units, plan, free=True, ma_override=None, forced_march=False):
        """Move an army.

        leader: Leader (Roman named), gleader Unit (Gallic named), or None (intrinsic, units[0] leads)
        units: list of CU objects that start with the leader (picked up at start)
        plan: list of ops ('to', s) / ('remove_im',) / ('siege',) / ('inside',)
        Returns dict(stopped=bool, battles=n).
        """
        if not units and leader is None:
            return dict(stopped=True)
        start = leader.loc if leader is not None else units[0].loc
        if not isinstance(start, int):
            return dict(stopped=True)
        units = [u for u in units if u.loc == start and not u.moved and not self.unit_besieged(u)]
        if leader is not None and isinstance(leader, Unit) and leader not in units:
            units = [leader] + units
        if leader is None and not units:
            return dict(stopped=True)
        # sub-leaders moving along (Roman legates with Caesar)
        subs = []
        if side == 'R' and isinstance(leader, Leader):
            subs = [l for l in self.leaders.values() if l.loc == start and l is not leader and not l.moved and leader.name == 'Caesar']
        alone = side == 'R' and isinstance(leader, Leader) and not units
        if ma_override is not None:
            ma = ma_override
        elif alone:
            ma = 7
        elif leader is not None:
            ma = leader.ma
        else:
            ma = min(u.ma for u in units) if units else 0
            if any(u.ma == 0 for u in units) and len(units) > 0:
                movers = [u for u in units if u.ma > 0]
                ma = min(u.ma for u in movers) if movers else 0
        if forced_march:
            ma += 1
        cr = leader.cr if leader is not None else 2
        if leader is None and units:
            # intrinsic leader: best unit leads; command rating 2
            cr = 2
        mp = ma
        cur = start
        prev = None
        res = dict(stopped=False, battles=0, path=[start])
        for u in units:
            u.moved = True; u.inside = False
        if isinstance(leader, Leader):
            leader.moved = True
        for l in subs:
            l.moved = True
        sieged_here = False
        for op in plan:
            if not units and not isinstance(leader, Leader):
                break
            ncu = len([u for u in units if not u.is_leader]) + len([u for u in units if u.is_leader and u is not leader])
            if op[0] == 'to':
                nxt = op[1]
                if (cur, nxt) not in EDGE:
                    break
                cost = self.step_cost(cur, nxt, ncu, cr)
                if cost > mp:
                    break
                if not self.can_enter(side, nxt, alone_roman_leader=alone):
                    break
                # channel crossing: storms at sea
                if EDGE[(cur, nxt)] == 'channel':
                    mp -= cost
                    if self.d6() == 6:
                        self.log('storm at sea')
                        continue
                    # fallthrough: entered
                else:
                    mp -= cost
                # interception by enemy before entering
                ok = self.intercept_check(side, leader, units, cur, nxt)
                if ok == 'backed_up':
                    res['stopped'] = True
                    break
                prev = cur
                cur = nxt
                for u in units:
                    u.loc = cur; u.inside = False
                if isinstance(leader, Leader):
                    leader.loc = cur
                for l in subs:
                    l.loc = cur
                res['path'].append(cur)
                # Germania / Britannia native attacks
                if REGION[cur] in ('Germania', 'Britannia') and side == 'R' and units:
                    if self.native_attack(cur, units, leader, prev):
                        res['stopped'] = True
                        break
                # enemy contact
                stop = self.contact(side, leader, units, subs, cur, prev, mp)
                units = [u for u in units if u.loc == cur]
                if isinstance(leader, Unit) and leader.loc != cur:
                    leader = None
                if stop == 'stop':
                    res['stopped'] = True
                    res['battles'] += 1
                    break
                elif stop == 'continue':
                    res['battles'] += 1
                if isinstance(leader, Leader) and leader.loc != cur:
                    res['stopped'] = True
                    break
                if not units and not alone:
                    res['stopped'] = True
                    break
            elif op[0] == 'remove_im':
                if mp >= 2 and self.ctrl[cur] == OTHER[side] and self.ctype[cur] == 'IM' and units:
                    mp -= 2
                    self.remove_im(cur)
            elif op[0] == 'siege':
                need = self.opt['siege_mp']
                if mp >= need and units and cur not in self.sieged_this_card:
                    if self.siege_roll(side, cur, leader, units, caesar=isinstance(leader, Leader) and leader.name == 'Caesar'):
                        mp -= need
            elif op[0] == 'inside':
                if self.fort_owner(cur) == side and not self.is_besieged(cur):
                    for u in units:
                        u.inside = True
                break
        if self.logging:
            ln = leader.name if leader is not None else 'stack'
            self.log(f'{side} move {ln}+{len(units)} {NAMES[start]}->{NAMES[cur]} ops={[o[0] for o in plan if o[0] != "to"]}')
        return res

    def native_attack(self, s, units, leader, prev):
        """Sugambri (CS 9) / Britanni (CS 7) attack check. Returns True if movement ends."""
        if any(u.loc == s and u.side == 'R' and u not in units for u in self.units.values()):
            return False
        if self.ctrl[s] == 'R':
            return False
        cs = sum(u.strength() for u in units)
        if self.roll2() < cs:
            return False
        tribe_cs = 9 if REGION[s] == 'Germania' else 7
        self.log(f'native attack at {NAMES[s]} vs CS {cs}')
        rerolls = (leader.br if isinstance(leader, Leader) else self.army_br('R', s, units))
        r_roll = self.roll_with_rerolls('R', cs, rerolls, tribe_cs)
        n_roll = self.roll2()
        rh, rs = battle_result(cs, r_roll)
        nh, ns = battle_result(tribe_cs, n_roll)
        win_r = (rh, rs) > (nh, ns)
        # natives never suffer losses; Roman loss reduction does not apply
        order = self.pol['R'].choose_losses(self, 'R', units, nh, reason='battle')
        self.lose_steps('R', order, nh, s)
        self.stats['battles'] += 1
        if not win_r:
            # Romans lose: retreat back where they came from
            survivors = [u for u in units if u.loc == s]
            for u in survivors:
                u.loc = prev
            if isinstance(leader, Leader) and leader.loc == s:
                leader.loc = prev
            for l in self.leaders.values():
                if l.loc == s:
                    l.loc = prev
        return True

    def roll_with_rerolls(self, side, strength, rerolls, opp_strength):
        """Simple self-only reroll for fixed-opponent combats."""
        a, b = self.d6(), self.d6()
        for _ in range(rerolls):
            lo = min(a, b)
            if (side == 'R' and lo <= 3) or (side != 'R' and lo <= 3):
                if a <= b: a = self.d6()
                else: b = self.d6()
        if side == 'R':
            a = max(a, 3); b = max(b, 3)
        return a + b

    # ------------------------------------------------------------ interception
    def intercept_check(self, side, leader, units, frm, to):
        enemy = OTHER[side]
        # eligibility of target space for the interceptor
        if self.ctrl[to] == side and not any(u.loc == to and u.side == enemy for u in self.units.values()):
            return None
        if any(u.loc == to and u.side == side and u not in units for u in self.units.values()):
            return None   # contains non-moving enemy (for interceptor) CUs
        candidates = {}
        for t, k in ADJ[to]:
            if k == 'channel':
                continue
            if t == to:
                continue
            us = [u for u in self.units.values() if u.loc == t and u.side == enemy and not self.unit_besieged(u)
                  and u.kind != 'german']
            if enemy == 'R':
                ls = [l for l in self.leaders.values() if l.loc == t]
            else:
                ls = [u for u in us if u.is_leader]
            if not us and not ls:
                continue
            # a stack that the mover just left by abandoning a siege can't intercept (ignored)
            candidates[t] = (us, ls, k)
        if not candidates:
            return None
        if REGION[to] in ('Germania', 'Britannia') and enemy == 'G':
            return None
        decisions = self.pol[enemy].intercept(self, enemy, to, frm, units, leader, candidates)
        if not decisions:
            return None
        for t, (us_taken, lead) in decisions.items():
            us0, ls0, k = candidates[t]
            br = (lead.br if lead is not None else self.army_br(enemy, t, us_taken, []))
            if enemy == 'G' and lead is None:
                gl = [u for u in us_taken if u.is_leader]
                br = gl[0].br if gl else self.army_br('G', t, us_taken)
            hook = lambda drm, e=enemy: self.surprise_ia(e, side, drm)
            self.stats['intercepts'] += 1
            if self.ia_roll(enemy, br, to, k == 'rough', hook):
                self.log(f'{enemy} intercepts into {NAMES[to]} from {NAMES[t]}')
                for u in us_taken:
                    u.loc = to; u.inside = False
                if isinstance(lead, Leader):
                    lead.loc = to
                if enemy == 'R':
                    for l in list(self.leaders.values()):
                        if l.loc == t and l is lead:
                            l.loc = to
                # mover may try to back up (avoid battle)
                if self.pol[side].back_up(self, side, units, leader, to, frm):
                    br2 = leader.br if leader is not None else self.army_br(side, frm, units)
                    if self.ia_roll(side, br2, frm, EDGE[(to, frm)] == 'rough'):
                        return 'backed_up'
                return 'intercepted'
        return None

    def surprise_ia(self, roller, other, drm):
        """Remedies for all Contingencies (#54): either player may modify by +/-2 before the roll."""
        extra = 0
        for side, sign in ((roller, +1), (other, -1)):
            if side not in ('R', 'G'):
                continue
            if 54 in self.hands[side] and self.pol[side].use_remedies(self, side, roller, drm):
                self.hands[side].remove(54); self.discard.append(54); self.card_left(side, 54); self.draw(side, 1)
                extra += 2 * sign
                break
        return extra

    # ------------------------------------------------------------ contact / battle
    def contact(self, side, leader, units, subs, s, prev, mp):
        """Mover has entered s. Resolve avoid battle / submission / battle.
        Returns None (no contact, keep moving), 'stop', or 'continue'."""
        enemy = OTHER[side]
        g = self.german_tribe()
        # German independent tribe in space
        if g and g.loc == s:
            return self.battle(side, units, leader, [g], None, s, prev, german=True)
        # defender declares inside/outside if it has a fort here
        defenders = [u for u in self.units.values() if u.loc == s and u.side == enemy]
        if not defenders:
            # a lone Roman leader is displaced when Gallic CUs enter his space (9.6),
            # unless he can shelter in a Roman Walled City there
            if side == 'G' and units and enemy == 'R' and not (self.ctype[s] == 'WC' and self.ctrl[s] == 'R'):
                for l in [l for l in self.leaders.values() if l.loc == s]:
                    self.displace(l)
            # fortification with no units: mover simply is there (siege possible later)
            return None
        if self.fort_owner(s) == enemy and not self.is_besieged_by_other(s, units):
            ins = self.pol[enemy].inside_outside(self, enemy, s, defenders, units)
            for u in defenders:
                u.inside = u in ins
        out = [u for u in defenders if not u.inside]
        if not out:
            return None
        # Submitting to Caesar (13.3): checked before any Avoid Battle attempt
        if side == 'R' and enemy == 'G':
            a_bs = sum(u.strength() for u in units if u.loc == s) + self.local_support('R', s)
            d_bs = sum(u.strength() for u in out) + self.local_support('G', s)
            if d_bs > 0 and a_bs >= 3 * d_bs:
                return self.battle(side, units, leader, out, None, s, prev)
        # avoid battle
        if self.pol[enemy].avoid(self, enemy, s, out, units, prev):
            dests = [t for t, k in ADJ[s] if t != prev and k != 'channel' and self.avoid_ok(enemy, t)]
            if dests:
                dest = self.pol[enemy].avoid_dest(self, enemy, s, out, dests)
                if enemy == 'R':
                    lead_br = self.army_br('R', s, out)
                else:
                    gl = [u for u in out if u.is_leader]
                    lead_br = gl[0].br if gl else self.army_br('G', s, out)
                self.stats['avoids'] += 1
                hook = lambda drm: self.surprise_ia(enemy, side, drm)
                if self.ia_roll(enemy, lead_br, dest, EDGE[(s, dest)] == 'rough', hook):
                    self.log(f'{enemy} avoids battle {NAMES[s]}->{NAMES[dest]}')
                    for u in out:
                        u.loc = dest; u.inside = False
                    if enemy == 'R':
                        for l in list(self.leaders.values()):
                            if l.loc == s and not any(u.loc == s and u.side == 'R' for u in self.units.values()):
                                l.loc = dest
                    return None
        out = [u for u in self.units.values() if u.loc == s and u.side == enemy and not u.inside]
        if not out:
            return None
        dl = None
        if enemy == 'R':
            ls = self.leaders_at(s, 'R')
            dl = max(ls, key=lambda l: (l.name == 'Caesar', l.br)) if ls else None
        return self.battle(side, units, leader, out, dl, s, prev)

    def is_besieged_by_other(self, s, movers):
        o = self.fort_owner(s)
        return any(u.loc == s and not u.inside and u.side == OTHER[o] and u not in movers for u in self.units.values())

    def avoid_ok(self, side, t):
        if any(u.loc == t and u.side == OTHER[side] for u in self.units.values()):
            return False
        g = self.german_tribe()
        if g and g.loc == t:
            return False
        if REGION[t] in ('Germania', 'Britannia') and side == 'G':
            return False
        if self.ctrl[t] == OTHER[side] and not any(u.loc == t and u.side == side for u in self.units.values()):
            return False
        return True

    def battle(self, att, a_units, a_leader, d_units, d_leader, s, prev, german=False, sortie=False):
        """Returns 'stop' or 'continue'."""
        dfn = 'X' if german else OTHER[att]
        a_units = [u for u in a_units if u.loc == s]
        a_bs = sum(u.strength() for u in a_units) + self.local_support(att, s)
        d_bs = sum(u.strength() for u in d_units) + (0 if german else self.local_support(dfn, s))
        # Submitting to Caesar
        if att == 'R' and dfn == 'G' and d_bs > 0 and a_bs >= 3 * d_bs:
            self.log(f'Gauls at {NAMES[s]} submit to Caesar ({a_bs}:{d_bs})')
            for u in d_units:
                self.submit_tribe(u) if u.kind in ('tribe', 'gleader') else self.to_holding(u)
            return 'continue'
        self.stats['battles'] += 1
        # rerolls
        if att == 'R':
            a_rr = a_leader.br if isinstance(a_leader, Leader) else self.army_br('R', s, a_units, [])
            d_rr = self.army_br('G', s, d_units) if not german else 0
        else:
            gl = [u for u in a_units if u.is_leader]
            a_rr = (a_leader.br if a_leader is not None else (gl[0].br if gl else self.army_br('G', s, a_units)))
            d_rr = (d_leader.br if d_leader is not None else self.army_br('R', s, d_units, [])) if not german else 0
        a_el = any(u.elite and u.full() for u in a_units)
        d_el = any(u.elite and u.full() for u in d_units)
        # Vow to Mars (+1 reroll)
        for sd in (att, dfn):
            if sd in ('R', 'G') and 52 in self.hands[sd] and self.pol[sd].use_vow_battle(self, sd, s, a_bs, d_bs, sd == att):
                self.hands[sd].remove(52); self.discard.append(52); self.card_left(sd, 52); self.draw(sd, 1)
                if sd == att: a_rr += 1
                else: d_rr += 1
        a_dice = [self.d6(), self.d6()]
        d_dice = [self.d6(), self.d6()]
        a_dice, d_dice, a_el_loss, d_el_loss = self.reroll_exchange(att, dfn, a_bs, d_bs, a_dice, d_dice, a_rr, d_rr, a_el, d_el)
        def total(side, dice):
            if side == 'R':
                return sum(max(3, x) for x in dice)
            return sum(dice)
        ah, astar = battle_result(a_bs, total(att, a_dice))
        dh, dstar = battle_result(d_bs, total(dfn, d_dice))
        if (ah, astar) > (dh, dstar):
            winner = 'A'
        elif (dh, dstar) > (ah, astar):
            winner = 'D'
        else:
            winner = 'draw'
        a_steps = sum(u.steps for u in a_units)
        d_steps = sum(u.steps for u in d_units)
        # loss reduction for the winner
        if winner == 'A':
            excess = max(0, ah - d_steps)
            dh = max(0, dh - excess // 2)
        elif winner == 'D':
            excess = max(0, dh - a_steps)
            ah = max(0, ah - excess // 2)
        self.log(f'battle {NAMES[s]} {att}{a_bs} vs {dfn}{d_bs}: hits {ah}/{dh} -> {winner}')
        # elite extra losses
        if a_el_loss:
            el = [u for u in a_units if u.elite and u.steps > 0]
            if el: self.lose_steps(att, el, 1, s)
        if d_el_loss:
            el = [u for u in d_units if u.elite and u.steps > 0]
            if el and dfn != 'X': self.lose_steps(dfn, el, 1, s)
        # apply losses
        if dfn == 'X':
            g = d_units[0]
            g.steps -= ah
            if g.steps <= 0:
                self.eliminate(g)
        else:
            order = self.pol[dfn].choose_losses(self, dfn, [u for u in d_units if u.loc == s], ah, reason='battle')
            self.lose_steps(dfn, order, ah, s)
        order = self.pol[att].choose_losses(self, att, [u for u in a_units if u.loc == s], dh, reason='battle')
        self.lose_steps(att, order, dh, s)
        a_left = [u for u in a_units if u.loc == s]
        d_left = [u for u in d_units if u.loc == s and u.steps > 0]
        if winner == 'A':
            if d_left and dfn != 'X':
                self.retreat(dfn, d_left, s, prev, defender=True)
            if a_left and a_bs >= 2 * d_bs:
                return 'continue'
            return 'stop'
        else:
            if a_left:
                self.retreat(att, a_left, s, prev, defender=False)
            if winner == 'draw' and False:
                pass
            return 'stop'

    def reroll_exchange(self, att, dfn, a_bs, d_bs, a_dice, d_dice, a_rr, d_rr, a_el, d_el):
        """Alternating rerolls, attacker first. Each side uses a shared greedy rule from its policy."""
        a_left, d_left = a_rr, d_rr
        a_el_avail, d_el_avail = a_el, d_el
        a_el_loss = d_el_loss = False
        turn = 'A'
        passes = 0
        guard = 0
        while guard < 30:
            guard += 1
            if turn == 'A':
                side, mine, theirs, left = att, a_dice, d_dice, a_left
                el_av = a_el_avail and a_left == 0
            else:
                side, mine, theirs, left = dfn, d_dice, a_dice, d_left
                el_av = d_el_avail and d_left == 0
            if left <= 0 and not el_av:
                passes += 1
                if passes >= 2:
                    break
                turn = 'D' if turn == 'A' else 'A'
                continue
            passes = 0
            if side == 'X':
                choice = None
            else:
                choice = self.pol[side].reroll_choice(self, side, (a_bs if turn == 'A' else d_bs), (d_bs if turn == 'A' else a_bs),
                                                      mine, theirs, side_is_attacker=(turn == 'A'), opp_side=(dfn if turn == 'A' else att))
            if choice is None:
                # pass uses one reroll
                if left > 0:
                    if turn == 'A': a_left -= 1
                    else: d_left -= 1
                else:
                    if turn == 'A': a_el_avail = False
                    else: d_el_avail = False
            else:
                which, idx = choice
                new = self.d6()
                if which == 'own':
                    mine[idx] = new
                else:
                    theirs[idx] = new
                if left > 0:
                    if turn == 'A': a_left -= 1
                    else: d_left -= 1
                else:
                    if turn == 'A':
                        a_el_avail = False
                        if new in (1, 6): a_el_loss = True
                    else:
                        d_el_avail = False
                        if new in (1, 6): d_el_loss = True
            turn = 'D' if turn == 'A' else 'A'
            if a_left <= 0 and d_left <= 0 and not a_el_avail and not d_el_avail:
                break
        return a_dice, d_dice, a_el_loss, d_el_loss

    def retreat(self, side, units, s, prev, defender=True):
        units = [u for u in units if u.loc == s]
        if not units:
            return
        # retreat into friendly fortification in the space
        if defender and self.fort_owner(s) == side:
            if self.pol[side].retreat_inside(self, side, s, units):
                for u in units:
                    u.inside = True
                self.move_leaders_with(side, s, s)
                return
        if not defender:
            dests = [prev]
        else:
            dests = [t for t, k in ADJ[s] if t != prev and not (REGION[t] in ('Germania', 'Britannia') and side == 'G')]
            g = self.german_tribe()
            dests = [t for t in dests if not (g and g.loc == t)]
        if not dests:
            for u in units:
                self.eliminate(u, 'no retreat')
            self.check_displacement(s)
            return
        dest = dests[0] if len(dests) == 1 else self.pol[side].choose_retreat(self, side, units, s, dests)
        # penalties
        pen = 0
        if self.ctrl[dest] == OTHER[side] and not any(u.loc == dest and u.side == side for u in self.units.values()):
            pen += 1
        if EDGE.get((s, dest)) == 'channel':
            pen += 1
        enemy_steps = sum(u.steps for u in self.units.values() if u.loc == dest and u.side == OTHER[side])
        pen += enemy_steps
        if pen:
            order = self.pol[side].choose_losses(self, side, units, pen, reason='retreat')
            self.lose_steps(side, order, pen, s)
        for u in units:
            if u.loc == s:
                u.loc = dest; u.inside = False
        self.move_leaders_with(side, s, dest)
        if enemy_steps and any(u.loc == dest and u.side == side for u in self.units.values()):
            # enemy CUs there must retreat (simplified: they retreat to their best adjacent space)
            them = [u for u in self.units.values() if u.loc == dest and u.side == OTHER[side]]
            self.retreat(OTHER[side], them, dest, s, defender=True)

    def move_leaders_with(self, side, s, dest):
        if side == 'R':
            for l in list(self.leaders.values()):
                if l.loc == s:
                    if any(u.loc == dest and u.side == 'R' for u in self.units.values()) or dest == s:
                        l.loc = dest
                    else:
                        self.displace(l)
        self.check_displacement(s)

    # ------------------------------------------------------------ sieges
    def fort_defense(self, s):
        owner = self.fort_owner(s)
        inside = [u for u in self.units.values() if u.loc == s and u.side == owner and u.inside]
        if self.ctype[s] == 'FT':
            gar = 3 if s in self.ft_up else 2
        else:
            gar = WC_GARRISON[s][0 if owner == 'R' else 1]
        return gar + sum(u.strength() for u in inside), inside

    def siege_drm(self, s, side, caesar):
        d = 0
        if caesar:
            d += 1
        if self.ctype[s] == 'FT':
            if s in self.ft_up:
                d -= 1
            if PORTS[s] and self.ft_tribe.get(s) and self.units[self.ft_tribe[s]].name == 'Veneti':
                if not self.naval_supremacy('R', 'Oceanus Atlanticus'):
                    d -= 2
        elif self.ctype[s] == 'WC' and self.ctrl[s] == 'R':
            d -= 1
        return d

    def siege_roll(self, side, s, leader, units, caesar=False):
        """One siege / subjugation attempt. Returns True if a roll (or submission) happened."""
        units = [u for u in self.units.values() if u.loc == s and u.side == side and not u.inside]
        att = sum(u.strength() for u in units)
        kind = self.ctype[s]
        if kind == 'SH' and side == 'R' and self.ctrl[s] == 'G':
            if att < 2:
                return False
            col = 2
            self.sieged_this_card.add(s)
            self.stats['sieges'] += 1
            for u in units:   # 14.3.2: every contributing CU counts as activated this card
                u.moved = True
            return self._siege_apply(side, s, col, caesar, units, subjugation=True)
        owner = self.fort_owner(s)
        if owner is None or owner == side:
            return False
        dfn, inside = self.fort_defense(s)
        col = odds_col(att, dfn)
        if col < 0:
            return False
        self.sieged_this_card.add(s)
        self.stats['sieges'] += 1
        for u in units:   # 14.3.2: every contributing CU counts as activated this card
            u.moved = True
        if col == 4:
            self.fort_surrender(side, s)
            return True
        return self._siege_apply(side, s, col, caesar, units)

    def _siege_apply(self, side, s, col, caesar, units, subjugation=False):
        drm = self.siege_drm(s, side, caesar) + self.opt['siege_shift']
        if side == 'R' and 52 in self.hands['R'] and self.pol['R'].use_vow_siege(self, s):
            self.hands['R'].remove(52); self.discard.append(52); self.card_left('R', 52); self.draw('R', 1); drm += 1
        roll = self.roll2() + drm
        res = siege_result(col, roll)
        if res == 'S':
            self.log(f'siege {NAMES[s]}: S')
            if subjugation:
                self.remove_stronghold(s)
            else:
                self.fort_surrender(side, s)
            return True
        loss, pts = res
        if loss:
            order = self.pol[side].choose_losses(self, side, units, loss, reason='siege')
            self.lose_steps(side, order, loss, s)
        if pts:
            self.siege[s] = self.siege.get(s, 0) + pts
        need = self.opt['sh_points'] if subjugation else 3
        self.log(f'siege {NAMES[s]} col{col} roll{roll}: loss {loss} pts {pts} -> {self.siege.get(s, 0)}')
        if self.siege.get(s, 0) >= need:
            if subjugation:
                self.remove_stronghold(s)
            else:
                self.fort_falls(side, s)
        return True

    def remove_stronghold(self, s):
        self.clear_ctrl(s)
        self.log(f'stronghold {NAMES[s]} subjugated')
        if s == OCTODURUS and not self.caesars_pass:
            self.caesars_pass = True
            self.add_vp(1, "Caesar's Pass")

    def fort_surrender(self, side, s):
        owner = self.fort_owner(s)
        inside = [u for u in self.units.values() if u.loc == s and u.side == owner and u.inside]
        if self.ctype[s] == 'FT':
            t = self.ft_tribe.get(s)
            for u in inside:
                self.submit_tribe(u) if u.kind in ('tribe', 'gleader') else self.to_holding(u)
            if t is not None and self.units[t].loc not in ('submitted', 'elim'):
                self.submit_tribe(self.units[t])
            if self.ctype[s] == 'FT':
                self.clear_ctrl(s)
        else:
            for u in inside:
                if owner == 'R':
                    self.eliminate(u, 'surrender')
                else:
                    self.submit_tribe(u) if u.kind in ('tribe', 'gleader') else self.to_holding(u)
            self.set_ctrl(s, side, 'WC')
            self.check_displacement(s)
        self.siege.pop(s, None)
        self.log(f'{NAMES[s]} surrenders to {side}')

    def fort_falls(self, side, s):
        owner = self.fort_owner(s)
        kind = self.ctype[s]
        t = self.ft_tribe.get(s)
        inside = [u for u in self.units.values() if u.loc == s and u.side == owner and u.inside]
        for u in inside:
            self.eliminate(u, 'siege')
        if kind == 'FT':
            if self.ctype[s] == 'FT':
                self.clear_ctrl(s)
            if t is not None and self.units[t].loc != 'elim':
                self.eliminate(self.units[t], 'fort fell')
        else:
            self.set_ctrl(s, side, 'WC')
        self.check_displacement(s)
        self.siege.pop(s, None)
        self.log(f'{NAMES[s]} falls to {side}')

    def lift_sieges(self):
        for s in list(self.siege):
            if self.ctype[s] == 'SH':
                if not any(u.loc == s and u.side == 'R' for u in self.units.values()):
                    self.siege.pop(s, None)
            elif not self.is_besieged(s):
                self.siege.pop(s, None)

    # ------------------------------------------------------------ cards
    def card_left(self, side, c):
        """Tell the owner's policy that card c has left its hand (spent, discarded or given away),
        before any replacement is drawn: a redrawn copy of the same card starts face down again."""
        f = getattr(self.pol.get(side) if isinstance(self.pol, dict) else None, 'card_left', None)
        if f:
            f(self, side, c)

    def draw(self, side, n):
        for _ in range(n):
            if not self.deck:
                if not self.discard:
                    return
                self.deck = self.discard; self.discard = []
                self.rng.shuffle(self.deck)
            self.hands[side].append(self.deck.pop())

    def deal(self):
        for side in ('R', 'G'):
            self.draw(side, 8)

    def ap(self, c):
        side = self.active or 'R'
        b = self.opt.get('ap_bonus_' + side, 0)
        k = self.opt.get('ap_first_' + side, 0)
        if k and self.turn_plays.get(side, 0) <= k:
            b = max(b, 1)
        return ap_value(c, self.opt.get('ap_edition') or self.edition) + b

    def event_allowed(self, side, c):
        info = CARDS[c]
        if info['side'] not in (side, 'W'):
            return False
        if info['kind'] in ('reaction', 'surprise'):
            return False
        if c == 4 and self.turn > 4:
            return False
        if c in (1, 2) and (self.caesar_delayed or not isinstance(self.leaders['Caesar'].loc, int)):
            return False
        return True

    # ------------------------------------------------------------ turn structure
    def play(self):
        try:
            for t in range(1, 7):
                self.turn = t
                self.reinforcement_phase()
                self.spring_muster()
                self.strategy_phase()
                self.winter_phase()
                if t == 3:
                    self.deck = list(CARDS.keys()); self.discard = []
                    self.hands = {'R': [], 'G': []}
                    self.rng.shuffle(self.deck)
            fv = self.final_vp()
            self.winner = 'R' if fv >= self.opt.get('vp_target', 12) else 'G'
            self.win_reason = f'end VP {fv}'
        except GameOver:
            pass
        return self.result()

    def result(self):
        return dict(winner=self.winner, reason=self.win_reason, vp=self.final_vp(), turn=self.turn,
                    stats=self.stats, elim=len(self.elim_tribes), elim_legions=len(self.elim_legions))

    # ---- reinforcement phase
    def reinforcement_phase(self):
        self.gallic_reinforcements()
        if self.turn >= 2:
            self.roman_replacements()
            self.place_caesar()
            self.roman_legates()
        self.deal()

    def legal_tribe_spaces(self, u):
        g = self.german_tribe()
        sp = []
        for s in PROVINCES[u.prov]['idx']:
            if SECTION[s] and u.name in SECTION_TRIBE and SECTION[s] != u.name:
                continue
            if STYPE[s] not in ('town', 'stronghold'):
                continue
            if self.ctype[s] in ('FT', 'SH', 'WC') or (self.ctrl[s] == 'R'):
                continue
            if any(x.loc == s and x.side == 'R' for x in self.units.values()):
                continue
            if g and g.loc == s:
                continue
            if s in self.devast:
                continue
            sp.append(s)
        return sp

    def place_tribe(self, u, s):
        moved_im = self.ctrl[s] == 'G' and self.ctype[s] == 'IM'
        u.loc = s; u.inside = True
        self.set_ctrl(s, 'G', 'FT', tribe=u.uid)
        if s == GERGOVIA and u.name == 'Arverni':
            self.ft_up.add(s)
        if moved_im:
            alt = [t for t in PROVINCES[u.prov]['idx'] if self.ctrl[t] is None and STYPE[t] == 'town'
                   and not any(x.loc == t and x.side == 'R' for x in self.units.values()) and t not in self.devast]
            if alt:
                self.set_ctrl(self.pol['G'].choose_space(self, 'G', alt, 'im_relocate'), 'G', 'IM')
        self.log(f'tribe {u.name} placed at {NAMES[s]}')

    def gallic_reinforcements(self):
        self.rng.shuffle(self.pool)
        drawn = [self.pool.pop() for _ in range(min(4, len(self.pool)))]
        keep, back = self.pol['G'].choose_reinforcements(self, [self.units[x] for x in drawn])
        for u in back:
            self.pool.append(u.uid)
        for u in keep:
            self.place_reinforcement(u)
        # Gallic leaders
        for name, t, reg in (('Ambiorix', 4, 'Belgica'), ('Vercingetorix', 5, 'Celtica')):
            u = next(x for x in self.units.values() if x.name == name)
            if self.turn == t and u.loc == f'turn{t}':
                opts = [s for s in range(N) if REGION[s] == reg and self.ctrl[s] == 'G']
                if opts:
                    u.loc = self.pol['G'].choose_space(self, 'G', opts, 'leader_arrival:' + name)
                else:
                    self.eliminate(u, 'no arrival space')

    def place_reinforcement(self, u, allow_council=True):
        sp = self.legal_tribe_spaces(u)
        choice = self.pol['G'].place_tribe_choice(self, u, sp, allow_council and len(self.council_tribes) < 2 or allow_council)
        if choice == 'council' and allow_council:
            if len(self.council_tribes) >= 2:
                # displace one tribe (not Arverni before turn 5)
                cands = [x for x in self.council_tribes if not (self.units[x].name == 'Arverni' and not self.arverni_free())]
                if not cands:
                    choice = sp[0] if sp else None
                else:
                    out = self.units[cands[0]]
                    self.council_tribes.remove(out.uid)
                    u.loc = 'council'; self.council_tribes.append(u.uid)
                    self.place_reinforcement(out, allow_council=False)
                    return
            else:
                u.loc = 'council'; self.council_tribes.append(u.uid)
                return
        if isinstance(choice, int) and choice in sp:
            self.place_tribe(u, choice)
            return
        if sp:
            self.place_tribe(u, sp[0]); return
        # submit
        u.steps = 1; u.loc = 'submitted'; self.submitted.append(u.uid)
        self.log(f'tribe {u.name} submits on arrival')

    def arverni_free(self):
        return self.turn >= 5 or len([n for n in self.elim_tribes if n not in ('Vercingetorix', 'Ambiorix')]) >= 6

    def roman_replacements(self):
        steps = 2
        prov_ims = [s for s in range(N) if REGION[s] == 'Provincia' and self.ctrl[s] == 'R' and self.ctype[s] == 'IM']
        extra = self.pol['R'].emergency_replacements(self, prov_ims)
        if extra:
            for s in extra[: (len(extra) // 3) * 3]:
                self.clear_ctrl(s)
            steps += len(extra) // 3
        self.apply_replacements(steps)
        if self.turn == 5:
            for u in list(self.units.values()):
                if u.loc == 'turn5':
                    opts = self.legion_arrival_spaces()
                    u.loc = self.pol['R'].choose_space(self, 'R', opts, 'reinforce') if opts else 'elim'
                    if u.loc == 'elim':
                        self.elim_legions.append(u.uid)

    def legion_arrival_spaces(self):
        rome = self.path_to_rome()
        opts = [s for s in range(N) if self.ctype[s] == 'WC' and self.ctrl[s] == 'R' and not self.is_besieged(s)]
        opts += [u.loc for u in self.on_map('R', 'legion') if u.loc in rome and not self.unit_besieged(u)]
        return sorted(set(opts))

    def apply_replacements(self, steps):
        rome = self.path_to_rome()
        while steps > 0:
            red = [u for u in self.on_map('R', 'legion') if u.steps == 1 and u.loc in rome and not self.unit_besieged(u)]
            if red:
                u = self.pol['R'].choose_replacement(self, red)
                u.steps = 2; steps -= 1
                continue
            if steps >= 2:
                el = [self.units[x] for x in self.elim_legions]
                opts = self.legion_arrival_spaces()
                if el and opts:
                    u = el[0]
                    self.elim_legions.remove(u.uid)
                    u.steps = 1; u.loc = self.pol['R'].choose_space(self, 'R', opts, 'replace')
                    steps -= 2
                    continue
            break

    def place_caesar(self):
        c = self.leaders['Caesar']
        if not self.caesar_delay_used and self.d6() == 1:
            self.caesar_delay_used = True
            self.caesar_delayed = True
            c.loc = 'rome'
            self.log('Caesar delayed')
            return
        self.caesar_delayed = False
        self.put_caesar()

    def put_caesar(self):
        c = self.leaders['Caesar']
        rome = self.path_to_rome()
        opts = [s for s in rome if self.ctrl[s] == 'R' and not self.is_besieged(s)]
        c.loc = self.pol['R'].choose_space(self, 'R', opts, 'caesar') if opts else BRIGANTIUM

    def roman_legates(self):
        # legates removed in winter; draw two (one may be kept)
        for k in [k for k, l in self.leaders.items() if k != 'Caesar']:
            if k != self.kept_legate:
                self.legate_cup.append(k)
                del self.leaders[k]
        n = 2 - (1 if self.kept_legate and self.kept_legate in self.leaders else 0)
        self.rng.shuffle(self.legate_cup)
        names = [self.legate_cup.pop() for _ in range(n)]
        if self.kept_legate and self.kept_legate in self.leaders:
            names.append(self.kept_legate)
        self.kept_legate = None
        opts = sorted(set([u.loc for u in self.on_map('R', 'legion')] +
                          [s for s in range(N) if self.ctype[s] == 'WC' and self.ctrl[s] == 'R']))
        for nm in names:
            b, c, m = ROMAN_LEADERS[nm]
            l = Leader(nm, 'R', b, c, m, 'cup')
            self.leaders[nm] = l
            l.loc = self.pol['R'].choose_space(self, 'R', opts, 'legate:' + nm) if opts else 'cup'

    # ---- spring muster
    def spring_muster(self):
        self.pol['G'].spring_muster(self)
        for u in self.units.values():
            u.moved = False

    def muster_move(self, units, path):
        """Gallic spring muster move of a stack along path (3 MP, restrictions 6.2)."""
        if not units:
            return
        start = units[0].loc
        mp = 3
        cur = start
        leader = next((u for u in units if u.is_leader), None)
        cr = leader.cr if leader else 2
        for nxt in path:
            if (cur, nxt) not in EDGE:
                break
            cost = self.step_cost(cur, nxt, len([u for u in units if u is not leader]), cr)
            if cost > mp or not self.muster_ok(nxt):
                break
            mp -= cost; cur = nxt
        # may not end in Roman-controlled space: back off
        while cur != start and self.ctrl[cur] == 'R':
            break
        if self.ctrl[cur] == 'R':
            return
        for u in units:
            u.loc = cur; u.inside = False

    def muster_ok(self, s):
        if REGION[s] in ('Germania', 'Britannia'):
            return False
        if any(u.loc == s and u.side == 'R' for u in self.units.values()):
            return False
        g = self.german_tribe()
        if g and g.loc == s:
            return False
        # no space where it could be intercepted: adjacent Roman army (Rome cannot
        # intercept into a Gallic-controlled space)
        if self.ctrl[s] == 'G':
            return True
        for t, k in ADJ[s]:
            if k != 'channel' and (any(u.loc == t and u.side == 'R' for u in self.units.values()) or
                                   any(l.loc == t for l in self.leaders.values())):
                return False
        return True

    # ---- strategy phase
    def strategy_phase(self):
        self.turn_plays = {'R': 0, 'G': 0}
        first = 'G'
        if 47 in self.hands['R'] and self.pol['R'].play_winter_campaign(self):
            first = 'R'
            self.hands['R'].remove(47); self.discard.append(47); self.card_left('R', 47)
            self.stats['plays']['R'] += 1
            self.reset_moved()
            self.active = 'R'
            self.pol['R'].winter_campaign_move(self)
            self.end_card_play('R')
            order = ['G', 'R']
        else:
            order = ['G', 'R']
        roman_plays = 1 if first == 'R' else 0
        idx = 0
        empty_streak = 0
        guard = 0
        while guard < 60:
            guard += 1
            side = order[idx % 2]
            idx += 1
            self.handle_surprises_start(side)
            if not self.hands[side]:
                empty_streak += 1
                if empty_streak >= 2 or not self.hands[OTHER[side]]:
                    if not self.hands[OTHER[side]] and not self.hands[side]:
                        break
                continue
            empty_streak = 0
            if side == 'R':
                roman_plays += 1
                if self.caesar_delayed and roman_plays == 2:
                    self.caesar_delayed = False
                    self.put_caesar()
            self.card_play(side)
            if not self.hands['R'] and not self.hands['G']:
                break
        # discard leftover surprise cards
        for side in ('R', 'G'):
            for c in self.hands[side]:
                self.card_left(side, c)
            self.discard.extend(self.hands[side]); self.hands[side] = []
        if self.caesar_delayed:
            self.caesar_delayed = False
            self.put_caesar()

    def handle_surprises_start(self, side):
        h = self.hands[side]
        sur = [c for c in h if CARDS[c]['kind'] == 'surprise']
        if not sur:
            return
        all_surprises = len(sur) == len(h)
        if all_surprises or self.pol[side].discard_surprise(self, side, sur):
            # discard an all-Surprise hand (or the cards the policy wishes) and draw replacements
            gone = [c for c in list(sur) if all_surprises or self.pol[side].discard_surprise(self, side, [c])]
            for c in gone:
                h.remove(c); self.discard.append(c); self.card_left(side, c)
            self.draw(side, len(gone))

    def reset_moved(self):
        for u in self.units.values():
            u.moved = False
        for l in self.leaders.values():
            l.moved = False
        self.sieged_this_card = set()

    def card_play(self, side):
        self.active = side
        self.turn_plays[side] = self.turn_plays.get(side, 0) + 1
        self.reset_moved()
        c, mode = self.pol[side].choose_play(self, side)
        if c not in self.hands[side]:
            c = [x for x in self.hands[side] if CARDS[x]['kind'] != 'surprise'][0]; mode = 'ap'
        if CARDS[c]['kind'] == 'surprise':
            # discarding a Surprise is not a card play (7.5.4): discard, replace, choose again
            self.hands[side].remove(c); self.discard.append(c); self.card_left(side, c); self.draw(side, 1)
            self.turn_plays[side] -= 1
            self._sur_guard = getattr(self, '_sur_guard', 0) + 1
            if self._sur_guard < 5 and any(CARDS[x]['kind'] != 'surprise' for x in self.hands[side]):
                self.card_play(side)
            self._sur_guard = 0
            return
        self.hands[side].remove(c)
        self.card_left(side, c)
        self.stats['plays'][side] += 1
        if mode in ('event', 'bonus') and not self.event_allowed(side, c):
            mode = 'ap'
        self.log(f'{side} plays #{c} {CARDS[c]["title"]} as {mode}')
        if mode in ('event', 'bonus'):
            opp = OTHER[side]
            if 24 in self.hands[opp] and self.pol[opp].react(self, opp, c):
                self.hands[opp].remove(24); self.discard.append(24); self.card_left(opp, 24)
                self.discard.append(c)
                self.draw(opp, 1); self.draw(side, 1)
                self.log(f'{opp} cancels #{c} with #24')
                if self.hands[side]:
                    self.card_play(side)
                return
            self.stats['events'][side] += 1
            import events
            events.do_event(self, side, c)
            if CARDS[c]['kind'] == 'bonus':
                self.reset_moved_except_event()
                self.pol[side].spend_ap(self, side, self.ap(c))
        else:
            self.pol[side].spend_ap(self, side, self.ap(c))
        # #42 leaves play only when its Event actually hands it to Rome; otherwise it is discarded
        if not (c == 42 and 42 in self.hands['R']):
            self.discard.append(c)
        self.end_card_play(side)

    def reset_moved_except_event(self):
        # CUs moved by the bonus event may not move again: keep their flag
        self.sieged_this_card = set(self.sieged_this_card)

    def end_card_play(self, side):
        self.lift_sieges()
        self.supply_phase(side)
        self.check_sudden_none()

    def check_sudden_none(self):
        pass

    # ---- winter
    def winter_phase(self):
        # A. return home
        self.siege = {}
        for u in list(self.on_map()):
            if u.merc:
                self.to_holding(u)
        for u in list(self.on_map('G', 'tribe')):
            ft = [s for s, t in self.ft_tribe.items() if t == u.uid]
            if ft:
                u.loc = ft[0]; u.inside = True
        for u in list(self.on_map('G', 'gleader')):
            reg = 'Belgica' if u.name == 'Ambiorix' else 'Celtica'
            opts = [s for s in range(N) if REGION[s] == reg and self.ctrl[s] == 'G'
                    and not any(x.loc == s and x.side == 'R' for x in self.units.values())]
            if opts:
                u.loc = self.pol['G'].choose_space(self, 'G', opts, 'winter_leader'); u.inside = False
            else:
                self.eliminate(u, 'winter')
        for u in self.units.values():
            if isinstance(u.loc, int) and u.side == 'G':
                pass
        # B. Roman winter
        keep = self.pol['R'].keep_legate(self)
        for k in [k for k in self.leaders if k != 'Caesar']:
            if k == keep:
                self.kept_legate = k
                self.leaders[k].loc = 'kept'
            else:
                self.legate_cup.append(k); del self.leaders[k]
        self.leaders['Caesar'].loc = 'rome'
        for u in self.on_map():
            u.inside = False if u.side == 'R' and self.fort_owner(u.loc) != 'R' else u.inside
        self.pol['R'].winter_camp(self)
        self.winter_attrition()
        # C. isolation
        self.isolation('R'); self.isolation('G')
        # D. political
        gp = self.governance()
        if gp <= 3:
            self.winner = 'G'; self.win_reason = f'governance {gp} on turn {self.turn}'
            raise GameOver()
        award = 2 if gp >= 9 else (1 if gp >= 7 else 0)
        if award:
            self.add_vp(award, f'governance {gp}')
        self.log(f'governance {gp}')
        net = self.vp - len(self.elim_legions) + len(self.elim_tribes) // 4
        if self.roman_auto_victory():
            self.winner = 'R'; self.win_reason = f'automatic victory turn {self.turn}'
            raise GameOver()
        # E. end of winter
        self.devast = set()
        for s in STRONGHOLD_SPACES:
            if self.ctrl[s] == 'G' and self.ctype[s] == 'IM' and not any(u.loc == s and u.side == 'R' for u in self.units.values()):
                self.set_ctrl(s, 'G', 'SH')
        for s in range(N):
            if self.ctrl[s] is None and any(u.loc == s and u.kind == 'legion' for u in self.units.values()):
                if REGION[s] not in ('Germania', 'Britannia') or True:
                    self.set_ctrl(s, 'R', 'IM')
                    self.after_im_change(s)
        if self.council_ims:
            self.council_ims -= (self.council_ims + 1) // 2
        for u in self.units.values():
            u.moved = False

    def final_vp(self):
        return self.vp - len(self.elim_legions) + len(self.elim_tribes) // 4

    def winter_camp_move(self, u, path):
        cur = u.loc
        mp = 3
        g = self.german_tribe()
        for nxt in path:
            if (cur, nxt) not in EDGE:
                break
            cost = 1 if EDGE[(cur, nxt)] == 'path' else 2
            if cost > mp:
                break
            if g and g.loc == nxt:
                break
            if REGION[nxt] in ('Germania', 'Britannia') and False:
                break
            mp -= cost; cur = nxt
        u.loc = cur
        u.inside = self.fort_owner(cur) == 'R'

    def forage(self, s):
        if self.ctype[s] == 'WC' and self.ctrl[s] == 'R':
            return 99
        if (self.ctrl[s] is not None and self.ctrl[s] != 'R') or s in self.devast:
            return 0
        if self.ctrl[s] == 'R':
            return 4
        return 2

    def winter_attrition(self):
        by = {}
        for u in self.on_map('R', 'legion'):
            by.setdefault(u.loc, []).append(u)
        for s, us in by.items():
            excess = len(us) - self.forage(s)
            if excess > 0:
                us = sorted(us, key=lambda u: (-u.steps, u.elite))
                for u in us[:excess]:
                    u.steps -= 1
                    self.stats['legion_steps_lost'] += 1
                    if u.steps <= 0:
                        self.eliminate(u, 'winter attrition')
                self.log(f'winter attrition {NAMES[s]} {excess}')

    def isolation(self, side):
        anchors = set()
        for s in range(N):
            if any(u.loc == s and u.side == side and not self.unit_besieged(u) for u in self.units.values()):
                anchors.add(s)
            if self.ctrl[s] == side and self.ctype[s] in ('SH', 'WC', 'FT') and not self.is_besieged(s):
                anchors.add(s)
            if self.ctrl[s] == side and PORTS[s] and any(self.naval_supremacy(side, z) for z in PORTS[s]):
                anchors.add(s)
        seen = set(anchors)
        dq = deque(anchors)

        def ok(t):
            if any(u.loc == t and u.side != side for u in self.units.values()):
                return False
            if t in self.devast:
                return False
            if self.ctrl[t] is not None and self.ctrl[t] != side:
                return False
            return True
        while dq:
            s = dq.popleft()
            for t, k in ADJ[s]:
                if t not in seen and ok(t):
                    seen.add(t); dq.append(t)
        # an IM is safe if any neighbour (or its own space, when it holds a friendly CU) is reached
        for s in range(N):
            if self.ctrl[s] == side and self.ctype[s] == 'IM' and s not in seen:
                if any(t in seen and ok(t) for t, k in ADJ[s]):
                    continue
                if side == 'G' and REGION[s] in ('Germania', 'Britannia'):
                    continue
                self.clear_ctrl(s)
                self.log(f'isolated {side} IM removed {NAMES[s]}')

    def governance(self):
        pc = self.prov_control()
        pts = 0
        for reg, dom, pres in (('Celtica', 5, 2), ('Belgica', 4, 2)):
            r = sum(1 for p in REG_PROVS[reg] if pc[p] == 'R')
            g = sum(1 for p in REG_PROVS[reg] if pc[p] == 'G')
            if r > g:
                pts += dom
            elif any(self.ctrl[s] == 'R' for p in REG_PROVS[reg] for s in PROVINCES[p]['idx']):
                pts += pres
        if any(self.ctrl[s] == 'R' for s in PROVINCES['Aquitania']['idx']):
            pts += 1
        for p, pen in (('Volcae', 1), ('Allobroges', 1), ('Narbonensis', 3)):
            if pc[p] != 'R':
                pts -= pen
        return pts

    def roman_auto_victory(self):
        if any(t == 'FT' for t in self.ctype):
            return False
        pc = self.prov_control()
        for reg, need in (('Belgica', 5), ('Celtica', 7), ('Aquitania', 1)):
            if sum(1 for p in REG_PROVS[reg] if pc[p] == 'R') < need:
                return False
        return all(pc[p] == 'R' for p in PROVINCIA)


def end_score(g):
    return g.final_vp()
