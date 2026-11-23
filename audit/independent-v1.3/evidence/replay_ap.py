"""Replay a prefix of every AP-only setting from the artifact's saved metadata.
python3 replay_ap.py REPO OUTPUT [PREFIX=3]
"""
import sys, json, time
from pathlib import Path
from multiprocessing import Pool
repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / 'code'))
from engine import Game
from harness import make


def one(task):
    name, lab, seed, settings, expected = task
    opt = dict(settings['options'])
    if lab == 'ap1':
        opt.update(settings['ap1_extra'])
    g = Game({s: make(settings[key], s, seed) for s, key in [('R', 'roman'), ('G', 'gallic')]},
             seed=seed, edition=settings['edition'], options=opt)
    r = g.play()
    actual = [r['vp'], r['winner'], r['reason']]
    assert sorted(g.deck + g.discard + g.hands['R'] + g.hands['G']) == list(range(1, 56))
    return dict(matchup=name, AP=lab, seed=seed, expected=expected, actual=actual,
                matches=actual == expected)


if __name__ == '__main__':
    data = json.loads((repo / 'results/ap_only_check_v1.3.json').read_text())
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    tasks = []
    for name, row in data['results'].items():
        for lab in ['ap1', 'ap2']:
            for i in range(min(n, row['n'])):
                v = row[lab]
                tasks.append((name, lab, row['seeds'][0] + i, row['settings'],
                              [v['vp'][i], v['winner'][i], v['reason'][i]]))
    t = time.time()
    with Pool(4) as pool:
        records = pool.map(one, tasks, chunksize=1)
    Path(sys.argv[2]).write_text(json.dumps(dict(records=records, seconds=time.time() - t), indent=2))
    assert all(r['matches'] for r in records)
    print(json.dumps(dict(replays=len(records), settings=6, allMatch=True, seconds=time.time() - t)))
