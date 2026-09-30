> **Audit record for `bio-atac-seq-differential-accessibility`**
> - Audited working candidate `dd1e7bda67b8992abed303553522a42d73f5af9fb5c69bbb955f3886a5463238`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/differential-accessibility), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Re-audit viewer: bio-atac-seq-differential-accessibility

Candidate: sha256-manifest-v1 `dd1e7bda67b8992abed303553522a42d73f5af9fb5c69bbb955f3886a5463238` (5 files, 46279 bytes), verified live before and after execution. Origin GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/differential-accessibility. Prior audit 890c5349... scored 64, rejected on M4 (P0 DAC-001).

**Decision: candidate-ready. Final 86 (Production Ready), static 85, execution average 86.8, Layer 1 35-36, Layer 2 50-54, assertions 28/29 (96.6%), no veto, no open P0.**

## Prior findings retested

| ID | Result | Evidence |
|---|---|---|
| DAC-001 P0 SVA | Fixed. SV enters `~SV1 + Condition`; skill table equals my own svaseq+DESeq2 fit (max dLFC 0); results change vs `~Condition` (1372 -> 822 sites); --sva=2/4/9 capped to 1 SV | logs/sva_probe.log, logs/sva*.log |
| DAC-002 CLI args | Fixed. `mypfx_*`, FDR .01, LFC 3 -> 212 sites; unknown flag and non-numeric threshold rc 1 | logs/args.log, badarg.log, badnum.log |
| DAC-003 normalization default | Fixed. Default lib/full; native gives RLE/RiP, 1096 sites | logs/default.log, native.log |
| DAC-004 TSS plot | Fixed. Annotation PDF has 2 pages, rendered | png/default_annoplot-2.png |
| DAC-005 zero hits | Fixed in default and --sva; warning, empty BEDs, rc 0 | logs/null.log, svanull.log |
| DAC-006 labels | Fixed. Actionable error; --case/--control reproduces 1181 | logs/labels.log, labels_ok.log |
| DAC-007 edgeR/design | Fixed. edgeR 1341 sites; design 1020; RUVseq and spike-in recipe-only (SVA/RUV recipe executed: nsv 1, padj<0.05 1764) | logs/edger.log, design.log, recipe_sva.log |
| DAC-008 plot thresholds | Fixed. MA/volcano titles match counts | png/default_diagnostics-2.png, png/sva_diagnostics-2/3.png |
| DAC-009 txdb | `none` executed; non-human TxDb still untested (P2) | logs/notxdb.log |
| DAC-010 design docs | Fixed. `~Batch + Condition` fails with "Invalid factors in design: Batch" | logs/designbad.log |

## Judgement on known limits

SVA mode skipping the blacklist filter and heatmap is an acceptable limit only if documented; it is documented only in the script header, so it is filed P2 (R-001, R-002), not a defect blocking readiness. Blacklist impact on this data is 0 of 2260 intervals.

## Findings (all P2)

- R-001 SVA mode skips blacklist filter with no warning.
- R-002 SVA-mode limits (direct DESeq2, ignores --method/--design, no heatmap) only in the script header; method-reference says "inside DiffBind".
- R-003 Threshold semantics differ: DiffBind fold is an lfcThreshold test (338 sites with |Fold|>=1 excluded; min reported 1.22) vs hard filter in SVA mode.
- R-004 Non-human TxDb untested; no caution that SVA on 2 vs 2 (1 SV, r=0.53 with Condition) may absorb signal.

## Coverage

Executed on real ENCODE chr1:1-30Mb (GM12878 vs K562, 2 vs 2): default, native, positional args, edgeR, design, --sva (1/2/4), zero-hit default and SVA, labels error/override, --txdb=none, bad flag, bad number, bad design, SVA recipe. Figures (PCA, MA, volcano, heatmap, annotation pie and TSS distance) rasterised with poppler and inspected for default and SVA modes. RUVseq and spike-in: recipe-only, not counted as executed. Non-human TxDb: static-only.

Scripts: `scripts/` (run_cli.sh, runall.sh, sva_probe.R, base_probe.R, fold_probe.R, recipe_sva.R, check_outputs.py, render.sh, build_report.py, validate_report.py). Logs: `logs/`. Figures: `png/`. Note: the python K562-only count in check_outputs.py dedups identical coordinates (1252); the R count is 2133; hit counts are computed identically across modes.
