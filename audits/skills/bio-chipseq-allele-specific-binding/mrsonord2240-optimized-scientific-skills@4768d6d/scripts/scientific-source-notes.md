# Scientific source and execution notes

## Exact bindings

- WASP v0.3.4 checkout `f980683cff5638660a966ff0d7c69598bc056e98` produced the documented paired remap files and expected provider HDF5 shapes.
- RASQUAL checkout `5aa553cf1b6501cf7ecd61a5efb34f7f20d354c6` executed the public bundled chr11 fixture through the candidate cohort driver.
- The official Bioconductor 3.22 index names BaalChIP 1.36.0. Its exact source tar has SHA-256 `f3d033913484173f5ae6bcdb62d199f122736e634b3861c8f165b32c475a227e`; DESCRIPTION records `RELEASE_3_22` and `Bioconductor 3.22`. Inspected source matches every candidate-used constructor, correction, getter and report interface.
- The tested AlleleSeq implementation is `https://github.com/trgaleev/AlleleSeq2.git` at `cfe8acf88989922da841e71238b360f8f57e813a`. The Rozowsky paper is retained separately as the canonical method source.

## Honest access and resource boundaries

- BaalChIP, Rsamtools, GenomicAlignments and rtracklayer are absent from the prepared R library. A fresh exact 1.36.0 source-install probe fails on those dependencies; retained tooling records the prior bounded Rhtslib compile limit. Source inspection, version gates, helper tests, preflights and atomic cleanup are credited; the statistical model is not.
- The full BaalChIP model, actual all-excluded terminal publication and actual no-call terminal publication remain unexecuted and uncredited. The candidate's helper-level structured-empty contract did execute.
- AlleleSeq lacks Python 2, STAR, Picard, the official `vcf2diploid.jar`, and matching legacy assets. The Make plan is inspection-only and no personalized-genome execution is claimed.
- All public and synthetic fixtures contain no private or patient data.

## Warning interpretation

The official WASP provider HDF5 smoke reports SNPs present in only one of its
paired IMPUTE2 inputs. The resulting `/chr22` shapes match the provider
baseline exactly; the warnings are retained in `evidence/execution.log` rather
than suppressed or treated as candidate output.
