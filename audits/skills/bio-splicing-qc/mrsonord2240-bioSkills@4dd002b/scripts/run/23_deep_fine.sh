source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run; D=$R/data/synthetic; mkdir -p $R/work/in2b; cd $R/work/in2b; cp $D/se_sat_deep.bam sample.bam; cp $D/se_sat_deep.bam.bai .; cp $D/synth.bed12 genes.bed12; cp -r $R/skill/examples .
asenv as-core python - <<'PY'
import sys; sys.path.insert(0, 'examples'); import splicing_qc as sq
for lo, hi, step in ((5, 100, 5), (80, 100, 5), (2, 100, 2)):
    c = sq.junction_saturation('sample.bam', 'genes.bed12', f'd_{lo}_{step}', lo=lo, hi=hi, step=step)
    print('deep library (truth: PLATEAU) lo=%d step=%d ->' % (lo, step), 'growth known %.3f' % c['growth_80_100']['known'], c['verdict'], '| known curve', c['known'])
PY
