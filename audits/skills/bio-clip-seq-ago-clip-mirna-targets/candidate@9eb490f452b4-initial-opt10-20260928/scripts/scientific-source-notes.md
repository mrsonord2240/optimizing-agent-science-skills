# Scientific and interface source notes

- Current public Hyb was audited at
  `028ab6371ce793ca5e86f475fce1f2cc6ad3c677`. Its executable is a GNU Make
  program; `hyb --version` reports GNU Make, so the Git commit is the portable
  identity. `db` resolves a prebuilt database beneath `HYB_HOME/data/db`.
- Two independent runs on committed official test data produced 111 valid
  16-field records each. Fields 4 and 10 are RNA identifiers and may contain
  microRNA or mRNA in either order. Field 3 is energy and field 5 is a
  coordinate.
- Yeo Lab chim-eCLIP source at
  `75fe74e90e6e4ca670a5af76836d80db09bdbcb1` is public CWL/wrapper software
  with library-specific preprocessing. Its complete human route was classified
  resource-infeasible for this bounded audit, not access-restricted.
- HEAP is Li et al. 2020, DOI `10.1016/j.molcel.2020.05.009`, with public GEO
  `GSE139349` data and CLIPanalyze source. Halo-Ago2 biological material is not
  reproducible in a software-only audit.
- Official TargetScanHuman 8 predictions use transcript and UTR-relative
  coordinates. A genomic overlap requires a versioned transcript-to-genome
  mapping and strand validation.
- `pyHyb` has no matching Python package distribution as of 2026-09-28;
  `hybkit` 0.3.6 is related software but was not silently substituted.
- miRDB 6.0 remains a public data download. DIANA documentation was reachable,
  but its documented example endpoint returned HTTP 500 and was classified
  documentation-only for this pass.

