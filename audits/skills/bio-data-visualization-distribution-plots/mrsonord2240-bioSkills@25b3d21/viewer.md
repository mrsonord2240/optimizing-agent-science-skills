> **Audit record for `bio-data-visualization-distribution-plots`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@25b3d21](https://github.com/mrsonord2240/bioSkills/tree/25b3d2162f76de9b1d0b5d98533bf76f7c970b05/data-visualization/distribution-plots) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-distribution-plots

Generated: 2026-09-23 · rendered from `report.json` by `tools/render_viewer.py`.

> This viewer is **generated from the audit report**, not written by the auditor. It restates the report's own recorded scores, notes and assertions and adds nothing to them. Where a hand-written viewer would argue from the runs, this one points at the scripts in [scripts/](scripts/) instead.

Source: `mrsonord2240/bioSkills@25b3d2162f76de9b1d0b5d98533bf76f7c970b05:data-visualization/distribution-plots`
Audit type: final-pass re-audit of the exact fixed commit
Category: Data Analysis · Execution mode: A · Complexity: Moderate · N = 7 · Executed: None

## What the Skill claims to do

Plot per-group distributions of continuous data using boxplots, violins, beeswarms, quasirandom jitter, and ggdist raincloud plots with sample-size honesty (Weissgerber 2015), KDE-bandwidth awareness, and N-aware encoding choices.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 57 | **94** | 4/4 | yes | ✅ |
| 2 | Variant A | 36 | 55 | **91** | 4/4 | yes | ✅ |
| 3 | Edge | 37 | 57 | **94** | 4/4 | yes | ✅ |
| 4 | Variant B | 35 | 55 | **90** | 4/4 | yes | ✅ |
| 5 | Stress | 38 | 57 | **95** | 4/4 | yes | ✅ |
| 6 | Adversarial | 37 | 57 | **94** | 4/4 | yes | ✅ |
| 7 | Scope Boundary | 37 | 57 | **94** | 4/4 | yes | ✅ |

**Execution Average: 93.1 / 100** · **Assertion Pass Rate: 28/28**

**Static: 93/100** · Static weighted 37.2 + dynamic weighted 55.9 = **93.1/100** → ⭐ Production Ready, deployable.

---

## Veto gates

### Skill veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| stability | PASS |  |
| contract | PASS |  |
| determinism | PASS |  |
| security | PASS |  |

### Research veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| scientific integrity | PASS | The corrected nrd/nrd0 relation, bounded-data trim advice, N ranges, and cited visualization claims agree with the executed checks; no unsupported clinical claim is made. |
| practice boundaries | PASS | This is a research visualization Skill and does not diagnose, prescribe, or triage individuals. |
| methodological ground | PASS | The decision table preserves raw observations at small N, treats KDE as bandwidth-sensitive, and now rejects incomplete or low-N split-violin cells instead of giving a misleading density. |
| code usability | PASS | The shipped R and Python tests, standalone R example, current R blocks, split guards, and PDF export all executed on the documented current stack. |

## Static score

| Category | Score | Note |
|---|---|---|
| functional suitability | 12/12 | The decision table, current ggdist raincloud, N annotations, current Python routes, and guarded split-violin workflow cover the stated task and ran. |
| reliability | 11/12 | Panel-wide SJ-to-nrd0 fallback, finite-value filtering, ordered two-level validation, and per-cell eligibility prevent the formerly silent failure modes; an empty eligible set is returned safely. |
| performance context | 7/8 | The 194-line operational Skill is concise, with executable end-to-end material in the shipped example and a lean usage guide. |
| agent usability | 14/16 | Version compatibility, a single N decision table, explicit failure remedies, deterministic jitter, and local-N labels provide actionable guidance; users must still choose a suitable encoding for their question. |
| human usability | 8/8 | The trigger, prerequisites, prompt examples, colors, and N-aware choices are clear and scoped to distribution visualization. |
| security | 12/12 | No network, credential, shell, or destructive-data route is introduced; example output is a caller-local PDF. |
| maintainability | 11/12 | The standalone deterministic example and focused R/Python tests are shipped beside the instructions; reusable guards use explicit column arguments. |
| agent specific | 18/20 | The description is specific, APIs and versions are named, archived gghalves is explicitly excluded, and the documented ptitprince compatibility limit is surfaced. |

## Input 1 — Canonical: Current R box, guarded violin, quasirandom, and ggdist raincloud

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 57/60 · **Total 94/100**
- Execution: run/exact-source/test_distribution_plots.R and run/reaudit_i1_r_current.R via data-visualization r.sh.
- Finding: The exact shipped R test and fresh current-stack blocks passed; the generated PNG was nonempty (27,301 B).

| Assertion | Result | Evidence |
|---|---|---|
| The shipped focused R test completes against the exact copied example | PASS | It printed its PASS line on ggplot2 4.0.3. |
| Current inline box+jitter draws every raw observation | PASS | ggplot_build returned 80 point rows for 80 input observations. |
| The guarded violin and quasirandom examples build nonempty layers | PASS | Both layer checks were nonempty; quasirandom returned 80 rows. |
| The current R render is a usable file | PASS | reaudit_i1_current_r.png was 27,301 B. |

## Input 2 — Variant A: Current Python RainCloud and seaborn boxenplot

- Status: ✅ COMPLETED · Basic 36/40 · Specialized 55/60 · **Total 91/100**
- Execution: run/reaudit_i2_python_current.py via data-visualization py.sh.
- Finding: The exact shipped Python smoke test and fresh calls passed; both PNGs were nonempty and the palette-only seaborn warning was absent.

| Assertion | Result | Evidence |
|---|---|---|
| The shipped Python test produces a RainCloud and a boxenplot | PASS | It reported 21,552 B and 12,210 B PNGs. |
| The documented current Python RainCloud call renders | PASS | Fresh RainCloud PNG was 21,711 B. |
| The hue-based seaborn boxenplot renders without the palette-only warning | PASS | Fresh boxen PNG was 12,210 B and no such warning was recorded. |
| The ptitprince compatibility caveat reflects current behavior | PASS | The expected Matplotlib orientation deprecation warning was observed and is documented as a recheck limit. |

## Input 3 — Edge: Tied/all-zero fallback and missing or low-N split cells

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 57/60 · **Total 94/100**
- Execution: run/reaudit_i3_split_edges.R via r.sh; inspected reaudit_i3_split.png.
- Finding: A tied/all-zero panel fell back to nrd0 and rendered. Invalid condition typing was rejected; incomplete and low-N clusters were removed before a stable three-cluster split plot rendered.

| Assertion | Result | Evidence |
|---|---|---|
| All-zero and tied strata choose the nrd0 fallback | PASS | safe_violin_bw returned nrd0. |
| The fallback panel still renders rather than becoming blank | PASS | The violin layer was nonempty and the tied PNG was 25,496 B. |
| The split guard rejects an unordered condition and removes invalid clusters | PASS | Unordered input errored; only three complete 40-by-40 clusters remained. |
| Complete-grid split sides are stable | PASS | Ordered interaction groups were Control/Treatment within each cluster; visual inspection confirmed fixed left/right halves. |

## Input 4 — Variant B: Prior real ALL microarray split-violin input

- Status: ✅ COMPLETED · Basic 35/40 · Specialized 55/60 · **Total 90/100**
- Execution: run/reaudit_i4_real_all.R via r.sh; real Bioconductor ALL data.
- Finding: The former real-data input used probe 38319_at. No stage had both B and T N >=30, so the current contract correctly omitted all split cells instead of rendering unstable or side-swapped half violins.

| Assertion | Result | Evidence |
|---|---|---|
| The previous real ALL data route loads and selects its B-vs-T probe | PASS | ALL loaded and selected 38319_at. |
| The real stage-by-lineage counts are measured before plotting | PASS | Counts were 19/1, 36/15, 23/10, and 12/2 for populated stages. |
| The current split guard excludes each ineligible real-data cell | PASS | No cluster had both conditions at N >=30 and guarded rows equaled zero. |
| Ineligible real data is not converted into a misleading split violin | PASS | The helper returned a valid empty frame rather than relying on geom parity. |

## Input 5 — Stress: Standalone exact shipped R example and PDF export

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Execution: run/exact-source/raincloud_phd.R via r.sh and run/reaudit_i4_example_pdf.py via py.sh.
- Finding: The copied exact source example ran without a prelude and wrote a usable Nature-column PDF.

| Assertion | Result | Evidence |
|---|---|---|
| The shipped example runs without externally prepared data frames | PASS | It completed directly from the copied exact source. |
| The example writes its declared raincloud.pdf | PASS | raincloud.pdf was created in the caller working directory. |
| The exported PDF is nonempty | PASS | The PDF was 27,314 B. |
| The exported PDF uses an embedded font marker and no Type3 font | PASS | Byte inspection found a font marker and no /Type3 token. |

## Input 6 — Adversarial: Bandwidth ratio, bounded-data trim, and N guidance

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 57/60 · **Total 94/100**
- Execution: run/reaudit_i5_nrd_trim.R via r.sh.
- Finding: The corrected nrd/nrd0 ratio, trim behavior, and unified N thresholds were directly checked.

| Assertion | Result | Evidence |
|---|---|---|
| nrd has a larger bandwidth than nrd0 | PASS | The observed ratio was 1.177777777778, equal to 1.06/0.9. |
| trim=TRUE does not extend a bounded violin beyond observed values | PASS | Drawn y range matched the observed minimum and maximum bounds. |
| The full N decision sequence is stated once in the Skill | PASS | All five bins 3-10 through >1000 were found. |
| Small-N and split-cell rules agree with the table | PASS | The checked strings require raw points below 30 and both split conditions at N >=30. |

## Input 7 — Scope Boundary: Shipped-file and current compatibility contract

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 57/60 · **Total 94/100**
- Execution: run/reaudit_i6_source_contract.py via py.sh.
- Finding: Every linked example/test exists, and source inspection confirmed the current ggdist, seeded R, and hue-based Python contracts.

| Assertion | Result | Evidence |
|---|---|---|
| Every referenced shipped example and focused test exists | PASS | The R example and both R/Python tests were present. |
| The R raincloud path uses current ggdist rather than required gghalves | PASS | The source names stat_halfeye and explicitly excludes gghalves as a required dependency. |
| The current R route records deterministic jitter | PASS | The documented jitter uses the fixed 20260923 seed. |
| The current Python seaborn route avoids the deprecated palette-only form | PASS | The source documents hue=group and legend=False. |

## Key strengths

- The exact current-stack R workflow replaces archived gghalves with ggdist and produced a standalone embedded-font PDF.
- Tied and constant strata now select a panel-wide nrd0 fallback instead of silently blanking an SJ violin panel.
- Ordered two-level validation and per-cell N filtering eliminate the missing-cell split-violin side swap seen in the archived audit.
- The R and Python routes, deterministic examples, source tests, and current compatibility limits are explicit and executable.
