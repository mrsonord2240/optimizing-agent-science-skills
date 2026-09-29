# Re-audit inputs

All fixtures and outputs are labelled synthetic when they do not use an official public input. The live Hyb case uses the pinned public test reads and hOH7 cache. The executed assertions and observed outcomes are summarized in `viewer.md` and retained under `evidence/`.

1. **Canonical Hyb repeatability:** execute the shipped wrapper twice from clean output directories on `runtime/hyb/data/fastq/testdata.txt`, named database hOH7, two replicates, and one fixed run id. Compare raw assignments, support records, five structured outputs, and stdout after its initial wall-clock timestamp line.
2. **Wrapper boundaries:** run with a path containing spaces and a literal wildcard; repeat against existing output; use a controlled failing Hyb executable returning 42; verify preservation and staging cleanup.
3. **Parser edge:** use 16-column fixtures with miRNA-first and target-first segments, matched expression provenance, missing and discordant read IDs, a malformed Hyb field count, and an invalid expression header.
4. **TargetScan variant:** map a plus- and a minus-strand site across two UTR exons; overlap with same- and opposite-strand peaks; supply a wrong release and an out-of-range site.
5. **Targeted UMI stress:** synthetic paired gzip FASTQ with an R2 prefix that supports explicit 9-nt and 10-nt cases; omit the length and test zero, non-integer, blank library, blank protocol, and too-short R2.
6. **Expression failure case:** two agreeing valid Hyb rows, `expression_value=NaN`, matched TPM provenance, and an expression threshold of 100. Expected scientific contract: reject the non-finite value or exclude it before consensus publication. Observed: it is accepted.
7. **Auxiliary bounded routes:** synthetic paired FASTQ for the documented total-Yeo UMI-tools plus cutadapt path; synthetic BAM with one soft-clipped and one unclipped record for the SAM diagnostic. These fixtures do not stand in for a real Yeo or AGO experiment.
