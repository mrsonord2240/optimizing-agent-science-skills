#!/usr/bin/env python3
"""Run EVERY fenced bash/python block of SKILL.md and usage-guide.md verbatim from a scratch copy
(fixtures named as in the docs: input.bam, in.bam, normal.bam, tumor.bam, targets.bed, rg_list.txt, reference.fa).
Records rc, stdout line count, stderr first line. This is only a crash/typo smoke test: correctness is
asserted separately in in1..in7. Human BAM (chr22) is the fixture, so chr1 regions legitimately return nothing."""
import os, re, shutil, subprocess, sys
AFD = os.environ['AFDATA']
SK, W = sys.argv[1], sys.argv[2]
shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
src = f'{AFD}/human/test.paired_end.sorted.bam'
for n in ('input.bam', 'in.bam', 'normal.bam', 'tumor.bam'):
    shutil.copy(src, f'{W}/{n}')
for n in ('input.bam', 'in.bam'):
    shutil.copy(src + '.bai', f'{W}/{n}.bai')
shutil.copy(f'{AFD}/human/genome.fasta', f'{W}/reference.fa'); shutil.copy(f'{AFD}/human/genome.fasta.fai', f'{W}/reference.fa.fai')
open(f'{W}/targets.bed', 'w').write('chr22\t1951\t2100\nchr22\t3000\t3200\n')
open(f'{W}/rg_list.txt', 'w').write('1\n')
rows = []
for fn in ('SKILL.md', 'usage-guide.md'):
    txt = open(f'{SK}/{fn}', encoding='utf-8').read()
    for i, m in enumerate(re.finditer(r'```(bash|python)\n(.*?)```', txt, re.S)):
        lang, code = m.group(1), m.group(2)
        line = txt[:m.start()].count('\n') + 2
        ext = 'sh' if lang == 'bash' else 'py'
        p = f'{W}/blk_{fn[:5]}_{i}.{ext}'
        open(p, 'w').write(code)
        cmd = ['bash', p] if lang == 'bash' else ['python', p]
        r = subprocess.run(cmd, cwd=W, capture_output=True, text=True, timeout=120)
        err = [l for l in r.stderr.splitlines() if l.strip()]
        rows.append((fn, line, lang, r.returncode, len(r.stdout.splitlines()), err[0][:110] if err else ''))
bad = 0
for fn, line, lang, rc, nout, e in rows:
    flag = 'ok ' if rc == 0 and not e else ('WARN' if rc == 0 else 'FAIL')
    if flag != 'ok ': bad += 1
    print(f'{flag} {fn}:{line:<4} {lang:6s} rc={rc} stdout_lines={nout:<5} {e}')
print(f'\n{len(rows)} blocks, {len(rows)-bad} clean, {bad} with warning/failure')
