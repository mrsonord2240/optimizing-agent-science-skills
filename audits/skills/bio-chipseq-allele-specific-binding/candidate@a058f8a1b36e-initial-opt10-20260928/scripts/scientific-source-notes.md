# Scientific and API source notes

## BaalChIP 1.38.0 official source

The prepared official source tar has SHA-256
`a0068181223d6b70865f8dabc7fc8e09bc763867a49f0b1503c12046380251a3`.
The following contracts are directly visible in that source:

- `R/BaalChIP-class.R:15-33` requires `samplesheet` to be a TSV filename
  with `group_name`, `target`, `replicate_number`, `bam_name`, and `bed_name`;
  `hets` tables require `ID`, `CHROM`, `POS`, `REF`, `ALT`, and optionally
  `RAF`.
- `R/BaalChIP-checks.R:17-47` calls `read.delim(samplesheet)` and validates
  those exact sample-sheet columns. The candidate instead passes an in-memory
  data frame with incompatible column names.
- `R/BaalChIP-methods.R:58-82` calls `dirname(samplesheet)` while checking
  heterozygous-table files. A data frame reaches a base-R type error.
- `R/allASBbias.R:143-199` uses a `RAF` column or group-named gDNA BAMs for
  relative-allele-frequency correction. If neither exists, `RAFcorrection`
  substitutes 0.5 for every variant. No detached CNV-BED argument exists.
- `R/BaalChIP-methods.R:548-549` confirms `getASB` uses `Iter`,
  `RMcorrection`, and `RAFcorrection` in this release.
- `R/BaalChIP-methods.R:755-764` shows `BaalChIP.report` returns a named list
  of per-group data frames, not one data frame.

The candidate's `cnvs <- 'HCC1395_ASCAT_cnvs.bed'` is never consumed. Its
heterozygous table has `AF`, not `RAF`, and lacks the required `ID`. Its report
code applies data-frame indexing directly to the returned list. These are
contract observations, not claims of a live full-package run: BaalChIP runtime
remained `RESOURCE_INFEASIBLE_BOUNDED` after the prepared install ceiling.

## WASP 0.3.4

The prepared live paired-end run at official commit
`f980683cff5638660a966ff0d7c69598bc056e98` emits separate
`input.remap.fq1.gz` and `input.remap.fq2.gz` files. Both mates must be remapped
with the original paired-end settings. The candidate command names a single
`step1.remap.fq.gz` file, passes only `-1`, and supplies no `-2` mate.

## RASQUAL

The prepared official commit `5aa553cf1b6501cf7ecd61a5efb34f7f20d354c6`
produces a finite 25-column result on the bundled C11orf21 example with
`phi=0.520004` and convergence status `0`. The candidate documents the live
single-feature flags accurately, but does not supply binary-input construction,
feature iteration, result parsing, or cohort multiplicity control.

## AlleleSeq2

Official commit `cfe8acf88989922da841e71238b360f8f57e813a` was available for a
Make dry run. The candidate Make command leaves `READS_R1`, `READS_R2`, and
`PREFIX` unset; the plan therefore contains blank input/output names. The
candidate's separate maternal/paternal Bowtie2 SAMs are not passed to that Make
target, which plans a STAR alignment. Full execution is
`UNAVAILABLE_FULL_TOOLCHAIN` because Python 2, STAR, Picard, and the official
`vcf2diploid` archive are unavailable. No unofficial substitute was used.
