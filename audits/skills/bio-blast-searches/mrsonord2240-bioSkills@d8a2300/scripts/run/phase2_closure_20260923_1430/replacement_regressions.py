"""Network-free source regression checks using the freshly fetched, source-owned RID XML."""
from __future__ import annotations
import ast, json, pathlib
from Bio.Blast import NCBIXML

run = pathlib.Path(__file__).parent
source = pathlib.Path(r"F:\OpenScience\wt\database-access-blast-searches\database-access\blast-searches")
xml = run / "rid_fetch.xml"

def functions_from(path: pathlib.Path, names: set[str]):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    keep = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom)) or (isinstance(node, ast.FunctionDef) and node.name in names)]
    module = ast.Module(body=keep, type_ignores=[])
    ns: dict[str, object] = {}
    exec(compile(module, str(path), "exec"), ns)
    return ns

basic = functions_from(source / "examples" / "basic_blast.py", {"top_n_by_bitscore"})
saved = functions_from(source / "examples" / "save_and_parse.py", {"parse_hits"})
with xml.open() as h:
    record = NCBIXML.read(h)
top = basic["top_n_by_bitscore"](record, n=10)
hits, saved_record = saved["parse_hits"](xml)

assert len(record.alignments) == 33
assert top[0]["accession"] == "NM_000518" and top[0]["identity"] == 1.0 and top[0]["coverage"] == 1.0
assert len(hits) == 33 and saved_record.query_length == 92 and hits[0]["accession"] == "NM_000518"

result = {"fresh_rid_xml": str(xml), "alignments": len(record.alignments), "basic_top": top[0], "save_and_parse_first": hits[0], "assertions": "PASS"}
(run / "replacement_regressions.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
