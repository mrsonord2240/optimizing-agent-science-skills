# Execution ledger — independent final re-audit

## New executions

Commands ran in the `science` WSL distro through `tools/wsl_isolated_exec.sh`, with unprivileged user `sci`, `WSL_INTEROP` unset, and `/mnt/f` not mounted. Current runtime probe: Python 3.12.14, PAML 4.10.10 (reported by CODeml), IQ-TREE 2.4.0, OpenJDK 21.0.10, R 4.4.3, ape 5.8.1, phytools 2.5.2, geiger 2.0.12, corHMM 2.8, OUwie 3.0.3. The explicit environment lock SHA-256 is `216277a7a3841fb84bd731034fbfe09ca28a7514289e9bc15c8a8d92e6f4856c`.

| Surface | Invocation/evidence | Inspected result |
|---|---|---|
| PAML unit and real-fixture tests | Candidate `tests/test_paml_rst.py`; [`paml-focused.log`](evidence/paml-focused.log) | 4/4 unit tests. Fresh codon plus both protein `rst` fixtures each returned 7 × 110 records and all values matched raw source rows. |
| CODeml codon writer/parser | [`run_codon_paml.py`](run_codon_paml.py); [`real-codon-paml/result.json`](evidence/real-codon-paml/result.json) | PAML 4.10.10 exit 0; 179,979-byte `rst`; 770 codon/AA records; bounds and codon/AA marginal relationship checked. |
| Provider CODeml protein writer/parser | [`run_protein_paml.py`](run_protein_paml.py); [`real-protein-paml/provider/result.json`](evidence/real-protein-paml/provider/result.json) | PAML 4.10.10 exit 0; 7 × 110; 770 source-row-matched posterior records. |
| Extracted CODeml protein writer/parser | Same script; [`real-protein-paml/extracted/result.json`](evidence/real-protein-paml/extracted/result.json) | PAML 4.10.10 exit 0; 7 × 110; 770 source-row-matched posterior records. |
| corHMM claim-family regression search | [`corhmm-claim-search.log`](evidence/corhmm-claim-search.log) | Full Skill tree scanned; no unconditional corHMM superiority or mandatory hidden-rate claim remains. The sole “mandatory” match is explicitly negated and conditional. |
| Candidate identity and worktree | [`candidate-manifest-before.tsv`](candidate-manifest-before.tsv), [`candidate-manifest-after.tsv`](candidate-manifest-after.tsv) | Both identities equal the expected SHA-256; 17 files, 1,628-byte manifest. Candidate worktree contains the expected untracked Skill subtree only; no cache artifacts. |

## Reused immutable evidence

Reuse validation is [`reuse-validation.json`](evidence/reuse-validation.json). Current candidate files match the focused-fix manifest exactly. The pinned environment lock and live version probe match recorded tooling. The reused tests' interfaces, fixtures, and assumptions remain unchanged.

| Surface | Evidence reused | Relevant current files |
|---|---|---|
| IQ-TREE real ASR and strict `.state` parser | `../fix-opt11-20260928/evidence/iqtree-results.json`; `../fix-opt11-20260928/evidence/iqtree-run/asr_iqtree.state` | `scripts/iqtree_ancestral.sh`, `scripts/iqtree_state.py` |
| GRASP official CLI and shipped wrapper | `../fix-opt11-20260928/evidence/grasp-validation.txt`; `../fix-opt11-20260928/evidence/grasp-candidate-wrapper.log` and output artifacts | `scripts/grasp_asr.sh` |
| Discrete trait, stochastic mapping, corHMM | `../fix-opt11-20260928/scripts/retest_r.R`; `../fix-opt11-20260928/evidence/r-sessionInfo.txt` | `scripts/stochastic_mapping.R` |
| Continuous BM/OUwie and transformed-model refusals | Same R regression and session record | `scripts/continuous_trait_asr.R` |
| No-data summary and parser boundaries | `../fix-opt11-20260928/evidence/python-results.json`; fresh no-data unit check in `evidence/paml-focused.log` | `scripts/ancestral_reconstruction.py`; `scripts/paml_rst.py` |

These workflows represent the required materially distinct executable families. Optional documentation-only methods are not counted as executed support. Before asserting executable support for FastML, RevBayes, BayesTraits, MrBayes, BEAST2, RPANDA, or the GRASP web service, run their current supported interface on a bounded representative dataset and inspect their actual ancestral-state/posterior output; the GRASP CLI was executed and validated separately.

No environment widening, package installation, candidate repair, or candidate write occurred. The only failed command was an initial redundant environment probe that tested directory existence rather than mountpoint status; it stopped before any version checks. The corrected probe passed and is recorded in `evidence/runtime-boundary.log`.
