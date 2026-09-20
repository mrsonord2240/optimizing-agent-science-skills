#!/bin/bash
cd /mnt/openscience/audits/bio-bam-statistics/run
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
{
echo "== SKILL: '\`reads mapped and paired\` - Properly paired'.  synth.bam (480 proper-flagged primary reads incl 20 QC-fail; 500 both-mapped)"
samtools stats data/synth.bam | grep -E "^SN\s(reads mapped and paired|reads properly paired|reads paired|reads QC failed|non-primary|supplementary|reads duplicated|filtered)" | cut -f2-3
echo "== insert size average: stats default (-m 0.99) vs -m 1.0 vs Skill pysam snippet, human real BAM"
samtools stats work/test.paired_end.sorted.bam | grep -E "^SN\sinsert size average"| cut -f2-3
samtools stats -m 1.0 work/test.paired_end.sorted.bam | grep -E "^SN\sinsert size average"| cut -f2-3
python -c "
import skill_snippets as s; s.skill_insert_size('work/test.paired_end.sorted.bam')"
echo "== stats -d / -F flags: exclude dups? (1000g has 101 dup-flagged)"
samtools stats work/batch/g1000.bam | grep -E "^SN\s(raw total|reads duplicated|reads mapped:)" | cut -f2-3
samtools stats -d work/batch/g1000.bam | grep -E "^SN\s(raw total|reads duplicated|filtered)" | cut -f2-3
echo "== duplicates % : flagstat prints no dup percentage; Skill dup-rate vs QC threshold table uses dup/total.  1000g: dup reads / primary"
python - <<'PY'
import sys; sys.path.insert(0,'.')
from truth import counts
T = counts('work/batch/g1000.bam'); print({k: T[k] for k in ('total','primary','secondary','duplicates','primary_duplicates')}, 'dup rate primary = %.3f%%' % (100*T['primary_duplicates']/T['primary']), ' dup/total (qc_report.py) = %.3f%%' % (100*T['duplicates']/T['total']))
PY
} > out/t9_stats_fields.txt 2>&1; cat out/t9_stats_fields.txt
