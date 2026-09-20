"""Build forced-failure variants of SKILL.md's rmats2sashimiplot block (b04.sh) for Input 3.
A: no --group-info line (2 colours for 6 replicates)     B: --group-info points at a missing file
C: old flag -t SE                                          D: no --group-info and --color with 2 colours but 4 replicates (mismatch)
"""
import sys
s = open('b04.sh').read()
GI = "    --group-info grouping.gf \\\n"
assert GI in s, 'group-info line not found'


def out(name, txt, d):
    txt = txt.replace('-o sashimi_rmats', f'-o {d}').replace('sashimi_rmats/Sashimi_plot', f'{d}/Sashimi_plot')
    open(name, 'w', newline='\n').write(txt)


out('b04_failA.sh', s.replace(GI, ''), 'sashimi_failA')
out('b04_failB.sh', s.replace('--group-info grouping.gf', '--group-info nofile.gf'), 'sashimi_failB')
out('b04_failC.sh', s.replace('--event-type SE', '-t SE'), 'sashimi_failC')
# D: no group info AND one label but colours = 2 while bams = 3 + 3 and l1/l2 given: same as A; variant with --color removed entirely
out('b04_failD.sh', s.replace(GI, '').replace("    --color '#1f77b4,#ff7f0e'\n", "    --color '#1f77b4'\n"), 'sashimi_failD')
