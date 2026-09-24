> **Audit record for `bio-proteomics-ptm-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@0dcaeb6](https://github.com/mrsonord2240/bioSkills/tree/0dcaeb6bfdafc308d0c5a9f39720df96d1969cd9/proteomics/ptm-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-ptm-analysis

Generated: 2026-09-23 · rendered from `report.json` by `tools/render_viewer.py`.

> This viewer is **generated from the audit report**, not written by the auditor. It restates the report's own recorded scores, notes and assertions and adds nothing to them. Where a hand-written viewer would argue from the runs, this one points at the scripts in [scripts/](scripts/) instead.

Source: `mrsonord2240/bioSkills@0dcaeb6bfdafc308d0c5a9f39720df96d1969cd9:proteomics/ptm-analysis`
Category: Data Analysis · Execution mode: D · Complexity: Complex · N = 7 · Executed: 7

## What the Skill claims to do

Frames PTM/phosphoproteomics analysis as three stacked inference layers on a biased enrichment - chemistry selection, site localization (FLR), and protein-level-adjusted quantification with MSstatsPTM - plus kinase-activity and functional triage.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 56 | **94** | 4/4 | yes | ✅ |
| 2 | Variant A | 37 | 56 | **93** | 4/4 | yes | ✅ |
| 3 | Edge | 35 | 53 | **88** | 4/4 | yes | ✅ |
| 4 | Variant B | 35 | 53 | **88** | 4/4 | yes | ✅ |
| 5 | Stress / multi-step | 37 | 53 | **90** | 4/4 | yes | ✅ |
| 6 | Scope Boundary | 37 | 55 | **92** | 4/4 | yes | ✅ |
| 7 | Adversarial | 36 | 53 | **89** | 4/4 | yes | ✅ |

**Execution Average: 90.6 / None** · **Assertion Pass Rate: 28/28**

**Static: 94/100** · Static weighted 37.6 + dynamic weighted 54.4 = **92/100** → ⭐ Production Ready, deployable.

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
| scientific integrity | PASS | No result, citation, or quantitative claim was fabricated in the seven evaluated outputs. |
| practice boundaries | PASS | The skill gives research-analysis guidance and does not diagnose an individual or prescribe treatment. |
| methodological ground | PASS | The tested routes preserve the stated localization, protein-adjustment, and prior-coverage safeguards. |
| code usability | PASS | The paired label-free, TMT, no-global proxy, and PTM-SEA routes produced their declared outputs under checked process ownership; the exact committed checkout passed 25 Python tests and all three R contracts. |

## Static score

| Category | Score | Note |
|---|---|---|
| functional suitability | 12/12 | The paired label-free, TMT, motif, KSEA, PTM-SEA, and explicitly labelled no-global proxy routes are implemented and exercised. |
| reliability | 11/12 | Checked runners require clean process completion, validate staged outputs, refuse clobbering, retain receipts, and publish only complete validated artifacts. |
| performance context | 7/8 | The split references and scripts avoid the former monolith; PTM-SEA remains necessarily compute-heavy. |
| agent usability | 15/16 | Decision tree, checked commands, completion markers, traps, and downstream boundaries are explicit. |
| human usability | 8/8 | Trigger, scope, input contracts, output labels, and safe invocation examples are clear. |
| security | 11/12 | No credentials or destructive broad cleanup are present; checked runners own only their process scope and use no-clobber publication. |
| maintainability | 11/12 | Focused scripts, references, contracts, and regression tests keep the paired and proxy paths distinct. |
| agent specific | 19/20 | Precise triggers, routing, stop conditions, publication contracts, and methodological refusal boundaries are present. |

## Input 1 — Canonical: Paired label-free phosphoproteome with a global proteome

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Execution: Executed the paired label-free workflow through run_checked.py on the synthetic truth-labelled phospho fixture. The worker exited 0 with no owned processes remaining and published a validated 36-row, 12-column adjusted_sites.csv; the exact committed checkout also passed the label-free R contract.
- Finding: The paired route now has validated output plus an observable clean-completion contract for unattended use.

| Assertion | Result | Evidence |
|---|---|---|
| The paired converter returns both PTM and PROTEIN inputs | PASS | stdout reports names(input): PTM PROTEIN. |
| The primary deliverable contains site-level adjusted results | PASS | adjusted_sites.csv parsed as 36 rows and 12 columns. |
| The contrast direction is explicit | PASS | stdout reports Treatment vs Control. |
| The workflow terminates successfully for automation | PASS | The checked receipt records worker_exit 0, active_processes_after_root_exit 0, validation success, and publication. |

## Input 2 — Variant A: TMT/isobaric paired phosphoproteome

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 56/60 · **Total 93/100**
- Execution: Executed msstatsptm_tmt.R through run_checked.py on the synthetic TMT10 fixture with 0-indexed channels. It cleanly published 35 adjusted rows in the declared 12-column schema, including TREAT pvalue_lfc and BH adj.pvalue_lfc; the exact committed checkout passed the TMT R contract.
- Finding: The TMT-specific converter, summarizer, contrast, threshold test, and checked publication path completed with the documented channel convention.

| Assertion | Result | Evidence |
|---|---|---|
| The TMT route returns PTM and PROTEIN | PASS | stdout reports PTM PROTEIN. |
| The TMT output is present and parseable | PASS | adjusted_sites_tmt.csv parsed as 35 rows and the declared 12 columns. |
| The documented contrast direction is retained | PASS | stdout reports Treatment vs Control. |
| The workflow returns a successful process status | PASS | The checked receipt records a clean worker exit, no lingering owned process, validation success, and publication. |

## Input 3 — Edge: KSEA with insufficient prior coverage

- Status: ✅ COMPLETED · Basic 35/40 · Specialized 53/60 · **Total 88/100**
- Execution: Built a valid one-row PhosphoSitePlus CSV and executed copied ksea_scores.R against the fresh adjusted output. It stopped before KSEA.Scores with the intended coverage message: 0 of 31 sites covered.
- Finding: The deliberate hard stop is scientifically correct and states the required prior, gene-symbol, and residue-format repairs.

| Assertion | Result | Evidence |
|---|---|---|
| A one-row prior does not reach KSEA scoring | PASS | The script stopped before package aggregation. |
| The failure reports prior coverage | PASS | The message states 0 of 31 sites. |
| The failure provides repair guidance | PASS | It names the full prior, HUGO symbols, and S473-style format. |
| No kinase score is fabricated | PASS | No output score table was written. |

## Input 4 — Variant B: Motif enrichment with experiment-matched background

- Status: ✅ COMPLETED · Basic 35/40 · Specialized 53/60 · **Total 88/100**
- Execution: Executed copied motif_enrichment.py on the synthetic MaxQuant site table and matching FASTA. It reported 35 foreground windows, 1,888 background windows from 35 proteins, and wrote a parseable 218-row CSV.
- Finding: The output correctly uses Fisher plus BH and does not mistake an unadjusted low p-value for a significant motif.

| Assertion | Result | Evidence |
|---|---|---|
| Class-I site filtering is applied | PASS | The script reported 35 eligible foreground windows. |
| The background is experiment-matched | PASS | It used 35 identified FASTA proteins, not the whole proteome. |
| Multiple testing correction is included | PASS | The output includes BH q values. |
| No motif is overcalled from nominal p values | PASS | The leading q values were 0.94114. |

## Input 5 — Stress / multi-step: PTM-SEA with real PTMsigDB identifiers

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 53/60 · **Total 90/100**
- Execution: Built 520 real v1.9.1 PTMsigDB identifiers and ran write-gct, ssGSEA2.0 with 1,000 permutations, and read under run_checked.py. The owned process scope completed cleanly, retained all four GCTs, and published a validated 111-row NES/FDR CSV.
- Finding: The complete output is parseable and the documented command now has bounded process ownership, validation, and checked publication.

| Assertion | Result | Evidence |
|---|---|---|
| The GCT has one localized-site id per row | PASS | write-gct wrote 520 unique ids. |
| The documented ssGSEA command produces score artifacts | PASS | scores, pvalues, FDR, and combined GCTs exist. |
| The result reader returns NES and FDR | PASS | The saved CSV parsed with 111 rows. |
| The command completes cleanly without supervision | PASS | The checked runner recorded worker exit 0 and no remaining process in its owned scope before publication. |

## Input 6 — Scope Boundary: Phospho-enriched data with no global proteome

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 55/60 · **Total 92/100**
- Execution: Executed the explicit no-global use_unmod=TRUE route through run_proxy_checked.py with only PTM evidence, annotation, FASTA, and qualifying unmodified peptides. It produced three proxy artifacts plus an internal manifest and wrapper-owned outer completion marker; the guarded worker exited 0 with no owned processes remaining. An unguarded Windows teardown control published nothing while producing byte-identical staged analysis files.
- Finding: The no-global route now validates its proxy assumptions and labels every result as a proxy-adjusted candidate rather than protein-adjusted regulation.

| Assertion | Result | Evidence |
|---|---|---|
| The documented no-global invocation can run with only its stated files | PASS | The guarded literal CLI run completed without annotation_protein, evidence_prot, or proteinGroups inputs. |
| The route validates whether unmodified peptides can support the proxy | PASS | It requires unambiguous mappings, two unique unmodified peptides per PTM protein, two replicates per condition, and complete protein-condition-replicate coverage. |
| The workflow does not silently report protein-adjusted regulation | PASS | Outputs and the completion marker identify no-global-proxy mode and proxy-adjusted candidates. |
| The scope warning against occupancy claims without a global proteome remains present | PASS | SKILL.md rejects regulatory KSEA/PTM-SEA claims from proxy output and distinguishes it from paired-global adjustment. |

## Input 7 — Adversarial: Request to call unadjusted phospho changes regulated

- Status: ✅ COMPLETED · Basic 36/40 · Specialized 53/60 · **Total 89/100**
- Execution: Evaluated the direct instructional response against the fresh label-free adjusted output and its 10 TREAT calls. The skill rejects both requested shortcuts: it requires ADJUSTED.Model plus an in-test effect threshold, and distinguishes model-based expected FLR from empirical FLR.
- Finding: The refusal is methodologically specific and preserves the correct research boundary.

| Assertion | Result | Evidence |
|---|---|---|
| Protein-only abundance confounding is identified | PASS | The main inference section explains why PTM.Model alone is insufficient. |
| The double-filter shortcut is rejected | PASS | The label-free script uses an in-test TREAT-style threshold. |
| Localization probability is not called empirical FLR | PASS | The failure-mode section distinguishes model-based and empirical FLR. |
| The response does not fabricate a regulated-site list | PASS | It routes to the actual adjusted analysis rather than inventing calls. |

## Key strengths

- The split SKILL.md, focused references, and parameterized scripts give agents a clear route to the major PTM workflows.
- Fresh label-free and TMT runs produced validated protein-adjusted site tables with the intended contrast direction and clean checked completion.
- KSEA guards prevent prior-coverage and non-finite-fold-change failures from becoming opaque package errors.
- Motif analysis uses an experiment-matched background and PTM-SEA successfully produced checked NES/FDR output.
- The no-global path now provides a runnable, explicitly limited proxy analysis without overstating regulatory evidence.
