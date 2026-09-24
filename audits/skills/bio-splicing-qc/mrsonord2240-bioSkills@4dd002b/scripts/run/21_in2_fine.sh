# Input 2b: the SKILL.md tip "add -l/-u/-s for a finer 80-100% range" and the helper's lo/hi/step args
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run; D=$R/data/synthetic; cd $R/work/in2/se_sat_mid
echo "--- RSeQC literal with -l 80 -u 100 -s 5"
asenv as-core junction_saturation.py -i sample.bam -r genes.bed12 -o fine --skip-plot -l 80 -u 100 -s 5 2>&1 | grep -E '^sampling|rror' | cut -c1-140; echo rc=${PIPESTATUS[0]}
asenv as-core python - <<'PY'
import sys; sys.path.insert(0, 'examples'); import splicing_qc as sq
for lo, hi, step in ((80, 100, 5), (80, 100, 2), (85, 100, 5), (50, 100, 10)):
    try:
        c = sq.junction_saturation('sample.bam', 'genes.bed12', f'fine_{lo}_{hi}_{step}', lo=lo, hi=hi, step=step)
        print(lo, hi, step, 'percent', c['percent'], 'known', c['known'], 'growth', {k: round(v, 3) for k, v in c['growth_80_100'].items()}, c['verdict'])
    except Exception as e: print(lo, hi, step, 'ERR', type(e).__name__, str(e)[:200])
PY
echo "--- correct way to refine (l == s): lo=2 hi=100 step=2 ; sample sizes from RSeQC"
asenv as-core junction_saturation.py -i sample.bam -r genes.bed12 -o fine2 --skip-plot -l 2 -u 100 -s 2 2>&1 | grep -E '^sampling' | awk 'NR%10==0 || NR>=48' | cut -c1-100
asenv as-core python - <<'PY'
import sys; sys.path.insert(0, 'examples'); import splicing_qc as sq
c = sq.junction_saturation('sample.bam', 'genes.bed12', 'fine3', lo=2, hi=100, step=2)
print('lo=2 hi=100 step=2: points', len(c['percent']), 'known@80', c['known'][c['percent'].index(80.0)], 'known@100', c['known'][-1], 'growth', {k: round(v, 3) for k, v in c['growth_80_100'].items()}, c['verdict'])
PY
echo "--- RSeQC source: accumulation of sample size (qcmodule/SAM.py saturation_junction)"
sed -n 4001,4021p /home/sci/micromamba/envs/as-core/lib/python3.13/site-packages/qcmodule/SAM.py
