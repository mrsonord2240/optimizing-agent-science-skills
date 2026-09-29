# Ordered finding ledger

Audit identity: `sha256-manifest-v1:eea7a056a3861ff085037d0d5ae9ea566c602c831524f6a517acb6fc77b341d6` (15 files; 1,441-byte manifest).

| Order | ID | Priority | State | Evidence | Required disposition |
|---:|---|---|---|---|---|
| 1 | TOOL-ASR-001 | P0 | open | Inputs 1 and 6; `evidence/paml-surfaces.json`; both retained real `rst` files | Replace both parsers with format-tested parsing of current PAML marginal output; fail closed on zero nodes/sites and regression-test real protein and codon outputs. |
| 2 | TOOL-ASR-002 | P0 | open | Input 5; `evidence/grasp-candidate-current.log`; `evidence/grasp-current-validation.txt` | Update the command to the official 2024 CLI and validate the actual emitted artifacts before reporting success. |
| 3 | TOOL-ASR-003 | P0 | open | Input 4; `evidence/ouwie-probe.log`; OUwie 3.0.3 reference manual | Use the fitted-object-only current call with explicit `knowledge=TRUE`, preserve the provider's strong interpretation warning, and do not promise absent uncertainty. |
| 4 | ASR-007 | P0 | open | Input 4; `scripts/continuous_trait_asr.R`; `scientific-source-notes.md` | Apply the selected model's fitted transformation/reconstruction correctly or stop with a supported-method message; do not label original-tree `fastAnc` output as EB/lambda/kappa/delta reconstruction. |
| 5 | TOOL-ASR-004 | P1 | open | Input 6; `evidence/python-surfaces.json` | Make empty/no-result summaries total and explicit; never dereference absent metrics and never present unknown quality as a completed reconstruction. |
| 6 | TOOL-ASR-005 | P1 | open | Inputs 2 and 6; official IQ-TREE `.state` contract; `evidence/python-surfaces.json` | Require identifiers plus at least one finite `p_X` column, validate posterior ranges/sums and state argmax, and reject malformed or empty tables. |
| 7 | ASR-008 | P1 | open | Inputs 3 and 7; `scripts/stochastic_mapping.R`; `evidence/r-surfaces.log` | Add explicit taxon/state validation and a caller-visible seed contract; replace raw subscript errors with stable actionable failures. |
| 8 | ASR-009 | P1 | open | Static source review; OUwie manual; `references/reporting-and-troubleshooting.md` | Replace categorical “correct/trust” statements with model-adequacy and sensitivity language; distinguish exploratory ancestral estimates from data and report uncertainty limitations. |
| 9 | TOOL-ASR-006 | P2 | open | `evidence/r-package-versions.tsv`; CRAN corHMM page; GitHub DESCRIPTION/API | Replace `corHMM 2.9+` with a tested source/version matrix and pin the installation source; test every advertised range rather than inferring it from 2.8. |

No audit-local repair was attempted. Every item changes a scientific method, interface, output contract, validation boundary, or version/provenance judgment and is outside the minor-repair budget.
