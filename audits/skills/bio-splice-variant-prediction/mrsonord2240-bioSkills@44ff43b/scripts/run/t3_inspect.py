import pandas as pd, sys
sys.dont_write_bytecode = True
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
a = pd.read_csv('out/mmsplice_plain.csv'); b = pd.read_csv('out/mmsplice_gz.csv')
print(a.shape, list(a.columns))
print('plain == gz:', a.equals(b))
print(a[['ID', 'gene_name', 'exons', 'delta_logit_psi', 'pathogenicity'] if 'pathogenicity' in a.columns else ['ID','delta_logit_psi']].to_string())
print('ID value counts (variants covered):', a.ID.nunique(), 'of 10 input records')
missing = set(open('data/panel_grch37.vcf').read().split('\n')) 
ids = [l.split('\t')[2] for l in open('data/panel_grch37.vcf') if not l.startswith('#')]
print('input ids not in output:', [i for i in ids if i not in set(a.ID)])
