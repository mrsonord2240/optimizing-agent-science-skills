> **Audit record for `bio-isoform-switching`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@306e225](https://github.com/mrsonord2240/bioSkills/tree/306e225a1d72aaa5b70504efc068cce0b4743416/alternative-splicing/isoform-switching) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-isoform-switching (RE-AUDIT of the fixed Skill)

Generated: 2026-09-20 | source: `mrsonord2240/bioSkills@306e225a1d72aaa5b70504efc068cce0b4743416:alternative-splicing/isoform-switching` (read from worktree `wt/as-isoswitch`, copied to `run/skill`, never run in place) | Category 3 Data Analysis | Mode D (SKILL + runnable example + converter) | Complex, N=8 (6 regression, 2 new)

**Pre-fix 66 (Beta Only, not deployable) -> now 82 (Limited Release, deployable).** No veto, no open P0, one open P1, five P2. Executed 8/8 inputs (unrun parts named below).

Everything below is from my own runs. `run/` holds every script and log (`run/99_run_order.sh` gives the order). Synthetic data (labelled SYNTHETIC, planted truth): `run/data/synth` (regression set, seed 20260920), `run/data/new1` (4 v 7, seed 8801), `run/data/new2` (5 v 5, seed 8802). Real data: nf-core rnasplice chrX, 2 GBR v 2 YRI (Salmon quants, Gibbs samples, GRCh37 GTF/FASTA) from `audit-envs/alternative-splicing/public-data`. Every R block of SKILL.md was extracted by `run/03_extract_blocks.py` and executed verbatim.

## Summary Table

| Input | Type | New? | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Canonical | regression | yes | 36 | 52 | 88 | 5/5 | ✅ |
| 2 | Variant A | regression | yes | 35 | 50 | 85 | 5/5 | ✅ |
| 3 | Edge (real chrX) | regression | yes | 32 | 46 | 78 | 4/5 | ✅ |
| 4 | Variant B (consequences) | regression | yes | 33 | 49 | 82 | 5/5 | ✅ |
| 5 | Stress + adversarial | regression | yes | 32 | 47 | 79 | 3/4 | ✅ |
| 6 | Scope boundary (swish/tximeta) | regression | yes | 34 | 49 | 83 | 5/5 | ✅ |
| 7 | Adversarial: count-route mechanism | **new** | yes | 31 | 45 | 76 | 4/5 | ✅ |
| 8 | Stress: 4v7 batch design | **new** | yes | 36 | 52 | 88 | 5/5 | ✅ |

**Execution Average 82.4/100** | **Assertions 36/39 (92%)** | Static 82 x 0.4 = 32.8 | Dynamic 82.4 x 0.6 = 49.4 | **FINAL 82 - Limited Release**

Floors for Limited Release all met (static 82 >= 70, exec 82.4 >= 75, Layer 1 avg 33.6 >= 28, Layer 2 avg 48.8 >= 42, assertions 92% >= 80%). The score, not a floor, keeps it below Production Ready (85).

## Pre-fix v now (what regressed, what moved)

| Pre-fix finding | Re-run here | Result |
|---|---|---|
| Manual pipeline stops at `samples(d)` | block executed verbatim (input 2) | runs; masking message reproduced (`find('samples')` = Biobase, DRIMSeq); 27 genes, 20/20 planted |
| Default count route finds 0 switches on real chrX; example stops | input 3, 7 | raw route 26 isoforms/20 genes, RPL10 q 4.6e-18; default 0; example exits cleanly at zero switches |
| Example is a banner + functions that do not run | inputs 3, 8 | runs end to end (demo, real chrX, my 4v7 set) |
| extractSequence before ORFs; hmmscan raw file rejected; `analyzeORF` overwrites CDS; CPC2 filter drops PTC isoforms | input 4 | all four now stated correctly and reproduced (order error text, converter, 0.96 -> 0.64, 10/10 v 8/10) |
| Positional design vector (0/20 on SRR IDs); no batch / replicate guidance | inputs 1, 5, 8 | name-keyed design: 20/20 on shuffled IDs; batch line works; 1v1 stops |
| dmFilter "default too strict"; Common Errors paraphrased | inputs 5, 6, 2 and `run/65` | dmFilter defaults now correct; all 14 Common Errors rows re-triggered and match |
| Nothing regressed: every pre-fix PASS still passes (dIF vs hand 7.32e-05 over 871 isoforms is byte-for-byte the pre-fix number) | | |

## Step 1 - Skill Veto
T1 PASS (every block, the example and the converter ran; failures were only ones I triggered on purpose) | T2 PASS (frontmatter name, description, tool_type, primary_tool, license) | T3 PASS (demo run twice: identical "35 isoforms in 14 genes", 14/14, 8/8; regression numbers identical to the pre-fix audit's; seeds fixed) | T4 PASS (no eval/exec of user strings, no credentials; example validates metadata; converter validates input).

## Step 2 - Static (82/100)

| Category | Score | Note |
|---|---|---|
| functional_suitability | 10/12 | Covers the whole promised surface. Every quoted number I re-derived reproduced except specificity after `analyzeORF` (0.95 measured, 0.89 stated) and the factor max (576 by EffectiveLength, 205 stated). Attributes an "auto-selecting wrapper" to the 2025 preprint, whose abstract does not say so. |
| reliability | 10/12 | 14 real error messages, all re-triggered and matching. Block's metadata check names no sample. n=2 false-positive behaviour not warned. |
| performance_context | 5/8 | 491 lines / 37 KB in one SKILL.md, no references/. Linear workflow. |
| agent_usability | 14/16 | Ordered steps, expected numbers and error text at each checkpoint; count-route section needs a second read. |
| human_usability | 6/8 | Natural trigger language; strict validation is by design; one opaque `stopifnot`. |
| security | 11/12 | No credentials, no eval, local only; inputs validated in example and converter. |
| maintainability | 10/12 | Blocks extract and run verbatim; example self-asserts. Provenance ("audit:") leaks into instructions. |
| agent_specific | 16/20 | Precise trigger; true scripts for the heavy logic; stop conditions present; no references/ split; n=2 caution missing. |

## The specific questions I was asked to judge

**Manual DTU pipeline (`samples(d)` masking; DEXSeq recovery vs DRIMSeq).** Fixed. `run/20_input2_manual_dtu.R` ran `blocks/r_03.R` verbatim on 6v6 with shuffled IDs: DEXSeq `perGeneQValue` < 0.05 in 27 genes = 20/20 planted + 1 null + 5 planted 0.15-shift + 1 planted 0.06-shift, exactly the composition the Skill states. stageR confirms the truly switching transcript 20/20. DRIMSeq (independent test) 27 genes, Jaccard 0.93. Null split 2 genes. 3v3 through the same block 25 genes, 20/20. The masking warning is real (`find('samples')` lists Biobase before DRIMSeq; the unqualified call fails with the quoted message) and `counts()` is also masked (DEXSeq, DESeq2, BiocGenerics).

**scaledTPM v raw counts (Skill: 0 v 26 on chrX, "consistent with length scaling, not proven").** I tested it four ways and the Skill's numbers and its hedge both hold, but the guidance is not fully safe.
- Reproduced (input 3): raw 26 isoforms/20 genes (RPL10 q 4.6e-18), lengthScaledTPM 28/22, scaledTPM 0/0, dtuScaledTPM 0/0, ISAR default 0/0 (RPL10 q 1). The manual DRIMSeq/DEXSeq pipeline: 13/13/2 (DEXSeq) and 11/11/7 (DRIMSeq) for raw/lengthScaled/scaledTPM, overlap 7 (input 7D).
- Cause tests (input 3C): raw x median(len)/len -> 0 switches; the same factors permuted across isoforms -> 34; sqrt of the factor -> 17 (a dose-response); factors applied but gene totals restored to raw -> still 0; per-sample constants only -> 25. So the loss comes from the isoform-specific length factor inside a gene, not from gene totals or library scaling. ISAR's wrapper rounds counts and uses per-isoform BH `padj` (source read, `run/64`). "Consistent with, not proven" is the honest wording.
- The Skill's remark that a clean simulation will not reveal it also holds, more strongly than it says: on my own sets (isoforms 0.5-5.4 kb, factor 0.35-3.5) **every** route, default included, recovered 20/20 with 0/195 null FP for DEXSeq (5v5) and satuRn (4v7) (input 7A/7B). Only the extreme factors of real data (0.02-18 by Length, up to 576 by EffectiveLength) break it.
- satuRn across routes (unrun by the fixer): ISAR's satuRn wrapper found 0 switches on real chrX 2v2 with either route (RPL10 q 0.40 raw, 0.11 default). The Skill says it was not compared; that gap is honest.
- **Where the guidance is not safe (P1):** the raw route is presented as the one that works because the default "lost every call". Nothing checks that raw is right. Input 7E ran the three possible 2v2 label splits: the true GBR v YRI split gave 26 isoforms/20 genes; the two mixed-population splits (no population signal) gave **11 and 15 genes** with raw counts (1 of 20 genes shared with the true split); the default route gave 0 in all three (min q = 1), i.e. it has no power on this data whatever the labels. At n=2 the raw calls are largely individual-level variation, so the Skill's "underpowered" framing misses that they can be anti-conservative. The Skill does tell users to compare routes and inspect `switchPlot`, but gives no null.

**Rewritten example, end to end.** Runs from a copy. Demo (no arguments, ~65 s): 35 isoforms in 14 genes, 14/14 planted, 0 other genes, NMD-sensitive genes = the 8 planted poison genes, PDF > 5 kB, "DEMO OK", identical on a second run. Real chrX (metadata rows shuffled): 26 isoforms/20 genes, annotated ORFs (1281), consequence types only from what exists, `switchPlot_RPL10.pdf`. Mixed labels: 11 isoforms (see above). Missing sample: stops with "only in quant: ERR204916". On my own 4v7 batch set in real-data mode (input 8): 38 isoforms in 20 genes = 20/20 planted, 0 non-planted, batch kept as covariate, ORFs predicted (no CDS in the GTF), NMD-sensitive up in 10/10 poison genes.

**Name-keyed design (shuffled IDs).** Inputs 1, 5, 8: SRR-style IDs and metadata rows shuffled; the block recovers 20/20 (3v3 DEXSeq, 6v6 satuRn, 4v7 satuRn) with dIF within 0.1 of truth 20/20 (19/20 when the batch column is used, as the Skill warns the covariate changes dIF). The pre-fix positional vector gave 0/20. One weakness: the block's `stopifnot(setequal(...))` names no sample when metadata and quantification disagree (the example does).

**`examples/hmmscan_to_pfamscan.py`.** 60/60 rows are column-identical to an independent parse of the domtblout (`run/63_converter_checks.sh`); Pfam-A.clans.tsv.gz fetched exactly as the Skill says; plain and gzipped clans files give identical output; no args prints the docstring (rc 1); missing clans file is a raw FileNotFoundError; a non-domtblout line stops with a clear message; an empty domtblout writes an empty file with a warning. `analyzePFAM` accepted it on synthetic (60 rows) and real chrX (264 rows, 69 isoforms); raw domtblout is rejected as stated. **NMD and domain checks:** poison isoform B NMD-sensitive and up 10/10 (8/10 with `removeNoncodinORFs = TRUE`, as the Skill says), 0 NMD calls outside poison genes; "Domain loss" A-down/C-up 10/10, 0 calls elsewhere, PF00240 never in an isoform C; 0 intron-retention calls where none were planted. Real chrX: annotated-ORF PTC flag v Ensembl `nonsense_mediated_decay` biotype sensitivity 0.96 (48/50), specificity 1.00 (1023/1028) on the unfiltered import (the Skill's number, reproduced); after `analyzeORF('longest')` over annotated ORFs 0.64 (32/50) and specificity 0.95 (Skill says 0.89; the direction and the sensitivity drop are confirmed).

**usage-guide.md dedup.** Nothing needed is lost. I checked every pre-fix item against SKILL.md: prerequisites -> Version Compatibility install block; "What the Agent Will Do" -> ordered workflow + consequence steps; tips (stageR, poison-exon direction, satuRn/DEXSeq rule, long-read, GENCODE basic v comprehensive, swish Gibbs, single-cell, TDP-43 tissue) -> stageR semantics, AS-NMD, Tool Selection, Decision tree/Pitfalls, swish failure mode, Single-Cell DTU, Disease examples. The guide is now a thin prompt list plus pointers.

**SKILL.md at 491 lines / 37 KB - loadable and usable?** Yes: valid frontmatter, one linear file, every code block runs verbatim. It is heavy (about 9-10k tokens) with no references/; the count-route, consequence-order and Common Errors sections are the natural split (P2).

**Hedging on what was not run.** tximeta rowData: I confirmed the Skill's account exactly (`makeLinkedTxome` ok; `tximeta(coldata)` returns an SE with 0 rowData columns and the message "couldn't find matching transcriptome", warning "Unknown or uninitialised column: sha256"; `run/61`) - well hedged. SignalP / IUPred2A / NetSurfP-2 / DeepTMHMM: each is marked "not run" or "read from source" in the tool table; their missing-file errors ("The file(s) ... does not exist") and the missing-SignalP consequence error are real and quoted correctly. satuRn across routes: see above. One unverifiable statement: the Skill says the Han 2025 preprint "describes an auto-selecting DTU wrapper and long-read/single-cell modes"; the bioRxiv abstract (fetched) says only that the standard workflow is now suited to long-read and single-cell data. Installed 2.6.0 exports just `isoformSwitchTestDEXSeq`/`isoformSwitchTestSatuRn`, each warning on replicate count, and NEWS shows `importRdata(detectUnwantedEffects = TRUE)` plus covariate correction of IF (the mechanism the Skill calls "not traced").

## Detailed Outputs (trimmed; full logs beside the scripts)

### Input 1 - Canonical (regression) - 88
Skill block `r_01.R` verbatim; synthetic 3v3 with shuffled SRR IDs and shuffled metadata rows, 6v6, and a control-v-control null. `run/10_input1_canonical.R`, log `10_input1.log`.
```
[PASS] 3v3 ISAR dIF == hand-computed dIF from quant.sf TPM | max abs diff 7.32e-05 over 871 isoforms
[3v3 DEXSeq] tested 300 genes | planted 20/20 | null FP 2 (GENE175,GENE206) | dge_only 0 | small(0.06) 0 | dte_like(0.15) 3
[PASS] direction correct, dIF within 0.1 of truth | dir 20/20 mag 20/20
6v6 test branch used: satuRn | planted 20/20 | null FP 0 | dir 20/20 mag 20/20
[PASS] NULL comparison (ctrl v ctrl 3v3, DEXSeq) <=3 genes called | 1 genes / 300 tested; min q 0.00337
```

### Input 2 - Variant A, manual DTU (regression) - 85
`run/20_input2_manual_dtu.R` (block `r_03.R` verbatim), log `20_input2.log`.
```
block finished; result columns: geneID,txID,gene,transcript | rows 700
find('samples'): .GlobalEnv,package:Biobase,package:DRIMSeq | find('counts'): package:DEXSeq,package:DESeq2,package:BiocGenerics,package:DRIMSeq
[PASS] unqualified samples(d) fails after library(DEXSeq) | unable to find an inherited method for function 'samples' for signature 'object = "dmDSdata"'
DEXSeq gene q<0.05: 27 genes | planted 20/20 | null 1 | dge_only 0 | small(0.06) 1 | dte_like(0.15) 5
[PASS] stageR confirms the truly switching transcript in >=19/20 planted genes | 20/20
DRIMSeq: 27 genes, planted 20/20, Jaccard with DEXSeq 0.93
null split gene calls: 2 | stageR confirmed transcripts: 3 ; 3v3 manual DEXSeq: 25 genes, planted 20/20
```

### Input 3 - Edge, real chrX (regression) - 78
`run/30_input3_real_chrX.R`, `35_example_runs.sh`, `71_real_label_permutation.R`, `72_efflen_factor.R`.
```
Skill block: 26 isoforms in 20 genes | RPL10 ENST00000406022 dIF -0.3291 q 4.63e-18   (hand: -0.3356)
ISAR default (calculateCountsFromAbundance=TRUE)     0 isoforms / 0 genes | RPL10 q 1
ISAR calculateCountsFromAbundance=FALSE (Skill)     26 isoforms / 20 genes | RPL10 q 4.63e-18
tximport lengthScaledTPM 28 / 22 (q 1.91e-18) | scaledTPM 0 / 0 | dtuScaledTPM 0 / 0
raw x median(len)/len 0 | same factors permuted 34 (24 genes) | per-sample constants 25 | sqrt(factor) 17 | length-scaled, gene totals restored 0
plain DEXSeq on ISAR-default counts: perGeneQ RPL10 = 1 (not 0), isoform padj all 1
true_GBR_v_YRI raw 26 iso / 20 genes | default 0 ;  mixed1 raw 11 / 11 genes | default 0 ;  mixed2 raw 19 / 15 genes | default 0
raw-route genes of the true split also called in a mixed split: mixed1 1/20; mixed2 1/20
example real mode: 26 isoforms in 20 genes, ORF origin Annotation 1281, plot switchPlot_RPL10.pdf (7 kB); bad metadata: "only in quant: ERR204916"
length factor: Length 0.023-18.1; EffectiveLength 0.019-575.8 (Skill: 0.019-205)
```
Assertion 5 FAIL: the Skill's n=2 / raw-route wording has no null (see P1). Note: my plain-DEXSeq check on the ISAR default counts gives RPL10 perGeneQ = 1; the fixer reported 0 for the tximeta scaledTPM manual path (different filter), so that comparison is route-specific, not a contradiction.

### Input 4 - Variant B, consequences (regression) - 82
`run/40a_input4_prep.R`, `40b_external.sh` (CPC2 + hmmscan in WSL), `40c_consequences.R`, `40d_real_consequences.R`, `41_orf_overwrite_check.R`, `63_converter_checks.sh`.
```
[PASS] NMD_status flags poison isoform B NMD-sensitive and up in 10/10 poison genes | 0 calls outside poison genes
[PASS] domains_identified 'Domain loss' A->C 10/10, quiet elsewhere | PF00240 20 rows in 10 genes, never in _C
removeNoncodinORFs = TRUE: NMD-sensitive B up in 8/10 poison genes (CPC2 labels B of GENE001 and GENE006 noncoding)
[PASS] raw hmmscan --domtblout rejected: "more columns than column names"
[PASS] extractSequence before ORFs (no-CDS GTF): Please run the 'addORFfromGTF()' ... function(s) to detect ORFs
converter: 60 rows, 0 mismatching columns vs independent domtblout parse; real chrX 264 rows, analyzePFAM 69 isoforms
real chrX unfiltered: annotated ORFs sens 0.96 (48/50) spec 1.00 (1023/1028) | after analyzeORF('longest') sens 0.64 (32/50) spec 0.95 (974/1028) | orf_origin Predicted 1738
```
Not run: SignalP, IUPred2A, NetSurfP-2, DeepTMHMM.

### Input 5 - Stress + adversarial (regression) - 79
`run/50_input5_stress_adversarial.R`, `65_common_errors_rest.R`.
```
no batch column   planted 20/20 | batch-artefact genes 11/30 | other null FP 0
batch column      planted 20/20 | batch-artefact genes  0/30 | other null FP 5
[PASS] batch == condition: "The supplied design matrix will result in a model matrix that is not full rank"
[PASS] constant batch: "In the designMatrix the following column(s): batch Contain constant information"
[PASS] 1v1: "A statistical test cannot be performed without replicates."
[PASS] '.1' IDs: Jaccard similarity < 0.925 ; with ignoreAfterPeriod = TRUE in BOTH calls: imported 875 isoform rows
[PASS] No genes were considered switching with the used cutoff values (reduceToSwitchingGenes = TRUE)
metadata missing one sample -> "setequal(ids, meta$sample_id) is not TRUE"   (assertion 4 FAIL: no sample named)
run/65: analyzeSignalP/IUPred2A missing file, dmFilter (both messages), swish without infReps: all match the Skill's rows
```

### Input 6 - Scope boundary, swish/tximeta (regression) - 83
`run/60_input6_swish.R`, `61_tximeta_warning.R`.
```
swish real 2v2: 391 tested | q<0.05: 6 | infReps 20 ; top ENST00000380861 log2FC -1.45 q 0.00694 ; median meanInfRV 0.69
infRV filter y[mcols(y)$meanInfRV < 1, ]: 231 of 391 kept ; character condition -> is.factor(condition) is not TRUE
tximeta linkedTxome: SE returned, 0 rowData columns; "couldn't find matching transcriptome, returning non-ranged SummarizedExperiment"
synthetic 6v6 swish: 62 called | TP 33/35 (all log2FC>0) | FP 29/848 ; count-only importRdata: planted 20/20, null FP 2
```

### Input 7 - Adversarial, count-route mechanism (NEW) - 76
`run/70_input7_new_count_route.R`, `71_real_label_permutation.R`, `62_isar_news.R`, `64_isar_source_dump.R`.
```
7A synthetic 5v5 (0.5-5.4 kb; factor 0.35-3.06), DEXSeq: raw / default / lengthScaledTPM / scaledTPM / dtuScaledTPM / emulated -> 20/20, null FP 0/195 each
7B synthetic 4v7, satuRn: raw / default / emulated -> 20/20, null FP 0/195 each
7C real chrX 2v2: satuRn wrapper raw 0 (RPL10 q 0.404), default 0 (q 0.113); DEXSeq wrapper raw 26 / default 0
7D manual block: countsFromAbundance no 13 (DRIMSeq 11, overlap 7) | lengthScaledTPM 13 (11, 7) | scaledTPM 2 (7, 1)
7E label permutation: see input 3
ISAR 2.6.0: exports isoformSwitchTestDEXSeq, isoformSwitchTestSatuRn; importRdata detectUnwantedEffects default TRUE; NEWS: "importRdata() now automatically corrects abundance and isoform fractions for unwanted covariates"
```
Assertion 5 FAIL (same P1 as input 3).

### Input 8 - Stress, 4v7 batch design (NEW) - 88
`run/04_gen_new.R` (seed 8801), `80_input8_new_unbalanced.R`, `81_input8_example.sh`, `82_eval_example_new.R`.
```
[4v7 satuRn, no batch column] tested 250 genes | planted 20/20 | batch-artefact genes 0/20 | other null FP 0/195 | dir 20/20 mag 20/20
[4v7 satuRn, batch column]    planted 20/20 | other null FP 0/195 | mag 19/20 ;  [4v7 DEXSeq forced, batch] planted 20/20 mag 19/20
[null split 3v4 among treatment samples, DEXSeq, batch] 4 of 250 genes called (1.6%)
example (real-data mode): 38 isoforms in 20 genes | planted 20/20 | other genes 0 | NMD_status up in 10/10 poison genes | PDF written
```
My batch effect (0.15 dIF diluted by the imbalance) produced no artefacts without adjustment, so batch removal was tested only in input 5.

## Research Veto (Category 3)
M1 PASS (checked numbers reproduce; two small figures differ; citations checked against Crossref/bioRxiv where possible, the preprint attribution is unverifiable) | M2 PASS (research analysis only; SCN1A ASO stated as "in clinical development, phase not verified") | M3 PASS (no principled error; n=2 caution under-stated, P1) | M4 PASS (all code ran; only licence-gated annotator calls not run and labelled so). No safety or scope assertion failed.

## Recommendations

- **[P1] Raw-count route and n=2 presented without a null** (inputs 3, 7). On real chrX 2v2 the two mixed-population splits called 11 and 15 genes with raw counts (true split 20; 1/20 shared); the default route gave 0 everywhere. The Skill says the default "lost every call" and calls n=2 "underpowered". Fix: put the permutation result in the Count route section, say n=2 calls are exploratory and can be anti-conservative, recommend a label-shuffle check and >=3 replicates.
- **[P2] Block's sample-ID check is opaque** (input 5). Reuse the example's stop() message.
- **[P2] Preprint attribution and covariate mechanism** (inputs 7, 8). Cite the abstract's actual wording; replace "not traced in the source" with the NEWS statement and `detectUnwantedEffects`.
- **[P2] Small numeric mismatches and provenance text** (inputs 3, 4). Specificity 0.95 v 0.89; factor range by Length v EffectiveLength; dmFilter message quoted without its first clause; "audit" wording inside SKILL.md.
- **[P2] SKILL.md is 491 lines in one file.** Move Count route, consequence detail and Common Errors to references/.
- **[P2] Licence-gated annotators still unrun** (input 4). Keep the "not run" flags.

## Clean-up checks
Nothing written inside `F:\OpenScience\external\` or the worktree `wt\as-isoswitch`; the Skill was copied to `run/skill` and run from there (`find run -name __pycache__` empty). No symlinks in `run/`. `work/` (staged copies, .rds, sequences, real GTF/FASTA copies, ~150 MB) and `data/synthB` (rebuilt by `50_input5`) were deleted; `data/synth`, `new1`, `new2` (2 MB each, synthetic with planted truth) are kept. Pre-fix report archived under `_pre-fix-20260920` was not modified. `public-data\` not written.
