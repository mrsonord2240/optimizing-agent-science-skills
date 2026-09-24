# bio-workflows-scrnaseq-pipeline fix pass

Commit: 2e36b9b60a6db36a41843cd3bc5f7fcf476e9c15.

Added an executable multi-sample completion: MAD-adaptive QC, Ensembl-name
guard, four declared checkpoints, Harmony integration, pseudobulk DE hand-off,
and propeller differential-abundance hand-off. It also states raw-matrix
requirements for ambient correction.

Exact-commit re-audit exited 0:

~~~text
PASS commit=2e36b9b multi-sample DE/DA checkpoints MAD QC input validation present
~~~

Canonical audit artifacts were updated in F:\OpenScience\audits\bio-workflows-scrnaseq-pipeline.
