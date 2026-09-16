# Residue-pair confidence for P01 residue 142 across the 16-replicate MUSCLE5 stratified ensemble,
# exactly as SKILL.md defines it: fraction of replicates placing the residue pair in the same column.
def read_efa(path):
    reps = []
    for block in open(path).read().split('<')[1:]:
        name, *rest = block.split('\n', 1)
        seqs = {}
        for rec in rest[0].split('>')[1:]:
            h, *lines = rec.split('\n'); seqs[h.strip()] = ''.join(lines)
        reps.append((name, seqs))
    return reps
def partner(seqs, sid, k, other):  # which residue index of `other` shares a column with residue k of sid
    s = seqs[sid]; n = -1
    for j, c in enumerate(s):
        if c != '-':
            n += 1
            if n == k:
                o = seqs[other]
                return None if o[j] == '-' else len(o[:j].replace('-', ''))
reps = read_efa('ens.efa')
print('replicates:', len(reps), [r[0] for r in reps][:4], '...')
for k in (141, 60, 250):
    confs = []
    for other in sorted(reps[0][1]):
        if other == 'P01': continue
        calls = [partner(s, 'P01', k, other) for _, s in reps]
        top = max(set(calls), key=calls.count)
        confs.append(calls.count(top) / len(calls))
    print(f'P01 residue {k+1}: mean pair confidence {sum(confs)/len(confs):.2f}; min {min(confs):.2f}')
# scan every P01 residue to show where the ensemble is uncertain
L = len(reps[0][1]['P01'].replace('-', ''))
low = []
for k in range(L):
    confs = []
    for other in sorted(reps[0][1]):
        if other == 'P01': continue
        calls = [partner(s, 'P01', k, other) for _, s in reps]
        confs.append(max(calls.count(c) for c in set(calls)) / len(calls))
    m = sum(confs) / len(confs)
    if m < 0.8: low.append((k + 1, round(m, 2)))
print(f'P01 residues with mean pair confidence < 0.8: {len(low)}/{L}:', low[:12], '...' if len(low) > 12 else '')
