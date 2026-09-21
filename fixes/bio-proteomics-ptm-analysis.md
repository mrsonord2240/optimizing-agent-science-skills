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


## Pass 5 (2026-09-15)

Re-audit after pass 2 scored **85 (raw 84.7)**, deployable, with the pass-2 KSEA correctness fix verified against
known truth (sign agreement 3/3, Spearman rho 1.0, a hand-computed Casado z matching the package to 0). That fix
was **not touched**. Worktree `F:\OpenScience\external\bioSkills-wt-prot5b`, branch `fix/proteomics-5b`, cut from
`openscience-fixes` at `1110c24`. Commit `b5355db`. Runtime: R 4.4.3 via the candidate `r.sh` -- MSstatsPTM 2.8.1,
MSstatsTMT 2.14.2, KSEAapp 2.0 (installed in the shared R-lib now, nothing installed or changed by this pass).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| No route for TMT / isobaric phosphoproteomics; the scope statement did not admit the gap | P1 | **Route written** (Sam's decision, 2026-09-15: write it, do not scope it out). New "TMT / isobaric plexes -- same adjustment, three different calls" subsection under the MSstatsPTM section: `labeling_type = 'TMT'` on `MaxQtoMSstatsPTMFormat`, `dataSummarizationPTM_TMT` (a different function, not a flag), `groupComparisonPTM(data.type = 'TMT')`, the MSstatsTMT annotation columns, and the `Condition = 'Norm'` reference channel `reference_norm`/`remove_norm_channel` need. Plus the two TMT-specific traps for the *adjustment* -- ratio compression biases `dFC_PTM - dFC_protein` rather than merely attenuating it, and enriched + global should share a plex. Decision Tree gained two rows; scope sentence now reads "label-free AND TMT"; usage-guide gained a TMT prompt and route line; `TMT_keyword` documented as belonging to the `sites_data =` route only | **ran, not parsed.** Built a synthetic TMT10 MaxQuant evidence pair (phospho + global, 8 sample channels + 2 pooled `Norm`) by reshaping the audit's own label-free synthetic set, so `truth_sites.csv` still applies. The block extracted verbatim from SKILL.md completes: `names(input)` = PTM PROTEIN, all four models, **39 ADJUSTED site rows**, Label `Treatment vs Control`. Against planted truth it behaves like the label-free route: protein_driven calls **6/8 -> 1/8** after adjustment, site_regulated **8/8** retained, masked **1/4 -> 3/4** recovered, sign agreement **8/8**, Spearman rho 0.691 vs true occupancy log2FC | The re-auditor could not execute the silent path for want of TMT evidence; this pass could. See the correction below |
| KSEA breaks on an empty filtered PX and on a single-match prior | P2 | Three guards around (never inside) the pass-2 correctness filter: `nrow(ks) == 0` stops with a message about one-condition sites; `Peptide = rep('NULL', nrow(ks))` instead of the length-1 literal; `nrow(PX) == 0` after the gene-symbol drop; and an explicit prior-coverage count, `paste(Gene, Residue.Both)` against `paste(SUB_GENE, SUB_MOD_RSD)` over the PhosphoSitePlus subset, stopping with the coverage number when it is below 2. Two Common Errors rows | ran: the re-audit's six-shape Input-D probe set plus a no-gene-symbol probe, with the block body spliced in verbatim. D4 (single-match prior) and D6 (empty PX) now stop with the coverage / one-condition messages instead of `no rows to aggregate` and `differing number of rows: 0, 1`. **D1, D2, D3 and D5 are unchanged to the last digit** -- BASO -2.5514841 FDR 0.008044892, PRO 3.3688957 FDR 0.001132050, RANDOM -0.6524595 FDR 0.257052400 | The coverage threshold is deliberately conservative; the real Input-1 table covers 14 of 31 sites and passes |
| Version Compatibility did not name the TMT dependency | P2 (found while working) | `MSstatsTMT 2.14.2 (the TMT route)` and `KSEAapp 2.0` added, with the check date | ran: versions printed from the session that executed the TMT route | |

**A claim I wrote and then had to correct.** The first draft of the TMT section said the reverse misconfiguration
is silent -- that TMT evidence left on the default `labeling_type = 'LF'` would make the converter read the MS1
`Intensity` column and collapse the channels. Executed on real TMT evidence, it is **not** silent: it stops with
`A non-empty vector of column names for 'by' is required`. Both directions are now documented with their exact
messages, with the point that neither message mentions labeling. (The forward direction reproduces the
re-audit's finding: a label-free annotation with `labeling_type = 'TMT'` gives `Extra columns included in the
annotation file that are not required ... Run, Raw.file, Fraction, TechRepMixture, Channel, Condition, Mixture,
BioReplicate` -- which doubles as the spec for the TMT annotation.)

**Label-free regression.** The MSstatsPTM block run verbatim from the edited SKILL.md on the audit's Input-1 data
still gives 36 ADJUSTED site rows, 10 regulated by TREAT (masked 2, null 3, site_regulated 5) and 1 non-finite
log2FC row -- the re-audit's numbers cell for cell. All three R fences `parse()`; all three Python fences and the
shipped `examples/phospho_analysis.py` `py_compile`.

## Left unfixed (pass 5)

- **[P2] Modification names hard-coded to phospho in both code paths.** Unchanged from pass 2: a six-substitution
  refactor of two working blocks, nothing computes a wrong answer.
- **[P2] PTM-SEA and empirical FLR have no runnable route.** ssGSEA2.0 and LuciPHOr2 are both installed, so this
  is now writable under the "missing referenced executables" rule -- but it is a second, independent route and
  this pass was already adding the TMT one. Flagged for a later pass rather than bundled in.
- **[P2] 391 -> 477 lines with no `references/`.** The TMT route necessarily grew the file. Splitting is a
  restructure, out of scope, and the static token-cost mark will get worse before it gets better.


## Pass 6 (2026-09-21)

Fix of the pass-5 confirmation audit (83, one open P1). Worktree `F:\OpenScience\wt\proteomics-ptm-analysis`, branch `fix/proteomics-ptm-analysis`. Runtime: R 4.4.3 via `r.sh`, MSstatsPTM 2.8.1, MSstatsTMT 2.14.2. Audit TMT10 synthetic evidence copied to the scratchpad.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| TMT section says Channel is `channel.1` .. `channel.N`; MaxQuant reporter columns are 0-indexed, so the annotation is rejected | P1 | Code comment now says channel names follow the evidence's `Reporter intensity corrected <n>` suffixes (`channel.0` .. `channel.9` for a 10-plex), read them off the header, and quotes the misleading `the channel name must be matched with that in input data` error. New Common Errors row for that message | ran: the SKILL.md TMT block, extracted verbatim, completes on the audit evidence with the 0-indexed annotation (names(input) PTM, PROTEIN; ADJUSTED 35 rows after the site filter); the audit's `channel.1..10` annotation confirmed present in the scratchpad copy. The rejection message itself is from the audit's run (viewer, Input 5) | Header check: evidence columns `Reporter intensity corrected 0` .. `9` |
| Reverse-direction TMT error quoted as one message could not be reproduced | P2 | Approach paragraph no longer quotes the `by` message; the Common Errors row lists the three loud errors the audit observed and says none names the labeling type, so check `labeling_type` first | docs: audit viewer Input 6 (three configurations, three messages); `by` message kept as one of the observed set (pass-5 capture) | |
| Redundancy (Sam's 2026-09-17 rule) | -- | `usage-guide.md`: deleted Prerequisites, "What the Agent Will Do" and Tips (all restate SKILL.md); replaced by a one-line pointer. Install commands moved into SKILL.md Version Compatibility | Tips content checked to exist in SKILL.md: paired global proteome (insight 3, decision tree), TiO2 vs Fe-IMAC (insight 1, decision tree), multiplicity columns (Python block comments, Common Errors), chloroacetamide (decision tree, Common Errors), motif background (decision tree, failure mode), prior-limited KSEA (Benchmark line), Ochoa triage (insight 4). Steps list restated the decision tree and TMT route (both in SKILL.md). The CLI search-engine line dropped (named in Scope) | |

All three R fences `parse()`; the shipped `examples/phospho_analysis.py` `py_compile`s (unchanged).

Left unfixed (pass 6):
- **[P2] PTM-SEA and empirical FLR still have no runnable route.** ssGSEA2.0 (`tools\ssGSEA2.0`) and LuciPHOr2 are installed, so the "missing referenced executables" rule says write them. Not cheap: PTM-SEA needs a flanking-sequence site GCT and PTMsigDB, and LuciPHOr2 needs spectra the audit data lack (no way to check it against truth here). Flagged to Sam, third pass deferring.
- **[P2] Modification names hard-coded to phospho in three code paths.** Unchanged reasoning (rewrites blocks that work).
- **[P2] SKILL.md heavy (about 480 lines), no `references/`.** Restructure, out of scope.


### 2026-09-21 addendum: LuciPHOr2 removed (Sam's decision)

The P2 "PTM-SEA and empirical FLR have no runnable route" was left open because LuciPHOr2 needs spectra the audit data lack. Sam decided to delete the reference rather than keep an unbacked mention: the LuciPHOr2 table row and its citation are removed from `SKILL.md`. The original LuciPHOr row and its 2013 citation stay (the citation backs the peptide-FDR-vs-site-FDR threshold). PTM-SEA is unchanged and still has no runnable block.

### 2026-09-21 addendum 2: PTM-SEA written (Sam: "go ahead and write it")

New `SKILL.md` section "PTM-SEA With ssGSEA2.0": `write_ptmsea_gct` (MaxQuant `Sequence window` [8:23] + `-p` -> the +/-7 flanking id PTMsigDB uses), the `ssgsea-cli.R` call, and `read_ptmsea`. Verified by extracting the three fences from the committed `SKILL.md` and running them as written (ssGSEA2.0 cae7bed, PTMsigDB v1.9.1, mass-spec env) on a planted table of real PTMsigDB ids: the 588 CDK1 substrate sites shifted +2 among 2,582 sites -> `KINASE-PSP_CDK1` rank 1 of 100 (NES 44.0, FDR 0.0056); the same values shuffled across sites -> CDK1 rank 37 (NES 0.47, FDR 0.95), no signature below FDR 0.05 (two sit at exactly 0.05). Found while testing: PTMsigDB also holds `-ac`/`-m2`/`-m3` ids (noted in the text; the helper builds `-p` only); only 100 of 495 signatures reach `-m 10` on 2,588 ids (checked by counting). Not tested: mouse/rat databases, PTMsigDB v2.0.0, multi-sample input. The audit's own synthetic phospho table has no sequence-window column and made-up proteins, so it could not be the test input.
