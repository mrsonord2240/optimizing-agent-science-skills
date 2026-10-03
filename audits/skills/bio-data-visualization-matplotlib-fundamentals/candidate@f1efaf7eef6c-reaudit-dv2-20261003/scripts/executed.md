Environment: Windows Python 3.12.13 via `py.sh` (MPLBACKEND=Agg), matplotlib 3.11.2, seaborn 0.13.2, numpy 2.5.3, pandas 3.0.6, cmcrameri (metadata 1.10), PIL 12.3.0; fingerprint sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 over `snapshots/lane1_versions.txt` (re-hashed identical); poppler (`pdffonts`, `pdftoppm`) in WSL `dv-cli`. Inputs: staged airway DESeq2 results; the script's own seeded synthetic data. Tool inventory: `TOOLS-bio-data-visualization-matplotlib-fundamentals.md` sha256 a4a13bf881d7db3a8a26cc45fe8aef405ca9d60316b9187db89bdc9eba35d83c. Skill bytes were not edited; scripts ran with the output directory as working directory.

| Surface | Classification | Evidence |
|---|---|---|
| `scripts/matplotlib_phd.py` (5 PDFs, sizes, fonts, text, colours, determinism) | executed | `scripts/m1_phd.py`, `logs/m1_phd.log`, `scripts/pdf_render_m.sh`, `logs/pdffonts_phd.log`; figures opened |
| seaborn.objects legend section 7 (MPL-007), stress variants, public route | executed | `scripts/m2_legend_stress.py`, `scripts/m2b_axes_probe.py`, `logs/m2_legend_stress.log`, `logs/m2b_axes_probe.log`; renders opened |
| SKILL.md python blocks (5), Saving block, colour binding on airway data | executed | `scripts/m3_skill_blocks.py`, `logs/m3_skill_blocks.log` |
| `references/chart-recipes.md` (2 blocks, 11 fragments) incl. Tick frequency (MPL-008) | executed | `scripts/staged_recipes.py`, `logs/staged_recipes.log` |
| `references/failure-modes.md` (22 checks) incl. tight_layout entry (MPL-009) | executed | `scripts/staged_failure_modes.py`, `logs/staged_failure_modes.log` |
| API/layout/EPS/rasterization claims in SKILL.md and usage-guide | executed | `scripts/m5_claims.py`, `logs/m5_claims.log` |
| First-loop regressions MPL-005, MPL-006 | executed | `scripts/m6_regress.py`, `logs/m6_regress.log` |
| Pandas4Warning origin (seaborn internals, not the Skill) | executed | `scripts/m1b_warn_origin.py`, `logs/m1b_warn_origin.log`: raised inside seaborn `Plot.plot()` via `pd.concat(copy=)` on pandas 3.0.6, hidden by Python's default filters, no effect on output |
| `usage-guide.md` | static-only | prose, prompts and the install line (covers every import of the script) |

Reused (not rerun): none. Notes: staged_recipes.py and staged_failure_modes.py are the staged tool copies of the fixer's scripts, read and run unchanged; m3_skill_blocks.py is adapted from the dv1 re-audit script. Failure-modes numeric claim 63x vs measured 66x from unrounded sizes (1.52 MB vs 23.2 KB) is within rounding of the stated 1.5 MB and 24 KB.
