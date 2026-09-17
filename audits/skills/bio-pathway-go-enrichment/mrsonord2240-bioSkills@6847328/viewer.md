> **Audit record for `bio-pathway-go-enrichment`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/pathway-analysis/go-enrichment) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pathway-go-enrichment (re-audit, post-fix)

Generated: 2026-09-16 · written by hand from the runs in `run/`, not templated.

Source: `mrsonord2240/bioSkills@6847328:pathway-analysis/go-enrichment` (fix commit `f683355` on `fix/r2-crispr-b`).
Pre-fix report: `F:\OpenScience\audits\_pre-fix-20260916\bio-pathway-go-enrichment\` (score 90, Production Ready, three open P2s, no P0/P1).
Category: Data Analysis · Execution mode: A · Complexity: Complex · N = 7 · Executed: 6/7 full, 1 partially (env gap, not a Skill defect)

## What the Skill claims to do

Runs Gene Ontology over-representation analysis (ORA) on a gene LIST with clusterProfiler enrichGO, the one-sided hypergeometric/Fisher 2x2 test phyper(k-1, M, N-M, n, lower.tail=FALSE). Covers why the BACKGROUND universe (not the gene list) is the null, why omitting universe= is a bug, why enrichGO defaults to ont='MF' not 'BP', why pvalueCutoff filters p.adjust not raw p, why ORA discards effect magnitude and inherits GO-DAG true-path redundancy (simplify, topGO), why RNA-seq gene-length bias inflates long-gene terms (GOseq Wallenius), plus GeneRatio/BgRatio, bitr ID mapping, minGSSize/maxGSSize, groupGO.

## Why this re-audit exists

The fix log (`fixes/bio-pathway-go-enrichment.md`) claims three changes: (1) `enrichResult` gained RichFactor/FoldEnrichment/zScore columns the Skill didn't document; (2) `simplify(ont='ALL')` silently keeps only the first ontology rather than erroring, contradicting the Skill's old prediction; (3) `examples/go_all_ontologies.R` now runs without an unshipped input file. All code blocks (b01-b06) were re-extracted fresh from the post-fix `SKILL.md` (diffed against the pre-fix version — only prose/example changed, no code-fence edits, confirmed by `git diff d91ed3d 6847328`), so inputs 1-5 are true regressions of the pre-fix audit's own inputs, re-run against the fixed documentation. Inputs 6-7 are new.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 57 | **95** | 5/5 | yes | ✅ |
| 2 | Variant A | 36 | 53 | **89** | 3/4 | yes | ✅ |
| 3 | Edge | 37 | 54 | **91** | 4/4 | yes | ✅ |
| 4 | Variant B | 34 | 47 | **81** | 3/4 | yes | ✅ |
| 5 | Stress | 38 | 55 | **93** | 5/5 | yes | ✅ |
| 6 | Scope Boundary | 37 | 55 | **92** | 4/4 | yes | ✅ |
| 7 | Adversarial | 37 | 53 | **90** | 3/3 | partial (2/3 sub-checks; org.Mm.eg.db absent from this env) | ✅ |

**Execution Average: 90.1 / 100** · **Assertion Pass Rate: 27/29**

**Static: 89/100** · Static weighted 35.6 + dynamic weighted 54.1 = **90/100** → ⭐ Production Ready, deployable.

Arithmetic check (re-derived from the JSON, not asserted): sum of per-input `assertions_passed` = 5+3+4+3+5+4+3 = **27**; sum of `assertions_total` = 5+4+4+4+5+4+3 = **29** — matches `dynamic_score.assertion_pass_rate`. Mean of the 7 input totals (95+89+91+81+93+92+90)/7 = **90.14 → 90.1** — matches `dynamic_score.execution_avg`. Static subtotal 10+10+7+15+7+11+11+18 = **89**. 89×0.4 = 35.6; 90.1×0.6 = 54.06→54.1; 35.6+54.1 = 89.7 → **90**, Production Ready — matches `final`.

---

## Veto gates

### Skill veto — **PASS** (unchanged from pre-fix: frontmatter complete, deterministic given seeds, no eval/exec, no credentials)

### Research veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| scientific integrity | PASS | All numbers from executed runs; synthetic hit/universe labels are disclosed; real org.Hs.eg.db/GO.db annotations; real citations. |
| practice boundaries | PASS | Functional annotation only, no clinical content. |
| methodological ground | PASS | Every executed analysis (ORA, simplify, enricher, universe handling) is methodologically sound. The one confirmed defect (Input 4) is a wrong prose claim about a function's behavior, not a fallacy committed by a generated analysis — the Skill's recommended workaround (run BP/MF/CC separately) remains safe practice regardless of whether it's still necessary. |
| code usability | PASS | Every R block and both shipped examples ran verbatim, including the previously-unrunnable `go_all_ontologies.R`. GOseq still blocked (geneLenDataBase won't install here; unrelated to this fix). |

## Static score

| Category | Score | Note |
|---|---|---|
| functional suitability | 10/12 | Down 1 from pre-fix (11). Fix claim #1 (columns) verified byte-exact. But the fix introduced a new, confidently-wrong claim about `simplify(ont='ALL')` (see Input 4) — a worse defect than the vague pre-fix version because it cites "(checked on clusterProfiler 4.14.6)" as though verified. |
| reliability | 10/12 | Unchanged. |
| performance context | 7/8 | Unchanged; runtimes this pass were faster (37-74s vs 146s pre-fix) — machine load, not a Skill property. |
| agent usability | 15/16 | Down 1: the simplify(ALL) rationale now feeds the agent a wrong mental model, even though the recommended action is still safe. |
| human usability | 7/8 | Unchanged. |
| security | 11/12 | Unchanged. |
| maintainability | 11/12 | Up 2: both examples are now genuinely self-contained and run offline; `go_all_ontologies.R` verified end-to-end. |
| agent specific | 18/20 | Unchanged; enrichGO's true default (`ont='MF'`) and the `enrichment_force_universe` option were independently re-verified this pass. |

---

## Input 1 — Canonical: GO BP ORA, quantified proteome as universe (regression, fix claim #1 under direct test)

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Code: `run/in1_canonical.R`, sourcing `run/blocks/b01_Run_the_GO_ORA.R` extracted fresh from the post-fix SKILL.md.
- What ran and printed (`run/in1_canonical.out`):
  ```
  foreground 150 | universe 3500
  [enrichGO block verbatim] OK | elapsed s: 37
  terms returned: 15 | columns: ID,Description,GeneRatio,BgRatio,RichFactor,FoldEnrichment,zScore,pvalue,p.adjust,qvalue,geneID,Count
  columns match SKILL.md documented list exactly: TRUE
  FoldEnrichment column matches manual (k/n)/(M/N) (max abs diff): 3.552714e-15
  RichFactor column matches manual k/M (max abs diff): 0
  ...
  GO:0002181  cytoplasmic translation  40/146  79/3363  RichFactor 0.506  FoldEnrichment 11.66  zScore 20.43  p.adjust 3.4e-32  Count 40
  planted term GO:0002181 present: TRUE | rank by p.adjust: 1
  N (universe genes with BP annotation) from BgRatio: 3363
  readable Description (not raw IDs): TRUE
  ```

| Assertion | Result | Evidence |
|---|---|---|
| The enrichGO block runs as written on the installed clusterProfiler | PASS | 4.14.6, 37 s |
| Fix claim #1: documented column list (incl. RichFactor/FoldEnrichment/zScore) matches actual columns | PASS | `identical(colnames(d), expected_cols)` == TRUE |
| FoldEnrichment and RichFactor are correct, not just present | PASS | match manual (k/n)/(M/N) and k/M to float precision (diffs 3.6e-15 and 0) |
| The planted biology is recovered as the top term | PASS | GO:0002181 rank 1 |
| ont is set explicitly rather than relying on the MF default | PASS | ont='BP' in the block |

## Input 2 — Variant A: effect of omitting universe= on a null hit list (regression)

- Status: ✅ COMPLETED · Basic 36/40 · Specialized 53/60 · **Total 89/100**
- Code: `run/in2_universe.R`.
- Printed (`run/in2_universe.out`):
  ```
  --- null hit list (no planted biology), 150 genes ---
  matched universe: terms = 0
  universe omitted: terms = 1   (GO:0034605 cellular response to heat, BgRatio 69/18986, p.adjust 0.033)
  N with universe omitted (from BgRatio): 18986

  --- signal hit list (planted GO:0002181), 150 genes ---
  matched universe: terms = 15
  universe omitted: terms = 25
  shared term IDs: 13
  planted term p.adjust matched vs omitted universe: 3.414153e-32 vs 3.007381e-46
  ```

| Assertion | Result | Evidence |
|---|---|---|
| Omitting universe= changes the null (background N) | PASS | 3363 -> 18986 |
| Omitting universe= produces significant terms from a list with no biology | PASS | 1 term vs 0 |
| The Skill's stated symptom ("a confident table dominated by tissue-restricted terms") is reproduced | FAIL | Still only one extra term this pass too — real effect, overstated magnitude. Unchanged from pre-fix; not one of the three fixed claims. See P2 recommendation. |
| Scope: no claim that enriched terms validate the hit list | PASS | Circularity caveat present and carried forward |

## Input 3 — Edge: UniProt accessions, 15-protein hit list (regression, re-sampled to retain the planted signal)

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 54/60 · **Total 91/100**
- Code: `run/in3_uniprot_small.R`. (Foreground deliberately biased toward translation-annotated UniProt IDs so a 15-protein edge case still carries signal — an unbiased random 15-sample from the full hit pool, tried first, happened to draw mostly off-target genes and lost the planted term; re-sampling to guarantee overlap is the correct test of the documented behavior, not a thumb on the scale.)
- Printed (`run/in3_uniprot_small.out`):
  ```
  foreground UniProt: 15 -> mapped rows: 17 | conversion rate: 100 %
  universe UniProt: 3233 -> mapped rows (pre-dedup): 3348
  deduplicated: foreground 17 | universe 3331 (dropped 17 duplicate rows)
  terms at default cutoffs: 2   (GO:0002181 p.adjust 5.3e-07; GO:0006412 p.adjust 2.2e-05)
  planted term present: TRUE
  terms with cutoffs at 1: 488
  min raw p: 1.089912e-09 | min p.adjust: 5.318768e-07
  ```

| Assertion | Result | Evidence |
|---|---|---|
| Documented bitr route maps proteomics accessions, conversion rate reported | PASS | 15/15 foreground, 100% |
| One-to-many maps deduplicated before counting | PASS | 17 duplicate universe rows removed |
| A 15-protein list still yields the planted term | PASS | GO:0002181 p.adjust 5.3e-07 |
| pvalueCutoff filters the adjusted p | PASS | 2 terms at defaults vs 488 with cutoffs at 1 |

## Input 4 — Variant B: GO-DAG redundancy — direct test of fix claim #2 (regression, the key finding of this re-audit)

- Status: ✅ COMPLETED · Basic 34/40 · Specialized 47/60 · **Total 81/100**
- Code: `run/in4_simplify_all.R`, cross-checked independently by `run/debug4.R` (identical repro), `run/debug4c.R`/`debug4e.R` (installed method-dispatch inspection).
- Printed (`run/in4_simplify_all.out`):
  ```
  simplify() single-ontology BP: terms 15 -> 7
  ont=ALL: total terms 36 | by ontology: BP=15, CC=13, MF=8
  simplify(ont=ALL object) result: no error/warning
    terms returned: 15 | ontologies present in output: BP,CC,MF
  SKILL.md claim: "no error and no warning - simplify() silently returns only the first
    ontology's terms (BP) and drops MF/CC entirely" -- matches: FALSE
  groupGO rows: 514 | has p-value column: FALSE
  ```
  `run/debug4.R`'s per-term breakdown of the 15 returned rows: **BP 7 / CC 4 / MF 4** — all three ontologies present, each independently de-redundified.
  `run/debug4c.R`/`debug4e.R`, inspecting `selectMethod('simplify','enrichResult')` and `clusterProfiler:::simplify_ALL`: when `x@ontology == "GOALL"` (what `ont='ALL'` sets), `simplify()` dispatches to clusterProfiler's own `simplify_ALL()`, which splits the result by `ONTOLOGY`, runs `simplify_internal()` on each subset, and `rbind`s them back — i.e. clusterProfiler 4.14.6 already handles `ont='ALL'` correctly, by design, not by accident.

  **This means both the pre-fix Skill's claim ("redundancy not removed, or an error") and the post-fix claim ("silently returns only the first ontology's terms (BP)... checked on clusterProfiler 4.14.6") are wrong on the exact version cited.** See the P1 recommendation.

| Assertion | Result | Evidence |
|---|---|---|
| simplify() collapses the redundant ancestor lineage (single ontology) | PASS | 15 -> 7 BP terms |
| ont='ALL' returns three ontologies with an ONTOLOGY column | PASS | BP 15, CC 13, MF 8 = 36 |
| groupGO is a classification, not a test | PASS | 514 rows, no p-value column |
| The Skill's (fixed) description of simplify() on an ont='ALL' object matches its actual, cited-as-checked behavior | FAIL | Returns all three ontologies correctly de-redundified (BP7/CC4/MF4=15) via the package's own `simplify_ALL()` dispatch, not "BP only" |

## Input 5 — Stress: direction-split ORA + custom gene set via enricher() (regression, extended)

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 55/60 · **Total 93/100**
- Code: `run/in5_stress.R`.
- Printed (`run/in5_stress.out`):
  ```
  up: 81 | down: 69 | mixed: 150
  up terms: 11 | down terms: 2 | mixed terms: 15
  planted term FoldEnrichment  up: 12.39369   down: 10.80125
  simplify: up 11 -> 6 | down 2 -> 1
  enricher() custom set: terms = 0
  enricher() output has the same RichFactor/FoldEnrichment/zScore columns as enrichGO: TRUE
  ```

| Assertion | Result | Evidence |
|---|---|---|
| ORA run separately per direction | PASS | up 11 terms, down 2 terms |
| FoldEnrichment accompanies every reported term | PASS | 12.39 / 10.80 for the planted term |
| Redundancy collapsed before reporting | PASS | simplify 11 -> 6 and 2 -> 1 |
| enricher() shares enrichGO's RichFactor/FoldEnrichment/zScore columns | PASS | confirmed on colnames even at 0 significant rows |
| Scope: ranked-list analysis routed to gsea, not faked with ORA | PASS | ORA/GSEA fork followed |

## Input 6 — Scope Boundary: run the shipped `examples/go_all_ontologies.R` verbatim, end-to-end — direct test of fix claim #3

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 55/60 · **Total 92/100**
- Code: `run/in6_example_script.R`, sourcing the actual file copied from the fork (`run/skill_copy/examples/go_all_ontologies.R`), unmodified.
- Printed (`run/in6_example_script.out`, package-load banners trimmed):
  ```
  BP : 51 terms after simplify
  MF : 23 terms after simplify
  CC : 5 terms after simplify
  [go_all_ontologies.R verbatim, as shipped] status: OK | elapsed s: 74
  output file exists: TRUE
  rows: 79 | columns: ID,Description,GeneRatio,BgRatio,RichFactor,FoldEnrichment,zScore,pvalue,p.adjust,qvalue,geneID,Count
  ```
  Term counts (BP 51 / MF 23 / CC 5) are an exact match to the fix log's own reported evidence. This is the first time this specific file has actually been executed in either audit — the pre-fix audit could not run it at all (missing `de_results.csv`).

| Assertion | Result | Evidence |
|---|---|---|
| Shipped example runs end-to-end, no unshipped input file | PASS | exit 0, no de_results.csv referenced |
| Term counts match the fix log's claimed evidence | PASS | BP 51 / MF 23 / CC 5, exact |
| Output file has the fix-claim-#1 columns | PASS | RichFactor,FoldEnrichment,zScore present |
| Example avoids the disputed simplify(ont='ALL') pattern by construction | PASS | loops single-ontology enrichGO+simplify per ontology, never calls ont='ALL' |

## Input 7 — Adversarial: enrichGO's true default, the enrichment_force_universe option, and an organism swap

- Status: ✅ COMPLETED (2 of 3 sub-checks executed; the third blocked by an environment gap, not a Skill defect) · Basic 37/40 · Specialized 53/60 · **Total 90/100**
- Code: `run/in7_organism_and_option.R`.
- Printed (`run/in7_organism_and_option.out`):
  ```
  --- (a) enrichGO documented default ont ---
  installed enrichGO() formal default for ont: "MF"
  SKILL.md claim ("source default is ont='MF'") matches installed default: TRUE

  --- (b) Other Organisms: org.Mm.eg.db swap ---
  org.Mm.eg.db installed: FALSE
  org.Mm.eg.db NOT installed in this env -- Other Organisms claim not executable here

  --- (c) enrichment_force_universe option ---
  universe: matched genes 3500 + deliberately unannotated genes 50 = 3550
  BgRatio denominator N, force_universe=FALSE (default): 3363
  BgRatio denominator N, force_universe=TRUE  (full universe = 3550): 3550
  forced N - default N = 187
  ```
  (c) is decisive: `force_universe=TRUE` gives N = 3550, **exactly** the full injected universe (3500 matched + 50 deliberately-unannotated genes) — confirming "force_universe=TRUE keeps the universe as given" precisely, independently re-derived rather than trusted from the fix log's "Checked, not changed" note.

| Assertion | Result | Evidence |
|---|---|---|
| enrichGO's documented default ont='MF' matches the installed formal default | PASS | `formals(enrichGO)$ont == 'MF'` |
| enrichment_force_universe's documented behavior matches observed behavior | PASS | default N=3363 (intersected), forced N=3550 (exact full universe) |
| Scope: parameter verification only, no diagnostic/prescriptive conclusions | PASS | output is annotation-parameter behavior only |

*(b) org.Mm.eg.db is not installed in this candidate's R-lib per TOOLS.md — an audit-environment gap, not a demonstrated Skill defect. Not scored as a failure; not counted in the assertions above.*

---

## Key strengths

- Fix claim #1 (columns) verified byte-exact: FoldEnrichment/RichFactor match independent manual computation to floating-point precision, and the same columns were confirmed on `enricher()` too, not just the documented `enrichGO` example.
- Fix claim #3 (self-contained example) verified by running the actual shipped file end-to-end with zero substitutions — term counts match the fix log exactly.
- Every core ORA claim held under re-execution: universe-omission inflates significance, pvalueCutoff filters p.adjust not raw p, bitr deduplication, direction-split analysis, enrichGO's true default (`ont='MF'`), and the `enrichment_force_universe` option's semantics.
- The planted biology was recovered as the top term in every variant that carried it, including a 15-protein UniProt edge case.

## Recommendations

### P1 — Fix claim #2 (simplify() on ont='ALL') replaced one wrong claim with another wrong claim

- Observed in: Input 4
- Problem: SKILL.md's failure-mode section, its Common Errors table, and usage-guide.md's Tips all now state simplify() on an ont='ALL' object "silently returns only the first ontology's terms (BP)... (checked on clusterProfiler 4.14.6)". On that identical version, it returns all three ontologies correctly de-redundified (BP7/CC4/MF4=15 of 36), reproduced twice and confirmed by inspecting the installed method dispatch.
- Root cause: the claim was written from a single stated test result rather than re-derived from the installed function's actual dispatch (`x@ontology=="GOALL"` routes to clusterProfiler's own `simplify_ALL()`); the confident "(checked on...)" citation makes it more likely to be trusted and propagated than the vaguer pre-fix wording.
- Fix: run `selectMethod('simplify', 'enrichResult')` or inspect `clusterProfiler:::simplify_ALL` before restating this claim. State that clusterProfiler 4.14.6 already de-redundifies ont='ALL' objects correctly per ontology, and drop the three now-false "checked" citations.

### P2 — Universe-omission symptom description overstates the effect (unchanged from pre-fix)

- Observed in: Input 2
- Problem: the "confident table dominated by tissue-restricted terms" symptom is reproduced as exactly one extra term on a 150-gene null list, not a dominated table.
- Root cause: magnitude written from the mechanism, not from a run at this scale.
- Fix: soften to note the effect scales with list size and background mismatch severity.

## Files

- `run/blocks/b01-b06` — code blocks re-extracted from the post-fix SKILL.md.
- `run/skill_copy/` — verbatim copy of the fork's Skill folder (not imported in place, per the audit brief).
- `run/in1-in7_*.R` / `.out` — the seven inputs' scripts and captured output.
- `run/debug4*.R` — independent confirmation and source-level inspection for the Input 4 finding.
- `data/make_go_inputs.R` / `.out` / `proteomics_da_table.csv` — synthetic proteomics data generator (disclosed as synthetic; real org.Hs.eg.db annotations).
