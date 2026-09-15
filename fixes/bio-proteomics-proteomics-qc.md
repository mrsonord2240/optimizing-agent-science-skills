# bio-proteomics-proteomics-qc fixes (2026-09-15)

Candidate `mass-spec-proteomics-analyst`. Worktree `F:\OpenScience\external\bioSkills-wt-proteomics-b`, branch `fix/proteomics-b`, commit `f3ad60f`. Runtime: candidate venv (pandas, scikit-learn, scipy); R 4.4 with MSstatsTMT 2.14.2 via `r.sh`; audit data `audits/bio-proteomics-proteomics-qc/data` (copied to scratchpad).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `raw_sample_qc` counts MaxQuant zeros as quantified | P1 | `replace(0, np.nan)` inside; zeros-are-missing sentence (MaxQuant, DIA-NN PG.MaxLFQ) | ran on `proteinGroups_failed.txt`: T4 1031 IDs, 31.3% missing (was 1500, 0%) | |
| Un-normalised column never named; no ID threshold | P1 | MaxQuant `Intensity`, DIA-NN `Precursor.Quantity`, raw TMT reporters named; `raw_sample_qc(raw, sample_groups)` adds fold-vs-group total and IDs, flag at <=0.5x total or <0.8x IDs; prose applies the rule to total signal, not boxplot median; failure mode updated | ran: failed file flags T4 on `Intensity` (0.41x total, 0.81x IDs), not on `LFQ intensity`; clean file flags nothing | DIA-NN column names from audit Input 2 run |
| `pca_batch_check` crashes / centres failed sample | P1 | Sample-index check with explicit error, complete cases instead of row-median fill, `n_components=min(5, n-1)`; Common Errors row | ran: RangeIndex raises clear ValueError; n=4 runs (3 PCs); T4 centroid distance 36.0 vs <=15.4 for others | |
| MSstatsTMT QC plot post-normalisation by default | P1 | Decision-tree row: `proteinSummarization(..., global_norm = FALSE, reference_norm = FALSE)`, PSM-level input; new `tmt_channel_balance()`; Common Errors row | ran: MSstatsTMT 2.14.2 with both FALSE, channel medians 23.96-24.52 (A) / 24.93-25.39 (B); balance code: 0 flags on audit plexes, flags a channel scaled 0.3x | Args from `args(proteinSummarization)` |
| PTXQC ">1%" contaminant flag misattributed | P2 | Lab-baseline + group-difference wording; `contaminant_fraction()`; example print aligned | ran: 4.19-6.52% on audit table | Attribution per audit's PTXQC 1.1.5 help check |
| Dead `abundance_bins`; "~14x" | P2 | `missingness_profile` returns present fraction per abundance bin; compression worded as ln2 x mean log2 (15-20x typical) in two places | ran: profile 0.34 -> 0.98 rising; 17.6x at mean log2 25.7 (ln2 x mean = 17.8) | |
| Batch guidance inconsistent; no stop conditions | P2 | Batch in design for the test, `removeBatchEffect`/ComBat for plots only; one stop-conditions sentence | text only | |
| Example median-fill PCA | -- | Complete cases, matching the Skill | ran: py_compile, exit 0, ctrl_3 still flagged | |

Unfixed: QC-report / exclusion-decision template and DIA/Level-1/2 code (new content, out of scope). DIA-NN "High precision" claim remains unverified (no DIA-NN here).

## Pass 2 (2026-09-15)

No change; left byte-identical. The re-audit (86, Production Ready) reports no P1 and no demonstrated defect in what runs -- every open item is a P2 asking for new content (commands, code for a prose-only step, a report template) or a wording softening, which the brief puts out of scope.

Also **not tested: the DIA-NN "High precision mode halves median CV" claim**, so the sentence is unchanged. It is not cheap here: the earlier library-free run under `audit-envs/.../public-work/diann_libfree` died during spectral prediction and left `diann_out` empty, so there is no library and no `.quant` file to reuse -- testing it means two full library-free DIA-NN runs over a 7.75M-precursor predicted library for three Astral runs. And PXD070049 has one replicate per condition (its own README says there is no CV or replicate-precision check), so a within-condition median CV cannot be computed from this data at all. Needs either a replicated dataset or a budgeted DIA-NN run.
