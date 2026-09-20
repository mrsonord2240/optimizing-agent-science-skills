> **Audit record for `bio-differential-splicing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@ec5b9cf](https://github.com/mrsonord2240/bioSkills/tree/ec5b9cf46e2b1c73a361724dab97168c464fcbac/alternative-splicing/differential-splicing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-differential-splicing (RE-AUDIT of the fixed Skill)

Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@ec5b9cf46e2b1c73a361724dab97168c464fcbac:alternative-splicing/differential-splicing`

Pre-fix audit: 73, Beta Only (archived `_pre-fix-20260920`). This audit: **85, Limited Release**, deployable True, no veto, no P0/P1.

> Numeric score 85 is in the Production Ready band, but the assertion pass-rate floor (>= 90%) is not met (31/35 = 88.6%), so scoring_rubric.md section 5 downgrades one tier. Other floors: static 84 >= 80, execution average 86.0 >= 85, Layer 1 35.0 >= 32, Layer 2 51.0 >= 48.

Method: Skill read from the commit (copied by `git archive` into `run/skill`, worktree untouched); shipped examples run from clean copies; every code block of SKILL.md that can run was extracted by `run/extract_blocks.py` and run verbatim. Data: planted set + first audit's sim (regression, byte-identical regeneration asserted), NEW simulations `make_sim2.py` (own seeds: main n<=6, batch-confounded, paired), real chrX 2v2. All synthetic data are labelled as such.

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 38 | 55 | 93 | 5/5 | ✅ COMPLETED |
| 2 | Variant A | yes | 35 | 52 | 87 | 4/5 | ✅ COMPLETED |
| 3 | Edge | yes | 36 | 53 | 89 | 5/5 | ✅ COMPLETED |
| 4 | Variant B | yes | 34 | 50 | 84 | 5/5 | ✅ COMPLETED |
| 5 | Stress | yes | 35 | 51 | 86 | 4/5 | ✅ COMPLETED |
| 6 | Scope Boundary | yes (MAJIQ part no) | 33 | 46 | 79 | 4/5 | ⚠️ PARTIAL |
| 7 | Adversarial | yes | 34 | 50 | 84 | 4/5 | ✅ COMPLETED |

**Execution Average: 86.0 / 100**  |  Static: 84/100  |  Final: 33.6 + 51.6 = 85  |  Assertion pass rate: 31/35 (88.6%)

## Regression vs the first audit (same inputs, fixed Skill)

| First-audit input | Then | Now |
|---|---|---|
| 1 rMATS planted 3v3 | worked only after adapting flags; shipped example failed on real chrX | verbatim block header-only as the Skill now warns; adapted run exact; shipped example runs from clean copy (planted 1 event, real chrX 197) |
| 2 leafcutter planted 3v3 | default flags stop, chrP dropped, names mismatch, exon_file undocumented | all four documented and reproduce; shipped R example completes end to end (deltapsi 0.5446) |
| 3 real chrX 2v2 | 4 tools, needed 3 workarounds | Skill lists them; numbers quoted (226/121, 36/24, 0.22) reproduce |
| 4 SUPPA2 3v3 | classical advised for n<=3 (0 power) | rule replaced; classical 0/24 (sim) and 0/28 (sim2) at 3v3, empirical 23/24 and 24/28 with false and null calls |
| 5 sim, 3v3/2v2 | rMATS 24/24, leafcutter 22/24 | rMATS 24/24, leafcutter 23/24, 2v2 rMATS 22/24 leafcutter 20/24 (in5r.log) |
| 6 MAJIQ / paired | PAIRADISE missing, silent header-only | installed env, reproducible; MAJIQ hedged, checked against docs |
| 7 confounders | residual + rank-sum: 0/20 at p<0.05 | group-coefficient model with aliasing check; 3v3 0 calls (stated), 4v4 4/30 |

## Detailed Outputs

### Input 1 - Canonical: rMATS-turbo 3v3 on the planted exon-skipping set (regression) + filter snippet + shipped example
**Executed:** True  |  **Status:** COMPLETED

**What ran and what it printed:** WSL as-core, rMATS-turbo 4.4.0, SYNTHETIC planted set (truth dPSI 0.587). Verbatim SKILL.md rMATS block (paired/150/firststrand) on single-end data: 0 rows, exactly as the Skill warns. Matched to the data (-t single, 50, fr-unstranded): IJC 80,80,80 / SJC 10,10,12 / 20,20,20 / 40,40,38, IncLevelDifference 0.587, FDR 1.2e-26. SKILL.md filter snippet run verbatim returns the event. Shipped examples/diff_splicing_rmats.sh from a clean copy: auto-detected -t single / 50, 1 SE event, coverage filter lists it. Swapped b1/b2: -0.587.

**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100
**Assertions:**
- [PASS] The verbatim SKILL.md rMATS block on single-end data gives a header-only table and the Skill says so - rc 0, 0 rows; "Match the command to the data" describes exactly this
- [PASS] Command matched to the data reproduces the planted counts and dPSI - counts identical to the planted 80/10/20/40; IncLevelDifference 0.5870 (assert in in1.log)
- [PASS] SKILL.md pandas filter snippet runs verbatim and returns the planted event - significant rows: 1, min_inc 20, min_skip 10
- [PASS] Shipped rMATS example runs from a clean copy and prints the filtered event - rc 0, "Detected ... -t single, --readLength 50", 1 SE event, awk filter prints it
- [PASS] Sign convention (b1 - b2) stated in the Skill holds - swapped lists give -0.587

### Input 2 - Variant A: leafcutter 3v3 on the planted set following SKILL.md, plus the shipped R example
**Executed:** True  |  **Status:** COMPLETED

**What ran and what it printed:** regtools 1.0.0 + leafcutter 0.2.9 (as-rleaf), SYNTHETIC planted set. Verbatim clustering block on contig chrP: rc 0, 0 introns (Skill: silently dropped); with -k True 3 introns. Default ds flags stop with the quoted message; -i 3 -g 3 -c 10 --exon_file (built with gtf_to_exons.R) runs: 1 cluster, p.adjust 4.0e-9, skipping-intron deltapsi +0.5446 (truth ~0.55). Verbatim R block prints the tables. Shipped R example (samples renamed control1..3/treatment1..3): NONSTANDARD_CONTIGS=TRUE completes end-to-end with the same numbers; as shipped on chrP it dies with an opaque colnames<- error.

**Scores:** Basic 35/40 | Specialized 52/60 | Total 87/100
**Assertions:**
- [PASS] Clustering without -k True drops a non-standard contig silently and -k True fixes it, as the Skill states - 0 introns (rc 0) vs 3 introns
- [PASS] Default -i 5 -g 3 -c 20 stops on a 3v3 design with the quoted message; -i 3 -g 3 -c 10 runs and recovers the planted effect - message present (grep count 1); deltapsi 0.5446, p.adjust 4e-9
- [PASS] gtf_to_exons.R and --exon_file work as documented (gene_name in the GTF) - exons file written; "Loading exons ..." and gene G1 in the results
- [PASS] Verbatim R block and the shipped R example (NONSTANDARD_CONTIGS=TRUE) run end to end and match the planted truth - assert in in2.log: 1 cluster, max deltapsi 0.5446
- [FAIL] Shipped R example reports an actionable error when clustering yields no introns - as shipped on chrP: "attempt to set colnames on an object with less than two dimensions" inside leafcutter; no row-count check after clustering (the rMATS example has one)

### Input 3 - Edge: Real chrX 2v2 (GBR v YRI) across rMATS, leafcutter, Shiba, SUPPA2 + permuted-label control
**Executed:** True  |  **Status:** COMPLETED

**What ran and what it printed:** REAL 2x75 nt paired-end data, GRCh37 (nf-core rnasplice; XS-tagged copies for leafcutter/Shiba). Shipped rMATS example from a clean copy: auto-detected -t paired / 75, 197 SE events (permuted: 191). Skill traps reproduced: fr-firststrand 121 SE vs fr-unstranded 226; --readLength 150 without --variable-read-length 0 rows, with it 197. leafcutter: -m 50 0 introns, -m 10 41 introns, 8 clusters tested, 0 significant (permuted 2); default flags stop; BAMs without XS give strand ? on all 2839 junctions. Shiba with the Skill config: 8 event files, 0 Diff==Yes (98 SE tested). SUPPA2 loop: empirical 36 calls true labels vs 24 permuted; classical 0 calls, min p 0.2207. rMATS FDR+dPSI hits: 9 genes, none pass the coverage filter.

**Scores:** Basic 36/40 | Specialized 53/60 | Total 89/100
**Assertions:**
- [PASS] Shipped rMATS example auto-detects paired 75 nt and produces the event tables from a clean copy - 197 SE / 46 A3SS / 36 A5SS / 17 MXE / 47 RI
- [PASS] The Skill's quoted rMATS traps reproduce (firststrand 226 -> 121; readLength 150 -> 0 rows, 197 with --variable-read-length) - 226 -> 121, 0, 197 measured
- [PASS] leafcutter statements hold: -m 50 leaves 0 clusters on shallow data, -m 10 works, default flags stop at 2v2, missing XS gives strand ? - 0 vs 41 introns; error message quoted; 2839 "?" junctions
- [PASS] Shiba runs with exactly the config keys listed in SKILL.md and writes all event-type tables - PSI_{SE,FIVE,THREE,MXE,RI,MSE,AFE,ALE}.txt present for real and permuted
- [PASS] SUPPA2 numbers quoted in the Skill reproduce (empirical 36 true vs 24 permuted; classical min p 0.22) - 36 / 24 / min p 0.2207

### Input 4 - Variant B: SUPPA2 2.4 on NEW simulation, n = 2..6, empirical and classical: re-measure the n>=4 rule
**Executed:** True  |  **Status:** COMPLETED

**What ran and what it printed:** as-suppa (SUPPA2 2.4, statsmodels 0.14.6), SYNTHETIC sim2 (own seed; 100 genes: SE + A5SS + A3SS; 28 strong / 8 moderate / 6 weak planted; TPM from the same molecules). Classical: 0/28 strong at n=2 (min p 0.2207) and n=3 (0.0765), 25/28 at n=4 (min p 0.0286), 28/28 at n=5-6. Empirical: n=2 20/28 strong, 3 false of 26 calls, 2 calls on the null; n=3 24/28, 2/27, 0 null; n=4 23/28, 1/25, 1 null; n=5 25/28, 0/26, 0; n=6 25/28, 0/26, 0. Old sim, 3v3: empirical 23/24 with 3 false + 2 null calls; classical 0/24 (min p 0.064). Classical calls on the null (raw p<0.05, |dPSI|>0.10): 3, 2, 5 at n=4, 5, 6.

**Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100
**Assertions:**
- [PASS] The SKILL.md SUPPA2 commands (same flags; the verbatim block itself ran in input 3) run on a header-only-names TPM file and write .dpsi for SE, A5 and A3 - 60/60 dpsi files; generateEvents made SE 80, A5 10, A3 10
- [PASS] Classical (Wilcoxon) mode has no power at n<=3 (smallest reachable p 0.22 / 0.077) - 0/28 strong at n=2,3; min p 0.2207 / 0.0765
- [PASS] Classical mode becomes usable at n=4 (Skill: 21/24, p 0.027) - 25/28 strong, min p 0.0286
- [PASS] Empirical mode at n<=3 finds most strong events but produces false and null-comparison calls - n=2: 20/28, 3/26 false, 2 null calls; n=3: 24/28, 2/27 false (smaller than the Skill's 14-23%)
- [PASS] Empirical mode at n>=4 is clean enough to use (Skill: n>=4) - n=4: 1/25 false, 1 null call; n=5,6: 0 false, 0 null; but only 25/28 strong and 1/8 moderate at n=6

### Input 5 - Stress: NEW sim2 (SE + A5SS + A3SS), n = 1, 2, 3, 4, 6, A vs B and null A vs C, rMATS / leafcutter / Shiba
**Executed:** True  |  **Status:** COMPLETED

**What ran and what it printed:** SYNTHETIC sim2, 6 replicates per group. rMATS Skill flags: FDR+dPSI strong 24/28 (n=2), 26 (3), 27 (4), 28 (6), direction correct on every called SE gene; null calls 2 (n=2), 0 (n>=3); n=1: 20/28 strong but 10 false of 35 calls and 4 null calls. leafcutter with -i n -g n -c 10: strong 25, 26, 26, 27 of 28, null calls 2, 0, 0, 0; 6v6 with -i 6 -g 6 gives the same 38 clusters as the example's cap -i 5 -g 5. Shiba n=2/4/6: 25, 27, 28 of 28 strong; null calls 4, 3, 3 (rMATS and leafcutter 2, 0, 0). The Skill coverage filter (sum of per-group minima >= 10) keeps only 20, 21, 22, 20 of the strong events at n=2, 3, 4, 6 (26-28 without it); on the first audit's data (SE only) it lost none. Old sim regression: rMATS 3v3 24/24 strong 0 null, leafcutter 3v3 23/24, SUPPA2 empirical 23/24, all as the first audit.

**Scores:** Basic 35/40 | Specialized 51/60 | Total 86/100
**Assertions:**
- [PASS] rMATS with the Skill flags recovers strong events with correct direction across n=2..6 - 24-28/28, direction 14/14 to 21/21
- [PASS] Null comparisons stay quiet for rMATS and leafcutter at n>=3 - 0 calls at n=3,4,6 for both (2 each at n=2)
- [PASS] leafcutter -i n -g n -c 10 works at each design size and the 6v6 rule agrees with the shipped example's cap - tested 93-94 clusters at every n; 38 vs 38 calls at 6v6
- [PASS] Shiba runs at n=2, 4, 6 with the documented config; the Skill's "not reproduced" hedge on its n=2 advantage is fair - no advantage at n=2 (25/28 vs leafcutter 25/28, rMATS 24/28); 3-4 null calls vs 0-2
- [FAIL] The Skill's recommended coverage filter (min_inc + min_skip >= 10 from per-group minima) keeps the true events - 20/28 strong at n=6 vs 28/28 without it; 4 of the 8 dropped are SE genes (data-dependent: no loss on the first audit's sim)

### Input 6 - Scope Boundary: MAJIQ V3/VOILA (licence-gated) hedging, paired tumor-normal --paired-stats with PAIRADISE, LeafcutterMD hand-off
**Executed:** True  |  **Status:** PARTIAL

**What ran and what it printed:** MAJIQ/VOILA NOT executed (licence-gated; pip: no distribution). Their hedged section was checked against the public MAJIQ 3.0.11.dev7 docs: build, psi-coverage, deltapsi, heterogen, -n NAME1 NAME2, -grp{1,2}, --splicegraph, --min-experiments, --mindenovo, --simplify, --strandness, --minreads, --minbins, splicegraph.zarr, moccasin batch step and "VOILA currently only supports MAJIQ v2" all appear; the V2-era flags the Skill calls unverified (--minpos, --mem-profile, settings.ini) do not. The docs say nothing about HET being conservative at n=5-10. PAIRADISE (executed): as-core without it reproduces the silent failure (rc 0, 0 rows, no FDR column); the Skill install path exists in the public repo; in as-pairadise with the fork profile the run took 27 s and gave a full table; default PSOCK: 3 of 3 runs did not exit in 150 s (one stalled at 10%, two reached 100% with the SE table already written). SYNTHETIC 5 pairs with private patient offsets: PAIRADISE 22 calls, strong 17/28, 0 false, direction 16/16; unpaired rMATS 21 calls, strong 18/28, 0 false.

**Scores:** Basic 33/40 | Specialized 46/60 | Total 79/100
**Assertions:**
- [PASS] PAIRADISE prerequisite claims hold: silent header-only failure without it, install path exists, fork workaround needed and works - rc 0 / 0 rows / no FDR; pairadise/src/pairadise_model present; 27 s with fork
- [PASS] The paired run returns calibrated calls with correct direction - 0 false calls, 16/16 direction (no gain over unpaired rMATS on this 5-pair sim: 17 vs 18 strong)
- [PASS] MAJIQ command names and flags in the Skill match the public V3 docs and V2-era flags are removed - all listed V3 items found in docs; minpos / mem-profile / settings.ini absent
- [PASS] MAJIQ is hedged as not run and unverified - version block and section header say so
- [FAIL] The MAJIQ line "HET ... conservative at n=5-10, where deltapsi reports more" is supported by the docs it is attributed to - the statistics page recommends TNOM for n<5 and Wilcoxon for n>5 and says nothing about conservativeness

### Input 7 - Adversarial: Batch-confounded design (imbalanced and fully confounded), leafcutter covariate, n=1 v n=1
**Executed:** True  |  **Status:** COMPLETED

**What ran and what it printed:** SYNTHETIC sim2b: 4v4, batch 3/1 vs 1/3, 20 null SE genes carry a +-2.0 logit batch shift, 30 true SE DS genes, random RIN. rMATS with the Skill filter: 24 calls, 19/30 true, 4/20 batch-driven false calls (3v3: 23 calls, 20/30, 2/20). PCA of the PSI matrix: PC1 |r| 0.97 with group, 0.66 with batch; PC2 0.73 with batch. SKILL.md snippet run verbatim per event (statsmodels 0.15.0): 4v4 (residual df 4) BH q<0.05 4 calls, all true, 0 batch-driven; 3v3 (df 2) 0 calls, as the Skill says. Aliased batch = group: the snippet raises the ValueError. leafcutter (-i 4 -g 4 -c 10): plain 41 calls (22/30 true, 3 batch-driven); with a batch column 31 calls (18/30, 0 batch-driven); batch = group (labels or 0/1): 86 clusters tested, all p ~ 1, 0 significant, no warning. n=1 v n=1 on sim2: null comparison 4 calls of 99 events; planted 35 calls with 10 false.

**Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100
**Assertions:**
- [PASS] SKILL.md confounder snippet runs verbatim and refuses an aliased batch/group design - ValueError "a covariate is aliased with group"; balanced design accepted
- [PASS] The stated power limit of the adjusted route (residual df) is accurate - 3v3 (df 2): 0 calls; 4v4 (df 4): 4 of 30 true events
- [PASS] leafcutter accepts a confounder as an extra groups-file column and it removes batch-driven calls - batch-driven calls 3 -> 0 while 18/30 true events stay
- [FAIL] leafcutter with batch = group "exits 0 and returns significant clusters, with no warning" - exits 0 with no warning, but 0 significant: every cluster p ~ 1 (labels and numeric encodings); claim is wrong in its second half
- [PASS] The n=1 v n=1 design gate (rMATS runs but gives false calls) holds - null 4/99 calls; planted 10 false among 35 calls

## Static evaluation (25 criteria)

| Category | Score | Note |
|---|---|---|
| functional_suitability | 10/12 | Every runnable claim checked reproduces: rMATS/leafcutter/Shiba/SUPPA2 commands, flags by design size, the SUPPA2 n table, planted truth. Deductions: MAJIQ/VOILA not runnable (hedged), the leafcutter batch = group sentence is wrong, the coverage filter loses recall, HET "conservative" line unsupported. |
| reliability | 9/12 | Post-run table checks (rows + FDR column) in the Skill and the rMATS example, aliasing check in the snippet, silent-failure modes documented. The leafcutter example has no check after clustering and fails opaquely on 0 introns; PSOCK hang description incomplete. |
| performance_context | 7/8 | SKILL.md 444 lines (under 500), usage-guide reduced to a pointer; dense but each section is used. |
| agent_usability | 14/16 | Decision tree, design gate, measured tables and exact flags per design size; one dropped-in unverified MAJIQ line; PCA check worded for PC1 only. |
| human_usability | 6/8 | Natural trigger language and example prompts in usage-guide; prompts do not mention batch or paired designs. |
| security | 11/12 | No credentials or eval; the examples quote variables and read paths from files. Batch-confounder snippet uses fixed formulas. |
| maintainability | 10/12 | Examples run from a clean copy and are checked; versions and check date stamped. No test harness ships; evidence numbers live in prose. |
| agent_specific | 17/20 | Description precise (no SOTA claim now), escape hatches (n=1 stop, single-patient hand-off, aliased batch), composability via Related Skills; MAJIQ path cannot be executed. |

**Static subtotal: 84/100**

## Vetoes
Skill veto: PASS (T1-T4). Research veto: PASS (M1-M4; M4 positive evidence = every block ran verbatim).

## Independent checks of the fix

- Deleted SUPPA2 classical mode for n<=3 and the "n>=4" rule: re-measured on new data (input 4). Holds for classical; for empirical the Skill's 14-23% false-call rate is 7-12% here; n>=4 is clean within noise; classical n>=4 has 2-5 raw-p calls on the null comparison (not stated).
- leafcutter -i/-g/-c by size and -k True: input 2, 3, 5 (2v2 to 6v6). The cap on -i at 5 in the example vs "smaller group size" in the text makes no difference at 6v6 (38 vs 38 calls).
- logit confounder route + aliasing check: input 7. Works as documented; leafcutter with a batch column is the stronger route at small n (recommendation).
- Two examples from a clean copy: input 1, 2, 3. rMATS example clean; leafcutter example clean except the opaque zero-intron failure.
- PAIRADISE in `as-pairadise` and `--paired-stats`, fork workaround: input 6. Reproduced; PSOCK also hangs after 100% (table already written).
- usage-guide dedup: compared with the pre-fix file. Deleted "What the Agent Will Do" and Tips restate the decision tree, filters, Confounder Handling, Result Prioritization and Pitfalls (each verified present in SKILL.md); nothing needed was lost. Install prerequisites moved to SKILL.md Install Notes (bioconda names rmats/regtools/suppa/shiba exist; installed versions 4.4.0/1.0.0/2.4/0.8.2).
- MAJIQ/VOILA and Shiba n=2 advantage: not executable / not reproduced; both hedged in the text. MAJIQ hedging judged adequate apart from the one HET sentence. Shiba: 25/28 strong at n=2, level with leafcutter and rMATS, more null calls (4 vs 2); the "not reproduced" wording is fair.

## Recommendations

**[P2] leafcutter batch = group sentence is wrong**  
Observed in: [7]  
Problem: SKILL.md says leafcutter_ds.R with batch = group "exits 0 and returns significant clusters, with no warning". Run with both label and 0/1 encodings: exit 0, no warning, 86 clusters tested, every p ~ 1, 0 significant.  
Root cause: The claim came from the first audit's wording and was not re-run when the section was rewritten.  
Fix: Say it exits 0 without a warning and returns non-informative p ~ 1 for every cluster; keep the rank check as the guard.

**[P2] Coverage filter uses per-group minima and drops true events**  
Observed in: [5]  
Problem: min_inc and min_skip are minima over all replicates of both groups, added together; on sim2 it kept 20-22 of 28 strong events (26-28 without it), and loses more as n grows. usage-guide prompts ask for >= 10 reads per replicate.  
Root cause: The sum of two separate minima is not a per-replicate total, and the minimum over more replicates only falls.  
Fix: Filter on the per-replicate total (IJC + SJC >= 10 in every replicate, or in at least half) and state the recall cost; update the shipped example the same way.

**[P2] MAJIQ HET "conservative at n=5-10" is not in the docs**  
Observed in: [6]  
Problem: The MAJIQ section is labelled as taken from the 3.0.11.dev7 docs, but the docs recommend TNOM for n<5 and Wilcoxon for n>5 and never call HET conservative.  
Root cause: A benchmark impression was left in a section that claims documentation as its source.  
Fix: Attribute it to the MAJIQ-HET paper or delete it; keep the docs-based n<5 / n>5 statistic advice.

**[P2] Shipped leafcutter example fails opaquely on zero introns**  
Observed in: [2]  
Problem: With contigs outside chr1..22,X,Y (or -m too high) clustering yields an empty counts table and the example dies inside leafcutter with a colnames<- error.  
Root cause: No check after the clustering step, unlike the rMATS example.  
Fix: After Step 2 count rows in leafcutter_perind_numers.counts.gz and stop with the -k True / -m hint when there are none.

**[P2] Confounder guidance: PCA wording and the better route at small n**  
Observed in: [7]  
Problem: "If PC1 separates by batch" would not flag the simulated design (PC1 tracks group, r 0.97; batch is on PC2). The per-event regression found 4/30 true events at 4v4, while leafcutter with a batch column kept 18/30 with 0 batch-driven calls. PAIRADISE default PSOCK also hangs after reaching 100% (2 of 3 runs), not only at a few percent.  
Root cause: Advice written from a 3v3 case and one hang pattern.  
Fix: Say "check every leading PC against batch", name leafcutter with a batch column as the first choice at n<=4, and add a timeout note to the PAIRADISE paragraph.

## Files

`run/`: 00_setup.sh, 01_make_data.sh, make_sim.py, make_sim2.py, common.sh, extract_blocks.py, in1..in8 scripts, eval_sim.py, eval_sim2.py, in3_analyze.py, in6_score.py, in7_analyze.py, make_report.py, bin/ (shims), skill/ (the audited commit), data/ (synthetic inputs, BAMs removed), out/ (small result files), *.log (captured output).
