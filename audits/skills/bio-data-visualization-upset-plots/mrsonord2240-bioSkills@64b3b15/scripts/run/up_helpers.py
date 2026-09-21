"""Helpers: independent set-operation truth + extraction of what upsetplot actually drew (matplotlib artists)."""
import itertools
import numpy as np
from matplotlib.colors import to_hex

def read_sets(path):
    sets = {}
    for i, line in enumerate(open(path, encoding='utf-8')):
        if i == 0:
            continue
        s, g = line.rstrip('\n').split('\t')
        sets.setdefault(s, []).append(g)
    return sets

def truth(sets):
    """{combo(tuple sorted by set order): (exclusive, inclusive)} for every non-empty combination, from set operations only."""
    names = list(sets)
    S = {n: set(v) for n, v in sets.items()}
    out = {}
    for k in range(1, len(names) + 1):
        for combo in itertools.combinations(names, k):
            inter = set.intersection(*[S[c] for c in combo])
            others = [S[n] for n in names if n not in combo]
            excl = inter - (set.union(*others) if others else set())
            if inter:
                out[combo] = (len(excl), len(inter))
    return out

def extract(ax, row_labels=None):
    """From the dict returned by UpSet.plot(): per-column membership, bar height, count label, bar colour; per-row totals."""
    inter = ax['intersections']; mat = ax['matrix']
    bars = sorted(inter.patches, key=lambda p: p.get_x())
    heights = [float(p.get_height()) for p in bars]
    bar_cols = [to_hex(p.get_facecolor()) for p in bars]
    labels = [t.get_text() for t in sorted(inter.texts, key=lambda t: t.get_position()[0])]
    rows = [t.get_text() for t in mat.get_yticklabels()]
    pc = [c for c in mat.collections if type(c).__name__ == 'PathCollection'][0]
    offs = pc.get_offsets(); fc = pc.get_facecolors()
    cols = {}
    for (x, y), c in zip(offs, fc):
        cols.setdefault(int(round(x)), []).append((int(round(y)), c))
    members, dot_cols = [], []
    for x in sorted(cols):
        pres = [(y, c) for y, c in cols[x] if c[3] > 0.9]
        members.append(tuple(rows[y] for y, _ in sorted(pres)))
        dot_cols.append(to_hex(pres[0][1][:3]) if pres else None)
    tot_patches = ax['totals'].patches
    totals = {}
    # totals bars are horizontal: one per row, y position tells the row
    for p in tot_patches:
        y = int(round(p.get_y() + p.get_height() / 2))
        totals[rows[y]] = float(abs(p.get_width()))
    return dict(heights=heights, bar_colors=bar_cols, labels=labels, members=members, dot_colors=dot_cols, rows=rows, totals=totals)
