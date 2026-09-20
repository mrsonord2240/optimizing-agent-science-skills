#!/bin/bash
# The Skill's DROP setup block: `drop init my_diagnostic_run` -> inspect config.yaml keys the Skill tells the user to edit.
W=/mnt/openscience/audits/bio-outlier-splicing-detection/run/drop_init; rm -rf $W; mkdir -p $W; cd $W
export PYTHONDONTWRITEBYTECODE=1
D="micromamba run -n as-drop"
$D drop --version
echo "== verbatim Skill command:"; $D drop init my_diagnostic_run 2>&1 | tail -4; echo "rc=$?"
echo "== corrected: mkdir + cd + drop init (no positional argument)"
mkdir my_diagnostic_run; cd my_diagnostic_run; $D drop init --help | head -12; $D drop init 2>&1 | tail -4; ls -a
echo "--- config.yaml keys (aberrantSplicing / aberrantExpression / mae blocks)"
grep -n -A28 '^aberrantSplicing' config.yaml | head -50
grep -n -B1 -A6 '^aberrantExpression' config.yaml | head -14
grep -n -A3 '^mae' config.yaml | head
echo "--- sample_annotation columns"; ls; head -2 sample_annotation.tsv 2>/dev/null; ls Data 2>/dev/null
echo "--- conda directives in DROP rules? (Skill says: snakemake --use-conda)"
grep -rln 'conda:' Scripts 2>/dev/null | head; grep -rn '^ *conda:' Scripts 2>/dev/null | head -3; echo "count files with conda: $(grep -rl 'conda:' Scripts 2>/dev/null | wc -l)"
echo "--- drop demo/init help"; $D drop --help 2>&1 | head -20
