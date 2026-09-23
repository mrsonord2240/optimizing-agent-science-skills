> **Audit record for `bio-pathway-reactome`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@f52df03](https://github.com/mrsonord2240/bioSkills/tree/f52df03856e4967084ee7010cb81076ac17b64bb/pathway-analysis/reactome-pathways) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-pathway-reactome — final-pass audit

## Verdict: Reject — 55/100

Source: `mrsonord2240/bioSkills@f52df03856e4967084ee7010cb81076ac17b64bb:pathway-analysis/reactome-pathways`.
The source worktree was clean before and after the audit. `auditor_independent` is `false`; this is the final pass described in `CHECKPOINT.md`.

The exact ORA example reached 20 rows, the copied GSEA source reached 54 rows with the planted pathway ranked first when the audit wrapper registered `SerialParam`, and `viewPathway` wrote a local PDF. Those semantic results do not satisfy the execution contract: every process that loaded ReactomePA exited `2816` during teardown. The unmodified GSEA example also spawned an owned 22-worker BiocParallel tree and did not complete; that tree alone was terminated after 50 seconds.

| Route | Semantic evidence | Exit contract |
| --- | --- | --- |
| Package/database load | ReactomePA and >20,000 local PATHID keys | FAIL: 2816 |
| Human ORA | 20 rows, CSV | FAIL: 2816 |
| Exact source ORA | 20 rows | FAIL: 2816 |
| Exact source GSEA default | did not complete | FAIL: owned worker tree |
| Exact source GSEA, serial audit wrapper | 54 rows; planted pathway rank 1 | FAIL: 2816 |
| `viewPathway` | non-empty local PDF | FAIL: 2816 |
| SYMBOL guard | returned `NULL` | FAIL: 2816 |
| Undocumented-organism claim | observed error did not match stated message | FAIL: 2816 |

## Blocking fixes

1. P0: In a fresh private R runtime, identify and repair the ReactomePA/DLL teardown fault; `library(ReactomePA)`, ORA, GSEA and viewPathway must exit 0.
2. P0: Bound the default GSEA backend (serial or deliberately bounded BiocParallel) and prove the shipped example finishes without a growing worker tree.
3. P1: Recheck and correct the undocumented-organism error text after the exit contract is fixed.

Execution provenance, copied source and output files are under `run/phase2_final_f52df03_private_20260923/`. The pre-final-pass report and viewer were archived under `F:\OpenScience\audits\_pre-fix-20260923\bio-pathway-reactome`.
