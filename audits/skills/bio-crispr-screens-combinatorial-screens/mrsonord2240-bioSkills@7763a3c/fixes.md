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
