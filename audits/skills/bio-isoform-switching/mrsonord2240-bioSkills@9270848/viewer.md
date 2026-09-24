> **Audit record for `bio-isoform-switching`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@9270848](https://github.com/mrsonord2240/bioSkills/tree/92708486d538d7f1c19d00f6117f149dfc2687b6/alternative-splicing/isoform-switching) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-isoform-switching

Generated: 2026-09-24 · rendered from `report.json` by `tools/render_viewer.py`.

> This viewer is **generated from the audit report**, not written by the auditor. It restates the report's own recorded scores, notes and assertions and adds nothing to them. Where a hand-written viewer would argue from the runs, this one points at the scripts in [scripts/](scripts/) instead.

Source: `mrsonord2240/bioSkills@92708486d538d7f1c19d00f6117f149dfc2687b6:alternative-splicing/isoform-switching`
Audit type: final-pass exact-commit corrective re-audit
Category: Data Analysis · Execution mode: D · Complexity: Complex · N = 6 · Executed: 6/6

## What the Skill claims to do

Analyzes differential transcript usage (DTU) and isoform switches with functional consequence prediction, distinguishing DTU from DGE and DTE and providing IsoformSwitchAnalyzeR, manual DRIMSeq/DEXSeq/stageR, and swish routes.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Regression Canonical | 38 | 57 | **95** | 4/4 | yes | ✅ |
| 2 | Regression Edge | 38 | 58 | **96** | 4/4 | yes | ✅ |
| 3 | Regression Adversarial | 37 | 56 | **93** | 3/3 | yes | ✅ |
| 4 | Fresh Variant | 38 | 58 | **96** | 4/4 | yes | ✅ |
| 5 | Fresh Contract | 37 | 56 | **93** | 6/6 | yes | ✅ |
| 6 | Fresh Syntax | 37 | 57 | **94** | 1/1 | yes | ✅ |

**Execution Average: 94.5 / 100** · **Assertion Pass Rate: 21/21**

**Static: 94/100** · Static weighted 37.6 + dynamic weighted 56.7 = **94/100** → ⭐ Production Ready, deployable.

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
| scientific integrity | PASS | All new numeric outcomes are from saved or freshly generated local planted-truth fixtures; version claims are bounded to installed 2.6.0 or explicitly source-read 2.8.0-2.12.0. |
| practice boundaries | PASS | The Skill remains research-analysis guidance and says NMD and switch predictions are probabilistic rather than diagnostic conclusions. |
| methodological ground | PASS | The repaired manual route was exercised on 3v5 non-syntactic sample names, while the workflow continues to require label-permutation scrutiny for small studies. |
| code usability | PASS | The packaged example and the exact manual normalization both completed on planted data, produced expected outputs, and recovered all planted switches. |

## Static score

| Category | Score | Note |
|---|---|---|
| functional suitability | 12/12 | Covers DTU framing, a runnable IsoformSwitchAnalyzeR workflow, a manual confirmation route, consequences, and uncertainty-aware DTE. |
| reliability | 12/12 | Name-keyed metadata, fixed seeding, explicit small-n limits, and manual ID normalization address the observed failure modes. |
| performance context | 6/8 | The single SKILL.md remains long, but its content is navigable and no split was needed solely to meet the 300-line target. |
| agent usability | 15/16 | Direct route choices, stops, version boundaries, and a runnable packaged example give agents concrete recovery paths. |
| human usability | 8/8 | Decision tables and explicit caveats distinguish exploratory small-n output from trusted conclusions. |
| security | 11/12 | No credentials or shell evaluation path; external licensed annotators are visibly optional and unrun. |
| maintainability | 12/12 | The runnable example, converter, version-qualified wording, and exact seed make the main routes maintainable. |
| agent specific | 18/20 | Accurate triggers, named input contracts, progressive workflow, and clear stop conditions; licensed external annotators remain environment-dependent. |

## Input 1 — Regression Canonical: Packaged synthetic demo

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Execution: Exact committed example ran with its built-in 3v3 synthetic Salmon fixture; it printed DEMO OK and wrote a >5 kB PDF.
- Finding: 14/14 planted switching genes and 8/8 planted poison-exon NMD genes were recovered; no non-planted genes were called.

| Assertion | Result | Evidence |
|---|---|---|
| The packaged script parses and starts without user data | PASS | Demo constructed its temporary Salmon, GTF, FASTA, and metadata inputs. |
| The planted switching genes are recovered | PASS | 14/14 reported by the script self-check. |
| The planted NMD consequence is recovered | PASS | 8/8 planted poison genes reported by the script self-check. |
| A plot is produced | PASS | The demo wrote switchPlot_TOY002.pdf and passed its file-size assertion. |

## Input 2 — Regression Edge: Manual DRIMSeq/DEXSeq/stageR on non-syntactic sample IDs

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 58/60 · **Total 96/100**
- Execution: The exact new ID-normalization lines were exercised with a fresh seeded 3v5 planted fixture whose directories include 1-ctrl and trt.1-b.
- Finding: Manual DEXSeq called 20 genes, recovered all 20 planted genes, and stageR returned 593 rows.

| Assertion | Result | Evidence |
|---|---|---|
| Non-syntactic IDs remain aligned through tximport and DRIMSeq | PASS | make.names() was applied to both metadata and named quant paths before tximport. |
| The manual DEXSeq model completes | PASS | No R error; per-gene q-values were produced. |
| Planted switches are recovered | PASS | 20/20 planted genes at q < 0.05. |
| stageR confirmation is reachable | PASS | getAdjustedPValues returned 593 rows. |

## Input 3 — Regression Adversarial: Installed IsoformSwitchAnalyzeR wrapper behavior

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 56/60 · **Total 93/100**
- Execution: Installed IsoformSwitchAnalyzeR 2.6.0 function bodies were inspected by R in the alternative-splicing environment.
- Finding: Part1 references both direct test wrappers and replicate logic; the installed namespace exports analyzeNetSurfP2.

| Assertion | Result | Evidence |
|---|---|---|
| The installed version is identified | PASS | IsoformSwitchAnalyzeR 2.6.0. |
| Part1 contains both selection branches | PASS | Function body contains isoformSwitchTestDEXSeq and isoformSwitchTestSatuRn. |
| The current NetSurfP importer claim is bounded | PASS | analyzeNetSurfP2 exists in the installed 2.6.0 namespace; later-version wording is labelled source-read. |

## Input 4 — Fresh Variant: Committed real-data example on fresh odd-ID 3v5 planted fixture

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 58/60 · **Total 96/100**
- Execution: The committed script was run in real-data mode with the fresh 3v5 fixture and its deliberately shuffled 1-ctrl/trt.N-b metadata.
- Finding: The output CSV contained 20 called genes: all 20 planted switches and no others; a 7,441-byte PDF was written.

| Assertion | Result | Evidence |
|---|---|---|
| The example joins unusual sample names by metadata key | PASS | All eight 1-ctrl/trt.N-b names were printed in the intended conditions. |
| The direct DEXSeq route completes | PASS | 39 switching isoforms in 20 genes were reported. |
| Fresh planted-truth recovery is exact | PASS | 20/20 planted genes and 0 other genes in significant_switches.csv. |
| Functional output is generated | PASS | ORFs, consequences, CSV, RDS, sequences, and a 7,441-byte switchPlot PDF were written. |

## Input 5 — Fresh Contract: Exact-source documentation contract

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 56/60 · **Total 93/100**
- Execution: A source-text checker ran against the committed worktree after the source commit.
- Finding: All six contract checks passed.

| Assertion | Result | Evidence |
|---|---|---|
| Stale auto-selection and unavailable-release claims are absent | PASS | Both retired phrases were absent. |
| Part1 selection is documented | PASS | The <=5/>5 Part1 behavior is stated. |
| NetSurfP version boundary is documented | PASS | The 2.12 analyzeNetSurfP3 boundary is named. |
| Workflow seed precedes importRdata | PASS | set.seed(1) precedes the workflow import. |
| Example seed precedes importRdata | PASS | set.seed(1) precedes the shipped-example import. |
| Manual ID normalization is present | PASS | Both metadata and files receive the same make.names() mapping. |

## Input 6 — Fresh Syntax: R parser check for committed packaged example

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 57/60 · **Total 94/100**
- Execution: R 4.4.3 parsed the exact committed example in the alternative-splicing environment.
- Finding: R_PARSE_OK was emitted.

| Assertion | Result | Evidence |
|---|---|---|
| The shipped R example is syntactically valid | PASS | parse(file=...) completed and emitted R_PARSE_OK. |

## Key strengths

- Exact-source evidence covers the shipped demo, the shipped real-data route, manual DTU, package behavior, documentation contract, and parsing.
- The repaired manual pipeline now handles non-syntactic sample names without a workaround.
- Small-n stochastic behavior and version boundaries are explicit instead of silently implied.
