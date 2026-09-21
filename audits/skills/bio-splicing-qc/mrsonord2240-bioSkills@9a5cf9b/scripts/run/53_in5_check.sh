source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run; S=/mnt/openscience/as-qc-reaudit-scratch/star/run2
asenv as-core python $R/52_in5_check.py $S $R/skill/examples $ASDATA/rnasplice/reference/genes_chrX.gtf
echo "--- STAR --help: alignIntronMax default and window derivation"
asenv as-core STAR --help | grep -A4 -E '^alignIntronMax|^winBinNbits|^winAnchorDistNbins|^alignSJoverhangMin|^alignSJDBoverhangMin|^limitSjdbInsertNsj' | head -50
echo "--- pass-2 SJ.out.tab: are merged novel junctions marked annotated (col6==1)?"
asenv as-core python - <<'PY'
merged = {tuple(l.split('\t')[:3]) for l in open('/mnt/openscience/as-qc-reaudit-scratch/star/run2/cohort_novel_SJ.tab')}
import collections
c = collections.Counter()
for l in open('/mnt/openscience/as-qc-reaudit-scratch/star/run2/pass2_ERR188383_SJ.out.tab'):
    f = l.split('\t')
    if tuple(f[:3]) in merged: c[f[5]] += 1
print('merged novel junctions present in pass2 SJ.out.tab, by col6 (annotated flag):', dict(c), 'of', len(merged))
PY
