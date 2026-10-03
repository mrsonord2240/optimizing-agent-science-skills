> **Audit record for `bio-machine-learning-atlas-mapping`**
> - Audited working candidate `ba864911e88a7d48e4576f9f7f4f1668ef0ed85ddd429c151bbb6ebfc39cd094`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/machine-learning/atlas-mapping), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-machine-learning-atlas-mapping

Generated: 2026-10-03  
Audit type: independent final re-audit (candidate certification)  
Exact candidate content SHA-256: `ba864911e88a7d48e4576f9f7f4f1668ef0ed85ddd429c151bbb6ebfc39cd094`

## Decision

**NOT candidate-ready.** The exact bytes miss two canonical gates: assertion pass rate 25/28 = 89.3% (needs 90%) and execution average 83.3 (needs 85). Static score, Layer 1 and Layer 2 averages, and veto status pass. One P1 (AM-006) and one P2 (AM-007) remain; AM-001 is cleared as a prose overclaim but not as a safe default path. Route to the fixer; both remaining items are small (one localized script change, the rest text).

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 36 | 54 | 90 | 5/5 | ✅ COMPLETED |
| 2 | Variant A | 35 | 53 | 88 | 5/5 | ✅ COMPLETED |
| 3 | Edge | 31 | 49 | 80 | 4/5 | ✅ COMPLETED |
| 4 | Edge | 32 | 50 | 82 | 4/5 | ✅ COMPLETED |
| 5 | Variant B | 34 | 52 | 86 | 4/4 | ✅ COMPLETED |
| 6 | Stress | 29 | 45 | 74 | 3/4 | ⚠️ COMPLETED |

**Execution average:** 83.3 / 100 (Layer 1 avg 32.8/40, Layer 2 avg 50.5/60)  
**Assertion pass rate:** 25 / 28  
**Static score:** 85 / 100  
**Final score:** 84 / 100 - ✅ Limited Release  
**Research veto:** PASS

Prior audit d4048dcc887b scored 77 with 14/23 assertions. Exact identity: [`source-identity.json`](source-identity.json).

## Prior findings (reproduced, not inherited)

| ID | Prior | Verdict on these bytes | Evidence |
|---|---|---|---|
| AM-001 | P1 | Partly cleared. Limitation is stated prominently and accurately and every table number reproduces; the gate is unchanged and the default check mode still misses the case. Residual filed as AM-006 (P1) and AM-007 (P2) | scripts/evidence/summary_r_*.json, distgate_d_*.json, marker_*_*.tsv |
| AM-002 | P2 | Fixed: Version Compatibility names Symphony, Azimuth, scPoli, popV, treeArches/scHPL, scGPT/Geneformer as not executed or bundled | SKILL.md Version Compatibility |
| AM-003 | P2 | Fixed: text states DataFrame; observed DataFrame (2638,8) | scripts/evidence/snippets_result.json |
| AM-004 | P2 | Fixed: SKILL.md blocks ran as written; script docstring states the input contract | scripts/evidence/snippets_result.json |
| AM-005 | P2 | Fixed: labels identical across runs, latent diff 0.0, query_annotated.h5ad written | scripts/evidence/compare_none.log |

## Executed versus static-only

| Surface | Classification | Evidence |
|---|---|---|
| scripts/scarches_annotation.py (none / Monocytes removed / B cells removed) | executed | scripts/run_case.py, scripts/evidence/summary_r_*.json |
| scripts/label_marker_check.py, curated and default markers, all three cases | executed | scripts/evidence/marker_*.tsv, summary_r_*.json |
| SKILL.md python blocks 1-3 as written | executed | scripts/run_skill_snippets.py, scripts/evidence/snippets_result.json |
| Reference-calibrated distance gate claim (table column) | executed (own script) | scripts/distance_gate_check.py, scripts/evidence/distgate_d_*.json |
| scripts/ood_gating_demo.py | executed | scripts/evidence/ood_demo.log |
| Symphony, Azimuth/Seurat (prose only) | static-only; labelled not executed or bundled in SKILL.md | n/a |
| scPoli, popV, treeArches/scHPL, scGPT/Geneformer | static-only, heavy-optional; labelled not executed in SKILL.md | n/a |

## Answers to the AM-001 questions

1. Numbers reproduce in this independent run (kNN gate Unknown 1.67% baseline, 1.59% Monocytes removed with 604/630 called DC, 76.3% B removed with 68 called DC; curated DC 0.160 and 0.525, nothing at baseline; derived DC 0.730 missed, T cells 0.563 false flag, T cells 0.605 at baseline; T cells NOT CHECKED with curated markers). The SKILL.md python blocks ran as written. A distance gate I computed myself (p99 of reference self-distances) flags 0.0% in both hold-outs; at p95 it flags 25% of monocytes and 99% of B cells but also 7.7% and 14.3% of all query cells.
2. The limitation is prominent (opening insight, a measured table, thresholds table, Common Errors row) and accurate. The header 'the step that makes labels trustworthy' and the usage guide still undersell it (AM-007).
3. The default is not acceptable as shipped. With no flags the script prints 'Flagged labels: none' on the Monocytes hold-out. The reason is checked: derived DC markers are LYZ, FTH1, HLA-DRB1, FGL2, CPVL (generic myeloid). The SKILL.md command line does show --markers, which is why this is rated against the script rather than the prose. Requiring --markers (or a loud banner) is needed for readiness.
4. Prose plus the check clears the overclaim, not the hazard. Following SKILL.md literally catches both hold-outs, but the shipped default path still lets the missing adjacent type through unflagged, so a P1 remains (AM-006).

## Veto review

- Skill veto: PASS (stability, contract, determinism, security all PASS).
- Research veto: PASS
  - scientific_integrity: PASS - Measured claims in SKILL.md reproduce: kNN gate 1.7%/1.6%/76.3% Unknown, 604/630 monocytes called DC, curated marker check DC 0.160/0.525, derived markers DC 0.730 and T cells 0.563; citations and thresholds unchanged and accurate.
  - practice_boundaries: PASS - Research-use single-cell annotation; no diagnostic or prescriptive medical conclusions.
  - methodological_ground: PASS - The limitation (a missing type adjacent to a reference type is confidently mislabelled and no latent gate catches it) is stated in the opening insight, a measured table and the thresholds table, and the Skill tells the agent to run a marker check with curated markers; the section header still overclaims and the check's default mode is unreliable (AM-006, AM-007), so this is a residual overclaim, not an inverted conclusion.
  - code_usability: PASS - All shipped scripts and the SKILL.md python blocks ran as written on CPU (scvi-tools 1.5.1); no errors.

## Static categories

- functional_suitability: 10/12 - Core scArches/scANVI mapping, kNN gate and a marker-agreement check are covered and executable; Symphony, Azimuth, scPoli, popV, treeArches and foundation models are labelled prose-only/not executed; the shipped check misses the monocyte case in its default mode (AM-006).
- reliability: 9/12 - Seeded and deterministic (labels identical, latent diff 0.0 across runs); no input-contract or shared-gene guard in the scripts; label_marker_check.py exits 0 and prints 'Flagged labels: none' in default mode on a held-out monocyte case; curated T-cell markers are unusable on the shipped 1604-gene set.
- performance_context: 7/8 - SKILL.md grew to about 190 lines; failure modes stay routed to a reference; dense but navigable.
- agent_usability: 14/16 - Limitation stated up front and again after the gate with measured numbers; snippets now define ref_vae/adata_ref and state the DataFrame return type and ran as written; the header 'the step that makes labels trustworthy' and usage-guide steps 5-6 and Tips still read as if the gate suffices (AM-007).
- human_usability: 7/8 - Triggers and usage-guide prompts fit user wording; usage-guide never mentions label_marker_check.py.
- security: 11/12 - No credentials, network or shell; scripts read local h5ad/JSON and write h5ad/TSV in the working directory.
- maintainability: 10/12 - Clean split into SKILL.md, failure-modes, curated markers JSON and three scripts with input contracts in docstrings; gate logic still duplicated across SKILL.md, script and demo.
- agent_specific: 17/20 - Precise description with sibling scope pointers and progressive disclosure; the bundled curated markers cover PBMC only and the check depends on agent-authored markers elsewhere.

## Detailed outputs

### Input 1 - Canonical: scripts/scarches_annotation.py unmodified on the staged PBMC pair (harness run_case.py none), compared with the tooling run

**Status:** COMPLETED - rc 0 (about 90 s CPU): accuracy 0.963 vs PBMC3k annotation, Unknown 1.67%, mean transfer_uncertainty 0.005 for correct vs 0.160 for wrong calls; predicted labels identical to the tooling worker's run with latent diff 0.0; query_annotated.h5ad (2638x1604; predicted_label, transfer_uncertainty, X_scANVI) written.  
**Scores:** Basic 36/40 | Specialized 54/60 | Total 90/100

**Assertions:**

- PASS - Script runs unmodified end to end on a realistic pair (rc 0, h5ad written)
- PASS - Accuracy against the independent annotation >= 0.9 (0.963)
- PASS - Gate separates wrong from right calls (0.160 vs 0.005)
- PASS - Repeated runs on identical inputs are identical (AM-005) (labels identical 2638/2638, max latent diff 0.0)
- PASS - Script persists labels, uncertainty and latent (AM-005) (query_annotated.h5ad with the three fields)

### Input 2 - Variant A: SKILL.md python blocks 1-3 executed as written (200/100/20/100 epochs) against a saved reference_model/

**Status:** COMPLETED - Blocks ran in order via exec: 150 s, 85 s, under 1 s, no errors; query latents (2638,30); predict(soft=True) is a DataFrame (2638,8) with rows summing to 1; Unknown 1.3%, accuracy 0.972 (0.985 among non-Unknown). Prelude supplied only the saved scVI reference model the text assumes.  
**Scores:** Basic 35/40 | Specialized 53/60 | Total 88/100

**Assertions:**

- PASS - Blocks run as written without edits (AM-004) (ref_vae, adata_ref and adata_query defined by the text plus the assumed saved model)
- PASS - predict(soft=True) type stated in SKILL.md matches (AM-003) (text says pandas DataFrame; observed DataFrame (2638,8))
- PASS - Soft probabilities sum to 1 (rows sum to 1)
- PASS - Saved-model surgery route reaches usable accuracy >= 0.8 (0.972)
- PASS - kNN gate block yields a plausible flagged fraction (1.3% Unknown)

### Input 3 - Edge: Held-out Monocytes: reference without Monocytes, map PBMC3k, inspect 630 query monocytes; both marker modes; independent distance gate

**Status:** COMPLETED - kNN gate flagged 1.59% Unknown, 604 of 630 (95.9%) called DC. Reference-calibrated distance gate (own script, p99) flagged 0.0% (p95: 25% of monocytes at 7.7% overall false flags). Curated markers flag DC (0.160); the default reference-derived markers do not (DC 0.730, T cells 0.632), and the derived DC markers are LYZ, FTH1, HLA-DRB1, FGL2, CPVL, i.e. generic myeloid. All table values in SKILL.md reproduce.  
**Scores:** Basic 31/40 | Specialized 49/60 | Total 80/100

**Assertions:**

- PASS - Script runs unmodified on a reference lacking Monocytes (rc 0)
- PASS - SKILL.md measured table reproduces (1.6% gated, DC 95.9%, distance gate 0.0%) (1.59%, 604/630, 0.0% at p99)
- PASS - Curated-marker check flags the adjacent mislabel (DC retained 0.160, flagged)
- PASS - SKILL.md's stated default-marker result reproduces (missed) (DC 0.730, no flag)
- FAIL - Check run with its default arguments flags the mislabelled label (prints 'Flagged labels: none' with no warning that derived markers are blind (AM-006))

### Input 4 - Edge: Held-out B cells: reference without B cells, map PBMC3k, inspect 342 query B cells; both marker modes

**Status:** COMPLETED - kNN gate flagged 76.3% Unknown (261/342), 68 (19.9%) called DC; distance gate p99 0.0% (p95 99.4% at 14.3% overall false flags). Curated markers flag DC (0.525); default derived markers false-flag T cells (0.563) and pass DC (0.796), so the B-cell mislabel is not named.  
**Scores:** Basic 32/40 | Specialized 50/60 | Total 82/100

**Assertions:**

- PASS - Script runs unmodified on a reference lacking B cells (rc 0)
- PASS - SKILL.md table reproduces (76.3% Unknown, DC 19.9%) (261/342, 68/342)
- PASS - Curated-marker check flags the mislabelled neighbour (DC 0.525)
- PASS - SKILL.md's stated default-marker result reproduces (false T flag) (T cells 0.563 flagged, DC 0.796)
- FAIL - Check run with its default arguments names the mislabelled label (flags T cells (true label, 1415 cells) and passes DC (AM-006))

### Input 5 - Variant B: scripts/ood_gating_demo.py synthetic far-cluster demonstration

**Status:** COMPLETED - rc 0: 100% of novel cells pass a 0.5 kNN-probability filter, 100% caught by the distance gate, 0% of known cells flagged; docstring states the limit (easy case only) and no longer calls kNN probability a softmax.  
**Scores:** Basic 34/40 | Specialized 52/60 | Total 86/100

**Assertions:**

- PASS - Demo runs without error and reproducibly (rc 0, same counts as before)
- PASS - Distance gate flags the novel cluster, spares known cells (100% / 0%)
- PASS - Probability filter is labelled as kNN probability, a stand-in for softmax (comment and docstring)
- PASS - Demo states that the real-data adjacent-type case is not caught (docstring LIMIT sentence; matches the measured 0.0% on the PBMC hold-outs)

### Input 6 - Stress: Baseline marker-check specificity on the unmodified pair (no hold-out), curated and default markers

**Status:** COMPLETED - Curated: nothing flagged (Monocytes 0.900, B 0.784, ILC 0.916, DC 0.955) but T cells (n=1408, 53% of cells) NOT CHECKED because 0 of 6 curated markers are in the 1604-gene set. Default: nothing flagged, T cells 0.605 against the 0.6 cutoff.  
**Scores:** Basic 29/40 | Specialized 45/60 | Total 74/100

**Assertions:**

- PASS - Curated check raises no false flag at baseline (none flagged)
- PASS - Default check raises no false flag at baseline (none flagged; T cells 0.605 borderline)
- FAIL - The largest label is verified under the documented (curated) path (T cells NOT CHECKED, 1408 of 2638 cells unverified (disclosed in SKILL.md, not resolved))
- PASS - Check prints a parseable per-label table and NOT CHECKED list, writes marker_check.tsv (rc 0, table and TSV as documented)

## Key strengths

- Limitation is stated at the top and in a measured table whose every number reproduced (95.9% DC, 1.6% / 76.3% Unknown, DC 0.160 / 0.525 with curated markers)
- Seeded, persisting, deterministic real-data template; SKILL.md snippets run as written on scvi-tools 1.5.1
- Prose-only (Symphony, Azimuth) and heavy-optional methods (scPoli, popV, treeArches, foundation models) are explicitly labelled not executed
- The marker check is a genuinely independent signal that catches both hold-outs when given curated markers

## Recommendations

- **[P1] AM-006 Default marker-check mode gives false reassurance (residual of AM-001)** (inputs [3, 4, 6]): Run with no --markers, label_marker_check.py prints 'Flagged labels: none' on the Monocytes hold-out (DC 0.730; 95.9% of held-out cells called DC) and flags the wrong label (T cells 0.563) on the B-cell hold-out, with no warning. SKILL.md documents this in prose and shows --markers in its command, but the script itself is silent, so an agent that omits the flag gets a confident wrong all-clear. Even with curated markers the largest label (T cells) is NOT CHECKED on the shipped pair, and curated markers exist only for PBMC. Fix: Make --markers required (or, if the default stays, print a loud UNRELIABLE banner and qualify 'Flagged labels: none'); state in the usage text that markers must come from prior knowledge. Small localized script change plus one SKILL.md sentence; no method change.
- **[P2] AM-007 Residual overclaims and omissions around the gate and the check** (inputs [3, 4, 6]): The section header still reads 'Out-of-Distribution Gating (the step that makes labels trustworthy)'; usage-guide steps 5-6 and Tips present the gate and 'marker sanity checks' without the limitation or scripts/label_marker_check.py; the table column 'reference-calibrated distance gate 0.0%' omits its threshold (p99 of reference self-distances; at p95 it flags 25% of monocytes and 99% of B cells at 8-14% false flags overall); the bundled curated T-cell markers cannot be used on the shipped pair. Fix: Retitle the header, add the check and its limitation to usage-guide.md, state the distance-gate threshold in the table note, and note that curated T-cell markers need a gene set that contains them. Text only.

## Ordered finding ledger

| Order | ID | Priority | State | Evidence inputs | Required disposition |
|---:|---|---|---|---|---|
| 1 | AM-006 | P1 | open | [3, 4, 6] | Default marker-check mode gives false reassurance (residual of AM-001). Make --markers required (or, if the default stays, print a loud UNRELIABLE banner and qualify 'Flagged labels: none'); state in the usage text that markers must come from prior knowledge. Small localized script change plus one SKILL.md sentence; no method change. |
| 2 | AM-007 | P2 | open | [3, 4, 6] | Residual overclaims and omissions around the gate and the check. Retitle the header, add the check and its limitation to usage-guide.md, state the distance-gate threshold in the table note, and note that curated T-cell markers need a gene set that contains them. Text only. |

AM-002 to AM-005 resolved. No audit-local repair was made; no Skill bytes changed.
