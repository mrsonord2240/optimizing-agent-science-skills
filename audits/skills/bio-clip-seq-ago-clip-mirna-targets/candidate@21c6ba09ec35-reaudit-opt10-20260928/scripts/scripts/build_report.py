#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path("/mnt/openscience/audits/bio-clip-seq-ago-clip-mirna-targets/reaudit-opt10-20260928")
CANDIDATE = Path("/mnt/openscience/wt/opt10-ago-clip/skills/bio-clip-seq-ago-clip-mirna-targets")
TOOLING = Path("/mnt/openscience/audit-envs/bio-clip-seq-ago-clip-mirna-targets")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


inputs = [
    {
        "index": 1,
        "type": "Canonical",
        "label": "Current Hyb official-data route and workflow-level repeatability",
        "status": "PARTIAL",
        "status_flag": "❌",
        "note": "The repaired wrapper executes current pinned Hyb and publishes complete structured outputs, but two independent two-run batches retained nonidentical direct-target sets despite equal 94/17 aggregate counts.",
        "basic": 26,
        "specialized": 42,
        "total": 68,
        "assertions_passed": 4,
        "assertions_total": 5,
        "assertions": [
            {"text": "The wrapper executes pinned Hyb 028ab63 on its official public input through the current named-database interface", "result": "PASS", "note": "Four fresh single-thread Hyb runs across two wrapper batches each emitted 111 non-empty 16-column rows."},
            {"text": "The wrapper publishes complete structured outputs and reason-coded exclusions", "result": "PASS", "note": "Each batch atomically published sites, targets, exclusions, manifest, raw outputs, and logs; counts reconciled to 111."},
            {"text": "The orientation-aware parser retains only assignments identical within each configured batch", "result": "PASS", "note": "Each two-run batch retained 94 assignments and excluded 17 as unstable_assignment."},
            {"text": "Repeating the complete two-run workflow on identical pinned inputs produces the same direct-target list", "result": "FAIL", "note": "Pair A and Pair B had seven accepted-only ids on each side and four changed assignments among shared ids; sites and target hashes differed."},
            {"text": "Raw Hyb and output identities are recorded for independent review", "result": "PASS", "note": "Both manifests retain commit, database, input hash, per-run hashes, output hashes, counts, and policy."},
        ],
    },
    {
        "index": 2,
        "type": "Variant A",
        "label": "Strict failure, path, overwrite, and atomic-publication boundaries",
        "status": "COMPLETED",
        "status_flag": "✅",
        "note": "Quoted space and literal-glob paths, exit-status propagation, overwrite refusal, failed-replacement preservation, and staging cleanup all passed independent controls.",
        "basic": 40,
        "specialized": 58,
        "total": 98,
        "assertions_passed": 5,
        "assertions_total": 5,
        "assertions": [
            {"text": "Paths containing spaces and literal glob characters remain literal", "result": "PASS", "note": "The wrapper completed with a spaced/literal-star FASTQ and spaced tool/output paths."},
            {"text": "An existing final output is not overwritten without explicit replacement", "result": "PASS", "note": "The rerun returned exit 73 and preserved the completed manifest."},
            {"text": "A Hyb subprocess status of 42 is propagated", "result": "PASS", "note": "The replacement attempt returned 42 and surfaced the controlled error."},
            {"text": "A failed replacement preserves the prior output", "result": "PASS", "note": "The sentinel in the prior final directory remained intact."},
            {"text": "A failed run leaves neither a partial final result nor staging residue", "result": "PASS", "note": "No matching stage directory remained after failure."},
        ],
    },
    {
        "index": 3,
        "type": "Edge",
        "label": "16-column orientation, expression provenance, schema, and ambiguity controls",
        "status": "COMPLETED",
        "status_flag": "✅",
        "note": "Independent fixtures verified fields 4/10 in either orientation, exact expression provenance, structured aggregation, reason codes, and fail-closed schema behavior.",
        "basic": 40,
        "specialized": 58,
        "total": 98,
        "assertions_passed": 5,
        "assertions_total": 5,
        "assertions": [
            {"text": "The parser recognizes one microRNA and one mRNA in either fields-4/10 orientation", "result": "PASS", "note": "Both mirna-first and target-first fixture rows were retained with the correct orientation."},
            {"text": "Expression values, units, and source provenance are preserved", "result": "PASS", "note": "The accepted rows retained 150 TPM and matched-small-rna source."},
            {"text": "Missing and differing cross-run assignments receive distinct reason codes", "result": "PASS", "note": "missing_from_replicate and unstable_assignment were emitted as expected."},
            {"text": "Malformed Hyb field counts fail closed", "result": "PASS", "note": "A three-field row returned nonzero with an expected-16 diagnostic."},
            {"text": "Malformed expression schemas fail closed", "result": "PASS", "note": "The parser rejected a reduced header before producing results."},
        ],
    },
    {
        "index": 4,
        "type": "Variant B",
        "label": "TargetScan spliced-coordinate projection and strand-safe overlap",
        "status": "COMPLETED",
        "status_flag": "✅",
        "note": "Plus- and minus-strand exon-spanning sites projected to versioned BED12, -split -s excluded the opposite strand, and release/range errors failed closed.",
        "basic": 39,
        "specialized": 58,
        "total": 97,
        "assertions_passed": 5,
        "assertions_total": 5,
        "assertions": [
            {"text": "TargetScan UTR-relative input is not treated as genomic BED", "result": "PASS", "note": "The converter requires a version-matched spliced UTR map and emits the coordinate contract in its manifest."},
            {"text": "Plus- and minus-strand exon-spanning sites project correctly", "result": "PASS", "note": "Both fixtures produced two-block BED12 rows with the expected strands."},
            {"text": "The overlap command is block- and strand-aware", "result": "PASS", "note": "bedtools intersect -split -s retained the two matching-strand peaks and excluded the opposite-strand peak."},
            {"text": "Release mismatch is rejected", "result": "PASS", "note": "A 7.2 command against an 8.0 map returned nonzero with a release diagnostic."},
            {"text": "Sites outside the mapped UTR fail closed", "result": "PASS", "note": "The out-of-range fixture returned nonzero instead of truncating the site."},
        ],
    },
    {
        "index": 5,
        "type": "Stress",
        "label": "Library-layout and external-surface claim boundaries",
        "status": "PARTIAL",
        "status_flag": "⚠️",
        "note": "Tool and evidence boundaries are substantially corrected, but the candidate still states that the pinned targeted-Yeo route takes a 9-nt R2 UMI while the live executable defaults to 10 and its CWL does not override it.",
        "basic": 30,
        "specialized": 39,
        "total": 69,
        "assertions_passed": 4,
        "assertions_total": 5,
        "assertions": [
            {"text": "Total and targeted Yeo library layouts are kept distinct", "result": "PASS", "note": "The candidate routes them separately and warns against transferring a generic paired pattern."},
            {"text": "The targeted-Yeo UMI length stated by the candidate matches the pinned executable contract", "result": "FAIL", "note": "Pinned CWL prose says 9 nt, targeted_miR_umi.py defaults to 10, the CWL supplies no umi_length, and the live default appended ten R2 bases."},
            {"text": "Hyb, Yeo CWL, HEAP, hybkit, and prediction services are not represented as interchangeable tools", "result": "PASS", "note": "The skill now distinguishes each interface and access state."},
            {"text": "Counts and absent overlaps are interpreted within assay context", "result": "PASS", "note": "Counts are recovery support rather than affinity, and absent AGO overlap is not represented as biological disproof."},
            {"text": "Unavailable full Yeo, HEAP wet lab, and DIANA execution are not credited as completed", "result": "PASS", "note": "They remain respectively resource-infeasible, biological-route unavailable, and remote unavailable."},
        ],
    },
]

report = {
    "meta": {
        "skill_name": "bio-clip-seq-ago-clip-mirna-targets",
        "description": "Identify direct miRNA-target interactions from AGO HITS-CLIP, AGO-CLEAR-CLIP, HEAP, chimeric eCLIP / miR-eCLIP, or CLASH, and reconcile direct chimeras with computational predictions.",
        "evaluated_on": "2026-09-28",
        "evaluator_version": "skill-auditor@1.0",
        "category": "Data Analysis",
        "execution_mode": "D",
        "complexity": "Moderate",
        "n_inputs": 5,
    },
    "veto_gates": {
        "skill_veto": {
            "gate": "FAIL",
            "stability": "PASS",
            "contract": "PASS",
            "determinism": "FAIL",
            "security": "PASS",
        },
        "research_veto": {
            "applicable": True,
            "gate": "FAIL",
            "scientific_integrity": {"result": "PASS", "detail": "No output fabricates a DOI, PMID, study size, p-value, biological result, or execution state; public, executed, resource-infeasible, wet-lab, and unavailable surfaces remain separated."},
            "practice_boundaries": {"result": "PASS", "detail": "The skill remains a research-analysis workflow and makes no patient-specific diagnosis, prescription, or clinical-treatment recommendation."},
            "methodological_ground": {"result": "FAIL", "detail": "The core direct-interaction workflow calls assignments stable after only two coincident runs, but repeating that entire two-run policy on identical pinned input changes accepted ids and assignments. The targeted-Yeo route also states an unresolved 9-nt UMI contract while the executable default actually extracts 10 nt."},
            "code_usability": {"result": "PASS", "detail": "All three shipped scripts are runnable in the prepared environment; 5/5 shipped tests and 9/9 independent contract assertions passed, including fail-closed and atomic-publication cases."},
        },
    },
    "static_score": {
        "subtotal": 88,
        "max": 100,
        "categories": {
            "functional_suitability": {"score": 10, "max": 12, "note": "The main Hyb and TargetScan routes are implemented and useful, but direct-target repeatability and one targeted-library contract remain unresolved."},
            "reliability": {"score": 9, "max": 12, "note": "Failure, overwrite, staging, parsing, and release gates are strong; workflow-level output repeatability remains defective."},
            "performance_context": {"score": 8, "max": 8, "note": "Progressive routing, bounded fixtures, and explicit execution classifications avoid unnecessary work."},
            "agent_usability": {"score": 14, "max": 16, "note": "The workflow and report contract are clear, but the targeted UMI statement gives an agent an incorrect exact length."},
            "human_usability": {"score": 7, "max": 8, "note": "Natural triggers and explicit failure guidance are strong; one external protocol detail requires independent resolution."},
            "security": {"score": 12, "max": 12, "note": "Inputs are validated, paths are quoted, no credentials are used, and final outputs are atomically protected."},
            "maintainability": {"score": 12, "max": 12, "note": "Responsibilities are separated across references and small scripts with focused regression coverage."},
            "agent_specific": {"score": 16, "max": 20, "note": "Triggering, disclosure, composition, and escape hatches are strong; repeated complete runs are not idempotent at the scientific-result layer."},
        },
    },
    "dynamic_score": {
        "inputs": inputs,
        "execution_avg": 86.0,
        "max": 100,
        "assertion_pass_rate": {"passed": 23, "total": 25},
    },
    "final": {
        "static_weighted": 35.2,
        "dynamic_weighted": 51.6,
        "score": 87,
        "max": 100,
        "grade": "Reject",
        "grade_symbol": "❌",
        "deployable": False,
        "veto_override": True,
    },
    "key_strengths": [
        "The repaired wrapper now uses the current pinned Hyb named-database and generated-output contract and publishes structured provenance atomically.",
        "Orientation-aware 16-column parsing, expression provenance, reason-coded exclusions, path safety, error propagation, and overwrite behavior passed independent controls.",
        "TargetScan 8 sites are projected through a versioned spliced UTR map and intersected with explicit block and strand semantics.",
        "Tool identity, direct-versus-indirect evidence, recovery-versus-affinity, species, access, and negative-evidence boundaries are materially improved.",
    ],
    "recommendations": [
        {
            "priority": "P0",
            "title": "AGO-004 — Make direct-target consensus workflow-level deterministic",
            "observed_in": [1],
            "problem": "Two separate two-run batches on identical pinned input each retained 94 and excluded 17, yet seven accepted ids changed on each side and four shared ids changed assignment.",
            "root_cause": "Agreement inside one pair does not establish stability when Hyb tie or multi-hit selection can coincidentally agree twice on different assignments across batches.",
            "fix": "Adopt and validate a workflow-level ambiguity policy across a prospectively fixed larger replicate panel or deterministic upstream selection rule; emit per-read cross-run support and require exact end-to-end repeatability before labeling direct targets stable.",
        },
        {
            "priority": "P1",
            "title": "AGO-005 — Resolve the targeted-Yeo UMI-length contract",
            "observed_in": [5],
            "problem": "The candidate says the pinned targeted route takes a 9-nt R2 UMI, but targeted_miR_umi.py defaults to 10, the CWL does not pass umi_length, and the live default extracts ten bases.",
            "root_cause": "The candidate treats a stale CWL comment as the executable contract without reconciling it with the bound command or the experimental library specification.",
            "fix": "Do not state an exact targeted UMI length until the protocol is resolved. Require a declared library UMI length and a pinned route that passes it explicitly, then add 9-nt and 10-nt regression fixtures tied to protocol provenance.",
        },
    ],
}

write(ROOT / "report.json", json.dumps(report, indent=2, ensure_ascii=False) + "\n")

viewer_lines = [
    "# Eval Viewer — bio-clip-seq-ago-clip-mirna-targets",
    "",
    "Generated: 2026-09-28",
    "",
    "## Summary Table",
    "",
    "| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |",
    "|---:|---|---:|---:|---:|---:|---|",
]
for item in inputs:
    viewer_lines.append(f"| {item['index']} | {item['type']} | {item['basic']} | {item['specialized']} | {item['total']} | {item['assertions_passed']}/{item['assertions_total']} | {item['status_flag']} {item['status']} |")
viewer_lines.extend([
    "",
    "**Execution Average:** 86.0 / 100  ",
    "**Assertion Pass Rate:** 23/25  ",
    "**Static Score:** 88 / 100  ",
    "**Weighted Score:** 87 / 100  ",
    "**Final Grade:** ❌ Reject — determinism and methodological vetoes override the numeric score.",
    "",
    "## Veto disposition",
    "",
    "- Skill veto: **FAIL** on determinism. Separate complete two-run workflows return different direct-target lists.",
    "- Research veto: **FAIL** on methodological ground. Two-run agreement is not enough to call an assignment stable under the observed stochasticity, and the targeted-Yeo UMI length remains internally inconsistent.",
    "- Stability, structural contract, security, scientific integrity, practice boundaries, and code usability pass.",
    "",
    "## Detailed Outputs",
])
for item in inputs:
    viewer_lines.extend([
        "",
        f"### Input {item['index']} — {item['type']}: {item['label']}",
        "",
        f"**Status:** {item['status_flag']} {item['status']}  ",
        f"**Output summary:** {item['note']}  ",
        f"**Scores:** Basic {item['basic']}/40 | Specialized {item['specialized']}/60 | Total {item['total']}/100",
        "",
        "**Assertions:**",
        "",
    ])
    for assertion in item["assertions"]:
        mark = "PASS" if assertion["result"] == "PASS" else "FAIL"
        viewer_lines.append(f"- [{mark}] {assertion['text']} — {assertion['note']}")
viewer_lines.extend([
    "",
    "## Open findings",
    "",
    "- **AGO-004 / P0:** complete two-run consensus batches are not reproducible at the accepted direct-target level.",
    "- **AGO-005 / P1:** the pinned targeted-Yeo CWL prose says 9 nt, while the executable default and live behavior are 10 nt and the CWL supplies no override.",
    "",
    "All other initial findings (AGO-001, AGO-002, AGO-003, AGO-006, AGO-007, AGO-008) are closed by independently executed evidence.",
])
write(ROOT / "viewer.md", "\n".join(viewer_lines) + "\n")

finding_ledger = """# Ordered finding ledger

## AGO-004 — P0 — Two-run agreement is not workflow-level deterministic

Two fresh complete wrapper batches used the same pinned Hyb commit, official
input, named database, single-thread controls, and two replicates. Both batches
retained 94 and excluded 17 assignments, but their accepted outputs were not
the same: seven read ids were accepted only in each batch and four shared read
ids had different normalized assignments. The candidate's statement that the
two-run parser retains "stable" assignments is therefore not supported at the
workflow level. This fails the result-determinism and methodological-ground
vetoes even though each individual pair reconciles and replays correctly.

## AGO-005 — P1 — Targeted-Yeo UMI length remains internally inconsistent

The candidate says the pinned targeted-miR route takes a nine-nucleotide UMI
from read 2. At source commit `75fe74e`, `extract_r2_umi.cwl` repeats that in
prose, but it does not bind `--umi_length`; `targeted_miR_umi.py` defaults to
10, and a live bounded invocation appended ten R2 bases. The skill must not
state an exact operational length until it requires a protocol-declared value
and passes that value explicitly through a pinned route.

## Closed initial findings

- AGO-001: closed — current named-database/goal/id/output Hyb contract executed.
- AGO-002: closed — orientation-aware 16-column parser passed real and synthetic controls.
- AGO-003: closed — quoting, validation, status propagation, staged publication, and replacement safety passed.
- AGO-006: closed — current tool identities and access states are separated.
- AGO-007: closed — counts, absent overlaps, and example thresholds have bounded interpretations.
- AGO-008: closed — structured outputs, manifests, reason codes, safe reruns, and focused tests are shipped.
"""
write(ROOT / "finding-ledger.md", finding_ledger)

execution = """# Execution classifications

## Executed

- Exact candidate shipped suite: 5/5 tests pass.
- Independent parser/wrapper adversarial harness: 9/9 assertions pass.
- Pinned Hyb `028ab63` official input: two fresh complete two-run wrapper batches (four underlying Hyb runs), 111 valid 16-column rows per run.
- Cross-batch consensus comparison at accepted-id and normalized-assignment level.
- Targeted-Yeo `targeted_miR_umi.py` default on bounded paired FASTQ.
- TargetScan plus/minus exon-spanning projection, release/range failures, and `bedtools intersect -split -s` overlap.

## Static or public-interface only

- Standard AGO peak calling and computational assignment outside the bundled converter.
- miRDB 6 public data and prediction-service descriptions.
- `hybkit` distinction from the Hyb direct-chimera engine.

## Resource-infeasible

- Full human Yeo chimeric-eCLIP CWL workflow without a real library and species-matched repeat/genome STAR indices.

## Biological route unavailable

- HEAP Halo-Ago2 library preparation and orthogonal reporter validation.

## Remote unavailable

- DIANA microT-CDS documented example endpoint (previously returned HTTP 500); not credited as executed.
"""
write(ROOT / "execution-classifications.md", execution)

source_notes = """# Scientific source notes

- The executable direct-chimera route is public Hyb commit `028ab6371ce793ca5e86f475fce1f2cc6ad3c677`; the commit, not GNU Make's version text, is the tool identity.
- The Yeo chimeric-eCLIP source is pinned at `75fe74e90e6e4ca670a5af76836d80db09bdbcb1`. Total-route 10-nt R1 extraction and targeted-route R2 extraction are distinct.
- The targeted source itself is contradictory: CWL prose says 9 nt, executable default is 10, and the CWL does not supply a length. The audit does not choose a biological truth from that conflict.
- TargetScanHuman 8 coordinates are treated as transcript/UTR relative and require an assembly-, annotation-, release-, and strand-matched spliced map before genomic overlap.
- HEAP is a Halo-Ago2 transgenic-mouse experimental method with public data and associated analysis code, not a standalone human HEAP CLI.
- Chimera read counts are recovery evidence affected by expression, ligation, amplification, depth, and filtering; they are not treated as binding affinity.
"""
write(ROOT / "scientific-source-notes.md", source_notes)

test_inputs = """# Re-audit test inputs

1. Canonical: run the exact current-Hyb wrapper twice as two independent two-replicate batches on pinned official input and compare accepted direct-target content, not only counts.
2. Variant A: challenge space/literal-glob paths, overwrite refusal, failing replacement, status 42 propagation, prior-output preservation, and staging cleanup.
3. Edge: exercise both 16-column RNA orientations, expression provenance, missing-versus-different assignment reasons, malformed row width, and malformed expression header.
4. Variant B: project plus/minus exon-spanning TargetScan sites to BED12, run `-split -s`, and reject release mismatch and out-of-range coordinates.
5. Stress: reconcile total versus targeted Yeo UMI layouts and classify Hyb, Yeo, HEAP, TargetScan, miRDB, DIANA, and standard AGO surfaces without overclaiming execution.
"""
write(ROOT / "inputs/test-inputs.md", test_inputs)

candidate_files = []
manifest_rows = []
for path in sorted((p for p in CANDIDATE.rglob("*") if p.is_file()), key=lambda p: p.relative_to(CANDIDATE).as_posix().encode("utf-8")):
    relative = path.relative_to(CANDIDATE).as_posix()
    raw = path.read_bytes()
    file_sha = hashlib.sha256(raw).hexdigest()
    blob = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    candidate_files.append({"path": relative, "bytes": len(raw), "git_blob": blob, "sha256": file_sha})
    manifest_rows.append(f"{relative}\t{len(raw)}\t{file_sha}")
identity = hashlib.sha256("\n".join(manifest_rows).encode()).hexdigest()

artifact_paths = [
    "report.json",
    "viewer.md",
    "finding-ledger.md",
    "execution-classifications.md",
    "scientific-source-notes.md",
    "inputs/test-inputs.md",
    "scripts/run_reaudit.sh",
    "scripts/reaudit_contracts.py",
    "scripts/compare_hyb_pairs.py",
    "scripts/yeo_targeted_check.py",
    "scripts/targetscan_overlap_check.py",
    "scripts/build_report.py",
    "validate_report.py",
    "evidence/shipped-tests.stdout",
    "evidence/shipped-tests.stderr",
    "evidence/contract-tests.stdout",
    "evidence/contract-tests.stderr",
    "evidence/contract-results.json",
    "evidence/hyb-pair-a.stdout",
    "evidence/hyb-pair-a.stderr",
    "evidence/hyb-pair-b.stdout",
    "evidence/hyb-pair-b.stderr",
    "evidence/hyb-repeatability.json",
    "evidence/yeo-targeted-contract.json",
    "evidence/targetscan-contract.json",
    "evidence/schema-validation.json",
]
artifacts = {relative: sha(ROOT / relative) for relative in artifact_paths}

source_identity = {
    "origin": {
        "repository": "GPTomics/bioSkills",
        "commit": "d91ed3d563019e649dc854c56ccd62551359488a",
        "path": "clip-seq/ago-clip-mirna-targets",
        "subtree": "6326a423789826240d0840be6897ddd69b21d940",
        "checkout": "F:\\optimizing-agent-science-skills\\external\\GPTomics__bioSkills",
        "status": "read-only source identity",
    },
    "candidate": {
        "branch": "optimize/ten-20260928-lane4-ago-clip",
        "commit": "0bc0b31fc52742dbec1034f698103434cc9460c3",
        "path": "F:\\OpenScience\\wt\\opt10-ago-clip\\skills\\bio-clip-seq-ago-clip-mirna-targets",
        "status_before": "untracked fixed subtree only",
        "status_after_execution": "untracked fixed subtree only; no candidate bytes changed",
        "content_sha256": identity,
        "content_manifest": {
            "file_count": len(candidate_files),
            "bytes": len("\n".join(manifest_rows).encode()),
            "recipe": "relative POSIX path, byte count, and lowercase SHA-256 separated by TAB; paths sorted with ordinal bytewise ordering; LF joins; no trailing LF",
        },
        "files": candidate_files,
    },
    "tooling": {
        "tools_md_sha256": sha(TOOLING / "TOOLS.md"),
        "environment_fingerprint_sha256": sha(TOOLING / "environment-fingerprint.json"),
        "environment_lock_sha256": sha(TOOLING / "environment-explicit.lock"),
        "rubric_skill_sha256": sha(ROOT / "skill-auditor/SKILL.md"),
    },
    "execution_classification": {
        "accessible_and_rerun": [
            "exact candidate shipped suite",
            "independent parser and wrapper adversarial matrix",
            "two fresh complete two-run current-Hyb batches on official input",
            "targeted-Yeo default extraction smoke",
            "TargetScan conversion and bedtools block/strand controls",
        ],
        "static_or_interface_only": ["standard AGO peak-calling route", "miRDB 6", "hybkit identity"],
        "resource_infeasible_bounded": ["complete human Yeo chimeric-eCLIP CWL workflow"],
        "wet_lab_unavailable": ["HEAP Halo-Ago2 library preparation", "orthogonal reporter validation"],
        "remote_unavailable": ["DIANA microT-CDS example endpoint"],
    },
    "audit_artifacts": artifacts,
    "candidate_cache_artifacts_after_execution": [],
}
if identity != "21c6ba09ec3580896c35adbe5175ac2e7bf161870e912e46d2bbca42190cfebc":
    raise SystemExit(f"candidate identity changed: {identity}")
write(ROOT / "source-identity.json", json.dumps(source_identity, indent=2, sort_keys=True) + "\n")
print(json.dumps({"candidate_identity": identity, "report_sha256": sha(ROOT / "report.json"), "viewer_sha256": sha(ROOT / "viewer.md"), "source_identity_sha256": sha(ROOT / "source-identity.json")}, indent=2))

