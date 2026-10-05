> **Audit record for `bio-workflows-crispr-screen-pipeline`**
> - Audited working candidate `e609525649bd5394ec66676a9025250ab8c27db23039968d44c6dfeb0c872c81`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/workflows/crispr-screen-pipeline), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-04 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Delta re-audit: bio-workflows-crispr-screen-pipeline (reaudit-delta-001)

Candidate `e609525649bd5394ec66676a9025250ab8c27db23039968d44c6dfeb0c872c81` over certified `05e557c86e77` (reaudit-002, candidate-ready, 88). Mode: delta. `skill_preflight --offline --shape` PASS, 19 files.

## Diff against certified bytes

sha256 manifest diff: exactly two files differ, `scripts/qc.py` and `routes/qc.md`. Every other file is byte-identical. Both changes match the brief and fix-003 edits.json (qc.py: default pattern gains `(?<=\d)R\d+(?=_)`, docstring, verdict block, exit; qc.md: F-16 prose). Route table, route names and script arguments unchanged, so the routing check was not rerun; routing evidence carries from reaudit-002.

## Executed (shared venv, qc.py as in routes/qc.md)

| Case | Verdict | Exit |
|---|---|---|
| Real HAP1, `plasmid=HAP1_T0` | QC FAIL, Pearson 0.789 | 1 |
| Real A375, default pattern (A375_C902R1_P1D14 names) | groups to one condition, Pearson 0.780, QC FAIL | 1 |
| Ungroupable names (Pl, Alpha, Beta, Gamma) | replicate Pearson NOT CHECKED, QC INCOMPLETE | 1 |
| Same, `min_depth=600` (gate fails too) | QC FAIL (FAIL wins over INCOMPLETE) | 1 |
| Same, `pattern=^(Alpha\|Beta\|Gamma)$` | Pearson 0.985, QC PASS | 0 |
| Old-default names: `_r1`, `_rep1`, `_A/_B/_C`, `_1/_2/_3`, `T18A/B/C` (QC-passing table) | each groups 3 samples, Pearson 0.985, QC PASS | 0 |

Logs: `oldnames.log` and the run root. Old-default names were checked on the resampled QC-passing HAP1 table with column names changed.

## Statements checked

- routes/qc.md "QC INCOMPLETE (exit 1): rerun with pattern=" matches qc.py behaviour.
- "0.8, the MAGeCK-VISPR guideline" matches the Li 2015 Table 1 value verified in reaudit-002; "0.85 comfortable" is gone.
- Outlier advice is conditional; the real HAP1 and A375 pairs (0.776/0.782/0.808; 0.767/0.781/0.792) have no clear outlier, so the report-as-failed branch applies.
- qc.py docstring and the route's grouping sentence still list the old patterns; the route sentence does not mention the new `R<n>` rule (cosmetic, not a defect: the INCOMPLETE guard covers any miss).

## Dispositions

| ID | Disposition |
|---|---|
| N-01 P1 | Resolved. |
| F-16 P2 | Resolved. |
| F-10, F-11, F-15 residue | Unchanged, open P2, none blocks readiness. |

No new findings. Scores: static 90 (functional 11, agent usability 15 re-scored; the rest carried), execution average 88.9, Layer 1 35.4, Layer 2 53.4, assertions 28/29 (96.6%), final 89. Readiness: candidate-ready.
