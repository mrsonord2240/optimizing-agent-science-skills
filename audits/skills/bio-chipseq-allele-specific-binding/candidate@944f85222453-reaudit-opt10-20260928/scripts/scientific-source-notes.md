# Scientific source and execution notes

## Exact bindings that passed

- WASP v0.3.4 checkout `f980683cff5638660a966ff0d7c69598bc056e98` produced the documented paired remap files and the expected provider HDF5 shapes.
- RASQUAL checkout `5aa553cf1b6501cf7ecd61a5efb34f7f20d354c6` executed the public bundled chr11 fixture through the candidate cohort driver.
- BaalChIP source version 1.38.0, SHA-256 `a0068181223d6b70865f8dabc7fc8e09bc763867a49f0b1503c12046380251a3`, supports the inspected constructor, correction, and report contracts. No statistical-model execution is claimed.

## Open source-identity defects

The exact BaalChIP `DESCRIPTION` says `git_branch: RELEASE_3_23` and
`Repository: Bioconductor 3.23`. The candidate instead calls version 1.38.0 a
Bioconductor 3.22 contract, while the prepared library contains
`BiocVersion 3.22.0`. This is not a cosmetic citation issue: the documented
`BiocManager::install()` route and the runner's strict 1.38.0 version check do
not describe one reproducible package universe.

The candidate's claim-level table links `gersteinlab/AlleleSeq`, but the exact
prepared checkout for `cfe8acf88989922da841e71238b360f8f57e813a` has origin
`https://github.com/trgaleev/AlleleSeq2.git`. The scientific paper may remain a
canonical method citation; the tested implementation needs its own exact link.

## Honest restricted and resource boundaries

- `BaalChIP` and `rtracklayer` were independently absent from the prepared R library. Retained bounded installation evidence records the Rhtslib compilation failure and timeout; this re-audit hashes that evidence and credits only source inspection, candidate contracts, preflights, and atomic cleanup.
- The full BaalChIP model, live imprinted/blacklist/chrX terminal branch, actual no-variant terminal publication, and actual no-call terminal publication remain unexecuted.
- AlleleSeq lacks Python 2, STAR, Picard, the official `vcf2diploid.jar`, and matching legacy assets. The Make plan was dry-run only and received no personalized-genome execution credit.
- All public/synthetic fixtures contain no private or patient data.

