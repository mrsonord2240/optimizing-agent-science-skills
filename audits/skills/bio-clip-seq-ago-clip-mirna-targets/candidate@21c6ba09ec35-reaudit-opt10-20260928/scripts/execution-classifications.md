# Execution classifications

## Executed

- Exact candidate shipped suite: 5/5 tests pass.
- Independent parser/wrapper adversarial harness: 9/9 assertions pass.
- Pinned Hyb `028ab63` official input: two fresh complete two-run wrapper batches (four underlying Hyb runs), 111 valid 16-column rows per run.
- Cross-batch consensus comparison at accepted-id and normalized-assignment level.
- Targeted-Yeo `targeted_miR_umi.py` default on bounded paired FASTQ.
- TargetScan plus/minus exon-spanning projection, release/range failures, and `bedtools intersect -split -s` overlap.

## Static or public-interface only

- Standard AGO peak calling and computational assignment outside the bundled converter.
- miRDB 6 public data and prediction-service descriptions.
- `hybkit` distinction from the Hyb direct-chimera engine.

## Resource-infeasible

- Full human Yeo chimeric-eCLIP CWL workflow without a real library and species-matched repeat/genome STAR indices.

## Biological route unavailable

- HEAP Halo-Ago2 library preparation and orthogonal reporter validation.

## Remote unavailable

- DIANA microT-CDS documented example endpoint (previously returned HTTP 500); not credited as executed.
