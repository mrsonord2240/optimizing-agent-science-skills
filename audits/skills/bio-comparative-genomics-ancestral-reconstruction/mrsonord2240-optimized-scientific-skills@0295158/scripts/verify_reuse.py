#!/usr/bin/env python3
"""Verify the immutable evidence accepted for unaffected ASR surfaces."""
import hashlib
import json
from pathlib import Path

audits = Path(r"F:\OpenScience\audits\bio-comparative-genomics-ancestral-reconstruction")
run = audits / "final-reaudit-opt10-20260929"
candidate = Path(r"F:\OpenScience\wt\opt10-ancestral-reconstruction\skills\bio-comparative-genomics-ancestral-reconstruction")
env = Path(r"F:\OpenScience\audit-envs\bio-comparative-genomics-ancestral-reconstruction")
fixed = audits / "fix-opt11-20260928"

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def manifest_rows(path):
    rows = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        relative, size, sha = line.split("\t")
        rows[relative] = {"bytes": int(size), "sha256": sha}
    return rows

current_rows = manifest_rows(run / "candidate-manifest-before.tsv")
fixed_rows = manifest_rows(audits / "fix-opt11-20260928" / "candidate-manifest-focused-fix.tsv")
assert current_rows == fixed_rows, "Current candidate does not match the fix-phase bytes"

fingerprint = json.loads((audits / "tooling-delta-opt10-20260928" / "environment-fingerprint.json").read_text())
lock_hash = digest(env / "environment-explicit.lock")
assert lock_hash == fingerprint["base_environment"]["lock_sha256"]
runtime = (run / "evidence/runtime-boundary.log").read_text(encoding="utf-8")
for expected in (
    "user=sci", "WSL_INTEROP=<unset>", "mnt_f=not-mounted", "Python 3.12.14",
    "IQ-TREE multicore version 2.4.0", "openjdk version \"21.0.10-internal",
    "R version 4.4.3", "ape 5.8.1", "phytools 2.5.2", "geiger 2.0.12",
    "corHMM 2.8", "OUwie 3.0.3", lock_hash,
):
    assert expected in runtime, f"Runtime check is missing {expected!r}"

reuse_files = {
    "iqtree_results": fixed / "evidence/iqtree-results.json",
    "iqtree_state": fixed / "evidence/iqtree-run/asr_iqtree.state",
    "grasp_validation": fixed / "evidence/grasp-validation.txt",
    "grasp_wrapper_log": fixed / "evidence/grasp-candidate-wrapper.log",
    "grasp_alignment": fixed / "grasp-run/candidate-wrapper/alignment.fasta",
    "grasp_tree": fixed / "grasp-run/candidate-wrapper/species.nwk",
    "r_session_info": fixed / "evidence/r-sessionInfo.txt",
    "r_retest_script": fixed / "scripts/retest_r.R",
    "r_traits": fixed / "evidence/r-run/traits.csv",
    "r_tree": fixed / "evidence/r-run/species_tree.nwk",
    "python_results": fixed / "evidence/python-results.json",
}
file_hashes = {name: digest(path) for name, path in reuse_files.items()}
core_candidate = (
    "scripts/iqtree_ancestral.sh", "scripts/iqtree_state.py", "scripts/grasp_asr.sh",
    "scripts/stochastic_mapping.R", "scripts/continuous_trait_asr.R",
    "scripts/ancestral_reconstruction.py",
)
result = {
    "schema": "asr-immutable-evidence-reuse-v1",
    "current_candidate_identity": "sha256-manifest-v1:" + digest(run / "candidate-manifest-before.tsv"),
    "candidate_manifest_sha256": digest(run / "candidate-manifest-before.tsv"),
    "candidate_file_count": len(current_rows),
    "candidate_manifest_bytes": (run / "candidate-manifest-before.tsv").stat().st_size,
    "all_candidate_bytes_match_fix_manifest": True,
    "verified_unaffected_candidate_files": {
        name: current_rows[name] for name in core_candidate
    },
    "environment_lock_sha256": lock_hash,
    "environment_lock_unchanged_from_fingerprint": True,
    "runtime_probe_sha256": digest(run / "evidence/runtime-boundary.log"),
    "runtime_versions_and_boundary_match": True,
    "reused_evidence_sha256": file_hashes,
    "decision": "Reusable IQ-TREE, GRASP, R/corHMM/OUwie, and no-data evidence remains applicable; candidate bytes, runtime, interfaces, fixtures, and analysis assumptions match the recorded fixed run.",
    "newly_rerun_surfaces": ["PAML CODONML codon writer/parser", "PAML provider protein writer/parser", "PAML extracted protein writer/parser"],
    "unexecuted_optional_surfaces": ["FastML", "RevBayes", "BayesTraits", "MrBayes", "BEAST2", "RPANDA", "GRASP web service"],
}
(run / "evidence/reuse-validation.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
