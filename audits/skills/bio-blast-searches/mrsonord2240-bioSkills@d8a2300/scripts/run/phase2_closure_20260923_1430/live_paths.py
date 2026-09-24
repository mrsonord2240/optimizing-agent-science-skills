"""Bounded live regression of two source-compatible NCBI BLAST request paths from copied source."""
from __future__ import annotations

import json
import pathlib
import sys
import time
import traceback
from datetime import datetime, timezone

from Bio.Blast import NCBIWWW, NCBIXML

OUT = pathlib.Path(__file__).with_name("live_paths.json")
HBB = ">HBB_partial\nATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAG"
HBA = "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR"


def attempt(label: str, **kwargs: object) -> dict[str, object]:
    started = datetime.now(timezone.utc).isoformat()
    t0 = time.monotonic()
    row: dict[str, object] = {"label": label, "started_utc": started, "kwargs": kwargs}
    try:
        handle = NCBIWWW.qblast(format_type="XML", **kwargs)
        record = NCBIXML.read(handle)
        handle.close()
        row.update(ok=True, query_length=record.query_length, database=record.database, alignments=len(record.alignments))
        if record.alignments:
            hsp = record.alignments[0].hsps[0]
            row.update(top_accession=record.alignments[0].accession, top_bits=round(hsp.bits, 3), top_evalue=hsp.expect)
    except Exception as exc:
        row.update(ok=False, error_type=type(exc).__name__, error=str(exc), traceback=traceback.format_exc(limit=5))
    row["elapsed_s"] = round(time.monotonic() - t0, 3)
    return row


if __name__ == "__main__":
    result = {"purpose": "Two bounded live request paths copied from the pinned source contract", "python": sys.version, "attempts": []}
    result["attempts"].append(attempt("basic_blast_contract", program="blastn", database="refseq_select_rna", sequence=HBB, expect=1e-10, word_size=11, hitlist_size=50))
    time.sleep(11)
    result["attempts"].append(attempt("rid_style_megablast_contract", program="blastn", database="refseq_select_rna", sequence=HBB, hitlist_size=50, megablast=True))
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(OUT.read_text(encoding="utf-8"))
