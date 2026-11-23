"""Recount all latest-change pairs and verify the new AP-only option's scope.
python3 check_experiments.py REPO OUTPUT
"""
import sys,json,statistics,math
from pathlib import Path
repo=Path(sys.argv[1]).resolve();sys.path.insert(0,str(repo/'code'))
from engine import Game,CARDS
from bots import BotPolicy

def close(a,b):assert math.isclose(a,b,abs_tol=1e-12),(a,b)
x=json.loads((repo/'results/latest_changes_v1.2.json').read_text());rows=0
for k,v in x.items():
    if k.startswith('_'):continue
    for opp,row in v.items():
        n=row['n'];assert len(row['per_seed_vp'])==len(row['per_seed_win'])==n
        assert all(type(w)is bool for w in row['per_seed_win'])
        close(statistics.mean(row['per_seed_vp']),row['vp']);close(sum(row['per_seed_win'])/n,row['win']);rows+=1
pairs={}
for k,opps in x['_paired'].items():
    base='R_final'if k.startswith('R')else'G_final';pairs[k]={}
    for opp,p in opps.items():
        a=x[k][opp]['per_seed_vp'];b=x[base][opp]['per_seed_vp'];assert len(a)==len(b)
        d=[aa-bb for aa,bb in zip(a,b)];mean=statistics.mean(d);se=statistics.stdev(d)/len(d)**.5
        close(mean,p['mean_vp_diff']);close(se,p['se']);pairs[k][opp]={'n':len(d),'mean':mean,'SE':se}

g2=Game({s:BotPolicy(s,71)for s in 'RG'},seed=71,edition=2,options={'ap_bonus_R':1})
g1=Game({s:BotPolicy(s,71)for s in 'RG'},seed=71,edition=2,options={'ap_bonus_R':1,'ap_edition':1})
assert g1.edition==g2.edition==2
assert {k:v for k,v in g1.opt.items()if k!='ap_edition'}==g2.opt
for key in ['siege_shift','siege_mp','sh_points','ia_friendly']:assert g1.opt[key]==g2.opt[key]
assert g1.ctrl==g2.ctrl and g1.ctype==g2.ctype and g1.deck==g2.deck and g1.rng.getstate()==g2.rng.getstate()
g1.active=g2.active='R'
for c in CARDS:
    assert g1.ap(c)==CARDS[c]['ap1']+1 and g2.ap(c)==CARDS[c]['ap2']+1

ap=json.loads((repo/'results/ap_only_check_v1.2.json').read_text());saved_rows=[]
for k,row in ap['results'].items():
    assert set(row['ap1'])==set(row['ap2'])=={'win'}
    assert 'vp'not in row['ap1']and'vp'not in row['ap2']
    saved_rows.append({'matchup':k,'n':row['n'],'ap1Keys':list(row['ap1']),'ap2Keys':list(row['ap2']),
                       'savedMeanDifference':row['paired_vp_diff'],'savedSE':row['se']})
result={'latestChangeCellsRecounted':rows,'latestChangePairedComparisons':pairs,
        'APOnlyScopeVerified':True,'APCardsChecked':len(CARDS),'R07':{
            'expected':'per-seed AP outcomes retained for independent paired-mean and SE recount',
            'actual':'only win-rate summaries, mean difference, SE and n are saved','rows':saved_rows}}
Path(sys.argv[2]).write_text(json.dumps(result,indent=2))
print(json.dumps({'latestChangeCells':rows,'pairedComparisons':sum(len(v)for v in pairs.values()),
                  'APOnlyScopeVerified':True,'APRawVPRetained':False}))
