"""Latest-change comparisons on the corrected engine, with per-seed results and paired differences."""
from harness import evaluate
import sys, statistics, json
R_VARS = {'R_final': {}, 'R_no_danger': {'regroup': False, 'safe_raid': False, 'r_pre': ('CONTINUE', 'PROTECT', 'SUBMIT')},
          'R_no_lagging': {'dominance_race': False}, 'R_no_caesar21': {'caesar_siege_col': None}}
G_VARS = {'G_final': {}, 'G_no_danger': {'g_safe_raid': 0}}
OPP = (('bot', 200), ('smart', 160), ('search', 100))
res = {}
for k in list(R_VARS) + list(G_VARS):
    out = {}
    for opp, n in OPP:
        seeds = range(20000, 20000 + n)
        if k in R_VARS:
            r = evaluate(('bot', R_VARS[k]), (opp, {}), seeds, options={'ap_bonus_R': 1})
            w = [x['winner'] == 'R' for x in r]
        else:
            opt = {'ap_bonus_R': 1} if opp == 'bot' else {}
            r = evaluate((opp, {}), ('bot', G_VARS[k]), seeds, options=opt)
            w = [x['winner'] == 'G' for x in r]
        out[opp] = dict(n=n, win=sum(w) / n, vp=statistics.mean(x['vp'] for x in r), per_seed_vp=[x['vp'] for x in r],
                        per_seed_win=w, elim_legions=statistics.mean(x['elim_legions'] for x in r))
    res[k] = out
    print(k, ' | '.join(f"{o}: {v['win']:.1%} {v['vp']:.2f}" for o, v in out.items()), flush=True)
    json.dump(res, open('latest_v1_2.json', 'w'))
pairs = {}
for k in list(res):
    base = 'R_final' if k.startswith('R') else 'G_final'
    if k == base:
        continue
    pairs[k] = {}
    for opp, n in OPP:
        d = [a - b for a, b in zip(res[k][opp]['per_seed_vp'], res[base][opp]['per_seed_vp'])]
        pairs[k][opp] = dict(mean_vp_diff=statistics.mean(d), se=statistics.stdev(d) / len(d) ** 0.5)
    print(k, ' | '.join(f"{o}: {v['mean_vp_diff']:+.2f} ± {v['se']:.2f}" for o, v in pairs[k].items()), flush=True)
res['_paired'] = pairs
json.dump(res, open('latest_v1_2.json', 'w'))
