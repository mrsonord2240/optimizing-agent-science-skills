# Fix log: bio-crispr-screens-combinatorial-screens (2026-09-19)

Fresh fixer. Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:crispr-screens/combinatorial-screens`.
Fork branch: `fix/cs-combo` off `main` at `b9a9bd5`, worktree `F:\OpenScience\wt\cs-combo`. Commit `7763a3c`.
Audit: `F:\OpenScience\audits\bio-crispr-screens-combinatorial-screens\` (87, Limited Release, deployable, no P0, 3 P1s).

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| `gi_score()` docstring/body used `paired_lfc`/`single_lfc`; `examples/gi_scoring.py` and usage-guide use `lfc`, causing `KeyError` on the documented file format | P1 | Renamed SKILL.md's `gi_score()` columns to `lfc` throughout (docstring + body), matching `examples/gi_scoring.py`'s convention | ran | Ran the corrected function (env python, `crispr-screen-analyst` venv, pandas 3.0.5/numpy 2.5.3/scipy 1.18.1) against a synthetic `paired_lfc`/`single_lfc` pair built in the documented `['gene_A','gene_B','lfc']`/`['gene','lfc']` format: no `KeyError`, planted synthetic-lethal pair recovered at z<-2 |
| `mageck mle`'s `interaction\|fdr` non-reproducible across identical reruns (39/40 genes differed per audit; no seed option) | P1 | Added an explicit non-reproducibility note under the MAGeCK MLE interpretation table in SKILL.md, pointing back to the deterministic GI z-score method for any claim that must hold across reruns | docs | Not rerun here (audit already ran the two-rerun comparison and confirmed via `mageck mle --help` that no seed flag exists); text states the audit's exact 39/40 figure and MAGeCK 0.5.9.5 version |
| No explicit clinical/practice-boundary escape hatch (Input 6 declined a patient-therapy request on general judgment only) | P1 | Added a Scope note under SKILL.md's Cross-Modality Validation section: screen hits are research leads, not patient-treatment recommendations | n/a (prose) | Short, single addition, placed where the Skill already discusses drug-target nomination |
| (standing rule, not audit-scored) usage-guide.md duplicated SKILL.md's Architecture Decision Tree and Quantitative Thresholds tables near-verbatim (flagged P2 in audit), and every Tips bullet but one restated Failure Modes / Cross-Modality Validation / the Cas9-vs-Cas12a recommendation | P2 (cheap) + dedup rule | Collapsed usage-guide.md's Decision Cheat Sheet table, Thresholds table, and Tips section to short pointers into the matching SKILL.md sections; kept the one non-duplicate Tips line (Perturb-seq pointer) | read | No fact deleted -- each now lives once in SKILL.md, which is unchanged content-wise (only the two P1-adjacent additions above touch SKILL.md's prose) |

## Unfixed

- P2 "no multiple-testing correction guidance for genome-scale z-score GI calling" and P2 "no minimum-N guidance for the z-score cutoff" -- left open. Both are method-guidance additions (new recommended defaults/thresholds), not corrections of an existing wrong claim, so out of scope for a fixer per FIX_BRIEF ("method-level changes only when the audit demonstrated the problem with a run" -- here the audit demonstrated the *symptom*, i.e. underpowered N=8 cutoff, but the brief's own examples/scope treat adding new statistical guidance as beyond "cheap P2 correction"). Left in `REMAINING.md`/audit record for a future pass; a re-auditor should confirm this call.

Nothing needs Sam.

# 2026-09-21 fix pass (Production Ready batch, 2 open P2s)

Fresh fixer. Worktree `F:\OpenScience\wt\crispr-screens-combinatorial-screens`, branch `fix/crispr-screens-combinatorial-screens` off staging `main` `431aa55`. Commit `1c9b412`. Env `crispr-screen-analyst` (pandas 3.0.5, numpy 2.5.3, scipy 1.18.1). SKILL.md 271 -> 249 lines; under 300, no split.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| No minimum-N guidance for the z<-2 GI cutoff (demonstrated at N=8 and N=9) | P2 | Added a "Minimum pair count" bullet to GI interpretation: z cutoff only with >= ~20-30 tested pairs where interactions are a minority; rank by raw `gi_score` for a handful of pairs; z cannot reach abs 2 at N<=5 | ran | Re-ran the re-auditor's `reaudit_smalln.py` (N=9: both planted pairs z -1.71/-1.85, missed; raw ranking puts both first). Own sweep, 2 planted GI=-2.5 pairs, null SD 0.4, 200 reps: missed 393/400 at N=9, 89/400 at N=12, 0/400 at N=20/30/50/100. Max possible z at N=6 is 2.04, N=9 is 2.67 (analytic) |
| No multiple-testing correction for genome-scale z calls | P2 | none | n/a | see Left unfixed |
| (redundancy) inline `gi_score()` block duplicated `examples/gi_scoring.py` | rule | Deleted the block, pointed at the example with its input columns and behaviour | ran | Ran the example on the audit's `paired_lfc_genome.tsv`/`single_lfc_genome.tsv`: 8 SL pairs at z < -4, 4 rescue, no error |
| (correction) two cross-references said the GI scoring section is "below"/"next section"; it is above | P2-level | Corrected both to "Genetic Interaction (GI) Scoring above" | read | |

## Left unfixed

- **`scripts/` move: none.** The remaining blocks are the MAGeCK MLE design-matrix heredoc plus one `mageck mle` call (illustrative design matrix, the content is the matrix) and a 9-line `in4mer_pair_analysis` helper; both below the runnable-pipeline bar. The one 18-line function (`gi_score`) duplicated an example and was deleted per the rule.

## Deleted passages -> new home

| deleted | now lives in |
| --- | --- |
| inline `gi_score()` function (SKILL.md GI Scoring) | `examples/gi_scoring.py` (pointer + description in SKILL.md; the missing-singleton `dropna` and column-name note are in the pointer text) |

Redundancy pass between SKILL.md and usage-guide.md was already done on 2026-09-19 (see above); usage-guide.md not touched.

# 2026-09-21 final pass, Phase 1 (fresh eyes on the multiple-testing P2)

Same-agent fixer+auditor final pass (`process/FINAL_PASS_BRIEF.md`). Worktree
`F:\OpenScience\wt\crispr-screens-combinatorial-screens`, branch `fix/crispr-screens-combinatorial-screens`
(same branch as the prior pass), commit `72e75e1`. Env `crispr-screen-analyst` (MAGeCK 0.5.9.5, pandas
3.0.5, numpy 2.5.3, scipy 1.18.1, statsmodels 0.15.0). SKILL.md 249 -> 251 lines; under 300, no split.

Dispatch asked me to re-examine the "multiple-testing (BH/FDR)" item that two prior passes (fixer
2026-09-21, re-auditor 2026-09-19 x2) had left open as "new content, no run ever demonstrated a false
positive." That reasoning turned out to rest on an untested assumption: every genome-scale synthetic
dataset either pass built planted a handful of *very large*-effect interactions (GI -1.8 to -2.5),
which inflate the self-normalized z-score's population SD enough to suppress noise from crossing the
threshold -- a property of that dataset design, not of the method. I ran two scenarios neither pass
had tried:

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| No FDR control at genome scale: an all-null 4,435-pair (Inzolia-scale) screen with zero true interactions gets 199-201 pairs falsely called by the raw z<-2/z>2 cutoff (the textbook ~4.5% two-sided rate); 20 true hits at a modest, realistic effect (GI=-0.3, SNR~5, vs. this Skill's own SNR~30 test cases) gives 178 raw calls, 158 (89%) false | P2 (reversed from "left unfixed" to fixed) | Added "Multiple testing at genome scale" bullet to SKILL.md's GI Scoring section with the numbers and exact `scipy.stats.norm.sf` + `statsmodels.stats.multitest.multipletests(..., method='fdr_bh')` call; added the same BH-FDR step to `examples/gi_scoring.py` (STEP 6.5), keeping raw classification alongside for the small hand-curated case; added a Common Errors row; added `statsmodels` to Version Compatibility and usage-guide Prerequisites | ran | BH-FDR on the all-null scenario: 0 false positives (vs 199-201 raw). BH-FDR on the modest-effect scenario: 0 false positives, 17/20 true hits recovered (vs 178 raw calls, 158 false). Re-ran updated `examples/gi_scoring.py` on the audit's own genome-scale data: 8 SL/4 rescue by both raw and BH-FDR -- identical to the prior pass's verified numbers, no regression |
| Minimum pair count bullet's own numeric claim ("0/400 at N>=20") does not reproduce | P2-level correction | Independent multi-seed reproduction (2 planted GI=-2.5 pairs, null SD 0.4) gives ~4% miss rate at N=20, ~0.5% at N=30, <=0.1% only from N=50. Corrected the bullet's numbers; raised recommended minimum from ~20-30 to ~50 pairs | ran | P(0/400 successes at the true ~3.3% rate) is ~2e-6 -- the original number was very likely one favorable run written up as if reproducible, not a fabrication, but not reliable either |

## Verified this phase (not previously run)

- SKILL.md's literal MAGeCK MLE bash block (heredoc `combo_design.txt` + `mageck mle
  --count-table/--design-matrix/--output-prefix`), copied verbatim and run against the audit's
  `combo_counts.txt`: exit 0, real `interaction|beta`/`interaction|fdr` output, planted gene `GENEA`
  correctly the most negative `interaction|beta` with `interaction|fdr`=0.0. Neither prior pass had
  run this exact heredoc verbatim (both used a pre-built `.sh` wrapper instead).
- `in4mer_pair_analysis` helper: never executed by any audit or fix pass before. Ran on a realistic
  4-pair/2-array-per-pair synthetic dataset; correct per-pair mean/std/count aggregation.
- `examples/gi_scoring.py` (pre-existing, unmodified logic) independently re-run on the audit's
  genome-scale data to confirm the baseline before adding the BH-FDR step.

## Left unfixed

- **`scripts/` move: none** (unchanged from the prior pass -- still true; no new runnable block of
  pipeline length was added this phase, only inline BH-FDR calls a few lines long).

Nothing needs Sam. See `F:\OpenScience\audits\_final_pass\bio-crispr-screens-combinatorial-screens\CHECKPOINT.md`
for the full checkpoint.
