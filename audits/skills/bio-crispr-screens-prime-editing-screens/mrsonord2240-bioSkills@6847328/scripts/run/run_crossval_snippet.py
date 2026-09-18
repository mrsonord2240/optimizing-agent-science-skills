import pandas as pd
# BE screen output (target conversion + bystander)
be_hits = pd.read_csv('be_screen_hits.tsv', sep='\t')
# PE screen output (intended edit + scaffold-incorp + indel)
pe_hits = pd.read_csv('pe_screen_hits.tsv', sep='\t')

# Intersect on intended variant
concordant = be_hits.merge(pe_hits, on='variant_id', suffixes=('_be', '_pe'))
# Filter to high-confidence: both methods call variant + same direction
concordant['high_confidence'] = (concordant['be_fdr'] < 0.05) & (concordant['pe_fdr'] < 0.05) & \
                                 (np.sign(concordant['be_lfc']) == np.sign(concordant['pe_lfc']))
print(concordant)
