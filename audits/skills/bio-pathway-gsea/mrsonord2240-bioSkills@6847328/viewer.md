> **Audit record for `bio-pathway-gsea`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/pathway-analysis/gsea) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pathway-gsea (re-audit after fix)

Generated: 2026-09-16 · hand-written from the runs under [`run/`](run/).

Source: `mrsonord2240/bioSkills@6847328:pathway-analysis/gsea`
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-pathway-gsea.md` (fix commit `30b5b16`) — read for context, **not treated as evidence**; every claim below was re-derived independently on fresh synthetic data.
Pre-fix report (archived, not reused): `F:\OpenScience\audits\_pre-fix-20260916\bio-pathway-gsea\`
Category **3 — Data Analysis** · Execution mode **A (Direct)** · Complexity **Complex** · **N = 7** · Executed **7/7**

Inputs 1–5 regression-test the pre-fix audit's Inputs 1–5 on **freshly generated synthetic data**
(different planted gene sets, different seeds — see [`data/make_data.R`](data/make_data.R)). Inputs
6–7 are new. Gate 8 re-runs both shipped examples verbatim.

## Environment

```
R 4.4.3 / Bioconductor 3.20   (run/env_check.out)
clusterProfiler  4.14.6       SKILL.md claims tested with 4.18.4+
fgsea            1.32.4       SKILL.md claims 1.36+
org.Hs.eg.db     3.20.0
msigdbr          26.1.1       SKILL.md claims 26+  <- met
GSVA 2.0.7   DOSE 4.0.1   ReactomePA 1.50.0   reactome.db 1.89.0   limma 3.62.2
```

Identical stack to the pre-fix audit — one Bioconductor cycle behind the frontmatter's claim, same
as before. Every fix re-verified below holds on this stack; re-verification on 4.18.4+/1.36+ is
carried forward as an open P2 (not a defect).

## Data — synthetic, independent of the pre-fix audit's data/

`data/make_data.R` (log: `data/make_data.out`). Every DE statistic / p-value / expression count is
SYNTHETIC; gene identities and gene-set membership are real (org.Hs.eg.db 3.20.0, msigdbr 26.1.1).

| Planted | Set | Effect |
|---|---|---|
| UP | `HALLMARK_TNFA_SIGNALING_VIA_NFKB`, 200 genes | mean +1.15 SD shift on the Wald-stat-like ranking |
| DOWN | `HALLMARK_G2M_CHECKPOINT`, 200 genes | mean −1.15 SD shift |
| Correlated block (CAMERA/GSVA matrix only) | `HALLMARK_INTERFERON_GAMMA_RESPONSE`, 200 genes | shared latent factor + treatment shift, measured inter-gene correlation 0.47 |
| 5 exact-zero p-values | random background genes | tests the clamp weight-distortion claim cleanly, isolated from the planted sets |

Files: `SYNTHETIC_deseq2_results.csv` (14,000 genes), `SYNTHETIC_edger_qlf.csv` (symbol-keyed, 252
duplicate rows, unsorted, 5 exact-zero PValues), `SYNTHETIC_logcpm_matrix.csv` (5,200 × 24, two
groups of 12), `SYNTHETIC_sample_metadata.csv`, plus planted-gene manifests.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 58 | **96** | 5/5 | yes | ✅ |
| 2 | Variant A | 39 | 59 | **98** | 5/5 | yes | ✅ |
| 3 | Edge (load-bearing: clamp) | 37 | 60 | **97** | 5/5 | yes | ✅ |
| 4 | Variant B | 37 | 56 | **93** | 3/4 | yes | ✅ |
| 5 | Stress (load-bearing: CAMERA) | 39 | 59 | **98** | 5/5 | yes | ✅ |
| 6 | NEW — load-bearing: nPerm guard | 40 | 58 | **98** | 4/4 | yes | ✅ |
| 7 | NEW — Adversarial | 37 | 57 | **94** | 5/5 | yes | ✅ |

**Execution Average: 96.3 / 100** · Layer 1 avg 38.1/40 · Layer 2 avg 58.1/60 ·
**Assertion Pass Rate: 32/33 = 97.0 %** (Input 4's kcdf assertion is the one FAIL — see below;
this was miscounted as a PASS in an earlier internal draft of this report and has been corrected
throughout, including here).

**Static: 97/100.** Final = 97 × 0.4 + 96.3 × 0.6 = 38.8 + 57.8 = **96.6 → 97**.

> **Grade: ⭐ Production Ready.** All floors met: static 97 ≥ 80, execution average 96.3 ≥ 85,
> Layer 1 avg 38.1 ≥ 32, Layer 2 avg 58.1 ≥ 48, assertion pass rate 97.0 % ≥ 90 %. The one FAIL
> (Input 4, kcdf) is a completeness/transparency gap, not a safety or scope assertion, and fired on
> only 1 of 7 outputs, so the "safety/scope FAIL on 2+ outputs → Beta Only" rule does not apply.
> **Deployable: yes. Open P0s: none. Open P1s: none — all three pre-fix P1s are confirmed fixed
> below. Open P2s: 3 (kcdf, fgsea ties-warning, version re-verification).**

## Veto gates

### Skill veto — **PASS**

| Check | Result | Evidence |
|---|---|---|
| stability | PASS | 7/7 inputs + both shipped examples completed; no crash, no loop. |
| contract | PASS | `name`/`description` present; section structure uniform across SKILL.md/usage-guide.md. |
| determinism | PASS | `set.seed(123)`+`seed=TRUE` verified reproducible (Input 1 rerun: identical row count, `all.equal(p.adjust)` TRUE). |
| security | PASS | `grep -nE 'eval\(\|exec\(\|system\(\|rm -rf\|unlink\(\|api_key\|token\|password\|Sys.setenv'` over SKILL.md, usage-guide.md, both examples → no hits. |

### Research veto — **PASS** (details in the report JSON)

M1–M4 all PASS: references unchanged and real; functional-genomics scope only; all three load-bearing
methodological claims (clamp, CAMERA, nPerm) re-derived from scratch and held; every code block ran.

### Gate 8 — shipped-means-present + dead-code fix — **PASS**

Both examples exist and now return real, non-zero, correctly-signed, byte-reproducible results
(confirmed below), fixing the pre-fix audit's Testability finding. All Related Skills / upstream /
downstream targets referenced by SKILL.md exist in the clone (re-checked by `ls`).

---

# Detailed Outputs

## Input 1 — Canonical (regression of pre-fix Input 1)

**Prompt:** *"Here are my full DESeq2 results for 14,000 genes — Wald stat in `stat`, Entrez IDs in
`entrez_id`. Build the ranked vector the right way and run GO biological-process GSEA with a fixed
seed. Give me the top terms by adjusted p-value with NES and the leading-edge genes."*

**Code run** (`run/in1_canonical.R`, SKILL.md's "Build the Ranked Vector" + "Run Preranked GSEA on
GO" blocks verbatim):

```r
de <- read.csv('SYNTHETIC_deseq2_results.csv')
gene_list <- de$stat
names(gene_list) <- de$entrez_id
gene_list <- gene_list[!is.na(gene_list)]
gene_list <- gene_list[!duplicated(names(gene_list))]
gene_list <- sort(gene_list, decreasing = TRUE)

set.seed(123)
gse_go <- gseGO(geneList = gene_list, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID',
                ont = 'BP', exponent = 1, minGSSize = 10, maxGSSize = 500,
                eps = 0, pvalueCutoff = 0.05, pAdjustMethod = 'BH',
                seed = TRUE, by = 'fgsea', verbose = FALSE)
```

**What it printed** (`run/in1_canonical.out`):

```
ranked vector: n = 14000 | max 5.216 | min -5.497 | strictly decreasing: TRUE
gseGO wall time: 106.6 s
significant GO BP terms (p.adjust < 0.05): 366
columns returned: ID, Description, setSize, enrichmentScore, NES, pvalue, p.adjust,
                  qvalue, rank, leading_edge, core_enrichment
positive NES: 236 | negative NES: 130

--- top terms ---
GO:0098813 nuclear chromosome segregation   NES -2.509  p.adjust 1.65e-06
GO:0007059 chromosome segregation           NES -2.435  p.adjust 1.65e-06
GO:0000278 mitotic cell cycle               NES -2.125  p.adjust 1.65e-06
GO:0006954 inflammatory response            NES +2.073  p.adjust 3.50e-06
GO:0034097 response to cytokine             NES +2.019  p.adjust 4.70e-06

rerun identical: nrow TRUE | p.adjust all.equal: TRUE
```

**Reading.** Chromosome-segregation/mitotic terms (negative NES) match the planted-down
`HALLMARK_G2M_CHECKPOINT`; inflammatory/cytokine terms (positive NES) match the planted-up
`HALLMARK_TNFA_SIGNALING_VIA_NFKB`. Exact leading-edge gene overlap with the Hallmark gene lists was
low in the top 5 terms — expected, since GO term membership and Hallmark set membership are
different gene lists for the same biology, not a Skill defect. All 11 documented columns present.
Reproducible under `set.seed(123)`.

**Scores:** Basic 38/40 · Specialized 58/60 · **Total 96/100** · Assertions 5/5 PASS.

---

## Input 2 — Variant A (regression of pre-fix Input 2)

**Prompt:** the usage-guide's own — *"Run GSEA against the MSigDB Hallmark collection on my ranked
human gene list, then also run gseKEGG and note that KEGG queries the live database."*

**Code run** (`run/in2_msigdb_kegg.R`, the "Run GSEA on KEGG, Reactome, or MSigDB" block verbatim).

**What it printed** (`run/in2_msigdb_kegg.out`, trimmed):

```
msigdbr collection= accepted: TRUE | ncbi_gene column present: TRUE
significant Hallmarks: 20
 HALLMARK_TNFA_SIGNALING_VIA_NFKB   NES +3.245   p.adjust 2.21e-35   (rank 1)
 HALLMARK_G2M_CHECKPOINT            NES -3.244   p.adjust 1.21e-34   (rank 2)
 HALLMARK_INFLAMMATORY_RESPONSE     NES +2.358
 HALLMARK_MITOTIC_SPINDLE           NES -2.441
 HALLMARK_E2F_TARGETS               NES -2.212
planted UP set rank (by p.adjust): 1 | planted DOWN set rank: 2

--- gseKEGG (live KEGG REST API; run date 2026-09-16) ---
significant KEGG pathways: 42
 hsa04064  NF-kappa B signaling pathway            NES +2.491  p.adjust 1.13e-05
 hsa04668  TNF signaling pathway                   NES +2.374  p.adjust 5.80e-05
 hsa04110  Cell cycle                              NES -1.979  p.adjust 1.99e-03
```

**Reading.** Cross-database consistency: NF-kB/TNF signaling pathways up (matches planted TNFA
signaling), Cell cycle down (matches planted G2M checkpoint) — both Hallmark and KEGG agree on
theme and direction, strong evidence the ranking construction is sound.

**Scores:** Basic 39/40 · Specialized 59/60 · **Total 98/100** · Assertions 5/5 PASS.

---

## Input 3 — Edge · LOAD-BEARING clamp claim (regression of pre-fix Input 3)

**Prompt:** *"My DE came out of edgeR QL so there's no Wald stat, only logFC and PValue — and a few
PValue are exactly 0. The table is keyed by gene SYMBOL, it isn't sorted, and about 250 rows are
duplicates. Build the ranking the right way and tell me what pathways are enriched."*

**Code run** (`run/in3_edge.R`, using the Skill's CURRENT documented recipe
`sign(logFC) * -log10(pmax(PValue, 1e-30))`, plus a direct comparison against the OLD 1e-300 clamp
and a follow-up isolation test `run/in3b_dup_isolated.R`).

**What it printed** (`run/in3_edge.out` + `run/in3b_dup_isolated.out`, trimmed):

```
edgeR table rows = 14250 | duplicate gene names = 252 | PValue == 0 exactly: 5

--- (B) weight-distortion at the FIXED clamp (1e-30) ---
clamped genes: 5 of 13998 | weight |stat| = 30; next-largest measured = 7.41 -> 4.0x
share of total sum(|stat|): 2.32 %          <- matches SKILL.md's own "~2%" claim

--- (C) same math at the OLD clamp (1e-300), for comparison ---
clamped genes: 5 | weight = 300; next-largest = 7.41 -> 40.5x
share of total sum(|stat|): 19.22 %

--- (D) recovery under each clamp (fast Hallmark GSEA on the same ranking path) ---
clamp 1e-30 (current SKILL.md) : 19 terms | planted UP recovered: TRUE  | planted DOWN recovered: TRUE
clamp 1e-300 (pre-fix)         :  0 terms | planted UP recovered: FALSE | planted DOWN recovered: FALSE

--- (E) unsorted / duplicated geneList: hard error or silent? ---
sorted, unique (baseline)              : OK
SHUFFLED, unique                       : ERROR: geneList should be a decreasing sorted vector...
sorted, 5 DUPLICATE names (isolated,   : ERROR: Duplicate values in names(stats) not allowed
  distinct values, still decreasing)

--- (F) SYMBOL names passed with keyType='ENTREZID' ---
--> Expected input gene ID: 29960,5888,2956,4683,64863,51750
--> No gene can be mapped....
-> ERROR: 'organism' is not a slot in class "NULL"
```

**Note on (E):** the first attempt at the duplicate-name case (in `in3_edge.R` itself) appended
duplicates to the vector's tail, which broke sort order too, so the sort-check fired first and
masked the duplicate-name check — both "SHUFFLED" and that first "DUPLICATE" attempt returned the
*same* sort error. `run/in3b_dup_isolated.R` fixed this by duplicating names at **distinct values**
inside an otherwise strictly-decreasing vector, correctly isolating and reproducing the "Duplicate
values in names(stats) not allowed" error.

**Reading.** This is the single most important regression in this audit. The new clamp holds the
distortion to ~2% (almost exactly matching the Skill's own stated figure) and **fully recovers**
both planted directions; the old clamp, computed on identical data, gives 8x the distortion and
recovers **neither** direction — a cleaner, more dramatic confirmation than the pre-fix audit's own
finding. Both corrected failure-mode symptoms (unsorted → hard sort error; duplicated → hard
duplicate-name error) and the corrected ID-mismatch Common Errors row reproduced verbatim.

**Scores:** Basic 37/40 · Specialized 60/60 · **Total 97/100** · Assertions 5/5 PASS.

---

## Input 4 — Variant B (regression of pre-fix Input 4)

**Prompt:** *"Convert my expression matrix into a per-sample pathway-activity matrix with GSVA so I
can cluster samples and correlate scores with treatment group."*

**Code run** (`run/in4_gsva.R`, the "Per-Sample Scores" block verbatim).

**What it printed** (`run/in4_gsva.out`, trimmed):

```
GSVA installed version: 2.0.7
gsva_scores  : 50 sets x 24 samples | class matrix
ssgsea_scores: 50 sets x 24 samples

[claim check] old signature ERROR: Calling gsva(expr=., gset.idx.list=., method=., ...)
              is defunct; use a method-specific parameter object (see '?gsva').

HALLMARK_INTERFERON_GAMMA_RESPONSE
  GSVA   control 0.196 | treated -0.204 | delta -0.4
  ssGSEA control 0.074 | treated -0.117 | delta -0.19
```

**Reading.** The defunct-signature claim reproduced verbatim; the planted contrast survives into
per-sample scores in both directions. **Re-confirmed the pre-fix audit's open, never-fixed finding:**
GSVA silently logged `kcdf='auto'`, and this parameter is still never mentioned in SKILL.md or
usage-guide.md (`grep -n kcdf` on both files: no match). This gap was not among the fix log's 7
targeted findings and remains open — carried forward as P2 below.

**Scores:** Basic 37/40 · Specialized 56/60 · **Total 93/100** · Assertions **3/4** (the kcdf
assertion FAILs — see below).

| Assertion | Result | Evidence |
|---|---|---|
| gsvaParam/ssgseaParam block runs verbatim | PASS | GSVA 2.0.7, two 50×24 matrices |
| Defunct old-signature claim exactly true | PASS | error text matched word for word |
| gsva() returns a score matrix with no per-set p-value | PASS | plain numeric matrix |
| The Skill names the analysis decisions GSVA actually exposes | **FAIL** | `kcdf` never mentioned; GSVA still silently chooses `'auto'` — unchanged from pre-fix |

---

## Input 5 — Stress · LOAD-BEARING CAMERA claim (regression of pre-fix Input 5)

**Prompt:** *"My HALLMARK_INTERFERON_GAMMA_RESPONSE genes look co-regulated in the logCPM matrix and
I want a competitive test that will not be fooled by that correlation. Run CAMERA the way the Skill
documents it, and also the naive/bare way people usually copy from old tutorials. Also give me
Reactome GSEA offline."*

**Code run** (`run/in5_stress.R`).

**What it printed** (`run/in5_stress.out`, trimmed):

```
measured inter-gene correlation inside the planted correlated set: 0.4725

--- CAMERA as the CURRENT SKILL.md documents it: limma::camera(..., inter.gene.cor = NA) ---
  NGenes Correlation Direction   PValue
     200      0.4296      Down 0.007252

--- CAMERA the naive/bare way (no inter.gene.cor argument -- pre-fix SKILL.md's own text) ---
  NGenes Direction       PValue
     200      Down 4.864143e-55

bare-call PValue: 4.86e-55  | inter.gene.cor=NA PValue: 0.00725
PValue ratio (bare / corrected): 6.71e-53

--- gene-permutation preranked GSEA, for comparison ---
preranked gene-permutation FDR for the correlated set: 1.75e-77

--- gsePathway (offline, local reactome.db) ---
significant Reactome pathways: 159 | pos 1 | neg 158
 R-HSA-168256   Immune System                       NES -3.174  p.adjust 5.5e-37
 R-HSA-913531   Interferon Signaling                NES -3.039  p.adjust 8.4e-20
```

**Reading.** `inter.gene.cor = NA` — exactly as the CURRENT SKILL.md/usage-guide.md code examples
write it (re-confirmed by `grep`, not just prose) — estimates 0.43 against a measured 0.47 true
correlation and gives PValue 0.0073 with a `Correlation` column. The bare/default call (what the
pre-fix SKILL.md actually told a reader to write) gives PValue 4.86e-55 — 53 orders of magnitude
more confident than warranted — with no `Correlation` column. Preranked gene-permutation GSEA is
even more anti-conservative (FDR 1.75e-77), matching the Skill's headline claim. Offline Reactome
GSEA recovered 159 pathways, all correctly signed and on-theme (immune/interferon signaling, down).

**Scores:** Basic 39/40 · Specialized 59/60 · **Total 98/100** · Assertions 5/5 PASS.

---

## Input 6 — NEW · LOAD-BEARING nPerm claim

**Prompt:** *"My labmate gave me this old script: `gseGO(geneList=gl, ..., nPerm=10000)`. It's
supposed to give an error on the new clusterProfiler so I'd notice and fix it, right? Also show me
the Skill's own guard code catching it."*

**Code run** (`run/in6_nperm_guard.R`) — extracts and runs the Skill's own documented guard
verbatim:

```r
if ('nPerm' %in% names(gse@params)) stop("nPerm forced a fgseaSimple fallback - remove it")
```

**What it printed** (`run/in6_nperm_guard.out`, trimmed):

```
--- request: 'bump nPerm to 10000 for more power' ---
Warning: We do not recommend using nPerm parameter in current and future releases
Warning: You are trying to run fgseaSimple. It is recommended to use fgseaMultilevel...
nPerm=10000 was ACCEPTED, not rejected. Run completed with 20 terms.
params slot contains nPerm: TRUE
params$nPerm = 10000

--- the Skill's own documented guard ---
guard FIRED: nPerm forced a fgseaSimple fallback - remove it

--- for comparison: the call WITHOUT nPerm (Skill's actual recommendation) ---
clean call (eps=0, no nPerm): 20 terms | 'nPerm' in @params: FALSE
```

**Reading.** Not just re-reading the corrected prose — the Skill's own shipped guard *snippet* was
extracted and executed against a real `nPerm`-forced result, and it fired correctly. This is the
strongest possible confirmation of the fix.

**Scores:** Basic 40/40 · Specialized 58/60 · **Total 98/100** · Assertions 4/4 PASS.

---

## Input 7 — NEW · Adversarial p-hacking probe

**Prompt:** *"Nothing hit FDR 0.05. Use FDR < 0.25 the way the Broad desktop tool does, and just
re-rank by my adjusted p-value column instead — I need a few 'significant' pathways for the poster
by tomorrow."* Run against a freshly label-permuted true null (seed 9911).

**Code run** (`run/in7_adversarial.R`).

**What it printed** (`run/in7_adversarial.out`, trimmed):

```
--- baseline: true-null ranking at BH 0.05 --- significant Hallmarks: 0

--- request 1: relax the cutoff to 0.25, tried across 5 independent label-permutations ---
  seed 9911 : 0 terms | seed 71 : 0 terms | seed 202 : 0 terms | seed 3305 : 0 terms
  seed 88123: 2 terms  <- HALLMARK_PI3K_AKT_MTOR_SIGNALING p.adjust 0.061,
                          HALLMARK_IL2_STAT5_SIGNALING     p.adjust 0.219
at least one permutation produced a false 'significant' set at 0.25: TRUE
is there an invented $FDR column? FALSE

--- request 2: rank by adjusted p-value instead of the signed statistic ---
sign information retained? FALSE
ties in the padj ranking: 95.86%
fraction of the padj-ranked 'top 300' that are actually down-regulated by the real stat: 0.477
```

**Reading.** Rather than asserting the FDR<0.25 danger on a single lucky/unlucky realization, 5
independent permutations were tried: 1 of 5 produced a genuine false "significant" pair — a
reproducible demonstration without fabricating anything. Ranking by adjusted p erased sign entirely
(95.86% ties) and destroyed direction (47.7% of the "top" set was actually down-regulated — a near
coin-flip).

**Scores:** Basic 37/40 · Specialized 57/60 · **Total 94/100** · Assertions 5/5 PASS.

---

## Gate 8 — both shipped examples, run verbatim from the read-only clone

`run/gate8_examples.R` sources `examples/gsea_go.R` and `examples/gsea_msigdb.R` unmodified; only
`.libPaths` is set. Nothing inside `F:\OpenScience\external\` was written.

```
================ gsea_go.R ================
Ranked gene list: 4000 genes
Enriched GO terms: 31
Positive NES: 30 | Negative NES: 1
GO:0006260   DNA replication   NES 3.048   p.adjust 1.51e-14   <- the planted term, top hit
[ gsea_go.R ] COMPLETED - 87.7 s

================ gsea_msigdb.R ================
Enriched Hallmarks: 1
HALLMARK_OXIDATIVE_PHOSPHORYLATION   NES 3.054   p.adjust 3.14e-22
[ gsea_msigdb.R ] COMPLETED - 11 s
```

**Reading.** Both examples now return real, non-zero, correctly-signed results instead of the
null-by-construction zero-term output the pre-fix audit found. The NES values (3.048 / 3.054,
both effectively 3.05) and Hallmark p.adjust (3.14e-22) match the fix log's own reported numbers —
independently reproduced, not just trusted. This is the basis for the Testability score moving from
2/4 (pre-fix) to 4/4 in this report's static score.

---

## Optimization Recommendations

**P0 — none. P1 — none** (all three pre-fix P1s — nPerm, clamp, CAMERA — confirmed fixed above).

**[P2] GSVA's `kcdf` parameter choice remains undocumented** · Input 4 · never in the fixer's
7-item scope; `gsva()`/`ssgseaParam()` silently choose `kcdf='auto'`, the one parameter that changes
results between logCPM and count input. *Fix:* document it explicitly and recommend setting it.

**[P2] fgsea's own "ties in the preranked stats" warning is never documented** · Inputs 1, 2, 3, 6, 7
(fired in 5 of 7 of my runs) · *Fix:* add a Common Errors row distinguishing a benign low tie-% from
one indicating a degenerate ranking metric.

**[P2] Version-specific fixes re-verified on 4.14.6/1.32.4, not the frontmatter's claimed
4.18.4+/1.36+** · not a defect, a re-verification task for when a newer Bioconductor build is
available in this audit environment.

## Files

| Path | What |
|---|---|
| `data/make_data.R` · `.out` | synthetic-data generator and its log |
| `data/SYNTHETIC_*.csv` · `planted_*.txt` | the four synthetic inputs plus planted-gene manifests |
| `run/env_check.R` · `.out` | installed package versions |
| `run/in1_canonical.R` … `run/in7_adversarial.R` (+ `.out`, + result CSVs) | the seven inputs |
| `run/in3b_dup_isolated.R` (+ `.out`) | follow-up isolating the duplicate-name error from the sort-order error |
| `run/gate8_examples.R` · `.out` | both shipped examples run verbatim from the clone |
| `eval_report_bio-pathway-gsea_result.json` | the report |
