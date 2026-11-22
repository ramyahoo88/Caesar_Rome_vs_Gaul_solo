"""Build the Simulation Report tables and charts from the final study JSON.
Usage: python3 make_report.py results_final/study.json out_dir"""
import json, sys, os, statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

src, out = sys.argv[1], sys.argv[2]
R = json.load(open(src))
OPPS = ['bot', 'smart', 'smart-aggressive', 'search']
LAB = {'bot': 'Bot', 'smart': 'Heuristic', 'smart-aggressive': 'Heuristic (aggressive)', 'search': 'Lookahead'}
COL = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100']
MARK = ['o', 's', '^', 'D']


def cell(k):
    r = R.get(k)
    if not r:
        return None
    n = r['n']; w = r['bot_wins']
    p = w / n
    se = (p * (1 - p) / n) ** 0.5
    return p, se, statistics.mean(r['vp']), n


def table(side):
    rows = ['| Level | ' + ' | '.join(LAB[o] for o in OPPS) + ' |', '|---|' + '---|' * len(OPPS)]
    for lvl in range(1, 6):
        cells = []
        for o in OPPS:
            c = cell(f'{side} L{lvl} vs {o}')
            cells.append('—' if c is None else f'{c[0]:.0%} ({c[2]:.1f} VP)')
        rows.append(f'| {lvl} | ' + ' | '.join(cells) + ' |')
    return '\n'.join(rows)


def chart(side, fname, ylabel):
    fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=200)
    lab = dict(LAB, bot='Concilium bot' if side == 'Imperator' else 'Imperator bot (+1 AP)')
    ends = []
    for i, o in enumerate(OPPS):
        xs, ys, es = [], [], []
        for lvl in range(1, 6):
            c = cell(f'{side} L{lvl} vs {o}')
            if c:
                xs.append(lvl); ys.append(100 * c[0]); es.append(100 * c[1])
        if not xs:
            continue
        ax.errorbar(xs, ys, yerr=es, color=COL[i], marker=MARK[i], markersize=6, linewidth=2, capsize=3,
                    label=f'vs {lab[o]}')
        ends.append([ys[-1], lab[o], xs[-1]])
    # direct labels at the line ends, pushed apart so they never overlap
    ends.sort(reverse=True)
    ends[0][0] = min(ends[0][0], 101)
    for j in range(1, len(ends)):
        if ends[j - 1][0] - ends[j][0] < 6:
            ends[j][0] = ends[j - 1][0] - 6
    for y, name, x in ends:
        ax.annotate(name, (x, y), xytext=(8, 0), textcoords='offset points', va='center', fontsize=7, color='#52514e')
    ax.set_xticks(range(1, 6)); ax.set_xlim(0.7, 6.3); ax.set_ylim(0, 105)
    ax.set_xlabel('Level'); ax.set_ylabel(ylabel)
    ax.grid(axis='y', color='#e6e5e0', linewidth=0.8); ax.set_axisbelow(True)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_color('#b5b3ad')
    ax.tick_params(colors='#52514e', labelsize=8)
    ax.legend(fontsize=7, frameon=False, loc='upper left' if side == 'Imperator' else 'lower right')
    fig.tight_layout()
    fig.savefig(os.path.join(out, fname))
    plt.close(fig)


os.makedirs(out, exist_ok=True)
chart('Imperator', 'imperator_levels.png', 'Imperator (Rome) wins, %')
chart('Concilium', 'concilium_levels.png', 'Concilium (Gaul) wins, %')
open(os.path.join(out, 'tables.md'), 'w').write(
    '### Imperator\n\n' + table('Imperator') + '\n\n### Concilium\n\n' + table('Concilium') + '\n')
print(open(os.path.join(out, 'tables.md')).read())
