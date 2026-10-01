> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@2f38178](https://github.com/mrsonord2240/optimized-scientific-skills/tree/2f381782596c6569fe5a8357556856512b7fbb6c/skills/bio-atac-seq-single-cell-atac) match audited candidate `01b8b5025bee5ae72e7c71dd81caf3602744838da3079f205fad44c890b74c68` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-atac-seq-single-cell-atac`**
> - Audited working candidate `01b8b5025bee5ae72e7c71dd81caf3602744838da3079f205fad44c890b74c68`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/single-cell-atac), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-single-cell-atac`** (delta re-audit of the RA-1 fix)
> - Audited working candidate `01b8b5025bee5ae72e7c71dd81caf3602744838da3079f205fad44c890b74c68`; provenance in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/single-cell-atac), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: skill-auditor@1.0 by AIPOCH (MIT). Performed 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not endorsed by the Skill's authors.

# Delta re-audit: RA-1

- Identity verified live: sha256-manifest-v1 `01b8b502...74c68`, 6 files, 38,189 bytes; only `SKILL.md` differs from `d12a77c4...`.
- Diff check: removing the single 179-byte inserted sentence from the new `SKILL.md` reproduces the prior `SKILL.md` hash `920e9abb...` exactly, so the change is only that sentence.
- Numbers: ARC kept-cell blacklist max 0.00405 (pre-QC max 0.00722; 57 of 128,741 peaks overlap the list) matches "max 0.004, near 0, 0.05 cut removes none". ATAC 1.0.1 `singlecell.csv` ratio is 0.177 at most among the 1,472 analysed cells (0.82 across all 5,335 called cells), so "up to 0.18" holds for the analysed set.
- Execution: signac_workflow.R, AMULET and regression surfaces are byte-identical to the certified `d12a77c4` run (reaudit-10x evidence reused); the change is prose only.
- Result: RA-1 closed. Final 89 (static 91, execution average 87.1 reused), assertions 31/31, no veto, no open findings.
- Non-blocking: the sentence does not name the ATAC dataset for the 0.18 figure, and the all-cells maximum is 0.82.
