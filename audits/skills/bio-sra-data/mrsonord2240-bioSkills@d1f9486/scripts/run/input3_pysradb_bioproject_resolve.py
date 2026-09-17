import sys
sys.stdout.reconfigure(encoding='utf-8')
from pysradb import SRAweb
db = SRAweb()
meta = db.sra_metadata('PRJEB37378', detailed=True)
print("rows:", len(meta))
print("ERR10419835 present:", 'ERR10419835' in meta['run_accession'].tolist())
print("cols:", list(meta.columns)[:15])
