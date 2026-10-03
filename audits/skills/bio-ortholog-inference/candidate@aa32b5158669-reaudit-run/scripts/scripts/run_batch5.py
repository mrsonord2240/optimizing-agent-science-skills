"""Print the full batch_compara frame for the example's five genes (human -> zebrafish) to see non-1:1 and error rows."""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'F:/OpenScience/wt/dbaccess-ortholog-inference/skills/bio-ortholog-inference/scripts')
import pandas as pd
import ortholog_clients as oc
pd.set_option('display.width', 250, 'display.max_columns', 20, 'display.max_colwidth', 90)
df = oc.batch_compara(['TP53', 'BRCA1', 'MYC', 'ATM', 'MDM2'], source='human', target='zebrafish')
print(df.to_string())
