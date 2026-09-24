"""Bounded independent HTTP probes of NCBI BLAST CGI; no skill source imported."""
from __future__ import annotations

import json
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

URL = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"
CASES = [
    ("invalid_rid_searchinfo", {"CMD": "Get", "FORMAT_OBJECT": "SearchInfo", "RID": "INVALID"}),
    ("invalid_rid_xml", {"CMD": "Get", "FORMAT_TYPE": "XML", "RID": "INVALID"}),
    ("plain_cgi", {"CMD": "Get"}),
]


def probe(label: str, params: dict[str, str]) -> dict[str, object]:
    url = URL + "?" + urllib.parse.urlencode(params)
    start = time.monotonic()
    row: dict[str, object] = {"case": label, "url": url, "started_utc": datetime.now(timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "bioSkills-audit/phase2-closure"})
        with urllib.request.urlopen(request, timeout=45, context=ssl.create_default_context()) as response:
            body = response.read(4096).decode("utf-8", "replace")
            row.update(status=response.status, content_type=response.headers.get("Content-Type"), body_prefix=body[:1000])
    except urllib.error.HTTPError as exc:
        row.update(error_type=type(exc).__name__, status=exc.code, reason=str(exc), body_prefix=exc.read(4096).decode("utf-8", "replace")[:1000])
    except Exception as exc:  # Evidence needs actual transport exception type.
        row.update(error_type=type(exc).__name__, reason=str(exc))
    row["elapsed_s"] = round(time.monotonic() - start, 3)
    return row


if __name__ == "__main__":
    result = {"purpose": "Independent CGI-status probe; no bioSkills code imported", "probes": []}
    for index, (label, params) in enumerate(CASES):
        if index:
            time.sleep(11)
        result["probes"].append(probe(label, params))
    print(json.dumps(result, indent=2, sort_keys=True))
