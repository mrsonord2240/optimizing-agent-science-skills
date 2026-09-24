> **Audit record for `bio-data-visualization-upset-plots`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@cbf6803](https://github.com/mrsonord2240/bioSkills/tree/cbf68034488c0a367703d34eb22b2931d0283fee/data-visualization/upset-plots) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-upset-plots

Generated: 2026-09-24 · rendered from `report.json` by `tools/render_viewer.py`.

> This viewer is **generated from the audit report**, not written by the auditor. It restates the report's own recorded scores, notes and assertions and adds nothing to them. Where a hand-written viewer would argue from the runs, this one points at the scripts in [scripts/](scripts/) instead.

Source: `mrsonord2240/bioSkills@cbf68034488c0a367703d34eb22b2931d0283fee:data-visualization/upset-plots`
Audit type: focused final-pass re-audit at the exact follow-up commit
Category: Data Analysis · Execution mode: A · Complexity: Moderate · N = 5 · Executed: None

## What the Skill claims to do

Build UpSet plots for intersections among gene, peak, variant, or feature sets using ComplexUpset, UpSetR, or upsetplot, with explicit sorting, input hygiene, query, and export guidance.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 57 | **95** | 5/5 | no | ✅ |
| 2 | Variant A | 38 | 56 | **94** | 4/4 | no | ✅ |
| 3 | Variant B | 36 | 55 | **91** | 5/5 | no | ✅ |
| 4 | Edge | 38 | 56 | **94** | 5/5 | no | ✅ |
| 5 | Stress | 38 | 56 | **94** | 4/4 | no | ✅ |

**Execution Average: 93.6 / 100** · **Assertion Pass Rate: 23/23**

**Static: 91/100** · Static weighted 36.4 + dynamic weighted 56.2 = **93/100** → ⭐ Production Ready, deployable.

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
| scientific integrity | PASS | The exact-commit routes preserve independently calculated exclusive membership counts and accurately distinguish exclusive intersections from inclusive mode. |
| practice boundaries | PASS | This is a visualization workflow and does not diagnose, prescribe, or triage individuals. |
| methodological ground | PASS | Planted and Hallmark inputs confirmed input hygiene, exclusive-count interpretation, sorting, set preservation, and real-data scale claims. |
| code usability | PASS | The canonical R route, direct shipped R example, exact pandas-2 Python example, Python guards, and Hallmark stress route all completed with populated files and assertions. |

## Static score

| Category | Score | Note |
|---|---|---|
| functional suitability | 11/12 | All three documented routes have runnable, scope-appropriate paths with correct input hygiene, sorting, queries, attributes, exports, and explicit rank-tie behavior. |
| reliability | 11/12 | Preflight reports removed bad identifiers and stops on an empty named set; Python makes its pandas-2 constraint explicit. The external upsetplot package emits future warnings under pandas 2 but completes. |
| performance context | 7/8 | The concise SKILL.md routes users to a modern default and limits static figures to readable intersection counts. |
| agent usability | 15/16 | The decision guidance separates ComplexUpset, legacy UpSetR, and Python behavior, with explicit common-error corrections and concrete commands. |
| human usability | 8/8 | The usage guide is short, has dependency commands and representative prompts, and points implementation detail back to SKILL.md. |
| security | 11/12 | No credentials, network calls, shell interpolation, or destructive operations appear. Examples deliberately write named plot files in the current directory. |
| maintainability | 10/12 | Shipped deterministic R and Python examples have clear version assumptions and named products; library deprecation warnings come from external packages rather than the source instructions. |
| agent specific | 18/20 | Trigger scope, progressive fallback guidance, deterministic examples, escape hatches, and the Python rank-tie caveat are clear. |

## Input 1 — Canonical: R planted overlap with query and attributes

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Finding: Fresh R vector produced five populated Cairo PDFs for cardinality, degree, one query, attributes, and legacy UpSetR.

| Assertion | Result | Evidence |
|---|---|---|
| Identifier preflight trims duplicates and rejects an empty named set | PASS | Known dirty and empty inputs behaved as documented. |
| Exclusive planted intersection counts equal independent truth | PASS | Observed descending counts were 6,5,4,4,3,2,2 and sum to the union. |
| Cardinality and degree routes render successfully | PASS | Both ComplexUpset PDFs exceeded 2 KB. |
| A nonempty single query and supplied metadata attributes render | PASS | Query and attribute PDFs were populated. |
| Legacy UpSetR preserves all named sets | PASS | The vector uses nsets=length(sets) and wrote a populated PDF. |

## Input 2 — Variant A: Exact shipped R example

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Finding: The exact committed example, invoked directly as documented, wrote all three named Cairo PDFs after its duplicate warnings.

| Assertion | Result | Evidence |
|---|---|---|
| The exact R example executes as a script | PASS | Direct r.sh execution completed. |
| All three documented PDFs are produced | PASS | upset_basic, upset_customized, and upset_queries exist. |
| Each R PDF is populated | PASS | Sizes were 29,452, 28,599, and 30,054 bytes. |
| Simulated duplicate IDs are reported before plotting | PASS | Warnings reported per-set duplicate removals and the final union. |

## Input 3 — Variant B: Exact shipped pandas-2 Python example

- Status: ✅ COMPLETED · Basic 36/40 · Specialized 55/60 · **Total 91/100**
- Finding: The exact Python example completed in the documented pandas-2 environment and created three PNG/PDF pairs including its metadata boxplot; the follow-up guard rechecked both tied and untied rank boundaries.

| Assertion | Result | Evidence |
|---|---|---|
| The version guard admits the documented pandas-2 environment | PASS | pandas 2.3.3 met the source guard. |
| All six documented Python output files are created | PASS | Three PNG/PDF figure pairs exceeded 2 KB. |
| The metadata boxplot route runs | PASS | upset_with_boxplot PNG and PDF were produced. |
| The rendered Python plot has no stray axes | PASS | The exact rendered PNG was inspected and contains a coherent UpSet layout plus boxplots. |
| Rank-limit guidance distinguishes tied from untied boundaries | PASS | The rerun rendered three bars without a tie and retained six bars at a tied rank-3 cutoff; the exact commit documents both behavior and exact-count pre-filtering. |

## Input 4 — Edge: Python input and presentation guards

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Finding: Independent pandas-2 vector used unequal planted counts and tested duplicate rejection, rank behavior, labels, exact styling, and PDF embedding.

| Assertion | Result | Evidence |
|---|---|---|
| from_contents rejects duplicate identifiers | PASS | The planted duplicate input raised ValueError. |
| A no-tie max_subset_rank limits the ranked bars | PASS | Three unequal leading bars were rendered for rank 3. |
| Manual intersection count labels are present | PASS | At least three annotation texts were attached to the bar axis. |
| present plus absent targets exact membership | PASS | The AB-only bar received the requested orange style. |
| Python PDF uses a non-Type3 embedded font | PASS | PDF bytes contain Type42 or CIDFontType2 and no Type3 marker. |

## Input 5 — Stress: Ten real Hallmark gene sets

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Finding: The real membership table rendered a populated top-20 ComplexUpset PDF from 10 sets, 1,211 genes, and 137 nonempty exclusive combinations.

| Assertion | Result | Evidence |
|---|---|---|
| All ten named Hallmark sets are nonempty | PASS | The audit fixture has ten nonempty sets. |
| The input has fewer nonempty combinations than the theoretical 1023 | PASS | Independent count was 137 nonempty exclusive combinations. |
| The top-20 route renders a populated export | PASS | hallmark_top20.pdf exceeded 2 KB. |
| The stress run remains within visualization scope | PASS | It reports membership intersections only and makes no clinical or causal claim. |

## Key strengths

- Exact R and Python shipped examples execute in the documented compatible environments and emit named populated files.
- Input hygiene makes duplicate, blank, missing, and empty-set behavior explicit instead of silently distorting intersections.
- ComplexUpset, UpSetR, and upsetplot behavior is described with tested sorting, query, compatibility, and exact-style constraints.
- The real Hallmark stress vector confirms that theoretical combinations and observed nonempty intersections are not conflated.
