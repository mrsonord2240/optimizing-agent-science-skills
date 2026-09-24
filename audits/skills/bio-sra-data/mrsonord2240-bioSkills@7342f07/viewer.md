> **Audit record for `bio-sra-data`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@7342f07](https://github.com/mrsonord2240/bioSkills/tree/7342f0782d258eba329460f76a8c7dea35abc7cb/database-access/sra-data) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@2.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-sra-data — Phase 2 final-pass audit

## Canonical final summary

**Final:** 91/100 — ⭐ Production Ready; deployable: true.

**Decision: ⭐ Production Ready (91/100).** The exact source `mrsonord2240/bioSkills@7342f0782d258eba329460f76a8c7dea35abc7cb:database-access/sra-data` passes all vetoes and is deployable.

| Audit metadata | Value |
|---|---|
| Evaluated | 2026-09-24 |
| Category / mode / complexity | Data Analysis / D / Complex |
| Dynamic inputs | 7, all executed |
| Auditor-independent | false |
| Required note | final pass: fixed and audited under one brief, see CHECKPOINT.md |
| Runtime | Audit-owned `/home/sci/sra-audit-20260923`: SRA Tools 3.4.1, EDirect 26.0, pysradb 2.5.1, Biopython 1.88 |
| Artifacts | `F:/OpenScience/audits/bio-sra-data/run/phase2_20260923/safety_final_tip` |

The source was clean before the repair. The narrow safety fix was committed as `7342f07`; the full final-pass run then used that exact tip. The superseded canonical report was archived in `F:/OpenScience/audits/_pre-fix-20260924-safety/bio-sra-data/`.

## Veto gates

| Gate | Result | Evidence |
|---|---|---|
| T1 stability | PASS | All seven final-pass vectors completed in the pinned private runtime. |
| T2 contract | PASS | Required files/frontmatter and declared data-access scope are present. |
| T3 determinism | PASS | The fixed source completed the repeat private-runtime run. |
| T4 security | PASS | Strict run-ID validation precedes paths/cleanup; owned stages and no-clobber publication are tested. |
| M1 scientific integrity | PASS | No unsupported scientific claims or fabricated references. |
| M2 practice boundaries | PASS | Controlled/missing-field data remains a file-free stop boundary. |
| M3 methodological ground | PASS | Live ENA output was MD5-verified; fallback is explicit and validated. |
| M4 code usability | PASS | Live run discovery, EDirect syntax, direct Toolkit fallback, and STRIDES fallback completed. |

## Dynamic execution

| # | Path | Result | Executed evidence |
|---:|---|---|---|
| 1 | Live ENA batch `ERR10419835` | ✅ 92 | Both mates downloaded and both MD5 checks passed. `outputs/input1_ena_live.stdout.txt` |
| 2 | `download_single.sh ERR10419835` | ✅ 90 | Toolkit reference failure remained staged/cleaned; ENA fallback produced two verified FASTQs. `outputs/input2_sra_toolkit.stdout.txt` |
| 3 | `pysradb_resolve.py GSE110009` | ✅ 92 | Resolved 74 SRRs. `outputs/input3_pysradb.*` |
| 4 | `find_sra_runs.py` | ✅ 92 | Completed live runinfo parsing: 5 BioProject, 506 RNA-Seq, 74 GSE runs. `outputs/input4_find_runs.stdout.txt` |
| 5 | Valid controlled-style missing-field guard | ✅ 91 | `ERR99999999` recorded as failed and produced no FASTQ. `outputs/input5_controlled_guard.stdout.txt` |
| 6 | `prefetch_large.sh ERR10419835` | ✅ 90 | No AWS CLI; owned prefetch stage safely fell back to two verified ENA FASTQs. `outputs/input6_strides_fallback.stdout.txt` |
| 7 | `efetch -db sra -id 8 -format runinfo` | ✅ 92 | Exact command rerun returned usable runinfo with exit 0. `commands/rerun_input7_edirect_format_runinfo.sh`; `outputs/input7_edirect_format_runinfo.{command,stdout,stderr,exit}.txt` |

Supplemental controls passed: the direct-script controlled fallback exited nonzero with no output, and the shipped safety test rejected `..`, `ERR/123`, and `--max-size`; it retained an existing destination and a dangling symlink while cleaning its owned stage.

The retained [final-vector manifest](run/phase2_20260923/safety_final_tip/commands/final_vector_manifest.md) maps every scored route to its exact final-tip evidence. The sole P2 recommendation is a Toolkit dependency-resolution preflight: the private Toolkit cannot resolve ERR10419835's normalized-reference dependency before attempting retrieval, while the staged ENA fallback completes safely.

## Safety repair delivered

- All direct, STRIDES, and batch run inputs must match uppercase `SRR`/`ERR`/`DRR` plus digits. Traversal, separators, and option-like values are rejected before path construction or cleanup.
- Toolkit cache and temporary FASTQ output are marked owned directories below `out_dir`; only those paths are cleaned.
- The public ENA fallback verifies MD5 through `download_batch.sh`, then uses no-clobber hard-link publication. Existing files and dangling symlinks are refused rather than replaced.
- `find_sra_runs.py` remains fixed with bytes decoding, CSV parsing, and the correct GSE-to-SRP-to-SRR route; the EDirect instruction remains `-format runinfo`.

## Scores

| Static | Dynamic | Final |
|---:|---:|---:|
| 90/100 | 91.3/100 | **91/100 — Production Ready** |

The seven totals sum to 639, so the dynamic average is 91.3. Assertion evidence is 27/28: EDirect returned usable output with exit 0 but recorded a post-response `curl (56)` transport warning.

## Canonical final-pass metadata

- Source: `mrsonord2240/bioSkills@7342f0782d258eba329460f76a8c7dea35abc7cb:database-access/sra-data`
- `auditor_independent:false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`

## Canonical final-pass metadata

- Source: `mrsonord2240/bioSkills@7342f0782d258eba329460f76a8c7dea35abc7cb:database-access/sra-data`
- `auditor_independent: false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`
