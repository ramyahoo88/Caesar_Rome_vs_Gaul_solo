"""Reconcile evidence, test the latest Control Table, and check deterministic/nonprivate decisions.
python3 release_checks.py REPO OUTPUT
"""
import sys,copy,random,json,hashlib,subprocess
from pathlib import Path
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]);sys.path.insert(0,str(root/'code'))
from engine import *
from bots import BotPolicy

class AuditBot(BotPolicy):
 def __init__(self,*a,**kw):super().__init__(*a,**kw);self.hidden_checks=0
 def choose_play(self,g,side):
  clone=object.__new__(BotPolicy);clone.__dict__=copy.deepcopy({k:v for k,v in self.__dict__.items()if k!='g_ref'})
  h=copy.copy(g);h.hands=dict(g.hands);h.hands[OTHER[side]]=[55]*len(g.hands[OTHER[side]])
  h.deck=list(reversed(g.deck));h.rng=random.Random(987654);h.logging=False
  other=BotPolicy.choose_play(clone,h,side);actual=super().choose_play(g,side)
  assert other==actual,('hidden-card dependency',g.seed,g.turn,side,other,actual)
  self.hidden_checks+=1;return actual

if __name__=='__main__':
 results={};stud=json.loads((root/'results/study_final.json').read_text());assert len(stud)==40
 assert sum(c['n']for c in stud.values())==5300
 for key,c in stud.items():
  assert len(c['vp'])==len(c['reasons'])==len(c['battles'])==len(c['sieges'])==c['n']
  target=(9 if 'L1 'in key else 10 if 'L2 'in key else 11 if 'L3 'in key else 12)if key.startswith('Concilium')else(10 if 'L4 'in key else 9 if 'L5 'in key else 12)
  roman=sum(reason.startswith('automatic') or (reason.startswith('end') and vp>=target)for vp,reason in zip(c['vp'],c['reasons']))
  # Determine exact terminal wording before relying on the score arithmetic.
  assert all(reason.startswith(('automatic','end','governance'))for reason in c['reasons'])
  wins=c['n']-roman if key.startswith('Concilium')else roman
  assert wins==c['bot_wins'],(key,wins,c['bot_wins'])
 results['archive']={'cells':40,'games':5300,'allCountsReconciled':True}

 # Text-derived region preference for equal Convert candidates. Both candidates are in Gallic provinces.
 cases=[(1,2,2,1,'Celtica'),(2,1,1,2,'Belgica'),(1,3,1,2,'Belgica'),(1,2,1,3,'Celtica'),(1,2,1,2,'Celtica'),(2,1,2,1,'Celtica'),(2,2,2,2,'Celtica'),(2,2,2,1,'Celtica'),(2,1,2,2,'Belgica')]
 got=[]
 for cr,cg,br,bg,want in cases:
  g=Game({s:BotPolicy(s,1)for s in 'RG'},seed=1);g.ctrl=[None]*N;g.ctype=[None]*N;g._pc_cache=None
  for u in g.units.values():u.loc='hold';u.inside=False;u.moved=False
  selected={}
  for reg,rn,gn in [('Celtica',cr,cg),('Belgica',br,bg)]:
   ps=REG_PROVS[reg]
   for j,p in enumerate(ps[:rn+gn]):
    for s in PROVINCES[p]['idx']:g.set_ctrl(s,'R'if j<rn else'G','IM')
   selected[reg]=PROVINCES[ps[rn]]['idx'][0]
  g.set_ctrl(IDX['Burdigala'],'R','IM');legs=[u for u in g.units.values()if u.kind=='legion'][:2]
  for u,t in zip(legs,selected.values()):u.loc=t
  opts=[('convert',s)for s in selected.values()];assert all(g.can_convert('R',s)for k,s in opts)
  a=g.pol['R'].roman_control_choice(g,opts);assert REGION[a[1]]==want
  got.append({'Celtica':[cr,cg],'Belgica':[br,bg],'expected':want,'actual':REGION[a[1]]})
 results['laggingRegionCases']=got

 rec=[]
 for seed in range(1040000,1040012):
  p={s:AuditBot(s,seed)for s in 'RG'};g=Game(p,seed=seed,options={'ap_bonus_R':1});r=g.play()
  rec.append({'seed':seed,'winner':r['winner'],'vp':r['vp'],'hiddenComparisons':sum(b.hidden_checks for b in p.values())})
 results['hiddenInformation']=rec

 deterministic=[]
 for seed in range(1040020,1040024):
  outputs=[]
  for target in [12,12,10]:
   g=Game({s:BotPolicy(s,seed)for s in 'RG'},seed=seed,log=True,options={'ap_bonus_R':1,'vp_target':target});r=g.play()
   outputs.append((r,hashlib.sha256('\n'.join(g.logs).encode()).hexdigest()))
  assert outputs[0]==outputs[1]
  assert outputs[0][1]==outputs[2][1] and outputs[0][0]['vp']==outputs[2][0]['vp']
  deterministic.append({'seed':seed,'trace_sha256':outputs[0][1],'sameSeedExact':True,'targetDoesNotChangePlay':True})
 results['deterministic']=deterministic
 out.write_text(json.dumps(results,indent=2));print(json.dumps({'archiveGames':5300,'regionCases':len(got),'hiddenGames':len(rec),'hiddenComparisons':sum(r['hiddenComparisons']for r in rec),'determinismCases':len(deterministic)}))
