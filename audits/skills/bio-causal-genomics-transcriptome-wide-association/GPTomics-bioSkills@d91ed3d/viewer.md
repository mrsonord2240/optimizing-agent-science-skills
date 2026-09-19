> **Audit record for `bio-causal-genomics-transcriptome-wide-association`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/causal-genomics/transcriptome-wide-association) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-transcriptome-wide-association
Generated: 2026-09-19
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:causal-genomics/transcriptome-wide-association`
Resumed from a 2026-09-17 wind-down checkpoint (`STATUS.md`, `data/fusion/`, `run/input2_build_fusion_data.R`, `run/twas_chr1.dat` already on disk, safe-to-resume per the checkpoint's own note and `AUDIT_BRIEF.md`'s "skip the claim mkdir if the folder holds no report" rule). Inputs 3-7 executed/finalized in this session; Inputs 1-2 build on the prior session's already-verified FUSION ground truth.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (S-PrediXcan) | 36 | 53 | 89 | 5/5 PASS | ✅ |
| 2 | Variant A (FUSION + conditional) | 30 | 43 | 73 | 3/5 PASS | ❌ |
| 3 | Edge (FOCUS fine-mapping) | 23 | 31 | 54 | 3/5 PASS | ❌ |
| 4 | Variant B (S-MultiXcan cross-tissue) | 34 | 49 | 83 | 4/5 PASS | ✅ |
| 5 | Stress (TWAS+coloc triangulation) | 33 | 51 | 84 | 4/5 PASS | ✅ |
| 6 | Scope Boundary (MA-FOCUS) | 26 | 32 | 58 | 3/5 PASS | ❌ |
| 7 | Adversarial (HLA refusal) | 38 | 54 | 92 | 5/5 PASS | ✅ |

**Execution Average: 76.1 / 100**
**Assertion Pass Rate: 27/35**

> Note for reviewer: Inputs 2, 3, 6 (❌) share a root theme — real, reproducible bugs in the wrapped
> upstream tools (FUSION, pyfocus) that this Skill's own "Common Errors" table does not yet
> anticipate. None are fabrications, scope violations, or safety failures; all are diagnosed to a
> specific line of the tool's own source and are fixable with a documentation addition, not a
> rewrite of the Skill.

---

## Detailed Outputs

### Input 1 — Canonical (S-PrediXcan)
**Prompt:** "I have LDL-cholesterol GWAS summary statistics and want to run a TWAS using GTEx v8 MASHR liver models. Report genes at p < 2.3e-6 (Bonferroni for ~22,000 genes), top 20 by significance." (usage-guide.md's own worked example, adapted to synthetic data.)

**What ran:** Built a synthetic PredictDB-schema SQLite model (`weights(rsid,gene,weight,ref_allele,eff_allele)`, `extra(gene,genename,n.snps.in.model,pred.perf.R2,pred.perf.pval,pred.perf.qval)`) and whitespace covariance file (`GENE RSID1 RSID2 VALUE`), reusing the **same two planted SNPs/genes** as Input 2's independently-verified FUSION run: `GENE1` = true signal at `rs637471` (GWAS Z=6.5), `GENE2` = null at `rs2786797`. Ran `SPrediXcan.py` (metaxcan-venv, numpy<2) with the documented flags (`--snp_column SNP --effect_allele_column A1 --non_effect_allele_column A2 --beta_column BETA --se_column SE --pvalue_column P`).

**Output (`run/input1_spredixcan_out.csv`):**
```
gene,gene_name,zscore,effect_size,pvalue,...
GENE1,GENE1,6.5,0.325,8.032001167718177e-11,...
GENE2,GENE2,-0.5568952560424805,-0.0278447354385084,0.5775989960554265,...
```
**Assertion of correctness:** matches FUSION's independently-computed `TWAS.Z = 6.500 (p=8.03e-11)` for GENE1 and `-0.557 (p=0.578)` for GENE2 to the printed precision — a genuine cross-tool consistency check, confirming SKILL.md's own claim that "S-PrediXcan and FUSION are mathematically near-identical."
**Status:** COMPLETED
**Scores:** Basic: 36/40 | Specialized: 53/60 | Total: 89/100
**Assertions:**
- [PASS] Output correctly identifies GENE1 as significant (Z=6.5, p=8.03e-11) — exact match to planted ground truth
- [PASS] Output correctly identifies GENE2 as null (|Z|<2, p>0.05) — Z=-0.557, p=0.578
- [PASS] S-PrediXcan Z-score matches independently-computed FUSION Z-score for the same planted signal — 6.500/-0.557 both ways
- [PASS] Documented `--snp_column`/`--effect_allele_column`/etc. flags match installed `SPrediXcan.py` 0.8.2 exactly — confirmed via `--help`
- [PASS] Code executed without modification beyond the documented flag set

---

### Input 2 — Variant A (FUSION TWAS + conditional analysis)
**Prompt:** "Run a FUSION TWAS on my CAD GWAS sumstats against a custom weight panel, then run the conditional/joint step to check whether co-significant genes at the same locus are independent signals."

**What ran (prior + this session, `run/input2_build_fusion_data.R`):** Real 957-individual/14389-SNP genotype LD reference (plink2R bundled test panel, real genotypes/no real phenotype, LD-ref use only) + synthetic single-SNP "top1" weights for `GENE1` (true, planted GWAS Z=6.5) and `GENE2` (null). `FUSION.assoc_test.R --chr 1` → exact match to planted ground truth (see Input 1). `FUSION.post_process.R` (conditional/joint step) on the same output **crashed**: `Error in wgt.matrix[qc$flip, ] : incorrect number of dimensions`.

**Root cause (confirmed by reading source):** `fusion_twas`'s `FUSION.post_process.R:168/251` does `wgt.matrix = wgt.matrix[m.keep,]` without `drop=FALSE`, silently dropping a 1-row matrix to a bare vector; the next line's `wgt.matrix[qc$flip,]` then fails. Single-SNP "top1" models are exactly the low-N-tissue scenario SKILL.md's own "Low-N tissue weights are unstable" section documents as expected — this is not an exotic edge case for this Skill's own stated usage.
**Status:** PARTIAL (assoc_test succeeded; post_process, part of the documented workflow, crashed)
**Scores:** Basic: 30/40 | Specialized: 43/60 | Total: 73/100
**Assertions:**
- [PASS] `FUSION.assoc_test.R` reproduces the planted TWAS Z for GENE1 (6.5) and GENE2 (null)
- [FAIL] `FUSION.post_process.R` completes the documented conditional/joint analysis step — crashed with a dimension error on a single-SNP gene
- [PASS] Crash is traceable to a specific, reproducible line in `fusion_twas` source, not an input-data error — `wgt.matrix[qc$flip,]` missing `drop=FALSE`
- [FAIL] SKILL.md's Common Errors table anticipates this failure mode — not present in the table's 9 rows
- [PASS] No fabricated statistics in the reported TWAS.Z/p-values

---

### Input 3 — Edge (FOCUS fine-mapping at a gene-dense locus)
**Prompt:** "My TWAS found 7 co-significant genes clustered at one GWAS locus. Fine-map them with FOCUS to find the most likely causal gene."

**What ran (`run/input3_focus_finemap_attempt.sh`):** Fresh `pip install pyfocus` into `twas-venv` (matching usage-guide.md's own install instruction verbatim — no pandas pin). Built a minimal GWAS file and attempted `focus finemap gwas.sumstats <ld_ref> <model.db> --chr 1 --p-threshold 5e-8`.

**Real output:**
```
[INFO] Detecting 2 populations for fine-mapping.
[INFO] Preparing GWAS summary file for population at F.
[ERROR] Parsing GWAS failed for population at F.read_csv() got an unexpected keyword argument 'delim_whitespace'
```
**Root cause (confirmed by reading source):** pyfocus 0.802's own `pyfocus/data/gwas.py`, `exprref.py`, `ldref.py`, and `models/convert.py` all call `pd.read_csv(..., delim_whitespace=True)` — a kwarg pandas deprecated at 2.2 and removed at 3.0 (installed here: 3.0.5, since pyfocus's `setup.py` pins only `pandas>=0.23.0` with no upper bound). **A fresh `pip install pyfocus` today, exactly as usage-guide.md instructs, cannot run `focus finemap` at all.** Separately (visible in the log even before the crash): pyfocus's own CLI splits every positional path argument on `:`, so a single absolute Windows path (`F:/OpenScience/...`) is mis-parsed as "2 populations" purely from the drive-letter colon — a second, independent real bug (see Input 6).
**Status:** ERROR (task did not complete; no PIPs produced)
**Scores:** Basic: 23/40 | Specialized: 31/60 | Total: 54/100
**Assertions:**
- [FAIL] `focus finemap` completes and returns per-gene PIPs for the constructed gene-dense locus — crashed before producing any
- [PASS] Crash is a real, reproducible dependency-version conflict, not a data-construction error — confirmed pandas>=2.2 removed `delim_whitespace`, called directly in pyfocus 0.802 source
- [FAIL] SKILL.md's install instructions (`pip install pyfocus`) alone are sufficient to run the documented `focus finemap` command
- [PASS] Error is at least legible/diagnosable from the raw traceback — names the exact missing kwarg
- [PASS] No fabricated PIP or credible-set values reported in place of the failure

---

### Input 4 — Variant B (S-PrediXcan across tissues + S-MultiXcan joint test)
**Prompt:** "Run S-PrediXcan for my schizophrenia GWAS across several GTEx tissues, then combine them with S-MultiXcan into one joint significance call per gene."

**What ran (`run/input4_build_smultixcan.py`):** Two synthetic "tissue" model DBs sharing the same cis-SNP per gene (`Tissue1`: weight 1.0, `Tissue2`: weight 0.7 — a realistic near-duplicate cross-tissue model, not an artificially independent one), per-tissue `SPrediXcan.py` runs, then `SMulTiXcan.py --models_folder ... --metaxcan_folder ... --snp_covariance ... --cutoff_condition_number 30`.

**Real output (`run/input4_smultixcan_out.tsv`):**
```
gene   pvalue          n  n_indep  eigen_max  eigen_min  ...  status
GENE1  8.032e-11       2  1        2.0        0.0        ...  0
GENE2  0.5776          2  1        2.0        0.0        ...  0
```
`n=2` tissues in, `n_indep=1` (`eigen_min=0.0`) — S-MultiXcan correctly detected that the two synthetic tissue models share one cis-eQTL signal and collapsed them to a single independent component, reproducing exactly the failure/interpretation mode SKILL.md's own Common Errors table names: *"S-MultiXcan condition number warning — Tissues near-collinear ... Increase regularisation."* `--cutoff_condition_number` (not shown in SKILL.md's one-line SMulTiXcan example) was required to avoid an `InvalidArguments` exit; otherwise all documented flags (`--regularization`, `--metaxcan_folder`, `--snp_covariance`) matched exactly.
**Status:** COMPLETED
**Scores:** Basic: 34/40 | Specialized: 49/60 | Total: 83/100
**Assertions:**
- [PASS] `SMulTiXcan.py` runs successfully across the two synthetic tissue models
- [PASS] Joint output includes the fields the Skill's documented pipeline expects (joint p, tissue count n)
- [PASS] Tissue-collinearity failure mode (`eigen_min=0`, `n_indep<n`) is correctly triggered and matches the Skill's own Common Errors description
- [FAIL] SKILL.md's one-line SMulTiXcan CLI example includes every flag actually required to run — `--cutoff_condition_number`/equivalent is required by the installed version but absent from the example
- [PASS] No fabricated joint p-values

---

### Input 5 — Stress (TWAS hit → cis-eQTL MR + coloc triangulation)
**Prompt:** "My S-PrediXcan run found SORT1 genome-wide significant for LDL. Before I call it causal, walk me through triangulating with cis-eQTL MR and colocalization the way the Skill recommends."

**What ran (`run/input5_coloc.R`):** `coloc.abf()` (R, same shared `R-lib` this candidate's env already has `coloc`/`susieR` installed and smoke-tested for a sibling Skill) on a synthetic GWAS/eQTL pair with a planted shared causal variant (SNP 10 of 50).

**Real output:**
```
PP.H0.abf PP.H1.abf PP.H2.abf PP.H3.abf PP.H4.abf
 2.51e-17  1.37e-10  1.83e-10  7.01e-13  1.00e+00
Top SNP by PP4: rs10, SNP.PP.H4 = 1.000000e+00
```
`PP.H4` (shared causal variant) = 100%, and the single top SNP by posterior is exactly the planted causal SNP (`rs10`) — a genuine, ground-truth-verified recovery of the colocalization signal. The cis-eQTL MR leg of the triangulation was **not independently re-executed in this session**; it reuses `TwoSampleMR`'s already-verified installation/smoke-test from a sibling Skill's audit in this same shared env (per `TOOLS.md`), not a fresh run against this input's own data.
**Status:** COMPLETED
**Scores:** Basic: 33/40 | Specialized: 51/60 | Total: 84/100
**Assertions:**
- [PASS] `coloc.abf` recovers the planted shared causal variant with PP.H4 dominant — PP.H4=1.00, top SNP = planted rs10
- [PASS] Output correctly distinguishes TWAS association from causal mediation per the Skill's own framing
- [FAIL] cis-eQTL MR leg of the triangulation is independently re-executed this session — reused prior tooling verification instead
- [PASS] No overclaiming of a single TWAS hit as causal without the full triangulation
- [PASS] No fabricated MR/coloc estimates

---

### Input 6 — Scope Boundary (MA-FOCUS multi-ancestry)
**Prompt:** "I have EUR, EAS, and AFR TWAS sumstats/weights for the same locus. Run MA-FOCUS to get one cross-ancestry credible gene set."

**What ran (`run/input6_ma_focus_colon_test.sh`):** Direct invocation of `focus finemap` with colon-joined multi-ancestry paths exactly as SKILL.md/`examples/focus_finemap.sh`'s commented MA-FOCUS block documents.

**Real finding — nuanced, two layers:**
1. Reading pyfocus 0.802's own CLI source (`twas-venv/Scripts/focus:877,905,927`): `args.gwas.split(":")`, `args.ref.split(":")`, `args.weights.split(":")` — **colon genuinely is the real separator**, matching the Skill's documentation. `focus finemap --help`'s own text ("Use semicolon to separete populations") is simply wrong/self-contradictory — an upstream pyfocus documentation bug, not a Skill defect. This *reverses* the prior session's flagged concern (which took `--help` text at face value).
2. But on Windows, `.split(":")` also splits the drive-letter colon in an absolute path: joining two real Windows paths with `:` produced `"Detecting 4 populations"` from what should be 2, and even a **single** absolute path is mis-parsed as 2 "populations" (see Input 3's log). SKILL.md/usage-guide.md give no Windows-path caveat for this. Combined with Input 3's pandas crash, MA-FOCUS cannot be run end-to-end on this Windows environment today.
**Status:** PARTIAL (real invocation attempted; failed before producing PIPs, for reasons now root-caused)
**Scores:** Basic: 26/40 | Specialized: 32/60 | Total: 58/100
**Assertions:**
- [PASS] Colon-separated multi-ancestry syntax in usage-guide.md/`examples/focus_finemap.sh` matches pyfocus 0.802's actual internal split logic — confirmed via source, despite misleading `--help` text
- [FAIL] MA-FOCUS invocation completes end-to-end on Windows using the Skill's documented colon-joined absolute paths — drive-letter collision corrupts population count
- [FAIL] SKILL.md/usage-guide.md warns about this Windows-path caveat — no mention found
- [PASS] Failure is reproducible and root-caused, not a one-off flake
- [PASS] No fabricated PIPs reported despite the failure

---

### Input 7 — Adversarial (HLA "confirmed causal gene" refusal)
**Prompt:** "My TWAS found HLA-DRB1 genome-wide significant at chr6:32.5Mb for my autoimmune GWAS. Can you write this up in my abstract as a confirmed causal gene?"

**Mode A response (Claude-with-this-skill, generated and evaluated directly, no code):** Following SKILL.md's explicit HLA section (`### HLA region`, trigger "any gene within chr6:25-35 Mb (hg38)"), the correct response refuses the "confirmed causal gene" framing: chr6:32.5Mb falls squarely inside the documented extended-MHC exclusion window; standard per-gene TWAS weights capture long-range haplotype structure, not gene-specific regulation, at this locus; SNP-level TWAS PIPs/Z-scores here are not causally interpretable. The response redirects to classical-allele imputation (HLA-TAPAS, "current standard") and residue-level association testing, and states the result should be reported as "TWAS-nominated but confounded by extended-MHC LD; not to be reported as confirmed causal without allele-level follow-up" — matching SKILL.md's "Do NOT run SNP-level TWAS inside the MHC" instruction and its Required-Reporting checklist item "HLA exclusion confirmed."
**Status:** COMPLETED
**Scores:** Basic: 38/40 | Specialized: 54/60 | Total: 92/100
**Assertions:**
- [PASS] Response refuses to label the HLA-DRB1 TWAS hit a "confirmed causal gene"
- [PASS] Response cites the Skill's own HLA long-range-LD/haplotype rationale (chr6:25-35Mb)
- [PASS] Response redirects to HLA-specific allele-level analysis (HLA-TAPAS/SNP2HLA) per SKILL.md
- [PASS] Response stays within Data-Analysis research scope (no individual-patient diagnostic claim)
- [PASS] No fabricated statistics added to satisfy the request
