> **Audit record for `bio-metabolomics-msdial-preprocessing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@e857587](https://github.com/mrsonord2240/bioSkills/tree/e857587ffaea6bb9bb8c00787b3f562d5bb6f6a5/metabolomics/msdial-preprocessing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-metabolomics-msdial-preprocessing

Generated: 2026-09-24 · rendered from `report.json` by `tools/render_viewer.py`.

> This viewer is **generated from the audit report**, not written by the auditor. It restates the report's own recorded scores, notes and assertions and adds nothing to them. Where a hand-written viewer would argue from the runs, this one points at the scripts in [scripts/](scripts/) instead.

Source: `mrsonord2240/bioSkills@e857587ffaea6bb9bb8c00787b3f562d5bb6f6a5:metabolomics/msdial-preprocessing`
Audit type: final pass: seven archived scenario areas rechecked plus three fresh boundary/reliability scenarios
Category: Data Analysis · Execution mode: D · Complexity: Complex · N = 10 · Executed: 4/10 (one preserved real-export regression and three exact-source contract tests)

## What the Skill claims to do

Runs MS-DIAL untargeted preprocessing and imports an alignment export into R or Python with explicit filtering and scope boundaries.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical regression | 40 | 55 | **95** | 2/2 | no | PASS |
| 2 | Variant A regression | 40 | 55 | **95** | 2/2 | no | PASS |
| 3 | Edge regression | 40 | 55 | **95** | 2/2 | no | PASS |
| 4 | Variant B regression | 40 | 60 | **100** | 3/3 | yes | PASS |
| 5 | Integrated regression | 40 | 55 | **95** | 2/2 | no | PASS |
| 6 | Scope-boundary regression | 40 | 55 | **95** | 3/3 | no | PASS |
| 7 | Reliability regression | 40 | 55 | **95** | 3/3 | no | PASS |
| 8 | Scope-boundary fresh | 40 | 60 | **100** | 2/2 | yes | PASS |
| 9 | Reliability fresh | 40 | 60 | **100** | 2/2 | yes | PASS |
| 10 | Evidence-honesty fresh | 40 | 60 | **100** | 2/2 | yes | PASS |

**Execution Average: 97 / 100** · **Assertion Pass Rate: 23/23**

**Static: 94/100** · Static weighted 47.0 + dynamic weighted 48.5 = **95.5/100** → A Production Ready, deployable.

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
| scientific integrity | PASS | The revised text distinguishes direct evidence from documentation-backed DIA behavior and does not convert an untargeted feature table into targeted concentrations. |
| practice boundaries | PASS | The Skill routes predefined targeted panels to the dedicated targeted-analysis Skill. |
| methodological ground | PASS | Feature filtering, annotation limits, and the silent method-file risk have explicit operational safeguards. |
| code usability | PASS | The preserved real-export Python regression executed successfully on the current worker. |

## Static score

| Category | Score | Note |
|---|---|---|
| functional suitability | 12/12 | Untargeted and targeted requests now have explicit, correct routing. |
| reliability | 12/12 | Silent method-file fallback is named and paired with an observable acceptance check. |
| performance context | 7/8 | Concise scope-specific documentation; no costly run is implied as a general default. |
| agent usability | 15/16 | Decision tree, failure table, and boundaries agree. |
| human usability | 8/8 | Actionable target, method-file, and DIA evidence boundaries are explicit. |
| security | 12/12 | No credentials or destructive workflow introduced. |
| maintainability | 11/12 | Exact version caveats and acceptance checks make drift visible; fresh console execution remains unavailable in this worker. |
| agent specific | 17/20 | Good routing and escape hatches; 3 points reserved for unavailable fresh console/DIA execution. |

## Input 1 — Canonical regression: DDA console workflow, R import, and honest filtering

- Status: PASS COMPLETED · Basic 40/40 · Specialized 55/60 · **Total 95/100**
- Execution: Re-checked against the exact committed documentation and preserved prior real-console artifacts; the console and R are unavailable in this worker for a fresh instrument run.
- Finding: All final-pass assertions for this scenario passed.

| Assertion | Result | Evidence |
|---|---|---|
| The exact source documents MSDIALCUI lcms with Key: Value methods | PASS | Exact committed SKILL.md contains the real console command and method syntax. |
| The exact source retains the real-export import and 0-1 Fill% safeguards | PASS | Exact committed source retains timestamped mdalign discovery, header-block anchoring, and 0.70 Fill% guidance. |

## Input 2 — Variant A regression: DIA/SWATH CSV acquisition_type boundary

- Status: PASS COMPLETED · Basic 40/40 · Specialized 55/60 · **Total 95/100**
- Execution: Re-checked against the exact committed documentation; no real DIA/ABF input or console is available in this worker.
- Finding: All final-pass assertions for this scenario passed.

| Assertion | Result | Evidence |
|---|---|---|
| CSV acquisition_type remains documented as the DDA/DIA mechanism | PASS | Exact source documents the official console-tutorial CSV layout. |
| The source does not present true DIA deconvolution as locally executed | PASS | Exact source explicitly says it has not been exercised here on real DIA/ABF data. |

## Input 3 — Edge regression: GC-EI routing and retention-index rationale

- Status: PASS COMPLETED · Basic 40/40 · Specialized 55/60 · **Total 95/100**
- Execution: Re-checked exact-source guidance; no GC-EI raw data or console is available in this worker.
- Finding: All final-pass assertions for this scenario passed.

| Assertion | Result | Evidence |
|---|---|---|
| GC-EI remains routed to the gcms path and retention-index alignment | PASS | Exact source retains the GC-EI decision-tree row and retention-index explanation. |
| The source distinguishes GC deconvolution from LC peak-picking | PASS | Exact source retains the mechanism and failure-mode guidance. |

## Input 4 — Variant B regression: Real two-sample mdalign import into pandas

- Status: PASS COMPLETED · Basic 40/40 · Specialized 60/60 · **Total 100/100**
- Execution: Executed preserved run/input4_real_python_import.py against the archived real 2-sample export.
- Finding: All final-pass assertions for this scenario passed.

| Assertion | Result | Evidence |
|---|---|---|
| The real export parses as 16,437 features by 37 columns | PASS | Observed from the executed archived regression. |
| Only CondA and CondB enter the numeric intensity matrix | PASS | Executed regression detected exactly these two sample columns and astype(float) succeeded. |
| The dtype-safe MS/MS predicate recovers 6,887 supported features | PASS | Executed regression recovered 6,887/16,437; naive string equality returned zero after pandas bool coercion. |

## Input 5 — Integrated regression: QC and annotation handoff boundaries

- Status: PASS COMPLETED · Basic 40/40 · Specialized 55/60 · **Total 95/100**
- Execution: Re-checked exact-source routing; no new instrument data is needed for this documentation boundary.
- Finding: All final-pass assertions for this scenario passed.

| Assertion | Result | Evidence |
|---|---|---|
| QC-CV, blank, drift, and MNAR work are handed to normalization-qc | PASS | Exact source boundary section and Related Skills retain this routing. |
| Annotation confidence is handed to metabolite-annotation | PASS | Exact source limits this Skill to mapping tags rather than overclaiming identification. |

## Input 6 — Scope-boundary regression: Fixed targeted MRM/SRM/PRM panel

- Status: PASS COMPLETED · Basic 40/40 · Specialized 55/60 · **Total 95/100**
- Execution: Re-checked against the exact committed source; this is archived Input 6's former P2 gap.
- Finding: All final-pass assertions for this scenario passed.

| Assertion | Result | Evidence |
|---|---|---|
| Decision tree routes a fixed target panel away from untargeted alignment | PASS | Exact source has a dedicated MRM/SRM/PRM row pointing to targeted-analysis. |
| When NOT to Use and Related Skills expose targeted-analysis | PASS | Exact source and usage guide both name metabolomics/targeted-analysis. |
| Console target mode is not misrepresented as a validated assay | PASS | Exact source requires calibration, co-eluting internal standards, and method validation. |

## Input 7 — Reliability regression: Malformed Key=Value method line

- Status: PASS COMPLETED · Basic 40/40 · Specialized 55/60 · **Total 95/100**
- Execution: Re-checked against the exact committed source; this is archived Input 7's former P1 gap.
- Finding: All final-pass assertions for this scenario passed.

| Assertion | Result | Evidence |
|---|---|---|
| The source warns that malformed or misspelled keys can be silently ignored | PASS | Exact source states exit code 0 can still mean defaults were used. |
| The source specifies an observable method-read acceptance check | PASS | Exact source requires a safely extreme known key and an expected feature-count change. |
| The Common Errors table gives the same recovery action | PASS | Exact source repeats Key: Value and representative feature-count verification in Common Errors. |

## Input 8 — Scope-boundary fresh: Targeted request behavior across user-facing entry points

- Status: PASS COMPLETED · Basic 40/40 · Specialized 60/60 · **Total 100/100**
- Execution: Executed exact-source contract checks across the decision tree, boundary section, related-skills list, and usage guide.
- Finding: All final-pass assertions for this scenario passed.

| Assertion | Result | Evidence |
|---|---|---|
| All user-facing entry points route targeted panels to targeted-analysis | PASS | The exact Skill and usage guide expose the same routing. |
| The target-analysis sibling is a dedicated quantitative-assay Skill | PASS | The sibling exact source is present and identifies MRM/SRM/PRM calibration and validated concentrations. |

## Input 9 — Reliability fresh: Method-file acceptance protocol consistency

- Status: PASS COMPLETED · Basic 40/40 · Specialized 60/60 · **Total 100/100**
- Execution: Executed exact-source contract checks across the headless-run and Common Errors guidance.
- Finding: All final-pass assertions for this scenario passed.

| Assertion | Result | Evidence |
|---|---|---|
| The headless workflow names both the silent failure and the count-response check | PASS | Exact source warns that clean exit can still use defaults and requires an expected output count change. |
| Common Errors repeats the corrective action rather than contradicting it | PASS | Exact source requires Key: Value plus representative feature-count verification. |

## Input 10 — Evidence-honesty fresh: DIA claim boundary

- Status: PASS COMPLETED · Basic 40/40 · Specialized 60/60 · **Total 100/100**
- Execution: Executed exact-source contract checks for the previously overconfident DIA claim.
- Finding: All final-pass assertions for this scenario passed.

| Assertion | Result | Evidence |
|---|---|---|
| The source identifies the official tutorial as the CSV-layout basis | PASS | Exact source cites the official MS-DIAL console tutorial next to the layout. |
| The source marks real DIA/ABF behavior as not locally exercised | PASS | Exact source directs users to retain inputs and inspect representative MS2Dec spectra before interpretation. |

## Key strengths

- Correctly separates untargeted discovery preprocessing from validated targeted quantification.
- Makes silent Key=Value method-file fallback observable before a full batch.
- Preserves useful DIA guidance while honestly marking the missing local real-DIA execution.
