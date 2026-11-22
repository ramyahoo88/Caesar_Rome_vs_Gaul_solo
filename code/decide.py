"""How games are decided: Imperator (level 3) vs Concilium (standard rules), VP sources and Governance by turn."""
import sys, json, statistics
from collections import Counter, defaultdict
from harness import evaluate

n = int(sys.argv[1]) if len(sys.argv) > 1 else 200
res = evaluate(('bot', {}), ('bot', {}), range(300000, 300000 + n), options={'ap_bonus_R': 1})
src = Counter(); gov = defaultdict(list)
for r in res:
    for t, v, why in r['vp_log']:
        k = why.split()[0]
        src[k] += v
        if k == 'governance':
            gov[t].append(int(why.split()[1]))
out = dict(
    n=n,
    rome_wins=sum(r['winner'] == 'R' for r in res),
    mean_vp=statistics.mean(r['vp'] for r in res),
    vp_hist=sorted(Counter(r['vp'] for r in res).items()),
    sources={k: v / n for k, v in src.items()},
    elim_legions=statistics.mean(r['elim_legions'] for r in res),
    elim_tribes=statistics.mean(r['elim'] for r in res),
    battles=statistics.mean(r['stats']['battles'] for r in res),
    sieges=statistics.mean(r['stats']['sieges'] for r in res),
    reasons=dict(Counter(r['reason'].split()[0] for r in res)),
    gov={t: dict(mean=statistics.mean(v), dist=sorted(Counter(v).items())) for t, v in sorted(gov.items())},
)
json.dump(out, open('results/decide.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
