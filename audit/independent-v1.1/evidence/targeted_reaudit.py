"""Independent additional states for Caesar solo v1.1, dcbfc22.
These assertions reproduce remaining defects; they should change after fixes.
python3 targeted_reaudit.py REPO OUTPUT_DIR
"""
import sys, json
from pathlib import Path
repo=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(repo/'code'))
from engine import Game, N, IDX, NAMES, ADJ, CARDS, PROV, PROVINCES
from bots import BotPolicy

def fresh(seed):
    g=Game({s:BotPolicy(s,seed)for s in 'RG'},seed=seed,log=True)
    for u in g.units.values():u.loc='hold';u.inside=False;u.moved=False
    for l in g.leaders.values():l.loc='cup';l.moved=False
    g.ctrl=[None]*N;g.ctype=[None]*N;g.siege={};g.ft_tribe={};g._pc_cache=None
    g.devast=set();g.sieged_this_card=set();return g

results=[]
# R01: all cards are already face-up Reserve Surprises. Both must be replaced.
g=fresh(9);g.hands={'R':[52,54],'G':[45]};g.deck=[7,6]
g.discard=[c for c in CARDS if c not in [52,54,45,7,6]]
p=g.pol['R'];p.reserve={52,54};p._reserve_turn=g.turn
assert len(g.deck+g.discard+g.hands['R']+g.hands['G'])==55
g.handle_surprises_start('R')
assert g.hands['R']==[54,6] and g.deck==[7]
results.append({'id':'R01','seed':9,'initialHand':[52,54],'initialReserve':[52,54],
                'deckTopFirst':[6,7],'expectedHand':[6,7],'actualHand':g.hands['R'],
                'expectedReplacementCount':2,'actualReplacementCount':1})

# Single-card opposite control: no mutation-of-loop-length problem.
g=fresh(9);g.hands={'R':[52],'G':[45]};g.deck=[7,6]
g.discard=[c for c in CARDS if c not in [52,45,7,6]]
g.pol['R'].reserve={52};g.pol['R']._reserve_turn=g.turn
g.handle_surprises_start('R');assert g.hands['R']==[6]

# R02: using #52 at a real siege and immediately drawing it back must not reveal the new draw.
g=fresh(94);g.hands={'R':[52,45],'G':[6,7,8,9,10,11,12,13]};g.deck=[]
g.discard=[c for c in CARDS if c not in g.hands['R']+g.hands['G']]
p=g.pol['R'];p.reserve={52};p._reserve_turn=g.turn
t=IDX['Gergovia'];a=next(u for u in g.units.values()if u.name=='Arverni');a.loc=t;a.inside=True
g.set_ctrl(t,'G','FT',a.uid);legs=[u for u in g.units.values()if u.kind=='legion'][:6]
for u in legs:u.loc=t
cz=g.leaders['Caesar'];cz.loc=t;g.roll2=lambda:2
assert g.siege_roll('R',t,cz,legs,caesar=True)
assert g.hands['R']==[45,52]
assert p.use_vow_siege(g,t) is True
assert len(g.deck+g.discard+g.hands['R']+g.hands['G'])==55
results.append({'id':'R02','seed':94,'operation':'siege at Gergovia with Caesar and six full Legions vs Arverni inside',
                'initialHand':[52,45],'initialReserve':[52],'drawPileInitiallyEmpty':True,
                'handAfterUseAndReplacement':g.hands['R'],'reserveAfterUseAndReplacement':sorted(p.reserve),
                'newOfferOccurred':False,'expectedUseVowAgain':False,'actualUseVowAgain':p.use_vow_siege(g,t)})

# R03: a named Gallic leader is itself a CS-1 CU and can threaten with local support.
g=fresh(31);g.turn=5;t=IDX['Bibracte'];start=next(s for s,k in ADJ[t]if k=='path')
v=next(u for u in g.units.values()if u.name=='Vercingetorix');v.loc=start
leg=next(u for u in g.units.values()if u.kind=='legion');leg.loc=t
for s in PROVINCES[PROV[t]]['idx']:
    if s!=t:g.set_ctrl(s,'G','IM')
assert g.local_support('G',t)==2 and g.local_support('R',t)==0
p=g.pol['R'];formed=p.gallic_armies(g)
assert any(l is v and us==[] for l,us,s in formed)
assert p.threat_armies(g,'G')==[]
observed=p.in_danger(g,'R',t,[],p.threat_after_move(g,'G',p.threat_armies(g,'G'),[],None))
assert observed is False
assert 1+2>=1.5*leg.strength()
results.append({'id':'R03','seed':31,'turn':5,'gallicLeader':v.name,'leaderOrigin':NAMES[start],
                'target':NAMES[t],'gallicControlledProvince':PROV[t],'gallicCS':1,'gallicLocalSupport':2,
                'romanCS':leg.strength(),'romanLocalSupport':0,'route':[NAMES[start],NAMES[t]],'routeMP':1,
                'expectedDanger':True,'actualDanger':observed,'formationIncludesLeaderOnlyArmy':True})
g.ctrl=[None]*N;g.ctype=[None]*N;g._pc_cache=None
assert g.local_support('G',t)==0 and 1<1.5*leg.strength()

# R05: this release's AP sensitivity script changes four other rule parameters.
opts=[]
for ed in (1,2):
    g=Game({s:BotPolicy(s,1)for s in 'RG'},seed=1,edition=ed)
    opts.append(g.opt)
diff={k:{'edition1':opts[0][k],'edition2':opts[1][k]}for k in opts[0]if opts[0][k]!=opts[1][k]}
assert set(diff)=={'siege_shift','siege_mp','sh_points','ia_friendly'}
script=(repo/'code/ed1b.py').read_text();assert 'edition=ed' in script
results.append({'id':'R05','expected':'AP-value-only comparison keeps all other rules fixed',
                'actualNonAPRuleDifferences':diff,'sourceScript':'code/ed1b.py'})

(out/'targeted-results.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
