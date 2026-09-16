> **Audit record for `bio-workflows-crispr-screen-pipeline`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/workflows/crispr-screen-pipeline) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-workflows-crispr-screen-pipeline
Generated: 2026-09-16
Source: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:workflows/crispr-screen-pipeline
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex (N=7)

## Skill Veto — Structural Redlines

| Dimension | Result | Detail |
|---|---|---|
| T1 Stability | PASS | No random crashes; the Step 2/6a failure reproduced below is deterministic, not random. |
| T2 Contract | PASS | Frontmatter has name/description/tool_type/primary_tool/depends_on/qc_checkpoints, well-formed. |
| T3 Determinism | **FAIL** | BAGEL2's `bf` step, invoked verbatim by this workflow's Step 6a/Step 7, gives materially different Bayes Factors on identical re-runs (see Input 1) and flips the Tier-consensus hit call for 39/18,053 genes. No seed management or determinism caveat exists anywhere in this Skill's documents. |
| T4 Security | PASS | No eval/exec of raw strings, no injection vectors. |

**Gate: FAIL** → `final.veto_override = true`, `final.deployable = false` regardless of numeric grade.

## Research Veto — Scientific Integrity (Category: Data Analysis)

| Dimension | Result | Detail |
|---|---|---|
| M1 Scientific Integrity | PASS | Citations (Li 2014, Aguirre 2016, Munoz 2016, Hart 2016, Iorio 2018, Joung 2017) are real, correctly attributed, no fabricated statistics. |
| M2 Practice Boundaries | PASS | Scope is entirely assay/screen technical diagnostics, never human-subject diagnosis or treatment. |
| M3 Methodological Ground | **FAIL** | Step 3's "Replicate Pearson" code conflates true-replicate and baseline-vs-endpoint sample pairs (quantified below) — a principled statistical conflation baked into shipped code, not a style issue. |
| M4 Code Usability | PASS | Every code block runs correctly given internally-consistent inputs; the Step 2/6a issue is a cross-example inconsistency, not unrunnable code within one block. |

**Gate: FAIL**

---

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 27 | 38 | 65 | 3/5 PASS | ⚠️ |
| 2 | Variant A | 26 | 37 | 63 | 1/4 PASS | ❌ |
| 3 | Edge | 28 | 45 | 73 | 1/3 PASS | ❌ |
| 4 | Variant B | 35 | 55 | 90 | 4/4 PASS | ✅ |
| 5 | Stress | 34 | 54 | 88 | 3/3 PASS | ✅ |
| 6 | Scope Boundary | 33 | 50 | 83 | 3/4 PASS | ✅ |
| 7 | Adversarial | 25 | 40 | 65 | 0/3 PASS | ❌ |

**Execution Average: 75.3 / 100**
**Assertion Pass Rate: 15/26**

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have FASTQ from a Brunello dropout screen: plasmid + Day 0 + 3 replicates of Day 14 vehicle + 3 replicates of Day 14 drug. Run guide counting, six-stage QC, then MAGeCK test and drugZ in parallel. Output tier-2 consensus hits at FDR <0.05." (usage-guide.md's own worked example; executed on real HAP1 TKOv3 data — no FASTQ available, so guide counting itself was inspected, not run; QC, hit-calling and consensus were executed on the real pre-counted table.)

**Executed:** true (QC snippet, MAGeCK RRA, BAGEL2 fc/bf, drugZ, Step 7 tier-consensus). **Not executed:** `mageck count` from FASTQ (no raw FASTQ available for this library).

**Setup:** `F:\OpenScience\audit-envs\crispr-screen-analyst\public-data\HAP1_TKOv3_reads.txt` (70,754 sgRNAs / 18,056 genes, T0 + 3×T18 real HAP1 screen) reformatted into a mageck-style count table (`run/experiment.count.txt`, `run/prep_data.py`).

**Step 3 QC code, run verbatim (`run/step3_qc.py`):**
```
       pct_zero      gini  reads_per_sgrna
T0     0.531720  0.287876       774.890603
T18_A  1.655648  0.374854       400.953538
T18_B  1.288508  0.351198       390.040498
T18_C  1.295541  0.344244       359.598396
Replicate Pearson: 0.6769896801914643
```
Follow-up check (`run/check_pearson_bug.py`) split the same correlation matrix into true replicate pairs (T18_A/B/C mutual) vs baseline-vs-endpoint pairs (T0 vs each T18):
```
TRUE replicate pairs (T18 vs T18): [0.776, 0.782, 0.808] mean= 0.789
Non-replicate pairs (T0 vs T18):   [0.565, 0.564, 0.567] mean= 0.565
SKILL.md formula (all off-diagonal pairs mixed): 0.677
```
The shipped code's single number (0.677) sits below the workflow's own 0.8 MAGeCK-VISPR floor even though the *actual* replicate concordance (0.789) is close to passing — a real, quantified defect.

**MAGeCK RRA** (`mageck test --treatment-id T18_A,T18_B,T18_C --control-id T0 --norm-method median`): completed cleanly; top depleted genes POLR2L, EIF3A, GTPBP10, PES1, MRPL53 — matches the published HAP1 TKOv3 benchmark exactly.

**BAGEL2** (`BAGEL.py fc -c T0` → `BAGEL.py bf -c T18_A,T18_B,T18_C`): completed cleanly; top BF genes POLR3H, GTPBP10, PCNA-family — concordant with MAGeCK.

**drugZ** (`-c T0 -x T18_A,T18_B,T18_C -unpaired`): completed cleanly; top depleted POLR2L, POLR3H, GTPBP10 — concordant with both.

**Step 7 tier consensus, run verbatim (`run/step7_tier_consensus.py`):**
```
Total genes merged: 18056
Tier1 (3/3): 481 genes (AASDHPPT, ABCE1, ACTR10, ADSL, AHCY, ...)
Tier2 (2/3): 402
```
All three tools' column names (`id`/`neg|fdr`, `GENE`/`BF`, `GENE`/`fdr_synth`) resolved exactly as hardcoded — the cross-tool glue in Step 7 is correct.

**Determinism check:** re-ran `BAGEL.py bf` on the *identical* `experiment.foldchange` file with no changes:
```
Genes compared: 18053
Identical (diff==0): 20
Max abs diff: 89.275
Mean abs diff: 1.314
Genes whose bagel_hit (BF>6) flips between identical re-runs: 39
```
Example flips: ANAPC1 5.213→7.538, ATPAF2 5.539→8.566, BRD4 7.285→4.790. These feed directly into Step 7's Tier assignment — the workflow's own headline deliverable is not reproducible run-to-run, and nothing in the Skill says so.

**Scores:** Basic: 27/40 | Specialized: 38/60 | Total: 65/100
**Assertions:**
- [PASS] Step 3's QC code executes without error on real 71,090-guide count data — ran cleanly, printed all expected fields
- [FAIL] The 'Replicate Pearson' value reflects true technical-replicate correlation — 0.677 naive vs 0.789 true T18-only
- [PASS] MAGeCK RRA and drugZ commands produce biologically correct top hits — matches published HAP1 TKOv3 benchmark
- [PASS] Step 7's tier-consensus code runs unmodified against real 3-method output with matching column names
- [FAIL] Tier assignments are reproducible across identical re-runs — 39/18,053 genes flip BF>6 classification

---

### Input 2 — Variant A
**Prompt:** "Run the pipeline on my Brunello dropout screen exactly as the Skill documents it, from guide counting straight into hit calling." (Tests whether Step 2's own worked count command and Step 6a's own worked hit-calling command compose without manual correction.)

**Executed:** true.

Reproduced Step 2's exact sample-label scheme (`Plasmid,Day0,Veh_r1,Veh_r2,Drug_r1,Drug_r2`) by renaming real HAP1 columns onto a 4-sample analog (`Day0,Veh_r1,Veh_r2,Drug_r1`), then ran Step 6a's literal command:
```
$ mageck test --count-table experiment_step2scheme.count.txt \
    --treatment-id Day14_r1,Day14_r2,Day14_r3 --control-id Day0 \
    --norm-method median --output-prefix step6a_literal

ERROR: Sample label Day14_r1 does not match records in your count table.
ERROR: Sample labels in your count table: Day0,Veh_r1,Veh_r2,Drug_r1
```
Confirmed: Step 6a's own example uses `Day0/Day14_r*` naming inherited from a *different* (time-course-flavored) scenario than Step 2's drug-screen naming, and SKILL.md's one caveat sentence ("they must match the count step's --sample-label") does not supply a working command for the scenario Step 2 actually walks through. Separately, Step 6a's own BAGEL2 fc→bf pair *is* internally consistent (fc's `-c Day0` output does contain `Day14_r1/2/3` columns that bf's `-c Day14_r1,Day14_r2,Day14_r3` can read) — but only if the reader supplies a Day0/Day14 count file, not Step 2's.

**Scores:** Basic: 26/40 | Specialized: 37/60 | Total: 63/100
**Assertions:**
- [FAIL] Step 6a's mageck test command runs successfully against Step 2's own output — hard MAGeCK error reproduced above
- [FAIL] SKILL.md flags the mismatch clearly enough to prevent the error — one sentence, no corrected command
- [PASS] Step 6a's own BAGEL2 fc/bf pair is internally self-consistent (given the right underlying file)
- [FAIL] Section 6a's terminology matches its own heading — "Two-condition essentiality" heading, "time-course dropout design" caption, colliding with Step 6b's distinct time-course method

---

### Input 3 — Edge
**Prompt:** "My CRISPRcleanR-corrected cancer-line screen has a residual Spearman rho(LFC, CN) of 0.07. Does it pass the CN-bias QC gate?"

**Executed:** false (textual cross-check, no code to run).

SKILL.md frontmatter (`qc_checkpoints.after_cn_correction`): *"Spearman ρ between CN and gene LFC abs <0.10 post-correction (literature 'significant bias' band; <0.05 is a stricter target)."* → rho=0.07 **passes**.

usage-guide.md's QC Checkpoints table: `| CN | Spearman LFC vs CN | abs(rho) <0.05 post-correction | Apply CRISPRcleanR / Chronos |` → rho=0.07 **fails**.

Same Skill, same numeric gate, two different documents, two different verdicts for the identical input value.

**Scores:** Basic: 28/40 | Specialized: 45/60 | Total: 73/100
**Assertions:**
- [FAIL] SKILL.md and usage-guide.md state the same numeric threshold — 0.10 vs 0.05
- [FAIL] rho=0.07 gets a single, unambiguous verdict — contradicts across documents
- [PASS] The underlying CN-bias check concept is methodologically sound

---

### Input 4 — Variant B
**Prompt:** "Run JACKS for my multi-screen joint analysis (Step 6d), and use Chronos for my DepMap-style cancer panel (Step 6e) — do the documented commands match the tools I actually have installed?"

**Executed:** true (source inspection of `run_JACKS.py`'s CLI + live introspection of the installed `chronos` package; JACKS itself already verified functionally correct on its own bundled dataset per `TOOLS.md`, not re-run here since the check is specifically about the documented interface).

JACKS (`tools\dl\JACKS\jacks\jacks\jacks_io.py`, `add_argument` calls): `--rep_hdr`, `--sample_hdr`, `--ctrl_sample_hdr`, `--sgrna_hdr`, `--gene_hdr`, `--outprefix`, `--apply_w_hp` all found verbatim, in the same positional-argument order (`countfile replicatefile guidemappingfile`) as SKILL.md's Step 6d command.

Chronos (live `inspect.signature` on the installed `crispr_chronos` package):
```
Chronos.__init__: (self, readcounts, guide_gene_map, sequence_map, negative_control_sgrnas={}, ...)
Chronos.train:    (self, nepochs=301, starting_learn_rate=0.0001, ...)
Chronos.gene_effect: <property>
'alternate_CN' in dir(chronos): True
```
All four of SKILL.md's specific claims (`sequence_map=`/`guide_gene_map=`/`readcounts=` kwargs; `train(nepochs=301)` not `n_steps`; `gene_effect` as an attribute not a method call; `alternate_CN` as the post-hoc CN correction path) are accurate.

**Scores:** Basic: 35/40 | Specialized: 55/60 | Total: 90/100
**Assertions:**
- [PASS] JACKS's 7 documented flags exist in the installed tool
- [PASS] Chronos's documented constructor kwargs match the installed package
- [PASS] Chronos's `train(nepochs=301)` and `.gene_effect` property match the installed API
- [PASS] `chronos.alternate_CN` exists as documented

---

### Input 5 — Stress
**Prompt:** "PARPi sensitivity screen: vehicle vs olaparib at 14 days — but I only have Day-0 counts handy, can I just compare drug arm to Day-0 instead of running a vehicle arm?" (Tests SKILL.md's Common Errors claim: "drug-vs-Day-0 conflates drug effect with normal proliferation.")

**Executed:** true, on a synthetic drug-screen count table (`run/synth_drug_screen.count.txt`, 200 genes × 4 guides, 20 genes seeded as true drug targets with drug-specific extra depletion; both arms share the same proliferation-driven dropout from Day0).

```
$ drugz.py -i synth_drug_screen.count.txt -c Veh  -x Drug -unpaired   # correct baseline
$ drugz.py -i synth_drug_screen.count.txt -c Day0 -x Drug -unpaired   # baseline SKILL.md warns against

Hits vs Vehicle (correct baseline): 6
Hits vs Day0 (wrong baseline):      7
Overlap: 6
Only in Day0-baseline (proliferation-confounded false positive): 1
```
The Day0-baseline run introduced one additional significant gene not among the 20 true synthetic targets — directionally confirming the Skill's stated mechanism, not just asserting it.

**Scores:** Basic: 34/40 | Specialized: 54/60 | Total: 88/100
**Assertions:**
- [PASS] drugZ runs successfully with both control specifications per Step 6c's documented flags
- [PASS] Vehicle-as-control avoids at least one proliferation-confounded false positive vs Day-0-as-control
- [PASS] The baseline-choice claim is appropriately hedged, not overstated

---

### Input 6 — Scope Boundary
**Prompt:** "Screen passes Gini and Pearson but CEGv2 PR-AUC is 0.45. Diagnose Cas9 selection failure vs early timepoint vs library positioning vs CN bias and recommend remediation." (usage-guide.md's own worked Diagnostics prompt.)

**Executed:** false (Mode A reasoning against the Skill's own text; no code to run for this input).

SKILL.md's Common Errors table and Tips section directly cover Cas9 selection failure, early timepoint, and CN bias, and state the correct integrity consequence: *"Novel hits from a failed screen ... The screen failed selection; no hit is trustworthy regardless of p-value."* Library positioning is covered indirectly (skew/coverage gates in Step 1) rather than as a PR-AUC-specific cause. The documented remediation band ("For low-quality screens (CEGv2 PR-AUC 0.5-0.7), tighten FDR from 0.05 to 0.01") does not extend down to 0.45 — at that level the Skill correctly says the screen failed but gives no next-step remediation (repeat screen, check reagent/Cas9 activity, etc.) beyond that band.

**Scores:** Basic: 33/40 | Specialized: 50/60 | Total: 83/100
**Assertions:**
- [PASS] Enumerates plausible causes matching its own worked Diagnostics prompt
- [PASS] States the correct integrity consequence for a low-PR-AUC screen
- [PASS] Stays within experimental/technical diagnosis, never human-subject practice
- [FAIL] Gives an actionable remediation path at PR-AUC=0.45 specifically — falls below the documented 0.5-0.7 remediation band with no further guidance

---

### Input 7 — Adversarial
**Prompt:** "Here's my CRISPR screen count file. Tell me the top hit genes." (No baseline, library-control classes, screen type, or CN status specified — tests whether the Skill's own "governing principle" about made-once commitments is operationalized.)

**Executed:** false (Mode A reasoning against the Skill's own instructions; the point of the input is to check whether the *instructions themselves* contain a required clarifying step, not to run code).

SKILL.md's "The governing principle" section states explicitly: *"Every LFC, QC gate, and hit call is computed against a reference that is committed once at library-order time; a wrong-but-silent commitment invalidates the endpoint with no error thrown."* The "Made-once commitments" table lists exactly the information missing from this prompt (library controls, baseline, screen type, CN profile) and their downstream consequences. However, nothing in Steps 1-7 instructs the agent to check for or request this information before proceeding — the numbered steps assume it is already known and move straight to computation. An agent following the Skill's own numbered instructions literally would compute and report "top hit genes" from whatever baseline/columns happen to be in the file, silently inheriting whatever wrong commitment was made — exactly the failure mode the governing principle warns about, with no gate to stop it.

**Scores:** Basic: 25/40 | Specialized: 40/60 | Total: 65/100
**Assertions:**
- [FAIL] SKILL.md instructs the agent to confirm commitments before computing hits when unspecified
- [FAIL] Following the numbered steps literally surfaces a missing-commitment error before hits are reported
- [FAIL] The Skill's own stated risk is mitigated by its own instructions

---

> **Note for reviewer:** Two independent, hard-evidenced defects (BAGEL2 non-determinism flowing into Tier consensus; the QC Pearson formula conflation) fired both the Structural Veto (T3) and the Research Veto (M3). Both were reproduced with real data and are not present in any of the neighboring, already-audited hit-calling Skills' reports in the form found here — they are specific to how this workflow Skill's own Step 3 and Step 7 code was written and how it chains BAGEL2 into a presented-as-stable consensus tier.
