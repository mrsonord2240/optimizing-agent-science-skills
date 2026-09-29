# Finding ledger — independent final re-audit

Candidate: `sha256-manifest-v1:a9eb2d1e1c3ac7f89d63f11deb7a436c14ab0c78a6469911812aa510eeb93e07` (17 files).

All inherited findings were independently reconsidered. No new issue was found. The two latest findings were directly retested; the other executable workflows were reused only after checking their exact candidate file hashes, environment lock/runtime, interfaces, and fixture assumptions.

| ID | Severity | Final disposition | Evidence |
|---|---|---|---|
| TOOL-ASR-001 | P0 | Fixed and independently passed for codon plus both protein `rst` routes. | `evidence/paml-focused.log`; `evidence/protein-paml-focused.log`; fresh run outputs under `evidence/real-codon-paml/` and `evidence/real-protein-paml/`. |
| TOOL-ASR-002 | P1 | Fixed; current official GRASP CLI and candidate wrapper outputs remain valid. | `../fix-opt11-20260928/evidence/grasp-validation.txt`; `grasp-candidate-wrapper.log`; current `scripts/grasp_asr.sh` hash matches the fixed manifest. |
| TOOL-ASR-003 | P1 | Fixed with an explicit OUwie fitted-object route; output is exploratory and has no uncertainty. | `../fix-opt11-20260928/scripts/retest_r.R`; `../fix-opt11-20260928/evidence/r-sessionInfo.txt`; current continuous script hash matches the fixed manifest. |
| TOOL-ASR-004 | P1 | Fixed; no-data summaries remain explicit and complete. | Four fresh unit tests in `evidence/paml-focused.log`; identity-matched `../fix-opt11-20260928/evidence/python-results.json`. |
| TOOL-ASR-005 | P1 | Fixed; real IQ-TREE states validate and incomplete/malformed tables reject. | `../fix-opt11-20260928/evidence/iqtree-results.json`; current IQ-TREE parser and wrapper hashes match the fixed manifest. |
| TOOL-ASR-006 | P2 | Fixed boundary: CRAN corHMM 2.8 is the tested route; GitHub 2.10.5 remains explicitly unsupported. | `../fix-opt11-20260928/evidence/r-sessionInfo.txt`; `../tooling-delta-opt10-20260928/environment-fingerprint.json`; full-tree claim search. |
| ASR-007 | P1 | Fixed; EB, lambda, kappa, and delta winners refuse to substitute original-tree BM output. | `../fix-opt11-20260928/scripts/retest_r.R`; `../fix-opt11-20260928/evidence/r-sessionInfo.txt`. |
| ASR-008 | P1 | Fixed; explicit stochastic seed, map count, and taxon reconciliation remain intact. | `../fix-opt11-20260928/scripts/retest_r.R`; `../fix-opt11-20260928/evidence/r-sessionInfo.txt`. |
| ASR-009 | P1 | Fixed; comparison guidance is scenario-qualified. | Complete static review and `evidence/corhmm-claim-search.log`. |
| ASR-010 | P1 | Fixed; real fixture checks derive every expectation from its own source `rst`, avoiding run-specific hardcoded posteriors. | Fresh 7 × 110 route checks in both PAML logs; `tests/test_paml_rst.py` in the exact candidate. |
| ASR-011 | P2 | Fixed; usage guide and connected method-selection wording are conditional; no unconditional corHMM superiority/mandatory claim remains. | Full-tree `rg` evidence in `evidence/corhmm-claim-search.log`. |

Open findings: none. Candidate readiness: pass for the exact identity above; downstream commit/intake remains the orchestrator's next phase.
