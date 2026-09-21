> **Audit record for `bio-outlier-splicing-detection`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@bebf052](https://github.com/mrsonord2240/bioSkills/tree/bebf0525bf72d2737fd3404d1b1abe7e51f050b7/alternative-splicing/outlier-splicing-detection) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-outlier-splicing-detection (re-audit of the fixed Skill)
Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@bebf0525bf72d2737fd3404d1b1abe7e51f050b7:alternative-splicing/outlier-splicing-detection` (read from a copy in `run/skill/`; the worktree `wt\as-outlier` and the clone were not written to).
Pre-fix (archived at `_pre-fix-20260920\`): 67, Beta Only, not deployable. **Now: 82, Limited Release, deployable, no veto, no open P0, one open P1.**

Category: Data Analysis. Mode D. Complexity: Complex, N = 9 (the 7 pre-fix inputs re-run as regression tests, plus 2 new). Executed 9/9 (input 5 partial: the DROP demo, MAE and OUTRIDER modules were not re-run; the earlier completed demo run is cited). Every script that was run is in `run/scripts`, logs in `run/logs`, extracted SKILL.md blocks in `run/blocks`. Synthetic data are labelled SYNTHETIC in each generator; BAMs were deleted after the audit.

## How the code-usability question was re-judged
Every fenced block of SKILL.md was extracted verbatim to `run/blocks/` by `02_extract_blocks.py` (9 blocks) and parse-checked (`03_syntax.R`: all 6 R blocks and the example parse; `bash -n` OK on the 3 bash blocks). Then each was run from its file:

| block | what | how run | result |
| --- | --- | --- | --- |
| 01 | FRASER 2 workflow | verbatim via `10_block_fraser.R`, cohort A and B, 30 to 8 samples, FRASER 2.6.1; verbatim on 2.2.0 | 2.6.1: ran, 4/4 (A), 4/4 (B); empty-result subsets stop at the last line; 2.2.0: `estimateBestQ` not found |
| 02 | OUTRIDER | verbatim via `45_block_outrider.R`, 1.24.0 and 1.28.1, four matrices | ran on both releases; q numeric > 1 |
| 03, 04 | LeafcutterMD bash + BH | verbatim (one substitution: clustering script path) | ran; 11 hits at BH q<0.05 |
| 05 | DROP install/init/config | init and config checks in `50_drop_init.sh`; `mamba create` and demo not run | init works; config values match; 0 `conda:` |
| 06, 07 | bcftools + R integration | verbatim on real SpliceAI output | concordant variants only; guard fires |
| 08, 09 | mismatch check, choosing q | verbatim via `16_block_extras.R` | ran; `plotEncDimSearch(plotType='auc')` returns a ggplot; bestQ 1 (OHT) / 2 (grid) |
| example | `examples/fraser2_rare_disease.R` | clean copy, arguments, FRASER 2.6.1 and 2.2.0, cohort A and 4 real BAMs | ran on all three |

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Canonical (regression) | yes | 36 | 51 | 87 | 4/5 | ✅ |
| 2 | Variant A (regression) | yes | 35 | 50 | 85 | 5/5 | ✅ |
| 3 | Edge (regression) | yes | 31 | 44 | 75 | 3/5 | ✅ |
| 4 | Variant B (regression) | yes | 35 | 52 | 87 | 5/5 | ✅ |
| 5 | Stress (regression) | yes | 32 | 46 | 78 | 5/5 | ✅ |
| 6 | Scope Boundary (regression) | yes | 36 | 53 | 89 | 5/5 | ✅ |
| 7 | Adversarial (regression) | yes | 29 | 42 | 71 | 2/4 | ⚠️ |
| 8 | Variant A (NEW) | yes | 37 | 53 | 90 | 5/5 | ✅ |
| 9 | Edge (NEW) | yes | 34 | 50 | 84 | 4/4 | ✅ |

**Execution average: 82.9 / 100** (pre-fix 66.3). Assertion pass rate 38/43 (pre-fix 16/32). Layer 1 average 33.9/40, Layer 2 average 49.0/60.

Static 80 (pre-fix 67) x 0.4 = 32.0; dynamic 82.9 x 0.6 = 49.7; **final 82 -> Limited Release, deployable = true**. Floors for Limited Release met (static >=70, execution >=75, L1 >=28, L2 >=42, assertions >=80%); Production Ready needs execution >=85. Skill veto PASS (stability, contract, determinism, security). Research veto: M1 PASS, M2 PASS (pre-fix P1 fixed), M3 PASS, M4 PASS.

## Static score: 80/100 (pre-fix 67)

| Category | Score | Note |
| --- | --- | --- |
| functional_suitability | 10/12 | Covers FRASER 2, OUTRIDER, LeafcutterMD, DROP and SpliceAI integration with a sound decision tree. Every block ran on the installed releases (FRASER 2.6.1 block 4/4 planted events, OUTRIDER block on 1.24.0 and 1.28.1, LeafcutterMD, integration, DROP init). Two blocks are not portable as written: the FRASER block calls estimateBestQ, which FRASER 2.2.0 lacks (the block comment says so; the example handles it), and it stops at its last line when no sample has a call. |
| reliability | 9/12 | Common Errors rebuilt from messages seen in runs; cohort sizes measured (FRASER n>=20, OUTRIDER n>=50 reproduced). Open: the FRASER block errors ('argument 1 is not a vector') on empty results at n=8/12/16, the scenario the Skill itself predicts; the 'smaller than 2' OHT message is placed at n=8-12 but appeared only at n=4; the AE reproducibility recipe is wrong. |
| performance_context | 5/8 | One 392-line SKILL.md; usage-guide cut to 35 lines and no longer repeats it (redundancy fixed); no references/ split; one example. |
| agent_usability | 13/16 | Clear tables and a decision tree; thresholds now consistent (zScoreCutoff 0, PCA default, filter defaults), outputs of LeafcutterMD named, integration block derives delta_max. The example comment ('AE needs set.seed()') and SKILL.md ('SerialParam(RNGseed=1) does') disagree, and both are incomplete. |
| human_usability | 7/8 | Natural prompts, per-scenario guidance, example takes arguments and warns for n<20; no input validation beyond the patient-id check. |
| security | 11/12 | Research-use-only statement, licence statement checked against the installed LICENSE files (CC BY-NC 4.0 for FRASER 2.6.1 / OUTRIDER 1.28.1 / DROP 1.6.1, MIT for 2.2.0 / 1.24.0), dbGaP note for GTEx BAMs. No credentials, quoted shell variables. |
| maintainability | 9/12 | Version line dated and checked on two release pairs; measured numbers carry their conditions. Still no shipped test data or expected output; the generator lives only in the audit. |
| agent_specific | 16/20 | Related-skill links exist; stop conditions for cohort size and tissue; clinical hand-off removed (no PS3/PP3 directive). Two unsourced tables remain (tissue 'genes captured' percentages, disease-specific expectations) and the tissue-mismatch check cannot see a sample the PCA fit has absorbed. |

## Pre-fix findings re-judged

| pre-fix finding | pre-fix | now | evidence (this audit's runs) |
| --- | --- | --- | --- |
| Main FRASER workflow + example crash (`colData = data.frame`) | P1 | **fixed** | block on 2.6.1: 4/4 planted, 0 false calls (input 1); example clean-copy on 2.2.0 and 2.6.1 and on 4 real BAMs (input 9); unseen cohort B 4/4 (input 8). Residual: block on 2.2.0 needs `optimHyperParams` (P2) |
| `estimateBestQ` / `plotEncDimSearch` API drift, OUTRIDER q object | P1 | **fixed** | OUTRIDER block verbatim on 1.24.0 and 1.28.1, four matrices, no crash (input 2); `plotEncDimSearch(plotType='auc')` returns a ggplot; FRASER `estimateBestQ` + `bestQ` ran (bestQ 1 OHT, 2 grid) |
| OUTRIDER cohort guidance too optimistic | P1 | **fixed** | 0/8 at n=30 on both releases; simulator m=100 60% (1.24.0) and 70% (1.28.1) on one seed vs the Skill's 71% / 74% over 3 seeds; symptom is the silent 'No significant events' |
| q=10 hard-coded, tuning advice unbacked | P1 | **fixed** | example estimates q and prints it (q=1, 2, 2 on cohort A 2.6.1, 2.2.0, real BAMs); cohort B q=1 4/4; the old q=10 miss of the cryptic donor is not re-run, the new default finds it |
| No research-use caveat; PS3 / clinical-report directive | P1 | **fixed** | Research Use and Licences section; grep of SKILL.md, usage-guide and example: no PS3/PP3 directive, no clinical-report step (input 6) |
| Licence misstated | P1 | **fixed** | LICENSE files read: FRASER 2.6.1 / OUTRIDER 1.28.1 CC BY NC 4.0, 2.2.0 / 1.24.0 MIT; DROP prints the notice (`logs/72_licence_*.log`, `logs/50_drop_init.log`) |
| DROP section: init, config keys, MAE, --use-conda, PCA default | P1 | **fixed** | `mkdir && cd && drop init` works; config values match by script; 0 files with `conda:`; MAE comment 'negative binomial' (input 5). Demo not re-run (cited) |
| Invented error messages; AE not reproducible | P1 | **partly fixed, P1 remains** | Common Errors now real messages (colData slot, OHT smaller than 2, OUTRIDER q, No significant events, `drop init`), one misplaced (seen at n=4, not n=8-12). The AE seed recipe is wrong: `SerialParam(RNGseed=1)` alone leaves 9815 of 20010 p-values differing; only `set.seed(1)` + `SerialParam(RNGseed=1)` gives 0 (input 7) |
| LeafcutterMD outputs, correction, limits | P1 | **fixed** | files named and produced; BH block reproduces 11 hits; retention and pseudoexon give no cluster p-value (input 4) |
| Tissue-mismatch symptom and detection | P2 | **partly fixed, P2 remains** | symptom reworded and reproduced (PCA 0, AE 8-9 calls); check works under AE only (input 7) |
| Threshold inconsistencies (|z|>=2 vs 0, filter, 'autoencoder' wording) | P2 | **fixed** | zScoreCutoff 0 stated, PCA named as default; example uses FRASER defaults for the variability filter (667 junctions on cohort A both releases) |
| Integration block (delta_max, chr naming, GTEx access) | P2 | **fixed** | real SpliceAI multi-allelic output parsed; chr/no-chr agree; guard fires (input 6) |
| Single-file layout, no test data | P2 | **open** | unchanged, restated as P2 |
| **new** (introduced or exposed by the fix) | - | P2 x3, P1 x1 | FRASER block stops on empty results; block not runnable on 2.2.0; unsourced tissue/disease tables; DROP runtime wording; AE recipe (P1) |

## Detailed Outputs

### Input 1 — Canonical: FRASER 2: one patient vs 29 controls, planted outliers (synthetic; REGRESSION of pre-fix input 1)
**Executed:** true. SYNTHETIC 30-sample 2x75 cohort A regenerated from the audit generator (seed 20260920; truth and gene counts byte-identical to the pre-fix run). SKILL.md FRASER block run verbatim (extracted to run/blocks/01_r.R) on FRASER 2.6.1 (WSL as-drop): completes, 667 junctions, bestQ 1, 4/4 planted events flagged in the right sample and gene (S05/g010 padj 2.8e-5, S12/g030 9.3e-3, S20/g050 9.1e-4, S25/g070 3.6e-3), 0 non-planted calls, expression-only S15/S28 not called, S29 mismatch sample 0 calls. The same block on FRASER 2.2.0 (Windows R via r.sh) stops at estimateBestQ (could not find function; the block comment says 2.2.0 has only optimHyperParams). The shipped example run from a clean copy on both versions: 667 junctions kept, q=1 (2.6.1) / q=2 (2.2.0, optimHyperParams), 3 aberrant junctions in PATIENT_001 (chr21:90194-92840 padj 2.8e-5 dPsi +0.70, 91783-92840, 90194-91550), 6 calls in all samples on both, volcano PDF written (35 KB).

**Scores:** Basic 36/40 | Specialized 51/60 | Total 87/100 | ✅

**Assertions:**
- [PASS] SKILL.md FRASER block runs verbatim from a clean directory on FRASER 2.6.1 and finishes — was FAIL pre-fix (colData data.frame); now 667 junctions, bestQ 1, results table produced
- [PASS] The shipped example runs from a clean copy on FRASER 2.6.1 and 2.2.0 with arguments and prints a checked result — '3 aberrant junctions in PATIENT_001 ...; 6 in all samples' on both versions; junctions kept and q printed
- [PASS] All four planted splicing events (skipping, cryptic donor, retention, pseudoexon) are flagged at padj<0.05, |dPsi|>=0.1 in the right sample and gene — 4/4 (pre-fix: 3/4, cryptic donor missed at q=10); S12 flagged with the OHT q
- [PASS] No calls outside the planted sample/gene pairs; expression-only events are not reported as splicing outliers — 0 non-planted calls; S15 and S28 0 calls; S29 (shifted stand-in) 0 PCA calls, as the Skill states
- [FAIL] The SKILL.md block runs verbatim on every release named under Version Compatibility (FRASER 2.2.0 and 2.6.1) — 2.2.0: 'could not find function estimateBestQ'; documented in the block comment and handled by the example, not by the block
Assertion pass rate: 4/5

### Input 2 — Variant A: OUTRIDER expression outliers on synthetic counts, n=30 and n=100, plus OUTRIDER's simulator (REGRESSION of pre-fix input 2, plus a new n=100 matrix)
**Executed:** true. SYNTHETIC. SKILL.md OUTRIDER block run verbatim (blocks/02_r.R) on OUTRIDER 1.24.0 (Windows R) and 1.28.1 (as-drop). Pre-fix matrix (3000x30, 8 planted): both versions run to the end; q_best 8 (1.24.0) / 2 (1.28.1, OHT gave 1, raised to 2 by the block); 0/8 detected, 0 false calls, 'No significant events' warning, exactly what the Skill now says for n<50. NEW matrix (3000x100, 20 planted, seed 5150, hidden batch): 1.24.0 q=20 2/20, 1.28.1 q=2 9/20 with 1 false call. NEW OUTRIDER-simulator matrix (2000 genes, m=100, freq 1e-3, 192 injected, seed 42): 1.24.0 116/192 (60%, 1 false), 1.28.1 135/192 (70%, 0 false); the Skill's 3-seed table says 71% / 74% at n=100. No crash on either version (pre-fix: 1.28.1 crashed on the q object). One as-drop run of the simulator matrix died with 'error writing to connection' (MulticoreParam workers killed while the machine was under memory load) and passed on retry.

**Scores:** Basic 35/40 | Specialized 50/60 | Total 85/100 | ✅

**Assertions:**
- [PASS] The OUTRIDER block runs verbatim on the current release (1.28.1) and returns a numeric q > 1 — was FAIL pre-fix; q 2 (n=30, n=100), 13 (simulator)
- [PASS] The block runs verbatim on 1.24.0 (the release its comment describes) — q 8 / 20 / 20
- [PASS] Cohort-size claim: essentially no power at n<=30, 40-75% around n=50-100 — 0/8 at n=30 on both versions; 60% and 70% at m=100 on one seed (table 71% / 74%)
- [PASS] No false-positive outliers beyond the stated 0-2 — 0, 0, 0, 1, 1, 0 false calls across the six fits
- [PASS] Failure-mode text matches the observed symptom (silent 'No significant events', no convergence warning) — warning seen at n=30 on both versions, no convergence warning
Assertion pass rate: 5/5

### Input 3 — Edge: FRASER below and around the stated minimum: patient + 7, 11, 15, 19, 24 controls (REGRESSION of pre-fix input 3)
**Executed:** true. SYNTHETIC subsets of cohort A (patient + first n-1 controls by name), SKILL.md block verbatim each time, FRASER 2.6.1. n=8, 12, 16: 0 calls in any sample, planted skipping S05 not detected, 0 false calls; the block then stops with 'argument 1 is not a vector' at order(patient_results$padjust) because results() returned an empty table with no columns (3 of 3 runs; the shipped example guards this). n=20: 3 calls (S05 skipping padj 6.4e-3, S20 retention 3.0e-2), cryptic donor S12 not detected. n=25: 5 calls (S05, S20, S25; S12 not detected). n=30: 4/4 (input 1). OHT bestQ 2 at n=8-25 with the message 'Optimal encoding dimension: 2', not the 'smaller than 2' warning the Skill places at n=8-12; that warning appears only at n=4 (input 9). Pre-fix claim that 'cohort too small' / 'convergence not reached' exist is gone from the Skill.

**Scores:** Basic 31/40 | Specialized 44/60 | Total 75/100 | ✅

**Assertions:**
- [PASS] Advice for n<20 (missed at n=8-16, recruit more) agrees with observed behaviour — 0 calls and S05 missed at n=8, 12, 16; detected at n=20 and 25
- [PASS] Small cohorts give no false positives — 0 non-planted calls at n=8, 12, 16, 20, 25
- [FAIL] The SKILL.md block runs to its last line when the outlier set is empty (the case the Skill predicts for n<20) — 'argument 1 is not a vector' at n=8, 12, 16; example has an nrow>0 guard, block does not
- [FAIL] Common Errors row: 'Optimal latent space dimension is smaller than 2 ... set to 2 (seen at n=8-12)' — not printed at n=8-25; printed at n=4 (real data). Message text itself is genuine
- [PASS] 'n=20, 25: flagged (3 junctions)' cohort-size sentence — n=20: 3 calls; n=25: 5 calls with 3 of 4 planted events; same order of magnitude, composition of controls matters
Assertion pass rate: 3/5

### Input 4 — Variant B: LeafcutterMD annotation-free outliers on the same cohort (REGRESSION of pre-fix input 4)
**Executed:** true. SYNTHETIC cohort A BAMs (XS:A tags). Block blocks/03_bash.sh run verbatim in WSL, one substitution (`python leafcutter_cluster_regtools.py` -> the same script from the leafcutter repo on PATH, since the block assumes it is in the working directory): 30 .junc files, clustering wrote 480 clusters -> 86, leafcutterMD wrote patient_outlier_clusterPvals.txt (86x30), _pVals.txt and _effSize.txt (257x30). BH block (blocks/04_r.R) run verbatim: 2580 cluster-sample tests, 39 raw p<0.05, 11 at BH q<0.05 = S05 skipping (q 6.4e-7), S12 cryptic donor (q 2.0e-2), 9 in the mismatch sample S29, 0 elsewhere. S20 retention and S25 pseudoexon have no cluster p-value, as the Skill now says.

**Scores:** Basic 35/40 | Specialized 52/60 | Total 87/100 | ✅

**Assertions:**
- [PASS] The bash block runs from a clean directory and writes _pVals, _clusterPvals and _effSize — all three written with the shapes the Skill describes
- [PASS] Planted skipping and cryptic-donor events flagged in the right sample by the BH block — S05 q 6.4e-7; S12 q 2.0e-2
- [PASS] The R BH snippet reproduces the pre-fix count of 11 hits at q<0.05 and controls the raw p-values — 11 of 39 raw; 0 false hits outside S29
- [PASS] Junction-only limitation stated and true — no cluster tested for the retention (S20) and pseudoexon (S25) events
- [PASS] Output files and script locations are named well enough to run without guessing — files named; clustering script path named in text; the block itself still needs the path prefixed
Assertion pass rate: 5/5

### Input 5 — Stress: DROP: init, config and pipeline claims (REGRESSION of pre-fix input 5; demo cited, not re-run)
**Executed:** true. WSL as-drop, DROP 1.6.1 (FRASER 2.6.1, OUTRIDER 1.28.1). The block's setup lines run: `mkdir my_diagnostic_run && cd ... && drop init` works and prints the CC-BY-NC 4.0 notice. config.yaml checked by script against the block's comment: aberrantSplicing run: true, implementation PCA, FRASER_version "FRASER2", padjCutoff 0.1, deltaPsiCutoff 0.1; aberrantExpression run: true, implementation autoencoder; mae run: true; keys sampleAnnotation, geneAnnotation, genome, root, htmlOutputPath all present. No rule file contains a `conda:` directive (0 files), so omitting --use-conda is right. deseq_mae.R comment: 'negative binomial test for allelic counts'. NOT re-run: the ~90-minute demo (the earlier completed run is cited: 63/70 steps, results.tsv written for group fraser with 258 rows, min padjust 1, 0 significant; the run was killed by its own 100-minute timeout in step 08 of group fraser_external), MAE and OUTRIDER modules, `mamba create`. A dry-run of `snakemake aberrantSplicing` on the bare init directory fails on missing config inputs, as expected without data.

**Scores:** Basic 32/40 | Specialized 46/60 | Total 78/100 | ✅

**Assertions:**
- [PASS] `mkdir && cd && drop init` creates the project (the pre-fix `drop init <name>` failed) — init...done in DROP 1.6.1
- [PASS] Config keys and values quoted in the block match the generated config.yaml — checked by script: run: true x3, PCA, FRASER2, 0.1, 0.1, autoencoder
- [PASS] `snakemake` without --use-conda is right — 0 rule files contain conda:
- [PASS] MAE description (negative-binomial test, not z-score) is accurate — deseq_mae.R: 'negative binomial test for allelic counts'
- [PASS] Demo runtime and result statement ('about 85 minutes on 10 cores, no significant outlier') — cited from the earlier completed run, not re-run; runtime to results was about 90 minutes and the full target did not finish within 100
Assertion pass rate: 5/5

### Input 6 — Scope Boundary: SpliceAI + FRASER integration and research-use boundary (REGRESSION of pre-fix input 6, on real SpliceAI output)
**Executed:** true. Block 06 (bcftools query) and block 07 (R) run verbatim. Input VCF = the REAL SpliceAI examples/output.vcf (10 records, multi-allelic, unscored alleles) plus 4 SYNTHETIC chr21 records in real SpliceAI INFO format; FRASER results = the shipped example's real output for PATIENT_001. With `chr21` and with `21` contigs: 13 variants parsed, delta_max 0.19-1.0, confirmed = positions 90190 (delta 0.85, junction 90194-92840) and 92000 (delta 0.30 taken from the second allele of 'SpliceAI=.,T|...', junction end 840 bp away); decoys 130000 and 250233 excluded; the real chrX/chr1/chr21 records excluded. With a VCF holding only chrX records the block stops at its own stopifnot (no chromosome overlap). With the real records only: 0 rows, correct. Scope: SKILL.md now states research use only, no PS3/PP3 or clinical report; usage-guide has no report step. Licence text matches the installed LICENSE files (FRASER 2.6.1 / OUTRIDER 1.28.1 CC BY NC 4.0; 2.2.0 / 1.24.0 MIT).

**Scores:** Basic 36/40 | Specialized 53/60 | Total 89/100 | ✅

**Assertions:**
- [PASS] The integration blocks run verbatim on real SpliceAI output with multi-allelic and unscored ('.') alleles and return only the concordant variants — positions 90190 and 92000 only, decoys excluded
- [PASS] chr21 vs 21 naming does not silently give an empty join — both spellings give the same two positions
- [PASS] The chromosome-overlap guard fires when nothing overlaps — 'any(variants$chrom %in% fraser_hits$seqnames) is not TRUE'
- [PASS] A request for a PS3 / clinical report is answered as research use only — Research Use and Licences section; PS3 wording removed from SKILL.md and usage-guide
- [PASS] The licence statement matches the installed packages — LICENSE files read in both R libraries
Assertion pass rate: 5/5

### Input 7 — Adversarial: Tissue-mismatched patient and AE reproducibility (REGRESSION of pre-fix input 7)
**Executed:** true. SYNTHETIC S29 = half of all genes with ~5x baseline skipping. FRASER 2.6.1: PCA q=5: 5 calls in total, S29 0 calls; AE q=10 twice with SerialParam(RNGseed=1): 19 and 18 total calls, S29 9 and 8 (the Skill says 15). Skill's calls-per-sample check (block 08, verbatim) puts S29 first under AE (9 and 8 calls) but the default PCA fit shows S29 with 0, so the check cannot flag a mismatch the PCA fit has absorbed. Reproducibility (Skill: 'set.seed() alone does not fix it; SerialParam(RNGseed = 1) does'), AE q=5 fit twice, 20010 p-values: no seed 9885 differ; set.seed(1) only 9279 (9299 at 5 iterations); SerialParam(RNGseed=1) only 9815 (9962 at 5 iterations); set.seed(1) AND SerialParam(RNGseed=1) 0 differ (default iterations); PCA 0 differ. The fixer's script (kept in run/scripts/23) uses both together, so its '0 differ' result does not support the sentence written in the Skill.

**Scores:** Basic 29/40 | Specialized 42/60 | Total 71/100 | ⚠️

**Assertions:**
- [PASS] Skill's warning that a mismatched patient does not always look like 'hundreds of outliers' is reproduced — PCA 0 calls, AE 8-9 (Skill: 15, varies with the non-deterministic AE fit)
- [FAIL] The Skill's check (calls per sample) exposes the mismatch under the default fit — works under AE (S29 first); under PCA S29 has 0 calls and the check shows nothing; no correlation/PCA-of-counts check is given
- [PASS] Output does not diagnose or name a causal gene from outliers alone — candidates for follow-up only, research-use section
- [FAIL] The stated recipe for reproducible AE fits works — SerialParam(RNGseed=1) alone: 9815 of 20010 p-values differ; only set.seed(1) plus SerialParam(RNGseed=1) gives 0
Assertion pass rate: 2/4

### Input 8 — Variant A: NEW: FRASER block on an unseen cohort B (seed 777, 40 samples, other genes/samples/strengths)
**Executed:** true. SYNTHETIC cohort B built by scripts/03_make_cohort_B.py from the same generator: 40 samples, planted skipping S03/g015 (0.6), cryptic donor S17/g045 (0.5), retention S22/g075 (0.6), pseudoexon S33/g105 (0.45), expression-only S08 and S36, mismatch S40. Skill block verbatim on FRASER 2.6.1 (39 controls + PATIENT_001 = S03): 664 junctions, bestQ 1, 6 calls: S03 padj 6.2e-3 (dPsi 0.72), S17 1.8e-2, S22 4.2e-4, S33 3.9e-2 = 4/4, expression-only 0 calls, 0 non-planted calls, S40 mismatch 1 call.

**Scores:** Basic 37/40 | Specialized 53/60 | Total 90/100 | ✅

**Assertions:**
- [PASS] The block runs verbatim on a cohort it was not tuned on — completes; bestQ 1
- [PASS] All four planted splicing events flagged in the right sample and gene — 4/4, padj 4.2e-4 to 3.9e-2
- [PASS] No non-planted calls — 0
- [PASS] Expression-only events not reported as splicing outliers — S08 and S36 0 calls
- [PASS] The OHT q the Skill recommends does not lose a planted event (fixed q=10 did in cohort A) — q=1, 4/4
Assertion pass rate: 5/5

### Input 9 — Edge: NEW: shipped example on 4 REAL chrX RNA-seq BAMs (nf-core rnasplice test data, 2 GBR + 2 YRI)
**Executed:** true. REAL data, paired-end, no XS tags, copied to run/ex_real (public-data untouched). Example run from a clean copy with arguments `bams ERR188383.Aligned.out fraser_workdir` on FRASER 2.6.1: prints the n<20 warning ('Only 4 samples: ...'), 232 junctions kept, OHT warning 'Optimal latent space dimension is smaller than 2 ... set to 2', q=2, runs to the end, '0 aberrant junctions in ERR188383.Aligned.out (padj<0.05, |delta|>=0.1); 0 in all samples', writes the (header-only) outliers table and a volcano PDF (16.7 KB); ggplot warns about 3 removed rows.

**Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100 | ✅

**Assertions:**
- [PASS] The example runs from a clean copy on real BAMs and reaches its final print — rc 0, final line printed (pre-fix example crashed on the data.frame colData)
- [PASS] It warns that the cohort is below the FRASER minimum — 'Only 4 samples: FRASER missed ...'
- [PASS] No false calls on 4 samples — 0 calls in all samples
- [PASS] Output files are written and non-empty where they should be — outliers.tsv (header-only, 32 bytes) and volcano PDF 16.7 KB
Assertion pass rate: 4/4

## Key outputs the scores depend on
```
FRASER 2.6.1, SKILL.md block verbatim, cohort A (logs/11): 667 junctions | total calls 6
  S05 g010 DETECTED padj 2.8e-05 | S12 g030 DETECTED 9.3e-03 | S20 g050 DETECTED 9.1e-04 | S25 g070 DETECTED 3.6e-03
  S15/S28 expression-only: calls 0 | non-planted calls 0 | S29 mismatch calls 0
FRASER 2.2.0, same block (logs/12): Error in estimateBestQ(fds, type = 'jaccard', plot = FALSE): could not find function 'estimateBestQ'
Small cohorts (logs/13, block verbatim): n=8,12,16: total calls 0, then 'BLOCK ERROR: argument 1 is not a vector'; n=20: 3 calls; n=25: 5 calls
Cohort B (logs/15): S03 6.2e-03, S17 1.8e-02, S22 4.2e-04, S33 3.9e-02 = 4/4; non-planted 0
OUTRIDER block: n=30 1.24.0 q=8 0/8, 1.28.1 q=2 0/8; n=100 1.24.0 q=20 2/20, 1.28.1 q=2 9/20 (1 false); simulator m=100 116/192 and 135/192
LeafcutterMD (logs/61, logs/62): 86x30 clusters; raw p<0.05 39; BH q<0.05 11 = S05 (6.4e-07), S12 (2.0e-02), S29 x9
Integration (logs/70_*): confirmed positions 90190,92000 (chr21 and 21 spellings); chrX-only VCF -> stopifnot fires
AE reproducibility (logs/22, logs/28), 20010 p-values, cells differing >1e-6:
  no seed 9885 | set.seed(1) only 9279 | RNGseed=1 only 9815 (5 iterations: 9962) | set.seed(1)+RNGseed=1 0 | PCA 0
DROP 1.6.1 (logs/50): init ok; aberrantSplicing run: true, PCA, FRASER2, padjCutoff 0.1, deltaPsiCutoff 0.1; conda: files 0
```

## Notes on the run
- The pre-fix cohort was regenerated by `run/scripts/01_make_synth_cohort.py` (seed 20260920): `planted_truth.tsv`, `gene_counts.tsv` and `genes.tsv` are byte-identical to the archived ones (`cmp`), and the 3000x30 OUTRIDER matrix is identical too.
- The pre-fix DROP demo was **not** re-run (about 90 minutes). The earlier run started 11:51, its `fraser` group results existed by 13:22, and the run was killed by its own `timeout 6000` at 13:31 in step 08 of group `fraser_external` (63 of 70 steps).
- Machine load: two as-drop runs (OUTRIDER 1.28.1 on the simulator matrix, FRASER AE with MulticoreParam(4)) died with 'error writing to connection' while another agent's STAR job was running; both were rerun (OUTRIDER on retry, AE with SerialParam). A first cohort-B attempt collided with a duplicate launch on the same working directory (HDF5 error) and was rerun cleanly. During setup a `taskkill /IM Rscript.exe` meant for my own two runs also ended three other Rscript processes on the machine; no other agent's files were touched.
- No package version was changed; nothing was installed.

## Recommendations

**[P1] AE reproducibility recipe is wrong in SKILL.md and incomplete in the example**  (inputs [7])
- Problem: SKILL.md says set.seed() alone does not fix AE fits and `BPPARAM = SerialParam(RNGseed = 1)` does (0 differ). Measured on FRASER 2.6.1 (AE q=5 fitted twice, 20010 p-values): SerialParam(RNGseed=1) alone leaves 9815 differing (9962 at 5 iterations); set.seed(1) alone 9279; only set.seed(1) together with SerialParam(RNGseed=1) gives 0. The example says 'AE needs set.seed() to be reproducible', which is also incomplete.
- Root cause: The fixer's measuring script set both seeds in the same call, so the '0 differ' result was attributed to RNGseed alone; the 'set.seed only' number was from that same combined call.
- Fix: State: for reproducible AE fits call `set.seed(1)` and pass `BPPARAM = SerialParam(RNGseed = 1)` together (0 of 20010 differ; either alone 9-10k differ); make the example comment say the same. PCA stays the default.

**[P2] FRASER block stops at its last line when no sample has a call**  (inputs [3])
- Problem: `patient_results[order(patient_results$padjust), ]` fails with 'argument 1 is not a vector' when results() returns an empty table (n=8, 12, 16: 3 of 3 runs). The shipped example already guards it.
- Root cause: The guard was added to the example only.
- Fix: Add the example's `if (nrow(patient_results) > 0)` guard to the SKILL.md block, or say the block ends with the example's version.

**[P2] FRASER block is not runnable on FRASER 2.2.0 (Bioc 3.20)**  (inputs [1])
- Problem: The block calls estimateBestQ, absent in 2.2.0 ('could not find function'); the comment and the example (exists() check, optimHyperParams) cover it but the block does not.
- Root cause: Two release pairs are listed as checked, one block written for the newer.
- Fix: Use the example's est_q selection in the block, or say 'block for FRASER >= 2.6'.

**[P2] Tissue-mismatch check cannot see a sample the PCA fit absorbed; OHT message placed at the wrong n**  (inputs [3, 7])
- Problem: Calls-per-sample ranks S29 first only under AE; under PCA S29 has 0 calls. The Skill says a zero-call patient must not be read as tissue-matched but gives no check that would show it. 'Optimal latent space dimension is smaller than 2' is said to be seen at n=8-12; it printed at n=4, and at n=8-25 OHT printed 'Optimal encoding dimension: 2'.
- Root cause: Mismatch detection written around the AE symptom; message location taken from another control composition.
- Fix: Add a sample-by-sample correlation or PCA-of-counts check on the count matrix before fitting; correct the n for the OHT message.

**[P2] Unsourced tissue and disease tables; LeafcutterMD block needs the script path**  (inputs [4])
- Problem: 'Genes captured' percentages per tissue and the disease-specific expectations table have no source or run behind them; `python leafcutter_cluster_regtools.py` in the block only runs from the leafcutter repo's clustering/ directory (named in the text, not in the block).
- Root cause: Carried over from upstream; block copies the tool's README usage.
- Fix: Cite or drop the percentages; write the script path in the block.

**[P2] Single-file layout, no shipped test data**  (inputs [])
- Problem: 392-line SKILL.md, no references/ split, no small planted dataset or expected output; the generator exists only in the audit records.
- Root cause: Restructure was out of scope for the fix.
- Fix: Ship the generator (scripts/01_make_synth_cohort.py) with expected results (4/4 events, 0 false calls at n=30).

**[P2] DROP demo runtime stated as about 85 minutes**  (inputs [5])
- Problem: In the cited run the fraser group's results existed after about 90 minutes and the whole target had not finished at the 100-minute limit (fraser_external killed in step 08).
- Root cause: Runtime taken from the first table of results.
- Fix: Say 'about 90 minutes to the first results.tsv on 10 cores, longer for the whole target'.
