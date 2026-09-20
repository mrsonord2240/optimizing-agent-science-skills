#!/usr/bin/env python3
"""Input 2b: examples/plot_sashimi.py (unmodified copy in run/skill/examples) imported and its batch_plot_rmats_events +
plot_specific_event called exactly as its __main__ comments show. Real chrX rMATS output."""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, '/mnt/openscience/audits/bio-sashimi-plots/run/skill/examples')
import plot_sashimi as ps

print('--- batch_plot_rmats_events (defaults: n_top=20, fdr 0.05, dpsi 0.1)')
ps.batch_plot_rmats_events('rmats_real/SE.MATS.JC.txt', 'sashimi_groups.tsv', 'annotation.gtf', '../out/ex_batch/')
import os
print('files produced:', os.listdir('../out/ex_batch/'))
print('--- plot_specific_event (aggregate=mean, per its own code)')
try:
    ps.plot_specific_event('sashimi_groups.tsv', 'annotation.gtf', 'X', 12994000, 12995500, '../out/ex_specific')
except Exception as e:
    print('plot_specific_event raised', type(e).__name__, e)
