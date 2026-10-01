> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@2f38178](https://github.com/mrsonord2240/optimized-scientific-skills/tree/2f381782596c6569fe5a8357556856512b7fbb6c/skills/bio-atac-seq-nucleosome-positioning) match audited candidate `2aa4d73b30023a6d14d690fa0e02f3a8b32a563d15bd445c24e257cb0e0ad18b` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-atac-seq-nucleosome-positioning`**
> - Audited working candidate `2aa4d73b30023a6d14d690fa0e02f3a8b32a563d15bd445c24e257cb0e0ad18b`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/nucleosome-positioning), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-nucleosome-positioning`**
> - Audited working candidate `2aa4d73b30023a6d14d690fa0e02f3a8b32a563d15bd445c24e257cb0e0ad18b`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/nucleosome-positioning), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Delta re-audit viewer (delta-cat2): bio-atac-seq-nucleosome-positioning

Candidate `sha256-manifest-v1 2aa4d73b30023a6d14d690fa0e02f3a8b32a563d15bd445c24e257cb0e0ad18b` (7 files, 34,808 bytes). Previous run: delta-cat-20260930 (`c8ef5320...`), score 85. Independent auditor; no Skill bytes edited.

**Final 85 (Production Ready), static 86, execution 85.0 (carried), assertions 22/24, no veto, no open P0. Decision: candidate-ready.**

## Delta verified

Relative to delta-cat, only `scripts/nucleosome_analysis.R` changed (logs/delta2_diff.log). The change is the two-line comment above the summary; no code changed. The script parses in the lane R env with `PARSE OK`, 4 expressions (logs/parse_check.log).

The new comment reads: "Counts use unshifted fragment widths; the exported NFR/mono BAMs are split from the Tn5-shifted fragments (9 bp shorter), so their read counts differ from these." It is accurate against the delta-cat evidence (logs/class_mechanism_from_delta-cat.log):
- The unshifted recount equals the summary counts (130,774 and 67,604).
- The recount with widths minus 9 bp equals the export counts exactly (141,651 and 64,579).

The comment leaves out the right-closed window boundaries. They play a minor part in the difference, and the statement is still true.

## Findings (all P2)

| ID | Status |
|---|---|
| NUCPOS-017 export vs summary counts | Resolved (cause documented correctly; fix option "state the difference in a script comment") |
| NUCPOS-016 NRL plateau ambiguity | Open, unchanged |
| NUCPOS-006 NucleoATAC third-party edit | Open, accepted workaround |
| NUCPOS-015 scPrinter untested | Open, deferred |

## Re-scored

Static: reliability 10 -> 11 (85 -> 86). Input 3's count-agreement assertion is behavioural and remains FAIL. Final = 0.4 x 86 + 0.6 x 85.0 = 85.4.

Scripts: `scripts/identity_diff.py`, `delta2_diff.py`, `parse_check.sh`, `build_delta2.py`. Logs: `logs/`.
