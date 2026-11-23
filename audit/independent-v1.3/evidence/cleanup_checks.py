"""Verify both original R06 positions, once-per-play timing and 101 complete games.
python3 cleanup_checks.py REPO OUTPUT_DIR
Observations happen before the Offer, after the engine's start-of-play handler.
"""
import sys, json, time
from pathlib import Path
from multiprocessing import Pool

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / 'code'))
from engine import Game, CARDS
from bots import BotPolicy
from replay_archive import ObservedGame, ObservedBot, make


class TraceBot(BotPolicy):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.frames = []

    def choose_play(self, g, side):
        before = list(g.hands[side])
        r = super().choose_play(g, side)
        self.frames.append(dict(handBeforeOffer=before, chosen=list(r),
                                reserveAfterOffer=sorted(self.reserve)))
        return r


class CountedGame(Game):
    def __init__(self, *a, **kw):
        self.cleanups = []
        super().__init__(*a, **kw)

    def handle_surprises_start(self, side):
        self.cleanups.append(dict(side=side, hand=list(self.hands[side])))
        return super().handle_surprises_start(side)


def probe(task):
    seed, search = task
    r = make(('search', {}) if search else ('bot', {}), 'R', seed)
    g = ObservedGame({'R': r, 'G': ObservedBot('G', seed)}, seed=seed,
                     options={} if search else {'ap_bonus_R': 1})
    result = g.play()
    assert sorted(g.deck + g.discard + g.hands['R'] + g.hands['G']) == list(range(1, 56))
    assert not g.missed_cleanup
    return dict(seed=seed, roman='search' if search else 'bot', result=result,
                missedForcedMarchCleanup=g.missed_cleanup)


if __name__ == '__main__':
    out.mkdir(parents=True, exist_ok=True)
    fixtures = []
    for trigger in [42, 21]:
        p, r = TraceBot('G', 0), TraceBot('R', 0)
        g = CountedGame({'G': p, 'R': r}, seed=0, log=True)
        rh = [6, 45] if trigger == 42 else [24, 45]
        g.hands = {'R': rh, 'G': [55, trigger, 47]}
        g.deck = [c for c in CARDS if c not in rh + [55, trigger, 47]]
        g.discard = []
        if trigger == 21:
            r.reserve, r._reserve_turn = {24}, g.turn
        g.card_play('G')
        assert p.frames[0]['chosen'] == [trigger, 'event']
        assert 55 in p.frames[0]['reserveAfterOffer']
        assert len(p.frames) >= 2 and 55 not in p.frames[1]['handBeforeOffer']
        assert 55 in g.discard
        assert len(g.cleanups) == len(p.frames) == 2
        if trigger == 21:
            assert any('cancels #21' in x for x in g.logs)
        assert sorted(g.deck + g.discard + g.hands['R'] + g.hands['G']) == list(range(1, 56))
        fixtures.append(dict(seed=0, trigger=trigger, romanInitialHand=rh,
                             gallicInitialHand=[55, trigger, 47], frames=p.frames,
                             cleanupCalls=g.cleanups, log=g.logs, passed=True))

    # Native strategy loop: it calls the handler exactly once for each actual card play.
    g = CountedGame({s: TraceBot(s, 123) for s in 'RG'}, seed=123)
    g.deal()
    g.strategy_phase()
    assert len(g.cleanups) == sum(len(p.frames) for p in g.pol.values())
    normal_calls = len(g.cleanups)

    # A discarded Surprise is a retry within the same play. Revealing #55 on that
    # attempt must not cause a second cleanup when the engine chooses again.
    class RetryBot(BotPolicy):
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)
            self.calls = 0

        def choose_play(self, g, side):
            self.calls += 1
            if self.calls == 1:
                self.reserve, self._reserve_turn = {55}, g.turn
                return 54, 'ap'
            assert 55 in g.hands[side]
            return 45, 'ap'

        def spend_ap(self, g, side, ap):
            pass

    p = RetryBot('G', 0)
    g = CountedGame({'R': BotPolicy('R', 0), 'G': p}, seed=0)
    g.hands = {'G': [54, 55, 45], 'R': [6]}
    g.deck = [c for c in CARDS if c not in [54, 55, 45, 6]]
    g.discard = []
    g.card_play('G')
    assert p.calls == 2 and len(g.cleanups) == 1
    assert 55 in g.hands['G'] and 55 not in g.discard
    assert g.turn_plays['G'] == 1
    retry = dict(choices=p.calls, cleanupCalls=len(g.cleanups),
                 countedCardPlays=g.turn_plays['G'], revealed55RetainedWithinSamePlay=True)

    t = time.time()
    tasks = [(s, False) for s in range(950000, 950100)] + [(200002, True)]
    with Pool(4) as pool:
        records = pool.map(probe, tasks, chunksize=1)
    result = dict(fixtures=fixtures, normalStrategyCleanupCalls=normal_calls,
                  retryControl=retry, records=records, games=len(records),
                  affectedGames=sum(bool(r['missedForcedMarchCleanup']) for r in records),
                  seconds=time.time() - t)
    (out / 'cleanup-results.json').write_text(json.dumps(result, indent=2))
    print(json.dumps({k: result[k] for k in ['games', 'affectedGames', 'seconds']}))
