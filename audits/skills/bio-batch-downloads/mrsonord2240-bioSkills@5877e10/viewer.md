> **Audit record for `bio-batch-downloads`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@5877e10](https://github.com/mrsonord2240/bioSkills/tree/5877e10e931bd361863c8e1d1feb5a738c8bb0dc/database-access/batch-downloads) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-batch-downloads — Phase 2 final-pass audit

**Result: 92/100 — Production Ready — deployable**

- Source: `mrsonord2240/bioSkills@5877e10e931bd361863c8e1d1feb5a738c8bb0dc:database-access/batch-downloads`
- Worktree: `F:\OpenScience\wt\database-access-batch-downloads`
- Environment: `F:\OpenScience\audit-envs\database-access` (Python, Biopython 1.88, pytest 9.1.1)
- Auditor exception: `auditor_independent: false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`

The pinned source began and ended clean. The final-pass audit executed all required dynamic inputs against the current source; no source files, publication state, or merge state were changed.

| Input | Executed evidence | Result |
|---|---|---|
| Current `batch_by_ids.py` direct/history paths | 6 direct records; 255 posted through EPost | pass |
| Forged WebEnv recovery | 368 records, checkpoint cleared, 3 EFetch calls | pass |
| EPost boundary | 200/201 IDs posted correctly | pass |
| Documented PubMed bulk flow | 1,000/1,000 MEDLINE records with titles (8,768 available) | pass |
| Current `robust_download.py` | 368 FASTA records; 0 CRLF bytes | pass |
| Current Datasets opt-in path | 4 history-server records; SARS-CoV-2 ZIP 22,246 bytes | pass |
| Large-query hard stop | source explicitly rejects EFetch-loop use above 1,000,000 | pass |
| Zero-hit history guard | returns 0 records without fetching | pass |
| 800k decision route | source directs mirror/Datasets consideration above 100,000 | pass |

The source regression suite passed: `7 passed in 3.24s`. The literal documented EDirect pipeline returned three FASTA headers. EDirect emitted transient `SSL_read` unexpected-EOF warnings while HTTP 200 responses completed; the pipeline result remained correct.

Static review scored 95. Dynamic execution scored 90.2 from 31/31 asserted checks; weighted final score is 92. The full machine-readable record is [eval_report_bio-batch-downloads_result.json](F:\OpenScience\audits\bio-batch-downloads\eval_report_bio-batch-downloads_result.json), and the retained phase record is [CHECKPOINT.md](F:\OpenScience\audits\_final_pass\bio-batch-downloads\CHECKPOINT.md).
