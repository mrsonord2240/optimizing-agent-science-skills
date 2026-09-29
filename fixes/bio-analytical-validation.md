# Fix log: bio-analytical-validation

- Fixed: 2026-09-28T12:08:39.8231912-07:00.
- Assignment: lane 1 `fix-scientific-skill` only.
- Baseline: `optimize/ten-20260928-lane1-analytical` at `0bc0b31fc52742dbec1034f698103434cc9460c3`; candidate subtree `b5a701c41d3afe697766a02a11b2954e12ff9d42`.
- Accepted audit: `F:\OpenScience\audits\bio-analytical-validation\initial-opt10-20260928\report.json`, SHA-256 `ac0d305985c88a1780aff8a96ce944846095179dff475bde454203926ab4ffc5`.
- Fixed candidate: manifest SHA-256 `bd66239b9133b70a7522d0d99e3bc4ebbed1b8c1291c74fad26367dfa339b2ab`; exact file identities in `F:\OpenScience\audits\bio-analytical-validation\fix-opt10-20260928\candidate-manifest.json`.

| Order | ID | Priority | State | Implementing change | Verification |
|---:|---|---:|---|---|---|
| 1 | `ADV-001` | P0 | fixed | Replaced assay-looking panel APIs with `sampling_only_*` and `theoretical_sampling_vaf95_lower_bound`; structured threshold output includes equal-VAF, independence, perfect-recovery/detection, and no-background/calling assumptions plus the explicit `not an achieved assay LoD95` interpretation. Updated every instruction and CLI boundary. | `regression-evidence.md`: legacy names absent; 16- and 48-locus bounds are monotone and carry the four assumptions; both relevant CLIs print the boundary. |
| 2 | `ADV-002` | P1 | fixed | Added finite numeric, physical range, dimensionality, equal-length, binary-outcome, minimum-level, per-level replicate, positive-integer, k-of-N, grid, and target-probability validation with stable `ValueError` messages. | `focused_regressions.py`: 11 invalid probes pass with exact actionable message fragments; all normal entry points exit 0. |
| 3 | `ADV-003` | P1 | fixed | Replaced the one-observation separated demo with five levels x 40 replicates that bracket 95%; separated/unidentified, non-converged, and nonpositive-slope fits now fail; result includes LoD95, delta-method Wald CI, slope, convergence, deviance, Pearson chi-square, residual df, level rates, and replicate diagnostics. | Warning-free demo: LoD95 0.003725, 95% CI [0.002578, 0.005383], slope 2.746, n=200. Fully separated replicated series is rejected with the documented stable error. |
| 4 | `ADV-004` | P1 | fixed | `simulate_dilution_series` now documents and uses a calibrated probit teaching model whose `true_lod_vaf` is exactly its theoretical 95% point; removed the unrelated `input_ng` argument. | Same seed and levels: changing 1e-3 to 5e-3 changed 211/600 outcomes (541 vs 378 positives); exact rerun is identical. |
| 5 | `ADV-005` | P2 | fixed | Default conversion is now 303.030303 GE/ng from 1,000 pg / 3.3 pg, with explicit `ge_per_ng` override. Documentation separates HCC1395 CRL-2324 / HCC1395BL CRL-2325 call set v1.2 / SRP162370 from ten-cell-line SEQC2 Sample A, Agilent Sample B 5190-8848, and A/B-derived fragmented Df/Ef/Ff / PRJNA677999 materials. | Regression confirms 3.3 ng = 1,000 GE and override behavior; source identifiers and DOIs are present in `SKILL.md` and `usage-guide.md`. |

## Changed candidate files

- `SKILL.md`
- `usage-guide.md`
- `scripts/ge_and_poisson.py`
- `scripts/lod95_probit.py`
- `scripts/panel_integrated_lod.py`
- `examples/detection_limits.py`

## Evidence

- Harness: `F:\OpenScience\audits\bio-analytical-validation\fix-opt10-20260928\focused_regressions.py`.
- Execution and scientific-value checks: `F:\OpenScience\audits\bio-analytical-validation\fix-opt10-20260928\regression-evidence.md`.
- Candidate identity: `F:\OpenScience\audits\bio-analytical-validation\fix-opt10-20260928\candidate-manifest.json`.
- Pinned environment: CPython 3.12.14, NumPy 1.26.4, SciPy 1.12.0, statsmodels 0.14.6. No dependency or version changed.

## Tooling impact and transition

- Impact: **changed**.
- Candidate runnable surfaces changed: all four Python entry points above.
- Prepared harness surface affected: `F:\OpenScience\audit-envs\bio-analytical-validation\smoke_test.py` uses removed names, assumes scalar probit output, and passes the retired simulation argument.
- Prepared documentation affected: `F:\OpenScience\audit-envs\bio-analytical-validation\TOOLS.md` contains obsolete values and the now-resolved separated-demo caveat.
- Next role at fix completion: `prepare-scientific-skill-tooling` in delta mode, then independent `reaudit-scientific-skill`.
- No product commit, push, publication, remote mutation, Marketplace action, readiness score, or self-certification was performed by the fixer.

## Independent final result

- Final candidate audit: `audits/skills/bio-analytical-validation/candidate@bd66239b9133-reaudit-opt10-20260928`.
- Result: **96/100, Production Ready**; **25/25 assertions pass**; both vetoes pass; no open P0 or required recommendation.
- The provider binding record is the canonical proof that committed shelf bytes match the independently audited candidate.
