#!/bin/bash
# Input 6 (scope boundary, regression of pre-fix input 6): assay decision table + multi-library claims, re-run against the FIXED SKILL.md text.
# Adds: the SKILL.md --use-read-groups block verbatim, and a check that the fixed workflow text now gates on assay (Step 0).
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W; rm -rf in06; mkdir in06; cd in06
python $RUN/00_make_synth.py >/dev/null; python $RUN/00b_make_synth2.py
prep() { samtools sort -n -o $1.ns.bam $2 && samtools fixmate -m $1.ns.bam $1.fm.bam && samtools sort -o $1.cs.bam $1.fm.bam; }
echo "### 6a. multi-library pooled marking: synth_multilib.bam (60 pairs, 30 coordinate-colliding pairs from DIFFERENT libraries). Truth: 0 duplicates"
prep ml $D/synth_multilib.bam
samtools markdup ml.cs.bam ml_def.bam; echo "  default samtools markdup:        flagged reads $(samtools view -c -f 1024 ml_def.bam) (over-marking, SKILL.md predicts this)"
samtools markdup --use-read-groups ml.cs.bam ml_rg.bam; echo "  --use-read-groups:               flagged reads $(samtools view -c -f 1024 ml_rg.bam)"
picard MarkDuplicates I=$D/synth_multilib.bam O=ml_pic.bam M=ml_pic.txt >/dev/null 2>&1; echo "  Picard (library aware):          flagged reads $(samtools view -c -f 1024 ml_pic.bam)"
echo "### 6b. same library, two RG IDs (two lanes): synth_samelib_2rg.bam. Truth: 30 dup pairs = 60 reads. SKILL.md: RG-ID keyed samtools vs LB keyed Picard"
prep sl $D/synth_samelib_2rg.bam
samtools markdup sl.cs.bam sl_def.bam; echo "  default:            flagged $(samtools view -c -f 1024 sl_def.bam)"
samtools markdup --use-read-groups sl.cs.bam sl_rg.bam; echo "  --use-read-groups:  flagged $(samtools view -c -f 1024 sl_rg.bam)"
picard MarkDuplicates I=$D/synth_samelib_2rg.bam O=sl_pic.bam M=sl_pic.txt >/dev/null 2>&1; echo "  Picard:             flagged $(samtools view -c -f 1024 sl_pic.bam)"
echo "### 6c. amplicon panel (no UMI), synthetic 1000 pairs / 10 amplicons: SKILL.md says markdup erases the dataset"
prep am $D/synth_amplicon.bam
samtools markdup am.cs.bam am_m.bam; echo "  flagged reads $(samtools view -c -f 1024 am_m.bam) of $(samtools view -c am_m.bam); non-dup reads left: $(samtools view -c -F 1024 am_m.bam)"
samtools markdup -r am.cs.bam am_r.bam; echo "  markdup -r leaves $(samtools view -c am_r.bam) records (coverage collapse from 100x to ~1x per amplicon)"
echo "### 6d. real ARTIC amplicon nanopore BAM (single-end, long reads) through fixmate|markdup as the Skill's workflow would"
prep nano $D/sars-cov-2_v5.3.2.nanopore.bam 2>&1 | tail -3
samtools markdup nano.cs.bam nano_m.bam 2>&1 | head -4; echo "  exit=$?  flagged $(samtools view -c -f 1024 nano_m.bam 2>/dev/null) of $(samtools view -c nano.cs.bam)"
echo "  max read length in BAM: $(samtools view $D/sars-cov-2_v5.3.2.nanopore.bam | awk '{ if (length($10)>m) m=length($10)} END{print m}')  (markdup -l default 300)"
samtools markdup -l 3000 nano.cs.bam nano_m2.bam 2>&1 | head -3; echo "  with -l 3000: flagged $(samtools view -c -f 1024 nano_m2.bam 2>/dev/null)"
echo "### 6e. bulk RNA-seq real PE BAM (SKILL.md: do NOT mark; duplicates are biological)"
prep rna $D/test.rna.paired_end.sorted.bam 2>&1 | tail -2
samtools markdup rna.cs.bam rna_m.bam 2>&1 | head -3; echo "  flagged $(samtools view -c -f 1024 rna_m.bam) of $(samtools view -c rna_m.bam) records"
picard MarkDuplicates I=$D/test.rna.paired_end.sorted.bam O=rna_pic.bam M=rna_pic.txt >/dev/null 2>&1; echo "  Picard flagged $(samtools view -c -f 1024 rna_pic.bam)"
python - <<'PY'
import pysam, collections
b = pysam.AlignmentFile("rna_m.bam"); tot = collections.Counter(); dup = collections.Counter()
for r in b:
    if r.is_unmapped or r.is_secondary or r.is_supplementary: continue
    bin_ = r.reference_start // 500
    tot[bin_] += 1; dup[bin_] += r.is_duplicate
top = sorted(tot, key=lambda k: -tot[k])[:3]
for k in top: print(f"  500bp bin {k*500}: {tot[k]} primary reads, {dup[k]} flagged ({dup[k]/tot[k]*100:.0f}%) -> highest-expression locus loses signal")
PY
echo "### 6f fixed-Skill text: is there now an assay gate in the workflow and in usage-guide?"
grep -n 'Step 0' $SK/SKILL.md $SK/usage-guide.md | cut -c1-260
echo "### 6g SKILL.md multi-library block, verbatim (in.bam/out.bam substituted), on the multilib BAM"
blk "## Multi-Library Pooled Marking" 1 | sed 's#in.bam#ml.cs.bam#; s#out.bam#ml_blk.bam#' > mlblk.sh; cat mlblk.sh; bash mlblk.sh 2>/dev/null; echo "  flagged $(samtools view -c -f 1024 ml_blk.bam) (truth 0)"
