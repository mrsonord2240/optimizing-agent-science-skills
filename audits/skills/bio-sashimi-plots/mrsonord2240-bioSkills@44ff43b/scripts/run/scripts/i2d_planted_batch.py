#!/usr/bin/env python3
"""Input 2d: examples/plot_sashimi.py batch_plot_rmats_events on the PLANTED rMATS SE output (contig chrP matches the BAMs).
The event's upstreamES is 100 so upstreamES-500 = -400 (region start < 1)."""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, '/mnt/openscience/audits/bio-sashimi-plots/run/skill/examples')
import plot_sashimi as ps
os.makedirs('../../out/ex_planted', exist_ok=True)
ps.create_grouping_file(['G1_rep1.bam','G1_rep2.bam','G1_rep3.bam','G2_rep1.bam','G2_rep2.bam','G2_rep3.bam'],
                        ['Control']*3 + ['Treatment']*3, 'ex_groups.tsv')
print(open('ex_groups.tsv').read())
ps.batch_plot_rmats_events('../rmats_planted/SE.MATS.JC.txt', 'ex_groups.tsv', 'planted.gtf', '../../out/ex_planted/')
print('files produced:', os.listdir('../../out/ex_planted/'))
