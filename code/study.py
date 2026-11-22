"""Final simulation study: every level of both bots against four computer opponents.
Seeds 100000+ and 200000+ were never used during development."""
import json, sys, time
from harness import evaluate

IMP_LEVELS = {1: {}, 2: {'ap_first_R': 4}, 3: {'ap_bonus_R': 1}, 4: {'ap_bonus_R': 1, 'vp_target': 10},
              5: {'ap_bonus_R': 1, 'vp_target': 9}}
CON_LEVELS = {1: {'vp_target': 9}, 2: {'vp_target': 10}, 3: {'vp_target': 11}, 4: {}, 5: {'ap_first_G': 4}}
OPPS = {'bot': ('bot', {}), 'smart': ('smart', {}), 'smart-aggressive': ('smart', {'aggr': 1.5, 'infl': 0.7}),
        'search': ('search', {})}


def main(n_fast=150, n_search=80, out='results/study_v1.json', sides=('Imperator', 'Concilium'), res=None):
    res = res or {}
    t0 = time.time()
    for side, levels in (('Imperator', IMP_LEVELS), ('Concilium', CON_LEVELS)):
        if side not in sides:
            continue
        for lvl, opt in levels.items():
            for oname, ospec in OPPS.items():
                n = n_search if oname == 'search' else n_fast
                if side == 'Imperator':
                    r = evaluate(('bot', {}), ospec, range(100000, 100000 + n), options=opt)
                    wins = sum(x['winner'] == 'R' for x in r)
                else:
                    # the paper-bot Rome opponent plays at its own level 3 (+1 AP on every card play)
                    o2 = dict(opt, ap_bonus_R=1) if oname == 'bot' else opt
                    r = evaluate(ospec, ('bot', {}), range(200000, 200000 + n), options=o2)
                    wins = sum(x['winner'] == 'G' for x in r)
                key = f'{side} L{lvl} vs {oname}'
                res[key] = dict(n=n, bot_wins=wins, vp=[x['vp'] for x in r], reasons=[x['reason'] for x in r],
                                battles=[x['stats']['battles'] for x in r], sieges=[x['stats']['sieges'] for x in r])
                print(key, wins, '/', n, f'{time.time()-t0:.0f}s', flush=True)
                json.dump(res, open(out, 'w'))


if __name__ == '__main__':
    main()
