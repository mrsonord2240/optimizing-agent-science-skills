# Input 6 (NEW, re-audit 2026-09-15, Edge): "Check HBB rs334 in the v3.1.2 genomes (GRCh38) as well, my colleague also
# typed GRCh37 into the v3 call by mistake; and get LoF constraint for USP9Y (chrY) and MALAT1 (non-coding).
# One of our IDs looks truncated (11-5227002-T) - what happens?" Live gnomAD GraphQL; SKILL.md code verbatim.
import json, sys, time
sys.path.insert(0, '..')
from p_skill_code import query_variant, grpmax_faf95, query_gene_constraint
p = query_variant('11', 5227002, 'T', 'A', build='GRCh38', dataset='gnomad_r3')
print('gnomad_r3 rs334 ->', None if p is None else {'genome_af': (p.get('genome') or {}).get('af'), 'exome': p.get('exome')}, '| grpmax_faf95:', grpmax_faf95(p)); time.sleep(0.5)
try:
    query_variant('11', 5248232, 'T', 'A', build='GRCh37', dataset='gnomad_r3')
except ValueError as e:
    print('GRCh37 on gnomad_r3 -> ValueError:', e)
for sym in ('USP9Y', 'MALAT1', 'DMD'):
    g = query_gene_constraint(sym); time.sleep(0.5)
    if g is None:
        print(sym, '-> None'); continue
    print(sym, 'chrom', g.get('chrom'), 'LOEUF', (g.get('gnomad_constraint') or {}).get('oe_lof_upper'), '| note:', g.get('constraint_note'))
try:
    print('truncated id ->', query_variant('11', 5227002, 'T', '', build='GRCh38'))
except RuntimeError as e:
    print('truncated id -> RuntimeError:', e)
