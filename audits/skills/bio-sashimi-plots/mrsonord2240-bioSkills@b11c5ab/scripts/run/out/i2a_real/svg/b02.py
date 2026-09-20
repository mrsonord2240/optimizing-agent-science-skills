import subprocess
import pandas as pd
from pathlib import Path
groups = pd.DataFrame({
    'sample_id': ['gbr1', 'gbr2', 'yri1', 'yri2'],
    'bam': ['/mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/bam/ERR188383.Aligned.out.bam', '/mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/bam/ERR188428.Aligned.out.bam', '/mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/bam/ERR188454.Aligned.out.bam', '/mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/bam/ERR204916.Aligned.out.bam'],
    'group': ['GBR', 'GBR', 'YRI', 'YRI']})
groups.to_csv('sashimi_groups.tsv', sep='\t', index=False, header=False)
Path('palette.txt').write_text('#1f77b4\n#ff7f0e\n')
