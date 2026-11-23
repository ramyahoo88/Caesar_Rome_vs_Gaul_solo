"""AP-value sensitivity: 2nd-edition rules throughout; only the card AP values switch to 1st edition."""
from harness import evaluate
import statistics, json
OUT = {}
for name, rs, gs, opt, n, who in (('imp_con', ('bot', {}), ('bot', {}), {'ap_bonus_R': 1}, 300, 'R'),
                                   ('imp_search', ('bot', {}), ('search', {}), {'ap_bonus_R': 1}, 120, 'R'),
                                   ('con_search', ('search', {}), ('bot', {}), {}, 120, 'G')):
    row = {}
    for lab, extra in (('ap2', {}), ('ap1', {'ap_edition': 1})):
        r = evaluate(rs, gs, range(14000, 14000 + n), edition=2, options=dict(opt, **extra))
        row[lab] = dict(win=sum(x['winner'] == who for x in r) / n, vp=[x['vp'] for x in r],
                        winner=[x['winner'] for x in r], reason=[x['reason'] for x in r])
    d = [a - b for a, b in zip(row['ap1']['vp'], row['ap2']['vp'])]
    row['paired_vp_diff'] = statistics.mean(d); row['se'] = statistics.stdev(d) / n ** 0.5; row['n'] = n
    row['seeds'] = [14000, 14000 + n]; row['settings'] = dict(edition=2, options=opt, ap1_extra={'ap_edition': 1}, roman=rs, gallic=gs)
    OUT[name] = row
    print(name, f"ap2 {row['ap2']['win']:.1%} ap1 {row['ap1']['win']:.1%} dVP {row['paired_vp_diff']:+.2f} ± {row['se']:.2f}", flush=True)
r = OUT
t = (f"Only the card AP values were switched to their 1st-edition numbers; every other rule stayed at the 2nd-edition settings, on the same seeds. "
     f"Imperator (level 3) beat Concilium in {r['imp_con']['ap1']['win']:.0%} of {r['imp_con']['n']} games ({r['imp_con']['ap2']['win']:.0%} with the assumed 2nd-edition values; "
     f"Roman VP {r['imp_con']['paired_vp_diff']:+.2f} ± {r['imp_con']['se']:.2f}), Imperator beat the Lookahead player in {r['imp_search']['ap1']['win']:.0%} of {r['imp_search']['n']} "
     f"({r['imp_search']['ap2']['win']:.0%}; {r['imp_search']['paired_vp_diff']:+.2f} ± {r['imp_search']['se']:.2f} VP), and Concilium under the standard rules beat the Lookahead "
     f"player in {r['con_search']['ap1']['win']:.0%} of {r['con_search']['n']} ({r['con_search']['ap2']['win']:.0%}; Roman VP {r['con_search']['paired_vp_diff']:+.2f} ± {r['con_search']['se']:.2f}).")
# every per-seed result is kept (VP, winner and end reason for both AP settings), so the paired
# statistics can be recomputed without re-running the games
json.dump(dict(results=OUT, text=t), open('ap_only.json', 'w'), indent=1)
print(t)
