# Input 3 (Variant B) -- adapted from SKILL.md's "Batch via pysradb metadata" pattern
# and examples/find_sra_runs.py's runs_via_pysradb() helper.
from pysradb import SRAweb

def bioproject_to_runs(prjna):
    db = SRAweb()
    return db.sra_metadata(prjna, detailed=True)

df = bioproject_to_runs('PRJEB37378')
print(f"PRJEB37378 -> {len(df)} rows")
print(df['run_accession'].head(10).tolist())
assert 'ERR10419835' in df['run_accession'].tolist(), "known-good accession missing from resolved list"
print("ERR10419835 present in resolved run list: OK")
df[['run_accession']].to_csv('accessions_prjeb37378.txt', index=False, header=False)
print(f"Wrote {len(df)} accessions to accessions_prjeb37378.txt")
