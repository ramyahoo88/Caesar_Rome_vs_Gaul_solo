from harness import evaluate
import statistics, json
R = {}
for ed in (2, 1):
    a = evaluate(('bot', {}), ('bot', {}), range(14000, 14200), edition=ed, options={'ap_bonus_R': 1})
    b = evaluate(('bot', {}), ('search', {}), range(14000, 14080), edition=ed, options={'ap_bonus_R': 1})
    c = evaluate(('search', {}), ('bot', {}), range(14000, 14080), edition=ed, options={})
    R[ed] = dict(imp_con=sum(x['winner'] == 'R' for x in a) / len(a), imp_search=sum(x['winner'] == 'R' for x in b) / len(b),
                 con_search=sum(x['winner'] == 'G' for x in c) / len(c))
    print(ed, R[ed], flush=True)
t = (f"With the 1st-edition values, Imperator (level 3) beat Concilium in {R[1]['imp_con']:.0%} of games ({R[2]['imp_con']:.0%} with the 2nd-edition values), "
     f"Imperator beat the Lookahead player in {R[1]['imp_search']:.0%} ({R[2]['imp_search']:.0%}), and Concilium under the standard rules beat the Lookahead player in "
     f"{R[1]['con_search']:.0%} ({R[2]['con_search']:.0%}); 200, 80 and 80 games.")
json.dump(dict(results=R, text=t), open('ed1.json', 'w'), indent=1)
print(t)
