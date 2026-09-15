# bio-proteomics-ptm-analysis fixes (2026-09-15)

Candidate `mass-spec-proteomics-analyst`. Worktree `F:\OpenScience\external\bioSkills-wt-proteomics-b`, branch `fix/proteomics-b`, commit `d6e18ac`. Runtime: R 4.4 with MSstatsPTM 2.8.1 via `r.sh`; candidate venv (pandas, scipy); KSEAapp 2.0 not installed, its CRAN source unpacked to the scratchpad and sourced. Audit data `audits/bio-proteomics-ptm-analysis/data` (copied to scratchpad).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| MSstatsPTM block fails: `append` assertion, `data.type = 'LF'` | P1 | `dataSummarizationPTM(..., use_log_file = FALSE, append = FALSE)`; `groupComparisonPTM(..., data.type = 'LabelFree')`; version header 2.8.1; two Common Errors rows | ran: SKILL.md block on audit phospho evidence, exit 0, three models returned | Defaults from `args()` on 2.8.1 |
| Protein dataset never built (`evidence_prot` missing) | P1 | `evidence_prot`, `which_proteinid_protein`, `stopifnot('PROTEIN' %in% names(input))`; Common Errors row | ran: `names(input)` = PTM, PROTEIN; protein_driven sites called after adjustment 0/6 | |
| Melt adds a bogus `Intensity` run | P1 | Columns selected by `Intensity <run>___[123]`, run label regex fixed; Common Errors row; example now carries per-run and aggregated columns | ran: audit `Phospho (STY)Sites.txt` gives runs C1-C4, T1-T4 only (24 columns); example exit 0, runs C1/T1 | |
| R path skips localization filter and keeps unmodified rows | P1 | Evidence pre-filtered to rows with Phospho in `Modified sequence` and max `Phospho (STY) Probabilities` >= 0.75; result rows without `_<residue><position>` dropped; failure-mode Fix says every route | ran: 0 tested sites with truth loc_prob < 0.75; 36 ADJUSTED rows, all sites (audit: 80 rows, 39 bare proteins) | Max-probability rule as recommended; multiply-phospho peptides pass on their best site |
| Motif NameError; no background, test or kinase-activity code | P1 | Motif block uses `phospho`; `matched_background()` and Fisher + BH `motif_enrichment()`; new KSEAapp section with `KSEA.Scores(KSData, PX, ...)`, PX column order, linear FC, gene mapping and prior source | ran: motif block on audit Sites + FASTA (35 foreground, 1888 background windows); `KSEA.Scores` sourced from KSEAapp 2.0 on its demo KSData/PX: 109 kinases, z-scores invert with 1/FC; PX contract per `PX.Rd` (docs) | KSEA not run on the audit data (synthetic gene symbols do not match the prior) |
| Double filter conflicts with differential-abundance | P2 | TREAT-style `pt((|log2FC| - 1)/SE, DF, lower.tail = FALSE)` + BH on ADJUSTED.Model replaces the double filter | ran: SE/DF columns present, 10 sites called | Evidence: audit lead-4 simulation (9-13% vs 5%) |
| Default contrast direction not stated | P2 | Explicit `contrast.matrix` (Treatment 1, Control -1); Label note in code, KSEA section and Common Errors | ran: Label `Treatment vs Control`; site_regulated signs match truth | |
| FLR and K-GG QC lack a runnable route | P2 | Spectra required for LuciPHOr2/DeepFLR; model-based `mean(1 - Localization prob)` labelled as such; ask for alkylation reagent; C-terminal GG-K regex | ran: regex flags the 4 artifact peptides in audit glygly evidence (25 rows) | |
| `use_unmod_peptides` proxy undocumented | P2 | Decision-tree row: optional TRUE with a proxy-adjusted label; ADJUSTED.Model absent without protein data | audit run: Input 3 | Not re-run |
| Small doc inconsistencies | P2 | Both filenames tried; example class bins `right=False` (0.75 is class I); "fake dephosphorylation" reworded as a masked form switch (Approach, failure mode, Common Errors, example); Ramsbottom 2022 JPR 21(7):1603-1615 added | ran: example shows 0.75 as class I; reference per audit Crossref check | |

Unfixed: none of the audit's findings. Not added: PTM-SEA/ssGSEA2.0 code (new content). DIA-NN `PTM.Q.Value` Common Errors row left as is (the audit marked it unverified, not a finding).

## Pass 2 (2026-09-15)

Re-audit score 83, deployable, one open P1. Worktree `F:\OpenScience\external\bioSkills-wt-prot2`, branch `fix/proteomics-2`, cut from `575ab94`. Runtime: R 4.4 with MSstatsPTM 2.8.1 via `r.sh`; KSEAapp 2.0 still not installed in the shared R-lib, so its CRAN source is sourced from the scratchpad (nothing installed or changed in the shared env). Audit data copied to the scratchpad; both `r` blocks extracted from the worktree SKILL.md and run.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| KSEA returns NaN for every kinase when any site has an infinite fold change | P1 | `ks <- adjusted[is.finite(adjusted$log2FC), ]` before PX (PX built from `ks`); the PX filter drops only `is.na(Gene)` now, since `is.finite(FC)` was the bug (FC = 2^-Inf = 0 is finite and `KSEA.Scores` then takes log2(0)); Common Errors row | ran: KSEA block on the auditor's Input-1 `adjusted` table (1 non-finite log2FC row) with the synthetic prior in PSP&NetworKIN layout: 3 kinases, no NaN z-scores, SYN_BASO_KINASE -2.55 and SYN_PRO_KINASE +3.37 against truth -1.2 and +1.2 | The auditor's P1, and their FC > 0 patch confirmed the cause. Filtering log2FC also removes +Inf, which FC > 0 would keep |
| `use_unmod_peptides = TRUE` crashes against the block's own class-I pre-filter | P2 | `use_unmod <- FALSE` flag at the top of the block; `keep <- is_mod & class I`, plus `| !is_mod` when the flag is on; passed as `use_unmod_peptides = use_unmod`; Decision Tree row and Common Errors row say the proxy needs the unmodified rows | ran: no-global variant with `use_unmod = FALSE` gives PTM.Model only (265 evidence rows, as before); with `TRUE` it now returns PTM/PROTEIN/ADJUSTED (507 rows) instead of the `Can't assign 4 names to a 0-column data.table` crash; the full block with the global run is unchanged at 36 ADJUSTED site rows and 10 regulated | |

Unfixed:
- **[P2] Modification names hard-coded to phospho.** A six-substitution refactor of two working blocks; nothing computes the wrong answer, so out of scope per the brief ("rewriting what works").
- **[P2] PTM-SEA and empirical FLR lack runnable routes.** New content (new tool commands), out of scope.
- **[P2] SKILL.md too heavy for context.** Restructuring into `references/`, not a correction.
