> **Audit record for `bio-ncbi-datasets-cli`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@48406b3](https://github.com/mrsonord2240/bioSkills/tree/48406b3c04c59a8e0d2de0664c1d32f6cd8bc683/database-access/ncbi-datasets-cli) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-ncbi-datasets-cli — final-pass Phase 2 result

## Canonical final summary

**Final:** 95/100 — ⭐ Production Ready; deployable: true.

**⭐ 95/100 — Production Ready.** The source at `mrsonord2240/bioSkills@48406b3c04c59a8e0d2de0664c1d32f6cd8bc683:database-access/ncbi-datasets-cli` was clean at audit start and end. Seven explicit formal inputs completed in private audit runtime child processes, with all 16 assertions passing.

| Input | Accepted record | Result |
|---|---|---|
| Source wrapper summary | `run/01_wrapper_summary.execution.json` | E. coli accession parsed |
| Current dataformat fields | `run/08_dataformat_corrected.execution.json` | TSV conversion passes |
| BRCA1 Mammalia orthologs | `run/09_ortholog_corrected.execution.json` | 271 live records |
| Invalid accession guardrail | `run/10_empty_accession_corrected.execution.json` | exit 0, zero records |
| Dehydrated fetch transformation | `run/05_bulk_transform.execution.json` | column 3 paths; no `out=0` |
| Version/catalog check | `run/06_version_and_help.execution.json` | Datasets 18.37.0 fields valid |
| Scope/integrity boundaries | `run/11_scope_corrected.execution.json` | guards present |

All accepted records state `executed: true`, an auditor-owned PID, and `intervention: none`. Early run labels `02`, `03`, `04`, and `07` are retained as non-evidence test-expectation corrections, not source failures; they were neither killed nor otherwise intervened upon.

One P2 documentation correction remains: in this build a nonexistent assembly accession returns exit code zero and **zero JSON-lines**, rather than the literal `{ "total_count": 0 }` payload shown in the Common errors table. The more important operational safeguard—never accepting exit zero without a nonzero result count—is correct and reproduced.

## Canonical final-pass metadata

- Source: `mrsonord2240/bioSkills@48406b3c04c59a8e0d2de0664c1d32f6cd8bc683:database-access/ncbi-datasets-cli`
- `auditor_independent:false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`

## Canonical final-pass metadata

- Source: `mrsonord2240/bioSkills@48406b3c04c59a8e0d2de0664c1d32f6cd8bc683:database-access/ncbi-datasets-cli`
- `auditor_independent: false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`
