"""
Input 2 (Variant A): "For GSE147507, resolve to SRA run accessions using pysradb
(the Skill's documented preferred path), so I can hand off to the sra-data skill
for FASTQ download."

Follows SKILL.md's documented "Link GEO Series to SRA runs (preferred path: pysradb)"
code pattern verbatim.
"""
from pysradb import SRAweb


def gse_to_srr(gse):
    db = SRAweb()
    srp_df = db.gse_to_srp(gse)
    if srp_df.empty:
        return []
    srp = srp_df['study_accession'].iloc[0]
    srr_df = db.srp_to_srr(srp)
    return srr_df['run_accession'].tolist()


GSE = 'GSE147507'
srrs = gse_to_srr(GSE)
print(f'{GSE} -> {len(srrs)} SRR runs')
print(f'first 5: {srrs[:5]}')

with open(f'{GSE}_sra_runs.txt', 'w') as f:
    for r in srrs:
        f.write(f'{r}\n')
print(f'Wrote {len(srrs)} accessions to {GSE}_sra_runs.txt')
print('Hand off to sra-data: bash download_batch.sh GSE147507_sra_runs.txt ./fastq')
