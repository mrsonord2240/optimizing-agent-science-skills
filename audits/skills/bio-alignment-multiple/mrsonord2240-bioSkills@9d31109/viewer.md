> **Audit record for `bio-alignment-multiple`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@9d31109](https://github.com/mrsonord2240/bioSkills/tree/9d31109159d4d490ec375d4ae88c9b77570f3840/alignment/multiple-alignment) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-multiple

## Exact-commit re-audit

| Audited source | Current staging source | Re-audited | Result |
|---|---|---|---|
| `966f838b0ba32918310bd223a34f71d78f190560` | `9d31109159d4d490ec375d4ae88c9b77570f3840` | 2026-09-24 | 19/19 focused assertions PASS |

The staging source differs from the audited blob and already includes the four corrective commits for the former P1/P2 findings. No new content change or empty commit was made in this pass.

## Scores

| Dimension | Score |
|---|---:|
| Static quality | 95 / 100 |
| Dynamic execution | 92.1 / 100 |
| Assertions | 32 / 32 PASS |
| Final | **93 / 100 — Production Ready** |

## Exact-commit validation

`runs/exact-commit-9d31109/reaudit_focused.py` verifies the staging SHA and the four corrective commits before reading the skill. It then:

- runs `muscle -align ... -stratified`, yielding 16 EFA blocks / 240 records, and confirms that the obsolete `-super5 -stratified` command is rejected;
- re-runs MAFFT `--auto` boundary fixtures, observing `alg=L` for 90 sequences and `alg=X` for the 150-sequence long-gene case;
- executes the source’s homology/orientation fence on the mixed fixture, flagging exactly one contaminant and all three reverse-strand homologs;
- confirms MAFFT emits three `_R_` headers and that the specialist reference routes exist.

The exact log is `runs/exact-commit-9d31109/reaudit_focused.log`.

## Finding disposition

| Prior finding | Priority | Disposition |
|---|---|---|
| MUSCLE5 ensemble command used unsupported super5 flags | P1 | Fixed and executed |
| MAFFT `--auto` strategy table was wrong | P2 | Fixed and executed |
| Homology/strand pre-flight and `_R_` handling absent | P2 | Fixed and executed |
| Specialist details always loaded | P2 | Fixed and source-checked |

**Remaining P0/P1/P2 findings: none.**
