# Deferred and unavailable surfaces

- A full Yeo biological workflow needs a real library, mature-miRNA data, and species-matched repeat/genome STAR indices. Only bounded synthetic total-route checks ran.
- HEAP reproduction is a wet-lab Halo-Ago2 mouse-model route and needs biological material.
- The documented DIANA microT-CDS example endpoint returned HTTP 500; the service surface was not treated as executed.
- Full AGO peak calling is not bundled as a runnable end-to-end pipeline and requires assay-specific inputs and an explicitly selected peak caller.
- The targeted Yeo source still conflicts between 9-nt prose and a 10-nt executable default. The local extractor requires a declared protocol length; it does not decide which applies to a library.
- Hyb stdout includes a timestamp as its first line. The two fresh workflow pairs differed only on that line; structured output and subsequent stdout were identical.

Initial isolated test invocation of the secondary-surface helper lacked the environment's `conda-env/bin` in PATH and stopped before running its first command. The helper was corrected to prepend the already prepared environment path and rerun; the fresh TargetScan and secondary-route evidence recorded in this audit passed. No package was installed or environment changed.
