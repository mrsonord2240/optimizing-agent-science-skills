import pandas as pd
d=pd.read_csv(r'F:\OpenScience\audit-envs\atac-seq\public-data\scatac\outs\singlecell.csv')
c=d[d.is__cell_barcode==1]; r=(c.blacklist_region_fragments/c.peak_region_fragments)
print('ATAC1.0.1 called cells',len(c),'max ratio',round(r.max(),4),'n>=0.05',int((r>=0.05).sum()))
