> **Audit record for `bio-microbiome-functional-prediction`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/microbiome/functional-prediction) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-microbiome-functional-prediction

Generated: 2026-09-19
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:microbiome/functional-prediction`
Category: Data Analysis | Execution Mode: D (Hybrid — CLI pipeline + Python/R QC/DA code + Claude reasoning) | Complexity: Complex (N=7)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 28 | 45 | 73 | 3/4 PASS | ❌ |
| 2 | Variant A | 30 | 44 | 74 | 3/3 PASS | ⚠️ |
| 3 | Edge | 31 | 51 | 82 | 3/4 PASS | ✅ |
| 4 | Variant B | 23 | 41 | 64 | 2/4 PASS | ❌ |
| 5 | Stress | 31 | 48 | 79 | 3/4 PASS | ❌ |
| 6 | Scope Boundary | 35 | 55 | 90 | 3/3 PASS | ✅ |
| 7 | Adversarial | 35 | 55 | 90 | 3/3 PASS | ✅ |

**Execution Average: 78.9 / 100**
**Assertion Pass Rate: 20/25 (80.0%)**
**Static Score: 81/100**
**Final Score: 80/100 — ✅ Limited Release, deployable, no veto**

> **Note for reviewer:** Check ❌ rows first. Inputs 1, 4, and 5 all hit the SAME class of problem — a piece of the skill's own documented code/instructions silently or loudly breaking against real, current tool output/behavior — despite three different mechanisms (wrong hardcoded filename, an unhandled standard input-format variant, and a cross-tool feature-name mismatch). This is a structural pattern, not three unrelated flukes: nothing in this skill's tooling/examples was re-verified end-to-end against a real dataset before shipping.

---

## Real Data & Tooling Used

- **Real ASVs**: denoised the public `moving-pictures` 16S V4 dataset (Caporaso et al., QIIME2's own tutorial data, EMP protocol) end-to-end in the `qiime2-amplicon-2024.10` WSL env: import → `demux emp-single` → `dada2 denoise-single --p-trunc-len 120`. Produced 770 real ASVs across 34 real human samples (gut=8, left palm=8, right palm=9, tongue=9).
- **PICRUSt2 2.6.3** (own WSL env `picrust2`, per `TOOLS.md`) ran the full documented `picrust2_pipeline.py` pipeline against these real ASVs, and separately against the amplicon-processing synthetic fixture (11 ASVs) as an out-of-reference edge case.
- **ALDEx2 1.38.0 / MaAsLin2 1.20.0** (Windows R env, `rr.sh`) ran real compositional DA on the real predicted MetaCyc pathway table, gut vs tongue.
- All scripts are saved under `run/`.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have a representative-sequence FASTA and an ASV abundance table from DADA2. Run PICRUSt2 with the recommended maximum-parsimony hidden-state method and produce KO, EC, and MetaCyc pathway tables." (SKILL.md's own example prompt, executed against real data)

**What ran:** `picrust2_pipeline.py -s exported-rep-seqs/dna-sequences.fasta -i exported-table/feature-table.tsv -o picrust2_out_real -p 4 --hsp_method mp --max_nsti 2 --verbose`, where `feature-table.tsv` came from the standard `qiime tools export` → `biom convert --to-tsv` path (`run/03_picrust2_real_moving_pictures.sh`).

**Output:**
```
Stopping - this line of the sequence abundance table has a differing number of fields from the first line after delimitting by tabs. This will need to be fixed.
#OTU ID	L1S105	L1S140	...
For reference, this is what the first line looks like:
# Constructed from biom file
EXIT_CODE=1
```
9m25s of real placement + hidden-state-prediction compute was discarded (the whole `picrust2_out_real/` directory was not created). Stripped the leading `# Constructed from biom file` comment line (`run/04_picrust2_real_moving_pictures_fixed.sh`) and re-ran: completed in 30m52s wall / 72m18s user (4 threads), producing real `bac.tre`, `arc.tre`, KO/EC predicted tables, `combined_marker_predicted_and_nsti.tsv.gz`, and a 503-pathway MetaCyc `path_abun_unstrat.tsv.gz`. `add_descriptions.py` ran clean on the corrected output.

**Scores:** Basic: 28/40 | Specialized: 45/60 | Total: 73/100
**Assertions:**
- [PASS] Output produces real KO/EC/MetaCyc pathway abundance tables as promised — 751 ASVs placed, 8101 KOs, 503 pathways, 34 samples.
- [FAIL] The documented CLI invocation runs without crashing on a real, standard-provenance ASV table (biom-exported TSV) — crashed after 9m25s of compute; no warning anywhere in SKILL.md.
- [PASS] add_descriptions.py step completes successfully — ran clean on the corrected table.
- [PASS] Placement/HSP quality is appropriate for the claimed best-case environment (human gut) — mean NSTI 0.077, median 0.001.

---

### Input 2 — Variant A
**Prompt:** "Run the q2-picrust2 full pipeline on my QIIME2 feature table and rep-seqs."

**What ran:** No execution — confirmed `q2-picrust2` is not installed in the tooled `qiime2-amplicon-2024.10` env (`qiime picrust2 --help` → "QIIME 2 has no plugin/command named 'picrust2'"). Evaluated by inspection of SKILL.md's decision-tree routing.

**Output (inspected guidance):** "Already in QIIME2 with .qza artifacts -> qiime2-workflow (q2-picrust2 plugin) | same engine; FeatureTable in, FeatureTable out, into qiime diversity/composition."

**Scores:** Basic: 30/40 | Specialized: 44/60 | Total: 74/100
**Assertions:**
- [PASS] Correctly identifies the QIIME2 .qza path and hands off to qiime2-workflow.
- [PASS] Does not fabricate an untested q2-picrust2 CLI invocation — delegates the concrete command rather than guessing flags.
- [PASS] Explains why the same engine applies (FeatureTable in/out).

---

### Input 3 — Edge
**Prompt:** "My ASVs come from a mock synthetic community not matched to any real reference — run PICRUSt2 and tell me if the results are trustworthy." (using the amplicon-processing synthetic fixture, 11 ASVs)

**What ran:** `picrust2_pipeline.py -s asv_seqs.fna -i asv_table.tsv -o picrust2_out -p 4 --hsp_method mp --max_nsti 2 --verbose` (`run/02_picrust2_synthetic_edge.sh`).

**Output:**
```
Stopping - all 11 input sequences aligned poorly to reference sequences
(--min_align option specified a minimum proportion of 0.8 aligning to reference sequences).
EXIT_CODE=1
```
Independently reproduces the tooling pass's finding. No output directory was created at all.

**Scores:** Basic: 31/40 | Specialized: 51/60 | Total: 82/100
**Assertions:**
- [PASS] Skill anticipates a poor-reference-coverage failure mode.
- [FAIL] Skill's error-table description matches the observed failure mode exactly — Common Errors table describes "near-empty output, most ASVs dropped" (post-hoc NSTI filtering after a completed run); the real failure here is a hard pre-NSTI placement abort with zero output.
- [PASS] No fabricated NSTI numbers reported for a run that produced none.
- [PASS] Recommends checking environment / considering FAPROTAX or shotgun for a failure like this.

---

### Input 4 — Variant B
**Prompt:** "Summarize the NSTI distribution from my PICRUSt2 output and report how many ASVs and what fraction of reads were dropped at the default NSTI cutoff." (SKILL.md's own mandatory QC snippet, run verbatim against Input 1's real output)

**What ran (verbatim, `run/05_nsti_report_verbatim.py`):**
```python
nsti = pd.read_csv('picrust2_out_real/marker_predicted_and_nsti.tsv.gz', sep='\t')
...
```
**Output:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'picrust2_out_real/marker_predicted_and_nsti.tsv.gz'
```
Real file present: `combined_marker_predicted_and_nsti.tsv.gz` (plus `bac_`/`arc_`/`*_reduced_` variants — never an unprefixed one). Corrected script (`run/06_nsti_report_corrected.py`):
```
mean NSTI 0.077  median 0.001
ASVs dropped at NSTI>2.0: 3/751  reads dropped: 0.0%
total ASVs in nsti file: 751  total ASVs in table: 770
MetaCyc pathways predicted: 503, samples: 34
KOs predicted: 8101, samples: 34
```

**Scores:** Basic: 23/40 | Specialized: 41/60 | Total: 64/100
**Assertions:**
- [FAIL] The documented NSTI file path exists after a real full-pipeline run — it does not.
- [FAIL] The mandatory NSTI code, run verbatim, completes without error — FileNotFoundError, reproduced directly.
- [PASS] Once the correct filename is substituted, the code produces accurate NSTI summary numbers.
- [PASS] No error is silently swallowed — loud, clear traceback, not a silent wrong answer.

---

### Input 5 — Stress
**Prompt:** "Run the full pipeline on my real ASV table, report NSTI, then run differential abundance on the predicted MetaCyc pathway table between two groups using at least two CoDA tools, and tell me how to interpret a significant pathway." (gut vs tongue, 8 vs 9 real samples)

**What ran (`run/07_predicted_pathway_da.R`):** ALDEx2 (`aldex()`, count-like features-as-rows per SKILL.md's explicit instruction) and MaAsLin2 (`Maaslin2()`, TSS+LOG) on the real 503-pathway predicted table.

**Output:**
```
ALDEx2:  162  /  385  pathways significant at we.eBH<0.05
MaAsLin2:  294  significant associations (qval<0.25 default)
Intersection ALDEx2 & MaAsLin2: 0 pathways        <- naive intersect(), following SKILL.md literally
Corrected (name-normalized) intersection: 162 / ALDEx2 hits: 162 / MaAsLin2 hits: 294   <- after make.names() normalization
```
MaAsLin2's `all_results.tsv` sanitizes MetaCyc IDs (`PWY-6829` → `PWY.6829`); ALDEx2 keeps the raw IDs. All 162 of ALDEx2's hits are a strict subset of MaAsLin2's 294 once names are normalized — real biological signal (gut vs tongue is a large, genuine difference), but the skill's literal "report the intersection" instruction silently returns an empty, wrong answer without name normalization.

**Scores:** Basic: 31/40 | Specialized: 48/60 | Total: 79/100
**Assertions:**
- [PASS] Uses >=2 CoDA tools as the skill's decision tree instructs.
- [PASS] Correctly formats ALDEx2 input as count-like features-as-rows per SKILL.md's explicit warning.
- [FAIL] Reports the cross-tool intersection accurately when following the skill's literal instruction — naive intersect() returns 0 instead of the real 162.
- [PASS] Frames the predicted-pathway DA result as hypothesis-generating per the circularity guidance.

---

### Input 6 — Scope Boundary
**Prompt:** "I have marine sediment 16S samples. Should I use PICRUSt2 or something else to answer whether the community is capable of nitrification?"

**What ran:** No code — pure reasoning/routing response, evaluated by inspection against the Decision Tree by Scenario and Tool Taxonomy tables.

**Output (expected agent response, matched against SKILL.md):** Recommends FAPROTAX over PICRUSt2, citing the gut/host-biased reference tree, expected high NSTI in marine sediment, and FAPROTAX's curated taxon→biogeochemical-function lookup (nitrification is exactly its use case) vs PICRUSt2's de-novo gene-content prediction.

**Scores:** Basic: 35/40 | Specialized: 55/60 | Total: 90/100
**Assertions:**
- [PASS] Recommends FAPROTAX over PICRUSt2 for a marine-sediment nitrification question.
- [PASS] Explains why (reference-tree bias / high expected NSTI).
- [PASS] Does not claim FAPROTAX predicts gene content.

---

### Input 7 — Adversarial
**Prompt:** "My PICRUSt2 pathway table shows significantly increased butyrate production in the treatment group compared to control — write this up as a result for my paper."

**What ran:** No code — pure reasoning response, evaluated against the "Claiming activity or expression" and "Circularity" Common Error sections.

**Output (expected agent response, matched against SKILL.md):** Refuses the "production" framing, restricts the claim to "increased predicted butyrate-production capacity," states that activity/expression claims require metatranscriptomics, and flags that if a taxonomic difference was already reported for the same groups, the predicted-function result is the same signal re-encoded, not independent corroboration.

**Scores:** Basic: 35/40 | Specialized: 55/60 | Total: 90/100
**Assertions:**
- [PASS] Refuses/corrects "increased butyrate production" to a potential/capacity framing.
- [PASS] Warns that activity/expression claims need metatranscriptomics, not PICRUSt2.
- [PASS] Flags potential circularity if a taxonomic difference was already reported for the same groups.

---

## Veto Gates

**Skill Veto (Step 1):** PASS on all four dimensions (T1–T4). No random/flaky crashes — both real failures found (Inputs 1, 4) are deterministic, 100%-reproducible tool-output-format mismatches, not instability. Valid frontmatter contract. Deterministic given fixed input. No security/injection issues (standard CLI, file-path arguments only).

**Research Veto (Step 6, Category 3 applies):** PASS on all four dimensions, including M4 (Code Usability) — see the detailed reasoning in `eval_report_..._result.json`'s `veto_gates.research_veto.code_usability.detail`. The mandatory-NSTI-snippet defect (Inputs 1, 4) is real and severe, scored heavily via P0 recommendations and the numeric Execution Average, but SKILL.md's own "Version Compatibility" section explicitly instructs the agent to verify installed versions and adapt example code to the observed API/output — exactly the recovery path that resolved this in practice — so it does not meet the bar of unrunnable-without-any-explanation.

## Final Recommendation

**Score 80/100 — ✅ Limited Release.** Deployable, no open P0, no veto. Below the ≥85 core floor for Production Ready (Execution Average ≥85 required; this skill's real Execution Average is 78.9). Recommend a fix pass targeting the three P1s (all concrete, mechanical, high-confidence fixes — one wrong hardcoded filename, one missing input-format caveat, one missing cross-tool name-normalization note) before re-audit.
