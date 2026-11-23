"""Replay two seeds from every latest-change experiment cell.
python3 replay_latest.py REPO OUTPUT
Reads literal configurations via AST; importing latest.py would run its full study.
"""
import sys,ast,json,time
from pathlib import Path
from multiprocessing import Pool
repo=Path(sys.argv[1]).resolve();sys.path.insert(0,str(repo/'code'))
from engine import Game
from harness import make

def one(task):
    label,opp,seed,rs,gs,opt,side,expected=task
    g=Game({'R':make(rs,'R',seed),'G':make(gs,'G',seed)},seed=seed,options=opt)
    r=g.play();actual=[r['vp'],r['winner']==side]
    assert sorted(g.deck+g.discard+g.hands['R']+g.hands['G'])==list(range(1,56))
    return {'variant':label,'opponent':opp,'seed':seed,'expected':expected,'actual':actual,'matches':actual==expected}

if __name__=='__main__':
    conf={}
    for node in ast.parse((repo/'code/latest.py').read_text()).body:
        if isinstance(node,ast.Assign):
            for t in node.targets:
                if isinstance(t,ast.Name)and t.id in ['R_VARS','G_VARS']:conf[t.id]=ast.literal_eval(node.value)
    data=json.loads((repo/'results/latest_changes_v1.3.json').read_text());tasks=[]
    for label,rows in data.items():
        if label.startswith('_'):continue
        for opp,row in rows.items():
            if label in conf['R_VARS']:rs,gs,opt,side=('bot',conf['R_VARS'][label]),(opp,{}),{'ap_bonus_R':1},'R'
            else:rs,gs,opt,side=(opp,{}),('bot',conf['G_VARS'][label]),({'ap_bonus_R':1}if opp=='bot'else{}),'G'
            for i in range(2):tasks.append((label,opp,20000+i,rs,gs,opt,side,[row['per_seed_vp'][i],row['per_seed_win'][i]]))
    t=time.time()
    with Pool(4)as p:records=p.map(one,tasks,chunksize=1)
    Path(sys.argv[2]).write_text(json.dumps({'records':records,'seconds':time.time()-t},indent=2))
    assert all(r['matches']for r in records)
    print(json.dumps({'replays':len(records),'cells':18,'allMatch':True,'seconds':time.time()-t}))
