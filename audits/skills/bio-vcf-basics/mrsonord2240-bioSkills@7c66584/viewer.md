> **Audit record for `bio-vcf-basics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@7c66584](https://github.com/mrsonord2240/bioSkills/tree/7c665843f733a0833f21fe95a7c7199376159059/variant-calling/vcf-basics) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-vcf-basics

**95/100 — ⭐ Production Ready — deployable: true.** Exact audited source: `7c665843f733a0833f21fe95a7c7199376159059` in isolated worktree `agent/finalpass-bio-vcf-basics-20260924`.

Final-pass declaration: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`. This is correction-and-regression evidence, not independent acceptance evidence.

## Corrections at the audited tip

- The Python viewer now prints a valid `QUAL=0` as `0.0`, while retaining `.` for a missing QUAL.
- PL/GL and GQ prose now distinguishes likelihood scaling from caller-dependent GQ derivation; it does not instruct agents to reconstruct GQ universally.
- Header guidance now distinguishes portable-VCF recommendations from BCF's required dictionaries.
- The Common Errors row includes the current bcftools 1.24 plain-gzip index diagnostic.

## Exact execution

Environment: bcftools 1.24; cyvcf2 0.34.0; WSL `science`. All archival data are synthetic. The reproducible runner is `runs/finalpass_20260924/run_archived_inputs.sh`; fresh cases are in `runs/finalpass_20260924/fresh_cases.py`.

| Input | Result |
|---|---|
| Archived 1 — view/query | Header table works; 8 SNPs, 3 indels, 11 total; shipped viewer executed. |
| Archived 2 — AB and confidence | AD-derived AB and eight high-QUAL / low-GQ S7 sites reproduced. |
| Archived 3 — missingness | SYN_S6: 76/361 no-calls; wrong reference imputation max AF bias 0.125; 2812/2812 caller PL/GQ checks agree. |
| Archived 4 — gVCF | Three `<NON_REF>` END blocks plus exactly one `N_ALT>1` candidate site; joint-genotyping boundary retained. |
| Archived 5 — convert/index/write | BCF and cyvcf2 agree on 32 regional records; plain gzip reports it cannot be usefully indexed; Writer keeps 350/361 QUAL>30 records. |
| Fresh 1 — QUAL zero | Viewer prints `QUAL=0.0` for a valid zero and `QUAL=.` only for missing. |
| Fresh 2 — caller fields | GL `[-0.8,0,-1.2]` maps to PL `[8,0,12]`; a distinct emitted GQ=99 remains a caller value, not a forced PL reconstruction. |

`py_compile` and `git diff --check main...HEAD` passed. All 28 assertions passed. Static score: 92/100; execution score: 97/100; weighted final: **95/100**. No open P0, P1, or P2 correction items remain. A later documentation pass may choose to split the dense core guide, but that is not an audit defect.
