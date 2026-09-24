import pandas as pd

# RSeQC .junction.xls: chrom, intron_st(0-based), intron_end(1-based), read_count, annotation
junc = pd.read_csv('sample_junc_annot.junction.xls', sep='\t')
junc['annotation'] = junc['annotation'].str.strip()    # RSeQC writes ' annotated' with a leading space
by_class = junc.groupby('annotation')['read_count'].sum()
known = by_class.get('annotated', 0) / by_class.sum()
novel = (by_class.get('partial_novel', 0) + by_class.get('complete_novel', 0)) / by_class.sum()
assert abs(known + novel - 1) < 1e-9, by_class.index.tolist()
print(f'known: {known:.1%}, novel: {novel:.1%}')
