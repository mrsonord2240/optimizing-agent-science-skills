source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/data
mkdir -p $RUN/out/ex_batch
echo "##### 2a SKILL.md batch block"; asenv as-core python $RUN/scripts/i2a_skillmd_batch.py 2>&1 | grep -av "label.size\|annotate\|^Warning\|size\|linewidth" | tail -15; echo "rc=${PIPESTATUS[0]}"
echo "##### 2b examples/plot_sashimi.py"; asenv as-core python $RUN/scripts/i2b_example_batch.py 2>&1 | grep -av "label.size\|annotate\|^Warning\|size\|linewidth" | tail -30
ls -la $RUN/out/sashimi_plots $RUN/out/ex_batch 2>&1 | head -20
