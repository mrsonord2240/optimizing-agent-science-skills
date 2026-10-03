Environment: Windows R 4.4.3 via `r.sh` (DESeq2 1.46.0, apeglm 1.28.0, ashr 2.2.63, EnhancedVolcano 1.24.0, ggplot2 4.0.3, ggrepel 0.9.8) and Python 3.12.13 via `py.sh` (matplotlib 3.11.2, adjustText 1.4.0, sanbomics 0.1.0 isolated under `py-extra/sanbomics`); fingerprint sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 over `snapshots/lane1_versions.txt`; pdffonts 26.07.0 in WSL `dv-cli`. Input: public airway dataset, `public-data/derived/airway_dds_condition.rds` (29,391 genes).

| Surface | Classification | Evidence |
|---|---|---|
| `scripts/volcano_phd.R` (lfcShrink, volcano, MA, cairo_pdf, EnhancedVolcano) | executed | `scripts/v1_phd.R`, `logs/v1_phd.log`, `logs/pdffonts_phd.log`; figures `out/phd/` opened |
| `scripts/volcano_plot.R` `volcano_plot()` | executed | same run; `out/phd/volcano_plot_fn.png` opened |
| lfcShrink apeglm / ashr / svalue / contrast claims, shrunken vs MLE | executed | `logs/v1_phd.log` |
| EnhancedVolcano colours and selectLab gotcha | executed | `logs/v1_phd.log`; `out/phd/enhancedvolcano_skill.png` opened |
| `scripts/ma_plot.py`, adjustText volcano | executed | `scripts/v2_python.py`, `logs/v2_python.log`; `out/py/` opened |
| `sanbomics.tools.volcano` (SKILL.md) | executed, failed (does not exist; import fails) | `logs/v2_python.log`; source grep of `tools.py` |
| edgeR `glmTreat`, ggbreak, plotMA (SKILL.md/failure-modes mentions) | static-only (exercised by the tooling smoke, not re-run here; plotMA PNG written) | n/a |
