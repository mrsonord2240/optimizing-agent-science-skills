"""Input 6b (NEW, auditor-made): build a small VCF on real chrX GRCh37 (X.fa, Ensembl GTF) with variants of KNOWN expected class:
 2 canonical donor GT->AT (G>A at intron +1... first base G of the GT) ; 2 canonical acceptor AG->AA (last G of intron); 3 exon-interior SNVs >=40 nt from sites; 3 deep-intronic SNVs >=200 nt from sites.
Usage: python 62_in6b_make_vcf.py <gtf> <fasta> <out.vcf>"""
import sys, collections, random, bisect
import pysam
gtf, fa, out = sys.argv[1:4]; g = pysam.FastaFile(fa); rng = random.Random(7)
tx = collections.defaultdict(list); strand = {}
for line in open(gtf):
    f = line.rstrip('\n').split('\t')
    if len(f) > 8 and f[2] == 'exon':
        t = f[8].split('transcript_id "')[1].split('"')[0]; tx[t].append((int(f[3]) - 1, int(f[4]))); strand[t] = f[6]
introns = []
for t, ex in tx.items():
    ex.sort()
    for (s1, e1), (s2, e2) in zip(ex, ex[1:]):
        if s2 - e1 > 600: introns.append((e1, s2, strand[t], (s1, e1), (s2, e2)))
introns = sorted(set(introns)); sites = sorted({p for i in introns for p in (i[0], i[1])})
far = lambda p, d: all(abs(sites[j] - p) > d for j in (bisect.bisect(sites, p) - 1, bisect.bisect(sites, p)) if 0 <= j < len(sites))
comp = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
var = []; rng.shuffle(introns)
def add(pos0, alt_pref, label):
    ref = g.fetch('X', pos0, pos0 + 1).upper(); alt = alt_pref if alt_pref != ref else ('A' if ref != 'A' else 'C')
    var.append((pos0 + 1, ref, alt, label))
nd = na = 0
for e1, s2, st, ex1, ex2 in introns:
    if st != '+': continue          # + strand only: intron first base 0-based e1 (G of GT), last base s2-1 (G of AG)
    if g.fetch('X', e1, e1 + 2).upper() == 'GT' and nd < 2: add(e1, 'A', 'donor_GT>AT'); nd += 1
    if g.fetch('X', s2 - 2, s2).upper() == 'AG' and na < 2: add(s2 - 1, 'A', 'acceptor_AG>AA'); na += 1
    if nd == 2 and na == 2: break
ne = nd_ = 0
for e1, s2, st, ex1, ex2 in introns:
    if ex1[1] - ex1[0] > 120 and far((ex1[0] + ex1[1]) // 2, 40) and ne < 3: add((ex1[0] + ex1[1]) // 2, 'T', 'exon_interior'); ne += 1
    mid = (e1 + s2) // 2
    if far(mid, 200) and nd_ < 3: add(mid, 'T', 'deep_intronic'); nd_ += 1
var = sorted(set(var))
with open(out, 'w') as fh:
    fh.write('##fileformat=VCFv4.2\n##contig=<ID=X,length=%d>\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n' % g.get_reference_length('X'))
    for pos, ref, alt, lab in var: fh.write(f'X\t{pos}\t{lab}\t{ref}\t{alt}\t.\t.\t.\n')
print(len(var), 'variants:', [(v[0], v[1] + '>' + v[2], v[3]) for v in var])
