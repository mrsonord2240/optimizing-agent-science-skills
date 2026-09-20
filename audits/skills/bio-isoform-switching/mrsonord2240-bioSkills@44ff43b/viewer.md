> **Audit record for `bio-isoform-switching`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@44ff43b](https://github.com/mrsonord2240/bioSkills/tree/44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b/alternative-splicing/isoform-switching) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-isoform-switching

Generated: 2026-09-20 | source: `mrsonord2240/bioSkills@44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b:alternative-splicing/isoform-switching` | Category 3 Data Analysis | Mode A | Complex, N=7

Scripts and logs: `run/` (every script named below). Synthetic data: `run/data/synth` (SYNTHETIC, seeded, planted truth in `truth_genes.tsv`). Real data: nf-core rnasplice chrX GBR v YRI 2 v 2 from `audit-envs/alternative-splicing/public-data`. Not executed: SignalP, IUPred2A, DeepTMHMM (licence-gated).

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 32 | 47 | 79 | 4/5 PASS | ✅ COMPLETED |
| 2 | Variant A | yes | 28 | 43 | 71 | 4/5 PASS | ⚠️ COMPLETED |
| 3 | Edge | yes | 23 | 28 | 51 | 2/5 PASS | ❌ PARTIAL |
| 4 | Variant B | yes | 25 | 38 | 63 | 2/5 PASS | ❌ PARTIAL |
| 5 | Stress | yes | 23 | 35 | 58 | 2/4 PASS | ⚠️ COMPLETED |
| 6 | Scope Boundary | yes | 28 | 41 | 69 | 3/5 PASS | ⚠️ COMPLETED |
| 7 | Adversarial | yes | 29 | 40 | 69 | 2/4 PASS | ⚠️ COMPLETED |

**Execution Average: 65.7 / 100** | **Assertion Pass Rate: 19/33** | Static 67 x 0.4 = 26.8 | Dynamic 65.7 x 0.6 = 39.4 | **FINAL 66 - Beta Only (not deployable; no veto, no P0)**

Floors: Static 67 (<70), Layer 1 avg 26.9 (<28), Layer 2 avg 38.9 (<42), assertions 58% (<80%): grade capped at Beta Only by score in any case.

## Step 1 - Skill Veto
T1 PASS (all failures deterministic, one-line/ordering fixes; no random crash, loop or unresolvable dependency) | T2 PASS (frontmatter name, description, tool_type, primary_tool, license present) | T3 PASS (re-ran Input 1: identical PASS/FAIL, counts and minimum q; swish seeded) | T4 PASS (no eval/exec, no credentials).

## Step 2 - Static (67/100)

| Category | Score | Note |
|---|---|---|
| functional_suitability | 8/12 | Covers ISAR v2 workflow, manual DRIMSeq/DEXSeq/stageR, swish, NMD/AS-NMD interpretation. Core detection verified against planted truth. Deductions: documented snippets that fail as written (samples(d), extractSequence order, full consequence list), wrong 'silently drops' and dmFilter-default claims, unverifiable v2 auto-selection. |
| reliability | 7/12 | Common Errors table exists but its messages are paraphrases and two remedies are wrong (version suffix, no-switch stop); example has file.exists guards that defer the crash; no n>=3 / replicate check. |
| performance_context | 5/8 | 440-line SKILL.md with no references/ directory and a usage-guide that repeats it; linear workflow otherwise. |
| agent_usability | 10/16 | Clear DGE/DTE/DTU table and decision tree (learnability). Inconsistent: satuRn in a 3v3 example v its own >5-replicate rule; analyzeORF ordering differs between snippets. Few checkpoints for verifying imports or counts. |
| human_usability | 5/8 | Technical but keyword-rich description; sample-order and batch mistakes are not forgiven or flagged. |
| security | 11/12 | No credentials, no eval/exec, local R only; design vector and sample IDs are not validated. |
| maintainability | 8/12 | SKILL + usage guide + example, cross-links resolve (all related skills exist). Example is a commented stub with hard-coded file names; no test data or expected output. |
| agent_specific | 13/20 | Trigger description precise. Progressive disclosure weak (no references). Escape hatches thin: no replicate minimum, no note that SignalP/IUPred2A/DeepTMHMM are licence-gated, no note that CPC2 filtering can drop PTC isoforms. |

## Version and claim verification (installed: ISAR 2.6.0, DRIMSeq 1.34.0, DEXSeq 1.52.0, satuRn 1.14.0, stageR 1.28.0, fishpond 2.12.0, tximeta 1.24.0)

- `run/00_versions.log`: every function/argument used in SKILL.md and the example exists (importIsoformExpression, importRdata, preFilter incl. IFcutoff/keepIsoformInAllConditions, isoformSwitchTestSatuRn/DEXSeq, extractSequence, analyzeORF/CPC2/PFAM/SignalP/IUPred2A, analyzeAlternativeSplicing, analyzeSwitchConsequences, extractTopSwitches, switchPlot, extractConsequenceSummary/Enrichment, extractSplicingSummary, extractSwitchSummary). `addIsofomIdAsColumn`, `isoformExonAnnoation` spellings are the package's own.
- No installed function auto-selects satuRn/DEXSeq; ISAR warns satuRn is not advised with few replicates. No long-read/single-cell argument in importRdata (2.6.0).
- `01_docs.log`: DRIMSeq dmFilter defaults are all 0 (the Skill's 'default too strict' is wrong). ISAR analyzePFAM needs pfam_scan / web-server rows with a CL clan column.
- Citations: ISAR v2 bioRxiv 10.64898/2025.12.08.693027 (Han et al 2025) and satuRn F1000Research 10:374 confirmed via bioRxiv/Crossref APIs.
- Shipped-means-present: SKILL.md, usage-guide.md, examples/isoform_switch_analysis.R exist; all Related Skills paths exist. No missing primary file.

## Detailed Outputs

### Input 1 - Canonical
**Prompt (realistic request):** Import Salmon, pre-filter, test switches; find the 20 planted switches (3 v 3).

**Executed:** true - Ran run/10_input1_isar_3v3.R from the SKILL.md code (importIsoformExpression -> importRdata -> preFilter -> isoformSwitchTestSatuRn; plus isoformSwitchTestDEXSeq, the test the Skill's own >5-replicate rule selects). 300 genes x 3 isoforms, 20 planted switches (10 poison-exon, 10 exon-skip), 10 sub-threshold (dIF 0.06), 5 gene-level-only decoys, 5 dIF 0.15. Truth in run/data/synth/truth_genes.tsv. Re-run gave identical output.

**Code:** run/10_input1_isar_3v3.R, helpers.R, 11_dif_check.R; logs 10_input1.log, 10_input1_rerun.log

**Output (trimmed):**
```
[PASS] ISAR dIF == hand-computed mean-of-sample-IF dIF | max abs diff 7.32e-05 over 871 isoforms
tested genes 300 | planted switches recovered 20/20 | null-gene false positives 2 (of 260) GENE175,GENE206 (DEXSeq) / 0 (satuRn)
dge_only called 0 | small_switch (dIF~0.06) called 0 | dte_like (true dIF 0.15) called 3
[PASS] direction correct 20/20 ; dIF within 0.1 of planted truth 20/20
[PASS] NULL comparison DEXSeq: 1 isoform call in 300 tested genes; satuRn 0
Warning: isoformSwitchTestSatuRn: You seem to have few replicates. We therefore recommend isoformSwitchTestDEXSeq()
```

**Scores:** Basic 32/40 | Specialized 47/60 | Total 79/100

**Assertions:**
- [PASS] ISAR dIF equals an independent hand computation from quant.sf TPM - max abs diff 7.32e-05 over 871 isoforms (ISAR IF = mean of per-sample fractions)
- [PASS] All 20 planted switches recovered with the right isoform direction and dIF within 0.1 of truth - 20/20 for satuRn and DEXSeq
- [PASS] Gene-level-only (DGE) decoys are not called as DTU - 0/5 called; DEXSeq 2 null-gene FP of 260 (0.8%)
- [PASS] Null comparison (control v control) stays quiet - DEXSeq 1 isoform call in 300 tested genes, satuRn 0; re-run identical
- [FAIL] The satuRn call in the workflow agrees with the Skill's own rule (satuRn only when a condition has >5 replicates) - 3 v 3 example calls isoformSwitchTestSatuRn; ISAR 2.6.0 warns 'few replicates... use isoformSwitchTestDEXSeq()'

### Input 2 - Variant A
**Prompt (realistic request):** Manual DRIMSeq -> DEXSeq -> stageR on 6 v 6.

**Executed:** true - Ran run/20_input2_manual_dtu.R. As written the code stops at samples(d) (Biobase::samples masks DRIMSeq::samples once library(DEXSeq) is attached; run/21_samples_mask.R shows this with the Skill's exact library() order). Ran after replacing samples(d) by DRIMSeq::samples(d). tximeta(coldata) replaced by tximport (synthetic data has no Salmon index).

**Code:** run/20_input2_manual_dtu.R, 21_samples_mask.R; logs 20_input2.log

**Output (trimmed):**
```
samples(d) unqualified: ERROR: unable to find an inherited method for function 'samples' for signature 'object = "dmDSdata"'   (find('samples') -> Biobase, DRIMSeq)
--- after DRIMSeq::samples(d) ---
gene-level q<0.05: 26 genes | planted 20/20 | null-gene FP 1 | dge_only 0 | small(0.06) 0 | dte_like(0.15) 5
[PASS] stageR confirms B/C transcript in 20/20 | DRIMSeq dmTest 27 genes, Jaccard 0.89
null split: 2 gene-level calls, 3 stageR-confirmed transcripts, 2 naive-BH transcripts
dtuScaledTPM: 27 genes, planted 20/20
```

**Scores:** Basic 28/40 | Specialized 43/60 | Total 71/100

**Assertions:**
- [FAIL] Pipeline code runs as written from the Skill - 'unable to find an inherited method for function samples for signature dmDSdata' (Biobase masks DRIMSeq); fix is DRIMSeq::samples(d)
- [PASS] After the one-token fix, all 20 planted switches are called at gene-level q<0.05 with <=5% null-gene FP - 20/20; 1/260 null FP; DGE decoys 0
- [PASS] stageR confirmation names the transcript that truly switches - B (poison) or C (skip) confirmed in 20/20 planted genes
- [PASS] An independent implementation (DRIMSeq dmTest) reaches the same gene set - 27 v 26 genes, Jaccard 0.89, both 20/20 planted
- [PASS] Null split (control 1-3 v 4-6) stays quiet through stageR - 2 gene-level calls in 291 genes

### Input 3 - Edge
**Prompt (realistic request):** Real chrX 2 v 2 plus the shipped example.

**Executed:** true - Ran run/30_input3_real_chrX.R, 35a_shipped_example_prep.R, 35a3-35a6 (real nf-core rnasplice chrX, GRCh37 Ensembl GTF, 4 samples). The shipped examples/isoform_switch_analysis.R was run from the copy in run/skill/examples.

**Code:** run/30_input3_real_chrX.R, 35a_shipped_example_prep.R, 35a2-35a6, 31_dmfilter_defaults.R; logs 30_input3.log, 35a*.log

**Output (trimmed):**
```
Skill design vector on 4 files: ERROR arguments imply differing number of rows: 4, 6 (loud)
dmFilter(min_samps_gene_expr=6) on n=4: ERROR min_samps_gene_expr <= ncol(x@counts) is not TRUE
DEXSeq 19 | DRIMSeq 12 | ISAR 20 genes ; DEXSeq v DRIMSeq overlap 6 ; ISAR v DEXSeq Jaccard 0.77
top switch RPL10 ENST00000406022: ISAR dIF -0.3291 vs hand -0.3356
Skill path (importIsoformExpression defaults):   q<0.05 & |dIF|>0.1 isoforms 0, RPL10 q 1
calculateCountsFromAbundance=FALSE / tximport raw: isoforms 26, genes 20, RPL10 q 4.6e-18
tximport lengthScaledTPM: 28 isoforms / 22 genes ; scaledTPM, dtuScaledTPM through ISAR: 0
plain DEXSeq on scaledTPM counts: 2 genes, RPL10 q=0 (ISAR wrapper gives q=1; cause not isolated)
shipped example as shipped: banner only. run_switch_analysis: ERROR No genes were considered switching
```

**Scores:** Basic 23/40 | Specialized 28/60 | Total 51/100

**Assertions:**
- [FAIL] Skill's hard-coded 6-sample values work on a 2 v 2 study without editing - design vector: loud data.frame error (good); dmFilter(min_samps_gene_expr=6) on 4 samples: 'min_samps_gene_expr <= ncol(x@counts) is not TRUE', no guidance
- [PASS] ISAR dIF for the top real switch matches a hand computation from quant.sf - RPL10 ENST00000406022: ISAR -0.3291 v hand -0.3356 (isoforms removed by preFilter change the denominator)
- [PASS] Independent implementations agree on the main real signal - DEXSeq 19, DRIMSeq 12, overlap 6; ISAR v manual DEXSeq overlap 17/20
- [FAIL] The Skill's default count route detects the clearest real switch (RPL10, counts in the thousands) - importIsoformExpression defaults -> 0 significant, RPL10 q=1; calculateCountsFromAbundance=FALSE or tximport raw -> 26 isoforms, RPL10 q=4.6e-18; cause not isolated (35a3-35a6)
- [FAIL] Shipped example runs end to end on real data - banner only as shipped; functions: run_switch_analysis stops (0 switches); extract_sequences fails without CDS lines and without an existing output dir; analyze_consequences needs analyzeAlternativeSplicing and SignalP

### Input 4 - Variant B
**Prompt (realistic request):** Functional consequences (planted NMD + domain loss; real chrX).

**Executed:** true - Ran run/40a_input4_prep.R, 40b_annot.sh + 40b2_hmmscan.sh (CPC2 in as-cpc2, HMMER hmmscan --cut_ga vs Pfam-A in as-annot), 40c_domtbl_to_pfamscan.py (own bridge), 40d, 36a-36d on real chrX. NOT executed: SignalP, IUPred2A, DeepTMHMM (licence-gated; analyzeSignalP/analyzeIUPred2A only tested for their missing-file errors). The consequence steps on synthetic data needed the ORF step reordered (see assertions).

**Code:** run/40a_input4_prep.R, 40a3_ptc_independent.R, 40b_annot.sh, 40b2_hmmscan.sh, 40b3_clans.sh (unused), 40c_domtbl_to_pfamscan.py, 40d_input4_consequences.R, 36a-36d

**Output (trimmed):**
```
Skill order extractSequence -> analyzeORF: ERROR Please run the 'addORFfromGTF()' ... to detect ORFs
PTC flag == planted poison isoform for 72/72 ; distance(ISAR) == |P|+|E3| for 10/10 (6 plus, 4 minus strand)
hmmscan --cut_ga vs Pfam-A: ubiquitin PF00240 E~1e-32 in A and B isoforms of all 10 skip genes, never in C
analyzePFAM(raw --domtblout): ERROR more columns than column names ; after pfam_scan-style bridge with clan: 60 domains imported
full 8-consequence list w/o SignalP: ERROR To test differences in signal peptides, the result of the SignalP analysis must be available
NMD (CPC2 removeNoncodinORFs=TRUE): 8/10 poison genes ; without CPC2: 10/10 ; domain loss 10/10 ; ES-only splicing 24 ES, 0 IR/A3/A5
real chrX: annotated-ORF PTC v Ensembl NMD biotype sens 0.96 (48/50) spec 1.00 ; after analyzeORF(longest): sens 0.64 spec 0.89, all orf_origin -> Predicted
real end-to-end consequence table 110 rows (IR, coding potential, ORF, NMD, domains)
```

**Scores:** Basic 25/40 | Specialized 38/60 | Total 63/100

**Assertions:**
- [FAIL] The documented order (extractSequence before analyzeORF) works - fails on GTF without CDS ('Please run addORFfromGTF()... to detect ORFs'); works only when the GTF carries CDS lines
- [FAIL] analyzePFAM accepts the output of the tool the Skill names (hmmscan against Pfam-A) - raw --domtblout: 'more columns than column names'; needs pfam_scan-style table with a CL clan column (Pfam-A.clans.tsv bridge used); Skill silent
- [FAIL] With the Skill's settings all 10 planted poison isoforms are flagged NMD-sensitive and up-regulated - 8/10 with CPC2 removeNoncodinORFs=TRUE (2 poison ORFs discarded as noncoding); 10/10 without CPC2
- [PASS] Domain-loss consequence flags the skipped-exon isoform with the right direction and stays quiet elsewhere - 10/10 'Domain loss' (C up, A down); 0 domain calls outside the 10 planted genes
- [PASS] Predicted NMD status agrees with an independent reference on real annotation - annotated-ORF PTC v Ensembl nonsense_mediated_decay biotype: sens 0.96 (48/50), spec 1.00 (1023/1028)

### Input 5 - Stress
**Prompt (realistic request):** Batch-confounded synthetic design and sample-order hazard.

**Executed:** true - Ran run/50_input5_batch_order.R. synthB = synth with b2 batch shifting A->C by 40% in 30 null genes, batch imbalanced with condition (ctrl 5 b1/1 b2, trt 1 b1/5 b2). The Skill shows a condition-only designMatrix and a positional condition vector.

**Code:** run/50_input5_batch_order.R; log 50_input5.log

**Output (trimmed):**
```
no batch column:  planted 20/20 | batch-artefact genes called 19/30 | other null FP 0 | total 45
batch column:     planted 20/20 | batch-artefact genes called  0/30 | other null FP 4 | total 28
batch == condition: ERROR The supplied design matrix will result in a model matrix that is not full rank
positional vector (Skill pattern), SRR IDs: planted recovered 0/20 ; joined by sample ID: 20/20
```

**Scores:** Basic 23/40 | Specialized 35/60 | Total 58/100

**Assertions:**
- [FAIL] The Skill's positional design vector is correct for arbitrary sample IDs - samples sorted alphabetically by importIsoformExpression; half the labels wrong -> 0/20 planted recovered, no warning
- [FAIL] The Skill tells the agent how to handle batch/covariates - no mention; ISAR accepts extra designMatrix columns
- [PASS] Adding a batch column removes the batch artefacts without losing planted switches - artefact genes called 19/30 -> 0/30; planted 20/20 (4 other null FP)
- [PASS] Perfect confounding is caught explicitly - 'The supplied design matrix will result in a model matrix that is not full rank'

### Input 6 - Scope Boundary
**Prompt (realistic request):** swish / tximeta / count-only import.

**Executed:** true - Ran run/60_input6_swish.R: real Salmon Gibbs (20 reps) chrX 2 v 2; SYNTHETIC 6 v 6 with planted DTE truth and Poisson-resampled 'inferential replicates'; count-only importRdata. tximeta -> linkedTxome match FAILED in this env (Salmon 2.7 index metadata, 'Unknown or uninitialised column sha256'), so rowData(se)$gene_id/tx_id lines were not executed on real tximeta output; that line was tested on a SIMULATED CharacterList rowData.

**Code:** run/60_input6_swish.R; log 60_input6.log

**Output (trimmed):**
```
tximeta linkedTxome: 'couldn't find matching transcriptome' (Salmon 2.7 index metadata), rowData empty -> gene_id lines not executed
SIMULATED CharacterList gene_id: data.frame() gives gene_id.group, gene_id.group_name, gene_id.value columns
swish(y, x='condition'): ERROR is.factor(condition) is not TRUE (default data.frame coldata)
real 2v2 swish: 391 tested, 6 q<0.05 ; 24 permutations available
synthetic 6v6: 33/35 planted DTE-up called (all log2FC>0), FP 29/848
count-only importRdata: planted 20/20, null FP 2
```

**Scores:** Basic 28/40 | Specialized 41/60 | Total 69/100

**Assertions:**
- [FAIL] The Skill's tximeta-based first lines give a transcript table usable by dmDSdata - not executable on real tximeta output here; SIMULATED CharacterList gene_id -> data.frame gives gene_id.group/.group_name/.value columns
- [FAIL] swish(y, x='condition') runs as written - 'is.factor(condition) is not TRUE' with a default data.frame coldata; Skill leaves coldata undefined
- [PASS] swish recovers planted DTE-up transcripts in the right direction - 33/35, all log2FC>0
- [PASS] swish false-positive rate <=5% on non-DTE transcripts - 29/848 = 3.4%
- [PASS] Count-only importRdata (the Skill's long-read route) recovers the planted switches - 20/20, 2 null FP

### Input 7 - Adversarial
**Prompt (realistic request):** Unreplicated, mismatched annotation, Common Errors.

**Executed:** true - Ran run/70_input7_adversarial.R on SYNTHETIC quants: 1 v 1 design; Ensembl-style '.1' version suffix on quant IDs against an unversioned GTF; real chrX GTF against synthetic quants; then each Common Errors row triggered and the real message recorded.

**Code:** run/70_input7_adversarial.R; log 70_input7.log

**Output (trimmed):**
```
1v1: ERROR A statistical test cannot be performed without replicates.
'.1'-versioned quant IDs v unversioned GTF: ERROR ... Jaccard similarity < 0.925 ... Only 0 overlap
real GTF v synthetic quants: same error, 900 quantified v 6001 annotated
analyzeIUPred2A(missing): ERROR (At least on of) the file(s) ... does not exist ; analyzeSignalP(missing): ERROR The file(s) ... does not exist
scaleInfReps/swish(no infReps): ERROR there are no inferential replicates in the assays of 'y'
dmFilter impossible thresholds: ERROR !No genes left after filtering!
isoformSwitchTestDEXSeq(reduceToSwitchingGenes=TRUE, no switches): ERROR No genes were considered switching with the used cutoff values
```

**Scores:** Basic 29/40 | Specialized 40/60 | Total 69/100

**Assertions:**
- [PASS] An unreplicated 1 v 1 request is refused rather than reported as significant switches - ISAR: 'A statistical test cannot be performed without replicates'; not from the Skill text
- [PASS] A wholly wrong annotation is rejected with a clear error - Jaccard similarity < 0.925, 0 overlap, message names the mismatch
- [FAIL] The Skill's remedy for annotation mismatch fixes the common Ensembl version-suffix case - quant IDs 'X.1' v GTF 'X' -> error; fix is ignoreAfterPeriod, not rebuilding the index
- [FAIL] Error strings in the Common Errors table match what the tools print - dmFilter: '!No genes left after filtering!'; analyzeIUPred2A: 'file(s) ... does not exist'; swish: 'there are no inferential replicates in the assays'; consequences: 'No genes were considered switching...'

## Research Veto (Category 3)
M1 PASS | M2 PASS | M3 PASS | M4 PASS (details in the JSON). No safety or scope assertion failed.

## Recommendations

- **[P1] Manual DTU pipeline stops at samples(d) after library(DEXSeq)** (inputs [2]): Biobase::samples masks DRIMSeq::samples, so model.matrix(~ condition, data = samples(d)) and sampleData = samples(d) fail with 'unable to find an inherited method' (verified with the Skill's exact library order, DRIMSeq 1.34.0, DEXSeq 1.52.0). Fix: Write DRIMSeq::samples(d) in both places (or drop the unused design_full line) and state the masking.
- **[P1] Default count route silently changes DTU results; shipped example stops on real data** (inputs [3]): importIsoformExpression defaults (scaledTPM counts) followed by isoformSwitchTestDEXSeq found 0 switches on real chrX 2v2 (RPL10 dIF -0.33, q=1) while raw NumReads or lengthScaledTPM found 26 isoforms in 20-22 genes; run_switch_analysis in the example then stops with 'No genes were considered switching'. The Skill never discusses count v abundance scaling. Fix: Add a short section: which count route the tests use, compare calculateCountsFromAbundance=TRUE/FALSE on the user's data, and wrap the test in a check that reports zero switches instead of erroring; run the example on the shipped test data.
- **[P1] Shipped example is a banner plus functions that do not run in the order given** (inputs [3, 4]): Run as shipped it prints one line. Calling its functions: extract_sequences fails on GTF without CDS (ORFs not yet predicted) and when the output directory does not exist; analyze_consequences fails because intron_retention needs analyzeAlternativeSplicing() (SKILL.md calls it, the example does not) and signal_peptide_identified needs SignalP; annotation.gtf/transcripts.fa are hard-coded. Fix: Make the example runnable on a bundled toy dataset: analyzeORF before extractSequence when the GTF has no CDS, dir.create the output, add analyzeAlternativeSplicing, and build the consequence list only from annotators that were imported.
- **[P1] Consequence workflow order and annotator formats are wrong or missing** (inputs [4]): SKILL.md runs extractSequence before analyzeORF (fails without CDS); says analyzeSwitchConsequences 'silently drops' consequence types with no annotation, but it errors ('the result of the SignalP analysis must be available'); names hmmscan for Pfam but analyzePFAM needs pfam_scan-style rows containing a CL clan (raw --domtblout fails); calls analyzeORF(longest) unconditionally, which overwrote annotated ORFs on real chrX (PTC v Ensembl NMD biotype sens 0.96 -> 0.64, spec 1.00 -> 0.89); CPC2 removeNoncodinORFs=TRUE removed 2/10 planted poison isoforms from the NMD call. Fix: Give the exact order (addAnnotatedORFs/ analyzeORF first when needed), the pfam_scan or web-server format analyzePFAM expects, the real failure text for missing annotators, and a warning that CPC2 filtering can drop PTC-bearing isoforms; use annotated ORFs when the GTF has CDS.
- **[P1] Design construction is positional and ignores replicates and batch** (inputs [1, 5, 7]): The design vector is hard-coded positionally against colnames(counts)[-1] (alphabetical): with SRR-style IDs it mislabels half the samples and recovered 0/20 planted switches with no warning. The Skill gives no minimum-replicate guidance (1v1 only stops through ISAR's own error) and does not mention that ISAR accepts a batch column (batch-confounded data: 19/30 artefact genes called without it, 0 with it). The 3v3 example uses satuRn although the Skill's own rule and ISAR's warning say DEXSeq for <=5 replicates. Fix: Build the design by joining sample metadata on sampleID, add a batch/covariate line, state n>=3 per condition and choose DEXSeq for <=5 replicates in the example call.
- **[P2] dmFilter 'default too strict' claim is wrong; thresholds hard-coded for 6 samples** (inputs [3]): DRIMSeq 1.34.0 dmFilter defaults are all 0 (no filtering); the quoted 3/10 values are the Skill's own example. min_samps_gene_expr=6 errors on n=4 with a cryptic message. Fix: Say these are suggested values, scale min_samps_* to group sizes.
- **[P2] Common Errors table is paraphrased and partly misdirected** (inputs [7]): Real messages: 'The annotation and quantification ... seems to be different (Jaccard similarity < 0.925)', '!No genes left after filtering!', 'No genes were considered switching with the used cutoff values' (at the test step), 'there are no inferential replicates in the assays'. Version-suffixed IDs need ignoreAfterPeriod, not a new Salmon index. Fix: Quote the real text and the right argument.
- **[P2] ISAR v2 claims (auto-select satuRn, long-read/single-cell mode, 2.11+) not verifiable** (inputs [1, 6]): Installed ISAR 2.6.0 (Bioc 3.20) has no auto-selection wrapper and no long-read/single-cell argument; the bioRxiv paper (Han et al 2025, 10.64898/2025.12.08.693027) exists but the version pin 2.11+ does not correspond to an installable Bioconductor release here. Fix: Name the exact version/branch, or describe the explicit isoformSwitchTestSatuRn/DEXSeq choice.
- **[P2] swish/tximeta snippets are incomplete** (inputs [6]): coldata is undefined and its condition column must be a factor for swish; rowData(se)$gene_id from tximeta is a CharacterList so the txdf data.frame() line misbehaves (simulated); infRV filtering is described but no code; tximeta needs a linkedTxome matching the Salmon index. Fix: Show coldata construction with factor(), unlist the gene_id, and add computeInfRV().
- **[P2] Small factual points and licence gating** (inputs []): STMN2 cryptic exon is a premature-polyadenylation truncation, not PTC-NMD like UNC13A; the '~22% escape NMD' figure is not verified; SignalP, IUPred2A and DeepTMHMM are licence/cloud-gated and not flagged; SKILL.md is 440 lines with no references/ and a repeating usage-guide. Fix: Correct the STMN2 mechanism, cite the figure or drop it, flag the gated tools, move detail into references/ and dedupe the usage guide.

## Clean-up checks
Nothing written inside `F:\OpenScience\external\`; `find <clone> -name __pycache__` returned nothing. Copied Skill under `run/skill`. No symlinks in `run/`. Large intermediates (.rds, real GTF/FASTA copies) deleted.
