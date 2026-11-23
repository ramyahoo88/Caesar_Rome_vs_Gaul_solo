"""Independent, small positions reproducing release defects. No release files are edited.
python3 focused_rules.py REPO OUTPUT_DIR
"""
import sys,json,copy
from pathlib import Path
repo=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();sys.path.insert(0,str(repo/'code'))
from engine import *
from bots import BotPolicy
from policies import BasePolicy
from heur import stack_strength,reach,path_to
findings=[]
def fresh(seed=1):
 g=Game({s:BotPolicy(s,seed)for s in 'RG'},seed=seed,log=True)
 for u in g.units.values():u.loc='hold';u.inside=False;u.moved=False
 for l in g.leaders.values():l.loc='cup';l.moved=False
 g.ctrl=[None]*N;g.ctype=[None]*N;g.siege={};g.ft_tribe={};g._pc_cache=None;g.devast=set();g.sieged_this_card=set();g.hands={'R':[],'G':[]}
 return g
def snapshot(g,name):
 d={k:getattr(g,k)for k in ['turn','ctrl','ctype','siege','ft_tribe','sieged_this_card','hands','active']}
 d['sieged_this_card']=list(d['sieged_this_card'])
 d['units']=[{k:getattr(u,k)for k in Unit.__slots__}for u in g.units.values()]
 d['leaders']=[{k:getattr(l,k)for k in Leader.__slots__}for l in g.leaders.values()]
 (out/name).write_text(json.dumps(d,indent=2))

# C01: Reserve #24 has not been revealed: Rome has not made any Offer at all.
class EventOpponent(BasePolicy):
 def choose_play(self,g,side):
  if 6 in g.hands[side]:return 6,'event'
  return next(c for c in g.hands[side] if CARDS[c]['kind']!='surprise'),'ap'
 def spend_ap(self,g,side,ap):pass
g=Game({'R':BotPolicy('R',9),'G':EventOpponent('G',9)},seed=9,log=True)
g.hands={'R':[24,45],'G':[6]};g.deck=[c for c in CARDS if c not in [24,45,6,7,8]]+[7,8];g.discard=[]
assert g.pol['R'].directive is None and g.pol['R'].reserve==[]
snapshot(g,'C01-unrevealed-reaction.json');g.card_play('G')
assert any('R cancels #6 with #24' in x for x in g.logs)
assert g.pol['R'].directive is None
findings.append({'id':'C01','expected':'Unrevealed #24 cannot be used before the first Roman Offer.','actual':'Rome cancels #6 before any Roman Directive/Offer.','log':[x for x in g.logs if 'cancel' in x]})

# C02: the Roman path is initially blocked by the Gallic army that is about to move.
g=fresh();b=g.pol['G'];u=next(u for u in g.units.values()if u.name=='Remi');u.steps=1;u.loc=IDX['Aduatuci']
r=[u for u in g.units.values()if u.kind=='legion'][:2]
for q in r:q.loc=IDX['Menapii']
t=IDX['Eburones'];g.set_ctrl(t,'R','IM');snapshot(g,'C02-danger-before-move.json')
before=b.roman_threat(g).get(t,0);plan=b.sweep(g,'G',lambda s:1 if s==t else 0)
assert before==0 and plan is not None
assert plan[2]==[('to',t),('remove_im',)]
h=copy.deepcopy(g);h.units[u.uid].loc=t;h.clear_ctrl(t)
# Independent hand-sized oracle: two Legions may move 3 MP, with the source vacated.
dist,parent=reach(h,'R',IDX['Menapii'],3,2,2)
assert t in dist;route=[IDX['Menapii']]+path_to(parent,t)
roman_bs=sum(q.strength()for q in r)+h.local_support('R',t)
gallic_bs=u.strength()+h.local_support('G',t)
assert roman_bs>=gallic_bs
findings.append({'id':'C02','from':'Aduatuci','to':'Eburones','enemy':'Menapii','chosenPlan':plan[2],'threatBefore':before,'actualRomanBS':roman_bs,'gallicBS':gallic_bs,'route':[NAMES[x]for x in route],'routeMP':dist[t]})
# Opposite control: remove one Legion, so an actual future attack is below the danger threshold.
h.units[r[1].uid].loc='hold';assert sum(x.strength()for x in h.on_map('R'))<gallic_bs

# C02b: REGROUP makes the same prospective-board mistake.
g=fresh();b=g.pol['R'];a=next(u for u in g.units.values()if u.name=='Arverni');a.loc=IDX['Menapii']
legs=[u for u in g.units.values()if u.kind=='legion'][:2];legs[0].loc=IDX['Aduatuci'];legs[1].loc=IDX['Eburones']
snapshot(g,'C02-regroup-before-move.json');calls=[];g.activate=lambda side,l,us,plan,**kw:calls.append((side,us,plan))
assert b.m_regroup(g,1)==1 and calls[0][2]==[('to',IDX['Eburones'])]
destination=IDX['Eburones'];legs[0].loc=destination
rd=sum(u.strength()for u in legs)+g.local_support('R',destination)
dist,parent=reach(g,'G',a.loc,3,2,1);assert destination in dist
attack=a.strength()+g.local_support('G',destination);assert attack>=1.5*rd
findings.append({'id':'C02b','mission':'REGROUP','from':'Aduatuci','to':'Eburones','enemy':'Menapii','gallicBS':attack,'romanBSAfterJoining':rd,'ratio':attack/rd,'route':[NAMES[a.loc]]+[NAMES[x]for x in path_to(parent,destination)]})

# C03: previously unactivated units contribute to a siege but remain available to move again.
g=fresh(11);t=IDX['Gergovia'];a=next(u for u in g.units.values()if u.name=='Arverni');a.loc=t;a.inside=True;g.set_ctrl(t,'G','FT',a.uid)
legs=[u for u in g.units.values()if u.kind=='legion'][:8]
for q in legs:q.loc=t
cz=g.leaders['Caesar'];cz.loc=t;g.roll2=lambda:2
snapshot(g,'C03-siege-contributors.json');g.activate('R',cz,legs[:6],[('siege',)])
assert g.stats['sieges']==1
assert all(q.moved for q in legs[:6]);assert not any(q.moved for q in legs[6:])
next_space=next(s for s,k in ADJ[t] if k=='path' and g.can_enter('R',s))
g.activate('R',None,legs[6:],[('to',next_space)])
assert all(q.loc==next_space for q in legs[6:])
findings.append({'id':'C03','siegeSpace':'Gergovia','contributingUnits':[q.name for q in legs],'unlockedContributors':[q.name for q in legs[6:]],'secondActivationDestination':NAMES[next_space],'sieges':g.stats['sieges']})

# C04: #42 played for AP disappears instead of entering the discard pile.
class APPlayer(BasePolicy):
 def choose_play(self,g,side):return g.hands[side][0],'ap'
 def spend_ap(self,g,side,ap):pass
for card in [42,45]:
 g=Game({'R':APPlayer('R',3),'G':APPlayer('G',3)},seed=3)
 g.hands={'R':[card],'G':[6]};g.deck=[c for c in CARDS if c not in [card,6]];g.discard=[]
 if card==42:snapshot(g,'C04-card42-for-AP.json')
 g.card_play('R');all_cards=g.deck+g.discard+g.hands['R']+g.hands['G']
 if card==42:
  assert card not in all_cards
  findings.append({'id':'C04','card':card,'mode':'ap','expected':'42 in discard','actual':'42 absent from deck, both hands and discard','totalCards':len(all_cards)})
 else:assert card in g.discard and len(all_cards)==55

# Latest Caesar siege eligibility: 2:1 is accepted even at zero existing siege points.
g=fresh(19);t=IDX['Gergovia'];a=next(u for u in g.units.values()if u.name=='Arverni');a.loc=next(s for s in PROVINCES['Arverni']['idx'] if s!=t and STYPE[s]=='town');g.set_ctrl(t,'G','FT',a.uid)
cz=g.leaders['Caesar'];cz.loc=t;legs=[u for u in g.units.values()if u.kind=='legion'][:2]
for q in legs:q.loc=t
captured=[];g.activate=lambda side,leader,units,ops,**kw:captured.append((side,leader.name if leader else None,[u.name for u in units],ops))
assert g.pol['R'].m_siege(g,1)==1 and captured[-1][1]=='Caesar'
findings.append({'control':'latest Caesar 2:1 eligibility','accepted':True,'plan':captured[-1]})

(out/'focused-rules-results.json').write_text(json.dumps(findings,indent=2));print(json.dumps(findings,indent=2))
