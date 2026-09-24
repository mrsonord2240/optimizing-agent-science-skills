> **Audit record for `bio-proteomics-dia-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@0e23cf7](https://github.com/mrsonord2240/bioSkills/tree/0e23cf7a1fc896bc332d5729ee93ae2b8d5dc291/proteomics/dia-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Skill Audit Viewer — `bio-proteomics-dia-analysis` (final pass)

**Source:** `mrsonord2240/bioSkills@0e23cf7a1fc896bc332d5729ee93ae2b8d5dc291:proteomics/dia-analysis`  
**Final score:** **92/100 — Production Ready** · Deployable: **yes**

Final-pass exception: `auditor_independent: false` — final pass: fixed and audited under one brief, see CHECKPOINT.md

All prior P0/P1/P2 findings are closed. The committed skill now uses a DIA-NN 2.x-compatible two-stage predicted-library route; directs matrix/report discrepancies to the installed run log instead of claiming a fixed direction; names required third-party-library fragment annotations; lists current outputs; keeps the runnable route in one file; and ships a synthetic Parquet fixture.

| Evidence set | Result |
|---|---|
| Archived synthetic report and public DIA-NN 2.6.1 report/log | PASS — exact source filter produced 887x8 and 4375x3 matrices, no `-Inf`; public matrix rows (4440) exceeded globally filtered report rows (4375). |
| Archived 600-run synthetic stress report | PASS — 2000x600, no `FALSE*`, no `-Inf`. |
| Archived staggered data / installed msconvert | PASS — demultiplex command exited 0. |
| Archived EasyPQP and public library-based output | PASS — installed help checked; library report produced 771x3 after global filter. |
| Fresh fixture and command-contract checks | PASS — global-only low-confidence group removed; Stage 1 had no raw files and Stage 2 used the produced library. |

The score is intentionally not higher: this pass did not repeat the prior multi-hour public raw DIA-NN search. It re-filtered the retained real 2.6.1 output and log with the exact committed source block, and the fresh shell test validates argument/stage structure with a stub rather than representing a new raw-data search.

Raw evidence: `run/finalpass_20260924/01_verify_exact_source.py`, `01_verify_exact_source.out.txt`, `02_rerun_archived_tools.py`, `02_rerun_archived_tools.out.txt`, and `easypqp_library_help.txt`.
