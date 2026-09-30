# Real-data check of the Skill's QC-table claims against the whole-genome Cell Ranger ATAC 1.0.1 singlecell.csv of 10x PBMC 5k
import pandas as pd, sys
d = pd.read_csv(sys.argv[1]); c = d[d.is__cell_barcode == 1]
pf = c.passed_filters
print('called cells', len(c), 'median passed_filters', pf.median())
print('<1000', int((pf < 1000).sum()), ' 1000-3000', int(((pf >= 1000) & (pf < 3000)).sum()), ' 3000-50000', int(((pf >= 3000) & (pf <= 50000)).sum()), ' >80000', int((pf > 80000).sum()))
print('cells below AMULET ~15K valid-read-pair depth (approx passed_filters<15000):', round(float((pf < 15000).mean()), 3))
fr = c.peak_region_fragments / c.passed_filters
print('FRiP>=0.15 frac', round(float((fr >= .15).mean()), 3), ' blacklist_ratio<0.05 frac', round(float(((c.blacklist_region_fragments / c.peak_region_fragments) < .05).mean()), 3))
print('script filter peak_region_fragments 1000-20000 keeps', int(((c.peak_region_fragments > 1000) & (c.peak_region_fragments < 20000)).sum()))
print('mito fraction (mitochondrial/total) median', round(float((c.mitochondrial / c.total).median()), 4), ' columns', list(d.columns))
