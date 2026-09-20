> **Audit record for `bio-differential-splicing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@44ff43b](https://github.com/mrsonord2240/bioSkills/tree/44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b/alternative-splicing/differential-splicing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-differential-splicing

Generated: 2026-09-20  |  Source: `mrsonord2240/bioSkills@44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b:alternative-splicing/differential-splicing`  |  Category: Data Analysis  |  Mode: D (hybrid)  |  Complexity: Complex, N=7

Env: `F:\OpenScience\audit-envs\alternative-splicing` (rMATS-turbo 4.4.0, leafcutter 0.2.9, SUPPA2 2.4, Shiba 0.8.2, regtools 1.0.0; MAJIQ/VOILA licence-gated, not installed). Data: planted exon-skipping set and a 120-gene simulation are **synthetic**; chrX 2v2 is **real** (GRCh37). All scripts are in `run\`.

## Skill Veto
T1 PASS, T2 PASS, T3 PASS, T4 PASS. Research Veto: M1-M4 PASS (MAJIQ code not executed, not counted).

## Static score (25 criteria)

| Category | Score | Note |
|---|---|---|
| functional_suitability | 8/12 | Core rMATS/leafcutter/SUPPA2 commands and output columns verified against installed tools (rMATS 4.4.0, leafcutter 0.2.9, SUPPA2 2.4, Shiba 0.8.2) and recover planted truth. Deductions: SUPPA2 -m classical advised for n<=3 has zero power; leafcutter n>=2/3 claim conflicts with default -i 5; --paired-stats prerequisite (PAIRADISE) missing; MAJIQ V3 block not executable here; no single-end (-t single) guidance. |
| reliability | 7/12 | Common Errors table exists, but the important failures are silent or unlisted: rMATS with wrong -t / readLength exits 0 with a header-only file; --paired-stats exits 0 with a header-only file; leafcutter_ds.R default flags stop at 3v3 with a message the Skill never mentions; group-file name mismatch gives "undefined columns selected". |
| performance_context | 6/8 | SKILL.md is 421 lines with no references/ directory; usage-guide.md repeats the tool summary. Workflow is otherwise linear. |
| agent_usability | 12/16 | Decision tree by design, thresholds table, output-column table and reconciliation table are clear and usable. Deductions: effect-size sign conventions are documented only for rMATS (SUPPA2 and leafcutter report group2-group1, Shiba alt-ref); Shiba invocation is left to an external website; leafcutter group-file name rule undocumented. |
| human_usability | 5/8 | Natural triggers (compare splicing between treatment groups, tissues, disease states). Little forgiveness: wrong -t/readLength/libType/-i values give empty or halted runs without guidance. |
| security | 11/12 | No credentials; system() call uses a fixed string; no eval of user strings. Minor: no input validation advice for file lists. |
| maintainability | 8/12 | Single monolithic SKILL.md plus a usage-guide and two examples; no test data or expected outputs; neither shipped example runs cleanly from a copy without edits. |
| agent_specific | 16/20 | Precise long description, good related-skill routing (outlier-splicing-detection for n=1 vs cohort), some out-of-scope routing; no stop condition for n=1 vs n=1 or for single-end data. |

**Static subtotal: 73/100**

## Summary table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 34 | 50 | 84 | 2/4 | ✅ COMPLETED |
| 2 | Variant A | yes | 31 | 44 | 75 | 2/4 | ⚠️ COMPLETED |
| 3 | Edge | yes | 32 | 46 | 78 | 3/5 | ⚠️ COMPLETED |
| 4 | Variant B | yes | 28 | 38 | 66 | 1/4 | ⚠️ COMPLETED |
| 5 | Stress | yes | 35 | 52 | 87 | 3/5 | ✅ COMPLETED |
| 6 | Scope Boundary | no (partial) | 27 | 36 | 63 | 2/4 | ❌ PARTIAL |
| 7 | Adversarial | yes | 26 | 36 | 62 | 1/4 | ❌ COMPLETED |

**Execution average: 73.6/100**  |  **Assertion pass rate: 14/30**  |  Layer 1 avg 30.4/40, Layer 2 avg 43.1/60

**Final = 73 x 0.4 + 73.6 x 0.6 = 29.2 + 44.2 = 73.4 -> 73 : ⚠️ Beta Only**; deployable = False; veto override = False. Executed inputs: 6/7 fully executed (Input 6 partial: MAJIQ not executed; --paired-stats attempted and failed).

Floors: Static 73 (<80 PR, >=70 LR), Execution avg 73.6 (<75), so Beta Only regardless of the numeric rounding.

## Test inputs and outputs

### Input 1 - Canonical: rMATS-turbo 3v3 on planted exon-skipping set + Skill filter snippet + shipped example

**Prompt:** I have n=3 vs n=3 RNA-seq BAMs; run rMATS-turbo with FDR<0.05 and |dPSI|>0.10, then filter for >=10 junction reads per replicate. (planted exon-skipping set; also run the shipped rMATS example from a copy)

**executed:** true  
**What ran and what it printed:** Ran on WSL as-core, rMATS-turbo 4.4.0. Planted single-end 3v3: adapted command (-t single --readLength 50 --novelSS --cstat 0.05) gave IncLevel1 0.8,0.8,0.769 / IncLevel2 0.2,0.2,0.208, IncLevelDifference +0.587 (truth 0.586966), FDR 1.2e-26; swapping --b1/--b2 gave -0.587 (sign claim verified). SKILL.md command verbatim (-t paired --readLength 150 --libType fr-firststrand) on the single-end data: rc 0, 0 events, header-only file. SKILL.md pandas filter ran; assertion (1 event, dPSI 0.587, min_inc 20, min_skip 10) printed ASSERT OK. Shipped examples/diff_splicing_rmats.sh from a copy on real chrX 75 nt reads: as shipped (READ_LENGTH=150) rc 0, prints "analysis complete", SE.MATS.JC.txt has 0 rows; with READ_LENGTH=75 it gives 197 SE events and its awk filter (no coverage filter) lists 4 hits whose counts are 0-3 reads.

**Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100

**Assertions:**
- [PASS] rMATS recovers the planted dPSI (0.587 +/- 0.002) with the documented b1-b2 sign - IncLevelDifference 0.587; -0.587 when b1/b2 swapped
- [PASS] SKILL.md filter (FDR<0.05, |dPSI|>0.10, per-rep coverage>=10) keeps the planted event and runs unmodified - ASSERT OK printed; 1 of 1 events kept
- [FAIL] SKILL.md rMATS command runs on the design given without silent failure - -t paired on single-end data: rc 0, header-only output; Skill never mentions -t single
- [FAIL] Shipped rMATS example produces results from a clean copy on real paired-end data - READ_LENGTH=150 on 75 nt reads: 0 SE rows, rc 0, "analysis complete" printed

### Input 2 - Variant A: leafcutter 3v3 on planted set, SKILL.md steps and shipped R example

**Prompt:** Use leafcutter Dirichlet-multinomial GLM on intron clusters from regtools junctions for annotation-free differential splicing. (planted 3v3; also the shipped R example)

**executed:** true  
**What ran and what it printed:** WSL as-core (regtools 1.0.0, clustering) + as-rleaf (leafcutter 0.2.9). regtools flags from SKILL.md (-a 8 -m 50 -s XS) accepted; junc scores 40,10,40. Clustering as documented gave 0 introns on contig chrP (script drops non-chr1-22/X/Y; -k True needed), then counts 40 44 38 10 12 9 etc. leafcutter_ds.R with the Skill's options (no -i) and 3v3: rc 1 "smallest group is less than min_samples_per_intron" (default -i 5); the Common-Errors flags --min_samples_per_intron 5 --min_samples_per_group 3 fail the same way. With -i 3: cluster p 4.0e-9, skipping-intron usage 0.118 vs 0.663, deltapsi +0.5446 (hand value 0.55). Group file with the Skill placeholder names s1..s6 -> "undefined columns selected". exon_file with columns chr,start,end,strand,gene_name labelled the cluster G1. leafcutter_ds.R is not on PATH after installing the R package. Shipped diff_splicing_leafcutter.R runs; its load_leafcutter_results()/annotate_clusters() work on real output (assert: 3 introns, max deltapsi 0.545) but the script writes a groups.txt (sample1..6) that cannot match the counts-table names, so its own pipeline stops with "undefined columns selected".

**Scores:** Basic 31/40 | Specialized 44/60 | Total 75/100

**Assertions:**
- [PASS] leafcutter recovers the planted skipping-intron shift (|deltapsi| ~0.55) at FDR<0.05 - deltapsi 0.5446, p.adjust 4e-9 with -i 3
- [FAIL] Documented command sequence runs at n=3 vs 3 with the flags given - default -i 5 stops; the -i/-g/-c flags are not mentioned; Common-Errors flags also stop
- [FAIL] Documented group-file recipe works with the counts table produced by the documented clustering step - sample names must equal junc basenames; s1..s6 / sample1..6 fail with "undefined columns selected"
- [PASS] Shipped R helper functions run on real leafcutter output and merge cluster with effect tables - ASSERT OK: 3 introns, max deltapsi 0.545

### Input 3 - Edge: Real chrX 2v2 (GBR vs YRI) across rMATS, leafcutter, Shiba, SUPPA2 + permuted control

**Prompt:** n=2 vs n=2 design (GBR vs YRI, real chrX): compare rMATS, leafcutter, Shiba and SUPPA2 and tell me which hits are trustworthy; include a permuted control.

**executed:** true  
**What ran and what it printed:** Real 2x75 nt data, 4 samples, GRCh37 (public-data\rnasplice; XS-tagged copies for leafcutter/Shiba). rMATS (-t paired --readLength 75 --variable-read-length --novelSS --cstat 0.05, unstranded): SE 226, A3SS 106, A5SS 90, MXE 20, RI 54 events; 9 events (7 genes) reach FDR<0.05 & |dPSI|>0.10 but 0 pass the Skill per-replicate coverage filter (min_inc+min_skip>=10), i.e. the coverage filter removes all low-count hits. With the Skill libType fr-firststrand on unstranded data SE events 226 -> 121 and summed junction counts 13,314 -> 5,570 (the "wrong libType halves junctions" pitfall verified). leafcutter with the Skill -m 50: 0 clusters on this ~100k-read subset; -m 10 -i 2 -g 2 -c 5: 13 clusters tested, 0 significant (real), 1 (permuted); default flags stop at 2v2. Shiba (shiba.py --mame, strand XS): 0 differential events real and permuted. SUPPA2 from Salmon TPM: empirical (-gc) 36 events / 32 genes at FDR<0.05 & |dPSI|>0.10 in the real comparison and 24 events / 23 genes in the permuted one; classical 0 in both (min p 0.22). Read-count tools agree there is nothing reliable at this depth; SUPPA2 empirical calls are the unstable ones, consistent with the Skill warning against n<=3.

**Scores:** Basic 32/40 | Specialized 46/60 | Total 78/100

**Assertions:**
- [PASS] All four documented tools run to completion on the 2v2 real data - rMATS, Shiba, SUPPA2 ok; leafcutter needs -i 2 -g 2 -c 5 and -m 10 on this depth
- [PASS] Skill coverage filter suppresses low-count rMATS hits - 9 FDR/dPSI hit events, 0 after min_inc+min_skip>=10
- [PASS] Skill wrong-libType pitfall is real - fr-firststrand on unstranded data: SE events 226 -> 121, counts -58%
- [FAIL] Skill n=2 guidance (leafcutter n>=2) works with the documented command - default flags stop at 2v2; need -i 2 -g 2 -c 5
- [FAIL] Shiba route in SKILL.md (snakemake -s snakeshiba.smk ... --use-singularity) runs as written - snakeshiba.smk lives in share/shiba-0.8.2-0, config needs a container key (KeyError line 58); shiba.py config.yaml is what ran

### Input 4 - Variant B: SUPPA2 diffSplice loop on synthetic 3v3 TPM (planted truth)

**Prompt:** I only have Salmon TPM for n=3 vs n=3; run the SUPPA2 differential splicing loop and report significant events. (synthetic sim with planted truth)

**executed:** true  
**What ran and what it printed:** WSL as-suppa (SUPPA2 2.4). SYNTHETIC 120-gene sim (24 strong + 6 weak planted dPSI, 90 no-change), TPM from the same molecules as the BAMs, 3v3. SKILL.md loop (generateEvents -f ioe -e SE SS MX RI; psiPerEvent; diffSplice -gc) ran. Empirical: 23/24 strong detected, 0/6 weak, direction 23/23 (SUPPA2 dPSI = cond2 - cond1, verified in diff_tools.py and on G000), 3 false positives among 26 calls (11.5% vs 5% nominal) all in low-coverage genes; null A vs C: 2 false positives. Classical (the Skill's advice for n<=3): 0/30 planted events detected, minimum p 0.064 before/at BH, null minimum 0.1. Cause verified in lib/diff_tools.py: classical = unpaired Mann-Whitney U, whose smallest two-sided p is 0.1 at 3v3 and 0.33 at 2v2; BH cannot lower it. TPM files must have a header of sample names only (undocumented); generateEvents on an SE-only annotation writes empty A5/A3/MX/RI files.

**Scores:** Basic 28/40 | Specialized 38/60 | Total 66/100

**Assertions:**
- [PASS] SUPPA2 empirical recovers planted strong events with correct direction - 23/24, 23/23 direction
- [FAIL] SUPPA2 empirical is roughly calibrated at n=3 on the null comparison - 2 FPs on A vs C; 3/26 calls false on A vs B (Skill itself warns 15-30% FDR)
- [FAIL] Skill advice "-m classical for n<=3" yields usable detections - 0/30 detected; Mann-Whitney min p is 0.1 at 3v3
- [FAIL] Skill table entry SUPPA2 classical "min reps n>=2" is a usable minimum - no p<0.33 is reachable at n=2 and none <0.1 at n=3

### Input 5 - Stress: Synthetic 120-gene simulation, 3v3 and 2v2, rMATS/leafcutter/Shiba, null and planted

**Prompt:** Run rMATS and leafcutter (and Shiba) on my 3v3 and 2v2 data, require concordance, and tell me the false-positive behaviour. (synthetic 120-gene sim, planted + null)

**executed:** true  
**What ran and what it printed:** SYNTHETIC data (run/make_sim.py): 24 strong (|d| 0.3-0.5) + 6 weak (0.15) planted DS genes, 70 no-change genes, 20 low-coverage no-change genes; A vs B truth, A vs C null. 3v3: rMATS (Skill flags; FDR<0.05,|dPSI|>0.10, per-rep coverage >=10) 24/24 strong, 0/6 weak, direction 24/24, 0 false positives (without the coverage filter 2 low-coverage false positives); null 0 calls. leafcutter (-i 3) 22/24 strong, 1/6 weak, 0 FP, direction 23/23; null 0. Shiba 22/24, 1/6, 1 FP, null 0. rMATS x leafcutter concordance: 22 shared calls, 22 true, 0 null; null: 0/0 (concordance rule verified). 2v2: rMATS 22/24 strong 3 FP with Skill filter, leafcutter 20/24 with 2-3 FP, Shiba 20/24 with 3 FP and 2 calls on the null comparison; the Skill claim that Shiba beats rMATS at n=2 is not supported in a sim without planted junction imbalance (and cannot be tested here). Shiba 0.8.2 crashes (KeyError) unless the GTF contains every event type with reads; decoy genes were added to make it run.

**Scores:** Basic 35/40 | Specialized 52/60 | Total 87/100

**Assertions:**
- [PASS] rMATS with the Skill filters recovers planted strong events with correct sign and no null false positives - 24/24, 24/24 sign, 0 FP; null 0
- [PASS] leafcutter stays quiet on the null comparison and gets direction right - 0 calls on A vs C; 23/23 direction
- [PASS] Two-family concordance rule (rMATS + leafcutter) yields only true calls - 22 concordant, all planted; 0 in null
- [FAIL] Skill claim that Shiba outperforms rMATS at n=2v2 holds on planted truth - Shiba 2 null calls and 3 FP; rMATS 0 null calls (no imbalance planted; claim untestable)
- [FAIL] Weak (|dPSI| 0.15) planted events are detected at standard thresholds - rMATS 0/6, leafcutter 1/6 at n=3 (power table in Skill says marginal below 0.2)

### Input 6 - Scope Boundary: MAJIQ HET cohort, paired tumor-normal --paired-stats, single patient vs cohort hand-off

**Prompt:** I have 30 tumor and 30 normal patients (MAJIQ HET), paired tumor-normal with --paired-stats, and one rare-disease patient vs controls.

**executed:** false  
**What ran and what it printed:** PARTIAL. MAJIQ V3 / VOILA are licence-gated academic downloads and are NOT installed: none of the MAJIQ commands (build, deltapsi, heterogen, voila view) were executed; the public MAJIQ page confirms V3 exists but does not show command syntax, so flags such as --minreads/--minpos/--mem-profile and splicegraph.zarr could not be checked. rMATS --paired-stats (Skill advice for tumor-normal) was executed on the synthetic sim: rc 0, log "Error in library(PAIRADISE): there is no package called PAIRADISE", output SE.MATS.JC.txt is header-only with no FDR column. No PAIRADISE install was attempted (shared env). leafcutterMD.R -h runs and lists -o -s -c -t -p (the hand-off tool for n=1 vs cohort exists); the FRASER2 hand-off was not exercised here.

**Scores:** Basic 27/40 | Specialized 36/60 | Total 63/100

**Assertions:**
- [PASS] Skill states which tools need a licence and routes n=1 vs cohort to outlier tools - usage-guide names academic licence for MAJIQ; SKILL.md routes single patient to FRASER2/leafcutterMD
- [FAIL] Advertised paired tumor-normal route (--paired-stats) works on a stock rMATS install - PAIRADISE missing: rc 0 with header-only output, no warning in Skill
- [FAIL] MAJIQ commands were verified against the installed version - MAJIQ not installed; not executed; flags unverified
- [PASS] Hand-off tool named for the out-of-scope regime exists and is invocable - leafcutterMD.R -h ran

### Input 7 - Adversarial: Batch-confounded design, perfectly confounded batch, and n=1 vs n=1 pilot

**Prompt:** My samples were prepared in two batches and batch is confounded with condition; adjust for it. Also I only have one sample per group, just run it.

**executed:** true  
**What ran and what it printed:** Synthetic sim, 3v3 A vs B with an arbitrary imbalanced batch and random RIN. SKILL.md logit-PSI residual snippet (verbatim block) ran; testing residuals by group with a rank-sum test (as the Skill says) gave minimum p 0.1000 (assert printed: cannot reach 0.05 at 3v3): 0/20 strong planted events at p<0.05. OLS logit_psi ~ group + batch + RIN (group coefficient tested) found 13/20 strong with 1 false positive in 55 null events. leafcutter_ds.R with batch as a third groups-file column (Skill claim, verified in the script source) ran and returned results; with batch identical to group it also exits 0 and returns 4 significant clusters with no rank-deficiency warning. rMATS n=1 vs n=1: runs, rc 0; on the null comparison 4 of 118 events pass FDR<0.05 & |dPSI|>0.10 (all false), on the planted comparison 22 calls of which 4 are false; the Skill gives no stop condition for n=1 vs n=1.

**Scores:** Basic 26/40 | Specialized 36/60 | Total 62/100

**Assertions:**
- [PASS] Skill leafcutter confounder claim (extra groups-file columns) is accurate - verified in leafcutter_ds.R source and by a run
- [FAIL] Skill PSI-residual confounder route can reach significance at n=3 vs 3 - rank-sum on residuals: min p 0.1, 0/20 strong events
- [FAIL] Skill warns that fully confounded batch/condition cannot be adjusted - only says check PCA; leafcutter silently returns results when batch = group
- [FAIL] Skill stops or warns for n=1 vs n=1 - no guidance; rMATS returns 4 false positives on the null comparison

## Verified claims (from the runs)

| Claim in SKILL.md / usage-guide | Verdict |
|---|---|
| rMATS IncLevelDifference sign = b1 - b2 | True (+0.587 / -0.587 on swap) |
| --cstat sets the |dPSI| null cutoff, default 0.0001 | True (--help) |
| rMATS per-replicate coverage filter matters | True (removes 2 low-coverage false positives in sim; all 7 real-data hits) |
| wrong --libType halves usable junctions | True (SE junction counts 13,314 -> 5,570 on unstranded data) |
| leafcutter confounders = extra groups-file columns; R arg confounders= | True (script source; run) |
| leafcutter n>=2 (n>=3 preferred) | Not with the shown flags (default -i 5 stops) |
| SUPPA2 empirical inflated FDR at n<=3 | True (2v2 real: 36 events; permuted 24; sim 3/26 and 2 null FPs) |
| SUPPA2 classical (Wilcoxon) fixes n<=3 | False (0/30 detected; min p 0.1 at 3v3) |
| rMATS n>=3 required | Runs and works at 2v2 in the sim (22/24 strong) |
| Shiba better than rMATS at n=2 | Not supported on a sim with no planted imbalance; untestable here |
| --paired-stats for tumor-normal | Fails silently on stock install (PAIRADISE absent) |
| MAJIQ V3 commands | Not executed; unverified |
| rMATS/leafcutter/SUPPA2/Shiba output-column names used in snippets | True (p.adjust, deltapsi, IncLevelDifference, FDR, IJC_SAMPLE_1 etc.) |

## Shipped-means-present
SKILL.md and usage-guide.md point at no files that are missing; `examples/` holds both files they imply. No `references/` directory is referenced. Neither example runs cleanly from a clean copy (see P1).

## Recommendations

**[P1] SUPPA2 "-m classical for n<=3" has zero power**  
Observed in: [3, 4]  
Problem: Classical mode is an unpaired Mann-Whitney U test; smallest two-sided p is 0.1 at 3v3 and 0.33 at 2v2 and BH cannot lower it. On the planted 3v3 set it detected 0/30 events; on real 2v2 it returned no p below 0.22. The table lists it with min reps n>=2.  
Root cause: The fallback was chosen for robustness without checking attainable p-values.  
Fix: Delete the advice to switch to classical for n<=3; state that SUPPA2 needs n>=4 per group (rank-sum min p 0.029) for any significance, and route n<=3 to rMATS/leafcutter/Shiba. Change the "Min reps" cell for SUPPA2 classical to n>=4.

**[P1] leafcutter n>=2/3 claim vs leafcutter_ds.R defaults**  
Observed in: [2, 3]  
Problem: With the options the Skill shows, leafcutter_ds.R stops at 3v3 and 2v2 ("smallest group is less than min_samples_per_intron"); the Common-Errors flags (--min_samples_per_intron 5 --min_samples_per_group 3) stop identically. Upstream says calibration is only checked down to 4 per group.  
Root cause: Defaults (-i 5 -g 3 -c 20) were not reconciled with the stated minimum replicates.  
Fix: Give the runnable command for 3v3 (e.g. -i 3 -g 3 -c 10) and 2v2 (-i 2 -g 2 -c 5), note the n>=4 calibration limit, and remove the -i 5 pre-filter suggestion for small designs. Also state that groups-file sample names must equal the .junc basenames and that non-chr contigs need -k True.

**[P1] Confounder route (residual + rank-sum) is powerless at n=3 and biased if confounded**  
Observed in: [7]  
Problem: Regressing out batch and RIN and testing residuals by group with a rank-sum test cannot give p<0.05 at 3v3 (0/20 strong events, min p 0.1); OLS with group and batch terms found 13/20 with 1/55 false positives. Regressing out only batch removes group signal when batch is imbalanced.  
Root cause: Residualisation was chosen for simplicity; the group term is left out of the model.  
Fix: Replace with logit-PSI ~ group + batch (+ covariates) and test the group coefficient (or limma/DEXSeq), and warn that residual+rank-sum needs n>=4 per group. State that a batch identical to condition cannot be adjusted (leafcutter silently returns results).

**[P1] Shipped examples fail or mislead from a clean copy**  
Observed in: [1, 2]  
Problem: diff_splicing_rmats.sh hard-codes READ_LENGTH=150: on 75 nt reads it exits 0, prints "analysis complete" and writes 0 SE rows; its awk filter has no coverage filter (4 hits at 0-3 reads). diff_splicing_leafcutter.R writes groups.txt with sample1..6 that cannot match the counts-table column names, so the following leafcutter_ds.R call dies with "undefined columns selected".  
Root cause: Examples were never run end to end against real data.  
Fix: Take READ_LENGTH from the data (or add --variable-read-length and an assertion that SE.MATS.JC.txt has rows), add the per-replicate coverage filter to the awk, and make the R example derive sample names from the .junc basenames and check them against the counts header before calling leafcutter_ds.R.

**[P1] --paired-stats advertised without its dependency; silent header-only output**  
Observed in: [6]  
Problem: SKILL.md recommends rMATS --paired-stats for tumor-normal. On a stock install rMATS logged "no package called PAIRADISE", returned rc 0 and wrote header-only tables without an FDR column.  
Root cause: R/PAIRADISE prerequisite not listed; no post-run check.  
Fix: List PAIRADISE (R) as a prerequisite, add a check that the FDR column exists and the file has rows, and say -t single is needed for single-end data.

**[P2] ΔPSI sign conventions differ by tool; reconciliation table blames event class**  
Observed in: [4, 5]  
Problem: rMATS IncLevelDifference = group1 - group2; SUPPA2 dPSI and leafcutter deltapsi = group2 - group1; Shiba dPSI = alt - ref. The table row "Both sig, opposite direction" attributes it to event mismatch only.  
Root cause: Only the rMATS sign is documented.  
Fix: Add a one-line sign convention per tool and list it first in the opposite-direction row.

**[P2] Shiba and MAJIQ sections are not runnable or checkable as written**  
Observed in: [3, 5, 6]  
Problem: snakeshiba.smk sits in the package share directory and needs a container key in config.yaml (KeyError otherwise); shiba.py config.yaml runs directly but needs XS tags, a GTF with every event type and reads for each type. Shiba 0.8.2 crashes (KeyError) otherwise. MAJIQ V3 flags were not verifiable (licence-gated) and --minreads/--minpos/--mem-profile are V2-era flags. Shiba superiority at n=2 is a citation, not tested (no advantage on a sim with no imbalance).  
Root cause: Sections written from tool websites, not run.  
Fix: Give a minimal config.yaml, the direct shiba.py call, the XS requirement, and mark the MAJIQ block as unverified against V3 with the docs link.

**[P2] Missing practical prerequisites and guards**  
Observed in: [1, 2, 7]  
Problem: No mention of -t single for single-end data (verbatim command exits 0 with 0 events), no stop condition for n=1 vs n=1 (rMATS returns 4/118 null false positives), leafcutter_ds.R is not on PATH after installing the R package, the gencode_exons.txt.gz source is unspecified, and SUPPA2 TPM files need a sample-names-only header.  
Root cause: Assumes a specific standard design.  
Fix: Add a short "design gate" (single-end, n=1, batch = condition) and the four prerequisites above.

## Key strengths
- Core rMATS-turbo and leafcutter usage is correct and recovered planted truth exactly (dPSI 0.587; deltapsi 0.545; 24/24 and 22/24 strong events with correct direction, no null false positives).
- Per-replicate coverage filter and the two-family concordance rule are sound: the filter removed all low-coverage false positives and rMATS x leafcutter concordance gave 22 calls, all true.
- Decision tree, thresholds table, output-column table and the wrong-libType / confounder / cryptic-splicing pitfalls are accurate and useful (libType pitfall verified: -58% junction counts).
- Good routing to sibling skills for out-of-regime designs, and leafcutter confounder-as-extra-column claim verified against the script source.

## Notes on the audit itself
- Two auditor errors were caught and fixed before scoring: (1) pandas read the truth class label `null` as NaN so no-change genes were dropped from the false-positive tally (label renamed `nochange`, all sim runs redone); (2) my first SUPPA2 TPM header carried a `Name` label (SUPPA2 wants sample names only). Both leave scripts in `run\`.
- Working tmp dirs and copied GTFs were deleted; no `__pycache__` in the source clone.
