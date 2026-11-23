"""Latest-change comparisons on the corrected v1.1 engine (seeds 20000+)."""
from harness import evaluate
import sys, statistics, json
R_VARS = {'R_final': {}, 'R_no_danger': {'regroup': False, 'safe_raid': False, 'r_pre': ('CONTINUE', 'PROTECT', 'SUBMIT')},
          'R_no_lagging': {'dominance_race': False}, 'R_no_caesar21': {'caesar_siege_col': None}}
G_VARS = {'G_final': {}, 'G_no_danger': {'g_safe_raid': 0}}
res = {}
for k in sys.argv[1:]:
    out = {}
    for opp, n in (('bot', 200), ('smart', 160), ('search', 100)):
        if k in R_VARS:
            r = evaluate(('bot', R_VARS[k]), (opp, {}), range(20000, 20000 + n), options={'ap_bonus_R': 1})
            w = sum(x['winner'] == 'R' for x in r) / n
        else:
            opt = {'ap_bonus_R': 1} if opp == 'bot' else {}
            r = evaluate((opp, {}), ('bot', G_VARS[k]), range(20000, 20000 + n), options=opt)
            w = sum(x['winner'] == 'G' for x in r) / n
        out[opp] = dict(n=n, win=w, vp=statistics.mean(x['vp'] for x in r),
                        elim_legions=statistics.mean(x['elim_legions'] for x in r))
    res[k] = out
    print(k, json.dumps(out), flush=True)
    json.dump(res, open(f'latest_{sys.argv[1]}.json', 'w'), indent=1)
