"""v1.1 re-audit: strict card conservation plus independent unit and score accounting.
Run: python3 campaign_audit.py REPO OUTPUT [N_PER_LEVEL=20]
"""
import sys,json,time,traceback,hashlib,copy
from pathlib import Path
from collections import Counter
from multiprocessing import Pool
repo=Path(sys.argv[1]).resolve();sys.path.insert(0,str(repo/'code'))
from engine import Game,N,CARDS,REGION,OTHER
from bots import BotPolicy
from harness import make
from replay_archive import ObservedGame

class CheckedGame(ObservedGame):
 def __init__(self,*a,**kw):
  self.checks=0;self.depth=0;self.hidden_checks=0;self.decisions=[];self.card_issues=[];self.was_missing=False
  super().__init__(*a,**kw)
 def check(self):
  cards=self.deck+self.discard+self.hands['R']+self.hands['G']
  if self.winner is None:
   counts=Counter(cards);missing=set(range(1,56))-set(cards);assert all(n==1 for n in counts.values());assert not(set(cards)-set(range(1,56)));assert not missing,('unexpected card loss',missing)
   if missing and not self.was_missing:self.card_issues.append({'turn':self.turn,'active':self.active,'missing':sorted(missing)})
   self.was_missing=bool(missing)
  for u in self.units.values():
   assert 0<=u.steps<=u.maxsteps,('steps',repr(u))
   if isinstance(u.loc,int):assert 0<=u.loc<N and u.steps>0,('location',repr(u))
   if isinstance(u.loc,int) and u.inside:assert self.fort_owner(u.loc)==u.side,('orphan shelter',repr(u))
  assert len(self.elim_legions)==len(set(self.elim_legions))
  assert len(self.elim_tribes)==len(set(self.elim_tribes))
  assert self.vp==sum(x[1] for x in self.vp_log),('VP ledger',self.vp,self.vp_log)
  self.checks+=1
 def card_play(self,side):
  self.depth+=1
  try:return super().card_play(side)
  finally:
   self.depth-=1
   if self.depth==0:self.check()

def one(task):
 label,opt,seed,rkind,gkind=task
 g=CheckedGame({'R':make((rkind,{}),'R',seed),'G':make((gkind,{}),'G',seed)},seed=seed,options=opt)
 error=None;r=None
 try:r=g.play();g.check();assert sorted(g.deck+g.discard+g.hands['R']+g.hands['G'])==list(range(1,56));assert r['winner'] in 'RG';assert r['reason']
 except Exception:error=traceback.format_exc()
 return dict(label=label,options=opt,seed=seed,result=r,error=error,checks=g.checks,card_issues=g.card_issues,reserveRedraws=g.reserve_redraws,partialReserveReplacements=g.partial_replacements)

if __name__=='__main__':
 out=Path(sys.argv[2]);n=int(sys.argv[3]) if len(sys.argv)>3 else 20
 imp={1:{},2:{'ap_first_R':4},3:{'ap_bonus_R':1},4:{'ap_bonus_R':1,'vp_target':10},5:{'ap_bonus_R':1,'vp_target':9}}
 con={1:{'vp_target':9},2:{'vp_target':10},3:{'vp_target':11},4:{},5:{'ap_first_G':4}}
 tasks=[]
 for level,opt in imp.items():tasks += [(f'Imperator L{level}',opt,810000+i,'bot','bot')for i in range(n)]
 for level,opt in con.items():tasks += [(f'Concilium L{level}',dict(opt,ap_bonus_R=1),820000+i,'bot','bot')for i in range(n)]
 # Independent purposeful opponents on both sides; these receive the normal level-three setup.
 for side in ['R','G']:
  tasks += [(f'L3 vs heuristic, bot {side}',{'ap_bonus_R':1} if side=='R' else {'vp_target':11},830000+i,'bot' if side=='R' else 'smart','smart' if side=='R' else 'bot')for i in range(20)]
 started=time.time()
 with Pool(4) as p:records=p.map(one,tasks,chunksize=2)
 result={'commit':__import__('subprocess').check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),'seconds':time.time()-started,'records':records}
 out.write_text(json.dumps(result,indent=2))
 print(json.dumps({'games':len(records),'checks':sum(r['checks']for r in records),'errors':sum(bool(r['error'])for r in records),'seconds':result['seconds']}))
 errors=[r for r in records if r['error']]
 for r in errors[:5]:print(r['label'],r['seed'],r['error'].splitlines()[-1])
 print('games with missing card 42',sum(bool(r['card_issues'])for r in records))

 print('games with partial Reserve replacements',sum(bool(r['partialReserveReplacements'])for r in records))
 print('games with immediate Reserve redraws',sum(bool(r['reserveRedraws'])for r in records))
