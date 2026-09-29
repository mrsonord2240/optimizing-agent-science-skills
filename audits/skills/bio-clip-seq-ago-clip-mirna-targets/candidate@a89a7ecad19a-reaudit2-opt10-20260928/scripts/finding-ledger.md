# Finding ledger

## Closed findings

### AGO-004 — P0 — Workflow-level direct-target determinism

**Disposition: closed on this exact candidate identity.** Two fresh wrapper workflows, each executing two clean single-thread Hyb replicates on the same pinned commit, official reads, hOH7 database, and fixed process controls, produced the same four raw Hyb outputs, 111 accepted sites, 111 targets, 111 per-read support records, empty exclusions, and identical structured manifests. All 25 non-stdout files per workflow matched byte-for-byte. Each stdout log differs only in its first wall-clock timestamp line; lines after that timestamp match. This stdout timestamp variance remains an explicit reproducibility limitation and is not reported as full-log byte identity.

### AGO-005 — P1 — Targeted-Yeo UMI length contract

**Disposition: closed locally; upstream protocol ambiguity remains disclosed.** The candidate no longer asserts a fixed targeted-route UMI length. It requires an explicit protocol-declared integer and provenance, binds those values to a manifest, and fails closed when required declaration fields are absent or invalid. Independent 9-nt and 10-nt fixtures produced the exact requested R2 prefixes; six missing/invalid/short-input cases emitted no outputs. The pinned upstream CWL prose (9 nt) and executable default (10 nt) remain discrepant, so the correct biological length still comes from each library protocol.

## Open finding

### AGO-009 — P0 — Non-finite expression bypasses the expression threshold

**Evidence:** `evidence/expression-nan-check.json`; saved reproduction is `scripts/expression_finite_check.py`. The input was two identical valid 16-column Hyb rows plus a matched expression row with value `NaN`, unit `TPM`, source `matched-small-RNA`, and required threshold `100`. The parser returned zero, wrote a complete manifest with one accepted row, and emitted `nan` in `sites.tsv`.

**Cause:** `consensus_hyb.py` calls `float()` on the string, which accepts NaN, and compares `expr[0] < threshold`; for NaN this expression is false, so the row passes the below-threshold exclusion.

**Required disposition:** reject non-finite measurements (at minimum NaN and positive/negative infinity) with the source line and field in the error; add regression fixtures and verify that invalid expression rows cannot produce an accepted target output. The exact candidate is rejected and is not candidate-ready.
