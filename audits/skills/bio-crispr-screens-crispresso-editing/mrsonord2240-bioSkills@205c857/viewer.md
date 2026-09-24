> **Audit record for `bio-crispr-screens-crispresso-editing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@205c857](https://github.com/mrsonord2240/bioSkills/tree/205c8574b66f30fb04cb2fdbd0464f6d37a70920/crispr-screens/crispresso-editing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-crispresso-editing

## Canonical final summary

**Final:** 93/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@205c8574b66f30fb04cb2fdbd0464f6d37a70920:crispr-screens/crispresso-editing`

## Result

**93/100 — Production Ready — deployable: true.** Both veto gates passed. This final-pass audit intentionally records `auditor_independent: false` and `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

| Input | Test | Basic | Specialized | Total | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Cas9 canonical | 38 | 57 | 95 | 4/4 | ✅ |
| 2 | CBE window | 38 | 57 | 95 | 4/4 | ✅ |
| 3 | Wrong locus | 35 | 54 | 89 | 4/4 | ✅ |
| 4 | Pooled pilot | 38 | 58 | 96 | 4/4 | ✅ |
| 5 | Batch + compare | 38 | 58 | 96 | 4/4 | ✅ |
| 6 | Parser + WGS | 38 | 58 | 96 | 4/4 | ✅ |
| 7 | Default BE | 38 | 57 | 95 | 4/4 | ✅ |
| 8 | Shipped shell syntax | 36 | 57 | 93 | 4/4 | ✅ |
| 9 | ABE window | 38 | 57 | 95 | 4/4 | ✅ |
| 10 | Prime editor | 38 | 57 | 95 | 4/4 | ✅ |
| 11 | Docker recovery probes | 38 | 58 | 96 | 4/4 | ✅ |

Execution average: **94.6/100**. Assertion pass rate: **44/44**. Static score: **90/100**.

## Fresh execution evidence

- `run/probe_docker_recovery_20260923.ps1` passed new `hello-world` and `CRISPResso --version` probes; version was 2.3.4.
- `run/fresh_20260923_complete/validation.json` passed all material checks: Cas9 Modified% 26.38297872, pooled rows 2, batch rows 2, WGS rows 2, 94.0% parser mapping, and prime-edit reference/prime/scaffold rows.
- All dynamic input records in the JSON set `executed: true` with an explicit `execution_note`.
- The unmodified source parser self-test, Python compilation, and shipped shell syntax check passed.

## Material observation

For a deliberately wrong amplicon, CRISPResso2 2.3.4 emitted `ERROR: No alignments were found` and wrote no quantification result, but its container exited 0. This does not invalidate the error route, but the Skill must not promise exit code 1. It is the sole P2.

## Archive

The rejected Docker-blocked canonical report and viewer were copied before replacement to `F:\OpenScience\audits\_pre-fix-20260923\bio-crispr-screens-crispresso-editing\rejected-docker-blocked-20260923\`.
