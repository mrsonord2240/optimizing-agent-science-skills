> **Audit record for `bio-machine-learning-atlas-mapping`**
> - Audited working candidate `8b4d96ad2465bd169dffb835c808d5783981f4acdc1f1e1121dbd9ab78dfbc04`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/machine-learning/atlas-mapping), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-machine-learning-atlas-mapping

Generated: 2026-10-03  
Audit type: independent final re-audit (candidate certification, final mode)  
Exact candidate content SHA-256: `8b4d96ad2465bd169dffb835c808d5783981f4acdc1f1e1121dbd9ab78dfbc04`

## Decision

**candidate-ready** for the exact identity above. Final score 87 (Production Ready), static 88, execution average 85.7 (Layer 1 avg 33.8/40, Layer 2 avg 51.8/60), assertion pass rate 28/29 = 96.6%, no veto, no P0/P1. One P2 (AM-008, a small script change) stays open; it fails closed and does not block readiness. The execution average clears its 85 gate by 0.7 points, driven down by the stress input.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 36 | 55 | 91 | 5/5 | ✅ COMPLETED |
| 2 | Variant A | 36 | 54 | 90 | 5/5 | ✅ COMPLETED |
| 3 | Edge | 34 | 53 | 87 | 5/5 | ✅ COMPLETED |
| 4 | Edge | 34 | 53 | 87 | 5/5 | ✅ COMPLETED |
| 5 | Variant B | 34 | 52 | 86 | 4/4 | ✅ COMPLETED |
| 6 | Stress | 29 | 44 | 73 | 4/5 | ⚠️ COMPLETED |

**Execution average:** 85.7 / 100  
**Assertion pass rate:** 28 / 29  
**Static score:** 88 / 100  
**Final score:** 87 / 100 - ⭐ Production Ready  
**Research veto:** PASS

Prior: d4048dcc887b scored 77; ba864911e88a scored 84 (Limited Release, 25/28, execution 83.3). Exact identity: [`source-identity.json`](source-identity.json).

## Prior findings (reproduced, not inherited)

| ID | Prior | Verdict on these bytes | Evidence |
|---|---|---|---|
| AM-001 | P1 | Documented-limited, not fixed in the method. The gate still passes the adjacent mislabel (kNN 1.59%, distance gate 0.0% at p99); the Skill states this, measures it, and mandates the curated marker check, which flags DC at 0.160 and 0.525 | scripts/evidence/summary_f_*.json, distgate_d_*.json |
| AM-006 | P1 | Fixed. No-flag run: rc 2, usage error, empty stdout, in all four runs. Script and SKILL.md/usage-guide contain no reference-derived path; absent markers give NOT CHECKED plus UNVERIFIED count, never a pass. Edge: an all-unchecked marker file crashes (AM-008) | scripts/evidence/driven_marker_runs.log |
| AM-007 | P2 | Fixed. Header plain; usage-guide step 6 and Tips name the marker check; threshold stated with p95 cost (25.4% / 99.4% of held-out cells, 7.7% / 14.3% overall, reproduced); T cells 8 of 8 markers, 0.703 not flagged; UNVERIFIED line on every run | SKILL.md, usage-guide.md, scripts/evidence/ |
| AM-002 | P2 | Still fixed: Version Compatibility lists Symphony, Azimuth, scPoli, popV, treeArches/scHPL, scGPT/Geneformer as not executed | SKILL.md |
| AM-003 | P2 | Still fixed: DataFrame (2638, 8) observed | scripts/evidence/snippets_result.json |
| AM-004 | P2 | Still fixed: SKILL.md blocks ran as written; script docstring states the input contract | scripts/evidence/snippets_result.json |
| AM-005 | P2 | Still fixed: labels 2638/2638 identical, latent diff 0.0, query_annotated.h5ad written | scripts/evidence/compare_none.log |

## Executed versus static-only

| Surface | Classification | Evidence |
|---|---|---|
| scripts/scarches_annotation.py (baseline x2, Monocytes removed, B cells removed) | executed | scripts/run_case.py, scripts/evidence/summary_f_*.json |
| scripts/label_marker_check.py: no flag, curated markers x4, own markers, empty markers | executed | scripts/evidence/marker_curated_*.tsv, driven_marker_runs.log |
| SKILL.md python blocks 1-3 as written | executed | scripts/run_skill_snippets.py, scripts/evidence/snippets_result.json |
| Distance-gate claim (own script, p99 and p95) | executed | scripts/distance_gate_check.py, scripts/evidence/distgate_d_*.json |
| scripts/ood_gating_demo.py | executed | scripts/evidence/ood_demo.log |
| Symphony, Azimuth/Seurat (prose only) | static-only; labelled not executed or bundled | n/a |
| scPoli, popV, treeArches/scHPL, scGPT/Geneformer | static-only, heavy-optional; labelled not executed | n/a |

## Judgment points

(a) The 0.6 cutoff is workable but not comfortable. Baseline T cells 0.703 (0.10 above), 0.696 and 0.701 in the hold-outs; the true flag in the B-cell hold-out is 0.525 (0.075 below). The cutoff sits in a 0.17 gap with margins of 0.075 to 0.10 on both sides, validated on one PBMC pair with silver labels. SKILL.md discloses 'set a priori, checked on the PBMC pair only' and 'recalibrate per tissue'; it does not say the T-cell markers were chosen before testing, which is fine, and it gives no margin figures.
(b) The script reports n_markers (markers with detection in the reference) per label, and lists labels with no usable markers as NOT CHECKED with an UNVERIFIED count. It does not show markers listed versus used and does not warn on a low count: a driven run judged DC on a single marker (retained 1.000, n_markers=1) with no flag. Adequate for the fixed curated set (DC 4 of 6, Monocytes 5 of 7), weak for agent-authored markers (AM-008).
(c) Read as an agent, SKILL.md would not trust a confidently wrong label: the opening insight, the measured table, 'Never report gated labels as validated', the mandatory marker check and the UNVERIFIED rule all point the same way. The residual risk is an agent that supplies generic same-lineage markers, which the group-level check cannot catch; this is disclosed.
(d) AM-002 to AM-005 not regressed (table above).

## Veto review

- Skill veto: PASS (stability, contract, determinism, security all PASS).
- Research veto: PASS
  - scientific_integrity: PASS - Every measured claim reproduced: kNN gate 1.67% / 1.59% / 76.3% Unknown, 604 of 630 held-out monocytes called DC, curated marker check DC 0.160 and 0.525 with nothing flagged at baseline, distance gate 0.0% at p99 and 25.4% / 99.4% at p95 with 7.7% / 14.3% overall false flags.
  - practice_boundaries: PASS - Research-use single-cell annotation; no diagnostic or prescriptive medical conclusions.
  - methodological_ground: PASS - The limitation (a missing type adjacent to a reference type is confidently mislabelled and no latent gate catches it) is stated in the opening insight, a measured table, the thresholds table and the usage guide; the only shipped verdict path requires curated markers, and labels it cannot check are reported as UNVERIFIED with a count. The marker cutoff is disclosed as set a priori and checked on one PBMC pair only.
  - code_usability: PASS - All shipped scripts and the SKILL.md python blocks ran as written on CPU (scvi-tools 1.5.1) with no errors; label_marker_check.py with no flag exits 2 with a usage error and no verdict.

## Static categories

- functional_suitability: 11/12 - Core scArches/scANVI mapping, kNN gate and a curated-marker agreement check are covered and executable; Symphony, Azimuth, scPoli, popV, treeArches and foundation models are labelled prose-only/not executed; the gate itself remains blind to a missing adjacent type, which is documented as limited.
- reliability: 10/12 - Seeded and deterministic (labels identical 2638/2638, latent diff 0.0); no-flag marker check fails closed (rc 2, no verdict); no shared-gene guard in the scripts; marker check dies with an AttributeError traceback when no label receives a verdict (AM-008).
- performance_context: 7/8 - SKILL.md is long but navigable; failure modes routed to a reference file.
- agent_usability: 15/16 - Limitation stated up front, in a measured table and in the usage guide; marker check is mandatory and its UNVERIFIED line makes unchecked labels visible; the per-label table shows markers used but not markers listed.
- human_usability: 7/8 - Triggers and usage-guide prompts fit user wording; usage guide now names the marker check.
- security: 11/12 - No credentials, network or shell; scripts read local h5ad/JSON and write h5ad/TSV in the working directory.
- maintainability: 10/12 - Clean split into SKILL.md, failure-modes, curated markers JSON and three scripts with input contracts in docstrings; gate logic duplicated across SKILL.md, script and demo.
- agent_specific: 17/20 - Precise description with sibling scope pointers and progressive disclosure; bundled curated markers cover PBMC and a 1604-gene set only, so other tissues need agent-authored markers.

## Detailed outputs

### Input 1 - Canonical: scripts/scarches_annotation.py unmodified on the staged PBMC pair, run twice (seeded), then label_marker_check.py with curated markers

**Status:** COMPLETED - Two independent runs: 2638/2638 labels identical, latent X_scANVI and transfer_uncertainty max diff 0.0, 1.67% Unknown, query_annotated.h5ad (2638x1604; adds predicted_label, transfer_uncertainty) written. Curated check at baseline: T 0.703 (8 of 8 markers), Monocytes 0.900, B 0.784, ILC 0.916, DC 0.955, nothing flagged; UNVERIFIED 13 of 2594 (Megakaryocytes/platelets, n=13 under 20).  
**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100

**Assertions:**

- PASS - Script runs unmodified from the staged inputs and writes query_annotated.h5ad (rc 0 twice; 2638x1604, obs has predicted_label and transfer_uncertainty)
- PASS - Identical seeded reruns (labels 1.0 identical, latent maxdiff 0.0, uncertainty maxdiff 0.0)
- PASS - Gate result matches SKILL.md baseline (1.7% Unknown) (1.668%)
- PASS - Curated check raises no false flag at baseline and now verifies T cells (none flagged; T 0.703 on 8/8 markers)
- PASS - Run ends by pointing to the curated check; unchecked labels counted (final print line names label_marker_check.py --markers; UNVERIFIED 13 of 2594 printed)

### Input 2 - Variant A: SKILL.md python blocks 1-3 executed as written (200/100/20/100 epochs) against a saved reference_model/

**Status:** COMPLETED - Blocks ran in order without edits (86 s, 131 s, 0 s). scVI query latent (2638, 30), scANVI latent (2638, 30), predict(soft=True) returned a DataFrame (2638, 8) with rows summing to 1, kNN gate flagged 1.3% Unknown, accuracy vs PBMC3k annotation 0.985 on non-Unknown cells.  
**Scores:** Basic 36/40 | Specialized 54/60 | Total 90/100

**Assertions:**

- PASS - Block 1 (scVI surgery) runs as written (query latent (2638, 30))
- PASS - Block 2 (scANVI transfer) runs as written (X_scANVI (2638, 30))
- PASS - predict(soft=True) is described as a DataFrame and is one (DataFrame (2638, 8), rows sum to 1)
- PASS - Block 3 (kNN gate) runs and flags a plausible fraction (1.3% Unknown)
- PASS - Labels agree with the silver truth outside Unknown (0.985 (0.972 overall))

### Input 3 - Edge: Held-out Monocytes: reference without Monocytes, map PBMC3k, curated markers, own distance gate

**Status:** COMPLETED - kNN gate 1.59% Unknown, 604 of 630 held-out monocytes called DC. Own distance gate: 0.0% at p99, 25.4% of monocytes at p95 with 7.7% of all query cells flagged. Curated markers flag DC at 0.160 (641 cells); T 0.696, B 0.789, ILC 0.886 pass. UNVERIFIED 17 of 2600. No-flag run: rc 2, usage error, empty stdout.  
**Scores:** Basic 34/40 | Specialized 53/60 | Total 87/100

**Assertions:**

- PASS - SKILL.md measured table reproduces (1.6% gated, DC 95.9%, distance gate 0.0%) (1.59%, 604/630, 0.0% at p99)
- PASS - Curated check flags the adjacent mislabel (DC 0.160 flagged)
- PASS - No-flag run yields no verdict (rc 2, usage error, stdout empty)
- PASS - Disclosed p95 cost of loosening the distance gate reproduces (25.4% of monocytes, 7.7% overall)
- PASS - Unchecked labels are counted (Megakaryocytes/platelets n=17, UNVERIFIED 17 of 2600)

### Input 4 - Edge: Held-out B cells: reference without B cells, map PBMC3k, curated markers, own distance gate

**Status:** COMPLETED - kNN gate 76.3% Unknown (261/342), 68 called DC; own distance gate 0.0% at p99, 99.4% of B cells at p95 with 14.3% overall flags. Curated DC retained 0.525 FLAGGED (94 cells); T 0.701, Monocytes 0.901, ILC 0.916 pass. UNVERIFIED 12 of 2321.  
**Scores:** Basic 34/40 | Specialized 53/60 | Total 87/100

**Assertions:**

- PASS - SKILL.md table reproduces (76.3% Unknown, DC 19.9%) (261/342, 68/342)
- PASS - Curated check flags the mislabelled neighbour (DC 0.525 flagged)
- PASS - Other labels are not falsely flagged (T 0.701, Mono 0.901, ILC 0.916)
- PASS - Disclosed p95 cost reproduces (99.4% of B cells, 14.3% overall)
- PASS - Unchecked labels are counted (UNVERIFIED 12 of 2321)

### Input 5 - Variant B: scripts/ood_gating_demo.py synthetic far-cluster demonstration

**Status:** COMPLETED - rc 0, 4 s: novel cluster passes a 0.5 kNN-probability filter but is caught by the distance gate (81 Unknown), known cells 0% flagged; docstring states this is the easy case only.  
**Scores:** Basic 34/40 | Specialized 52/60 | Total 86/100

**Assertions:**

- PASS - Demo runs without error (rc 0)
- PASS - Distance gate flags the novel cluster and spares known cells (81 Unknown; known wrongly flagged 0%)
- PASS - Probability filter labelled as a stand-in for softmax (comment and docstring)
- PASS - Demo states the real-data adjacent-type case is not caught (docstring limit sentence)

### Input 6 - Stress: Agent-driven marker check from SKILL.md instructions: own markers.json with genes absent from the 1604-gene set, an empty marker file, and the no-flag call

**Status:** COMPLETED - Own markers (CD3D/CD3E/IL7R/CD2 for T, JCHAIN/XBP1/SDC1/MZB1 for Plasma, CST3/HLA-DPB1 for DC): T cells, ILC, Megakaryocytes get 0 usable markers and are listed NOT CHECKED, UNVERIFIED 1584 of 2594 (61.1%) printed; DC is judged on one marker (retained 1.000, n_markers=1) with no listed-versus-used count and no low-count warning; the line 'Flagged labels: none' is still printed. Empty {} markers: all labels NOT CHECKED, then an AttributeError traceback (rc 1) instead of a message, and the UNVERIFIED line is lost. No-flag: rc 2, no verdict.  
**Scores:** Basic 29/40 | Specialized 44/60 | Total 73/100

**Assertions:**

- PASS - No-flag call gives no verdict (rc 2, usage error)
- PASS - Labels with no usable markers are never passed silently (NOT CHECKED list plus UNVERIFIED 61.1% on own markers)
- PASS - Per-label table shows how many markers backed each verdict (n_markers column (DC 1, Monocytes 2, B cells 2))
- PASS - A label judged on very few markers is flagged or its listed count shown (visible only as n_markers=1; no listed count, no warning (judged adequate but weak, see AM-008))
- FAIL - When no label receives a verdict the script ends with a message, not a traceback (AttributeError 'DataFrame' object has no attribute 'flagged', rc 1 (fails closed, UNVERIFIED line not printed) (AM-008))

## Key strengths

- No-flag and absent-marker paths fail closed: rc 2 usage error with no verdict, and every unchecked label is listed with a counted UNVERIFIED line
- Limitation is stated up front, in a measured table and in the usage guide, and every measured number (kNN gate, distance gate at p99 and p95, curated DC 0.160 / 0.525) reproduced in this independent run
- Seeded, persisting, deterministic real-data template; SKILL.md snippets run as written on scvi-tools 1.5.1
- Prose-only (Symphony, Azimuth) and heavy-optional methods (scPoli, popV, treeArches, foundation models) are explicitly labelled not executed

## Recommendations

- **[P2] AM-008 Marker check: no message when nothing is checkable, and no listed-versus-used marker count** (inputs [6]): With a marker file that matches no predicted label (empty {} or genes absent from the gene set for every label) label_marker_check.py prints NOT CHECKED then dies with AttributeError (rc 1) and never prints the UNVERIFIED line. Separately a label can be judged on one marker (DC retained 1.000 on 1 of 3 listed) with only the n_markers column as evidence. Fix: Guard the empty result (print the UNVERIFIED line and exit non-zero with a message), add an n_listed column and warn when n_markers is below 3. Small script change; the SKILL.md wording needs no change.

## Ordered finding ledger

| Order | ID | Priority | State | Evidence inputs | Required disposition |
|---:|---|---|---|---|---|
| 1 | AM-008 | P2 | open (non-blocking) | [6] | Marker check: no message when nothing is checkable, and no listed-versus-used marker count. Guard the empty result (print the UNVERIFIED line and exit non-zero with a message), add an n_listed column and warn when n_markers is below 3. Small script change; the SKILL.md wording needs no change. |

AM-001 documented-limited; AM-002 to AM-007 resolved. No audit-local repair was made; no Skill bytes changed.
