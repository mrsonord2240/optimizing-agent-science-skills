import pandas as pd
be_hits = pd.DataFrame({'variant_id':['V1','V2','V3'], 'be_fdr':[0.01,0.2,0.03], 'be_lfc':[-1.5,0.3,-0.9]})
pe_hits = pd.DataFrame({'variant_id':['V1','V2','V3'], 'pe_fdr':[0.02,0.15,0.04], 'pe_lfc':[-1.2,0.4,0.8]})
be_hits.to_csv('be_screen_hits.tsv', sep='\t', index=False)
pe_hits.to_csv('pe_screen_hits.tsv', sep='\t', index=False)
