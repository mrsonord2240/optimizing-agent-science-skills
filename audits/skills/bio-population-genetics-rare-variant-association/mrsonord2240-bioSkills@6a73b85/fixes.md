# bio-population-genetics-rare-variant-association — fixes (2026-09-15)

Branch `fix/variant`. Runtime: WSL `agents` distro, regenie 4.1.3, plink2 a6.9, r-saige 1.3.1 (audit envs under /tmp/vaca); audit data copied to /tmp/vacafix/rv.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| SAIGE-GENE+ `--annotation_in_groupTest` separators reversed | P1 | `"lof,missense;lof,missense;lof;synonymous"`; comment now says comma = test, semicolon = annotations joined within a test | help: `step2_SPAtests.R --help` (SAIGE 1.3.1) states this; ran step 2 on audit data: groups `lof`, `missense;lof`, `missense;lof;synonymous` + Cauchy, exit 0, G21 Cauchy p 4.3e-8 | step 1 null reused from audit run in4 |
| regenie step-1 block omits `--bt` | P1 | `--bt` added, with note to fit step 1 on common array variants | ran (via example step 1): exit 0 | |
| `rare_variant_test.sh` runs step 1 on rare-variant genotypes | P1 | Separate `<array_prefix>` and `<exome_prefix>` arguments | ran: array/wes audit data, exit 0; G21 LoF SKAT-O LOG10P 7.93, G01 LoF+missense ACAT-O 4.01 | `bash -n` ok |
| "implicit singleton mask" | P2 | `.all` mask added; singleton masks need `--singleton-carrier` | audit regenie 4.1.3 output (`.all` masks, no singleton) | |
| SAIGE bgen step-2 command incomplete | P2 | `--bgenFileIndex`, `--sampleFile` added | help: both flags listed in `step2_SPAtests.R --help` | bgen form not run (no bgen/bgi built) |

Left unfixed: none.

## Backlog pass — 2026-09-15

Branch `fix/backlog-db` (worktree `F:\OpenScience\external\bioSkills-wt-db`). Runtime note: the prior
pass's WSL `agents` SAIGE 1.3.1 under `/tmp/vaca` is gone (confirmed 2026-09-16: no Rscript on WSL
`agents` PATH, no SAIGE/`step2_SPAtests.R` anywhere under `/`, no R conda env). The Windows R-lib at
`F:\OpenScience\audit-envs\variant-annotation-curation-analyst\R-lib` has SKAT and SPAtest but not
SAIGE.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| SAIGE bgen command omits --chrom or --LOCO=FALSE | P2 | Added `--chrom 1` to the SAIGE-GENE+ bgen `step2_SPAtests.R` command, renamed output to `gene_tests_chr1.txt`, and added a comment stating LOCO defaults TRUE, gene/region-based tests then require `--chrom` (recommended: one run per chromosome, each using that chromosome's own LOCO null from step 1), with `--LOCO=FALSE` as the alternative only if step 1 was not fit with LOCO | docs/source: SAIGE 1.3.1 `extdata/step2_SPAtests.R` source (github.com/saigegit/SAIGE) confirms `--LOCO` default=TRUE and `--chrom` required when LOCO specified; official SAIGE-doc `set_step2` page's bgen set-test example command uses exactly `--chrom=1 --LOCO=TRUE` | could not run — SAIGE not installed anywhere on this machine currently (see runtime note above); --help itself unreachable for the same reason, used GitHub source + official docs instead |
| SSD route does not warn about sample order | P2 | Expanded the one-line SSD-scan mention in SKILL.md (`Generate_SSD_SetID`/`Open_SSD`/`SKAT.SSD.All`) into a short code block: read the `.fam` file and `stopifnot(identical(fam$V2, covar_df$IID))` before the `SKAT_Null_Model` call that feeds `SKAT.SSD.All` (matches by row position, no ID join) | ran: R 4.x + SKAT 2.2.5 via `F:\OpenScience\runtime\envs\.r\lib\R\bin\x64\Rscript.exe` with `R_LIBS_USER=...\R-lib`; extracted new block to a temp `.R` file, `Rscript -e "parse(...)"` OK; synthetic test — shuffled covar_df and covar_df missing one ID both trip `stopifnot`, same data re-sorted to match `fam$V2` passes and `SKAT_Null_Model` fits (class `SKAT_NULL_Model_ADJ`) | commit `c410117` |
| Common Errors table misses step-1 trait-type/variance traps | P2 | Added two rows to the Common Errors table: regenie step-1 `phenotype '...' has very few unique values` (binary trait run without `--bt`) -> add `--bt`; regenie step-1 `Uh-oh, SNP ... has low variance` (ridge null fit on rare instead of common variants) -> fit step 1 on QC'd common array-type variants. Wording matches the existing step-1 code comments in this Skill | docs/source: regenie not on WSL `agents` this round (same runtime loss as items 13-14); both error strings confirmed verbatim by `curl`-fetching `rgcgithub/regenie` master source directly (`src/Pheno.cpp` line 922, `src/Data.cpp` line 209), cross-checked against GitHub issue rgcgithub/regenie#542 | commit `aec65fa`. **rare-variant-association complete (3/3: items 13-14-15). Full 15-item backlog/db slice complete.** |

## Final pass — 2026-09-24

Source commit: `6a73b8555e5ad5f07439e6f0870f5cf85542b083`.

The usage guide now exposes the SKAT SSD positional `.fam`/covariate matching invariant, requires `stopifnot(identical(fam$V2, covar_df$IID))`, and explains reordering before a scan. Seven archived scenario contracts plus two fresh inputs passed 14/14 assertions. The audit is 94/100 Production Ready with no open recommendations. External regenie, SAIGE, and SKAT runtimes were unavailable and are explicitly not claimed as executed.
