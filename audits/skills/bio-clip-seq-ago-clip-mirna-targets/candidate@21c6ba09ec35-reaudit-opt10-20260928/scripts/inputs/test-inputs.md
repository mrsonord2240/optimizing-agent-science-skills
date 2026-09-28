# Re-audit test inputs

1. Canonical: run the exact current-Hyb wrapper twice as two independent two-replicate batches on pinned official input and compare accepted direct-target content, not only counts.
2. Variant A: challenge space/literal-glob paths, overwrite refusal, failing replacement, status 42 propagation, prior-output preservation, and staging cleanup.
3. Edge: exercise both 16-column RNA orientations, expression provenance, missing-versus-different assignment reasons, malformed row width, and malformed expression header.
4. Variant B: project plus/minus exon-spanning TargetScan sites to BED12, run `-split -s`, and reject release mismatch and out-of-range coordinates.
5. Stress: reconcile total versus targeted Yeo UMI layouts and classify Hyb, Yeo, HEAP, TargetScan, miRDB, DIANA, and standard AGO surfaces without overclaiming execution.
