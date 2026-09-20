#!/usr/bin/env python3
"""For each BAM: compare the Skill's pysam counters (SKILL.md 'Count Reads' block 028 and the shipped examples/qc_report.py)
with `samtools flagstat -O tsv` (QC-passed column, percentages as printed by flagstat) AND with hand counts from record
flags (regress/truth.py). Prints PASS/FAIL per BAM with every mismatching field.
usage: t_qc_vs_flagstat.py <bam> [<bam> ...]"""
import sys, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from truth import counts


def flagstat(bam):
    out = subprocess.run(['samtools', 'flagstat', '-O', 'tsv', bam], capture_output=True, text=True).stdout
    d = {}
    for l in out.splitlines():
        a = l.split('\t')
        d[a[2]] = (a[0], a[1])
    return d


def run_block(script, bam):
    src = open(script, encoding='utf-8').read().replace("'input.bam'", repr(bam))
    p = subprocess.run([sys.executable, '-c', src], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def run_script(script, bam):
    p = subprocess.run([sys.executable, script, bam], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def num(x):
    return int(x.replace(',', ''))


tot_fail = 0
for bam in sys.argv[1:]:
    fs = flagstat(bam)
    T = counts(bam)
    P = lambda k: int(fs[k][0])
    PF = lambda k: int(fs[k][0]) + int(fs[k][1])
    fails = []

    def chk(name, obs, exp):
        if obs != exp:
            fails.append(f'{name}: got {obs!r} expected {exp!r}')

    chk('flagstat primary(pass+fail) vs hand', PF('primary'), T['primary'])
    chk('flagstat primary mapped(pass+fail) vs hand', PF('primary mapped'), T['primary_mapped'])
    # ---- block 028 Count Reads
    rc, out, err = run_block(os.path.join(HERE, 'blocks', '028_python.py'), bam)
    m = re.search(r'Primary QC-passed: (\d+)', out)
    if P('primary') == 0:
        chk('028: exits with a message on 0 QC-passed primary (no traceback)',
            rc != 0 and 'Traceback' not in err and 'no QC-passed primary' in (out + err), True)
    else:
        chk('028 rc', rc, 0)
        if m:
            chk('028 primary QC-passed', int(m.group(1)), P('primary'))
            mm = re.search(r'Mapped: (\d+) \(([\d.]+)% of primary\)', out)
            chk('028 mapped', int(mm.group(1)), P('primary mapped'))
            chk('028 mapped %', mm.group(2) + '%', fs.get('primary mapped %', ('?',))[0])
            if P('paired in sequencing') > 0:
                pm = re.search(r'Properly paired: (\d+) \(([\d.]+)% of primary paired\)', out)
                chk('028 proper', int(pm.group(1)), P('properly paired'))
                chk('028 proper %', pm.group(2) + '%', fs['properly paired %'][0])
            else:
                chk('028 SE message', 'Single-end data' in out, True)
        else:
            fails.append('028 printed no Primary line: ' + out[:80] + err[-120:])
    # ---- qc_report.py
    rc2, out2, err2 = run_script(os.path.join(HERE, 'skill', 'examples', 'qc_report.py'), bam)
    chk('qc_report rc', rc2, 0)
    if 'Traceback' in err2:
        fails.append('qc_report traceback: ' + err2.strip().splitlines()[-1])
    g = lambda pat: re.search(pat, out2)
    mt = g(r'Total records:\s+([\d,]+) \(primary ([\d,]+) \+ secondary ([\d,]+) \+ supplementary ([\d,]+)\)')
    if mt:
        chk('qc total records', num(mt.group(1)), PF('total (QC-passed reads + QC-failed reads)'))
        chk('qc primary', num(mt.group(2)), PF('primary'))
        chk('qc secondary', num(mt.group(3)), PF('secondary'))
        chk('qc supplementary', num(mt.group(4)), PF('supplementary'))
        q = g(r'QC-failed primary:\s+([\d,]+)')
        chk('qc qcfail primary', num(q.group(1)), int(fs['primary'][1]))
        q = g(r'QC-passed primary:\s+([\d,]+)')
        chk('qc passed primary', num(q.group(1)), P('primary'))
        if P('primary') > 0:
            q = g(r'Mapped:\s+([\d,]+) \(([\d.]+|n/a)')
            chk('qc mapped', num(q.group(1)), P('primary mapped'))
            chk('qc mapped %', q.group(2) + '%', fs['primary mapped %'][0])
            q = g(r'Properly paired:\s+([\d,]+) \(([\d.]+|n/a)')
            chk('qc proper', num(q.group(1)), P('properly paired'))
            if P('paired in sequencing'):
                chk('qc proper %', q.group(2) + '%', fs['properly paired %'][0])
            else:
                chk('qc proper % n/a for SE', q.group(2), 'n/a')
            q = g(r'Duplicates:\s+([\d,]+)')
            chk('qc dup', num(q.group(1)), P('primary duplicates'))
        else:
            chk('qc says nothing to report', 'nothing to report' in out2, True)
    else:
        fails.append('qc_report header not parsed: ' + out2[:100])
    tot_fail += len(fails)
    print(f'{"PASS" if not fails else "FAIL"} {os.path.basename(bam)}  primary={P("primary")} qcfail={fs["primary"][1]} '
          f'sec={PF("secondary")} supp={PF("supplementary")} 028rc={rc} qc_report_rc={rc2}'
          + ('' if not fails else '\n   ' + '\n   '.join(fails)))
print('TOTAL_MISMATCHES', tot_fail)
