# bio-population-genetics-rare-variant-association — final-pass fix log (2026-09-24)

Source branch: `agent/finalpass-bio-population-genetics-rare-variant-association-20260924`  
Source commit: `6a73b8555e5ad5f07439e6f0870f5cf85542b083`  
Source path: `population-genetics/rare-variant-association`

| Priority | Finding | Correction | Verification |
|---|---|---|---|
| P2 | The SKAT SSD row-order invariant was present in `SKILL.md` but not in the user-facing usage guide. A reader could use a shuffled covariate table and receive a plausible but invalid scan because `SKAT.SSD.All` matches rows by position. | Added the positional-matching warning, required `.fam`/`covar_df` identity assertion, and reorder instruction to `usage-guide.md`. | Final-pass current-source harness: the guide contains positional matching, `stopifnot(identical(fam$V2, covar_df$IID))`, and shuffled-table warning assertions. |

The prior three recommendations (SAIGE `--chrom`/LOCO guard, SKAT SSD source-level
row-order guard, and regenie step-1 error recovery) were already corrected at the
source tip and were rechecked as current-source contracts. Final audit: seven
archived scenario contracts plus two fresh inputs, **14/14 assertions passed**.
The raw report and viewer are source-pinned at the commit above with
`auditor_independent: false` and the required final-pass note. No publish, merge,
push, promotion, or shared index/backlog change was made.

External engine limit: no regenie, SAIGE, or SKAT runtime is installed in the
current audit host; this pass does not claim external-engine execution.
