> **Audit record for `bio-chipseq-allele-specific-binding`**
> - Audited working candidate `944f852224538df92c581ab4a42889202ab10639f54974130f841782f5c90ead`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/chip-seq/allele-specific-binding), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-chipseq-allele-specific-binding

Generated: 2026-09-28  
Exact candidate: `944f852224538df92c581ab4a42889202ab10639f54974130f841782f5c90ead`

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|---|
| 1 | Canonical | 40 | 58 | 98 | 5/5 | ✅ |
| 2 | Variant A | 30 | 45 | 75 | 4/5 | ❌ Partial |
| 3 | Edge | 39 | 58 | 97 | 5/5 | ✅ |
| 4 | Variant B | 40 | 59 | 99 | 5/5 | ✅ |
| 5 | Stress | 35 | 53 | 88 | 4/5 | ✅ with provenance finding |

**Execution average:** 91.4 / 100  
**Assertion pass rate:** 23 / 25  
**Static score:** 92 / 100  
**Final score:** 92 / 100 — ⭐ Production Ready by the strict numeric rubric

The optimization workflow readiness decision is stricter than the numeric
grade: `CBA-009` is an open P1 package/environment contract defect, so this
exact candidate is not yet candidate-ready.

## Detailed outputs

### Input 1 — Paired-end WASP mapping-bias route

Fresh v0.3.4 execution produced the exact mate-specific remap files, six
records in each mate, four input alignments, four remap-kept alignments, and
four final paired alignments. The provider chr22 IMPUTE2/HAPS run also produced
all four expected HDF5 shapes. All five assertions passed. Evidence:
`evidence/wasp-live.tsv` and `evidence/wasp-hdf5-live.tsv`.

### Input 2 — Cancer BaalChIP correction

Measured RAF and indexed-gDNA preflights both passed and recorded their actual
correction source. Ten invalid-state probes returned the expected structured
errors. The missing-package full invocation exited nonzero, published no final
output, left zero matching staging directories, and preserved an unrelated
sentinel. The model remains unexecuted. Four assertions passed; the release
binding failed because BaalChIP 1.38.0 is a Bioconductor 3.23 package, not the
documented 3.22 package. Evidence: `evidence/execution.log`,
`evidence/run-artifacts/`, and `evidence/source-binding-check.tsv`.

### Input 3 — Exclusion and contract boundaries

Live imprinted-locus and chrX controls each retained the expected two of three
rows. Assembly and contig mismatches failed before model loading. The helper
suite passed group-list report selection, required columns, and structured
empty output. All five assertions passed. Evidence:
`evidence/interval-live.tsv` and `evidence/execution.log`.

### Input 4 — Public two-feature RASQUAL cohort

Candidate `prepare` emitted exact 2-by-24 Y/K and 24-by-4 X native-double
binaries. Candidate `run` executed C11orf21 and TSPAN32 once each from the
public chr11 fixture; both rows had valid shape, finite phi, convergence zero,
and finite family p/q values. A repeated output path was refused. All five
assertions passed. Evidence: `evidence/rasqual-binary-contract.tsv` and
`evidence/rasqual-cohort.tsv`.

### Input 5 — AlleleSeq routing boundary

The official legacy runtime remains unavailable, and no partial result was
credited. The Make dry-run and missing prerequisites are recorded. Four
assertions passed; exact checkout provenance failed because the candidate links
one repository while the prepared `cfe8acf` checkout names another origin.
Evidence: `evidence/alleleseq-dryrun-boundary.tsv` and
`evidence/source-binding-check.tsv`.

## Finding disposition

`CBA-001` through `CBA-006` and `CBA-008` are fixed. The source-binding part
of `CBA-007` is reopened as `CBA-009` (P1, BaalChIP release/environment) and
`CBA-010` (P2, exact AlleleSeq repository). Both veto gates pass; no unavailable
component was converted into a live pass.

