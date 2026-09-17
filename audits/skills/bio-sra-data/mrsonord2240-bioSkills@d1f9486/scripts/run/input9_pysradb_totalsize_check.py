import sys, io
sys.stdout.reconfigure(encoding='utf-8')
from pysradb import SRAweb
db = SRAweb()
for acc in ["ERR10419835", "ERR10015134"]:
    meta = db.sra_metadata(acc, detailed=True)
    cols = list(meta.columns)
    print(f"=== {acc} ===")
    print("has total_size col:", "total_size" in cols)
    print("has public_size col:", "public_size" in cols)
    row = meta.iloc[0]
    if "total_size" in cols:
        print("total_size:", row.get("total_size"))
    if "public_size" in cols:
        print("public_size:", row.get("public_size"))
    print()
