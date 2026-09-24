"""Input 4: check the Skill's claims about un-scoreable/edge records and its parsers (unscored_report, not_scored) against real output."""
import sys, re
sys.path.insert(0, 'skill/examples')
import numpy as np, pandas as pd
from splice_parsers import (parse_spliceai_vcf, parse_pangolin_vcf, classify_delta, read_input_vcf, unscored_report, build_concordance)
fails = []
def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

# --- edge_grch37: 7 records, 9 ALT alleles (multiallelic has 3)
inp = read_input_vcf('data/edge_grch37.vcf')
print('input alleles', len(inp), list(inp['id']))
raw = [l for l in open('out/sai_edge_grch37.vcf') if not l.startswith('#')]
tagged_ids = [l.split('\t')[2] for l in raw if 'SpliceAI=' in l]
print('records tagged by SpliceAI:', tagged_ids)
s = parse_spliceai_vcf('out/sai_edge_grch37.vcf')
rep = unscored_report('data/edge_grch37.vcf', s['key'], 'SpliceAI')
print('\n'.join(rep))
missing_ids = {r.split('for ')[1].split(' ')[0] for r in rep}
chk('unscored_report names exactly REF-mismatch, 150bp deletion (>2*D) and intergenic',
    missing_ids == {'ref_mismatch', 'del_150bp_over_donor', 'intergenic_snv'})
chk('multi-allelic G>A,C,T: 3 ALT rows scored', s['key'].str.startswith('X:193062:G>').sum() >= 3 and set(['A', 'C', 'T']) <= set(k.split('>')[1] for k in s['key'] if k.startswith('X:193062:G>')))
chk('60bp deletion scored, delta_max >= 0.8', s.loc[s['key'].str.startswith('X:193032:C'), 'delta_max'].max() >= 0.8)
# N-only / star / symbolic
n = parse_spliceai_vcf('out/sai_aso_mask.vcf')
print(n[['key', 'gene', 'delta_max']].to_string() if len(n) else 'aso: no rows')
lab = classify_delta(n['delta_max']) if len(n) else []
print('N-only allele rows:', len(n), 'labels', list(lab))
chk('N-only alleles -> "." -> NaN -> not_scored (never BP4)', len(n) > 0 and n['delta_max'].isna().all() and all(x == 'not_scored' for x in lab))
st = parse_spliceai_vcf('out/sai_edge_star_allele.vcf')
rep_star = unscored_report('data/edge_star_allele.vcf', st['key'], 'SpliceAI')
print('star allele report:', rep_star, '| rows', len(st))
chk('"*" ALT surfaced by unscored_report (not silently dropped)', len(rep_star) == 1)
dellog = open('out/sai_edge_symbolic_DEL.log').read()
chk('symbolic <DEL> crashes SpliceAI with OSError (as the Skill says)', "Can't write record" in dellog or 'OSError' in dellog)
# chr-prefixed contig with bare-contig FASTA
c = parse_spliceai_vcf('out/sai_edge_chr_prefixed.vcf')
chk('chr-prefixed VCF scored by SpliceAI 1.3.1 against bare-contig FASTA (Skill says both tools score)', len(c) == 1 and c['delta_max'].iloc[0] >= 0.9)
# --- Pangolin edges
p = parse_pangolin_vcf('out/pang_edge_grch37.vcf')
print(p.to_string())
pin = read_input_vcf('data/edge_grch37.vcf')
rp = unscored_report('data/edge_grch37.vcf', p['key'], 'Pangolin')
print('\n'.join(rp))
chk('Pangolin multi-allelic: only ALT[0] (G>A) scored; C and T reported missing by unscored_report',
    any('X:193062:G>C' in r for r in rp) and any('X:193062:G>T' in r for r in rp) and not any('X:193062:G>A' in r for r in rp))
chk('Pangolin ref_mismatch record not scored and reported', any('ref_mismatch' in r for r in rp))
pc = parse_pangolin_vcf('out/pang_edge_chr_prefixed.vcf')
chk('Pangolin scores chr-prefixed VCF (as Skill says)', len(pc) == 1 and abs(pc['loss'].iloc[0]) >= 0.5)
print('FAILS:', fails)
