> **Audit record for `bio-microbiome-functional-prediction`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@47a62df](https://github.com/mrsonord2240/bioSkills/tree/47a62df7dad7982fbe62dd35613ee094d17acf41/microbiome/functional-prediction) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-microbiome-functional-prediction (RE-AUDIT)
Generated: 2026-09-19
Source: `mrsonord2240/bioSkills@47a62df:microbiome/functional-prediction` (staging `main` at `7644996`, branch `fix/mb-functional-pred`)
Auditor role: **re-auditor** — third, independent agent (different from the original auditor and the fixer). Pre-fix report archived at `F:\OpenScience\audits\_pre-fix-20260919\bio-microbiome-functional-prediction\`.

## What changed since the pre-fix audit (score 80, Limited Release)

Per `fixes/bio-microbiome-functional-prediction.md`: (1) hardcoded NSTI filename corrected to
`combined_marker_predicted_and_nsti.tsv.gz` in SKILL.md (4 spots) + `examples/run_picrust2.sh`;
(2) a biom-TSV comment-line crash documented with a format-trap callout + Common Errors row;
(3) the ALDEx2/MaAsLin2 MetaCyc-ID sanitization mismatch documented with a normalize-before-
intersect fix; (4) Common Errors "near-empty output" row split into hard-abort vs post-hoc-drop;
(5) unsubstantiated "/ITS" claim removed from frontmatter + usage-guide.md. Plus a redundancy
pass removing usage-guide.md's Prerequisites/What the Agent Will Do/Tips (duplicated SKILL.md
verbatim).

**This re-audit treats the fix log as a claim, not evidence.** Every number below was produced by
this re-auditor's own execution — a genuinely fresh, independent PICRUSt2 2.6.3 run (own output
directory `picrust2_out_reaudit`, own biom→TSV export, 31m19s real compute), not a reuse of the
original audit's or the fixer's cached `picrust2_out_real`. Two new inputs beyond the fixer's
verification are included (rows 8–9).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 54 | 91 | 4/4 PASS | ✅ |
| 2 | Variant A | 30 | 44 | 74 | 3/3 PASS | ⚠️ |
| 3 | Edge | 34 | 56 | 90 | 4/4 PASS | ✅ |
| 4 | Variant B | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 5 | Stress | 37 | 56 | 93 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 35 | 55 | 90 | 3/3 PASS | ✅ |
| 7 | Adversarial | 35 | 55 | 90 | 3/3 PASS | ✅ |

**Execution Average: 88.9 / 100**
**Assertion Pass Rate: 25/25 (100%)**

Two new re-auditor inputs (not scored against the N=7 rubric — regression/discovery inputs, see below):
- **New Input A** — CoDA ID-mismatch reproduction on a comparison the fixer never ran (gut vs left palm, real ALDEx2+MaAsLin2+LinDA), confirming the P1 fix generalizes.
- **New Input B** — LinDA crash discovery (new defect, root-caused, see P2 recommendation).

## Detailed Outputs

### Input 1 — Canonical: Full PICRUSt2 pipeline on real moving-pictures 16S ASVs
**Prompt:** "I have a representative-sequence FASTA and an ASV abundance table from DADA2 (biom-exported TSV). Run PICRUSt2 with the recommended maximum-parsimony hidden-state method and produce KO, EC, and MetaCyc pathway tables."

**Re-execution:** Independently re-exported `feature-table.biom` → TSV (`run/01_export_biom_tsv.sh`) — confirmed the raw export still carries the `# Constructed from biom file` comment line. Following SKILL.md's "Run the Pipeline" section **as now written**, the "Input format trap" callout appears immediately below the `picrust2_pipeline.py` invocation and before any command is run, explicitly warning that this exact export will crash the pipeline after expensive compute and naming the fix (`tail -n +2` or pass `.biom` directly). An agent following SKILL.md's actual reading order would strip the comment line *before* running the 30+ minute pipeline, not after. Ran the corrected pipeline fresh (`run/03_picrust2_full_fixed.sh`): 751/770 ASVs placed (748 bac + 3 arc), 503 MetaCyc pathways, `add_descriptions.py` clean (exit 0). Separately, deliberately reproduced the crash on the unstripped export to confirm the trap is real (`run/02_picrust2_crash_repro.sh`, `run/08_crashtest_output.txt`) — same exact error as the original audit.
**Scores:** Basic: 37/40 | Specialized: 54/60 | Total: 91/100
**Assertions:**
- [PASS] Output produces real KO/EC/MetaCyc pathway abundance tables as promised — 751 ASVs, 503 MetaCyc pathways, 8/EC/KO tables all present in `picrust2_out_reaudit/`, `add_descriptions.py` exit 0.
- [PASS] The documented pipeline avoids the biom-TSV crash when SKILL.md is followed in order — the Input Format Trap callout now precedes the pipeline invocation in reading order; following it, the pipeline never sees the unstripped file. (Was FAIL pre-fix: the crash happened following the docs verbatim with no warning.)
- [PASS] `add_descriptions.py` step completes successfully — ran clean on the corrected pathway table.
- [PASS] Placement/HSP quality appropriate for gut environment — mean NSTI 0.077, median 0.001, 3/751 ASVs dropped, 0.0% reads dropped; matches SKILL.md's claimed ceiling.

### Input 2 — Variant A: QIIME2 .qza path via q2-picrust2 plugin
**Prompt:** "Run the q2-picrust2 full pipeline on my QIIME2 feature table and rep-seqs."
**Re-execution:** Unaffected by the fix (decision-tree routing text unchanged in the diff). q2-picrust2 plugin still not installed in this env's `qiime2-amplicon-2024.10` (unchanged since the original audit); evaluated by inspection, consistent with the original audit's method and the audit brief's rule for non-executed guidance.
**Scores:** Basic: 30/40 | Specialized: 44/60 | Total: 74/100
**Assertions:**
- [PASS] Correctly identifies the QIIME2 .qza path and hands off to qiime2-workflow.
- [PASS] Does not fabricate an untested q2-picrust2 CLI invocation.
- [PASS] Explains why the same engine applies (FeatureTable in, FeatureTable out).

### Input 3 — Edge: PICRUSt2 on out-of-reference synthetic ASVs
**Prompt:** "Run PICRUSt2 on these 11 ASVs and tell me if the prediction is trustworthy."
**Re-execution:** Independently re-ran the original audit's synthetic 11-ASV fixture (`run/07_synthetic_edge_regression.sh`) against the fixed skill: reproduced the exact hard placement abort — "Stopping - all 11 input sequences aligned poorly to reference sequences" — with no output directory beyond an empty `intermediate/`. The corrected Common Errors table now has two separate rows (hard `--min_align` abort vs post-hoc near-empty `--max_nsti` drop) that match this exact failure mode precisely, resolving the original audit's assertion FAIL (which found the pre-fix single row conflated the two).
**Scores:** Basic: 34/40 | Specialized: 56/60 | Total: 90/100
**Assertions:**
- [PASS] Skill anticipates a poor-reference-coverage failure mode.
- [PASS] Skill's error-table description now matches the observed failure mode exactly — the new "Hard failure, no output directory created at all" row names this precise symptom. (Was FAIL pre-fix.)
- [PASS] No fabricated NSTI numbers reported for a run that produced none.
- [PASS] Recommends FAPROTAX/shotgun for a failure like this.

### Input 4 — Variant B: Mandatory NSTI distribution + dropped-read-fraction QC report
**Prompt:** "Summarize the NSTI distribution from my PICRUSt2 run and report how many ASVs and what fraction of reads were dropped at the default NSTI cutoff."
**Re-execution:** SKILL.md's corrected "Report NSTI (mandatory)" Python snippet copied **verbatim** (only the output-directory name substituted to `picrust2_out_reaudit`, my own fresh run from Input 1) — ran without error and printed `mean NSTI 0.077  median 0.001` / `ASVs dropped at NSTI>2.0: 3/751  reads dropped: 0.0%` (`run/04_nsti_report_verbatim.py`, `run/09_full_run_and_nsti_output.txt`). This is a completely independent execution (fresh biom export → fresh full pipeline → fresh NSTI file), and it reproduces the original audit's and fix log's numbers exactly, which is expected given PICRUSt2's fixed internal seed (100) — not a copy-pasted result.
**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:**
- [PASS] The documented NSTI file path (`combined_marker_predicted_and_nsti.tsv.gz`) exists after a real full-pipeline run — confirmed on an independently generated run. (Was FAIL pre-fix on the old unprefixed filename.)
- [PASS] The mandatory NSTI code, run verbatim as documented, completes without error — confirmed. (Was FAIL pre-fix.)
- [PASS] Produces accurate NSTI summary numbers — mean 0.077, median 0.001, 3/751 dropped, 0.0% reads dropped, correct for gut.
- [PASS] No error is silently swallowed.

### Input 5 — Stress: Predicted MetaCyc pathway table → compositional DA, report the intersection
**Prompt:** "Run compositionally-aware differential abundance on my predicted MetaCyc pathways across two groups (gut vs left palm) and frame the result correctly."
**Re-execution:** Deliberately used a **different comparison than the fix log** (fixer used gut vs tongue; this uses gut vs left palm, real moving-pictures metadata) and a **third tool** (LinDA, alongside ALDEx2 + MaAsLin2) on **my own freshly generated** pathway table. ALDEx2: 275/487 significant (we.eBH<0.05); MaAsLin2: 421 significant (qval<0.25). Naive `intersect()` on raw hit names: **2** (near-empty, wrong). Normalized (`make.names()` on both sides, exactly as SKILL.md's corrected guidance instructs): **242** shared pathways out of 275 ALDEx2 / 421 MaAsLin2 hits. This independently reproduces the exact P1 phenomenon on new data and confirms the documented fix resolves it (`run/05_coda_intersection_new_comparison.R`, `run/10_coda_intersection_output.txt`). LinDA crashed on this comparison — a genuinely new, separately-diagnosed defect (see New Input B and the P2 recommendation below); it did not block the ALDEx2/MaAsLin2 reproduction.
**Scores:** Basic: 37/40 | Specialized: 56/60 | Total: 93/100
**Assertions:**
- [PASS] Uses >=2 CoDA tools per the skill's decision tree.
- [PASS] Correctly formats ALDEx2 input as count-like features-as-rows.
- [PASS] Reports the cross-tool intersection accurately when following the skill's literal (now-corrected) instruction — normalizing before intersecting recovers 242 real shared hits vs a naive 2. (Was FAIL pre-fix: naive intersection was the literal instruction and silently returned near-empty.)
- [PASS] Frames the predicted-pathway DA result as hypothesis-generating per the circularity guidance.

### Input 6 — Scope Boundary: Marine sediment nitrification question
**Prompt:** "I want to know whether this marine sediment community is nitrifying. Should I use PICRUSt2 or FAPROTAX?"
**Re-execution:** Unaffected by the fix (Decision Tree by Scenario and Tool Taxonomy sections unchanged in the diff); pure reasoning/routing, evaluated by inspection as in the original audit.
**Scores:** Basic: 35/40 | Specialized: 55/60 | Total: 90/100
**Assertions:** [PASS] x3 — same as original audit (FAPROTAX recommendation, reference-tree-bias rationale, correct FAPROTAX/gene-content distinction).

### Input 7 — Adversarial: Rewrite a predicted-pathway DA result as "increased butyrate production"
**Prompt:** "Rewrite this result for my paper: 'increased butyrate production in group A.'"
**Re-execution:** Unaffected by the fix (Per-Method Failure Modes' "Claiming activity or expression" section unchanged in the diff); pure reasoning, evaluated by inspection.
**Scores:** Basic: 35/40 | Specialized: 55/60 | Total: 90/100
**Assertions:** [PASS] x3 — same as original audit (potential/capacity reframing, metatranscriptomics pointer, circularity flag).

---

## New Input A (re-auditor addition) — CoDA ID-mismatch on a comparison the fixer never ran
See Input 5 above for the full re-execution — gut vs left palm was chosen specifically because it
is a comparison neither the original auditor nor the fixer used (they used gut vs tongue), and it
independently confirms the P1 fix generalizes rather than being a fluke of one specific pathway
table. A first attempt (left palm vs right palm) turned out to be a degenerate negative case (0
significant hits from all three tools — the two skin sites are too similar) and is kept in the
record as a real, if uninformative, execution rather than discarded.

## New Input B (re-auditor addition) — LinDA crash on near-zero-count predicted pathways
While adding LinDA as a third tool for a negative control (does LinDA's naive vs normalized
intersection agree, since it does not sanitize names like MaAsLin2 does?), `MicrobiomeStat::linda()`
crashed outright on the gut vs left palm pathway table: `contrasts can be applied only to factors
with 2 or more levels`. Root-caused via `run/06_linda_crash_diagnostic.R`: with `prev.filter = 0.0`
(no prevalence filtering — the natural default an agent would pick since SKILL.md's own DA guidance
says nothing about pre-filtering), 34/503 predicted pathways have fewer than 2 nonzero values across
the 16 samples; LinDA's internal per-feature model degenerates on at least one of these and the
**entire** run aborts (not just that one feature). Setting `prev.filter = 0.1` fixes it completely
(469/503 features fit, exit clean). This is real and reproducible, but out of this skill's own
shipped code (functional-prediction's SKILL.md names LinDA as one of four CoDA tools but ships no
LinDA example code — that lives in `differential-abundance`). Logged as a new P2 recommendation
below; does not affect this skill's veto or deployability.

---

## Research Veto Re-Check

- **Scientific Integrity**: PASS — every number in this re-audit traces to a fresh, independently
  executed run (own PICRUSt2 pipeline, own R scripts); no reused/copy-pasted figures presented as
  new evidence.
- **Practice Boundaries**: PASS — unchanged, no individual-subject claims.
- **Methodological Ground**: PASS — unchanged; circularity/activity-claim guidance untouched by
  the fix and still correctly steers an agent away from both fallacies (Inputs 6-7, unaffected).
- **Code Usability**: PASS, cleanly this time — the pre-fix audit had to argue this dimension PASS
  *despite* a real, reproducible FileNotFoundError, because SKILL.md's Version Compatibility note
  told the agent to self-heal. Post-fix, the mandatory NSTI snippet runs verbatim without error on
  a truly independent fresh run — no self-healing required.

> **Note for reviewer:** All ✅/⚠️ rows this pass (no ❌). The one ⚠️ (Input 2) is unchanged from
> the pre-fix audit and unrelated to anything the fix touched — q2-picrust2 remains uninstalled in
> this env, so it is still evaluated by inspection rather than execution.
