> **Audit record for `bio-microbiome-taxonomy-assignment`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@60fd788](https://github.com/mrsonord2240/bioSkills/tree/60fd788ddba9db5cdfdd157003ee4274e5c47349/microbiome/taxonomy-assignment) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-microbiome-taxonomy-assignment

Generated: 2026-09-23. Source: `mrsonord2240/bioSkills@60fd788ddba9db5cdfdd157003ee4274e5c47349:microbiome/taxonomy-assignment`.

## Result

**89/100 — Production Ready — deployable: true.** Both veto gates pass. This final-pass report deliberately records `auditor_independent: false` and the required CHECKPOINT note.

Fresh execution covered QIIME2 region extraction/training/classify-sklearn/consensus-vsearch, organelle filters, the shipped DADA2 example on 770 real moving-pictures ASVs, pre-trained and fresh-train paths of the shipped IDTAXA script, and seeded versus unseeded DADA2 behavior. Evidence and every executed script are in `run/2026-09-23-final-pass/`.

| Area | Fresh result |
|---|---|
| DADA2 example | 658/770 genus calls; seeded rerun 0 differences |
| DADA2 negative control | 15/770 unseeded genus differences |
| IDTAXA pre-trained | 482/770 genus calls; rerun `identical() TRUE` |
| IDTAXA fresh training | 3,000 real SILVA records; 169/770 genus calls; rerun `identical() TRUE` |
| QIIME2 | Extracted reference, trained NB classifier, emitted sklearn and vsearch taxonomy artifacts |

## Finding

P1: the QIIME2 `filter-seqs` example uses obsolete options (`--i-data`/`--o-filtered-data`); QIIME2 2024.10 rejected both. It now requires `--i-sequences`/`--o-filtered-sequences`.

P1: the DADA2 example's claimed all-NA wrong-reference safeguard is not discriminative. On a deliberately incompatible one-sequence reference, the exact shipped example reported **770/770 genus calls** and did not stop. A nonzero genus fraction cannot validate reference/primer compatibility.

P2: both DADA2 example invocations wrote complete output and then ended with a segmentation fault in this R runtime. This needs a clean-session reproduction before automation treats its exit status as reliable.

The dated prior audit remains preserved in `F:\OpenScience\audits\_pre-fix-20260919c\bio-microbiome-taxonomy-assignment`.
