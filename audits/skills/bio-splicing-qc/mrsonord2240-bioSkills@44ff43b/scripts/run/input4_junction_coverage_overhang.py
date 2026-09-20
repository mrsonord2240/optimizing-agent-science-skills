#!/usr/bin/env python
"""
Input 4 (variant B): per-junction read counts / overhang / ">=10 reads" thresholds.
Skill code under test (extracted VERBATIM from SKILL.md by regex, not retyped):
  SKILL.md::junction_stats                      (overhang + counts)
  examples/splicing_qc.py::count_junction_reads / analyze_junction_coverage / generate_qc_report
Truth: SYNTHETIC overhang BAM (planted CIGARs), synthetic multi-mapper / =X-CIGAR BAMs, real chrX PE BAM vs independent
fragment-level pysam count and regtools.
Run: asenv as-core python input4_junction_coverage_overhang.py
"""
import sys, os, re, json, shutil, subprocess, types
from collections import Counter, defaultdict
sys.dont_write_bytecode = True
RUN = '/mnt/openscience/audits/bio-splicing-qc/run'
D = f'{RUN}/data/synthetic'
AS = '/mnt/openscience/audit-envs/alternative-splicing/public-data'
W = f'{RUN}/work/in4'
shutil.rmtree(W, ignore_errors=True)
os.makedirs(W)
import pysam

# ---- extract SKILL.md block verbatim
md = open(f'{RUN}/skill_copy/SKILL.md', encoding='utf-8').read()
m = re.search(r'```python\n(import pysam\nfrom collections import defaultdict\n\ndef junction_stats.*?)\ncounts, overhang = junction_stats', md, re.S)
assert m, 'junction_stats block not found in SKILL.md'
code = m.group(1)
open(f'{RUN}/work/skillmd_junction_stats.py', 'w').write(code)
mod = types.ModuleType('skillmd'); exec(compile(code, 'SKILL.md::junction_stats', 'exec'), mod.__dict__)
junction_stats = mod.junction_stats
sys.path.insert(0, f'{RUN}/skill_copy/examples')
import splicing_qc as sq

res = {}
# =============== A. overhang truth on planted CIGARs
counts, ov = junction_stats(f'{D}/se_overhang.bam')
print('A. SKILL.md junction_stats on planted overhang BAM (12 reads per shape):')
truth_by_start = {100000: ('mj_micro4  (30M1000N4M800N66M)  true adjacent overhang: 4 and 4', (4, 4)),
                  105000: ('mj_micro10 (20M700N10M900N70M)  true: 10 and 10', (10, 10)),
                  110000: ('one_ov6   (6M500N94M)           true: 6', (6,)),
                  115000: ('one_ov50  (50M600N50M)          true: 50', (50,))}
rows = []
for k in sorted(counts):
    rows.append((k, counts[k], ov[k]))
    print('   junction', k, 'reads', counts[k], 'SKILL overhang', ov[k])
res['A_junction_stats'] = [dict(junction=list(k), reads=c, skill_overhang=o) for k, c, o in rows]
# assertions vs truth
first_micro = [(k, c, o) for k, c, o in rows if k[1] in (100030, 101030 + 0)]
# planted junction coordinates (0-based intron start = 100000+30=100030 ; second 100000+30+1000+4=101034)
truth_junc = {(100030, 101030): 4, (101034, 101834): 4,
              (105020, 105720): 10, (105730, 106630): 10,
              (110006, 110506): 6, (115050, 115650): 50}
chk = {}
for (s, e), t in truth_junc.items():
    key = ('chrS', s, e)
    chk[f'{s}-{e}'] = dict(true=t, skill=ov.get(key), reads=counts.get(key))
    print(f'   ASSERT junction {s}-{e}: true overhang {t}, Skill {ov.get(key)}', 'OK' if ov.get(key) == t else 'MISMATCH')
res['A_assert'] = chk

# =============== B. examples/splicing_qc.py::count_junction_reads min_overhang parameter
c8 = sq.count_junction_reads(f'{D}/se_overhang.bam', min_overhang=8)
c99 = sq.count_junction_reads(f'{D}/se_overhang.bam', min_overhang=99)
print('B. count_junction_reads(min_overhang=8) total reads/junctions:', sum(c8.values()), len(c8), '| min_overhang=99:', sum(c99.values()), len(c99), '| identical:', c8 == c99)
res['B_min_overhang_noop'] = dict(identical=(c8 == c99), n_junctions=len(c8), total_reads=sum(c8.values()))
# expected if honoured: overhang<8 excluded -> one_ov6 and mj_micro4 junctions (12 reads each; 3 junctions) drop
print('   expected if honoured (>=8): junction (110006,110506) and both micro4 junctions absent; present =',
      [(k[1], k[2]) for k in c8 if (k[1], k[2]) in {(110006, 110506), (100030, 101030), (101034, 101834)}])

# =============== C. =/X CIGAR ops: the example ignores ops 7/8 when advancing ref_pos
hdr = pysam.AlignmentHeader.from_dict({'HD': {'VN': '1.6', 'SO': 'coordinate'}, 'SQ': [{'SN': 'chrS', 'LN': 700000}]})
p = f'{W}/eqx.bam'
with pysam.AlignmentFile(p, 'wb', header=hdr) as fh:
    for i in range(5):
        r = pysam.AlignedSegment(hdr); r.query_name = f'e{i}'; r.reference_id = 0; r.reference_start = 200000
        r.cigartuples = [(7, 40), (8, 1), (7, 9), (3, 1000), (7, 50)]   # 50=/X then 1000N then 50=
        r.query_sequence = 'A' * 100; r.query_qualities = pysam.qualitystring_to_array('I' * 100); r.flag = 0; r.mapping_quality = 255
        fh.write(r)
pysam.index(p)
ce = sq.count_junction_reads(p)
cs, _ = junction_stats(p)
print('C. =/X CIGAR read, true junction (200050,201050):  example ->', dict(ce), ' | SKILL.md junction_stats ->', dict(cs))
res['C_eqx'] = dict(example=[[list(k), v] for k, v in ce.items()], skillmd=[[list(k), v] for k, v in cs.items()], true=[200050, 201050])

# =============== D. multi-mappers (NH>1, MAPQ<=3) counted
p = f'{W}/multi.bam'
n_multi = 0; n_tot = 0
with pysam.AlignmentFile(f'{D}/se_clean.bam') as fi, pysam.AlignmentFile(p, 'wb', template=fi) as fo:
    for i, rd in enumerate(fi):
        if any(o == 3 for o, _ in rd.cigartuples):
            n_tot += 1
            if n_tot % 4 == 0:
                rd.set_tag('NH', 4); rd.mapping_quality = 3; n_multi += 1
        fo.write(rd)
pysam.index(p)
cm = sq.count_junction_reads(p)
cu = Counter()
with pysam.AlignmentFile(p) as fh:
    for rd in fh:
        if rd.is_unmapped or rd.is_secondary or rd.get_tag('NH') > 1:
            continue
        pos = rd.reference_start
        for op, ln in rd.cigartuples:
            if op == 3: cu[(rd.reference_name, pos, pos + ln)] += 1
            if op in (0, 2, 3, 7, 8): pos += ln
print(f'D. multimapper contamination: {n_multi}/{n_tot} spliced reads flagged NH=4 MAPQ 3. Skill counts {sum(cm.values())} junction reads/{len(cm)} junctions; unique-only truth {sum(cu.values())}/{len(cu)}')
res['D_multimappers'] = dict(skill_reads=sum(cm.values()), skill_junctions=len(cm), unique_reads=sum(cu.values()), unique_junctions=len(cu),
                             skill_ge10=sq.analyze_junction_coverage(cm)['junctions_ge_10'], unique_ge10=sum(1 for c in cu.values() if c >= 10))

# =============== E. real chrX PE data: read-level (Skill) vs fragment-level vs regtools vs STAR SJ (later)
bam = f'{AS}/derived/xs_bams/ERR188383.xs.bam'
skill_counts = sq.count_junction_reads(bam)
cov = sq.analyze_junction_coverage(skill_counts)
frag = defaultdict(set)
with pysam.AlignmentFile(bam) as fh:
    for rd in fh:
        if rd.is_unmapped or rd.is_secondary:
            continue
        pos = rd.reference_start
        for op, ln in rd.cigartuples:
            if op == 3: frag[(rd.reference_name, pos, pos + ln)].add(rd.query_name)
            if op in (0, 2, 3, 7, 8): pos += ln
fc = {k: len(v) for k, v in frag.items()}
diff = sum(1 for k in skill_counts if skill_counts[k] != fc[k])
print('E. real chrX ERR188383: Skill read-level junctions', len(skill_counts), 'reads', sum(skill_counts.values()), '| fragment-level reads', sum(fc.values()),
      '| junctions whose count differs', diff, '| ge10 read-level', cov['junctions_ge_10'], 'ge10 fragment-level', sum(1 for c in fc.values() if c >= 10))
res['E_real_chrX'] = dict(skill_junctions=len(skill_counts), skill_reads=sum(skill_counts.values()), fragment_reads=sum(fc.values()), junctions_differing=diff,
                          skill_ge10=cov['junctions_ge_10'], fragment_ge10=sum(1 for c in fc.values() if c >= 10), pct_ge_10=cov['pct_ge_10'], median=cov['median_reads'])
# regtools
rt = f'{W}/ERR188383.junc'
r = subprocess.run(['regtools', 'junctions', 'extract', '-a', '8', '-m', '50', '-s', 'XS', '-o', rt, bam], capture_output=True, text=True)
rtc = {}
for l in open(rt):
    f = l.split()
    if f[0] == 'track': continue
    st, en = int(f[1]), int(f[2]); blk = [int(x) for x in f[10].split(',')]
    rtc[(f[0], st + blk[0], en - blk[1])] = int(f[4])
common = set(rtc) & set(skill_counts)
print('   regtools junctions', len(rtc), 'common with Skill', len(common), '; sum reads regtools', sum(rtc.values()),
      '; identical counts on common', sum(1 for k in common if rtc[k] == skill_counts[k]), '/', len(common))
res['E_regtools'] = dict(n=len(rtc), common=len(common), identical=sum(1 for k in common if rtc[k] == skill_counts[k]), regtools_reads=sum(rtc.values()),
                         regtools_ge10=sum(1 for v in rtc.values() if v >= 10))
# Skill's own quality verdict in generate_qc_report on real data
print('E. analyze_junction_coverage:', cov)

# =============== F. generate_qc_report end-to-end on real chrX (uses junction_saturation + annotation + coverage)
os.makedirs(f'{W}/rep', exist_ok=True)
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    st = sq.generate_qc_report(bam, f'{AS}/derived/chrX.bed12', f'{W}/rep/ERR188383')
out = buf.getvalue()
print('F. generate_qc_report() stdout:\n' + out)
res['F_report'] = dict(stdout=out, returned=st)
# empty BAM edge: no spliced reads
p = f'{W}/nosplice.bam'
with pysam.AlignmentFile(p, 'wb', header=hdr) as fh:
    r = pysam.AlignedSegment(hdr); r.query_name = 'x'; r.reference_id = 0; r.reference_start = 1000; r.cigartuples = [(0, 50)]
    r.query_sequence = 'A' * 50; r.query_qualities = pysam.qualitystring_to_array('I' * 50); r.flag = 0; r.mapping_quality = 255; fh.write(r)
pysam.index(p)
try:
    sq.generate_qc_report(p, f'{D}/synth.bed12', f'{W}/rep/nosplice')
    res['F_nosplice'] = 'completed'
except Exception as e:
    res['F_nosplice'] = repr(e)[:300]
    print('   generate_qc_report on a BAM without spliced reads ->', repr(e)[:300])
# BAM without index
p2 = f'{W}/noindex.bam'
shutil.copy(f'{D}/se_overhang.bam', p2)
try:
    junction_stats(p2); res['F_noindex'] = 'ok'
except Exception as e:
    res['F_noindex'] = repr(e)[:200]; print('   junction_stats on BAM lacking .bai ->', repr(e)[:200])
json.dump(res, open(f'{RUN}/work/input4_result.json', 'w'), indent=1, default=str)
