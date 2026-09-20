import pandas as pd
import re

def parse_spliceai_vcf(vcf_path):
    rows = []
    with open(vcf_path) as f:
        for line in f:
            if line.startswith('#'):
                continue
            fields = line.strip().split('\t')
            info = fields[7]
            m = re.search(r'SpliceAI=([^;]+)', info)
            if not m:
                continue
            for ann in m.group(1).split(','):
                parts = ann.split('|')
                allele, symbol = parts[0], parts[1]
                ds = [float(p) if p != '.' else 0 for p in parts[2:6]]
                dp = parts[6:10]
                rows.append({
                    'chrom': fields[0], 'pos': int(fields[1]),
                    'ref': fields[3], 'alt': allele,
                    'gene': symbol,
                    'DS_AG': ds[0], 'DS_AL': ds[1],
                    'DS_DG': ds[2], 'DS_DL': ds[3],
                    'delta_max': max(ds),
                })
    return pd.DataFrame(rows)

