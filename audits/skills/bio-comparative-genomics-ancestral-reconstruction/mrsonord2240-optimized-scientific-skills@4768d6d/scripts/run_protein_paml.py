#!/usr/bin/env python3
"""Fresh independent protein CODeml runs through both shipped writer routes."""
import hashlib
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys

env = pathlib.Path("/mnt/openscience/audit-envs/bio-comparative-genomics-ancestral-reconstruction")
candidate = pathlib.Path("/mnt/openscience/wt/opt10-ancestral-reconstruction/skills/bio-comparative-genomics-ancestral-reconstruction")
out_root = pathlib.Path("/mnt/openscience/audits/bio-comparative-genomics-ancestral-reconstruction/final-reaudit-opt10-20260929/evidence/real-protein-paml")
out_root.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(candidate / "scripts"))
sys.path.insert(0, str(candidate / "tests"))
from Bio import AlignIO, Phylo
import ancestral_reconstruction as provider
import codeml_asr as extracted
from test_paml_rst import assert_real_rst

alignment = AlignIO.read(env / "data/cytochrome-c-aligned.fasta", "fasta")
rename = {record.id: f"T{i:02d}" for i, record in enumerate(alignment, 1)}
for record in alignment:
    record.id = rename[record.id]
    record.name = record.id
    record.description = ""
tree = Phylo.read(env / "data/cytochrome-c-rooted.nwk", "newick")
for tip in tree.get_terminals():
    tip.name = rename[tip.name]

results = []
for label, writer in (
    ("provider", lambda run: provider.write_asr_control("alignment.phy", "tree.nwk", "mlc", str(run))),
    ("extracted", lambda run: extracted.write_codeml_ctl("alignment.phy", "tree.nwk", str(run), seqtype="protein")),
):
    run = out_root / label
    run.mkdir(exist_ok=True)
    AlignIO.write(alignment, run / "alignment.phy", "phylip-sequential")
    tmp_tree = run / "tree.raw.nwk"
    Phylo.write(tree, tmp_tree, "newick")
    (run / "tree.nwk").write_text(f"8 1\n{tmp_tree.read_text().strip()}\n", encoding="utf-8")
    tmp_tree.unlink()
    shutil.copy2(env / "conda-env/dat/lg.dat", run / "lg.dat")
    ctl = writer(run)
    proc = subprocess.run([str(env / "conda-env/bin/codeml"), pathlib.Path(ctl).name],
                          cwd=run, text=True, capture_output=True, timeout=300)
    rst = run / "rst"
    if proc.returncode != 0 or not rst.is_file():
        raise RuntimeError(f"{label} CODEML failed: rc={proc.returncode}; stdout={proc.stdout}; stderr={proc.stderr}")
    ancestors, posteriors = assert_real_rst(rst)
    if label == "provider":
        provider_ancestors = provider.parse_rst_ancestors(rst)
        provider_rows = provider.extract_site_probabilities(rst)
        if provider_ancestors != ancestors or len(provider_rows) != 770:
            raise AssertionError("Provider API differs from the shared source-row oracle")
    else:
        parsed = extracted.parse_rst_posteriors(rst)
        if len(parsed) != 7 or any(len(rows) != 110 for rows in parsed.values()):
            raise AssertionError("Extracted API does not return 7 nodes x 110 sites")
    result = {
        "route": label,
        "status": "PASS_FRESH_PROTEIN_CODeml_4_10_10",
        "returncode": proc.returncode,
        "rst_bytes": rst.stat().st_size,
        "rst_sha256": hashlib.sha256(rst.read_bytes()).hexdigest(),
        "alignment_sha256": hashlib.sha256((run / "alignment.phy").read_bytes()).hexdigest(),
        "tree_sha256": hashlib.sha256((run / "tree.nwk").read_bytes()).hexdigest(),
        "nodes": len(ancestors),
        "sites_per_node": 110,
        "posterior_records": sum(map(len, posteriors.values())),
        "Node10_sites_1_2": [(row["state"], row["probability"]) for row in posteriors["Node10"][:2]],
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }
    (run / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    results.append(result)
print(json.dumps([{key: value for key, value in row.items() if key not in {"stdout", "stderr"}} for row in results], indent=2))
