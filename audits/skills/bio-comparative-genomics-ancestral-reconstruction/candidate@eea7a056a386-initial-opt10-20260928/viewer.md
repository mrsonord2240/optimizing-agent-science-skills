> **Audit record for `bio-comparative-genomics-ancestral-reconstruction`**
> - Audited working candidate `eea7a056a3861ff085037d0d5ae9ea566c602c831524f6a517acb6fc77b341d6`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/comparative-genomics/ancestral-reconstruction), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-comparative-genomics-ancestral-reconstruction

Generated: 2026-09-28  
Candidate: `sha256-manifest-v1:eea7a056a3861ff085037d0d5ae9ea566c602c831524f6a517acb6fc77b341d6`  
Category / mode / complexity: Data Analysis / D / Complex

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|---|
| 1 | Canonical | 17 | 19 | 36 | 1/4 | ❌ |
| 2 | Variant A | 38 | 55 | 93 | 4/4 | ✅ |
| 3 | Edge | 34 | 50 | 84 | 4/4 | ✅ |
| 4 | Variant B | 14 | 17 | 31 | 1/4 | ❌ |
| 5 | Stress | 6 | 8 | 14 | 1/4 | ❌ |
| 6 | Scope Boundary | 12 | 14 | 26 | 1/4 | ❌ |
| 7 | Adversarial | 25 | 30 | 55 | 3/4 | ⚠️ |

**Static Score:** 65 / 100  
**Execution Average:** 48.4 / 100  
**Assertion Pass Rate:** 15 / 28  
**Weighted Score:** 55 / 100  
**Verdict:** Reject; deployable `false`; both veto gates fail.

## Veto Gates

### Skill Veto — FAIL

- T1 Operational stability: **FAIL** — three central advertised runtime routes fail on current provider outputs/interfaces, and malformed or empty results are unsafe.
- T2 Structural contract: **FAIL** — parsers silently return empty/NaN outputs and the GRASP wrapper promises filenames the provider does not emit.
- T3 Result determinism: **FAIL** — the stochastic mapping script has no seed argument or internal seed management despite producing 1,000 random histories.
- T4 Security: **PASS** — no raw eval, credentials, destructive operations, or access-control bypass was found.

### Research Veto — FAIL

- M1 Scientific integrity: **PASS** — no fabricated study results, statistics, or identifiers were observed.
- M2 Practice boundaries: **PASS** — outputs remain comparative-genomics analysis and do not cross clinical practice boundaries.
- M3 Methodological ground: **FAIL** — the continuous script does not reconstruct under selected EB/lambda/kappa/delta fits, and OU estimates are over-interpreted relative to current OUwie documentation.
- M4 Code usability: **FAIL** — PAML parsing, GRASP, OUwie, and malformed/empty posterior routes fail or silently produce unusable outputs.

## Detailed Outputs

### Input 1 — Canonical: PAML protein ASR and shipped parsers

**Prompt:** Reconstruct the public eight-taxon cytochrome-c ancestor with the packaged PAML workflow and return ancestral sequences plus per-site posterior confidence.

**Output:** Both packaged control writers execute PAML 4.10.10 successfully on the retained 110-column alignment. Each run writes a nonempty `rst` and `mlc`; PAML reports marginal reconstruction at seven internal nodes. Nevertheless, `parse_rst_ancestors` returns `{}`, `extract_site_probabilities` returns `[]`, and `parse_rst_posteriors` returns zero nodes. The real current output is matrix-oriented and contains none of the block headers assumed by the parsers.

**Scores:** Basic 17/40 | Specialized 19/60 | Total 36/100

**Assertions:**

- PASS — Both control writers produce valid provider runs and artifacts.
- FAIL — The provider sequence parser recovers no ancestor.
- FAIL — The provider posterior parser recovers no site probability.
- FAIL — The extracted parser recovers no node posterior.

Evidence: `evidence/paml-surfaces.json`, `evidence/paml-provider-rst.txt`, `evidence/paml-extracted-rst.txt`.

### Input 2 — Variant A: IQ-TREE marginal protein ASR

**Prompt:** Run the packaged IQ-TREE ancestral workflow on the same rooted protein alignment and validate every posterior row.

**Output:** IQ-TREE 2.4.0 completes. The `.state` table contains 660 rows, 6 internal nodes, 110 sites, and 20 posterior columns. All probabilities are finite, each row sum differs from one by at most `3e-5`, reported states match posterior argmax, and regrouping through the packaged parser preserves all rows.

**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100

**Assertions:** 4/4 PASS.

Evidence: `evidence/iqtree-output-validation.txt`.

### Input 3 — Edge: stochastic mapping and hidden rates

**Prompt:** Fit ER, SYM, and ARD to a deterministic 30-tip binary trait fixture, run 1,000 stochastic maps, and fit the packaged corHMM hidden-rate comparison.

**Output:** The exact script selects ARD by AIC, creates 1,000 stochastic maps, returns 59 stochastic-summary rows and 29 corHMM marginal node rows, and completes with installed corHMM 2.8. The audit harness fixes seed 20260928; the candidate script itself has no seed interface.

**Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100

**Assertions:** 4/4 PASS for the declared matched fixture.

Evidence: `evidence/r-surfaces.log`.

### Input 4 — Variant B: continuous-trait models and OU

**Prompt:** Compare BM, OU, EB, lambda, kappa, and delta on a 35-tip continuous-trait fixture and reconstruct under the selected model, including the OU route.

**Output:** All six AIC values, lambda, and K are finite and BM wins the retained fixture. The BM `fastAnc` branch returns 34 ancestors. A direct OUwie 3.0.3 probe shows that the candidate's `OUwie.anc(fit, data=df)` call is rejected because `data` is unused, while a current `OUwie.anc(fit, knowledge=TRUE)` control completes. For EB/lambda/kappa/delta winners, the candidate never applies the winning fit and instead runs `contMap` on the original tree. Current OUwie documentation also says `OUwie.anc` has no uncertainty and is intended mainly for visualization and model intuition.

**Scores:** Basic 14/40 | Specialized 17/60 | Total 31/100

**Assertions:** 1/4 PASS.

Evidence: `evidence/r-surfaces.log`, `evidence/ouwie-probe.log`, `scientific-source-notes.md`.

### Input 5 — Stress: current official GRASP CLI

**Prompt:** Run the packaged GRASP shell against the current official 2024 command-line JAR and validate all promised output artifacts.

**Output:** A valid official-interface control emits seven 110-column ancestor sequences, an eight-tip labeled tree, and nonempty ASR JSON. The exact candidate shell exits 5 because the current CLI rejects `-aln`; the remaining command and promised output names also differ from current help.

**Scores:** Basic 6/40 | Specialized 8/60 | Total 14/100

**Assertions:** 1/4 PASS.

Evidence: `evidence/grasp-candidate-current.log`, `evidence/grasp-current-validation.txt`, `evidence/grasp-current-outputs.tsv`.

### Input 6 — Scope Boundary: empty and malformed posterior contracts

**Prompt:** Exercise the packaged summary on an empty PAML probability set and parse an IQ-TREE state table that lacks all posterior columns.

**Output:** A valid miniature IQ-TREE fixture returns maximum posteriors 0.97 and 0.70. An empty PAML probability list yields a short `quality=unknown` object that the packaged summarizer dereferences as if populated, raising `KeyError: total_sites`. An IQ-TREE table with no `p_*` columns is accepted and assigned `NaN` maximum posterior rather than rejected.

**Scores:** Basic 12/40 | Specialized 14/60 | Total 26/100

**Assertions:** 1/4 PASS.

Evidence: `evidence/python-surfaces.json`.

### Input 7 — Adversarial: taxon and outgroup mismatch

**Prompt:** Supply an absent IQ-TREE outgroup and a discrete-trait table missing one tree taxon; ensure both are rejected before any reconstruction is accepted.

**Output:** The IQ-TREE negative control exits 2 and no output is accepted. The missing-trait-row case also stops before an accepted map result, but exposes only `subscript out of bounds`, with no taxon name or recovery guidance.

**Scores:** Basic 25/40 | Specialized 30/60 | Total 55/100

**Assertions:** 3/4 PASS.

Evidence: `evidence/r-surfaces.log` and the prepared negative-control log referenced by `TOOLS.md`.

## Ordered Findings

1. **P0 TOOL-ASR-001** — Both PAML parsers are incompatible with current real `rst` output.
2. **P0 TOOL-ASR-002** — The GRASP command and artifact contract are stale.
3. **P0 TOOL-ASR-003** — The OUwie reconstruction branch uses a stale interface and overstates its interpretability.
4. **P0 ASR-007** — Non-BM winners are not actually used for reconstruction.
5. **P1 TOOL-ASR-004** — Empty posterior summaries crash.
6. **P1 TOOL-ASR-005** — Missing IQ-TREE posterior columns are accepted as NaN.
7. **P1 ASR-008** — Stochastic seed and taxon contracts are missing.
8. **P1 ASR-009** — Routed reconciliation language makes categorical model claims.
9. **P2 TOOL-ASR-006** — The corHMM `2.9+` range is unpinned and untested across the CRAN/GitHub split.

The machine-readable report and exact fixes are in `report.json`; the single ordered fixer queue is in `finding-ledger.md`.
