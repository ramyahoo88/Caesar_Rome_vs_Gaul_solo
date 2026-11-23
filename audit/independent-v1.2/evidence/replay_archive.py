"""Replay a prefix of every archived final-study cell on the shipped engine.
python3 replay_archive.py REPO OUTPUT [PREFIX=3]
Also observe Reserve edge cases without changing policy decisions.
"""
import sys,json,re,copy,time
from pathlib import Path
from multiprocessing import Pool
repo=Path(sys.argv[1]).resolve();sys.path.insert(0,str(repo/'code'))
from engine import Game,CARDS
from harness import make
from study import IMP_LEVELS,CON_LEVELS,OPPS

class ObservedGame(Game):
    def __init__(self,*a,**kw):
        self.reserve_redraws=[];self.partial_replacements=[];self.replacement_draws=None
        self.missed_cleanup=[];self.audit_depth=0
        super().__init__(*a,**kw)
    def card_play(self,side):
        p=self.pol[side]
        if (getattr(p,'_reserve_turn',None)==self.turn and 55 in getattr(p,'reserve',())
            and 55 in self.hands[side] and any(CARDS[c]['kind']!='surprise'for c in self.hands[side])):
            self.missed_cleanup.append({'turn':self.turn,'side':side,'depth':self.audit_depth,
                                        'handBeforeOffer':list(self.hands[side])})
        self.audit_depth+=1
        try:return super().card_play(side)
        finally:self.audit_depth-=1
    def draw(self,side,n):
        p=self.pol[side]
        stale=set(getattr(p,'reserve',()))-set(self.hands[side]) if getattr(p,'_reserve_turn',None)==self.turn else set()
        if self.replacement_draws is not None:self.replacement_draws+=n
        super().draw(side,n)
        hit=stale & set(self.hands[side])
        if hit:self.reserve_redraws.append({'turn':self.turn,'side':side,'cards':sorted(hit)})
    def handle_surprises_start(self,side):
        h=list(self.hands[side]);p=self.pol[side]
        all_reserve=bool(h) and all(CARDS[c]['kind']=='surprise'for c in h) and getattr(p,'_reserve_turn',None)==self.turn and set(h)<=set(getattr(p,'reserve',()))
        self.replacement_draws=0
        try:super().handle_surprises_start(side)
        finally:
            if all_reserve and self.replacement_draws!=len(h):
                self.partial_replacements.append({'turn':self.turn,'side':side,'hand':h,'replacements':self.replacement_draws})
            self.replacement_draws=None

def one(task):
    key,seed,rspec,gspec,opt,expected=task
    g=ObservedGame({'R':make(rspec,'R',seed),'G':make(gspec,'G',seed)},seed=seed,options=opt)
    r=g.play();actual=[r['vp'],r['reason'],r['stats']['battles'],r['stats']['sieges']]
    allc=g.deck+g.discard+g.hands['R']+g.hands['G'];assert sorted(allc)==list(range(1,56))
    return {'cell':key,'seed':seed,'expected':expected,'actual':actual,'matches':actual==expected,
            'reserveRedraws':g.reserve_redraws,'partialReserveReplacements':g.partial_replacements,
            'missedForcedMarchCleanup':g.missed_cleanup}

if __name__=='__main__':
    prefix=int(sys.argv[3])if len(sys.argv)>3 else 3
    data=json.loads((repo/'results/study_final.json').read_text());tasks=[]
    for key,c in data.items():
        m=re.fullmatch(r'(Imperator|Concilium) L([1-5]) vs (.*)',key);side,lv,opp=m.group(1),int(m.group(2)),m.group(3)
        opt=copy.deepcopy((IMP_LEVELS if side=='Imperator'else CON_LEVELS)[lv])
        if side=='Imperator':rs,gs=('bot',{}),OPPS[opp];seedbase=100000
        else:
            rs,gs=OPPS[opp],('bot',{});seedbase=200000
            if opp=='bot':opt['ap_bonus_R']=1
        for i in range(min(prefix,c['n'])):
            tasks.append((key,seedbase+i,rs,gs,opt,[c['vp'][i],c['reasons'][i],c['battles'][i],c['sieges'][i]]))
    start=time.time()
    with Pool(4)as p:records=p.map(one,tasks,chunksize=1)
    result={'commit':__import__('subprocess').check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),
            'prefixPerCell':prefix,'records':records,'seconds':time.time()-start}
    Path(sys.argv[2]).write_text(json.dumps(result,indent=2))
    mismatches=[r for r in records if not r['matches']]
    print(json.dumps({'replays':len(records),'cells':len(data),'mismatches':len(mismatches),
                      'runsWithPartialReplacement':sum(bool(r['partialReserveReplacements'])for r in records),
                      'runsWithReserveRedraw':sum(bool(r['reserveRedraws'])for r in records),'seconds':result['seconds']}))
    assert not mismatches,mismatches[:3]
