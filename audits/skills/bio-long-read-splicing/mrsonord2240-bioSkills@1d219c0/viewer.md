> **Audit record for `bio-long-read-splicing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@1d219c0](https://github.com/mrsonord2240/bioSkills/tree/1d219c0a0bc1a422f6bc26a12f1dc2e08466ea61/alternative-splicing/long-read-splicing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-long-read-splicing (FINAL EXACT-COMMIT AUDIT)

Generated: 2026-09-24  
Source: `mrsonord2240/bioSkills@1d219c0a0bc1a422f6bc26a12f1dc2e08466ea61:alternative-splicing/long-read-splicing`.  
**Result: static 91, execution average 90.4, final 91, Production Ready, deployable true, no open P0/P1/P2.**  

## Exact-commit evidence

- Fresh static check: YAML/frontmatter and 14 code fences are balanced; `references/microexons.md` exists; both SKILL.md and usage-guide link the shipped example; the FLAIR output gate, uLTRA boundary, verified-kit-adapter rule, and valid-`zm` result are present.
- Retained independent execution logs substantiate the unchanged analysis commands: planted and real FLAIR, IsoQuant/Bambu, SQANTI3, rMATS-long, DTU, microexon controls, skera -> lima -> refine, and shipped-example runs.
- Runtime recovery: WSL environments `as-lr`, `as-lr-drim`, `as-sqanti`, and `as-pb` are installed. The historic `asenv` shell helper is absent and is replaceable by direct environment executables. Retention cleanup removed the generated fixture directories after the earlier run, so this final pass does not mislabel retained evidence as a new full execution.

## Resolved findings

- The diffSplice zero-exit failure is now a documented output-file gate.
- Direct-RNA error-rate scope and real-read bonus side effects are explicit; uLTRA is no longer a peer rescue route.
- The Kinnex synthetic-array result accurately explains the `zm` fixture dependency and does not invent an adapter filename.
- The heavy microexon evidence moved into a linked reference and the parameterized example is linked from both entry documents.

Full structured assertions and retained run details are in `eval_report_bio-long-read-splicing_result.json` and `run/logs/`.
