> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@e58c885](https://github.com/mrsonord2240/optimized-scientific-skills/tree/e58c8855faaf8dcba2341453d73b62bcade3e78c/skills/bio-machine-learning-atlas-mapping) match audited candidate `a579d86464c9fd84579b6645107d0f6c72b87f091da33839966cc6b08c8a75ef` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-machine-learning-atlas-mapping`**
> - Audited working candidate `a579d86464c9fd84579b6645107d0f6c72b87f091da33839966cc6b08c8a75ef`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/machine-learning/atlas-mapping), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) delta re-audit worker E4, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-machine-learning-atlas-mapping

Generated: 2026-10-03
Audit type: independent delta re-audit (text-only change to certified bytes: frontmatter description reworded to fix AM-009), lane E4, worker E4 (did not normalize, tool, audit or fix this Skill)
Exact candidate content SHA-256: `a579d86464c9fd84579b6645107d0f6c72b87f091da33839966cc6b08c8a75ef` (7 files, 39483 bytes; `skill_preflight --offline` PASS before and after, candidate bytes untouched)
Certified baseline: `becbe61423e78eaae064b907ae4dc929d87852078244bf2586f218ca69b7eab3` (static 87, final 86); scores carried forward, only agent_specific re-scored.

## Result

**Static 88/100; Execution average 85.7/100; Final 86.6 (87); assertion pass rate 28/29; Layer 1 33.8/40; Layer 2 51.8/60.**
Grade: Production Ready. Skill veto PASS; Research veto PASS. Decision: **candidate-ready** for exact identity `a579d86464c9`.
Static moved 87 to 88: agent_specific 16 to 17, rubric 8.1 Trigger Precision = 3 ("mostly precise; minor over- or under-triggering risk"), the same line the pre-trim record held. Static weighted 35.2 + dynamic 51.4 = 86.62, rounds to 87 (certified delta record: 86).

## Delta qualification

- Only `SKILL.md` differs from the certified bytes; the other six files are byte-identical. The line diff is exactly one line, `description:`.
- Reverting `fix-description2-20261003/edits.json` on a scratch copy reproduces `becbe61423e78eaae064b907ae4dc929d87852078244bf2586f218ca69b7eab3` exactly.
- PyYAML `safe_load`: valid, `description` is one `str` (229 chars), keys name, category, description, tool_type, primary_tool, license, author; `name` equals the directory.
- Body byte-identical, so no command or script path changed; certified execution evidence applies.

## AM-009 verdict: resolved

New text: "Use when projecting a new single-cell dataset into an existing reference atlas embedding without retraining the reference, choosing a reference-mapping method, or judging whether labels transferred from the atlas are trustworthy."

- Rule conformance: one sentence, `Use when <task or situation>.`, no tool list, no coverage summary, no pointer to another Skill. Pass.
- Discrimination (shelf `bio-single-cell-cell-annotation`: "Automated reference-based cell type annotation ... using CellTypist, SingleR, Azimuth, scANVI, and scmap ... annotating cell types from a reference atlas or pretrained model, transferring labels onto a query, assessing prediction confidence and rejection, or triaging ... novel type versus doublet..."):
  - "Annotate cells from a reference with CellTypist or SingleR": the new description is about projection into an embedding; CellTypist and SingleR produce no shared embedding and are named only by cell-annotation. An agent picks cell-annotation. Correct.
  - "Map my query onto a saved scVI/scANVI atlas": matches "projecting ... into an existing reference atlas embedding without retraining the reference" almost word for word; cell-annotation names scANVI but frames the task as annotation. An agent picks atlas-mapping. Correct. This is the residual risk: cell-annotation also lists scANVI, so a request worded only "annotate with scANVI" is genuinely ambiguous, and a reasonable agent could take either.
  - Other single-cell siblings: batch-integration (no reference, integrate batches), markers-annotation (manual), preprocessing, doublet-detection, multimodal-integration (joint modalities) are separated.
- Residual, not scored as a finding: the third clause (judging whether transferred labels are trustworthy) overlaps cell-annotation's confidence/rejection trigger, and the body has no Related Skills hand-off to cell-annotation for classifier-only annotation (the certified AM-009 text also proposed this). An optional one-line body addition; it does not change the verdict because the first clause now carries the separation.

## Accuracy of "without retraining the reference"

True for the Skill's core path, with two qualifications. Independent check (`scripts/frozen_ref_check.py`, `logs/frozen_ref_summary.txt`, scvi-tools 1.5.1, 1222-cell reference, 2638-cell query): after `prepare_query_anndata` + `load_query_data` + 15 epochs at `weight_decay=0.0`, the saved reference reloads identical, the reference model object is bit-identical, and 33 tensors are bit-identical to the reference (every `z_encoder` tensor among them); only the decoder first layer (new batch columns) and the decoder batch-norm affine parameters changed (scvi-tools default `freeze_batchnorm_decoder=False`). So reference cells' embedding does not move; the query is fitted by fine-tuning a few query-side/decoder parameters.
- Qualification 1: the body's repeated "frozen reference weights" is slightly loose, since the decoder batch-norm affine parameters are fine-tuned by default. This is a body statement in certified bytes, not part of this change; embedding invariance, which is what the claim needs, holds. Observation only.
- Qualification 2: the clause is true of scArches surgery, Symphony and Azimuth (fixed references), scPoli and treeArches (built on scArches). It is not true of fine-tuned scGPT/Geneformer, and CellTypist/popV do not project into an embedding at all. The Skill labels all of these in its own table, and the clause qualifies the first, primary task; not an overstatement of what the Skill teaches, and the heavier methods are routed through the "choosing a method" clause.
Verdict: accurate, not an overstatement for the task it names.

## Open findings

- P2: AM-008 Marker check: no message when nothing is checkable, and no listed-versus-used marker count (unchanged).
- AM-009: resolved (closed).

All other certified dispositions are unchanged.

## Not executed

Unchanged from the certified record: Symphony, Azimuth/Seurat, scPoli, popV, treeArches/scHPL, scGPT/Geneformer are prose-only and labelled not executed. No other script was rerun (body unchanged).

## Evidence

Run root `F:\OpenScience\audits\bio-machine-learning-atlas-mapping\reaudit-delta3-20261003\` (scripts/qualify_delta3.py, scripts/build_delta3.py, scripts/frozen_ref_check.py, logs/qualify.json, logs/frozen_ref_summary.txt).
