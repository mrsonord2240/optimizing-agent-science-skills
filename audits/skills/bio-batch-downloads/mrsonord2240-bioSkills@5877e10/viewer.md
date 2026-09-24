> **Audit record for `bio-batch-downloads`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@5877e10](https://github.com/mrsonord2240/bioSkills/tree/5877e10e931bd361863c8e1d1feb5a738c8bb0dc/database-access/batch-downloads) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-batch-downloads — Phase 2 structured re-audit

## Canonical final summary

**Final:** 92/100 — ⭐ Production Ready; deployable: true.

**Result: 92/100 — Production Ready — deployable**

- Source: `mrsonord2240/bioSkills@5877e10e931bd361863c8e1d1feb5a738c8bb0dc:database-access/batch-downloads`
- Environment: `F:\OpenScience\audit-envs\database-access` (Biopython 1.88, pytest 9.1.1)
- `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

The re-audit ran from an audit-owned `git archive` of the exact source tip. The source worktree was not used or modified. Fresh live runs completed `batch_by_ids.py` (6 direct records; 200+55 EPost submission), `batch_fasta.py` (4 INS RefSeq mRNAs), and `robust_download.py` (368 BRCA1 records). The exact copied `test_robust_download.py` passed 7/7 in 3.14 seconds.

All nine required inputs have explicit executed evidence, scores, and three assertions in the machine-readable report. The previous artifacts remain preserved under `run/phase2_reaudit_20260923_1740/previous_incomplete_*`.

Evidence: `run/phase2_reaudit_20260923_1740/{pytest.log,batch_by_ids.py.log,batch_fasta.py.log,robust_download.py.log,structured_results.json}`.
auditor_independent: false
