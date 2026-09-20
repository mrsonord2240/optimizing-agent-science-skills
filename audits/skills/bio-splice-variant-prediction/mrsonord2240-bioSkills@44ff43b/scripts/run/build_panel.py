# Build the SYNTHETIC-PANEL VCF (real GRCh37 chrX variants; the VCF itself is assembled here) and assert REF alleles against X.fa (GRCh37).
# Sources for truth labels: Ensembl GRCh37 VEP/ClinVar lookups in q_ensembl.py / q_benign.py (run 2026-09-20).
import pyfaidx, sys
fa = pyfaidx.Fasta('/mnt/openscience/audit-envs/alternative-splicing/public-data/derived/X.fa')
def base(p, n=1): return fa['X'][p-1:p-1+n].seq.upper()
# name, pos, expected_ref, alt, class
P = [
 ('PLCXD1_donor_G>A',        193062,    'G', 'A', 'canonical donor (real)'),
 ('DMD_c.31+1G>A',           33229398,  'C', 'T', 'ClinVar pathogenic, canonical donor +1 (minus strand)'),
 ('GLA_c.370-1G>A',          100656798, 'C', 'T', 'ClinVar pathogenic, canonical acceptor -1 (minus strand)'),
 ('DMD_c.9563+1G>A',         31227614,  'C', 'T', 'ClinVar pathogenic, canonical donor +1 (minus strand)'),
 ('GLA_c.639+919G>A',        100654735, 'C', 'T', 'deep-intronic pseudoexon (Ishii 2002), ClinVar pathogenic'),
 ('OTC_c.386+5G>A',          38240687,  'G', 'A', 'donor +5 consensus (literature; not asserted)'),
 ('GLA_rs2071228_benign',    100653109, 'G', 'A', 'ClinVar benign intronic'),
 ('GLA_rs782094147_benign',  100652764, 'C', 'T', 'ClinVar benign intronic'),
 ('GLA_rs151195362_benign',  100653379, 'C', 'T', 'ClinVar benign synonymous'),
]
ok = True
lines = []
for n, p, r, a, c in P:
    got = base(p)
    print(n, p, 'ref_in_fasta=%s expected=%s' % (got, r), 'OK' if got == r else 'MISMATCH')
    ok &= (got == r)
    lines.append((n, 'X', p, r, a, c))
# canonical donor GT deletion (indel) at PLCXD1 : anchor base + GT
anch = base(193061); gt = base(193062, 2)
print('PLCXD1 donor dinucleotide at 193062-193063 =', gt, 'anchor', anch)
assert gt == 'GT'
lines.append(('PLCXD1_donor_GTdel', 'X', 193061, anch + 'GT', anch, 'canonical donor deleted (2bp del)'))
hdr = '##fileformat=VCFv4.2\n##contig=<ID=X,length=155270560>\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n'
with open(sys.argv[1], 'w', newline='\n') as f:
    f.write(hdr)
    for n, c, p, r, a, cl in sorted(lines, key=lambda x: x[2]):
        f.write('\t'.join([c, str(p), n, r, a, '.', '.', '.']) + '\n')
print('REF check all OK:', ok)
assert ok
