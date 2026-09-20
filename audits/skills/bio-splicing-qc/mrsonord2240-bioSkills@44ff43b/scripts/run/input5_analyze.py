#!/usr/bin/env python
"""Analyse the Input 5 STAR outputs against independent counts. Run after input5_star_2pass.sh: asenv as-core python input5_analyze.py"""
import sys, os, json, glob
from collections import defaultdict, Counter
sys.dont_write_bytecode = True
RUN = '/mnt/openscience/audits/bio-splicing-qc/run'
W = f'{RUN}/work/in5'
AS = '/mnt/openscience/audit-envs/alternative-splicing/public-data'
sys.path.insert(0, f'{RUN}/skill_copy/examples')
import splicing_qc as sq
import pysam
res = {}

# annotated introns from the GTF (STAR SJ coordinates: 1-based first/last intron base)
tx = defaultdict(list)
for l in open(f'{AS}/rnasplice/reference/genes_chrX.gtf'):
    f = l.rstrip('\n').split('\t')
    if len(f) > 8 and f[2] == 'exon':
        tid = f[8].split('transcript_id "')[1].split('"')[0]
        tx[tid].append((int(f[3]), int(f[4])))
gtf_introns = set()
for ex in tx.values():
    ex.sort()
    for (s1, e1), (s2, e2) in zip(ex[:-1], ex[1:]):
        if s2 - e1 - 1 > 0:
            gtf_introns.add((e1 + 1, s2 - 1))
print('GTF annotated introns (chrX):', len(gtf_introns))

def read_sj(p):
    d = {}
    for l in open(p):
        f = l.split()
        d[(int(f[1]), int(f[2]))] = dict(strand=int(f[3]), motif=int(f[4]), annot=int(f[5]), uniq=int(f[6]), multi=int(f[7]), ovh=int(f[8]))
    return d

samples = ['ERR188383', 'ERR188428', 'ERR188454', 'ERR204916']
p1 = {s: read_sj(f'{W}/pass1_{s}_SJ.out.tab') for s in samples}
p2 = {s: read_sj(f'{W}/pass2_{s}_SJ.out.tab') for s in samples}
# 1. what does SJ.out.tab column 6 mean in pass 1?
for s in samples[:1]:
    d = p1[s]
    a = sum(1 for k, v in d.items() if v['annot'] == 1); a_in = sum(1 for k, v in d.items() if v['annot'] == 1 and k in gtf_introns)
    print(f'pass1 {s}: rows {len(d)} annot==1 {a} of which in GTF {a_in}')
# 2. merged file semantic
rows = [l.split() for l in open(f'{W}/cohort_novel_SJ.tab')]
keys = [(int(r[1]), int(r[2])) for r in rows]
ukeys = set(keys)
in_gtf = sum(1 for k in ukeys if k in gtf_introns)
print(f'cohort_novel_SJ.tab: {len(rows)} lines, {len(ukeys)} distinct junctions, {in_gtf} of them are ALREADY in the GTF (named "novel"), truly novel: {len(ukeys) - in_gtf}')
dup = len(rows) - len(ukeys)
print('duplicate junction lines (same start/end, different counts because of sort -u on full lines):', dup)
res['merge'] = dict(lines=len(rows), distinct=len(ukeys), in_gtf=in_gtf, novel=len(ukeys) - in_gtf, duplicate_lines=dup)
# what did the filter drop? annotated non-canonical
allrows = []
for s in samples:
    for k, v in p1[s].items():
        allrows.append((s, k, v))
canon_drop = [(s, k, v) for s, k, v in allrows if v['motif'] == 0 and v['uniq'] >= 3]
print('pass1 rows with >=3 unique reads but motif==0 (dropped by $5>0):', len(canon_drop), '; of these annotated:', sum(1 for _, _, v in canon_drop if v['annot'] == 1),
      '; strand defined (col4>0):', sum(1 for _, _, v in canon_drop if v['strand'] > 0))
und = [(s, k, v) for s, k, v in allrows if v['strand'] == 0 and v['uniq'] >= 3]
print('pass1 rows with >=3 unique reads and strand==0 (undefined):', len(und), '; of which motif>0:', sum(1 for _, _, v in und if v['motif'] > 0))
res['filter'] = dict(dropped_noncanonical_ge3=len(canon_drop), dropped_annotated=sum(1 for _, _, v in canon_drop if v['annot'] == 1),
                     strand_undefined_ge3=len(und), strand_undefined_but_motif_gt0=sum(1 for _, _, v in und if v['motif'] > 0))
# 3. pass 2 col 6 semantic
for s in samples[:1]:
    d = p2[s]
    a = [k for k, v in d.items() if v['annot'] == 1]
    a_not_gtf = [k for k in a if k not in gtf_introns]
    print(f'pass2 {s}: rows {len(d)} annot==1: {len(a)}; annotated-in-file but NOT in GTF (came from pass-1 insertion): {len(a_not_gtf)}')
    res['pass2_annot_flag'] = dict(rows=len(d), annot1=len(a), annot1_not_in_gtf=len(a_not_gtf))
    novel_unique_p1 = sum(1 for k, v in p1[s].items() if k not in gtf_introns and v['uniq'] >= 1)
    novel_unique_p2 = sum(1 for k, v in d.items() if k not in gtf_introns and v['uniq'] >= 1)
    novel_flag0_p2 = sum(1 for k, v in d.items() if v['annot'] == 0)
    print(f'   junctions not in GTF with >=1 unique read: pass1 {novel_unique_p1}, pass2 {novel_unique_p2}; rows still flagged unannotated in pass2: {novel_flag0_p2}')
    res['pass2_novel'] = dict(pass1_not_in_gtf=novel_unique_p1, pass2_not_in_gtf=novel_unique_p2, pass2_flag0=novel_flag0_p2)
# 4. XS tags in pass2 BAM
n = x = 0
with pysam.AlignmentFile(f'{W}/pass2_ERR188383_Aligned.sortedByCoord.out.bam') as fh:
    for r in fh:
        if r.cigartuples and any(o == 3 for o, _ in r.cigartuples):
            n += 1; x += r.has_tag('XS')
print(f'pass2 BAM: spliced records {n}, with XS tag {x}')
res['xs'] = dict(spliced=n, with_xs=x)
# 5. Skill counts vs STAR SJ.out.tab (unique) on pass-2 BAM
bam = f'{W}/pass2_ERR188383_Aligned.sortedByCoord.out.bam'
try:
    sq.count_junction_reads(bam)
    res['star_bam_index_needed'] = False
except ValueError as e:
    print('Skill count_junction_reads on the STAR-sorted BAM as produced (no .bai):', e)
    res['star_bam_index_needed'] = str(e)
pysam.index(bam)
sc = sq.count_junction_reads(bam)
sj = p2['ERR188383']
star = {(s0, e): v['uniq'] + v['multi'] for (s0, e), v in sj.items()}
staru = {(s0, e): v['uniq'] for (s0, e), v in sj.items()}
skill = {(k[1] + 1, k[2]): c for k, c in sc.items()}
frag = defaultdict(set); fragu = defaultdict(set)
with pysam.AlignmentFile(bam) as fh:
    for r in fh:
        if r.is_unmapped or r.is_secondary: continue
        pos = r.reference_start
        for op, ln in r.cigartuples:
            if op == 3:
                frag[(pos + 1, pos + ln)].add(r.query_name)
                if r.get_tag('NH') == 1: fragu[(pos + 1, pos + ln)].add(r.query_name)
            if op in (0, 2, 3, 7, 8): pos += ln
common = set(skill) & set(star)
eq_read = sum(1 for k in common if skill[k] == staru[k])
eq_frag = sum(1 for k in common if len(fragu.get(k, ())) == staru[k])
print(f'Skill junction_reads vs STAR SJ.out.tab (unique col7): Skill junctions {len(skill)}, STAR {len(star)}, common {len(common)}; count equal read-level {eq_read}, fragment-level(unique) {eq_frag}')
print(f'   sums: Skill (all primary records, incl. multimappers) {sum(skill.values())}; STAR unique {sum(staru.values())}; STAR unique+multi {sum(star.values())}; fragment unique {sum(len(v) for v in fragu.values())}')
ge10_skill = sum(1 for c in skill.values() if c >= 10); ge10_star = sum(1 for c in staru.values() if c >= 10)
print(f'   junctions >=10 reads: Skill {ge10_skill}/{len(skill)} = {ge10_skill/len(skill):.1%}; STAR unique {ge10_star}/{len(staru)} = {ge10_star/len(staru):.1%}')
res['skill_vs_star'] = dict(skill_j=len(skill), star_j=len(star), common=len(common), eq_read=eq_read, eq_frag=eq_frag, skill_sum=sum(skill.values()),
                            star_uniq_sum=sum(staru.values()), star_all_sum=sum(star.values()), frag_uniq_sum=sum(len(v) for v in fragu.values()), ge10_skill=ge10_skill, ge10_star=ge10_star)
# 6. mapping stats
for s in samples:
    t = open(f'{W}/pass2_{s}_Log.final.out').read()
    u = [l for l in t.split('\n') if 'Uniquely mapped reads %' in l][0].split('|')[1].strip()
    t1 = open(f'{W}/pass1_{s}_Log.final.out').read()
    u1 = [l for l in t1.split('\n') if 'Uniquely mapped reads %' in l][0].split('|')[1].strip()
    print(f'{s}: uniquely mapped pass1 {u1} pass2 {u}; SJ rows pass1 {len(p1[s])} pass2 {len(p2[s])}')
# 7. pass-2 Log.out insertion counts
for l in open(f'{W}/pass2_ERR188383_Log.out'):
    if 'sjdb' in l.lower() and ('insert' in l.lower() or 'number' in l.lower() or 'junction' in l.lower()):
        print('  Log.out:', l.strip()[:200])
# 8. ReadsPerGene exists and parses
rg = [l.split('\t') for l in open(f'{W}/pass2_ERR188383_ReadsPerGene.out.tab')]
print('ReadsPerGene rows:', len(rg), 'first 4:', [r[:2] for r in rg[:4]])
json.dump(res, open(f'{RUN}/work/input5_result.json', 'w'), indent=1)
