import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, '/mnt/openscience/audits/bio-sashimi-plots/run/skill/examples')
import plot_sashimi as ps
ps.plot_sashimi('ex_groups.tsv', 'chrP:1-1200', '../../out/ex_plot_fn', 'planted.gtf', options={'min_junc': 5, 'format': 'svg'})
print('size', os.path.getsize('../../out/ex_plot_fn.svg'))
