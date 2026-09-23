> **Audit record for `bio-blast-searches`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@d8a2300](https://github.com/mrsonord2240/bioSkills/tree/d8a2300a9a90869eccd13a5867d22d00709c6e6c/database-access/blast-searches) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-blast-searches — Phase 2 final-pass audit

**Result: 78/100 — Limited Release — not deployable pending live-service revalidation**

- Source: `mrsonord2240/bioSkills@d8a2300a9a90869eccd13a5867d22d00709c6e6c:database-access/blast-searches`
- Worktree: `F:\OpenScience\wt\database-access-blast-searches`
- Environment: `F:\OpenScience\audit-envs\database-access` (Biopython 1.88)
- Auditor exception: `auditor_independent: false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`

The pinned source began and ended clean. All seven audit inputs were explicitly executed. Fresh live remote-BLAST success is blocked by the NCBI BLAST CGI at audit time, so this is not a source-code rejection and it is not a production-ready approval.

| Input | Execution evidence | Result |
|---|---|---|
| `examples/basic_blast.py` | Entered current `NCBIWWW.qblast()`, then `RemoteDisconnected` | external failure |
| `examples/blastp_filtered.py` | Entered current Swiss-Prot request, then same error | external failure |
| PAM30 short-peptide reference | Literal current block executed with controlled requester; verified PAM30, word=2, gapcosts `9 1`, CBS=3 | pass, network-free |
| E-value decision | Current formula/database-size/bit-score decision checks | pass |
| Megablast and XML path | Current fixture parsed: 33 alignments, `NM_000518` top; fixed literal contract checked; live request did not complete in 300 s | partial/external |
| 200-CDS boundary | Current source routes >50 to local BLAST and >1000 to DIAMOND/MMseqs2 | pass |
| RID client and defline guard | Missing-defline rejection passed; valid HBB RID run received same CGI connection close | partial/external |

The failure was reproduced outside the source code: direct `curl` to `https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&RID=INVALID` reported an abrupt server close. The same condition affected Biopython `qblast()` and the stdlib RID client, so it is recorded as an external availability/path blocker rather than attributed to a particular implementation.

Static review scored 94. Dynamic execution scored 67.4 from 20/28 asserted checks; weighted final score is 78. The research code-usability veto is **BLOCKED**, therefore `deployable` is false until the four live routes can be rerun successfully. See [eval_report_bio-blast-searches_result.json](F:\OpenScience\audits\bio-blast-searches\eval_report_bio-blast-searches_result.json) and [CHECKPOINT.md](F:\OpenScience\audits\_final_pass\bio-blast-searches\CHECKPOINT.md).
