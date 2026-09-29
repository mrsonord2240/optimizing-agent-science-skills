# Finding ledger — independent re-audit

| ID | Initial disposition | Fresh adjudication | Evidence |
|---|---|---|---|
| TOOL-ASR-001 | Claimed fixed; initial test had no prepared real codon rst fixture | **REOPENED P0.** Protein parser routes pass; real PAML 4.10.10 codon `rst` parser raises `ValueError: PAML rst contains no marginal site rows`. | `evidence/paml-codon-results.json`; `evidence/codon-paml/rst`; `retest_codon_paml.py` |
| TOOL-ASR-002 | Fixed current GRASP argument/output contract | **PASS.** Current official JAR and candidate wrapper complete; 7 × 110 ancestor sequence, 8 tree tips, four JSON fields validated. | `evidence/grasp-current/`; `evidence/grasp-candidate-conda/` |
| TOOL-ASR-003 | Fixed fitted-object OUwie call, exploratory only | **PASS WITH DOCUMENTED LIMIT.** Real OUwie 3.0.3 fitted-object `OUwie.anc` call returned 29 points; no uncertainty is provided. Default single-regime `check.identify` diagnostic was reproduced and disclosed. | `retest_r.R`; `evidence/r-sessionInfo.txt`; `evidence/r-run/` |
| TOOL-ASR-004 | Fixed empty result handling | **PASS.** Empty input returns `no_data`, zero counts, null summary, unknown quality. | `evidence/python-results.json` |
| TOOL-ASR-005 | Fixed strict IQ-TREE parser | **PASS.** Real 660-row current output and malformed-column/empty/bad-sum/bad-argmax/NaN cases validated. | `evidence/python-results.json`; `evidence/iqtree-run/` |
| TOOL-ASR-006 | Source/version gap addressed | **PASS.** CRAN corHMM 2.8 marked tested; GitHub 2.10.5 remains explicitly untested and unsupported. | `evidence/TOOLS.md`; `evidence/tooling-delta-reference/` |
| ASR-007 | Refusal for transformed models | **PASS.** EB, lambda, kappa, delta winners each refuse output instead of substituting original-tree reconstruction. | `retest_r.R`; R run record summarized in `evidence/r-results.md` |
| ASR-008 | Seed/taxon reconciliation | **PASS.** Explicit seed required; 1,000 maps and posterior rows returned; missing taxa rejected with names/action. | `retest_r.R`; `evidence/r-results.md`; `evidence/r-run/` |
| ASR-009 | Rewritten as scenario matrix | **REMAINS OPEN P1 (residual wording).** Matrix is qualified, but usage guide still says corHMM “supersedes simpler Mk approaches” and is the “modern standard,” without conditions. | Candidate `usage-guide.md`; `viewer.md` |

## New finding

The codon parser defect is not an environment failure. Real PAML 4.10.10 codeml exited successfully with a complete marginal `rst`; only the candidate parser failed. The synthetic synonym-codon fixture was chosen to isolate PAML output-format compatibility from biological coding-sequence validity. A biologically sourced codon fixture remains desirable but is not required to establish this parser failure.
