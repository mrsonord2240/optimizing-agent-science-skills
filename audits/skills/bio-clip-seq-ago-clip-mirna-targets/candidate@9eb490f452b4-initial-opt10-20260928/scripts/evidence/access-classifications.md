# Live interface and access classifications (2026-09-28)

## Hyb

- **Classification:** public and locally executable; current public source,
  not a versioned package release.
- **Authority:** `https://github.com/gkudla/hyb`, pinned current `master` at
  `028ab6371ce793ca5e86f475fce1f2cc6ad3c677`.
- **Interface:** the executable is a GNU Make program. Live help requires a
  goal, for example `hyb help`; analysis syntax is
  `hyb detect in=<FASTQ> db=<database-name> qc=none align=bowtie2 type=mim`.
  `db` names a prebuilt index beneath `HYB_HOME/data/db`; it is not an
  arbitrary combined FASTA pathname.
- **Version behavior:** `hyb --version` exits zero but reports GNU Make 4.4.1,
  not a Hyb semantic version. The repository has no tags. Use the Git commit
  as the executable identity.
- **Real smoke:** the repository's `testdata.txt` against its hOH7 reference
  produced 111 unambiguous `type=mim` rows. The output name was
  `official_test_comp_hOH7_hybrids_ua.hyb` and every row had 16 fields.
  Fields 4 and 10 contain the two RNA identities; field 3 is folding energy,
  field 5 is the first segment's read-coordinate start.
- **Aligner requirement:** Bowtie2 is directly required for `align=bowtie2`;
  the tested index was built by Bowtie2 2.5.4 from 57,726 public reference
  sequences. The live Makefile also supports `blastall`, `blastn`, `blat`,
  `pblat`, and pre-aligned BLAST input, each with its own index/tool contract.

## Yeo Lab chimeric eCLIP

- **Classification:** public executable workflow source; full human workflow
  is resource-infeasible for this bounded tooling pass, not access-restricted.
- **Authority:** `https://github.com/YeoLab/chim-eCLIP`, pinned current `main`
  at `75fe74e90e6e4ca670a5af76836d80db09bdbcb1` (MIT; repository not archived).
- **Interface:** CWL and wrapper workflows under `wf/`, with named total,
  targeted, single-end, trim-only, and candidate-only routes. The repository
  README documents exact UMI/cutadapt, Bowtie, STAR, samtools, and dedup
  outputs. The current pipeline does not use the candidate's Hyb wrapper.
- **Execution boundary:** a complete run requires library-specific reads,
  mature-miRNA reference, repeat and genome STAR indices, annotation files,
  and the workflow's supporting executables. The Yeo eCLIP documentation
  recommends roughly 200 GB of free space for human inputs, indices, and
  intermediates. No gated asset was bypassed; exact UMI/cutadapt semantics
  were instead live-smoked with bounded fixtures.

## HEAP

- **Classification:** public experimental method and public datasets, but no
  standalone product called a "HEAP pipeline" was identified.
- **Authority:** Li et al., 2020, DOI `10.1016/j.molcel.2020.05.009`, with data
  at GEO `GSE139349`. The paper routes peak calling to CLIPanalyze at
  `https://bitbucket.org/leslielab/clipanalyze`.
- **Interface/access:** HEAP requires Halo-Ago2 biological material, including
  the engineered mouse system for the in-vivo route. CLIPanalyze remains
  publicly fetchable at commit `fcab2db41b0c29be54d1adc917b55394e448f6fe`
  (2019-01-15) and is an R package for CLIP-seq analysis; it is not a HEAP-only
  command-line workflow. Biological library preparation was not executable in
  this software-only tooling pass.

## pyHyb / Hyb-format Python tooling

- **Classification:** advertised `pyHyb 0.4+` surface is unavailable or
  misidentified.
- `python -m pip index versions pyHyb` returned no matching distribution on
  2026-09-28. The public GitHub repository named `KalEktor/PyHyb` is an
  unrelated hybrid-material builder.
- The relevant modern Hyb-format package is `hybkit`, whose latest public PyPI
  release is 0.3.6, not pyHyb 0.4+. It was classified only and not substituted
  silently for the advertised dependency.

## Target prediction resources

- **TargetScanHuman 8.0 — public/downloadable, data-only in this Skill.** The
  official 8,305,482-byte prediction archive was downloaded and parsed. It
  contains transcript/UTR-relative sites, so it cannot be used as the
  candidate's genomic BED input without a versioned coordinate conversion.
- **miRDB 6.0 — public/downloadable, data/web surface.** The official download
  page still identifies release 6.0 (June 2019). The prediction archive at
  `https://mirdb.org/download/miRDB_v6.0_prediction_result.txt.gz` advertised
  59,483,982 bytes and supports byte ranges. No local CLI is supplied or
  invoked by the Skill.
- **DIANA microT-CDS — public documentation/web service, live endpoint failed.**
  The official DIANA help page documents the v5 REST query syntax, but its
  documented example endpoint returned HTTP 500 during this pass. This is a
  remote documentation-only surface for the candidate; no credentials or
  bypass were attempted.

## User action and rerun

No user action is needed for Hyb, preprocessing, TargetScan download, miRDB
download, or local overlap checks. A full Yeo chimeric-eCLIP run needs a real
library plus species-matched STAR/repeat indices and a much larger disposable
run allocation. HEAP requires suitable Halo-Ago2 experimental material. DIANA
must return to service, or the user must select a versioned downloadable
prediction set, before it can be tested as a live remote prediction surface.
