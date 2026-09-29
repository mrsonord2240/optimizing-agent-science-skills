> **Audit record for `bio-comparative-genomics-ancestral-reconstruction`**
> - Audited working candidate `a9eb2d1e1c3ac7f89d63f11deb7a436c14ab0c78a6469911812aa510eeb93e07`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/comparative-genomics/ancestral-reconstruction), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-comparative-genomics-ancestral-reconstruction

Generated: 2026-09-28 (America/Los_Angeles). This independent final re-audit evaluates the exact candidate identity in [`source-identity.json`](source-identity.json).

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical PAML codon | 39 | 58 | 97 | 5/5 | ✅ |
| 2 | PAML protein variants | 39 | 58 | 97 | 5/5 | ✅ |
| 3 | Reused unaffected workflows | 36 | 55 | 91 | 5/5 | ✅ |

**Static score:** 88/100  
**Execution average:** 95.0/100  
**Assertion pass rate:** 15/15  
**Weighted final score:** 92/100 — ⭐ Production Ready. Both veto gates pass. All final readiness floors are met: static 88, execution 95.0, Layer 1 average 38, Layer 2 average 57, and 100% assertion pass rate.

## Input 1 — Fresh PAML codon ancestral reconstruction

The candidate's codon control-file writer ran CODONML 4.10.10 on the retained eight-sequence, 110-site fixture. CODONML exited 0 and generated a fresh `rst`; the candidate parser returned seven nodes and 770 codon/ amino-acid posterior records. The focused test compared all states and probability fields at all 110 sites against the rows in that exact run's `rst`.

Evidence: [`run_codon_paml.py`](run_codon_paml.py), [`result.json`](evidence/real-codon-paml/result.json), [`paml-focused.log`](evidence/paml-focused.log).

| Assertion | Result | Evidence |
|---|---|---|
| Current CODONML run completes and produces a marginal `rst` | PASS | PAML 4.10.10 exit 0; fresh output SHA recorded. |
| Parser returns 7 nodes × 110 sites | PASS | 770 records. |
| Every state and codon/amino-acid posterior matches the exact source row | PASS | All nodes and sites inspected. |
| Posterior bounds and codon-to-amino-acid consistency hold | PASS | All records checked. |
| Four focused parser/unit tests pass | PASS | 4/4. |

## Input 2 — Two PAML protein writer/parser routes

Both shipped writer routes ran CODeml 4.10.10 on the protein fixture. Each produced a fresh 7 × 110 `rst`. The shared source-row oracle checked every state/probability record; the results are route-specific, so no exact posterior magnitude is reused as a universal expectation.

Evidence: [`run_protein_paml.py`](run_protein_paml.py), [`provider/result.json`](evidence/real-protein-paml/provider/result.json), [`extracted/result.json`](evidence/real-protein-paml/extracted/result.json), [`protein-paml-focused.log`](evidence/protein-paml-focused.log).

| Assertion | Result | Evidence |
|---|---|---|
| Provider and extracted writer routes complete with current PAML | PASS | Both invocations exited 0. |
| Each parser returns 7 nodes × 110 sites | PASS | 770 records per route. |
| Every parsed value matches its own run's PAML source row | PASS | All sites and nodes checked for both routes. |
| Public wrapper APIs retain residue and probability semantics | PASS | Provider and extracted shapes inspected. |
| Real-fixture tests avoid brittle exact posterior constants | PASS | Expectations come from each `rst`; synthetic controls remain deterministic. |

## Input 3 — Reused unaffected core workflows and outputs

Evidence was reused only where relevant candidate bytes, environment lock/runtime, interfaces, input provenance, and assumptions were unchanged. Live checks confirmed Python 3.12.14, IQ-TREE 2.4.0, OpenJDK 21.0.10, R 4.4.3, ape 5.8.1, phytools 2.5.2, geiger 2.0.12, corHMM 2.8, OUwie 3.0.3, and the recorded environment lock SHA-256.

Evidence: [`runtime-boundary.log`](evidence/runtime-boundary.log), [`reuse-validation.json`](evidence/reuse-validation.json), fixed-phase IQ-TREE/GRASP/R evidence in `../fix-opt11-20260928/evidence/`.

| Assertion | Result | Evidence |
|---|---|---|
| IQ-TREE output validates and malformed posterior tables reject | PASS | 660 rows; posterior sums and maximum states validated; five invalid controls rejected. |
| Current GRASP CLI and candidate wrapper produce advertised outputs | PASS | Seven 110-column ancestor sequences, eight tips, structured JSON. |
| Seeded discrete mapping reports maps and rejects taxon mismatch | PASS | 1,000 maps and named taxon error. |
| BM and OU routes report distinct uncertainty limits; transformed winners refuse substitution | PASS | 34 BM intervals, 29 OUwie exploratory points without uncertainty, four refusals. |
| Reused evidence still matches fixed bytes/runtime/interfaces/assumptions | PASS | Current 17-file manifest matches fix-phase manifest; lock and live versions match. |

## Vetoes and recommendations

- Structural/security veto: PASS.
- Research integrity veto: PASS.
- Open P0/P1/P2 findings: none.
- Optional documentation-only tools are not counted as executed support; they require their own current interface/output validation before being described as executable workflows.
- Recommendations: none.
