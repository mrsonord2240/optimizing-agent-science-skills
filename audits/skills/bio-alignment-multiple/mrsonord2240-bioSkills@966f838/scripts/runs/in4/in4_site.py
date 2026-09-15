# Input 4 (variant B): is the column holding P01 residue 142 stable enough to call a conserved/catalytic site?
# SKILL.md "Cross-Aligner Sensitivity Check" (MAFFT L-INS-i vs MUSCLE5 -align) + MUSCLE5 ensemble confidence.
from Bio import AlignIO
def col_of(aln, sid, k):          # 0-based residue k of sequence sid -> column index
    s = str(next(r.seq for r in aln if r.id == sid)); n = -1
    for j, c in enumerate(s):
        if c != '-':
            n += 1
            if n == k: return j
def residues_in_col(aln, j):     # which residue (seq, index) of every sequence sits in column j
    out = {}
    for r in aln:
        s = str(r.seq)
        out[r.id] = None if s[j] == '-' else (s[j], len(s[:j].replace('-', '')))
    return out
site = 141  # residue 142 (1-based) of P01
A = {name: AlignIO.read(f, 'fasta') for name, f in (('MAFFT L-INS-i', 'linsi.fasta'), ('MUSCLE5 -align', 'muscle.afa'), ('MUSCLE5 maxcc', 'maxcc.afa'))}
cols = {n: residues_in_col(a, col_of(a, 'P01', site)) for n, a in A.items()}
ref = cols['MAFFT L-INS-i']
for n, c in cols.items():
    agree = sum(c[k] == ref[k] for k in ref)
    print(f'{n:15s} column residues: ' + ''.join((c[k][0] if c[k] else '-') for k in sorted(c)) + f'   identical residue set vs MAFFT: {agree}/{len(ref)}')
lc = AlignIO.read('lc.afa', 'fasta'); mx = A['MUSCLE5 maxcc']; j = col_of(mx, 'P01', site)
print('MUSCLE5 letter confidence (0-9) at that column:', ''.join(str(r.seq)[j] for r in sorted(lc, key=lambda r: r.id)))
# same for a site in a gappy region for contrast
for site2 in (60, 250):
    cs = {n: residues_in_col(a, col_of(a, 'P01', site2)) for n, a in A.items()}
    r0 = cs['MAFFT L-INS-i']
    print(f'P01 residue {site2+1}: agreement MUSCLE vs MAFFT {sum(cs["MUSCLE5 -align"][k]==r0[k] for k in r0)}/15;',
          'LC:', ''.join(str(r.seq)[col_of(mx, "P01", site2)] for r in sorted(lc, key=lambda r: r.id)))
