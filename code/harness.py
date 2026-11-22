"""Parallel evaluation harness."""
import sys, time, json, statistics
from multiprocessing import Pool
from engine import Game

FACTORIES = {}


def make(spec, side, seed):
    kind, kw = spec
    if kind == 'smart':
        from smart import SmartPolicy
        return SmartPolicy(side, seed, **kw)
    if kind == 'bot':
        from bots import BotPolicy
        return BotPolicy(side, seed, **kw)
    if kind == 'hyb_control':
        from hybrid import BotSmartControl
        return BotSmartControl(side, seed, **kw)
    if kind == 'hyb_cards':
        from hybrid import BotCardsSmart
        return BotCardsSmart(side, seed, **kw)
    if kind == 'hyb_missions':
        from hybrid import BotSearchMissions
        return BotSearchMissions(side, seed, **kw)
    if kind == 'search':
        from search import SearchPolicy
        return SearchPolicy(side, seed, **kw)
    if kind == 'base':
        from policies import BasePolicy
        return BasePolicy(side, seed, **kw)
    raise ValueError(kind)


def one(args):
    rspec, gspec, seed, edition, options = args
    g = Game({'R': make(rspec, 'R', seed), 'G': make(gspec, 'G', seed)}, seed=seed, edition=edition, options=options)
    r = g.play()
    r['seed'] = seed
    r['vp_log'] = g.vp_log
    r['govs'] = None
    return r


def evaluate(rspec, gspec, seeds, edition=2, options=None, procs=2):
    args = [(rspec, gspec, s, edition, options) for s in seeds]
    with Pool(procs) as p:
        res = p.map(one, args, chunksize=4)
    return res


def rate(res):
    return sum(1 for r in res if r['winner'] == 'R') / len(res)


def line(res, label):
    n = len(res)
    rw = rate(res)
    vp = statistics.mean(r['vp'] for r in res)
    gl = sum(1 for r in res if r['reason'].startswith('governance'))
    return f'{label:34s} n={n:4d} Rome {rw:6.1%}  meanVP {vp:5.2f}  govLoss {gl:3d}'


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    seeds = range(1000, 1000 + n)
    t = time.time()
    for lab, r, g in [('smart v smart', ('smart', {}), ('smart', {})),
                      ('botR v smartG', ('bot', {}), ('smart', {})),
                      ('smartR v botG', ('smart', {}), ('bot', {})),
                      ('botR v botG', ('bot', {}), ('bot', {}))]:
        print(line(evaluate(r, g, seeds), lab), flush=True)
    print(f'{time.time()-t:.0f}s')
