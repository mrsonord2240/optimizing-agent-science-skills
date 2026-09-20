#!/usr/bin/env python
"""
Input 3 (edge): strandedness verification with RSeQC infer_experiment.py on SYNTHETIC PE BAMs of known protocol
(dUTP / forward / unstranded / 20% and 40% leakage), the real chrX GEUVADIS data, and failure modes (contig-name mismatch,
BED6 instead of BED12, tiny BAM, -q semantics).  Then applies the SKILL.md decision table mechanically.
Run: asenv as-core python input3_strandedness.py
"""
import sys, os, re, json, subprocess, shutil
sys.dont_write_bytecode = True
RUN = '/mnt/openscience/audits/bio-splicing-qc/run'
D = f'{RUN}/data/synthetic'
AS = '/mnt/openscience/audit-envs/alternative-splicing/public-data'
W = f'{RUN}/work/in3'
shutil.rmtree(W, ignore_errors=True)
os.makedirs(W)
import pysam

def infer(bam, bed, extra=()):
    r = subprocess.run(['infer_experiment.py', '-i', bam, '-r', bed, *extra], capture_output=True, text=True)
    return r

def parse(txt):
    d = {}
    m = re.search(r'This is (\w+) Data', txt); d['layout'] = m.group(1) if m else None
    m = re.search(r'failed to determine:\s*([\d.]+)', txt); d['failed'] = float(m.group(1)) if m else None
    fr = re.findall(r'Fraction of reads explained by "([^"]+)":\s*([\d.]+)', txt)
    d['fractions'] = {k: float(v) for k, v in fr}
    return d

def skill_table(d):
    """SKILL.md 'Strandedness Verification' table applied to the parsed output (PE naming for both layouts)"""
    fs = d['fractions']
    if not fs:
        return 'NO OUTPUT / cannot parse', None
    fwd = [v for k, v in fs.items() if k in ('1++,1--,2+-,2-+', '++,--')]
    rev = [v for k, v in fs.items() if k in ('1+-,1-+,2++,2--', '+-,-+')]
    f, r = (fwd[0] if fwd else 0), (rev[0] if rev else 0)
    if f >= 0.9:
        return 'forward-stranded -> rMATS fr-secondstrand', (f, r)
    if r >= 0.9:
        return 'reverse-stranded -> rMATS fr-firststrand', (f, r)
    if abs(f - r) < 0.15:
        return 'unstranded -> fr-unstranded', (f, r)
    return f'ambiguous (fwd {f:.2f}, rev {r:.2f}; Quality-threshold table: 70-90% acceptable)', (f, r)

res = {}
bed = f'{D}/synth.bed12'
for nm, truth in [('dutp', 'reverse (dUTP) 100%'), ('fwd', 'forward 100%'), ('unstr', 'unstranded 50/50'),
                  ('dutp_leak20', 'reverse 80%'), ('dutp_leak40', 'reverse 60%')]:
    r = infer(f'{D}/pe_{nm}.bam', bed)
    p = parse(r.stdout + r.stderr)
    call, fr = skill_table(p)
    res[nm] = dict(truth=truth, rc=r.returncode, parsed=p, skill_call=call)
    print(f'{nm:12s} truth={truth:22s} rc={r.returncode} {p}  -> {call}', flush=True)

# SE library (unstranded synthetic SE junction BAM has random strand flags)
r = infer(f'{D}/se_clean.bam', bed)
p = parse(r.stdout + r.stderr); print('SE se_clean (random strand flags):', p, skill_table(p)[0])
res['se_clean'] = dict(parsed=p, skill_call=skill_table(p)[0])

# REAL chrX GEUVADIS (unstranded, per TOOLS.md 0.46/0.45)
r = infer(f'{AS}/derived/xs_bams/ERR188383.xs.bam', f'{AS}/derived/chrX.bed12')
p = parse(r.stdout + r.stderr); print('REAL chrX ERR188383:', p, skill_table(p)[0])
print(r.stdout[-600:] + r.stderr[-300:])
res['real_chrX'] = dict(parsed=p, skill_call=skill_table(p)[0])
# the Skill's exact command has -s 200000 (the default); chrX BAM has ~100k records -> fewer than -s
# real chrX, Skill's own command line
r = infer(f'{AS}/derived/xs_bams/ERR188383.xs.bam', f'{AS}/derived/chrX.bed12', ['-s', '200000'])
print('real chrX with -s 200000 stdout:', r.stdout.strip().replace('\n', ' | '), '| stderr:', r.stderr.strip()[-200:])

# ---- failure modes
# 1. contig-name mismatch
r = infer(f'{D}/pe_dutp.bam', f'{D}/synth_nochr.bed12')
print('MISMATCH contig  rc=%d stdout=%r stderr_tail=%r' % (r.returncode, r.stdout.strip()[-300:], r.stderr.strip()[-200:]))
p = parse(r.stdout + r.stderr); res['mismatch'] = dict(rc=r.returncode, parsed=p, stdout=r.stdout[-300:], stderr=r.stderr[-300:], skill_call=skill_table(p)[0])
print('   skill decision on this output:', skill_table(p)[0])
# 2. BED6 instead of BED12
r = infer(f'{D}/pe_dutp.bam', f'{D}/synth.bed6')
print('BED6  rc=%d stdout=%r stderr_tail=%r' % (r.returncode, r.stdout.strip()[-300:], r.stderr.strip()[-300:]))
res['bed6'] = dict(rc=r.returncode, stdout=r.stdout[-300:], stderr=r.stderr[-300:])
# 3. GTF instead of BED
gtf = f'{AS}/rnasplice/reference/genes_chrX.gtf'
r = infer(f'{AS}/derived/xs_bams/ERR188383.xs.bam', gtf)
print('GTF  rc=%d stdout=%r stderr_tail=%r' % (r.returncode, r.stdout.strip()[-300:], r.stderr.strip()[-300:]))
res['gtf'] = dict(rc=r.returncode, stdout=r.stdout[-300:], stderr=r.stderr[-300:])
# 4. -q semantics: MAPQ 3 multimappers. Skill fix: "use -q 30 to filter by quality" (default is already 30).
r30 = infer(f'{D}/pe_rrna.bam', bed)   # rRNA reads are outside the BED; use pe_dutp with modified MAPQ instead
# rewrite pe_dutp with MAPQ 1 everywhere
src = f'{D}/pe_dutp.bam'; dst = f'{W}/pe_dutp_mapq1.bam'
with pysam.AlignmentFile(src) as fi, pysam.AlignmentFile(dst, 'wb', template=fi) as fo:
    for rd in fi:
        rd.mapping_quality = 1
        fo.write(rd)
pysam.index(dst)
a = infer(dst, bed); b = infer(dst, bed, ['-q', '0'])
print('MAPQ1 BAM default(-q30):', parse(a.stdout + a.stderr), '| stdout tail:', a.stdout.strip()[-200:].replace('\n', ' | '))
print('MAPQ1 BAM -q 0        :', parse(b.stdout + b.stderr))
res['mapq'] = dict(default=parse(a.stdout + a.stderr), q0=parse(b.stdout + b.stderr), default_rc=a.returncode)
# 5. tiny BAM (fewer reads than -s): 300 reads
tiny = f'{W}/tiny.bam'
with pysam.AlignmentFile(f'{D}/pe_dutp.bam') as fi, pysam.AlignmentFile(tiny, 'wb', template=fi) as fo:
    for i, rd in enumerate(fi):
        if i >= 300:
            break
        fo.write(rd)
pysam.index(tiny)
t = infer(tiny, bed)
print('TINY(300 recs) rc=%d parsed=%s' % (t.returncode, parse(t.stdout + t.stderr)))
res['tiny'] = dict(rc=t.returncode, parsed=parse(t.stdout + t.stderr))
json.dump(res, open(f'{RUN}/work/input3_result.json', 'w'), indent=1, default=str)
