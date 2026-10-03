#!/bin/bash
# Audit run 1 (initial) for bio-splicing-quantification. Run inside WSL `science` via wsl_run.sh.
# Inputs: ecosystem staging (read-only). Outputs: ../out/ only.
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
D=$AS/public-data; R=$D/rnasplice; P=$D/planted
SKILL=/mnt/openscience/wt/norm-bio-splicing-quantification/skills/bio-splicing-quantification
RUN=/mnt/openscience/audits/bio-splicing-quantification/run-initial-1
O=$RUN/out; mkdir -p $O; cd $O
CB=/home/sci/micromamba/envs/as-core/bin
echo "== versions"; micromamba run -n as-core rmats.py --version 2>&1 | tail -1; micromamba run -n as-core python -c "import pandas,statsmodels;print('as-core pandas',pandas.__version__,'statsmodels',statsmodels.__version__)"
micromamba run -n as-suppa python -c "import pandas,statsmodels;print('as-suppa pandas',pandas.__version__,'statsmodels',statsmodels.__version__)"

echo "== A. rMATS real chrX 2v2, Skill command flags (readLength 75, paired)"
mkdir -p rmats_real/out rmats_real/tmp
echo "$R/bam/ERR188383.Aligned.out.bam,$R/bam/ERR188428.Aligned.out.bam" > rmats_real/b1.txt
echo "$R/bam/ERR188454.Aligned.out.bam,$R/bam/ERR204916.Aligned.out.bam" > rmats_real/b2.txt
micromamba run -n as-core rmats.py --b1 rmats_real/b1.txt --b2 rmats_real/b2.txt --gtf $R/reference/genes_chrX.gtf -t paired --readLength 75 \
  --variable-read-length --libType fr-firststrand --nthread 8 --od rmats_real/out --tmp rmats_real/tmp --novelSS --statoff > rmats_real/rmats.log 2>&1
echo "rmats real rc=$?"; wc -l rmats_real/out/*.MATS.JC.txt

echo "== B. rMATS planted (hand-checkable)"
mkdir -p rmats_planted/out rmats_planted/tmp
micromamba run -n as-core rmats.py --b1 $P/b1.txt --b2 $P/b2.txt --gtf $P/planted.gtf -t single --readLength 50 --nthread 2 --od rmats_planted/out --tmp rmats_planted/tmp --libType fr-unstranded --statoff > rmats_planted/rmats.log 2>&1
echo "rmats planted rc=$?"

echo "== C. SUPPA2 planted + chrX through scripts/quantify_splicing.py (as-suppa)"
mkdir -p suppa
micromamba run -n as-suppa python $RUN/scripts/mk_tpm.py $R suppa
cat > suppa/run_skill_script.py <<PYEOF
import sys
sys.path.insert(0, '$SKILL/scripts')
import quantify_splicing as q
for tag, gtf, tpm in [('planted', '$P/planted.gtf', '$P/planted_tpm.txt'), ('chrX', '$R/reference/genes_chrX.gtf', 'suppa/chrX_tpm.tsv')]:
    files = q.run_suppa2_quantification(gtf, tpm, f'suppa/{tag}')
    print(tag, 'psi files', sorted(files))
PYEOF
micromamba run -n as-suppa python suppa/run_skill_script.py 2>&1 | grep -v '^$' | tail -8
echo "planted SE PSI:"; cat suppa/planted_psi_SE.psi

echo "== D. SUPPA2 TPM header trap + statsmodels in as-core"
printf 'Name\tA\tB\tC\nT_inc\t80\t20\t50\nT_skip\t20\t80\t50\n' > suppa/tpm_pandas_default_header.tsv
micromamba run -n as-suppa suppa.py psiPerEvent -i suppa/planted_SE_strict.ioe -e suppa/tpm_pandas_default_header.tsv -o suppa/hdrtest 2>&1 | tail -3; ls suppa/hdrtest.psi 2>&1 | head -1
echo "-- as-core suppa.py psiPerEvent (statsmodels 0.15?)"
micromamba run -n as-core suppa.py psiPerEvent -i suppa/planted_SE_strict.ioe -e $P/planted_tpm.txt -o suppa/core_try 2>&1 | tail -4

echo "== E. regtools/leafcutter: STAR BAM without XS tags (Skill route) vs XS-tagged"
mkdir -p lc_noxs lc_xs
for s in ERR188383 ERR188428 ERR188454 ERR204916; do
  $CB/regtools junctions extract -a 8 -m 50 -s XS $R/bam/$s.Aligned.out.bam -o lc_noxs/$s.junc 2> lc_noxs/$s.err; echo "$s noXS rc=$? junc_lines=$(wc -l < lc_noxs/$s.junc) strand_col_counts: $(tail -n +2 lc_noxs/$s.junc | cut -f6 | sort | uniq -c | tr '\n' ' ')"
  $CB/regtools junctions extract -a 8 -m 50 -s XS $D/derived/xs_bams/$s.xs.bam -o lc_xs/$s.junc 2> lc_xs/$s.err; echo "$s XS rc=$? junc_lines=$(wc -l < lc_xs/$s.junc) strand_col_counts: $(tail -n +2 lc_xs/$s.junc | cut -f6 | sort | uniq -c | tr '\n' ' ')"
done
LC=$AS/tools/bin/leafcutter_cluster_regtools.py
for v in lc_noxs lc_xs; do (cd $v; ls *.junc > juncfiles.txt
  bash $LC -j juncfiles.txt -o leafcutter -m 50 -l 500000 > cluster.log 2>&1; echo "$v cluster rc=$? clusters=$(($(zcat leafcutter_perind.counts.gz 2>/dev/null | wc -l)-1))"
  tail -2 cluster.log | cut -c1-200); done

echo "== F. IRFinder syntax: Skill reference literal vs real CLI (reference reused read-only)"
REF=$AS/logs/smoke_irfinder/ref
mkdir -p irf; 
echo "-- literal: IRFinder FastQ -r REF -d out sample.fastq"
timeout 300 bash $AS/tools/bin/IRFinder FastQ -r $REF -d $O/irf/literal $R/fastq/ERR188383_chrX_1.fastq.gz > irf/literal.log 2>&1; echo "literal rc=$?"; tail -5 irf/literal.log | cut -c1-200; ls irf/literal 2>&1 | head -3
echo "-- IRFinder --version"; bash $AS/tools/bin/IRFinder --version 2>&1 | head -2
echo "== done"
