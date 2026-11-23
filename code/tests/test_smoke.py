"""Smoke tests: complete bot-vs-bot games run, finish legally and are reproducible.
Run from the code folder:  python3 -m pytest -q tests   (or: python3 tests/test_smoke.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import Game, N
from bots import BotPolicy


def play(seed, **opt):
    g = Game({'R': BotPolicy('R', seed), 'G': BotPolicy('G', seed)}, seed=seed, options=opt)
    return g, g.play()


def test_games_finish():
    for s in range(5):
        g, r = play(s, ap_bonus_R=1)
        assert r['winner'] in ('R', 'G')
        assert 1 <= r['turn'] <= 6
        assert -10 <= r['vp'] <= 30


def test_reproducible():
    _, a = play(123, ap_bonus_R=1)
    _, b = play(123, ap_bonus_R=1)
    assert (a['winner'], a['vp'], a['stats']['battles'], a['stats']['sieges']) == \
           (b['winner'], b['vp'], b['stats']['battles'], b['stats']['sieges'])


def test_board_invariants():
    g, _ = play(7, ap_bonus_R=1)
    for u in g.units.values():
        assert u.steps >= 0
        if isinstance(u.loc, int):
            assert 0 <= u.loc < N and u.steps > 0
    for s in range(N):
        if g.ctype[s] == 'FT':
            assert g.ctrl[s] == 'G'


def test_card_conservation():
    for s in range(4):
        g, _ = play(s, ap_bonus_R=1)
        allc = g.deck + g.discard + g.hands['R'] + g.hands['G']
        assert len(allc) == 55 and len(set(allc)) == 55


def test_levels_change_only_ap_or_target():
    # VP target levels play the same game; only the winner test changes
    _, a = play(42, ap_bonus_R=1)
    _, b = play(42, ap_bonus_R=1, vp_target=10)
    assert a['vp'] == b['vp']
    assert (b['winner'] == 'R') == (a['reason'].startswith('end') and a['vp'] >= 10 or a['reason'].startswith('automatic'))


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn(); print('ok', name)
