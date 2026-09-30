# Re-audit: fail-fast guards, QC gate (own synthetic + fixer's real 2-epoch metrics), fresh-start behaviours
source /mnt/openscience/audit-envs/bio-atac-seq-deep-learning-atac/scripts/env.sh
export PATH=/home/sci/micromamba/envs/dlatac-tf/bin:$PATH
S=/mnt/openscience/wt/atac-deep-learning-atac/skills/bio-atac-seq-deep-learning-atac/scripts
P=$ME/public-cache/pseudo; R=$ME/run/reaudit; G=$R/guards; rm -rf $G; mkdir -p $G
V=$ME/run/skillscript/variants_pseudo.tsv
cut -f1-4 $V > $G/v4.tsv; cut -f1-3 $P/pseudo.narrowPeak > $G/p3.bed
t(){ local s=$(date +%s); "$@" >$G/last.log 2>&1; local e=$?; echo "  exit=$e in $(( $(date +%s)-s ))s :: $(tail -1 $G/last.log | cut -c1-160)"; }
echo "a missing BAM";     t bash $S/chrombpnet_pipeline.sh $G/nope.bam $P/pseudo.narrowPeak $P/pseudo.fa $P/pseudo.chrom.sizes $G/o1
echo "b 3-col peaks";     t bash $S/chrombpnet_pipeline.sh $P/pseudo.bam $G/p3.bed $P/pseudo.fa $P/pseudo.chrom.sizes $G/o2
echo "c 4-col VARIANTS";  VARIANTS=$G/v4.tsv VARIANT_SCORER=$ME/src/variant-scorer t bash $S/chrombpnet_pipeline.sh $P/pseudo.bam $P/pseudo.narrowPeak $P/pseudo.fa $P/pseudo.chrom.sizes $G/o3
echo "d placeholder scorer"; VARIANTS=$V VARIANT_SCORER=/path/to/variant-scorer t bash $S/chrombpnet_pipeline.sh $P/pseudo.bam $P/pseudo.narrowPeak $P/pseudo.fa $P/pseudo.chrom.sizes $G/o4
echo "e stale nonpeaks_auxiliary"; mkdir -p $G/o5/nonpeaks_auxiliary; t bash $S/chrombpnet_pipeline.sh $P/pseudo.bam $P/pseudo.narrowPeak $P/pseudo.fa $P/pseudo.chrom.sizes $G/o5
echo "f no chrombpnet on PATH"; PATH=/usr/bin:/bin t bash $S/chrombpnet_pipeline.sh $P/pseudo.bam $P/pseudo.narrowPeak $P/pseudo.fa $P/pseudo.chrom.sizes $G/o6
echo "g already trained OUTDIR (no RESUME)"; mkdir -p $G/o7/bias/models; t bash $S/chrombpnet_pipeline.sh $P/pseudo.bam $P/pseudo.narrowPeak $P/pseudo.fa $P/pseudo.chrom.sizes $G/o7
echo "== QC gate: own synthetic files (planted truth by construction)"
Q=$G/qc; mkdir -p $Q
echo '{"counts_metrics":{"peaks":{"pearsonr":-0.1}}}' > $Q/bias_ok.json
echo '{"counts_metrics":{"peaks":{"pearsonr":-0.4}}}' > $Q/bias_border.json
echo '{"counts_metrics":{"peaks":{"pearsonr":-0.35}}}' > $Q/bias_bad.json
echo '{"counts_metrics":{"regions":{"pearsonr":0.62}},"profile_metrics":{"regions":{"median_norm_jsd":0.41}}}' > $Q/m_pred_ok.json
echo '{"counts_metrics":{"peaks":{"pearsonr":0.62}},"profile_metrics":{"peaks":{"median_norm_jsd":0.41}}}' > $Q/m_train_ok.json
echo '{"counts_metrics":{"regions":{"pearsonr":0.49}},"profile_metrics":{"regions":{"median_norm_jsd":0.41}}}' > $Q/m_low.json
echo 'corrected_0.0012' > $Q/r_ok.txt; echo 'uncorrected_0.0041' > $Q/r_bad.txt
g(){ python3 $S/chrombpnet_qc_gate.py "$@" >$Q/o.txt 2>&1; echo "  exit=$? :: $(grep -c PASS $Q/o.txt) PASS $(grep -c FAIL $Q/o.txt) FAIL"; }
echo "all ok (pred_bw 'regions' key) expect 0"; g $Q/bias_ok.json $Q/m_pred_ok.json $Q/r_ok.txt
echo "all ok (train 'peaks' key) expect 0"; g $Q/bias_ok.json $Q/m_train_ok.json $Q/r_ok.txt
echo "bias -0.35 expect 0? threshold >-0.3 so FAIL expect 1"; g $Q/bias_bad.json $Q/m_pred_ok.json $Q/r_ok.txt
echo "corrected 0.49 expect 1"; g $Q/bias_ok.json $Q/m_low.json $Q/r_ok.txt
echo "bad response expect 1"; g $Q/bias_ok.json $Q/m_pred_ok.json $Q/r_bad.txt
echo "missing file expect 2"; g $Q/nope.json $Q/m_pred_ok.json $Q/r_ok.txt
echo "wrong argc expect nonzero"; python3 $S/chrombpnet_qc_gate.py >/dev/null 2>&1; echo "  exit=$?"
echo "== real fixer fixture metrics through gate (bias 0.475, corrected 0.484 -> expect exit 1)"
PO=/mnt/openscience/audits/bio-atac-seq-deep-learning-atac/fix-run/pipeline_outputs; ls $PO | head -20
python3 $S/chrombpnet_qc_gate.py $PO/bias_metrics.json $PO/qc_chrombpnet_metrics.json $PO/nobias_max_bias_response.txt; echo "  exit=$?"
