"""NEW input panel (auditor's own, not in the fixer's panel): CFTR + BRCA1, GRCh38.
Coordinates: Ensembl VEP HGVS endpoint (pathogenic set) and ClinVar esummary SPDI (Likely benign set); every REF is asserted
against the hg38 FASTA (UCSC chr7 downloaded 2026-09-20 + chr17), minus-strand gene records given as genomic (forward) alleles.
usage: python mk_new_panel.py /mnt/openscience/as-spvp-reaudit-scratch/hg38_chr7_chr17.upper.fa"""
import sys
from pyfaidx import Fasta
fa = Fasta(sys.argv[1])
# id, chrom, pos, ref, alt, expectation
V = [
 ('CFTR_c.3717+12191C>T_3849+10kb_pseudoexon', 'chr7', 117639961, 'C', 'T', 'deep-intronic pseudoexon (literature)'),
 ('CFTR_c.1585-1G>A_acceptor', 'chr7', 117587738, 'G', 'A', 'canonical acceptor'),
 ('CFTR_c.1393-1G>A_acceptor', 'chr7', 117559463, 'G', 'A', 'canonical acceptor'),
 ('BRCA1_c.594-2A>C_acceptor', 'chr17', 43095924, 'T', 'G', 'canonical acceptor (minus strand: genomic T>G)'),
 ('BRCA1_c.5074+1G>A_donor', 'chr17', 43067607, 'C', 'T', 'canonical donor (minus strand: genomic C>T)'),
 ('BRCA1_c.212+3A>G_donor+3', 'chr17', 43106453, 'T', 'C', 'donor +3 (minus strand: genomic T>C)'),
 ('CFTR_c.3718-15A>T_LB', 'chr7', 117642423, 'A', 'T', 'ClinVar likely benign'),
 ('CFTR_c.4242+9T>C_LB', 'chr7', 117665573, 'T', 'C', 'ClinVar likely benign'),
 ('CFTR_c.4137-18A>G_LB', 'chr7', 117665441, 'A', 'G', 'ClinVar likely benign'),
 ('CFTR_c.2909-10T>G_LB', 'chr7', 117606664, 'T', 'G', 'ClinVar likely benign'),
 ('BRCA1_c.5332+84G>A_LB', 'chr17', 43050979, 'C', 'T', 'ClinVar likely benign'),
 ('BRCA1_c.594-4A>T_LB', 'chr17', 43095926, 'T', 'A', 'ClinVar likely benign (2 bp from an acceptor)'),
]
out = ['##fileformat=VCFv4.2', '##contig=<ID=chr7,length=159345973>', '##contig=<ID=chr17,length=83257441>',
       '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO']
bad = 0
for vid, ch, pos, ref, alt, note in V:
    got = str(fa[ch][pos - 1:pos - 1 + len(ref)]).upper()
    ok = got == ref
    if not ok:
        # try the complement (gene-strand allele given by the source)
        comp = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
        if got == comp[ref]:
            print(f'{vid}: allele given on gene strand, complementing {ref}>{alt}')
            ref, alt, ok = comp[ref], comp[alt], True
    print(f'{vid}: {ch}:{pos} REF {ref} fasta {got} {"OK" if ok else "MISMATCH"} | {note}')
    bad += not ok
    out.append(f'{ch}\t{pos}\t{vid}\t{ref}\t{alt}\t.\t.\t.')
open('data/panel_new_grch38.vcf', 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('MISMATCHES', bad)
