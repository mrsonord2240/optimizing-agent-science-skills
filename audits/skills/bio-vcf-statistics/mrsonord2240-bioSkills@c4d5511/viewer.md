> **Audit record for `bio-vcf-statistics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c4d5511](https://github.com/mrsonord2240/bioSkills/tree/c4d5511fe2830349a9d65609495018ed862ead58/variant-calling/vcf-statistics) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-vcf-statistics — exact-commit final audit

| Field | Result |
|---|---|
| Source | `mrsonord2240/bioSkills@c4d5511fe2830349a9d65609495018ed862ead58:variant-calling/vcf-statistics` |
| Audit method | Focused exact-commit re-audit; auditor independence is `false` |
| Assertions | **15/15 passed** |
| Final | **94 / 100 — ⭐ Production Ready** |
| Deployable | `true`; no veto override |

## What changed

The per-sample AD quick check previously accepted `0/1`, `0|1`, and `1|0`, but omitted the valid unphased ordering `1/0`. The Skill and usage guide now use `^(0[\/|]1|1[\/|]0)$`. They also state that this is a biallelic-only quick check: multi-allelic AD must be parsed explicitly.

## Exact evidence

`run/exact-commit-c4d5511/reaudit_focused.sh` first records its pinned SHA and checks the source contract, then uses the synthetic eight-sample cohort. The coordinator-side Windows Git check verified the isolated worktree's exact SHA and clean state before the WSL execution.

- `bcftools stats -s -` produced 8 PSC rows; Ti/Tv extraction returned **1.43**.
- Strict `FILTER=PASS` counted **0** raw records while `FILTER=.,PASS` counted **361**, matching the documented distinction.
- A deliberately orientation-mixed stream contained **372** `1/0` genotypes. The shipped regex retained all **747/747** biallelic heterozygotes.
- The documented `INFO/ExcessHet > 54.69` route identified the **6** planted excess-heterozygosity artifacts.

The complete command and log are retained beside this report. peddy and somalier are not claimed as newly executed in this focused pass; their human/build/site-panel requirements are tested here as documented operational boundaries.

No open P0, P1, or P2 findings remain.
