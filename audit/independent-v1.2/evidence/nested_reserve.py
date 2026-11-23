"""New v1.2 timing cases plus a fresh full-game observation sweep.
python3 nested_reserve.py REPO OUTPUT_DIR [PROBE_GAMES=100]
Assertions reproduce the remaining defect; no production code is edited.
"""
import sys,json,time
from pathlib import Path
from multiprocessing import Pool
repo=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(repo/'code'))
from engine import Game,CARDS
from bots import BotPolicy
from replay_archive import ObservedGame

class TraceBot(BotPolicy):
    def __init__(self,*a,**kw):super().__init__(*a,**kw);self.frames=[]
    def choose_play(self,g,side):
        before=list(g.hands[side]);r=super().choose_play(g,side)
        self.frames.append({'handBeforeOffer':before,'chosen':list(r),'reserveAfterOffer':sorted(self.reserve)})
        return r

def probe(seed):
    g=ObservedGame({s:BotPolicy(s,seed)for s in 'RG'},seed=seed,options={'ap_bonus_R':1})
    r=g.play();assert sorted(g.deck+g.discard+g.hands['R']+g.hands['G'])==list(range(1,56))
    return {'seed':seed,'result':r,'missedForcedMarchCleanup':g.missed_cleanup}

if __name__=='__main__':
    fixtures=[]
    for trigger in [42,21]:
        p=TraceBot('G',0);r=TraceBot('R',0);g=Game({'G':p,'R':r},seed=0,log=True)
        rh=[6,45]if trigger==42 else[24,45]
        g.hands={'R':rh,'G':[55,trigger,47]}
        g.deck=[c for c in CARDS if c not in rh+[55,trigger,47]];g.discard=[]
        if trigger==21:r.reserve={24};r._reserve_turn=g.turn
        g.handle_surprises_start('G')       # ordinary entry path; unrevealed #55 stays
        assert 55 not in p.reserve
        g.card_play('G')
        assert p.frames[0]['chosen']==[trigger,'event']and 55 in p.frames[0]['reserveAfterOffer']
        assert len(p.frames)>=2 and 55 in p.frames[1]['handBeforeOffer']
        assert 55 in g.hands['G']and 55 not in g.discard
        assert sorted(g.deck+g.discard+g.hands['R']+g.hands['G'])==list(range(1,56))
        fixtures.append({'id':'R06','seed':0,'trigger':trigger,'romanInitialHand':rh,
                         'gallicInitialHand':[55,trigger,47],'romanReserveInitially':[24]if trigger==21 else[],
                         'expected55DiscardedBeforeSecondOffer':True,'actual55DiscardedBeforeSecondOffer':False,
                         'frames':p.frames,'gallicHandAfter':g.hands['G'],'log':g.logs})
    # Opposite control: the normal strategy-loop start correctly expires a revealed #55.
    g=Game({s:BotPolicy(s,0)for s in 'RG'},seed=0);g.hands={'G':[55,47],'R':[45]}
    g.deck=[c for c in CARDS if c not in [55,47,45]];g.discard=[]
    g.pol['G'].reserve={55};g.pol['G']._reserve_turn=g.turn
    g.handle_surprises_start('G');assert 55 not in g.hands['G']and 55 in g.discard
    (out/'nested-reserve-fixtures.json').write_text(json.dumps(fixtures,indent=2))
    n=int(sys.argv[3])if len(sys.argv)>3 else 100;t=time.time()
    with Pool(4)as pool:records=pool.map(probe,range(950000,950000+n))
    result={'fixtures':fixtures,'probeGames':n,'probeRecords':records,'seconds':time.time()-t,
            'affectedProbeGames':sum(bool(r['missedForcedMarchCleanup'])for r in records)}
    (out/'nested-reserve-results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({'fixtures':len(fixtures),'probeGames':n,'affectedProbeGames':result['affectedProbeGames'],'seconds':result['seconds']}))
