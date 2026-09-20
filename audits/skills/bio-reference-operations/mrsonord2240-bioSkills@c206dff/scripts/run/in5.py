#!/usr/bin/env python
"""INPUT 5 (Stress): the Skill's pysam Python code, executed VERBATIM from the shipped .md files
(consensus_at_position, build_consensus, simple_consensus, compare_to_ref, fetch-all-chromosomes), on planted-truth
synthetic data with a coverage gap, a soft-masked reference, and the real human chr22 slice. Each result is compared with
an independent computation."""
import contextlib, io, json, os, shutil, sys, time
sys.path.insert(0, '/mnt/openscience/audits/bio-reference-operations/run')
from auditlib import *
import pysam
from collections import Counter

D = f'{W}/work/in5'
shutil.rmtree(D, ignore_errors=True)
os.makedirs(D)
SY = f'{W}/data/synthetic'
for f in ('synth_chr.bam', 'synth_chr.bam.bai', 'synth.fa'):
    shutil.copy(f'{SY}/{f}', f'{D}/{f}')
HB = f'{W}/data/real'
shutil.copy(f'{HB}/test.paired_end.sorted.bam', f'{D}/h.bam'); shutil.copy(f'{HB}/test.paired_end.sorted.bam.bai', f'{D}/h.bam.bai')
shutil.copy(f'{HB}/genome.fasta', f'{D}/hs.fa')
T = json.load(open(f'{SY}/truth.json'))
S = {k: v.upper() for k, v in T['seqs'].items()}
alt = {int(k): v for k, v in T['alt'].items()}
HOM, HET50, HET20, ERR1 = T['HOM'], T['HET50'], T['HET20'], T['ERR1']

snip = lambda n: open(f'{W}/snippets/{n}.txt', encoding='utf-8').read()

# ---- 1. SKILL.md consensus_at_position (skill_22), verbatim; only file name and position substituted
ns = {}
src = snip('skill_22_python').replace("'input.bam'", f"'{D}/synth_chr.bam'").replace("'chr1', 1000000", "'chr1', 200").replace('chr1:1000000', 'chr1:200')
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(src, ns)
print(buf.getvalue().strip())
cap = ns['consensus_at_position']
with pysam.AlignmentFile(f'{D}/synth_chr.bam') as bam:
    got = {p: cap(bam, 'chr1', p) for p in (HOM, HET50, HET20, ERR1, 1200, 1550)}
print('consensus_at_position ->', got)
check('consensus_at_position (SKILL 236-245) verbatim runs: hom-alt site -> planted alt', got[HOM] == alt[HOM] and 'Consensus at chr1:200 = C' in buf.getvalue(), buf.getvalue().strip())
check('  ...20%-alt site -> majority A; 3%-alt site -> ref; uncovered site -> N; depth-2 site -> alt (no min depth in this helper)', got[HET20] == S['chr1'][HET20] and got[ERR1] == S['chr1'][ERR1] and got[1200] == 'N' and got[1550] == alt[T['LOW']], got)
print('  note: SKILL prints "chr1:1000000" for a 0-based pos argument; this run used pos=200 -> 1-based chr1:201')

# ---- 2. SKILL build_consensus (skill_23) and usage-guide simple_consensus (ug_11) / compare_to_ref (ug_12), verbatim
exec(snip('skill_23_python'), ns)
exec(snip('ug_11_python'), ns)
exec(snip('ug_12_python'), ns)
build, simple, cmp_ = ns['build_consensus'], ns['simple_consensus'], ns['compare_to_ref']

# oracle: samtools consensus keeping reference coordinates (show-del yes, show-ins no, -d 3)
rc, o, e = sh(f'samtools consensus -d 3 --show-del yes --show-ins no -a {D}/synth_chr.bam', D)
truth1 = by = {h.split()[0]: s for h, s in fa_records(o)}['chr1']

t0 = time.time()
bc = build(f'{D}/synth_chr.bam', 'chr1', 0, 1700)
print('build_consensus(chr1,0,1700,min_depth=3): length', len(bc), 'in %.2fs' % (time.time() - t0))
check('build_consensus (SKILL 260-276) on a 1700-bp region returns 1700 characters (one per reference position)', len(bc) == 1700, f'returned {len(bc)}')
print('  uncovered columns are silently DROPPED: 1700 - %d = %d missing (the 500-bp gap 1000-1499 has no pileup column)' % (len(bc), 1700 - len(bc)))
# alignment with the reference is lost after the gap
ref1 = S['chr1']
mismatch_vs_ref = sum(1 for i, c in enumerate(bc) if c != 'N' and c != ref1[i])
mismatch_true = sum(1 for i in range(1700) if truth1[i] not in ('N',) and truth1[i] != ref1[i])
print('  positional mismatches vs reference: build_consensus %d (spurious, shifted after gap) vs true %d (samtools consensus oracle)' % (mismatch_vs_ref, mismatch_true))
print('  (with min_depth=3 the shifted island is all N, which hides the shift on this synthetic set; see min_depth=1 below and the real data)')
bc1 = build(f'{D}/synth_chr.bam', 'chr1', 0, 1700, min_depth=1)
sp1 = sum(1 for i, c in enumerate(bc1) if c != 'N' and c != ref1[i])
print('  with min_depth=1 (the depth-2 island is called): length', len(bc1), '| positional mismatches vs reference', sp1, '(true differences: %d)' % mismatch_true)
check('build_consensus(min_depth=1): the 200-bp island after the 500-bp gap lands 500 positions early -> ~150 spurious positional differences vs reference', sp1 > 100, sp1)
prefix_ok = all(a == b for a, b in zip(bc[:1000], truth1[:1000]) if 'N' not in (a, b) and 'M' not in (a, b))
check('...but the columns BEFORE the gap agree with the oracle consensus (function logic itself is right where coverage is contiguous)', prefix_ok)

sc = simple(f'{D}/synth_chr.bam', 'chr1', 0, 1700)
check('usage-guide simple_consensus (min_depth=5) has the same defect (length %d != 1700)' % len(sc), len(sc) != 1700)

# ---- 3. compare_to_ref (ug_12) on the gap region and on a contiguous region
d_all = cmp_(f'{D}/synth_chr.bam', f'{D}/synth.fa', 'chr1', 0, 1700)
d_contig = cmp_(f'{D}/synth_chr.bam', f'{D}/synth.fa', 'chr1', 0, 1000)
print('compare_to_ref chr1:0-1700 ->', len(d_all), 'differences; chr1:0-1000 ->', len(d_contig), d_contig[:5])
print('  (synthetic island has depth 2 < min_depth 5 so it is N here; the false-difference flood is shown on the real slice below)')
# contiguous region: expected differences vs reference are hom-alt at HOM (and the 50/50 tie base if it is alt)
exp_pos = {HOM}
got_pos = {p for p, r, c in d_contig}
print('  contiguous 0-1000: differences at 0-based positions', sorted(got_pos), '| planted hom-alt', HOM, '| 50/50 tie column', HET50)
check('compare_to_ref on contiguous coverage finds the planted hom-alt (pos 200) and reports it 0-based with (ref, alt) = (A, C)', (HOM, S['chr1'][HOM], alt[HOM]) in d_contig, d_contig[:3])
check('compare_to_ref on contiguous coverage: no other false differences except the 50/50 tie column %d' % HET50, got_pos <= {HOM, HET50}, sorted(got_pos))

# ---- 4. soft-masked reference => case-mismatch false positives
masked = S['chr1'][:100] + S['chr1'][100:400].lower() + S['chr1'][400:]
open(f'{D}/masked.fa', 'w').write('>chr1\n' + '\n'.join(masked[i:i + 60] for i in range(0, len(masked), 60)) + '\n')
d_mask = cmp_(f'{D}/synth_chr.bam', f'{D}/masked.fa', 'chr1', 0, 1000)
false_case = [x for x in d_mask if x[1].islower()]
print('compare_to_ref with a soft-masked (lowercase) reference 100-399:', len(d_mask), 'differences,', len(false_case), 'are pure case artefacts, e.g.', d_mask[:2])
check('compare_to_ref is case-sensitive: a soft-masked (lowercase) reference stretch of 300 bp yields ~300 false "differences" (consensus is upper-case)', len(false_case) >= 250, len(false_case))

# ---- 5. real human chr22 slice
t0 = time.time()
refh = parse_fasta(f'{D}/hs.fa')['chr22'].upper()
dh = cmp_(f'{D}/h.bam', f'{D}/hs.fa', 'chr22', 1951, 4617)
print('compare_to_ref human chr22:1951-4617 -> %d differences in %.1fs' % (len(dh), time.time() - t0))
# independent: positions where the majority base != ref at columns with depth>=5 (same defaults as simple_consensus min_depth=5)
cnt = {}
with pysam.AlignmentFile(f'{D}/h.bam') as f:
    for col in f.pileup('chr22', 1951, 4617, truncate=True):
        c = Counter()
        for r in col.pileups:
            if r.is_del or r.is_refskip or r.query_position is None:
                continue
            c[r.alignment.query_sequence[r.query_position].upper()] += 1
        cnt[col.reference_pos] = c
true_diff = [p for p, c in cnt.items() if sum(c.values()) >= 5 and c.most_common(1)[0][0] != refh[p]]
covered_cols = len(cnt)
span = 4617 - 1951
print('  covered columns %d of %d span (%.0f%%); independent true differences (depth>=5 majority != ref): %d' % (covered_cols, span, 100 * covered_cols / span, len(true_diff)))
sc_h = simple(f'{D}/h.bam', 'chr22', 1951, 4617)
print('  simple_consensus length', len(sc_h), 'vs span', span)
check('real human slice: simple_consensus length != region span because uncovered columns are dropped', len(sc_h) == covered_cols and len(sc_h) != span, (len(sc_h), span))
check('real human slice: compare_to_ref reports far more differences than the independent true count (misalignment)', len(dh) > 5 * max(len(true_diff), 1), (len(dh), len(true_diff)))
# corrected logic (position-keyed) -- how a correct implementation compares to the oracle
fixed = [(p, refh[p], cnt[p].most_common(1)[0][0]) for p in sorted(cnt) if sum(cnt[p].values()) >= 5 and cnt[p].most_common(1)[0][0] != refh[p]]
rc, o, e = sh(f'samtools consensus -d 5 --show-del yes --show-ins no -r chr22:1952-4617 {D}/h.bam', D)
orc = fa_records(o)[0][1]
orc_diff = [1951 + i for i, c in enumerate(orc) if c not in ('N',) and c != refh[1951 + i]]
cnt_raw = {}
with pysam.AlignmentFile(f'{D}/h.bam') as f:
    for col in f.pileup('chr22', 1951, 4617, truncate=True, min_base_quality=0, ignore_overlaps=False):
        c = Counter()
        for r in col.pileups:
            if r.is_del or r.is_refskip or r.query_position is None:
                continue
            c[r.alignment.query_sequence[r.query_position].upper()] += 1
        cnt_raw[col.reference_pos] = c
fixed_raw = {p for p, c in cnt_raw.items() if sum(c.values()) >= 5 and c.most_common(1)[0][0] != refh[p]}
print('  column 2122: pysam default pileup counts', dict(cnt[2122]), 'vs raw (Q>=0, overlaps kept)', dict(cnt_raw[2122]))
extra = [(p, orc[p - 1951], dict(cnt_raw.get(p, {})), refh[p]) for p in orc_diff if p not in fixed_raw and len(set(c for _, c in cnt_raw[p].most_common(2))) > 1]
print('  (column 2122 is a 2/2/1 tie: Bayesian tie-break, excluded as ambiguous)')
print('  samtools consensus -d 5 non-N differences vs ref:', len(orc_diff), '| independent majority differences (depth>=5, raw counts):', len(fixed_raw), '| extra in consensus:', extra)
check('position-keyed reference implementation and samtools consensus -d 5 agree on every non-tie differing column (true differences: %d)' % len(fixed_raw), not extra, extra)

# ---- 6. pysam pileup defaults the helpers silently inherit
with pysam.AlignmentFile(f'{D}/h.bam') as f:
    d_def = {col.reference_pos: col.nsegments for col in f.pileup('chr22', 2000, 2100, truncate=True)}
    d_raw = {col.reference_pos: col.nsegments for col in f.pileup('chr22', 2000, 2100, truncate=True, min_base_quality=0, ignore_overlaps=False, flag_filter=0)}
lost = sum(d_raw.get(p, 0) - d_def.get(p, 0) for p in d_raw)
print('pysam.pileup default filters vs raw over chr22:2001-2100: reads counted default %d vs raw %d' % (sum(d_def.values()), sum(d_raw.values())))
check('SKILL says the majority vote "ignores base qualities" (SKILL 254) -- but pysam.pileup silently drops bases with Q<13, duplicates, secondary reads and de-duplicates overlapping mates by default', sum(d_raw.values()) > sum(d_def.values()), (sum(d_def.values()), sum(d_raw.values())))

# ---- 7. remaining pysam snippets from the guides, verbatim, on the real slice
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(snip('skill_21_python').replace("'reference.fa'", f"'{D}/hs.fa'"), {'pysam': pysam})
out = buf.getvalue().splitlines()
check('SKILL "Fetch All Chromosomes" (skill_21) verbatim: prints ">chr22" and first 100 bases + "..."', out[0] == '>chr22' and out[1].upper() == refh[:100] + '...', out[:2])
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(snip('ug_09_python').replace("'reference.fa'", f"'{D}/hs.fa'"), {'pysam': pysam})
check('usage-guide "Get Reference Info" (ug_09) prints "Chromosomes: 1" and "chr22: 40,001 bp"', 'Chromosomes: 1' in buf.getvalue() and 'chr22: 40,001 bp' in buf.getvalue(), buf.getvalue().strip())

summary()
