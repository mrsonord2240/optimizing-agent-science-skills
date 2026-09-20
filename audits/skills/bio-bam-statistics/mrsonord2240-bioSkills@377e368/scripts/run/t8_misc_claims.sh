#!/bin/bash
# Spot-check of remaining SKILL.md factual claims: mosdepth --flag default and supplementary handling, samtools depth -q/-Q meaning,
# `samtools coverage -H`, `depth -s` semantics, qc_report.py determinism and clean-copy run, py_compile of shipped script.
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; cd $R/work; D=$R/data
mosdepth --help 2>&1 | grep -E -- '--flag|--mapq|--fast-mode|--use-median|--quantize|--thresholds' | head -8
echo "--- supplementary handling: synth.bam has 10 supplementary 50M50S on synth2 (50 bp each = 500 bases)"
mosdepth -t 1 ms1 $D/synth.bam; grep synth2 ms1.mosdepth.summary.txt
mosdepth -t 1 --flag 3844 ms2 $D/synth.bam; grep synth2 ms2.mosdepth.summary.txt
samtools depth -aa -r synth2 $D/synth.bam | awk '{s+=$3} END{print "samtools depth synth2 sum (supp included):", s}'
echo "  planted truth synth2 default-depth total: 3500 (incl 10 supp x 50 = 500)"
samtools depth --help 2>&1 | grep -E -- '-q|-Q|-J|-s ' | head -6
samtools coverage --help 2>&1 | grep -E -- ' -H| -m| -r| -b' | head -5
echo "--- shipped qc_report.py: py_compile from the copy, and two runs byte-identical"
python -m py_compile $R/skill/examples/qc_report.py && echo "py_compile OK"; rm -rf $R/skill/examples/__pycache__
B=$AFDATA/human/test.paired_end.sorted.bam
python $R/skill/examples/qc_report.py $B > q1.txt; python $R/skill/examples/qc_report.py $B > q2.txt; cmp q1.txt q2.txt && echo "qc_report deterministic (identical)"
python $R/skill/examples/qc_report.py; echo "no-arg rc=$?"
python $R/skill/examples/qc_report.py /nonexistent.bam 2>&1 | tail -2; echo "missing-file rc=${PIPESTATUS[0]}"
echo "--- every file the Skill points at exists (shipped-means-present)"
ls -l $R/skill $R/skill/examples
grep -n 'examples/qc_report.py' $R/skill/SKILL.md $R/skill/usage-guide.md | cut -c1-120
for s in sam-bam-basics alignment-indexing alignment-validation duplicate-handling alignment-filtering sequence-io/sequence-statistics; do d=/mnt/openscience/external/mrsonord2240__bioSkills; ls -d $d/*/$(basename $s) 2>/dev/null || ls -d $d/$s 2>/dev/null || echo "MISSING related skill $s"; done
echo "--- security grep on shipped code"; grep -nE 'eval\(|exec\(|os\.system|subprocess|shell=True|password|token|api[_-]?key|rm -rf' $R/skill/examples/qc_report.py $R/skill/SKILL.md $R/skill/usage-guide.md | head
find $R/skill -name __pycache__ | head -2
