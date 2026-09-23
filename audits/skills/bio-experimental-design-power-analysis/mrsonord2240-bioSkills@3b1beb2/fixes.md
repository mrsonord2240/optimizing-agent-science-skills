# bio-experimental-design-power-analysis — 2026-09-17

Worktree: `F:\OpenScience\wt\ed-power`, branch `fix/ed-power`, commits `e9cc709` (feat), `d657e59` (refactor).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| scRNA-seq route (powsimR) ships no runnable code | P1 | Added "scRNA-seq Power — Pseudobulk on Donors, Not Cells" section + new `examples/scrna_pseudobulk_power.R` using edgeR (already a stated dependency) to aggregate cells to donor pseudobulk and power on donor count, instead of powsimR (GitHub-only, not installed, install forbidden by dispatch) | ran | R 4.4.3 / edgeR 4.4.2, `r.sh examples/scrna_pseudobulk_power.R`: pseudobulk power ~0.000-0.070 at 4-12 donors vs. cell-level power 0.94-0.98 at realized FDR 0.87-0.89 — reproduces the prior audit's independent simulation (`run/04_input4_variantB_scrna.out`: pb power 0.000-0.087, cell FDR 0.872-0.892) to within simulation noise. |
| ATAC/ChIP/methylation route ships no runnable code | P1 | Added "ATAC-seq / ChIP-seq / Methylation Power" section reusing `RNASeqPower::rnapower()`/`PROPER` directly on per-region counts (no new tool) | ran + docs | `rnapower(depth=10, n=6, cv=0.5, effect=1.5, alpha=0.05)` on RNASeqPower 1.46.0 returns 0.220 (real, finite). Backed by the package's own vignette title, "Sample Size for RNA-Seq and similar Studies" (`vignette('samplesize')`), confirming the model is generic NB, not RNA-seq-specific. |
| Proteomics route ships no runnable code, separate from its multiplicity gap below | P1 | Added "Proteomics Power" section with a runnable `pwr::pwr.t.test` block | ran | pwr 1.3.0. |
| Proteomics decision-tree row drops proteome-wide multiplicity control, understating n 3-7x | P1 | Same Proteomics section: added Bonferroni-corrected `sig.level` alongside the raw call, reporting both; added matching Failure Mode / Common Errors / Reviewer Pushback rows | ran | pwr 1.3.0, `d=1.2`: raw n=12, Bonferroni (4000 proteins) n=43 — matches the audit's own numbers (`run/05_input5_stress_proteomics.out`) exactly. |
| `rnapower()`'s `depth` has no documented units or budget conversion | P1 | Added "Depth Units" section citing RNASeqPower's own vignette (`samplesize.Rnw`, installed): coverage >= 0.1 per million mapped reads for 85-95% of targets, so `depth ~= 0.1 x reads(millions)`; worked 20M-read example; added a Quantitative Thresholds row and a Common Errors row | ran + docs | RNASeqPower 1.46.0. `rnapower(depth=2, n=14, cv=0.3, effect=1.5, alpha=0.05)` = 0.287 vs. `rnapower(depth=20, ...)` = 0.818 — same n, opposite verdict depending on the unconverted vs. converted depth; the Skill's own flagship `depth=20` example implies ~200M reads/sample, unusually deep, now flagged explicitly rather than left implicit. |
| No guidance when the computed n is not fundable | P2 | Added a Failure Mode + Common Errors row: report power at the affordable n, or solve `rnapower()` for the minimum detectable effect instead | docs | `rnapower()`'s own contract (any one of `n`/`power`/`effect` may be omitted and solved for) already supports this; no new code needed, just the missing instruction. |
| Simulation determinism rests on an undocumented PROPER default | P2 | Version Compatibility now states `RNAseq.SimOptions.2grp`'s default `sim.seed=11111` explicitly and how to override it with `sim.seed=` | ran | Confirmed against the installed package's own source: `getAnywhere("RNAseq.SimOptions.2grp")` shows `if (missing(sim.seed)) sim.seed = 11111; set.seed(sim.seed)`. |
| Reviewer Pushback table promises "power curve provided" but no code calls a plotting function | P2 (unflagged contradiction, fixed under "internal contradictions") | Added `plotPower(powr)` to the existing PROPER simulation block | ran | PROPER 1.38.0, `plotPower()` runs against `comparePower()` output with no error (verified writing to a `pdf()` device). |

## Redundancy pass (every-pass rule, not audit-flagged)

`usage-guide.md`'s `## What the Agent Will Do` and `## Tips` sections fully restated `SKILL.md` content:

| Deleted passage | Now lives in SKILL.md |
|---|---|
| "Identify the assay and whether pilot data exist" / "Choose closed-form ... or simulation ..." | Decision Tree by Scenario |
| "Report power as a function of replicate number ... not a single transcriptome-wide value" | The Single Most Important Modern Insight |
| "Advise on the depth-versus-replicate allocation under budget constraints" | Depth vs Replicates -- the Budget Question |
| "Flag misuse of observed power and recommend effect-size/CI reporting" | Per-Method Failure Modes — Observed (post-hoc) power |
| Tips: "Power is per-gene; report marginal power..." | The Single Most Important Modern Insight |
| Tips: "Use simulation from the mean-dispersion trend..." | Simulation-Based Power section |
| Tips: "Estimate the CV or dispersion from pilot data..." | CV / Dispersion Guidelines |
| Tips: "Past roughly 10-20 million mapped reads, add replicates..." | Depth vs Replicates -- the Budget Question |
| Tips: "Power to the minimum biologically meaningful effect..." | Per-Method Failure Modes — Powering to the expected (or pilot-observed) effect |
| Tips: "Never use observed (post-hoc) power..." | Per-Method Failure Modes — Observed (post-hoc) power |

`usage-guide.md` now holds only Overview, Prerequisites, Quick Start, Example Prompts and Related Skills (71 -> 53 lines). Nothing the agent needs was deleted — every fact above already existed in SKILL.md before this pass, or was added there in the same commit.

## Unfixed / declined

None. All 3 P1s and both flagged P2s were fixed; the unflagged reviewer-pushback contradiction was fixed alongside them since it was a one-line addition (`plotPower(powr)`) directly enabled by the P1 work already being done on that block.

## Findings fixed: 5/5 (3 P1, 2 P2) + 1 unflagged contradiction.

Nothing needs Sam.

---

# 2026-09-21 (P2 batch)

Worktree `F:\OpenScience\wt\experimental-design-power-analysis`, branch `fix/experimental-design-power-analysis` (from staging `431aa55`). Audit: `F:\OpenScience\audits\bio-experimental-design-power-analysis\` (92, Production Ready, 2 P2). Env: crispr-screen-analyst (R 4.4.3 via `r.sh`; RNASeqPower 1.46.0, pwr 1.3.0, edgeR 4.4.2).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| No documented parameter-range validation across closed-form calls | P2 | Added a "Parameter ranges" paragraph to Version Compatibility. Stated from what actually ran, not the audit's suggested wording: `alpha`/`power` in (0,1); `effect` is a positive fold change != 1 (0.5 == 2, so no separate depletion rule; the audit's "effect > 1 (or < 1)" was refined); `rnapower()` does not validate (power=1.2 -> NaN + warning; power=1 and effect=1 -> Inf; alpha=1.5 -> 0.999; effect=0 -> 1; negative cv treated as positive; effect=-2, negative depth -> NaN + warning), while `pwr.t.test` errors on power/sig.level outside [0,1] | ran | Script run via `r.sh` on RNASeqPower 1.46.0 / pwr 1.3.0; every value quoted is the printed output. |

## Redundancy / dedup this pass

| Deleted passage | Now lives in |
|---|---|
| SKILL.md scRNA-seq section, inline 10-line edgeR block (`DGEList` ... `glmQLFTest`, `p.adjust`) | `examples/scrna_pseudobulk_power.R` (same calls, lines under `# --- pseudobulk by donor`); SKILL.md keeps a one-line description of the step and the pointer. Example re-run as invoked: pseudobulk power 0.000 / 0.070, cell-level FDR 0.897 / 0.888 at 4 / 12 donors. |

`usage-guide.md` redundancy pass was already done on 2026-09-17 (see above); nothing further to remove.

## Length and scripts

SKILL.md 264 -> 256 lines: under 300, no split. `scripts/`: no complete runnable block of ~15+ lines is inline (largest are 8-10 lines; the one candidate duplicated the shipped example and was deleted above), so no `scripts/` move and no third commit.

## Left unfixed

- **powsimR unverified (P2):** it is GitHub-only with a compile-required dependency (`bayNorm`), and installing into the shared env is forbidden. The audit itself says no action required for deployment; the Skill already carries a runnable, verified substitute (`examples/scrna_pseudobulk_power.R`) and warns of signature drift in Version Compatibility. Claim kept, not deleted, because it is labelled optional and the Skill backs the same question with code.

Findings fixed: 1/2 P2 (the other left unfixed, reason above).
