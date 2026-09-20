#!/bin/bash
# Input 7 (NEW, auditor's own truth): the fixer's NEW runnable blocks (biobambam2 bammarkduplicates2, sambamba markdup, pbmarkdup,
# mapDamage --rescale, Picard UmiAwareMarkDuplicatesWithMateCigar) plus the core workflow, on planted truth the fixer never saw.
#  7a  SYNTHETIC planted2.bam (10_make_planted2.py): 5' soft clips, reverse SE reads, mixed PE/SE, near-miss non-dups; truth 140 flagged reads
#  7b  pbmarkdup: see in07b_pbmarkdup.sh
#  7c  mapDamage --rescale on a SYNTHETIC damaged single-end BAM (C>T at 5' ends planted)
#  7d  Picard UmiAware block on the real UMI BAM (planted-truth version is in08)
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W; rm -rf in07; mkdir in07; cd in07
echo "############ 7a planted2.bam"
python $RUN/10_make_planted2.py planted2.bam
mkdir wf; cp planted2.bam wf/input.bam
( cd wf; blk "## Duplicate Marking Workflow" 1 > s.sh; bash -e s.sh; echo "[SKILL.md workflow steps 1-5] records $(samtools view -c marked.bam) flagged $(flagged marked.bam)" )
mkdir pl; cp planted2.bam pl/input.bam
( cd pl; blk "### Pipeline Version (Optimized)" 1 > p.sh; bash p.sh 2>/dev/null; echo "[SKILL.md optimized pipeline] exit=$? records $(samtools view -c marked.bam) flagged $(flagged marked.bam)" )
ASSAY=wgs bash $SK/examples/markdup_pipeline.sh planted2.bam ex_out.bam >/dev/null 2>&1; echo "[shipped example] exit=$? flagged $(flagged ex_out.bam)"
picard MarkDuplicates I=planted2.bam O=pic.bam M=pic.txt >/dev/null 2>&1
echo "[Picard] flagged $(flagged pic.bam); metrics row: $(grep -A1 '^LIBRARY' pic.txt | tail -1 | cut -f1-9 | tr '\t' ' ')"
blk "### biobambam2, sambamba" 1 > bb.sh; echo "[extracted biobambam2/sambamba block]"; cat bb.sh
grep '^bammarkduplicates2' bb.sh | sed 's#input.bam#planted2.bam#; s#O=marked.bam#O=bb.bam#; s#M=metrics.txt#M=bb_metrics.txt#' > bb1.sh
grep '^sambamba' bb.sh | sed 's#input.bam#planted2.bam#; s#marked.bam#sb.bam#' > bb2.sh
cat bb1.sh bb2.sh
extra bash bb1.sh > bb1.out 2> bb1.err; echo "[biobambam2 block] exit=$? flagged $(flagged bb.bam); metrics columns: $(grep -m1 '^LIBRARY' bb_metrics.txt | cut -c1-110)"
echo "   metrics row: $(grep -A1 '^LIBRARY' bb_metrics.txt | tail -1 | cut -f1-9 | tr '\t' ' ')"
bash bb2.sh > bb2.out 2>&1; echo "[sambamba block] exit=$? flagged $(flagged sb.bam)"
samtools collate -O -u planted2.bam col | samtools view -h | samblaster -M 2>samblaster.log | samtools view -b -o sblast.bam -; echo "[samblaster] flagged $(flagged sblast.bam)"
python - <<'PY'
import pysam, itertools
from collections import Counter
def flagged(p): return {(r.query_name, r.flag & 192) for r in pysam.AlignmentFile(p) if r.is_duplicate}
sets = {k: flagged(f) for k, f in [("samtools", "wf/marked.bam"), ("picard", "pic.bam"), ("biobambam2", "bb.bam"), ("sambamba", "sb.bam")]}
for a, b in itertools.combinations(sets, 2):
    print(f"  (name,read1/2) set difference {a} vs {b}: {len(sets[a] ^ sets[b])} of {len(sets[a])} / {len(sets[b])}")
for k in sets:
    c = Counter(n.split("_")[0].rstrip("0123456789c") if n[0] == "E" else n[0] for n, _ in sets[k])
    print(f"  {k:10s} flagged reads per family {dict(sorted(c.items()))}  (truth A 80, B 30, C 0, E1 20, E2 10, F 0)")
PY

echo "############ 7c mapDamage --rescale"
mkdir -p md; cd md
cp $D/human_genome.fasta ref.fa; samtools faidx ref.fa
python $RUN/mk_damage.py
blk "### Ancient DNA: mapDamage rescale after markdup" 1 > md.sh; echo "[extracted mapDamage block]"; cat md.sh
( time bash md.sh ) > md.out 2> md.err; echo "[mapDamage block verbatim] exit=$?  $(grep -E '^real' md.err)"; grep -iE 'Successful|error|Traceback' md.out md.err | head -3
echo "  files: $(ls mapdamage_out | tr '\n' ' ')"
echo "  rescaled bam bytes: $(stat -c %s mapdamage_out/marked.rescaled.bam)  records in/out: $(samtools view -c marked.bam)/$(samtools view -c mapdamage_out/marked.rescaled.bam)"
python $RUN/md_check.py
echo "  5' C>T frequency reported by mapDamage at pos 1: $(head -3 mapdamage_out/5pCtoT_freq.txt | tail -1)"
cd ..

echo "############ 7d Picard UmiAware block verbatim, real UMI BAM"
mkdir -p um; cd um
samtools sort -n -o ns.bam $D/test.paired_end.umi_unsorted.bam; samtools fixmate -m ns.bam fm.bam; samtools sort -o coordsort_fixmate.bam fm.bam
blk "### Picard UMI-aware marking" 1 > um.sh; cat um.sh
bash um.sh > um.out 2> um.err; echo "[Picard UmiAware block] exit=$? flagged $(flagged marked.bam)  records $(samtools view -c marked.bam)/$(samtools view -c coordsort_fixmate.bam)"
grep -iE 'exception|error' um.err | head -3
samtools markdup --barcode-tag RX coordsort_fixmate.bam sm.bam; samtools markdup coordsort_fixmate.bam pm.bam
echo "  samtools --barcode-tag RX flagged $(flagged sm.bam) ; plain samtools markdup flagged $(flagged pm.bam)"
