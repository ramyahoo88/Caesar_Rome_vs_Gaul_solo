"""Regression tests for the independent v1.0 audit findings C01-C04 (corrected behaviour).
The positions follow audit/independent-v1.0/evidence/focused_rules.py, which asserted the old,
defective behaviour.  Run from the code folder:  python3 tests/test_audit_fixes.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import Game, N, IDX, ADJ, CARDS, PROVINCES, STYPE
from bots import BotPolicy
from policies import BasePolicy


def fresh(seed=1):
    g = Game({s: BotPolicy(s, seed) for s in 'RG'}, seed=seed, log=True)
    for u in g.units.values():
        u.loc = 'hold'; u.inside = False; u.moved = False
    for l in g.leaders.values():
        l.loc = 'cup'; l.moved = False
    g.ctrl = [None] * N; g.ctype = [None] * N; g.siege = {}; g.ft_tribe = {}; g._pc_cache = None
    g.devast = set(); g.sieged_this_card = set(); g.hands = {'R': [], 'G': []}
    return g


class EventOpponent(BasePolicy):
    def choose_play(self, g, side):
        if 6 in g.hands[side]:
            return 6, 'event'
        return next(c for c in g.hands[side] if CARDS[c]['kind'] != 'surprise'), 'ap'

    def spend_ap(self, g, side, ap):
        pass


class APPlayer(BasePolicy):
    def choose_play(self, g, side):
        return g.hands[side][0], 'ap'

    def spend_ap(self, g, side, ap):
        pass


def test_c01_unrevealed_reaction_is_not_used():
    g = Game({'R': BotPolicy('R', 9), 'G': EventOpponent('G', 9)}, seed=9, log=True)
    g.hands = {'R': [24, 45], 'G': [6]}
    g.deck = [c for c in CARDS if c not in (24, 45, 6, 7, 8)] + [7, 8]; g.discard = []
    g.card_play('G')
    assert not any('cancels' in x for x in g.logs)
    assert 24 in g.hands['R']


def test_c01_revealed_reaction_is_used():
    g = Game({'R': BotPolicy('R', 9), 'G': EventOpponent('G', 9)}, seed=9, log=True)
    g.hands = {'R': [24, 45], 'G': [6]}
    g.deck = [c for c in CARDS if c not in (24, 45, 6, 7, 8)] + [7, 8]; g.discard = []
    g.pol['R'].choose_play(g, 'R')            # the Offer reveals #24 into the Reserve
    assert 24 in g.pol['R'].reserve
    g.card_play('G')
    assert any('R cancels #6 with #24' in x for x in g.logs)


def test_c01_reserve_cleared_each_turn():
    g = Game({'R': BotPolicy('R', 9), 'G': EventOpponent('G', 9)}, seed=9)
    g.hands = {'R': [24, 45], 'G': [6]}
    g.pol['R'].choose_play(g, 'R')
    g.turn += 1
    assert not g.pol['R'].in_reserve(g, 'R', 24)


def test_c02_sweep_respects_vacated_route():
    g = fresh(); b = g.pol['G']
    u = next(x for x in g.units.values() if x.name == 'Remi'); u.steps = 1; u.loc = IDX['Aduatuci']
    legs = [x for x in g.units.values() if x.kind == 'legion'][:2]
    for q in legs:
        q.loc = IDX['Menapii']
    t = IDX['Eburones']; g.set_ctrl(t, 'R', 'IM')
    assert b.sweep(g, 'G', lambda s: 1 if s == t else 0) is None
    legs[1].loc = 'hold'                     # control: one Legion is too weak, the raid is safe
    plan = b.sweep(g, 'G', lambda s: 1 if s == t else 0)
    assert plan is not None and plan[2][-1] == ('remove_im',)


def test_c02_regroup_respects_vacated_route():
    g = fresh(); b = g.pol['R']
    a = next(x for x in g.units.values() if x.name == 'Arverni'); a.loc = IDX['Menapii']
    legs = [x for x in g.units.values() if x.kind == 'legion'][:2]
    legs[0].loc = IDX['Aduatuci']; legs[1].loc = IDX['Eburones']
    calls = []
    g.activate = lambda side, l, us, plan, **kw: calls.append(plan)
    b.m_regroup(g, 1)
    assert all(p[-1] != ('to', IDX['Eburones']) for p in calls)


def test_c03_siege_contributors_are_activated():
    g = fresh(11); t = IDX['Gergovia']
    a = next(x for x in g.units.values() if x.name == 'Arverni'); a.loc = t; a.inside = True
    g.set_ctrl(t, 'G', 'FT', a.uid)
    legs = [x for x in g.units.values() if x.kind == 'legion'][:8]
    for q in legs:
        q.loc = t
    cz = g.leaders['Caesar']; cz.loc = t; g.roll2 = lambda: 2
    g.activate('R', cz, legs[:6], [('siege',)])
    assert g.stats['sieges'] == 1 and all(q.moved for q in legs)
    nxt = next(s for s, k in ADJ[t] if k == 'path' and g.can_enter('R', s))
    g.activate('R', None, legs[6:], [('to', nxt)])
    assert all(q.loc == t for q in legs[6:])


def test_c04_card42_conserved():
    for card in (42, 45):
        g = Game({'R': APPlayer('R', 3), 'G': APPlayer('G', 3)}, seed=3)
        g.hands = {'R': [card], 'G': [6]}; g.deck = [c for c in CARDS if c not in (card, 6)]; g.discard = []
        g.card_play('R')
        allc = g.deck + g.discard + g.hands['R'] + g.hands['G']
        assert card in g.discard and len(allc) == 55


def test_c04_card42_event_hands_it_to_rome():
    class G42(BasePolicy):
        def choose_play(self, g, side):
            if 42 in g.hands[side]:
                return 42, 'event'
            return g.hands[side][0], 'ap'

        def spend_ap(self, g, side, ap):
            pass
    g = Game({'R': APPlayer('R', 3), 'G': G42('G', 3)}, seed=3)
    g.hands = {'R': [10, 11], 'G': [42, 6]}; g.deck = [c for c in CARDS if c not in (10, 11, 42, 6)]; g.discard = []
    g.card_play('G')
    allc = g.deck + g.discard + g.hands['R'] + g.hands['G']
    assert 42 in g.hands['R'] and 42 not in g.discard and len(allc) == 55



# ---------------------------------------------------------------- v1.1 re-audit (R01-R03)
from engine import PROV


def test_r01_all_surprise_reserve_fully_replaced():
    g = fresh(9); g.hands = {'R': [52, 54], 'G': [45]}; g.deck = [7, 6]
    g.discard = [c for c in CARDS if c not in (52, 54, 45, 7, 6)]
    p = g.pol['R']; p.reserve = {52, 54}; p._reserve_turn = g.turn
    g.handle_surprises_start('R')
    assert sorted(g.hands['R']) == [6, 7] and g.deck == []
    assert len(g.deck + g.discard + g.hands['R'] + g.hands['G']) == 55


def test_r01_three_surprises_and_mixed_hand():
    g = fresh(9); g.hands = {'R': [52, 54, 55], 'G': [45]}; g.deck = [8, 7, 6]
    g.discard = [c for c in CARDS if c not in (52, 54, 55, 45, 8, 7, 6)]
    g.handle_surprises_start('R')
    assert sorted(g.hands['R']) == [6, 7, 8]
    # mixed hand: only a revealed #55 goes; an unrevealed one stays
    g = fresh(9); g.hands = {'R': [55, 10], 'G': [45]}; g.deck = [6]
    g.discard = [c for c in CARDS if c not in (55, 10, 45, 6)]
    g.handle_surprises_start('R'); assert sorted(g.hands['R']) == [10, 55]
    g.pol['R'].reserve = {55}; g.pol['R']._reserve_turn = g.turn
    g.handle_surprises_start('R'); assert sorted(g.hands['R']) == [6, 10]


def test_r02_redrawn_reserve_card_is_face_down():
    g = fresh(94); g.hands = {'R': [52, 45], 'G': [6, 7, 8, 9, 10, 11, 12, 13]}; g.deck = []
    g.discard = [c for c in CARDS if c not in g.hands['R'] + g.hands['G']]
    p = g.pol['R']; p.reserve = {52}; p._reserve_turn = g.turn
    t = IDX['Gergovia']; a = next(u for u in g.units.values() if u.name == 'Arverni'); a.loc = t; a.inside = True
    g.set_ctrl(t, 'G', 'FT', a.uid)
    legs = [u for u in g.units.values() if u.kind == 'legion'][:6]
    for u in legs:
        u.loc = t
    cz = g.leaders['Caesar']; cz.loc = t; g.roll2 = lambda: 2
    assert g.siege_roll('R', t, cz, legs, caesar=True)
    assert sorted(g.hands['R']) == [45, 52]            # #52 spent, reshuffled and drawn back
    assert p.use_vow_siege(g, t) is False              # ... but it is face down again


def test_r03_gallic_leader_alone_is_a_threat():
    g = fresh(31); g.turn = 5; t = IDX['Bibracte']; start = next(s for s, k in ADJ[t] if k == 'path')
    v = next(u for u in g.units.values() if u.name == 'Vercingetorix'); v.loc = start
    leg = next(u for u in g.units.values() if u.kind == 'legion'); leg.loc = t
    for s in PROVINCES[PROV[t]]['idx']:
        if s != t:
            g.set_ctrl(s, 'G', 'IM')
    p = g.pol['R']
    base = p.threat_armies(g, 'G')
    assert any(l is v for cs, d, l, us, st in base)
    assert p.in_danger(g, 'R', t, [], p.threat_after_move(g, 'G', base, [], None)) is True
    g.ctrl = [None] * N; g.ctype = [None] * N; g._pc_cache = None      # control: no Local Support
    base = p.threat_armies(g, 'G')
    assert p.in_danger(g, 'R', t, [], p.threat_after_move(g, 'G', base, [], None)) is False


# ---------------------------------------------------------------- v1.2 re-audit (R06)
class TraceBot(BotPolicy):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw); self.frames = []

    def choose_play(self, g, side):
        before = list(g.hands[side]); r = super().choose_play(g, side)
        self.frames.append({'hand': before, 'chosen': list(r), 'reserve': sorted(self.reserve)})
        return r


def _extra_play_case(trigger):
    p = TraceBot('G', 0); r = TraceBot('R', 0); g = Game({'G': p, 'R': r}, seed=0, log=True)
    rh = [6, 45] if trigger == 42 else [24, 45]
    g.hands = {'R': rh, 'G': [55, trigger, 47]}
    g.deck = [c for c in CARDS if c not in rh + [55, trigger, 47]]; g.discard = []
    if trigger == 21:
        r.reserve = {24}; r._reserve_turn = g.turn
    g.card_play('G')
    return g, p


def test_r06_forced_march_cleanup_before_extra_play_after_42():
    g, p = _extra_play_case(42)
    assert p.frames[0]['chosen'] == [42, 'event'] and 55 in p.frames[0]['reserve']
    assert len(p.frames) >= 2 and 55 not in p.frames[1]['hand']     # discarded before the second Offer
    assert 55 in g.discard
    assert sorted(g.deck + g.discard + g.hands['R'] + g.hands['G']) == list(range(1, 56))


def test_r06_forced_march_cleanup_before_play_after_cancel():
    g, p = _extra_play_case(21)
    assert any('cancels #21' in x for x in g.logs)
    assert len(p.frames) >= 2 and 55 not in p.frames[1]['hand']
    assert sorted(g.deck + g.discard + g.hands['R'] + g.hands['G']) == list(range(1, 56))


def test_r06_unrevealed_forced_march_stays_and_normal_path_discards():
    g = Game({s: BotPolicy(s, 0) for s in 'RG'}, seed=0); g.hands = {'G': [55, 47], 'R': [45]}
    g.deck = [c for c in CARDS if c not in (55, 47, 45)]; g.discard = []
    g.handle_surprises_start('G'); assert 55 in g.hands['G']          # face down: stays
    g.pol['G'].reserve = {55}; g.pol['G']._reserve_turn = g.turn
    g.handle_surprises_start('G'); assert 55 not in g.hands['G'] and 55 in g.discard

if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn(); print('ok', name)
