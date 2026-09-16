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

---

# Pass 3 — 2026-09-15 (re-audit at 84, Limited Release, CORE floor 85)

Branch `fix/proteomics-3` (worktree `F:\OpenScience\external\bioSkills-wt-prot3`), branched from
`fix/proteomics-2` @ `d1b8fdc`. Commit `1b80f7d`. Evidence: the re-audit at
`F:\OpenScience\audits\bio-proteomics-quantification\` (2026-09-15 14:57/14:58), not the archived pre-fix
report. Runtime: R 4.4.3 via `r.sh` (MSnbase 2.32.0, iq 2.0.1), Python 3.12 shared venv.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| maxLFQ block does not do what its own Goal states ("from a peptide quant matrix", but the code takes ONE protein group), and the prose names `iq::preprocess` without ever connecting it to `maxLFQ` (Inputs 2, 9) | P1 | block now runs the documented iq route `preprocess` -> `create_protein_list` -> `create_protein_table`, keeping the single-protein call underneath | ran: `data/evidence.txt` (10369 rows, 299 proteins, 8 runs) -> 299 x 8 protein matrix, per-run medians within +/-0.14 log2 (the audit's Input 2 saw the same spread); block re-extracted from the edited SKILL.md and sourced verbatim | this is the part of the P1 that is a correction rather than new content |
| `maxLFQ()$estimate` is an UNNAMED vector in input column order; the comment claimed "one MaxLFQ value per sample" | P1 | `setNames(result$estimate, colnames(...))` plus a Common Errors row | ran: `is.null(names(result$estimate))` is TRUE on iq 2.0.1; the column order on this data is `C1,C2,C3,C4,T1,T4,T2,T3` — not sorted, so an unnamed vector silently transposes samples | the audit hit the same thing as a bug in its own scaffold (Input 2) |
| `create_protein_table()$annotation` marks proteins whose samples are NOT on one common scale; not mentioned | P1 | `disconnected <- rownames(...)[nzchar(protein_table$annotation)]` in the block | ran: 3 of 299 proteins annotated, matching the audit's "3 with disconnected-sample annotations" | |
| `makeImpuritiesMatrix(x = 16)` errors, there is no TMTpro template, and the Skill says neither (Input 8) | P2 | block comment + Common Errors row: templates exist only for x = 4/6/8/10; TMTpro needs the lot CoA via `filename=` with 16 offset columns; `reporters = TMT16` exists, `TMT18` does not | ran + source read: x = 4/6/8/10 return matrices, x = 11/16 stop with `length of 'dimnames' [1] not equal to array extent`; `print(MSnbase::makeImpuritiesMatrix)` shows the else branch is `diag(x)` with NULL dimnames; built a 16-channel CoA CSV and ran `makeImpuritiesMatrix(filename=, edit=FALSE)` -> 16x16, accepted by `purityCorrect` on a 16-channel MSnSet (0 negatives) | MSnbase 2.32.0 |

Also: the TMT block was re-run verbatim on `data/tmt10_synthetic.mzML` after the comment edits (22.2 s,
24 x 10 corrected, 0 negatives). All six blocks re-extracted and `parse()` / `ast.parse()` clean. Pure ASCII.

## Left unfixed

- **P1, remaining part — SILAC labeling-efficiency / Arg->Pro check code.** Reconsidered as the dispatch
  asked. The Skill *instructs* the agent to verify >=95% incorporation on a heavy-only pilot; it never
  claims to supply the calculation, and nothing in it is wrong or self-contradictory. A new function is new
  content. Left.
- **P1, remaining part — AP-MS control-IP scoring code.** Same reading: the failure mode and the
  decision-tree row tell the agent what to do, and the audit confirmed that route recovers 15/15
  interactors. A SAINT/CompPASS-style scorer is a new section. Left.
- Not a Skill defect, noted only: R reads MaxQuant's all-empty `Reverse` / `Potential contaminant` columns
  as `logical NA`, so a `!= '+'` filter subsets to NA rows. Hit it in my own scaffold; the Skill has no
  such filter.
