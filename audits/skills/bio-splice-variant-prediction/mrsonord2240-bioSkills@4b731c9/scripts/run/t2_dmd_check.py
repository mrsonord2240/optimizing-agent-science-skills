import re
def best(path):
    d = {}
    for l in open(path):
        if l.startswith('#'): continue
        c = l.rstrip('\n').split('\t'); m = re.search(r'Pangolin=([^;\t]+)', c[7])
        v = [(float(b), int(a)) for g in (m.group(1).split(',') if m else []) for x in g.split('|')[1:] if re.fullmatch(r'-?\d+:-?[\d.e-]+', x) for a, b in [x.split(':')]]
        loss = min([t for t in v if t[0] < 0], default=(0.0, None))
        d[c[2]] = loss
    return d
R = {(db, m): best(f'out/dmd_{db}_m{m}.vcf') for db in ['canon', 'all'] for m in ['False', 'True']}
print(f"{'variant':48s} mF/canon   mT/canon   mF/all     mT/all")
alt_erased = alt_kept_all = 0; alt_n = 0; can_kept = can_n = 0
for vid in R[('canon', 'False')]:
    row = [R[k][vid][0] for k in [('canon', 'False'), ('canon', 'True'), ('all', 'False'), ('all', 'True')]]
    print(f'{vid:48s}', '  '.join(f'{x:+.2f}    ' for x in row))
    if 'altonly' in vid:
        alt_n += 1; alt_erased += abs(row[1]) < 0.005 and row[0] < -0.2; alt_kept_all += row[3] < -0.2 and abs(row[3] - row[2]) < 0.03
    else:
        can_n += 1; can_kept += row[1] < -0.2
print(f'alt-only sites: {alt_n}; loss present at mask False AND erased at mask True/canonical DB: {alt_erased}; kept with all-transcript DB: {alt_kept_all}')
print(f'canonical sites: {can_n}; loss kept at mask True/canonical: {can_kept}')
