# bio-crispr-screens-base-editing-analysis fixes (2026-09-16)

Worktree `F:\OpenScience\wt\crispr-b`, branch `fix/r2-crispr-b`, commit `5106c26`. Runtime:
CRISPResso2 2.3.4 (`pinellolab/crispresso2:latest` Docker), real synthetic-CBE output at
`F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\base-editing-synthetic\results\` (the
auditor's own real run, read-only, reused rather than regenerated); real MAGeCK
`sgrna_summary.txt` reused from `F:\OpenScience\audits\bio-crispr-screens-mageck-analysis\run\`;
BE-Hive via `F:\OpenScience\audit-envs\crispr-screen-analyst\tools\behive-venv\`.

## Round-2 audit pass — 2026-09-16 (M4 Code Usability veto, Reject/54)

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `find_be_spacers()` silently misattributes target/bystander for reverse-strand spacers: `genomic_pos` computed in reverse-complement coordinate space, compared against forward-strand codon boundaries with no conversion | P0 | Convert `genomic_pos` back to forward-CDS coordinates (`len(cds_sequence) - 1 - pos_in_seq`) for `strand == '-'` before the codon-overlap check | ran | Hand-constructed a reverse-strand spacer with a known-by-construction true forward index (idx 27, inside codon 10's [27,30) range): buggy code called it "bystander", fixed code correctly calls it "target". Also reproduced the audit's own random-CDS case (target_aa=40, seed=1): 14 reverse-strand window positions, every target/bystander call now matches the hand-recomputed true forward-CDS codon membership. |
| `filter_by_editing_efficiency()` crashes (`KeyError: 'Position'`) — real `Quantification_window_nucleotide_percentage_table.txt` has no `Position` column and is the transpose of what the code assumed | P0 | Rewrote to read with `index_col=0` (rows = nucleotide identity A/C/G/T/N/-), select the column positionally by `target_pos` (headers repeat — the real reference-base-per-position header is not a usable label), and fixed the value scale: the file stores fractions 0-1, not 0-100 despite its name, so `editing_pct = 1 - original_frac` replaces the old `(100 - original_pct) / 100` | ran | Real CRISPResso2 2.3.4 output: target C (pos 5) → 0.50 editing, exactly matching planted ground truth (50.00%); bystander C (pos 7) → 0.30, matching ground truth (30.00%). |
| `deconvolute_bystander()` crashes (`KeyError: 'Reference_pct'`) — real `Alleles_frequency_table.zip` has no such column | P0 | Changed the groupby aggregation column to `%Reads` (the real column) | ran | Real allele table: partition reproduces the planted 40/30/20/10 (unmodified/target-only/target+bystander/bystander-only) split exactly, sums to 100%. |
| `aggregate_variant_scores()` crashes (`KeyError: 'sgRNA'`) merging against real MAGeCK output | P0 | Merge key changed to `sgrna` (real MAGeCK `sgrna_summary.txt` column is lowercase) | ran | Ran against a real MAGeCK `sgrna_summary.txt` (columns `sgrna, Gene, ..., LFC, ...`) with a matching toy `variant_annotation_df`; merges cleanly, aggregation shape correct. |
| No bundled function validates its input schema before indexing, so any future drift is a bare, unhelpful `KeyError` | P1 | Added an explicit schema check (raises a specific `ValueError` naming the missing/unexpected column or position) to the top of `filter_by_editing_efficiency()`, `deconvolute_bystander()`, and `aggregate_variant_scores()` | ran | Confirmed the checks don't fire on real data (all three functions still run to completion and reproduce the same ground-truth outputs above). |
| BE-Hive integration is a single sentence with no code sample and no mention of its 50nt-substrate convention or internal position-numbering offset | P1 | Added a new "BE-Hive Editing-Efficiency Prediction" section with a runnable `init_model`/`predict` example, an explicit 50nt substrate construction (19nt upstream + 20nt spacer + 3nt PAM + 8nt downstream), and an assertion telling the agent to cross-check the substrate/spacer offset before trusting `pred_df`'s position-labeled columns | ran | Ran on BE-Hive git HEAD (maxwshen/be_predict_bystander, `tools\behive-venv`): `Total predicted probability = 0.9795`, real non-stub `pred_df` with `C4`/`C6` columns (BE-Hive's own naming) correctly identifying the planted target (spacer pos 5) and bystander (spacer pos 7). |
| Base Editor Chemistry Selection table and the editing-efficiency threshold convention duplicated near-verbatim between SKILL.md and usage-guide.md | P2 | Replaced usage-guide.md's duplicated threshold sentence and per-editor-window bullet with cross-references to SKILL.md's fuller table/convention; left usage-guide.md's distinct "Chemistry Cheat Sheet" (need→editor quick-decision table) as-is since it isn't the same content | docs | Cheap, as scoped; no functional change. |

All 7 `recommendations[]` entries (4 P0, 2 P1, 1 P2) fixed. Also updated the Version Compatibility
banner to name CRISPResso2 2.3.4 and BE-Hive git HEAD (2026-09-16), the versions every fix above
was actually checked against, replacing an untested "2.2.14+ / 1.0+" claim.

**Verification method:** all four fixed Python functions were extracted verbatim from the
committed SKILL.md (via a script that regexes out the ```python blocks), `py_compile`-checked,
and re-run end-to-end in that exact extracted form against real CRISPResso2 2.3.4 output, a real
MAGeCK `sgrna_summary.txt`, and BE-Hive git HEAD — not just checked in a scratch reimplementation.
`examples/base_editing_analysis.sh` was unchanged (no defect found in it this pass) and passes
`bash -n`.

Nothing left unfixed.

## Round-3 fix pass — 2026-09-21

Worktree `F:\OpenScience\wt\crispr-screens-base-editing-analysis`, branch `fix/crispr-screens-base-editing-analysis`.
Latest audit (2026-09-16 re-audit, core 87): 1 P1, 1 P2. Runtime: env venv Python 3.12.13, pandas 3.0.5, biopython 1.88.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `find_be_spacers()` raises bare `KeyError: 'n_bystanders'` when no candidate spacer exists | P1 | Return an empty DataFrame with the six result columns when `candidates` is empty | ran | Old function reproduced the KeyError on `'A'*60`; new one returns shape (0, 6) with the columns. Non-empty output on a seeded random 300nt CDS (target_aa=40) is identical to the old function's (`DataFrame.equals`). |
| `find_be_spacers()` has no editor-name validation | P2 | `ValueError` listing valid editors | ran | Bad editor raises the ValueError. |
| Lowercase-masked CDS silently finds no PAMs (audit's root cause for the empty case) | P2 (extra) | Upper-case `cds_sequence` after validation | ran | Lowercase input gives the same 25 candidates as uppercase. |
| Docstring promised a `predicted_aa_changes` column the function never returns | P2 (extra) | Docstring now lists the real columns | read | Internal contradiction. |
| `usage-guide.md` restated SKILL.md (dedup rule) | P2 | See below | read | |

### Deleted passages and where the content lives

- usage-guide "Prerequisites": `conda install` line -> SKILL.md Version Compatibility; BE-Hive and be-validation-pipeline clones already in SKILL.md; "Required inputs" -> SKILL.md "Broad be-validation-pipeline" section.
- usage-guide "What the Agent Will Do" (13-step workflow): steps already in SKILL.md (window math, library design, filtering, CRISPResso flags in `examples/`, hit calling, bystander deconvolution, ratio, ClinVar); MOI 0.3 and Gini <0.1 -> new SKILL.md Quantitative Thresholds rows.
- usage-guide "Tips": each already in SKILL.md (Failure Modes, Thresholds, Chemistry Selection); drugZ-vs-MAGeCK and "reuse the notebooks" -> SKILL.md be-validation-pipeline section; BE+PE gold standard -> Validation Strategy.
- usage-guide "Chemistry Cheat Sheet": covered by SKILL.md Chemistry Selection table, its Decision rule and the Cas9 vs BE vs PE table.
- usage-guide "Validation Strategy" table -> moved to SKILL.md as "Validation Strategy".

Disagreement logged: usage-guide gave `--base_editor_output` in workflow text while SKILL.md/examples use `--base_edit` for CRISPRessoBatch; the usage-guide copy is gone, SKILL.md untouched there.

Nothing left unfixed. Not run: no CRISPResso2/BE-Hive re-run (no change to those parts).

## 2026-09-21 (structure)

Worktree `F:\OpenScience\wt\crispr-screens-base-editing-analysis`, branch `fix/crispr-screens-base-editing-analysis`. Commits `2d75dcb` (split), `c9c5e09` (scripts). No behaviour or claim changes.

**Split.** `SKILL.md` 448 -> 180 lines (182 after the scripts pointer). Moved verbatim to `references/`: `be-hive-prediction.md` (was BE-Hive section), `library-design.md` (sgRNA Library Design), `screen-analysis.md` (Editing Efficiency Filtering, Bystander Edit Attribution, Hit Calling), `published-screens.md` (Hanna 2021, Cuella-Martin 2021), `be-validation-pipeline.md`. "Reference Files" index added to SKILL.md. Three one-phrase edits so pointers still resolve: "worked example below" -> `references/be-hive-prediction.md`; "the parsers below" -> "the parsers in this Skill"; "editing-efficiency convention above" -> "in `screen-analysis.md`". Verified: multiset comparison of non-blank lines, only those three lines differ; all python fences `ast.parse`, bash fence `bash -n`. Stayed in SKILL.md: chemistry table, window math, Cas9/BE/PE table, Validation Strategy, Failure Modes, Thresholds, Common Errors.

**Scripts** (old location -> script; each has header, argparse CLI, function body unchanged; the reference file keeps a one-command invocation):

| old block | script | run as invoked, on | assertions |
| --- | --- | --- | --- |
| `references/be-hive-prediction.md` python | `scripts/behive_predict.py` | BE-Hive venv, synthetic guide | total probability 0.9795, C4/C6 columns, offset assert |
| `references/library-design.md` `find_be_spacers` | `scripts/find_be_spacers.py` | seeded random 300nt CDS (target_aa 40) | output `.equals` pre-move function (25 spacers); `'A'*60` -> (0,6); lowercase CDS same count; bad editor -> ValueError |
| `references/screen-analysis.md` `filter_by_editing_efficiency` | `scripts/filter_by_editing_efficiency.py` | audit's real CRISPResso2 2.3.4 output (`base-editing-synthetic\results`) | pos 5 -> 0.50, pos 7 -> 0.30 (ground truth); pos 99 -> ValueError |
| `deconvolute_bystander` | `scripts/deconvolute_bystander.py` | same run's `Alleles_frequency_table.zip` | 40/10/30/20 split = planted truth |
| `aggregate_variant_scores` | `scripts/aggregate_variant_scores.py` | real MAGeCK `input1_canonical.sgrna_summary.txt` (71,090 sgRNAs) + synthetic annotation | row counts of target_only/mixed match the annotation |

Nothing stayed inline that qualified; the be-validation-pipeline bash (git clone / docker run / notebook list, ~10 lines of a workflow outline needing a Docker run and external repo) stayed inline as it is not a self-contained runnable script. `examples/base_editing_analysis.sh` untouched; no block duplicated it.

Noticed, not changed (structure-only task): `references/library-design.md` "Approach" says each spacer is annotated with predicted amino acid changes, but `find_be_spacers` returns only target/bystander positions.

## Final pass, Phase 1 — 2026-09-21

Worktree `F:\OpenScience\wt\crispr-screens-base-editing-analysis`, branch `fix/crispr-screens-base-editing-analysis`, commit `dd1d90a`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `references/library-design.md` "Approach" line promised `find_be_spacers` annotates spacers with predicted amino acid changes; function returns only nucleotide-level `target_positions`/`bystander_positions` | P2 | Corrected the line to describe the real output; pointed to variant-calling/variant-annotation (VEP) for protein consequence, matching SKILL.md's own Related Skills row. Same overclaim in `usage-guide.md`'s Library Design example prompt corrected to real column names. | ran | Hand-built a CDS with a window position landing exactly in the target codon (spacer_start=22, window pos 6, aa 10): real return is `target_positions=[6]`, `bystander_positions=[]` -- a position list, not an amino-acid label. Confirms the genuine mismatch. |
| `references/be-validation-pipeline.md` docker `CRISPRessoBatch --batch_settings batch_file.txt --skip_failed --base_edit` -- `--base_edit` is not a valid flag | P0 (broken command) | Replaced with `--base_editor_output`, the real CRISPRessoBatch flag | ran | Real CRISPResso2 2.3.4 (`pinellolab/crispresso2:latest`): `--base_edit` -> `error: ambiguous option: --base_edit could match --base_editor_output, --base_editor_consider_changes_outside_qw, --base_editor_target_ref_skip_allele_count`. Checked `CRISPRessoBatch --help`: `--base_editor_output` is the documented flag. Re-ran with the fix: parses correctly, proceeds past argument handling to file I/O (fails only on the placeholder fastq path, as expected). Not caught by any prior audit or fix pass on this Skill. |

**Every runnable block re-verified this pass** (regression check, no other defects found): `find_be_spacers.py` CLI + empty-result + lowercase + bad-editor cases; `filter_by_editing_efficiency.py` against real CRISPResso2 2.3.4 output (pos5=0.5, pos7=0.3, pos99=ValueError); `deconvolute_bystander.py` against the same run's `Alleles_frequency_table.zip` (40/30/20/10 split); `aggregate_variant_scores.py` against real MAGeCK `sgrna_summary.txt`; `behive_predict.py` against BE-Hive git HEAD (0.9795 total probability). All match prior fix-log ground truth. `examples/base_editing_analysis.sh` passes `bash -n`; its `CRISPResso --base_editor_output`/`--conversion_nuc_from`/`--conversion_nuc_to` flags checked against real `--help` (all valid). All 5 `.py` files `py_compile` clean.

Nothing left unfixed. Checkpoint: `F:\OpenScience\audits\_final_pass\bio-crispr-screens-base-editing-analysis\CHECKPOINT.md`.
