> **Audit record for `bio-causal-genomics-colocalization-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@dd57ffa](https://github.com/mrsonord2240/bioSkills/tree/dd57ffa39c21e80666c0ed1e8ece61a76cd8a76d/causal-genomics/colocalization-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-22 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-colocalization-analysis

Generated: 2026-09-22  
Source: `mrsonord2240/bioSkills@dd57ffa39c21e80666c0ed1e8ece61a76cd8a76d:causal-genomics/colocalization-analysis`  
Mode: D (Hybrid) | Category: Data Analysis | Complexity: Complex

This is a directed final-pass re-audit. `meta.auditor_independent` is deliberately `false`: final pass, as directed; see `F:\OpenScience\audits\_final_pass\bio-causal-genomics-colocalization-analysis\CHECKPOINT.md`. The rejected `9266ded` report and complete evidence are preserved at [`_pre-fix-20260922/.../rejected-9266ded-artifacts`](F:/OpenScience/audits/_pre-fix-20260922/bio-causal-genomics-colocalization-analysis/rejected-9266ded-artifacts/).

## Result

**PASS — 98/100, Production Ready, deployable: true.** All vetoes pass. The former M3/P0 is closed: `scripts/coloc_susie.R` independently checks eQTL z-scores against the supplied LD matrix before SuSiE/coloc, and rejects mismatches instead of emitting PP.H4.

| Inputs | Assertions | Execution average | Static | Research veto |
|---:|---:|---:|---:|---|
| 12 completed | 59/60 | 97.8 | 98 | PASS |

## Corrective evidence

The shipped executable regression was freshly run through the Windows-compatible Git Bash route:

```
PASS: eQTL LD mismatch rejected (lambda=1.000000) before coloc output
```

The prior rejected fixture was also rerun on the corrected tip. It measured `EQTL_LAMBDA_WITH_WRONG_LD=1.000000`, stopped with `LD reference mismatched to eQTL z-scores`, and did not write `coloc_susie_summary.tsv`.

Two new inputs independently probed the contract:

| Input | Fixture | Evidence | Result |
|---:|---|---|---|
| 11 | New independent eQTL identity-LD panel vs AR(1) GWAS LD | eQTL lambda `0.974438`; explicit eQTL guard; no summary file | PASS |
| 12 | New self-consistent 140-SNP matched-LD locus | GWAS/eQTL lambdas `0.022585, 0.000000`; `rs42 x rs42`, PP.H4=1; summary written | PASS |

Inputs 1–9 reran the complete prior regression set: coloc.abf p12 grid, both shipped SuSiE examples, MHC/chr8 boundaries, real SMR/HEIDI controls, low-power PP.H3 scope, complement-aware harmonisation, current coloc.abf CLI, and the former matched-LD coloc.susie control. All content and output-file assertions passed. All ten shipped R files also parse; see `run/parse_all_r_sources_output.txt`.

## Remaining P1s

- The shared Windows R wrapper intermittently returns exit 139 after output has fully materialized, including expected `stop()` paths. This audit relied on explicit output/file assertions and does not count those statuses as successful exits.
- The documented moloc, eCAVIAR, and PWCoCo alternatives still need isolated-environment execution; their unavailable dependencies are unchanged from the checkpoint.

All runnable scripts, fixture inputs, outputs, and assertions are retained in [`run/`](F:/OpenScience/audits/bio-causal-genomics-colocalization-analysis/run/). The structured result is [`eval_report_bio-causal-genomics-colocalization-analysis_result.json`](F:/OpenScience/audits/bio-causal-genomics-colocalization-analysis/eval_report_bio-causal-genomics-colocalization-analysis_result.json).
