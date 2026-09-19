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
