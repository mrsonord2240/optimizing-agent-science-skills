> **Audit record for `bio-sra-data`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@1ef54e5](https://github.com/mrsonord2240/bioSkills/tree/1ef54e50ff0b2afbd4405b666e79793667dba5c0/database-access/sra-data) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@2.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-sra-data — Phase 2 final-pass audit

**Decision: ⛔ Reject (59/100).** The exact source `mrsonord2240/bioSkills@1ef54e50ff0b2afbd4405b666e79793667dba5c0:database-access/sra-data` is not deployable. Both the Skill stability veto and Research code-usability veto fail.

| Audit metadata | Value |
|---|---|
| Evaluated | 2026-09-23 |
| Category / mode / complexity | Data Analysis / D / Complex |
| Dynamic inputs | 7, all executed |
| Auditor-independent | false |
| Required note | final pass: fixed and audited under one brief, see CHECKPOINT.md |
| Runtime | Audit-owned `/home/sci/sra-audit-20260923`: SRA Tools 3.4.1, EDirect 26.0, pysradb 2.5.1, Biopython 1.88 |
| Artifacts | `F:/OpenScience/audits/bio-sra-data/run/phase2_20260923` |

The source tree was confirmed clean at the required tip before and after testing; no source file was edited. The previous canonical report was preserved in `F:/OpenScience/audits/_pre-fix-20260923/bio-sra-data/` before this report was written.

## Veto gates

| Gate | Result | Evidence |
|---|---|---|
| T1 stability | **FAIL** | Three of seven documented dynamic routes reproducibly fail: direct SRA conversion, STRIDES fallback, and `find_sra_runs.py`. |
| T2 contract | PASS | Required files/frontmatter and declared data-access scope are present. |
| T3 determinism | PASS | Outputs and exit behavior were reproducible in an audit-owned pinned environment. |
| T4 security | PASS | No secrets, arbitrary execution, or controlled-access bypass was found. |
| M1 scientific integrity | PASS | No unsupported scientific claims or fabricated references. |
| M2 practice boundaries | PASS | No clinical recommendation; controlled-access case stops safely. |
| M3 methodological ground | PASS | Live ENA download verifies MD5 and the missing-field guard prevents false success. |
| M4 code usability | **FAIL** | `find_sra_runs.py` crashes on bytes/text handling; the direct toolkit route cannot complete FASTQ conversion for the tested public accession. |

## Dynamic execution

| # | Documented path | Result | Executed evidence |
|---:|---|---|---|
| 1 | `examples/download_batch.sh ERR10419835` | ✅ 92 | Live ENA download of both mates; both MD5 checks passed. `outputs/input1_ena_live.stdout.txt` |
| 2 | `examples/download_single.sh ERR10419835` | ❌ 20 | Exit 3. SRA Tools 3.4.1 selected normalized format and could not resolve `NC_000913.2`; no FASTQs. `outputs/input2_sra_toolkit.*` |
| 3 | `scripts/pysradb_resolve.py GSE110009` | ✅ 92 | Resolved 74 SRRs. `outputs/input3_pysradb.*` |
| 4 | `examples/find_sra_runs.py` | ❌ 20 | `TypeError: a bytes-like object is required, not 'str'` at `split('\\n')`. `outputs/input4_find_runs.stderr.txt` |
| 5 | Controlled-access/missing-field branch | ✅ 88 | Safe nonzero result, no FASTQs, failed accession recorded. The accepted standalone recheck is `outputs/input5_controlled_guard_recheck.stdout.txt`. |
| 6 | `examples/prefetch_large.sh ERR10419835` fallback | ❌ 30 | No AWS CLI, took documented prefetch fallback, then the same unresolved reference failure; exit 3. `outputs/input6_strides_fallback.*` |
| 7 | `efetch -db sra -id 8 -rettype runinfo` | ❌ 20 | Exact documentation emits `Unrecognized option -rettype`. Audit control `-format runinfo` returned runinfo, proving a syntax defect. `outputs/input7_edirect*` |

All seven listed inputs were executed. A first controlled-fixture invocation had a harness-usage error and is explicitly excluded; the standalone recheck above is the accepted evidence.

## Required corrective work

1. **P0 — Fix `find_sra_runs.py`.** Normalize `handle.read()` to text before CSV splitting and verify the script against live SRA runinfo using a pinned Biopython version.
2. **P0 — Repair or explicitly reroute the direct SRA path.** In a clean cache, prove the documented command sequence completes `prefetch`, `vdb-validate`, and `fasterq-dump` for a public accession under its pinned SRA Tools version. If normalized-format/reference dependencies remain unsupported, detect that condition and direct users to the already verified ENA route.
3. **P1 — Correct EDirect syntax.** Replace `-rettype runinfo` with verified `-format runinfo` and retain a simple success/output check.

## Scores

| Static | Dynamic | Final |
|---:|---:|---:|
| 65/100 | 54.3/100 | **59/100 — Reject** |

The numeric score does not override the vetoes.
