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

---

# Pass 4 — 2026-09-15 (re-audit at 84, Limited Release, CORE floor 85)

Branch `fix/proteomics-4-quant` (worktree `F:\OpenScience\external\bioSkills-wt-prot4c`), branched from
`fix/proteomics-3` @ `e8d2cd4`. Commit `1855824`. Evidence: the same re-audit at
`F:\OpenScience\audits\bio-proteomics-quantification\` (84, static 84, exec 84.0). Runtime: Python 3.12
shared venv (pandas 3.0.5, numpy 2.5.3).

This pass closes the **remaining part of the P1** that passes 1 and 3 both declined as "new content, not
corrections" — the re-auditor's "promised routines have no code" (Inputs 2, 3, 7, 9). Sam reversed that
call on 2026-09-15: the executables are the right fix. The table-level iq MaxLFQ part of the same P1 was
already done in pass 3, so what remained was SILAC labeling efficiency / Arg->Pro and AP-MS scoring.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| SILAC labeling-efficiency and Arg->Pro check have no code; the Skill instructs the agent to verify >= 95% incorporation on a heavy-only pilot and never supplies the calculation (Input 3, assertion FAIL) | P1 (part) | new block ahead of the ratio block: `silac_labeling_efficiency()` (intensity-weighted incorporation, per-peptide median, count below 95%, and the log2 H/L bias a 1:1 mix inherits, `log2(e / (2 - e))`) and `arg_to_pro_shift()` (slope of log2 H/L per proline, which separates scrambling from a flat labeling offset; Pro6 variable-mod route named); `ValueError` on an all-zero table | ran: block extracted verbatim from the edited SKILL.md and exec'd on a synthetic 1200-peptide pilot built at incorporation 0.93 / Arg->Pro 0.08 — recovered 0.9306 and 0.0745 (slope -0.1117 vs the true log2(0.92) = -0.1203); guard raises. Second, independent check: inverting the bias formula on the audit's own `silac_proteins.csv` gives implied incorporation 0.924 from the pooled -0.220 median log2 H/L on true-unchanged proteins — the Input-3 prompt states a 93% pilot | the -0.22 pooled offset is the same quantity the auditor printed as "label-efficiency bias -0.218" |
| AP-MS control-IP scoring has no code; the decision tree and failure mode say what to do in prose only (Input 7, assertion FAIL, specialized code scored 10 "no Skill code") | P1 (part) | new "AP-MS / Affinity-Enrichment Scoring" section: `score_vs_control_ips()` — no data-internal normalization, detection required in every bait replicate, log2 enrichment over control IPs with absent controls floored at that control run's detection limit (bait-only prey score finitely, not `+Inf`), plus a worst-bait-vs-best-control margin; followed by what SAINTexpress / CompPASS / CRAPome need before their statistics mean anything | ran: block extracted verbatim and run on `data/apms_lfq.csv` — 17 called, 15/15 true interactors, 0 of 60 sticky binders, 0 Inf cells, NaN enrichment only where `n_bait == 0`; byte-identical outcome to the auditor's own scaffold. The route the section warns against (median-normalize, rank against the input lysate) returns 46 sticky in its top 50 on the same data | median log2 enrichment by class: bait 6.82, interactor 5.99, sticky 0.02, background 0.09 |

Also, pointers only (no behaviour change): the two SILAC and the AP-MS failure-mode "Fix:" lines now name
the functions; four Common Errors rows added (all-negative H/L from incomplete labeling, Pro-dose shift,
AP-MS top-N-over-input); Ong & Mann 2006, Sowa 2009, Teo 2014 (SAINTexpress) and Mellacheruvu 2013
(CRAPome) added to References. All eight fenced blocks re-extracted after the edit: five `.py` `py_compile`
clean, three `.R` `parse()` clean. The untouched SILAC ratio block re-run verbatim reproduces the audit's
371 both / 13 L-only / 11 none / 5 H-only. Pure ASCII, 404 lines. Passes 1-3 untouched.

## Left unfixed

- **P2 TMTpro 16/18 impurity correction** — already closed in pass 3 (block comment + Common Errors row
  giving the x = 4/6/8/10 template limit, the `filename=` CoA route with 16 offset columns, and
  `reporters = TMT16` with no `TMT18`). Nothing left.
- Nothing else open from the 2026-09-15 re-audit.

## Noted, not a Skill defect

- The synthetic SILAC protein table carries a genuine ~-0.22 log2 H/L offset on true-unchanged proteins
  (implied incorporation 0.92), consistent with the 93% pilot in the Input-3 prompt. Useful as a fixture;
  it is not a defect in the Skill.

---

# 2026-09-21 - P2 pass, redundancy, split, scripts

Worktree `F:\OpenScience\wt\proteomics-quantification`, branch `fix/proteomics-quantification` (from staging `431aa55`). Commits `d3187a5` (fix + redundancy), `fa1e2b1` (split), `42e619d` (scripts). Evidence: `F:\OpenScience\audits\bio-proteomics-quantification\` (5 P2). Env `mass-spec-proteomics-analyst`: R 4.4.3 via `r.sh` (MSnbase 2.32.0, MSstats 4.14.2, iq 2.0.1), shared venv Python 3.12 (numpy 2.5.3, pandas 3.0.5).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| TMTpro needs hand-editing; CoA layout omits the leading Tag column | P2 | Commented `quantify(raw, reporters = TMT16, ...)` beside the TMT10 call; CoA layout now names the Tag column (read as row.names, error text quoted) with the extdata header rows inline | ran on `tmt10_synthetic.mzML`: `quantify(TMT16)` gives 24 x 16; a 16-channel CoA csv with Tag column (offset headers `-1`/`1` and `+1`/`+2`) -> `makeImpuritiesMatrix(filename=, edit=FALSE)` 16x16 -> `purityCorrect` 0 negatives (NA only in the 6 channels the 10-plex file lacks) | the commented `imp <- makeImpuritiesMatrix(filename = ...)` line was already there; the finding's second commented line is that one |
| AP-MS scorer absorbs a failed control IP silently | P2 | Prints `control runs with no data, excluded: [...]`, raises if every control is empty, adds `n_ctrl_runs_used` | ran on `apms_lfq.csv`: baseline 17 called / 3 runs; CtrlIP1 zeroed -> warning, 17 called / 2 runs; all zeroed -> ValueError | now `scripts/apms_score.py` |
| `min_bait_reps` default trade-off undiscussed | P2 | Approach sentence: strict default costs a one-replicate dropout, `min_bait_reps=2` the usual compromise, report what the looser setting adds | ran (example): prey with one of 3 bait replicates zeroed is missed by the default and called at `min_bait_reps=2` | |
| Nothing exercises SILAC or AP-MS code | P2 | `examples/lfq_normalization.py` gains a seeded SILAC pilot (asserts incorporation 0.93 +/- 0.02, Arg->Pro 0.08 +/- 0.02) and a seeded AP-MS matrix (asserts called set == planted interactors, sticky binders excluded, dead control counted); cited from the median-centering, IRS, SILAC and AP-MS sections | ran: exit 0, all asserts pass | the pilot's incorporation is read on proline-free peptides: on all peptides Arg->Pro drains the heavy channel and the pooled figure reads low (0.942 for planted 0.95 at 10% conversion); not changed in the Skill |
| 404 lines in one file | P2 | Split (below) | line counts, fence parse | SKILL.md 428 -> 272 lines after the split |

Line counts: SKILL.md 406 (start) -> 428 after fixes and install line -> 272 after the split -> 247 after scripts. Split moved verbatim: Isobaric section -> `references/tmt_isobaric.md`, SILAC section -> `references/silac.md`, AP-MS section -> `references/affinity_enrichment.md`; Reference Files index plus pointers on four decision-tree rows and two failure-mode cross-references. Checked: only six pointer lines differ from the pre-split text, python fences `ast.parse`, R fences `parse()`.

## Left unfixed

None of the five findings. Noticed, not changed: `silac_labeling_efficiency` reads incorporation on whatever table it is given, so on a pilot with Pro-containing peptides the pooled figure is biased low by Arg->Pro; documented in this log only (method-level change with no audit run behind it).

## Deleted passage -> new home (redundancy pass, `usage-guide.md`)

| deleted | new home |
|---|---|
| Prerequisites (pip / BiocManager / iq install) | `SKILL.md` Version Compatibility, "Install:" line (scipy and MSstatsTMT dropped: not used by any block) |
| "What the Agent Will Do" steps 1-7 | `SKILL.md` decision tree, Insight 2, Quantitative Thresholds, Common Errors (zero -> NaN row; summarizer sensitivity; hand-off to differential-abundance in Scope) |
| Tips (7 bullets) | zeros -> NaN: Common Errors; median centering is not MaxLFQ: Tool Taxonomy / failure mode; report summarizer: Insight 2; TMT compression, TMT plexes without IRS, SILAC on/off, NSAF: Per-Method Failure Modes |
| Related Skills (identical to SKILL.md) | `SKILL.md` Related Skills; guide points at it |

Added to the guide: one AP-MS example prompt.

## Moved code (old location -> script path)

| old location | new path | notes |
|---|---|---|
| `SKILL.md` MSstats block | `scripts/msstats_summarize.R` | args parametrised, optional MBimpute; ran: 296 proteins, 2305 rows |
| `SKILL.md` iq MaxLFQ table route | `scripts/maxlfq_iq.R` | single-protein `setNames` snippet stays inline; ran: 299 x 8, 3 disconnected |
| `references/silac.md` labeling + Arg->Pro functions | `scripts/silac_checks.py` | CLI + import; ran on a seeded pilot: 0.9419 pooled incorporation, conversion 0.10 recovered |
| `references/affinity_enrichment.md` scorer | `scripts/apms_score.py` | CLI + import; ran on `apms_lfq.csv`: 17 called |
| `references/tmt_isobaric.md` SL + IRS block | deleted, points at `examples/lfq_normalization.py` | duplicated the example |
| `references/tmt_isobaric.md` TMT reporter R block, `silac_log2_ratio`, median centering | kept inline | short code; rest is CoA guidance |

---

# Final pass Phase 1 — 2026-09-23

Worktree `F:\OpenScience\wt\proteomics-quantification`, branch `fix/proteomics-quantification`, commit `fb1efc10a979717f1fc66a48a6a8b12e95aa6401`. Runtime: Python 3.12 shared venv (numpy 2.5.3, pandas 3.0.5); R 4.4.3 via `r.sh` (MSstats 4.14.2, iq 2.0.1, MSnbase 2.32.0).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `silac_labeling_efficiency` reads incorporation falsely low when a heavy-only pilot includes Pro-containing peptides affected by Arg->Pro conversion (Revisit list) | P1 | When `Sequence` is available, calculate incorporation only on Pro-free signal peptides; report `n_signal_peptides`, `pro_containing_excluded`, and `sequence_column_used`; update the SILAC reference and exercise the public example through the helper | ran: seeded 1,000-peptide pilot at 0.93 incorporation / 0.10 conversion returned 0.9300 after excluding 759 Pro-containing peptides; unsafe all-peptide fallback read 0.9186; CLI JSON, all-Pro guard, `py_compile`, and every example assertion passed | Sequence-free inputs retain the old all-peptide calculation but explicitly report `sequence_column_used: false`, so they are not silently treated as conversion-safe |

## Left unfixed / checkpoint blocker

- **P1 verification limitation — TMT reporter R block:** `MSnbase::quantify` -> `purityCorrect` produced and asserted a 24 x 10 reporter matrix with 0 negative values on `tmt10_synthetic.mzML`, but the R process exits 11 after output. A separate `library(MSnbase)` probe also exits 11 and warns that `mzR` was built against Rcpp 1.0.13 while Rcpp 1.1.1 is installed. A private binary `mzR` kept the mismatch; a private source rebuild failed at `boost/regex/v4/regex.hpp` missing. The shared R library was not changed. Resolving this needs a compatible mzR/Rcpp build for the audit R 4.4.3 environment (or an approved environment rebuild); all source-side TMT assertions otherwise pass.
