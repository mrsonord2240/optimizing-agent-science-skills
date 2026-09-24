"""Parse the fetched RID XML and record only audit-relevant result facts."""
from __future__ import annotations

import json
import pathlib
import sys
from datetime import datetime, timezone

from Bio.Blast import NCBIXML

xml_path = pathlib.Path(sys.argv[1])
with xml_path.open() as handle:
    record = NCBIXML.read(handle)
result = {
    "parsed_utc": datetime.now(timezone.utc).isoformat(),
    "xml": str(xml_path),
    "query_length": record.query_length,
    "database": record.database,
    "alignments": len(record.alignments),
}
if record.alignments:
    alignment = record.alignments[0]
    hsp = alignment.hsps[0]
    result["top_hit"] = {
        "accession": alignment.accession,
        "title": alignment.title,
        "bits": hsp.bits,
        "evalue": hsp.expect,
        "identity": hsp.identities / hsp.align_length,
        "coverage": hsp.align_length / record.query_length,
    }
pathlib.Path(__file__).with_name("rid_fetch_parse.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
