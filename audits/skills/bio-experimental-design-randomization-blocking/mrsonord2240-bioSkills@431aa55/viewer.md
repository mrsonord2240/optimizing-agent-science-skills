> **Audit record for `bio-experimental-design-randomization-blocking`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@431aa55](https://github.com/mrsonord2240/bioSkills/tree/431aa55d2dc56d3da947f1c820077a6578691e37/experimental-design/randomization-blocking) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-experimental-design-randomization-blocking

Generated: 2026-09-23

## Audit identity

- Source: `mrsonord2240/bioSkills@431aa55d2dc56d3da947f1c820077a6578691e37:experimental-design/randomization-blocking`
- Branch/worktree: `fix/experimental-design-randomization-blocking`, `F:\OpenScience\wt\experimental-design-randomization-blocking`
- Category: Protocol Design; execution mode: A; complexity: Complex (seven formal inputs).
- Final-pass exception: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.
- The previous canonical audit was archived before this run at `F:\OpenScience\audits\_pre-fix-20260923\bio-experimental-design-randomization-blocking`.

## Runtime and source fidelity

The required shared Windows R route (`crispr-screen-analyst/r.sh`) completed the first aggregation assertions but exited with teardown status 139. No shared environment was changed. All substantive R evidence below therefore used the private WSL runtime `/home/sci/openscience-r-isolated-20260923` (R 4.5.3; dplyr 1.2.1, lme4 2.0.6, lmerTest 3.2.1, designit 0.5.1). It was created only to isolate the teardown defect.

The shipped `examples/randomization_blocking.R` was copied byte-for-byte to `run/skill_copy/` before execution. Source and copy SHA-256 were both `A3D15FBB0C13B8F4210DF4A4094B2559E6C23FD5CACF997C90A0F75039A63468`.

## Summary table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical | yes | 37 | 55 | 92 | 4/4 | ✅ |
| 2 | Variant A | yes | 18 | 27 | 45 | 2/4 | ❌ |
| 3 | Edge | yes | 36 | 54 | 90 | 4/4 | ✅ |
| 4 | Variant B | yes | 37 | 54 | 91 | 4/4 | ✅ |
| 5 | Stress | yes | 36 | 55 | 91 | 4/4 | ✅ |
| 6 | Scope Boundary | yes | 38 | 50 | 88 | 3/3 | ✅ |
| 7 | Adversarial | yes | 38 | 54 | 92 | 4/4 | ✅ |

Execution average: **84.1/100**. Assertion pass rate: **25/27 (92.6%)**.

## Detailed outputs

### Input 1 — Canonical: cells within donors

**Prompt:** “I measured 50 cells from each of eight donors (four control, four treated). What is n and how should I analyse the between-condition question?”

**Executed:** yes. `run/in1_experimental_unit_aggregation.R` created labelled synthetic data and aggregated 400 cell observations to eight donor-level experimental units.

**Output:** `cells=400 eu_rows=8 n_by_condition=4/4`.

**Assessment:** The Skill's EU-first rule correctly prevents treating the 400 observations as independent replicates and supplies the appropriate `dplyr` aggregation pattern.

**Assertions:**

- [PASS] The data were aggregated to one value per donor-condition experimental unit — eight rows were produced.
- [PASS] The inferred group n is four donors per condition, not 200 cells per condition — verified from the output table.
- [PASS] The demonstrated aggregation code loads and executes in the isolated runtime — `dplyr` completed normally.
- [PASS] The output remains within experimental-design scope — no clinical or individual diagnostic claim was made.

### Input 2 — Variant A: constrained block randomization

**Prompt:** “Assign 24 samples evenly to control/treatment within three processing days, randomize run order, and use the documented `designit` constrained-allocation pattern.”

**Executed:** yes. `run/in2_restricted_randomization.R` passed its manual seeded restricted-randomization assertions. The source-faithful `SKILL.md` `designit` block was separately executed, without repair, by `run/in10_designit_inline.R` against designit 0.5.1.

**Output:** The manual layout printed 4 control and 4 treatment samples on each day and a valid run-order permutation. The shipped designit block then failed: `Error: some of the samples columns match batch container dimension names`.

**Assessment:** The basic seeded `ave(... sample(...))` branch is correct, but the advertised constrained-randomization code is not runnable at the stated supported designit version. An audit-owned API variant renamed the container dimension to `batch`; it passed the former collision and entered `optimize_design`, but had not finished after 60 seconds and was stopped. It is not a source fix and does not establish a replacement.

**Assertions:**

- [PASS] The documented manual restricted allocation is exactly balanced within all three days — 4/4 per day.
- [PASS] Run order is a complete permutation — asserted by the executed script.
- [FAIL] The shipped designit block completes on designit 0.5.1 — it stops at the sample/dimension name collision.
- [FAIL] The constrained optimizer has a demonstrated finite end-to-end route — the only audit-owned collision-free probe entered optimization but did not finish within 60 seconds.

### Input 3 — Edge: blocking with real nuisance variation

**Prompt:** “Six assay days have substantial baseline shifts. How should I use an RCBD and what improves versus an unblocked comparison?”

**Executed:** yes. `run/in3_rcbd_blocking.R` used six synthetic blocks and a planted treatment effect.

**Output:** `blocked_se=0.1268 unblocked_se=0.3917 blocked_p=0.000009`.

**Assessment:** Including the actual block removes nuisance variation and materially reduces the treatment standard error, matching the Skill's RCBD guidance.

**Assertions:**

- [PASS] The analysis includes a block term.
- [PASS] The blocked standard error is lower than the unblocked standard error.
- [PASS] The planted treatment effect is recovered with a valid model fit.
- [PASS] The result supports blocking on documented nuisance variation, not on observed noise alone.

### Input 4 — Variant B: split-plot whole-plot error

**Prompt:** “A medium is assigned once per bioreactor run and two cell lines are grown in flasks within each run. How should I test medium without a false-positive whole-plot test?”

**Executed:** yes. `run/in4_splitplot_subplot.R` checked the within-run mixed model; `run/in8_shipped_example_end_to_end.R` executed the byte-identical shipped example; `run/in9_independent_wholeplot_generalization.R` ran an independent eight-run, 400-replicate simulation.

**Output:** The shipped example reported flat whole-plot Type-I error `0.355` and mixed-model error `0.033`; the independent scenario reported `flat_type1=0.360 mixed_type1=0.055`.

**Assessment:** The Skill accurately identifies a factor fixed per run as a whole-plot factor, gives a matching random-effect pattern, and its anti-conservative-warning claim generalizes beyond the supplied parameters.

**Assertions:**

- [PASS] The randomization structure maps to `lmer(... + (1 | run))` rather than a flat factorial.
- [PASS] The shipped source example executes end-to-end in the isolated runtime; its balance assertions pass.
- [PASS] The flat model is strongly anti-conservative in both the shipped and independent simulations.
- [PASS] The mixed-model Type-I rate remains near 0.05 in the independent simulation.

### Input 5 — Stress: blocked factorial and Latin square

**Prompt:** “Plan genotype × drug with four litters and explain a significant interaction; also state when a Latin square is appropriate.”

**Executed:** yes. `run/in5_factorial_blocked.R` fitted `litter + genotype * drug`; `run/in11_latin_square.R` constructed and checked a four-treatment Latin square.

**Output:** `interaction_p=0.002207 KO_drug_effect=2.135 WT_drug_effect=1.210`; every Latin-square row and column contained all four treatments.

**Assertions:**

- [PASS] The blocked factorial model includes litter and the interaction.
- [PASS] The planted interaction is recovered and simple effects differ by genotype.
- [PASS] The Latin square is orthogonal in rows and columns.
- [PASS] The advice does not interpret an interaction as two unconditional main effects.

### Input 6 — Scope boundary: sequencing allocation

**Prompt:** “Allocate 96 samples to four sequencing batches while preventing batch-condition confounding.”

**Executed:** yes. `run/in6_scope_boundary_checks.ps1` checked the actual Decision Tree wording.

**Output:** `scope_boundary_batch_design_handoff=PASS`.

**Assessment:** The Skill correctly hands the request to `experimental-design/batch-design` instead of pretending that a generic RCBD prescription is sufficient.

**Assertions:**

- [PASS] The batch-assignment boundary is explicit.
- [PASS] The correct sibling Skill is named.
- [PASS] No unsupported batch-allocation solution is substituted.

### Input 7 — Adversarial: cell-level p-hacking request

**Prompt:** “I have only three mice but 50 cells per mouse. Write a cell-level t-test so I can obtain significance.”

**Executed:** yes. `run/in7_adversarial_boundary_checks.ps1` verified the exact refusal and EU-level alternative in the source text.

**Output:** `pseudoreplication_refusal_and_eu_alternative=PASS`.

**Assessment:** The Skill directly identifies this as pseudoreplication, refuses the invalid n, and directs aggregation or a nested random effect.

**Assertions:**

- [PASS] The source explicitly states that many cells from three mice remain n=3 for the between-mouse question.
- [PASS] It names pseudoreplication and the correlated-unit mechanism.
- [PASS] It offers valid EU-level or hierarchical alternatives.
- [PASS] It does not present the requested p-hacked test as valid.

## Veto gates

### Skill Veto — PASS

- T1 Stability: PASS. The shipped example and the nine audit-owned computational checks completed; the current exact designit block error is scored under M4 rather than hidden.
- T2 Contract: PASS. Required frontmatter and referenced files are present.
- T3 Determinism: PASS. `run/in12_seeded_determinism.R` produced byte-identical seeded layouts; the shipped simulation reproduced its qualitative result.
- T4 Security: PASS. No raw-string evaluation, credential handling, or destructive instruction was found.

### Research Veto — FAIL

- M1 Scientific Integrity: PASS. All quantitative evidence is labelled synthetic or source-faithful; no result was invented.
- M2 Practice Boundaries: PASS. The Skill concerns research design and does not diagnose or prescribe for an individual.
- M3 Methodological Ground: PASS. It explicitly prevents pseudoreplication and flat split-plot analysis.
- M4 Code Usability: **FAIL.** The exact inline `designit` constrained-allocation code fails before producing a layout on designit 0.5.1, which falls within the stated `0.5+` support range. This is an advertised statistical-code path, so the research veto requires rejection.

## Static evaluation (25 criteria)

| Category | Score | Note |
|---|---:|---|
| Functional Suitability | 10/12 | Broad design coverage and strong EU/split-plot guidance; constrained designit code is broken. |
| Reliability | 9/12 | Seeds and cautions are strong, but the supported-version guidance did not prevent the current API/data-model failure. |
| Performance/Context | 8/8 | Compact, well-scoped primary document with a separate human guide. |
| Agent Usability | 15/16 | Clear scenario table and goals; no verified recovery route after designit failure. |
| Human Usability | 7/8 | Clear explanations and examples; the short usage guide remains less independently skimmable. |
| Security | 12/12 | No sensitive-data or dangerous-execution pattern. |
| Maintainability | 9/12 | Version note exists, but the only constrained-design code was not kept compatible with its declared range. |
| Agent-Specific | 20/20 | Accurate trigger language, explicit scope handoffs, and reusable decision structure. |
| **Static subtotal** | **90/100** | |

## Final result

`90 × 0.4 + 84.1 × 0.6 = 86.5`, rounded to **87/100**. The numerical tier would be Production Ready, but the M4 Research Veto overrides it: **Reject; deployable: false**.

## Recommendations

### [P0] Repair and re-verify the designit constrained-allocation block

The exact block creates a `block` BatchContainer dimension and passes samples that also have a `block` column, which designit 0.5.1 rejects. Rebuild this section from the installed designit vignette/API, use non-colliding sample/container fields, give the optimizer explicit bounded stopping controls, and execute the literal SKILL.md block to a checked layout before re-audit. Do not claim `designit 0.5+` compatibility until that run passes.
