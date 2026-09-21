#!/bin/bash
# SKILL.md DROP block (blocks/05_bash.sh), init part, in as-drop: mkdir + cd + drop init, then check every config claim
W=/mnt/openscience/audits/bio-outlier-splicing-detection/run/drop_init; rm -rf $W; mkdir -p $W; cd $W
export PYTHONDONTWRITEBYTECODE=1
D="micromamba run -n as-drop"
$D drop --version
mkdir my_diagnostic_run && cd my_diagnostic_run
$D drop init 2>&1 | tail -n 6
ls -a
echo "--- config claims"
python3 - <<'PY'
import re
t = open('config.yaml').read()
def block(name):
    m = re.search(r'^%s:\n((?:[ \t-].*\n|\n)*)' % name, t, re.M); return m.group(1) if m else ''
for name in ('aberrantSplicing', 'aberrantExpression', 'mae'):
    b = block(name)
    print(name, '| run:', re.search(r'^\s+run:\s*(\S+)', b, re.M).group(1), '| implementation:', (re.search(r'^\s+implementation:\s*(\S+)', b, re.M) or [None, 'n/a'])[1],
          '| FRASER_version:', (re.search(r'FRASER_version:\s*(\S+)', b) or [None, 'n/a'])[1], '| padjCutoff:', (re.search(r'padjCutoff:\s*(\S+)', b) or [None, 'n/a'])[1],
          '| deltaPsiCutoff:', (re.search(r'deltaPsiCutoff:\s*(\S+)', b) or [None, 'n/a'])[1])
for k in ('sampleAnnotation', 'geneAnnotation', 'genome', 'root', 'htmlOutputPath'):
    print('top-level key', k, ':', 'FOUND' if re.search(r'^%s:' % k, t, re.M) or re.search(r'^\s+%s:' % k, t, re.M) else 'MISSING')
PY
echo "files containing conda: directive = $(grep -rl '^ *conda:' Scripts 2>/dev/null | wc -l)"
echo "--- snakemake target exists? (dry run, init'd project has no data so expect missing-input, not unknown target)"
$D snakemake -n aberrantSplicing --cores 4 2>&1 | tail -n 8 | cut -c1-200
$D snakemake --list-target-rules 2>/dev/null | grep -i "aberrantSplicing\|aberrantExpression\|^mae" | head
