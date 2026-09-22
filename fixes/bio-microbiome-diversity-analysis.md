# Fix log: bio-microbiome-diversity-analysis

2026-09-19 — fixer pass on `fix/mb-diversity-analysis` (worktree `F:\OpenScience\wt\mb-div`), base
`mrsonord2240/bioSkills@ff10062`. Source audit: `F:\OpenScience\audits\bio-microbiome-diversity-analysis\`
(92/100, Production Ready, deployable, no open P0).

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| `examples/diversity_analysis.R` crashes with `"object 'Group' not found"` at the `adonis2` call — `meta <- data.frame(sample_data(ps_rare))` never got a `Group` column; only the separate `alpha` data.frame did | P1 | Added `meta$Group <- sample_data(ps_rare)$SampleType` immediately after the `meta <-` line | ran | Ran the full script end-to-end on its own `GlobalPatterns` demo data (not a trimmed copy): completes with `Done.` and both plots written, no further errors — the crash was isolated to this one line; nothing downstream also referenced the missing column. |
| SKILL.md's Beta Diversity/PERMANOVA section had no repeated-measures/pseudo-replication guidance, unlike the parallel Alpha Diversity section (`"escalate to lme4/nlme for repeated measures"`) | P1 | Added a `strata = meta$SubjectID` `adonis2` line to the Beta Diversity in R code block, plus a short note explaining that pooling repeated/matched samples without `strata=` pseudo-replicates | ran | Reproduced live on the audit env's longitudinal fixture (`datagen/asvtable/long_phyloseq.rds`, not reusing the audit's saved numbers): naive pooled PERMANOVA R2=0.0528, p=0.098; `strata=SubjectID`-restricted R2=0.0528, p=1 — matches the auditor's numbers exactly, confirming the guidance is accurate. |
| P2: NMDS never mentioned; RPCA named in Tool Taxonomy/Decision Tree but only a one-line CLI reference, no worked example | P2 | Not added | help/docs | NMDS would introduce a tool the Skill's Decision Tree never currently claims — out of scope per FIX_BRIEF ("do not add a tool the Skill never mentioned"). RPCA is already claimed but its backing tools (DEICODE/gemelli) are deliberately not installed in the audit env: per `TOOLS.md` §4, installing them into the shared `qiime2-amplicon-2024.10` env would downgrade `scipy` to 1.10.1 and `scikit-bio` to 0.5.9 from the versions QIIME2 pins — a no-version-change violation. No installed tool exists to write and verify a worked example against, so left documented-but-thin as the audit found it. |
| Mandatory redundancy pass | — | `usage-guide.md`'s "Prerequisites" install commands (BiocManager/vegan/GUniFrac, QIIME2 conda env, scikit-bio pip) existed only there — moved into a new SKILL.md "Required Setup" section; `usage-guide.md`'s Prerequisites section replaced with a one-line pointer. `usage-guide.md`'s "What the Agent Will Do" (8-step workflow) and "Tips" (9 bullets) sections deleted entirely — inspection confirmed every point in both was already stated in SKILL.md (Scope routing, Choosing the Sampling Depth, Building the Tree, Alpha/Beta Diversity in R, Per-Method Failure Modes, Common Errors), so nothing was left to migrate. | inspection + `parse()`/`bash -n` on all changed code | `usage-guide.md` now holds only Overview/Prerequisites-pointer/Quick Start/Example Prompts/Related Skills. |

## Unfixed

- P2 NMDS/RPCA gap — not addressed; see table above for why (out of scope / tool not installed without violating the no-version-change rule).

## Verification

- `examples/diversity_analysis.R`: ran end-to-end with `rr.sh` against real `GlobalPatterns` data in
  `F:\OpenScience\audit-envs\microbiome-metagenomics-analyst\` (phyloseq 1.50.0, vegan 2.7.3) — completes
  clean.
- Strata fix: ran end-to-end against `datagen/asvtable/long_phyloseq.rds` in the same env — output
  matches the audit's reported p=0.098 (naive) / p=1 (strata) exactly.
- All changed `.R` code (the example script and both SKILL.md R code blocks, extracted and parsed
  together) passed `Rscript --vanilla -e "parse(...)"`. The one shipped `.sh` example was not touched
  and re-checked with `bash -n` regardless — clean.
- No packages installed or version-changed in the shared env.

## Environment

`F:\OpenScience\audit-envs\microbiome-metagenomics-analyst\` (R 4.4.3 / Bioconductor 3.20 via `rr.sh`,
phyloseq 1.50.0, vegan 2.7.3, picante 1.8.2, GUniFrac 1.9). See its `TOOLS.md` for the DEICODE/gemelli
non-install rationale cited above.

## 2026-09-21 - P2 batch (fixer; branch `fix/microbiome-diversity-analysis`, commit 69c0d36)

Env: `microbiome-metagenomics-analyst` (R 4.4.3 via `rr.sh`; phyloseq 1.50.0, vegan 2.7.3). SKILL.md 251 -> 274 lines (under the 300 threshold, no split).

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| Sampling-depth plateau has no numeric heuristic | P2 | New `scripts/pick_sampling_depth.R` (analytic `vegan::rarefy` over a depth grid; paired relative richness gain per 1000 reads < `tol`=1%; only depths keeping >= `min_keep`=85% of samples; prints curve, chosen depth, dropped samples, writes `depth_curve.tsv`). Invocation + explanation added to "Choosing the Sampling Depth" | ran | On the audit's `asv_counts.tsv` (40 samples): depth 7771, 35/40 kept, dropped S03, S17, S20, S29, S40 (audit's improvised heuristic gave 7169, 36 kept - same neighbourhood). Independent check in Python (hypergeometric expected richness): 141.176 vs script 141.176; dropped list = samples with total < 7771. Tiny `tol` runs the "no plateau" branch and says so; a QIIME2-style `#OTU ID` header also parses. First draft used a per-step gain that depended on grid width and, at 90% survivors, reported no plateau; changed to per-1000-reads gain and 85% floor. |
| NMDS never mentioned | P2 | `vegan::metaMDS` snippet (takes the Bray distance, `set.seed`, stress guidance) in new "NMDS and compositional (Aitchison) ordination in R" subsection | ran | Block extracted from SKILL.md and executed on the audit phyloseq object (36 samples after rarefying to 7000) and on GlobalPatterns (stress 0.172). Stress is ~0 on the audit fixture because its two groups collapse to two tight clusters; the text says ~0 means few-points data, not a great fit. Previous fix log declined this as "a tool the Skill never mentioned"; the audit names it as a recommendation and it is a vegan call in the section's own idiom, so it is written. |
| RPCA only a one-line CLI mention | P2 | Runnable `vegdist(method='robust.aitchison')` + adonis2 and `prcomp(decostand(., 'rclr'))` (axes + loadings); text states this is not DEICODE's RPCA (no OptSpace completion) and points to `qiime deicode rpca`/gemelli in its own env, marked not run here. Decision-tree row updated | ran (R block); docs only (DEICODE command) | Block run with assertions: adonis2 R2=0.52, p=0.001; permutest(betadisper) p=0.231; 40 scores x 200 loadings. DEICODE not installed (TOOLS.md sec.4: pip closure downgrades scipy/scikit-bio in the QIIME2 env; brief forbids install). |
| Redundancy (each fact once) | - | Deleted 4 Common Errors rows (PCoA fewer points; unweighted-vs-weighted; Shannon base; adonis2 vs overlap) that restate Per-Method Failure Modes, replaced by one pointer sentence; deleted the Alpha-section Shannon-base sentence; added `log2(e)` conversion to the Shannon failure mode | grep | usage-guide.md was already reduced in the earlier pass (overview, prompts, related skills only); nothing to do there. |

### Left unfixed

- Full DEICODE/gemelli RPCA worked example: needs an install into the QIIME2 env (downgrades scipy 1.10.1 / scikit-bio 0.5.9, forbidden) or a new dedicated env, which the batch brief also forbids. Backed instead by the runnable rclr/robust-Aitchison route above; the DEICODE command is documented, not run.
- Inline bash blocks in "Choosing the Sampling Depth" and "Building the Tree" (10-11 lines each) partly mirror `examples/core_metrics_qiime2.sh`. Left: under the ~15-line script threshold, they carry per-flag comments the agent uses, and `examples/` is exempt from the dedup rule.
- Thresholds table repeats a few statements from the Knobs and Failure Modes sections (min(sample_sums), alpha=0.5, DA rarefaction). Left: the table is where the citations and numeric floors live; collapsing it would drop the sources.

### Deleted passage -> new home

| deleted | now in |
| --- | --- |
| Common Errors: PCoA has fewer points than samples | Per-Method Failure Modes, "Sampling-depth sample-massacre" (symptom + fix) |
| Common Errors: unweighted UniFrac significant, weighted not | Failure Modes "Unweighted-vs-weighted flip"; Decision Tree row "Do not want to metric-shop" (single-metric hit tentative) |
| Common Errors: R and QIIME2 Shannon disagree | Failure Modes "Shannon base mismatch" (`log2(e)` added there) |
| Common Errors: adonis2 p<0.001 but groups overlap | Failure Modes "PERMANOVA dispersion"; Beta Diversity section (betadisper mandatory) |
| Alpha section: "Shannon from estimate_richness is in nats; QIIME2 log2..." | Failure Modes "Shannon base mismatch"; Tool Taxonomy Shannon row |

### Scripts

| old location | script |
| --- | --- |
| (new code, no prior inline copy) plateau-depth heuristic | `microbiome/diversity-analysis/scripts/pick_sampling_depth.R`, invoked from "Choosing the Sampling Depth" |
