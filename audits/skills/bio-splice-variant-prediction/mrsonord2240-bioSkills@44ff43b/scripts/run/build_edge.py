# Build SYNTHETIC edge-case VCFs on real GRCh37 chrX sequence for SpliceAI/Pangolin input-handling tests (INPUT 4).
import pyfaidx
fa = pyfaidx.Fasta('/mnt/openscience/audit-envs/alternative-splicing/public-data/derived/X.fa')
b = lambda p, n=1: fa['X'][p-1:p-1+n].seq.upper()
tx = sorted({(int(l.split('\t')[3]), int(l.split('\t')[4])) for l in open('/mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/reference/genes_chrX.gtf') if l.split('\t')[2] == 'transcript'})
gap = (0, 0); end = 0
for s, e in tx:
    if s - end > gap[1] - gap[0]:
        gap = (end, s)
    end = max(end, e)
ig = (gap[0] + gap[1]) // 2
while b(ig) not in 'ACGT':
    ig += 1
print('intergenic test position X:%d (largest transcript gap %s)' % (ig, gap))
donor = 193062
alt_of = lambda p: 'A' if b(p) != 'A' else 'C'
rows = [  # id, pos, ref, alt
    ('ok_control_G>A', donor, b(donor), 'A'),
    ('ref_mismatch', donor, 'C', 'A'),
    ('intergenic_snv', ig, b(ig), alt_of(ig)),
    ('multiallelic', donor, b(donor), 'A,C,T'),
    ('del_60bp_over_donor', donor - 30, b(donor - 30, 61), b(donor - 30)),
    ('del_150bp_over_donor', donor - 30, b(donor - 30, 151), b(donor - 30)),
    ('ins_4bp_at_donor', donor, b(donor), b(donor) + 'ACGT'),
]
hdr = '##fileformat=VCFv4.2\n##contig=<ID=X,length=155270560>\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n'
with open('data/edge_grch37.vcf', 'w', newline='\n') as f:
    f.write(hdr)
    for n, p, r, a in sorted(rows, key=lambda x: x[1]):
        f.write('\t'.join(['X', str(p), n, r, a, '.', '.', '.']) + '\n')
with open('data/edge_chr_prefixed.vcf', 'w', newline='\n') as f:   # same control record, contig named chrX (FASTA contig is X)
    f.write(hdr.replace('ID=X,', 'ID=chrX,'))
    f.write('\t'.join(['chrX', str(donor), 'chr_prefixed_control', b(donor), 'A', '.', '.', '.']) + '\n')
for nm, alt in (('symbolic_DEL', '<DEL>'), ('star_allele', '*')):
    with open('data/edge_%s.vcf' % nm, 'w', newline='\n') as f:
        f.write(hdr)
        f.write('\t'.join(['X', str(donor), nm, b(donor), alt, '.', '.', '.']) + '\n')
for l in open('data/edge_grch37.vcf'):
    print(l[:120].rstrip())
