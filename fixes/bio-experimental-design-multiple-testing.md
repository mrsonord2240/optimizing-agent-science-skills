# bio-experimental-design-multiple-testing — 2026-09-18

Worktree: `F:\OpenScience\wt\ed-mtc`, branch `fix/ed-mtc`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| IHW has no failure-mode coverage; canonical `ihw(pvalue ~ mean_expression, data = de_table, alpha = 0.05)` segfaults | P1 | Added "IHW segfaults or silently reduces to BH" to Per-Method Failure Modes (names `lp_solver = "lpsymphony"`, the `nbins <- floor(m/1500)` auto rule and its collapse-to-BH at `nbins==1`, the "more than 1000 p-values" guard, and a fallback to plain BH with the power cost quantified). Pinned `nbins = 5` in the SKILL.md code block and in `examples/multiple_testing_correction.R`. Rewrote the shipped example's IHW step to run `ihw()` in a retried child process (`system2(Rscript, ...)`) since a segfault is a process crash, not an R error `tryCatch` can catch. | ran | On the audit's own `synthetic_de_pvalues.csv` (m=18,000): 12 attempts across `nbins` 2/3/4/5 crashed 6/12 (50%) vs ~75% (3/4) at default `nbins`=12 — pinning `nbins` **reduces but does not eliminate** the crash, contradicting the stronger "nbins<=5 is stable" claim in the env's `TOOLS.md`; documented the weaker, correct claim instead. The child-process retry pattern was run twice end-to-end: once exhausted 3 retries and fell back to BH (exit 0, no crash), once succeeded with IHW (95 vs 93 discoveries, exit 0) — both paths verified crash-free. Extracted `IHW::ihw.default` source directly (`asNamespace("IHW")`) to confirm the exact `nbins` formula and the "Only 1 bin; IHW reduces to Benjamini Hochberg" / "more than 1000 p-values" messages verbatim, IHW 1.34.0. |
| q-value one-liner unreliable on small families; `qvalue(pvalues)` throws or gives bad pi0-hat below ~1000 tests | P1 | Added family-size floor + `lambda = 0` fallback to the FDR/q-value code block; added "q-value fails on small families" to Per-Method Failure Modes; noted `pi0.method='bootstrap'` in the Quantitative Thresholds/code | ran | Own simulation, 200 reps/size, qvalue 2.38.0: m=20 errored 77/200 (38.5%, audit reported 178/500=35.6%), m=50 errored 15/200 (7.5%, audit reported 35/500=7%) — independently reproduces the audit within sampling noise. `pi0.method='bootstrap'` does **not** fix it: same ~38%/7.5% failure rate on a *different* error (`missing values ... na.rm`), not the spline error — this is new information beyond the audit and beyond the finding's suggested fix, documented honestly rather than presenting bootstrap as a working fallback. `lambda=0` had 0/200 errors at both sizes and returned pi0=1.0 exactly (planted truth) every time. |
| BH-to-BY rule prescribes a large power loss on an undiagnosable symptom | P1 | Rewrote "Dependence" section, the BH-dependence failure mode, the Decision Tree row (split into "unknown/positive dependence -> BH" and "actually-expected negative dependence -> BY"), the Reconciliation row, the Algorithmic Taxonomy row, and the Common Errors index | ran | Own Python simulation (statsmodels `fdr_bh`/`fdr_by`, 400 reps x 3 structures, m=5000): mean FDP held at 0.045/0.045/0.046 across independent/positive-block(rho=0.8)/negative-pair (audit: 0.0444/0.0393/0.0453) — independently reproduces "BH's mean never fails." SD(FDP) rose 0.0127->0.0434 under positive-block (audit: 0.0114->0.0425); P(FDP>0.10) rose 0.000->0.120 (audit: 0.092). BY power 0.19-0.20 vs BH ~0.50 (a larger relative loss than the audit's 0.605->0.288/53%, same direction and order of magnitude) — cited the audit's more precise 1,200-replicate number in SKILL.md rather than my noisier 400-rep one, per the "re-derive at least one number yourself" bar. |
| FCR-adjusted intervals named four times ("Decision Tree", failure mode, Common Errors), shipped nowhere | P1 | Added new "False Coverage Rate — CIs on a Selected Set" section with a runnable `1 - alpha*R/m` (Benjamini-Yekutieli 2005) R code block; added the 2005 citation to References; pointed the failure-mode Fix line and Decision Tree row at the new section | ran | Own Python simulation (BH-selected set, m=5000/500 alt): naive coverage 42.9% -> FCR-adjusted 95.3%. Also ran the exact R block verbatim on a second synthetic set (m=2000): naive 50.0% -> FCR-adjusted 90.9%. Both independently confirm the formula's direction; cited the audit's 82.4%->97.6% in-text as the primary number since it used the audit's actual selected set. |

## Redundancy pass (every-pass rule, not audit-flagged)

`SKILL.md` internal duplication collapsed to one home, per the redundancy rule:

- **Common Errors** table restated every Per-Method Failure Mode's cause/solution in different words (5 rows, one-to-one with the failure-mode sections). Converted it to a symptom-only index that names the matching failure-mode heading instead of repeating cause/solution — nothing the agent needs was dropped, since every fact still lives in Per-Method Failure Modes.

`usage-guide.md` restated agent-actionable facts already owned by `SKILL.md`:

| Deleted from usage-guide.md | Already in SKILL.md |
|---|---|
| `## Tips` (6 bullets: FDR-vs-FWER default, BH/BY dependence rule, q-value pi0 power claim, IHW covariate independence, statsmodels default trap, filtering independence) | "The Single Most Important Modern Insight"; "Dependence — BH's Guarantee, BY's Cost"; "FDR — Benjamini-Hochberg and the q-value"; "Covariate-Weighted FDR — IHW"; Version Compatibility note + Python Equivalent; "Independent Filtering" |

Left the now-updated BH/BY framing in `## Tips` would have re-introduced the exact "realized FDR exceeds nominal" claim this pass just corrected in `SKILL.md` — one more reason to delete rather than edit-in-place per the rule's own rationale ("two copies drift"). `Prerequisites`, `Quick Start`, `Example Prompts`, `What the Agent Will Do`, and `Related Skills` are unique-to-humans / non-duplicative and were left as is.

## Findings fixed: 4/4 P1s. No P0s existed. One cheap P2 (shipped example's IHW step crashing on `m=10000`, part of the same crash family as the IHW P1) fixed as a side effect of the child-process retry pattern; the other two P2s (shipped example's misleading `rgamma` IHW covariate teaching a zero power gain, and taxonomy-only coverage of IDR/local FDR/independent filtering) were left unfixed — both require restructuring the shared synthetic data generator or new content beyond "extend the existing section," outside this pass's scope.

Nothing needs Sam. Flag for the re-auditor: this pass found the env's `TOOLS.md` claim "IHW... `nbins <= 5` is stable" to be too strong (50% crash rate at nbins 2-5 across 12 of my own trials, vs ~75% at default) — SKILL.md now states the weaker, verified claim (pin nbins, retry in a child process, fall back to BH) rather than the disproven "stable" framing.


---

# bio-experimental-design-multiple-testing — 2026-09-21

Worktree: `F:\OpenScience\wt\experimental-design-multiple-testing`, branch `fix/experimental-design-multiple-testing`. Source: latest re-audit (score 89, Production Ready; 1 open P1, 2 P2). Env: `mass-spec-proteomics-analyst\r.sh` (R 4.4.3, IHW 1.34.0, qvalue 2.38.0).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Bare `ihw()` one-liner is the primary IHW code block and crashes ~50% | P1 | Replaced the block with `ihw_safe()` (child-process `Rscript` via `system2`, `nbins = 5`, 3 tries, BH fallback returning `method`/`attempts`); states `de_table` has columns `pvalue`, `mean_expression`; the bare call is now only described as the thing not to run. IHW failure-mode Fix points at `ihw_safe()` instead of restating the pattern | ran | SKILL.md block extracted verbatim and run on the audit's 18k `de_pvalues_reaudit.csv`: run 1 IHW on attempt 2 (first child crashed, parent unaffected), 1018 vs BH 1006, realized FDP 0.040; run 2 all 3 children crashed, fell back to BH, 1006, parent exit 0. Forced-failure test (mismatched covariate) also returned the BH fallback, padj identical to `p.adjust(p,'BH')` |
| Shipped example BH step showed realized FDR 0.108 on its fixed seed | P2 | `examples/multiple_testing_correction.R` section 1 now averages counts and FDP over 50 draws (`mean_fdp` column) | ran (sections 1-2; parses) | BH mean FDP 0.046 vs nominal 0.05, Bonferroni/Holm 0.004, BY 0.005. Section 3 (IHW child retry) unchanged |
| lfdr had no threshold rule | P2 | Added Efron's `lfdr < 0.2` convention and `mean(lfdr[called])` as the set-FDR estimate to the q-value block | ran | qvalue 2.38.0, m=18,000: 987 called, mean lfdr 0.043, realized FDP 0.0375 (audit reproduced); lfdr < 0.1: 825 called, mean 0.022, realized 0.017 |
| IDR promised in description/taxonomy/reference with no code | P2 | Chose delete-the-claim: no `idr` binary on this machine and the tool is outside the Skill's scope. Removed from frontmatter `description`, the taxonomy row, and the Li 2011 reference | grep (no `IDR` left) | |

Redundancy: the IHW CAUTION comment block in SKILL.md (segfault rate, nbins, child process, fallback) was restated in the failure mode's Fix; the code-block prose now holds the instruction and the failure mode holds mechanism + pointer. Nothing left the Skill. `usage-guide.md` untouched (no IDR mention, no duplicated facts beyond the previous pass).

Left unfixed: the `de_table` P2 in agent_usability is closed by the same change. Not touched: shipped example's `rgamma` IHW covariate (null covariate, no power gain) and a `locfdr` package mention in the taxonomy row (no code, no audit finding).

---

## 2026-09-21 (structure)

Worktree `F:\OpenScience\wt\experimental-design-multiple-testing`, branch `fix/experimental-design-multiple-testing`. Env `crispr-screen-analyst\r.sh` (R 4.4.3, IHW 1.34.0).

- **Split:** none. SKILL.md was 277 lines (under 300).
- **Moved to `scripts/`:** the `ihw_safe()` block (SKILL.md, "Covariate-Weighted FDR -- IHW", ~18 lines) -> `scripts/ihw_safe.R`, code verbatim plus a header (purpose, inputs, usage) and a CLI entry (`Rscript scripts/ihw_safe.R in.csv pvalue mean_expression out.csv [alpha]`). SKILL.md keeps `source('scripts/ihw_safe.R')` and the three-line call. SKILL.md 277 -> 266 lines. Commit `refactor(experimental-design/multiple-testing): move runnable code to scripts/`.
- **How run** (audit's `data\de_pvalues_reaudit.csv`, m=18,000, exactly as SKILL.md invokes it): `source()` path returned IHW on attempt 1, 1018 discoveries vs BH 1006, realized FDP 0.040 (asserted < 0.1, padj in [0,1], length = m); CLI path gave the same 1018; forced failure (mismatched covariate length) returned the BH fallback with padj identical to `p.adjust(p, 'BH')` and attempts = 2. A separate full-length run had all 3 children fail (one hung, 130 s CPU, and I killed it by PID; the others exited without output) and fell back to BH, 1006, exit 0.
- **Stayed inline:** BH/q-value block (commented fragment illustrating a point, not a runnable pipeline), FCR block (10 lines), Python `multipletests` (2 lines). `examples/multiple_testing_correction.R` keeps its own inline IHW child-process retry; examples stay as they are.
- **Noticed, not changed (behaviour):** `ihw_safe()` has no timeout. On this loaded machine one IHW child hung rather than crashed (130 s CPU on m=18,000, where the normal run is seconds), and the wrapper would wait indefinitely. A per-child timeout is a behaviour change, so it was left.

---

## 2026-09-23 corrective Phase 1

Worktree `F:\OpenScience\wt\experimental-design-multiple-testing`, branch `fix/experimental-design-multiple-testing`. Env `crispr-screen-analyst\r.sh` (R 4.4.3, IHW 1.34.0, qvalue 2.38.0). Rejected tip: `ed2c5e1`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Shipped `examples/multiple_testing_correction.R` printed q-value and IHW output, then exited 139 in every Phase 2 run | P0 / M4 | Replaced its duplicate IHW retry implementation with the tested `scripts/ihw_safe.R` interface. Initial direct delegation still exited 139, so added `scripts/qvalue_safe.R`: qvalue runs in an isolated worker, writes `pi0` and discoveries before teardown, and the parent only falls back to BH if no usable worker output exists. The example no longer loads qvalue in the outer process. | ran | Focused isolation found `requireNamespace('qvalue')` alone exits nonzero during teardown in this Windows R environment, whereas `qvalue_safe()` alone and followed by `ihw_safe()` exit 0. Parsed the changed R files via the designated wrapper. The exact full-example audit runner exited 0 once; its three-run repetition harness recorded `run=1/2/3 exit=0`, each with pi0 0.912, 98 q-value discoveries, and 85 IHW versus 93 BH discoveries. No shared environment versions or locks changed. |

Left unfixed: the pre-existing P2 `locfdr` taxonomy-only mention remains outside this P0 corrective pass; it does not affect the repaired shipped-example exit path.
