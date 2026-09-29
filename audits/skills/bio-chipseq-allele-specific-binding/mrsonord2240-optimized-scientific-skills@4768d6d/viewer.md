> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@4768d6d](https://github.com/mrsonord2240/optimized-scientific-skills/tree/4768d6d40a2ca58b8323aca739c5598b6c5782ff/skills/bio-chipseq-allele-specific-binding) match audited candidate `03415aabaa66de0ef1b747e3fc664dae6d2868e42bf52a2c104d990db5e6057f` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-chipseq-allele-specific-binding`**
> - Audited working candidate `03415aabaa66de0ef1b747e3fc664dae6d2868e42bf52a2c104d990db5e6057f`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/chip-seq/allele-specific-binding), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-chipseq-allele-specific-binding

Generated: 2026-09-28  
Exact candidate: `03415aabaa66de0ef1b747e3fc664dae6d2868e42bf52a2c104d990db5e6057f`

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|---|
| 1 | Canonical | 40 | 58 | 98 | 5/5 | ✅ |
| 2 | Variant A | 34 | 48 | 82 | 5/5 | ❌ Partial, resource-infeasible model uncredited |
| 3 | Edge | 39 | 58 | 97 | 5/5 | ✅ |
| 4 | Variant B | 40 | 59 | 99 | 5/5 | ✅ |
| 5 | Stress | 38 | 58 | 96 | 5/5 | ✅ |

**Execution average:** 94.4 / 100  
**Assertion pass rate:** 25 / 25  
**Static score:** 96 / 100  
**Final score:** 95 / 100 — ⭐ Production Ready

Both veto gates pass. `CBA-009` and `CBA-010` are closed on the exact
candidate. The bounded full BaalChIP model and its actual all-excluded/no-call
terminal publications remain resource-infeasible and receive no execution
credit; AlleleSeq remains external-only and uncredited. Those honest access
classifications are not open product defects.

## Detailed outputs

### Input 1 — Paired-end WASP mapping-bias route

Fresh WASP v0.3.4 execution emitted `input.remap.fq1.gz` and
`input.remap.fq2.gz`, with six records per mate. Four input alignments yielded
four final paired alignments, equal to direct plus remap keeps. A fresh provider
chromosome-22 IMPUTE2/HAPS run reproduced all four expected HDF5 shapes. All
five assertions passed. Evidence: `evidence/wasp-live.tsv` and
`evidence/wasp-hdf5-live.tsv`.

### Input 2 — Cancer BaalChIP correction

Official Bioconductor 3.22 metadata, the BaalChIP 1.36.0 DESCRIPTION and
source, candidate constants, runtime gate, tests, and status output all bind
one R 4.5 contract. Used constructor, correction, getter, and named-report APIs
match the exact source. Fresh measured-RAF and indexed-gDNA preflights passed;
ten invalid-state probes failed with their expected structured codes. The
missing-package model invocation exited nonzero, published no final output,
left no matching partial, and preserved an unrelated sentinel. The exact
source install remains blocked by missing compiled Bioconductor dependencies,
so the full model and terminal publications are partial/resource-infeasible and
uncredited. All five accessible-contract assertions passed. Evidence:
`evidence/baalchip-source-binding.tsv`, `package-install-probe.log`,
`baalchip-runtime-boundary.tsv`, and `run-artifacts/`.

### Input 3 — Exclusion and contract boundaries

Live imprinted-locus and chrX controls each retained the expected two of three
rows. Assembly and contig mismatches failed before model loading. The R helper
suite passed named-list report selection, required columns, structured empty
output, and incompatible-report rejection. All five assertions passed.
Evidence: `evidence/interval-live.tsv` and `evidence/execution.log`.

### Input 4 — Public two-feature RASQUAL cohort

Candidate `prepare` emitted exact 2-by-24 Y/K and 24-by-4 X native-double
binaries. Candidate `run` executed C11orf21 and TSPAN32 once each from the
public chr11 fixture; both rows had valid shape, finite phi, convergence zero,
and finite family p/q values. A repeated output path was refused. All five
assertions passed. Evidence: `evidence/rasqual-binary-contract.tsv` and
`evidence/rasqual-cohort.tsv`.

### Input 5 — AlleleSeq routing boundary

The read-only checkout independently reports
`https://github.com/trgaleev/AlleleSeq2.git` at exact commit
`cfe8acf88989922da841e71238b360f8f57e813a`, matching the candidate's tested
implementation binding. The Rozowsky paper remains a separate canonical-method
citation. Python 2, STAR, Picard, the official `vcf2diploid.jar`, and matching
assets remain unavailable; no partial personalized-genome result was credited.
All five assertions passed. Evidence: `evidence/alleleseq-binding.tsv` and
`evidence/alleleseq-boundary.tsv`.

## Final disposition

`CBA-001` through `CBA-010` are closed. No new findings were opened. No
audit-local repair was attempted, candidate bytes were unchanged, and this
exact identity is candidate-ready for the optimization workflow's later batch
assembly step.
