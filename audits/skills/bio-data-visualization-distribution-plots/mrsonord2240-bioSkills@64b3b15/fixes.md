# bio-data-visualization-distribution-plots fix log

## 2026-09-23 (final backlog P1/P2)

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Archived gghalves raincloud fails on ggplot2 4.x | P1 | Replaced the required R gghalves route with `ggdist::stat_halfeye`; rebuilt the standalone example around the supported route. | Ran `examples/test_distribution_plots.R` and a copied standalone `raincloud_phd.R` with data-visualization `r.sh`; PDF was 27,314 B. | The Skill names gghalves only to explain why it is not a dependency. |
| SJ blanks a panel when a stratum is tied or constant | P1 | Added `safe_violin_bw()`: test every nonmissing group with `bw.SJ` and choose one panel-wide `nrd0` fallback on failure. | R focused test renders a tied/constant + variable panel with the fallback and checks a nonempty PNG. | Constant strata retain raw points; they do not support a density interpretation. |
| Split violin changes side with a missing cell or tiny group | P1 | Added `prepare_split_violin_data()` requiring an ordered two-level condition factor and omitting clusters without both cells at N >= 30. | R test checks only three complete 40x40 clusters reach `p_split`; split PNG is nonempty. | No arbitrary numeric split was added. |
| Shipped example was a fragment and counted N from another frame | P1 | Rewrote `examples/raincloud_phd.R` as a deterministic standalone workflow building all frames; each plot derives labels from its own nonmissing values. | Direct run from a copied file and focused test passed. | `raincloud.pdf` is written only to the caller's working directory. |
| nrd/nrd0 relationship was reversed | P2 | Corrected the explanation: `nrd` is 1.06/0.9 times `nrd0` and smooths more. | Checked in the R-backed source and focused fallback test. | SJ remains preferred when it is valid. |
| N text snippet lacked `y` | P2 | Replaced it with a `stat_summary` example returning both `y` and a nonmissing-N label; standalone plots use axis labels. | R focused test checks NA-safe local labels. | |
| trim guidance could imply impossible values | P2 | Changed bounded-data advice to `trim = TRUE` or explicit bounds; documented why `trim = FALSE` can extrapolate. | Source review against audit reproducer. | |
| N thresholds disagreed | P2 | Consolidated one decision table: raw points <30, raincloud 30-200, letter-value >=201, density >1000; split cells require >=30. | R examples match their declared ranges. | |
| Python warnings / bandwidth limits and unseeded jitter | P2 | Documented ptitprince Scott-only limitation and matplotlib recheck, used `hue` + `legend=False` for seaborn boxenplot, and seeded R jitter. | `examples/test_python_distribution_plots.py` via `py.sh`: raincloud 21,721 B and boxen 12,210 B; `py_compile` passed. | Python RainCloud ran on ptitprince 0.3.1 / matplotlib 3.11.2. |
| usage guide repeated operational rules | P2 | Reduced `usage-guide.md` to overview, prerequisites, prompts, and related Skills; operational content now lives only in `SKILL.md`. | Grep/source review. | Deleted repeated N table, tips, and agent-workflow list; their canonical home is `SKILL.md`. |

`SKILL.md` is 194 lines after the correction, so a references split is not required. No complete 15+ line runnable block remains in `SKILL.md`: the executable end-to-end workflow is the standalone example, and its focused R/Python tests sit beside it.
