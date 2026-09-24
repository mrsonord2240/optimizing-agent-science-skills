> **Audit record for `bio-splice-variant-prediction`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@4b731c9](https://github.com/mrsonord2240/bioSkills/tree/4b731c929804830dee9ea5862ce8d1ec340f7f78/alternative-splicing/splice-variant-prediction) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-splice-variant-prediction

**90/100 — Production Ready.** Skill and research vetoes pass; no open P0, P1, or P2 findings.

`auditor_independent=false: this final pass was performed by the same agent that made the fixes.`

Source audited: `F:\OpenScience\wt\final-splice-variant-prediction` commit `4b731c929804830dee9ea5862ce8d1ec340f7f78`.

## Executed evidence

- Archived real-output parser/concordance suite: 6/6 pass.
- Fresh mixed GRCh37 input with a real SpliceAI run: supported records completed; a `<DEL>` row became `not_scored` rather than aborting the batch.
- Fresh all-symbolic long-REF input: generated a header-only safe VCF and a bounded warning key.
- Archived GRCh38 auditor panel rerun through real SpliceAI: overlapping-gene output exposes both `top_score_gene` and `annotated_genes` (for example, the OTC row retains `RP5-972B16.2,OTC`).

Raw logs and outputs: `run/final_pass_20260924/`.

## Corrections verified

- Unsupported `*` and symbolic ALTs are pre-filtered only for SpliceAI execution and remain visible in the final result as `not_scored`.
- Overlapping annotations now use truthful `top_score_gene` and `annotated_genes` fields; clinical/MANE transcript resolution remains explicit user work.
- Documentation no longer implies that extended-window scoring rescues every deep-intronic variant or that predictor concordance proves pathogenicity.

## Honest limits

Branchpoint tools with unavailable standalone resources are not claimed as executable. SpliceTransformer and CI-SpliceAI remain optional, heavyweight external integrations whose weights and versions must be recorded for each analysis. The score is capped below the mid-90s because this correction audit is non-independent.
