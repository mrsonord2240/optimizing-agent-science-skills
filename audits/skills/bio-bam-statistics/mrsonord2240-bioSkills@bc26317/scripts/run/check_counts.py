#!/usr/bin/env python3
"""Compare samtools flagstat / stats / idxstats against hand-counted truth, and test the Skill's cross-check equation.
usage: check_counts.py <bam> [--expect-json truth.json]
Prints one line per assertion: PASS/FAIL name observed expected.
"""
import subprocess, re, sys, json
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
from truth import counts

bam = sys.argv[1]
T = counts(bam)


def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


fs_txt = run(f'samtools flagstat {bam}')
print('--- samtools flagstat ---'); print(fs_txt)
fs = {}
for line in fs_txt.splitlines():
    m = re.match(r'(\d+) \+ (\d+) (.*)', line)
    if m:
        key = re.sub(r' \([\d.]+% : .*\)$', '', m.group(3)).strip()
        fs[key] = (int(m.group(1)), int(m.group(2)), line)

sn = {}
for line in run(f'samtools stats {bam}').splitlines():
    if line.startswith('SN\t'):
        _, k, v = line.split('\t')[:3]
        sn[k.rstrip(':')] = v
idx = [l.split('\t') for l in run(f'samtools idxstats {bam}').splitlines()]
print('--- idxstats ---'); print('\n'.join('\t'.join(x) for x in idx))

fails = 0
def chk(name, obs, exp):
    global fails
    ok = obs == exp
    fails += (not ok)
    print(('PASS' if ok else 'FAIL'), name, 'observed=', obs, 'expected=', exp)

# flagstat pairs are (QC-passed, QC-failed)
tot_all = fs['in total (QC-passed reads + QC-failed reads)'][0] + fs['in total (QC-passed reads + QC-failed reads)'][1]
chk('flagstat total(pass+fail) == hand total', tot_all, T['total'])
chk('flagstat secondary == hand', sum(fs['secondary'][:2]), T['secondary'])
chk('flagstat supplementary == hand', sum(fs['supplementary'][:2]), T['supplementary'])
chk('flagstat duplicates == hand', sum(fs['duplicates'][:2]), T['duplicates'])
chk('flagstat mapped == hand mapped(all records)', sum(fs['mapped'][:2]), T['mapped'])
chk('flagstat primary mapped == hand', sum(fs['primary mapped'][:2]), T['primary_mapped'])
chk('flagstat properly paired == hand (primary)', sum(fs['properly paired'][:2]), T['proper_primary'])
chk('flagstat singletons == hand', sum(fs['singletons'][:2]), T['singletons'])
chk('flagstat mate diff chr == hand', sum(fs['with mate mapped to a different chr'][:2]), T['mate_diff_chr'])
chk('flagstat mate diff chr mq5 == hand', sum(fs['with mate mapped to a different chr (mapQ>=5)'][:2]), T['mate_diff_chr_mq5'])
chk('stats raw total sequences == hand primary', int(sn['raw total sequences']), T['primary'])
chk('stats reads QC failed == hand', int(sn['reads QC failed']), T['qcfail'])
chk('stats reads mapped == hand primary_mapped', int(sn['reads mapped']), T['primary_mapped'])
chk('idxstats mapped col sum == hand mapped (all records incl sec/supp)', sum(int(x[2]) for x in idx if len(x) > 3), T['mapped'])
chk('idxstats unmapped col sum == hand unmapped (placed + * lines)', sum(int(x[3]) for x in idx if len(x) > 3), T['unmapped'])
print('idxstats mapped sum', sum(int(x[2]) for x in idx if len(x)>3), ' unmapped col sum', sum(int(x[3]) for x in idx if len(x)>3),
      ' hand mapped(all)', T['mapped'], ' hand unmapped', T['unmapped'])
# Skill's cross-check:   input_read_count = flagstat_total - secondary - supplementary = stats_raw_total_sequences
ftot = fs['in total (QC-passed reads + QC-failed reads)']
lhs_pass_only = ftot[0] - fs['secondary'][0] - fs['supplementary'][0]
lhs_both = ftot[0] + ftot[1] - sum(fs['secondary'][:2]) - sum(fs['supplementary'][:2])
print('SKILL cross-check: flagstat_total(QC-passed col only) - sec - supp =', lhs_pass_only, '; pass+fail version =', lhs_both,
      '; stats raw total sequences =', sn['raw total sequences'])
print('CONTROL (negative control, not scored): QC-passed-column-only form gives', lhs_pass_only, 'vs raw total sequences', int(sn['raw total sequences']), '-> differs when QC-failed reads exist; the Skill now states pass+fail')
chk('Skill cross-check eq holds (pass+fail)', lhs_both, int(sn['raw total sequences']))
print('SUMMARY', bam, 'FAILS=', fails)
print('HAND', json.dumps(T))
