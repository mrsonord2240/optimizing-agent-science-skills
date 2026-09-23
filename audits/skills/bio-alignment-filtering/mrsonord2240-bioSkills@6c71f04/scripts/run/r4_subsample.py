#!/usr/bin/env python3
"""Input 4 (regression, Variant B): reproducible, pair-consistent subsampling. The bash block and the pysam recipe are
EXTRACTED from the fixed SKILL.md and executed. Real 1000G HG00349 BAM (9601 records) and nf-core human PE BAM.
Second method for every count: pysam over the output (template membership), not the samtools exit code."""
import collections, os, shutil, sys
import pysam
from lib import check, sh, block, finish

AFD = os.environ['AFDATA']; W = sys.argv[1]; SK = sys.argv[2]
MD = f'{SK}/SKILL.md'
shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
G = f'{AFD}/1000g/HG00349.chr20_1400000-1500000.bam'
H = f'{AFD}/human/test.paired_end.sorted.bam'
shutil.copy(G, f'{W}/input.bam'); shutil.copy(G, f'{W}/in.bam'); shutil.copy(G, f'{W}/tumor.bam'); shutil.copy(H, f'{W}/normal.bam')
def cnt(p): return int(sh(f'samtools view -c {p}')[1])
def tmpl(p): return collections.Counter(r.query_name for r in pysam.AlignmentFile(p))
full = tmpl(f'{W}/input.bam'); N = cnt(f'{W}/input.bam')
print('records', N, 'templates', len(full), 'templates with >1 record', sum(1 for v in full.values() if v > 1))

# --- claims 1-2: -s SEED.FRAC is pair/template consistent and deterministic ---
sh(f'samtools view -s 42.1 -b -o {W}/s42a.bam {W}/input.bam'); sh(f'samtools view -s 42.1 -b -o {W}/s42b.bam {W}/input.bam')
t = tmpl(f'{W}/s42a.bam')
check('-s 42.1: every kept template has ALL its records (mates + secondary) kept', all(t[q] == full[q] for q in t), f'{len(t)} templates kept of {len(full)}')
check('-s 42.1: about 10% of templates', 0.08 <= len(t) / len(full) <= 0.12, f'{len(t)/len(full):.3f}')
same = sh(f'cmp <(samtools view {W}/s42a.bam) <(samtools view {W}/s42b.bam) && echo SAME')[1]
check('-s 42.1 twice: identical records', 'SAME' in same)

# --- claim 2 (fixed text): bare -s 0.1 is deterministic and means seed 0; 1.24 --subsample default seed changed ---
sh(f'samtools view -s 0.1 -b -o {W}/b1.bam {W}/input.bam'); sh(f'samtools view -s 0.1 -b -o {W}/b2.bam {W}/input.bam')
sh(f'samtools view --subsample 0.1 --subsample-seed 0 -b -o {W}/z0.bam {W}/input.bam')
sh(f'samtools view --subsample 0.1 -b -o {W}/auto1.bam {W}/input.bam'); sh(f'samtools view --subsample 0.1 -b -o {W}/auto2.bam {W}/input.bam')
def same2(a, b): return 'SAME' in sh(f'cmp <(samtools view {a}) <(samtools view {b}) && echo SAME')[1]
check('bare -s 0.1 twice: byte-identical (text: "deterministic too")', same2(f'{W}/b1.bam', f'{W}/b2.bam'), f'{cnt(f"{W}/b1.bam")} records')
check('bare -s 0.1 == --subsample 0.1 --subsample-seed 0 (text: "it means seed 0")', same2(f'{W}/b1.bam', f'{W}/z0.bam'))
check('--subsample 0.1 (no seed) differs from seed 0 on 1.24 (text: header-hash "auto" seed)', not same2(f'{W}/auto1.bam', f'{W}/z0.bam'), f'auto {cnt(f"{W}/auto1.bam")} vs seed0 {cnt(f"{W}/z0.bam")} (text quotes 1001 vs 1015)')
check('--subsample 0.1 twice on the same file: identical (header-derived)', same2(f'{W}/auto1.bam', f'{W}/auto2.bam'))
h = sh('samtools view --help 2>&1 | grep -A3 subsample-seed')[1]
check('samtools 1.24 --help documents --subsample-seed INT|auto with header hash', 'auto' in h and 'hash of the input header' in h, h.strip().splitlines()[0][:60])
sh(f'samtools view -s 42.1 -b -o {W}/x.bam {W}/input.bam')

# --- claim 3: nested keep-sets for the same seed; independent seeds for sequential cuts ---
sh(f'samtools view -s 1.5 -b {W}/input.bam > {W}/half1.bam'); sh(f'samtools view -s 2.25 -b {W}/half1.bam > {W}/quarter.bam')
sh(f'samtools view -s 1.25 -b {W}/half1.bam > {W}/nested.bam'); sh(f'samtools view -s 1.25 -b {W}/input.bam > {W}/direct25.bam')
check('sequential -s 1.5 then -s 2.25 (independent seeds): ~12.5% of original', abs(cnt(f'{W}/quarter.bam') / N - 0.125) < 0.02, f'{cnt(f"{W}/quarter.bam")} of {N} = {cnt(f"{W}/quarter.bam")/N:.3f}')
check('same seed: -s 1.5 then -s 1.25 keeps the same reads as direct -s 1.25 (nested 25%, not 12.5%)', same2(f'{W}/nested.bam', f'{W}/direct25.bam'), f'{cnt(f"{W}/nested.bam")} vs {cnt(f"{W}/direct25.bam")}')

# --- claim: fraction >= 1 spliced into -s silently keeps ~8% (the trap the guard removes) ---
sh(f'samtools view -s 1.084419 -b -o {W}/trap.bam {W}/input.bam')
print('   trap: -s 1.084419 keeps', cnt(f'{W}/trap.bam'), 'of', N)
check('text: "-s 1.084419" keeps only ~8% of reads', 0.06 <= cnt(f'{W}/trap.bam') / N <= 0.11, f'{cnt(f"{W}/trap.bam")/N:.3f}')

# --- SKILL.md "Subsample Reads" bash block, EXTRACTED and run ---
code = block(MD, 'Subsample Reads (Deterministic, Pair-Consistent)', 'bash', 'target=10000000')
def run_block(target, tag):
    d = f'{W}/blk_{tag}'; os.makedirs(d, exist_ok=True)
    for f in ('input.bam', 'in.bam', 'tumor.bam', 'normal.bam'): shutil.copy(f'{W}/{f}', f'{d}/{f}')
    open(f'{d}/block.sh', 'w').write(code.replace('target=10000000', f'target={target}'))
    rc, so, se = sh('bash block.sh', cwd=d)
    return d, rc, so, se
# (a) target above the total -> guard
d, rc, so, se = run_block(10000000, 'big')
check('block with target 10M > total: rc 0, stderr says copied unchanged', rc == 0 and 'copying unchanged' in se, se.strip()[:110])
check('coverage-matching guard: matched.bam == input.bam (9601 records, not ~8%)', cnt(f'{d}/matched.bam') == N, f'{cnt(f"{d}/matched.bam")}')
check('all block outputs exist', all(os.path.exists(f'{d}/{f}') for f in ('subset.bam', 'half1.bam', 'quarter.bam', 'matched.bam', 'tumor_matched.bam')))
# tumor (9601 rec) vs normal (5644 rec): tumor pulled down
nt = int(sh(f'samtools view -c -F 2308 {d}/tumor_matched.bam')[1]); nn = int(sh(f'samtools view -c -F 2308 {d}/normal.bam')[1])
check('tumor-normal: tumor pulled down toward normal (within 10% of 5640)', abs(nt - nn) / nn < 0.10, f'tumor_matched {nt} vs normal {nn}')
# (b) target below total
for tgt in (3000, 1000, 6000):
    d, rc, so, se = run_block(tgt, f'{tgt}')
    total = int(sh(f'samtools view -c -F 2304 {W}/input.bam')[1])
    got = int(sh(f'samtools view -c -F 2304 {d}/matched.bam')[1])
    check(f'coverage-matching target {tgt} (primary count): within 10% of target', rc == 0 and abs(got - tgt) / tgt < 0.10, f'{got} primary reads (total {total}) err={(got-tgt)/tgt:+.1%}')
# (c) edge: target == total, target one below total
tot = int(sh(f'samtools view -c -F 2304 {W}/input.bam')[1])
for tgt in (tot, tot - 1, 1):
    d, rc, so, se = run_block(tgt, f'e{tgt}')
    got = cnt(f'{d}/matched.bam')
    print(f'   edge target={tgt} (total primary {tot}): matched.bam {got} records; rc={rc}; stderr={se.strip()[:60]!r}')
check('target == total -> unchanged copy', cnt(f'{W}/blk_e{tot}/matched.bam') == N)
r = cnt(f'{W}/blk_e{tot-1}/matched.bam')
check('target == total-1: keeps nearly everything (>=90%), not ~0', r / N >= 0.90, f'{r} of {N}')
r = cnt(f'{W}/blk_e1/matched.bam')
print('   target 1 -> matched', r, 'records')
# frac rounds to 1.000000 (the one place the guard leaves open)
sh(f'samtools view -s 1.000000 -b -o {W}/f1.bam {W}/input.bam')
print('   -s 1.000000 (what the snippet would emit if t/n rounds to 1.000000) keeps', cnt(f'{W}/f1.bam'), 'of', N)

# --- pysam subsample recipe (extracted) ---
recipe = block(MD, 'Subsample (Pair-Consistent)', 'python', 'blake2b')
def run_py(seed, fraction, out):
    c = recipe.replace('fraction = 0.1', f'fraction = {fraction}').replace('seed = 42', f'seed = {seed}').replace("'input.bam'", f"'{W}/input.bam'").replace("'subset.bam'", f"'{out}'")
    exec(compile(c, 'pysam_subsample', 'exec'), {})
    return tmpl(out)
sets = {}
for seed in (42, 1, 7, 100, 12345, 0):
    c = run_py(seed, 0.1, f'{W}/py{seed}.bam'); sets[seed] = set(c)
    check(f'pysam seed {seed}: all records of a kept template kept; ~10% templates', all(c[q] == full[q] for q in c) and 0.07 <= len(c) / len(full) <= 0.13, f'{len(c)} templates ({len(c)/len(full):.3f})')
def jac(a, b): return len(a & b) / len(a | b)
js = [jac(sets[a], sets[b]) for a in sets for b in sets if a < b]
check('pysam seeds give independent samples (all pairwise Jaccard < 0.12; independent 10% samples expect 0.053)', max(js) < 0.12, f'max {max(js):.3f} min {min(js):.3f}')
c2 = run_py(42, 0.1, f'{W}/py42b.bam')
check('pysam seed 42 rerun: same template set', set(c2) == sets[42])
check('pysam and samtools -s 42.1 pick DIFFERENT reads (text says so)', jac(sets[42], set(t)) < 0.12, f'Jaccard {jac(sets[42], set(t)):.3f}')
for fr in (0.0, 1.0, 0.5):
    c = run_py(42, fr, f'{W}/pyf.bam')
    print(f'   pysam fraction {fr}: {len(c)} templates of {len(full)} ({len(c)/len(full):.3f})')
check('pysam fraction 1.0 keeps everything, 0.0 keeps nothing', len(run_py(42, 1.0, f'{W}/pyf.bam')) == len(full) and len(run_py(42, 0.0, f'{W}/pyf.bam')) == 0)
# unbiasedness: fraction realised across 12 seeds averages ~0.10
fr = [len(run_py(s, 0.1, f'{W}/pyf.bam')) / len(full) for s in range(200, 212)]
check('pysam fraction unbiased (mean of 12 seeds within 0.09-0.11)', 0.09 <= sum(fr) / len(fr) <= 0.11, f'mean {sum(fr)/len(fr):.4f}')
finish()
