Environment: Windows Python 3.12.13 via `py.sh` (matplotlib 3.11.2, seaborn 0.13.2, numpy 2.5.3, pandas 3.0.6, cmcrameri); fingerprint sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 over `snapshots/lane1_versions.txt`; pdffonts/pdftoppm 26.07.0 in WSL `dv-cli`. Input: public airway DESeq2 results; synthetic data in the shipped script.

| Surface | Classification | Evidence |
|---|---|---|
| `scripts/matplotlib_phd.py` (all seven sections) | executed | `scripts/m1_phd_check.py`, `logs/m1_phd_check.log`, `logs/pdffonts_phd.log`; PDFs rendered and opened (`out/phd/*_pdf.png`) |
| SKILL.md seaborn recipe on real data, seaborn.objects | executed | `scripts/m2_real_volcano.py`, `logs/m2_real_volcano.log`; `out/vol/` opened |
| SKILL.md Standard Setup + Saving block, chart-recipes.md blocks, failure-modes.md claims | executed | `scripts/m3_recipes.py`, `m3b_type3_probe.py`, `m3c_type3_bisect.py`, logs; `out/rec/` opened |
| EPS transparency warning (tooling lead) | executed, did not reproduce on the Skill's own recipes | `logs/m3_recipes.log` last lines |
| usage-guide.md tips | static-only (restate SKILL.md) | n/a |
