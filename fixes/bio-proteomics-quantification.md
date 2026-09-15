# bio-proteomics-quantification fixes (2026-09-15)

Branch `fix/proteomics` (worktree `F:\OpenScience\external\bioSkills-wt-proteomics`). Runtime: candidate venv (pandas 3.0.5, numpy 2.5.3) and R via `r.sh` (MSstats 4.14.2, iq 2.0.1, MSnbase 2.32.0, limma 3.62.2). SKILL.md blocks were extracted and run on copies of the audit data.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| MaxQuant `read.table` silently drops rows at apostrophes | P1 | `quote = '', comment.char = ''` on both tables, `stopifnot` row count vs `readLines`; Common Errors row | ran: evidence 10369 rows, proteinGroups 1560, MSstats 296 proteins (audit Skill read: 2954 rows, 57 proteins) | |
| `makeImpuritiesMatrix(x = 10)` blocks non-interactive runs | P1 | `edit = FALSE`; commented `filename = 'lot_coa.csv', edit = FALSE` CoA route; TMT10 N/C interleaving note in failure mode; Common Errors row | ran under Rscript on `tmt10_synthetic.mzML`: block completed (24 x 10) in 23 s; filename route returned 6 x 6 | MSnbase ships no TMT10 CoA csv, so the filename route was checked with its TMT6 template |
| `MBimpute = FALSE` contradicts "censored-value handling" / MSstats-AFT | P1 | Approach, decision-tree row, code comments and Common Errors row now say FALSE = no censoring model (on/off -> `-Inf`, `oneConditionMissing`), TRUE = the only AFT route; DA Skill taxonomy aligned in its own commit | help: `dataProcess` MBimpute/censoredInt docs (MSstats 4.14.2); audit run showed 0 vs 573 imputed rows | MBimpute default in the snippet left FALSE, now labelled |
| `iq::maxLFQ` does no delayed normalization; median centering assumption hidden | P2 | Header bullet, taxonomy, Approach and code comment require run-normalized input (`iq::preprocess(median_normalization = TRUE)`); median-centering Approach states the unchanged/symmetric assumption; Pham 2020 reference | help: `?maxLFQ`, `?preprocess` (iq 2.0.1); block ran on a toy matrix | peptide-matrix scaffold not added (new content) |
| SILAC +/-Inf breaks limma | P2 | Vectorized `silac_log2_ratio` returns NaN ratio + presence flag (both / H-only / L-only / none); Approach, failure-mode fix and Common Errors row | ran on `silac_proteins.csv`: 0 Inf, rep1 both 371 / L-only 13 / H-only 5 / none 11; `eBayes(trend, robust)` ran on 376 rows after dropping all-NaN rows | labeling-efficiency and Arg->Pro check code not added (new content) |
| IRS silently yields Inf/NaN on 0/NaN reference; tautological example check | P2 | Mask references `<= 0`/NaN and print unbridged proteins (SKILL.md and example, positional reference column); example simulates shared protein levels and checks the non-reference plex offset | ran on `tmt_plexA/B` with 3 zero + 3 NaN plex-B references: 6 reported, 0 Inf, offset +1.053 -> -0.059; example exit 0 (offset +0.951 -> -0.019), `py_compile` OK | |
| No clinical-use stop condition | P2 | One Scope sentence routing patient classification / treatment decisions to validated clinical assays | n/a (text) | |

Also: version line changed to the checked versions.

Left unfixed: none of the findings; the two partial items above (maxLFQ scaffold, SILAC labeling-check code) were left out as new content.
