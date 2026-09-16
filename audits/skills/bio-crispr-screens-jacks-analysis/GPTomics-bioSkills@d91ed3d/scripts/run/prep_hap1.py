"""
Build real JACKS input files (countfile / guidemap / repmap) from the real HAP1 TKOv3
pooled-knockout screen (hart-lab/bagel, via public-data/HAP1_TKOv3_reads.txt) -- this is
the same real single-cell-line data used to smoke-test MAGeCK/BAGEL2/drugZ for this
candidate. JACKS' own SKILL.md never shows building input files from a raw counts table
with SEQUENCE-based sgRNA IDs, so this exercises whether an agent, following only
SKILL.md + usage-guide.md, can correctly adapt real data to JACKS' expected schema.
"""
import pandas as pd

SRC = r"F:\OpenScience\audit-envs\crispr-screen-analyst\public-data\HAP1_TKOv3_reads.txt"
OUT = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\data"

df = pd.read_csv(SRC, sep='\t')
print("rows:", len(df), "cols:", list(df.columns))
print("unique SEQUENCE:", df['SEQUENCE'].nunique(), "of", len(df))

# SEQUENCE is not guaranteed unique across genes (paralog guides can share sequence);
# build an explicit unique sgRNA id the way a careful analyst would, since JACKS keys
# guides by this id in both the countfile and the guidemapping file.
df = df.reset_index(drop=True)
df['sgRNA_id'] = df['GENE'].astype(str) + '_' + df.groupby('GENE').cumcount().astype(str)
dupe_seq = df['SEQUENCE'].duplicated().sum()
print("duplicate SEQUENCE rows (would have collided if SEQUENCE used as id):", dupe_seq)

counts = df[['sgRNA_id', 'GENE', 'HAP1_T0', 'HAP1_T18A', 'HAP1_T18B', 'HAP1_T18C']].rename(
    columns={'sgRNA_id': 'sgRNA', 'GENE': 'gene'})
counts.to_csv(f'{OUT}/hap1_counts.txt', sep='\t', index=False)

guidemap = df[['sgRNA_id', 'GENE']].rename(columns={'sgRNA_id': 'sgRNA', 'GENE': 'Gene'})
guidemap.to_csv(f'{OUT}/hap1_guidemap.txt', sep='\t', index=False)

repmap_rows = [
    ('HAP1_T0', 'T0'),
    ('HAP1_T18A', 'T18'),
    ('HAP1_T18B', 'T18'),
    ('HAP1_T18C', 'T18'),
]
repmap = pd.DataFrame(repmap_rows, columns=['Replicate', 'Sample'])
repmap.to_csv(f'{OUT}/hap1_repmap.txt', sep='\t', index=False)

print("Wrote hap1_counts.txt, hap1_guidemap.txt, hap1_repmap.txt to", OUT)
print(counts.head(3).to_string(index=False))
print(repmap.to_string(index=False))
