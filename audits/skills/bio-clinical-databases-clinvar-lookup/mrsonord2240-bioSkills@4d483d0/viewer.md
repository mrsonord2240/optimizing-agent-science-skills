> **Audit record for `bio-clinical-databases-clinvar-lookup`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@4d483d0](https://github.com/mrsonord2240/bioSkills/tree/4d483d0451fcd60cb3ab62dfa4cd047ec59b3615/clinical-databases/clinvar-lookup) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-clinical-databases-clinvar-lookup

Re-audited 2026-09-24 against exact current staging `main` source: `mrsonord2240/bioSkills@4d483d0451fcd60cb3ab62dfa4cd047ec59b3615:clinical-databases/clinvar-lookup`.

No source change or commit was needed in this pass. The current source already contains each remedy from the last audit, and the focused executable checks passed at that exact SHA.

| Measure | Prior audit | Exact-current re-audit |
|---|---:|---:|
| Static score | 82/100 | 89/100 |
| Dynamic execution | 85.1/100 | 88.0/100 |
| Assertion reconciliation | 25/27 | 27/27 |
| Final | 84 — Limited Release | **88 — Production Ready** |
| Open P0/P1/P2 | 0/0/3 | **0/0/0** |

## Exact-byte comparison

- `fc575c5` makes `batch_resolve_to_car_then_clinvar()` retain rows for non-400 Registry failures and preserves the service `message`.
- `905893a` adds participant-derived variant governance and `NCBI_API_KEY` guidance.
- `f26acc9` relocates pushback, reconciliation, and tripartite-schema tables from `SKILL.md` to `usage-guide.md`.

No stale implementation contradicted those changes, and no further P0/P1/P2 was found.

## Executed validation

- Live ClinVar: variation `17661` returned `VCV000017661`, `Pathogenic`, `reviewed by expert panel`.
- Live ClinGen Allele Registry: `NC_000017.11:g.43106487A>C` resolved to `CA001182`.
- Batch of two valid HGVS strings plus invalid `NC_000013.14:g.32316461G>A` produced all three rows; the invalid row retained `Unknown reference: NC_000013.14` rather than aborting the batch.
- Conflict parsing classified `Likely_pathogenic(2)|Likely_benign(1)` as `severe`; VCF command contract retained `INFO/ONCDN,INFO/SCIDN`.
- Live `clinvar_search_gene('BRCA1', pathogenic_only=True)` returned count `4725`, `4725` IDs, all unique; `max_ids=1200` returned its documented whole last page of `1500`.
- Source assertions confirmed consent/IRB, `NCBI_API_KEY`, and progressive-disclosure guidance. `py_compile` and `git diff --check` passed.

The assertion total is reconciled transparently: 25 assertions already passing in the archived full audit remain on byte-compared unchanged behavior; the two formerly failing batch assertions were executed again at the exact current SHA.

## Evidence

- [Prior report archive](re-audit-20260924/pre-current/eval_report_bio-clinical-databases-clinvar-lookup_result.json)
- [Focused validation](re-audit-20260924/run-focused/focused_validation.out)
- [Pagination validation](re-audit-20260924/run-focused/pagination_validation.out)
- [Canonical machine report](eval_report_bio-clinical-databases-clinvar-lookup_result.json)

## Remaining findings

None at P0, P1, or P2. The skill validator still warns about pre-existing legacy frontmatter keys (`author`, `primary_tool`, `tool_type`); this is not a source regression or a release-blocking finding.
