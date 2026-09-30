# bio-atac-seq-differential-accessibility fix pass - 2026-09-30

`use_sva=TRUE` crashed on 4 samples and the surrogate variables never entered the model. They now do (`~SV1 + Condition`), matching an independent fit, and results change as expected (1,372 to 822 sites). The CLI honours its arguments, edgeR and `--design` ship in the script, and the default normalization matches the docs. SVA mode skips the blacklist filter and heatmap.

- Final candidate audit: `audits/skills/bio-atac-seq-differential-accessibility/candidate@dd1e7bda67b8-reaudit-run`
- Result: **86/100, Production Ready**; no open P0.
- Candidate identity: `dd1e7bda67b8992abed303553522a42d73f5af9fb5c69bbb955f3886a5463238`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
