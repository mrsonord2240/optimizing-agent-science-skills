# Fix log — bio-crispr-screens-mageck-analysis (2026-09-16)

Worktree: `F:\OpenScience\wt\crispr-a`, branch `fix/r2-crispr-a`. Verified against MAGeCK 0.5.9.5
(`F:\OpenScience\audit-envs\crispr-screen-analyst\`) and MAGeCKFlute 1.99.2001 (R 4.4.3 / Bioc 3.20).

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| MLE permutation-FDR undocumented-sensitive to `--permutation-round`/covariates | P1 | Added a quantified "Permutation-Round Sensitivity" note to the MLE section, a matching Quantitative Thresholds row, and `--permutation-round 10` to the worked MLE example, citing `--permutation-round`'s own default (2) vs `--help`'s suggested value (10) | ran — real HAP1 TKOv3 T0-vs-T18 counts (1500-gene/5880-sgRNA random subset, `design_real.txt`: baseline+treatment), `mageck mle --permutation-round {1,2,5}` | see exact numbers below; rounds 10/20 not run (see note) |
| MAGeCKFlute `FluteRRA` example fails as documented | P1 | Added `proj=` argument + `dir.create()` of `outdir/MAGeCKFlute_<proj>/` to both `FluteRRA`/`FluteMLE` examples; added a Common Errors row naming the remaining `undefined columns selected` error as a known MAGeCKFlute-build compatibility gap | ran — real `input1_canonical.gene_summary/sgrna_summary.txt` (Input 1's actual mageck test output) via `r.sh`; directory-creation step now succeeds, reproduces the same `OmitCommonEssential` column error the audit found | fix resolves the directory bug; the deeper column error is a real MAGeCKFlute 1.99.2001 (unreleased GitHub HEAD) incompatibility, documented rather than patched (upstream package, not this Skill's code) |
| No platform caveat/fallback for `mageck-vispr` | P1 | Added a platform note above the VISPR command block: Linux/Mac-only, points to `[[screen-qc]]` as the Windows-compatible fallback | checked against `TOOLS.md` (confirmed absent: `ModuleNotFoundError`, no PyPI/Windows build) and the audit's own Input-6 finding | no code to run — a doc fix |
| `volcano()` Python snippet missing `import pandas as pd` | P2 | Added the import | ran — against real `input1_canonical.gene_summary.txt`, produces `volcano_fixed_test.png` | |
| "Every gene appears significant" overstates the heavy-selection symptom | P2 | Rephrased in both the RRA algorithm section and the Failure Modes entry to cover both manifestations (universal significance, or asymmetric recall collapse) with the audit's real numbers (100%/0% -> 100%/100% recall by direction) | numbers taken from the audit's own Input 3 run (independently reproducible, not rerun this pass — the audit's `run/` data is read-only) | |
| No explicit anti-fabrication instruction | P2 | Added one line after the tool-overview bullets: never report FDR/LFC/beta without having actually run mageck on the user's data | doc-only, matches brief's suggested wording | |

## Permutation-round quantification (top P1)

Real data: HAP1 TKOv3 T0-vs-T18 triplicate counts (`HAP1_TKOv3_reads.txt`, the same file Input 1 of
the audit used), a random 1500-gene / 5880-sgRNA subset. Full 18,056-gene genome-scale MLE is a
multi-hour job per `TOOLS.md` note #7 -- confirmed directly: a full-genome `--permutation-round 1`
run was still mid-first-permutation-thread after several minutes and was stopped in favor of a
real-data subset sized for a same-session sweep. Design: `baseline` (all 1) + `treatment` (0 for T0,
1 for T18A/B/C) -- the same two-condition comparison Input 1 ran via RRA, run here via MLE
specifically to stress the permutation-FDR column.

`mageck mle --count-table HAP1_subset1500.txt --design-matrix design_real.txt --norm-method median
--permutation-round {R}` for R in 1, 2, 5. Results (genes with `treatment|fdr < 0.05`):

| `--permutation-round` | genes FDR<0.05 | genes `wald-fdr`<0.05 | flips vs pr=2 (default) |
|---|---|---|---|
| 1 | 49 | 108 | 5 |
| 2 (tool default) | 48 | 108 | -- |
| 5 | 67 | 108 | 19 (40% of pr=2's hit count) |

`wald-fdr` is exactly stable (108) across all three rounds, as expected (it's asymptotic, not
permutation-derived). The permutation `fdr` column is not: going from the tool's own default (2) to
5 -- still well short of `--help`'s suggested 10 -- moves the hit count by 40% and flips 19 individual
genes' significance calls. Rounds 10 and 20 were not run: per the coordinator's direction, the
already-observed 2-vs-5 spread is a sufficient, defensible real-data measurement of the effect, and
running higher rounds at even a 1500-gene subset was consuming disproportionate wall-clock for a
documentation fix (each round scales roughly linearly with permutation count and 4 sgRNA-per-gene
group sizes). These three data points are enough to show the direction and rough magnitude of the
effect; SKILL.md's new note states the 2-vs-5 numbers and the general rule (cross-check `wald-fdr`,
prefer `--permutation-round >= 10` for boundary calls) rather than implying a fully-characterized
curve.

## Unfixed

Nothing left open from the report's `recommendations[]` (3 P1 + 3 P2, all six addressed above).
`--permutation-round` 10 and 20 were not empirically run (time-boxed, see above) -- the SKILL.md fix
states the 1/2/5 real-data numbers and cites `--help`'s own suggested value of 10 rather than a
directly-measured number at that round count.

## Final pass — 2026-09-24 (`d2134ad0c94f2e442d6c21f81f51b00db4ca15e1`)

| finding | priority | change | verified |
|---|---|---|---|
| Paired samples were incorrectly routed away from RRA | P1 | The decision table now selects `mageck test --paired` for a pure two-condition matched design and reserves MLE for pairing combined with additional factors. | Fresh deterministic four-donor paired fixture: `mageck test --paired` recovered 6/6 planted hits. |
| FluteMLE used the implicit `baseline` intercept as `ctrlname` | P1 | The example uses emitted `day7`/`day21` conditions and states that `baseline` is not an output condition; the Common Errors table gives the recovery path. | Final-pass static assertion checked the literal example and the archived MLE scenario was rerun at permutation-round 10. |
| Default MLE permutation FDR was presented as more reproducible and general than warranted | P1 | The guidance now states that identical default-round reruns can move boundary calls, requires an explicit higher round count for reported results, and labels prior flip counts illustrative rather than universal. | Two fresh round-10 time-course runs recovered all 20 planted hits with matching beta signs; a fresh independently sampled HAP1 subset completed at rounds 2 and 5. |
| Historical MAGeCKFlute development-build column error had no specific release-build recovery | P2 | Version Compatibility now identifies the historical 1.99.2001 development-build boundary and directs users to retain MAGeCK outputs and retry visualization with a released compatible build. | The final pass preserves this as an external compatibility condition rather than misreporting it as a hit-calling failure. |

Final-pass harness: `F:\OpenScience\audits\_final_pass\bio-crispr-screens-mageck-analysis\run\final_pass_verify.py`.
It reran all seven archived scenario classes and two fresh fixtures: **32/32 assertions passed**.
