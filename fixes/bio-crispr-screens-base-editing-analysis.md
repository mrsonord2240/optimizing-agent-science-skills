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
