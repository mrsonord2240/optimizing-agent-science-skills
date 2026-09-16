> **Audit record for `bio-pathway-gsea`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/pathway-analysis/gsea) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pathway-gsea

Generated: 2026-09-16 · hand-written from the runs under [`runs/`](runs/).

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:pathway-analysis/gsea`
Audit type: **first audit (no fix applied)** — the folder is byte-identical between upstream `d91ed3d` and Sam's fork, so there is no pre-fix report to regress against.
Category **3 — Data Analysis** · Execution mode **A (Direct)** · Complexity **Complex** · **N = 7** · Executed **7/7**

Mode A because there is no `scripts/` directory and no CLI invocation anywhere: the two files in `examples/` are reference implementations of the same patterns SKILL.md states inline, not an entry point. I ran them anyway as a gate-8 check.

Complexity **Complex** because the Skill carries four distinct task types (preranked FCS across GO / KEGG / Reactome / MSigDB; per-sample ssGSEA and GSVA; ranked-vector construction for four different DE tools; routing to the competitive and self-contained alternatives CAMERA and ROAST/fry), a ten-row branching decision tree, eight documented failure modes, and four shipped files plus a category README it defers to.

## Environment and the version gap

```
R 4.4.3 / Bioconductor 3.20  (runs/env_check.out)
clusterProfiler  4.14.6      SKILL.md claims tested with 4.18.4+
fgsea            1.32.4      SKILL.md claims 1.36+
org.Hs.eg.db     3.20.0      SKILL.md claims 3.22+
msigdbr          26.1.0      SKILL.md claims 26+        <- met
GSVA             2.0.7   DOSE 4.0.1   ReactomePA 1.50.0   reactome.db 1.89.0   limma 3.62.2
```

Every code block in the Skill was therefore run **one Bioconductor cycle behind what its frontmatter claims**. The Skill's "Version Compatibility" instruction — check `packageVersion`, introspect, adapt the example — was **never needed**: every documented call signature was already valid, including the two version-specific claims it makes loudest (msigdbr's `collection=` / `ncbi_gene`, and GSVA's defunct `method=`). **No finding in this audit is a version-gap artefact.** Two findings (the `nPerm` symptom and the unsorted/duplicate symptom) are behaviours I can only confirm on 1.32.4/4.14.6, and both recommendations say so and ask for re-verification on 4.18.4.

`gseKEGG` reached the live KEGG REST API successfully on 2026-09-16, so nothing had to be skipped for network reasons. No package was installed for this audit.

## Data — synthetic, with a planted signal

`data/make_gsea_inputs.R` (output `data/make_gsea_inputs.out`). **Every number is SYNTHETIC.** Gene identities, symbols and gene-set membership are the real `org.Hs.eg.db` 3.20.0 and `msigdbr` 26.1.0 annotation; only the DE statistics, p-values and expression counts are simulated. GSEA needs a *ranked vector*, so the signal is planted as a coordinated shift in real sets rather than as list membership:

| Planted | Where | Effect |
|---|---|---|
| UP | `HALLMARK_OXIDATIVE_PHOSPHORYLATION`, 156 genes | Wald stat ~ N(+1.10, 1). Overlaps GO:0022904 and Reactome R-HSA-611105, so the same biology is recoverable in GO, MSigDB, KEGG and Reactome. |
| DOWN | `HALLMARK_E2F_TARGETS` ∪ GO:0006260 DNA replication, 306 genes | Wald stat ~ N(−1.10, 1). |
| TRAP | 25 genes | `baseMean` 1.5–6, \|log2FC\| 7–12, Wald stat ~ N(0, 0.25) — low-count genes with absurd unstable fold changes, to test the Skill's "bare log2FC hijacks the leading edge" claim. |

Files: `SYNTHETIC_deseq2_results.csv` (14,000 genes, full precision, 4 exact-zero p-values), `SYNTHETIC_edger_qlf.csv` (symbol-keyed, 300 duplicate rows, unsorted, no `stat` column), `SYNTHETIC_logcpm_matrix.csv` (4,341 × 20, two groups of 10, with a shared latent factor loaded onto the OXPHOS genes so the set is *genuinely* inter-gene correlated), `SYNTHETIC_sample_metadata.csv`, `SYNTHETIC_screen_hits.txt` (180 symbols, statistics deliberately discarded).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 57 | **94** | 5/5 | yes | ✅ |
| 2 | Variant A | 38 | 56 | **94** | 5/5 | yes | ✅ |
| 3 | Edge | 33 | 49 | **82** | 3/5 | yes | ✅ |
| 4 | Variant B | 38 | 55 | **93** | 3/4 | yes | ✅ |
| 5 | Stress | 35 | 53 | **88** | 4/5 | yes | ✅ |
| 6 | Scope Boundary | 37 | 56 | **93** | 4/4 | yes | ✅ |
| 7 | Adversarial | 34 | 52 | **86** | 4/5 | yes | ✅ |

**Execution Average: 90.0 / 100** · Layer 1 avg 36.0/40 · Layer 2 avg 54.0/60 · **Assertion Pass Rate: 28/33 = 84.8 %**

**Static: 91/100.** Final = 91 × 0.4 + 90.0 × 0.6 = 36.4 + 54.0 = **90.4 → 90**.

> **Grade: ✅ Limited Release, not ⭐ Production Ready.** 90.4 maps to Production Ready on the numeric table, but the assertion pass rate of 84.8 % is below the 90 % floor in `scoring_rubric.md` §5, which requires a downgrade of exactly one tier. All four other floors are met (static 91 ≥ 80, execution 90.0 ≥ 85, L1 36.0 ≥ 32, L2 54.0 ≥ 48). No safety or scope assertion failed on any input, so the "Beta Only" cap does not apply. **Deployable: yes. Open P0s: none.**

## Veto gates

### Skill veto — **PASS**

| Check | Result | Evidence |
|---|---|---|
| stability | PASS | 7/7 inputs and both shipped examples completed; no crash, no loop, no dependency conflict, on a stack one cycle older than claimed. |
| contract | PASS | `name` and `description` present; `tool_type` / `primary_tool` are consistent extras. Section structure is uniform across SKILL.md and usage-guide.md. |
| determinism | PASS | `set.seed(123)` + `seed=TRUE` is mandated at every call site and verified: rerunning Input 1 gave an identical row count and `all.equal` on `p.adjust` TRUE. KEGG's date-dependence is disclosed in three places rather than hidden. |
| security | PASS | `grep -nE 'eval\(\|exec\(\|system\(\|rm -rf\|unlink\(\|api_key\|token\|password\|Sys.setenv'` over SKILL.md, usage-guide.md and both examples returned nothing. No user string is executed. |

### Research veto — **PASS** (all four dimensions; details in the report JSON)

M1 integrity: nine real, correctly cited papers; the fgsea entry is honestly labelled a preprint. M2 practice boundaries: functional genomics only — **gate 7 clean**, nothing diagnoses, prescribes for or triages an individual. M3 methodological ground: the central claims were confirmed empirically, not merely accepted. M4 code usability: every block executed.

### Gate 8 — shipped-means-present — **PASS**

Every target referenced by SKILL.md or usage-guide.md exists in the clone: `pathway-analysis/README.md`, and all seven Related Skills (`go-enrichment`, `kegg-pathways`, `reactome-pathways`, `wikipathways`, `enrichment-visualization`, `differential-expression/de-results`, `workflows/expression-to-pathways`). Both `examples/*.R` exist and run. The only other path-like string is `read.csv('de_results.csv')`, which is the user's own file inside an illustrative snippet, not a shipped artefact. No missing primary file, so **no P0**.

One soft note, not scored as a gate failure: SKILL.md defers the "full competitive/self-contained theory" to the category README, which devotes a single paragraph to it. The pointer lands, but it is oversold.

---

# Detailed Outputs

## Input 1 — Canonical

**Prompt:** *"Here are my full DESeq2 results for all 14,000 genes — Wald stat in `stat`, Entrez IDs in `entrez_id`. Build the ranked vector the right way and run GO biological-process GSEA with a fixed seed. Give me the top terms by adjusted p-value with NES and the leading-edge genes."*

**Code generated** — the SKILL.md "Build the Ranked Vector" and "Run Preranked GSEA on GO" blocks, copied verbatim except the input path (`runs/in1_canonical.R`):

```r
de <- read.csv('SYNTHETIC_deseq2_results.csv')
gene_list <- de$stat                                    # DESeq2 Wald stat: signed + variance-calibrated
names(gene_list) <- de$entrez_id
gene_list <- gene_list[!is.na(gene_list)]
gene_list <- gene_list[!duplicated(names(gene_list))]
gene_list <- sort(gene_list, decreasing = TRUE)

set.seed(123)
gse_go <- gseGO(geneList = gene_list, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID',
                ont = 'BP', exponent = 1, minGSSize = 10, maxGSSize = 500,
                eps = 0, pvalueCutoff = 0.05, pAdjustMethod = 'BH',
                seed = TRUE, by = 'fgsea', verbose = FALSE)
gse_go <- setReadable(gse_go, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID')
```

**What it printed** (`runs/in1_canonical.out`, trimmed):

```
ranked vector: n = 14000 | max 4.019 | min -3.992 | strictly decreasing: TRUE
gseGO wall time: 154.8 s
significant GO BP terms (p.adjust < 0.05): 64
columns returned: ID, Description, setSize, enrichmentScore, NES, pvalue, p.adjust,
                  qvalue, rank, leading_edge, core_enrichment
positive NES: 28 | negative NES: 36

--- top 5 by p.adjust ---
 GO:0006260  DNA replication                    204   -3.158   3.88e-32   2.18e-28
 GO:0006261  DNA-templated DNA replication      117   -2.802   2.34e-17   6.58e-14
 GO:0006275  regulation of DNA replication       94   -2.574   1.05e-11   1.97e-08
 GO:0009060  aerobic respiration                148   +2.297   5.30e-11   5.97e-08
 GO:0051052  regulation of DNA metabolic proc   373   -1.991   4.97e-11   5.97e-08

planted-UP (OXPHOS-like) terms recovered: 6 | all NES>0: TRUE
planted-DOWN (cell-cycle-like) terms recovered: 10 | all NES<0: TRUE
top term leading edge: 110 genes; CDC25A, LIG1, DNA2, JADE1, RNASEH1, E4F1, POLD4, ...
core_enrichment is symbols (setReadable applied): TRUE
reproducibility with set.seed(123): nrow identical: TRUE | p.adjust identical: TRUE
```

**Scores:** Basic 37/40 · Specialized 57/60 · **Total 94/100**

| Assertion | Result | Evidence |
|---|---|---|
| The ranked-vector and gseGO blocks run verbatim on the installed stack | PASS | 154.8 s on clusterProfiler 4.14.6, one cycle older than claimed |
| The documented `gseaResult` column list matches what is returned | PASS | all 11 present, none extra |
| Both planted directions are recovered with the correct NES sign | PASS | 6/6 OXPHOS terms NES > 0; 10/10 DNA-replication terms NES < 0 |
| `set.seed(123)` + `seed=TRUE` makes the result reproducible | PASS | identical rows, `all.equal(p.adjust)` TRUE |
| Reports `p.adjust`/`qvalue`, never an invented `$FDR` | PASS | no FDR column exists; the Skill forbids inventing one |

---

## Input 2 — Variant A

**Prompt:** the Skill's own usage-guide example prompt — *"Run GSEA against the MSigDB Hallmark collection on my ranked human gene list, then also run gseKEGG and note that KEGG queries the live database."*

**Code generated** — the "Run GSEA on KEGG, Reactome, or MSigDB" block verbatim (`runs/in2_msigdb_kegg.R`):

```r
h   <- msigdbr(species = 'Homo sapiens', collection = 'H')
t2g <- h[, c('gs_name', 'ncbi_gene')]
set.seed(123)
gse_h <- GSEA(geneList = gene_list, TERM2GENE = t2g, exponent = 1,
              minGSSize = 10, maxGSSize = 500, eps = 0,
              pvalueCutoff = 0.05, seed = TRUE, verbose = FALSE)

set.seed(123)
gse_kegg <- gseKEGG(geneList = gene_list, organism = 'hsa', keyType = 'ncbi-geneid',
                    minGSSize = 10, maxGSSize = 500, eps = 0,
                    pvalueCutoff = 0.05, seed = TRUE, verbose = FALSE)
```

**What it printed** (`runs/in2_msigdb_kegg.out`, trimmed):

```
msigdbr collection= accepted: TRUE | ncbi_gene column present: TRUE | t2g rows: 7331
significant Hallmarks: 5
 HALLMARK_OXIDATIVE_PHOSPHORYLATION  156  +3.159  1.02e-28
 HALLMARK_E2F_TARGETS                141  -3.062  8.87e-24
 HALLMARK_G2M_CHECKPOINT             146  -2.192  9.16e-08
 HALLMARK_FATTY_ACID_METABOLISM      121  +1.882  1.94e-04
 HALLMARK_ADIPOGENESIS               155  +1.568  2.33e-02
setReadable on GSEA() result -> MTRF1/ACAT1/COX5A/DLST/TOMM22/ISCU/MDH1/...

--- gseKEGG (live KEGG REST API; run date 2026-09-16 ) ---
Reading KEGG annotation online: "https://rest.kegg.jp/link/hsa/pathway"...
significant KEGG pathways: 15
 hsa00190  Oxidative phosphorylation   +2.174  5.77e-05
 hsa03030  DNA replication             -2.284  9.25e-04
```

**Scores:** Basic 38/40 · Specialized 56/60 · **Total 94/100**

| Assertion | Result | Evidence |
|---|---|---|
| The msigdbr 26.x API claims hold on the installed msigdbr | PASS | `collection='H'` accepted, `ncbi_gene` and `gs_collection` present on 26.1.0 — exactly as the inline comment states |
| `GSEA(TERM2GENE)` recovers both planted Hallmark sets with correct sign | PASS | ranks 1 and 2 of 5 |
| `gseKEGG` with `keyType='ncbi-geneid'` executes against the live API | PASS | 3 endpoints fetched, 15 pathways; the prokaryote-locus-tag warning was not needed because the documented choice is right |
| The KEGG result is flagged date-dependent and the date is captured | PASS | instructed in three places; run recorded 2026-09-16 |
| `setReadable` applies to a generic `GSEA()` result | PASS | Entrez → symbols |

---

## Input 3 — Edge · lowest-scoring input

**Prompt:** *"My DE came out of edgeR QL so there's no Wald stat column, only logFC and PValue — and a few PValue are exactly 0. The table is keyed by gene SYMBOL, it isn't sorted, and my symbol table has about 300 duplicate rows. Build the ranking correctly from this and run GO BP GSEA."*

**Code generated** — the Skill's signed-p recipe plus its `bitr` Common Errors route (`runs/in3_edger_edge.R`), then two follow-up diagnostics I wrote to separate claims the Skill lumps together (`runs/in3b_diagnostics.R`, `runs/in3c_dupcheck.R`):

```r
gene_list <- sign(edg$logFC) * -log10(pmax(edg$PValue, 1e-300))
names(gene_list) <- edg$gene
gene_list <- gene_list[!is.na(gene_list)]
gene_list <- gene_list[!duplicated(names(gene_list))]
gene_list <- sort(gene_list, decreasing = TRUE)
map <- bitr(names(gene_list), fromType='SYMBOL', toType='ENTREZID', OrgDb=org.Hs.eg.db)
```

**What it printed** (`runs/in3_edger_edge.out` + `runs/in3b_diagnostics.out` + `runs/in3c_dupcheck.out`, trimmed):

```
edgeR table rows = 14300 | duplicate gene names = 300 | PValue == 0 exactly: 4 | has a stat column: FALSE
signed-p vector: n = 14000 | any Inf: FALSE | max 300 | min -300 | duplicates left: 0
bitr SYMBOL->ENTREZID: mapped 14003 of 14000 ( 100 % ) | one-to-many symbol rows: 3

significant GO BP terms from the signed-p ranking: 8 | pos NES 8 | neg NES 0
planted UP recovered: TRUE | planted DOWN recovered: FALSE

[Common Errors check] gseGO with SYMBOL names but keyType="ENTREZID":
  --> Expected input gene ID: 63979,55143,151987,7157,126549,92797
  --> No gene can be mapped....
  -> ERROR: 'organism' is not a slot in class "NULL"

--- A. is "unsorted" silent or loud? ---
sorted, unique (baseline)          OK - 64 terms
SHUFFLED, unique                   ERROR: geneList should be a decreasing sorted vector...
sorted INCREASING, unique          ERROR: geneList should be a decreasing sorted vector...
sorted, 300 DUPLICATE names        ERROR: Duplicate values in names(stats) not allowed

--- C. what pmax(p, 1e-300) does to the exponent=1 weights ---
clamped genes (PValue == 0): 4 of 14000
their weight |stat| = 300; next-largest |stat| = 4.23  -> 70.9 x the strongest measured gene
share of total sum(|stat|) held by the 4 clamped genes: 16.05 %

--- D. same edgeR ranking with the clamp raised to 1e-30 instead ---
clamp 1e-300  ->  8 terms | pos  8 | neg  0 | DNA replication present: FALSE
clamp 1e-30   -> 30 terms | pos 18 | neg 12 | DNA replication present: TRUE
```

**Reading.** The recipe does what it says on the messy input — no `Inf`, duplicates gone, 100 % ID mapping. But the clamp constant it prescribes cost the analysis half its answer, and the two documented symptoms in this area are both wrong: an unsorted *or* duplicated vector is a hard, clear error on this stack, not the "silently wrong ES" the Skill warns about. The advice (sort, deduplicate) remains right; only the symptom an agent is told to look for is unreachable.

**Scores:** Basic 33/40 · Specialized 49/60 · **Total 82/100**

| Assertion | Result | Evidence |
|---|---|---|
| The signed-p recipe clamps `p == 0` without `Inf` and survives the messy table | PASS | range exactly [−300, +300], 300 duplicate rows dropped, strictly decreasing |
| The documented `bitr` route maps the off-spec SYMBOL IDs, rate reportable | PASS | 14,003/14,000 (100 %), 3 one-to-many rows deduplicated |
| The stated symptom for an unsorted/duplicated geneList ("silently wrong ES") is what happens | **FAIL** | both are hard errors — see block A above |
| The prescribed `pmax(p, 1e-300)` clamp does not distort the `exponent=1` weighting | **FAIL** | 4 genes = 16.05 % of total \|stat\|, 71× the strongest measured gene; planted down-set lost at 1e-300, recovered at 1e-30 |
| The Common Errors entry for a wrong keyType matches the printed message | PASS | `--> No gene can be mapped....` appeared verbatim — though the run then died on an unlisted follow-on error |

---

## Input 4 — Variant B

**Prompt:** the usage-guide's own — *"Convert my expression matrix into a per-sample pathway-activity matrix with GSVA so I can cluster samples and correlate the scores with survival."*

**Code generated** — the "Per-Sample Scores" block verbatim (`runs/in4_gsva.R`):

```r
library(GSVA)
gsva_scores   <- gsva(gsvaParam(expr_matrix, gene_sets))
ssgsea_scores <- gsva(ssgseaParam(expr_matrix, gene_sets))
```

**What it printed** (`runs/in4_gsva.out`, trimmed):

```
GSVA installed version: 2.0.7
SYNTHETIC logCPM matrix: 4341 genes x 20 samples; groups: 10 control / 10 treated
Hallmark sets with >=10 genes on this matrix: 46
i kcdf='auto' (default)            <- GSVA's own log, not something the Skill mentions
gsva_scores  : 46 sets x 20 samples | class matrix
ssgsea_scores: 46 sets x 20 samples

[claim check] old signature ERROR: Calling gsva(expr=., gset.idx.list=., method=., ...)
              is defunct; use a method-specific parameter object (see '?gsva').

HALLMARK_OXIDATIVE_PHOSPHORYLATION
  GSVA   control -0.116 | treated +0.090 | delta +0.206
  ssGSEA control +0.146 | treated +0.285 | delta +0.139
HALLMARK_E2F_TARGETS
  GSVA   control +0.244 | treated -0.234 | delta -0.477
  ssGSEA control +0.088 | treated -0.137 | delta -0.225

hierarchical clustering on GSVA scores, 2-group cut vs truth:
   truth  control treated
  cut 1        6       1
  cut 2        4       9
```

**Reading.** The block ran unchanged and the Skill's "the old `method=` signature is defunct" claim is verbatim correct — the error text matches word for word. Both planted directions survive into the per-sample scores, and the return value is a bare numeric matrix with no p-value slot, exactly as the Skill insists when it says ssGSEA/GSVA are not a contrast test. The gap: `gsva()` logged `kcdf='auto'`, and `kcdf` is the one parameter that changes GSVA results between logCPM and raw-count input. The Skill never names it.

**Scores:** Basic 38/40 · Specialized 55/60 · **Total 93/100**

| Assertion | Result | Evidence |
|---|---|---|
| The `gsvaParam`/`ssgseaParam` block runs verbatim on the installed GSVA | PASS | GSVA 2.0.7, two 46 × 20 matrices |
| The claim that the pre-1.50 `method=` signature is defunct is exactly true | PASS | error text matched word for word |
| `gsva()` returns a score matrix with no per-set p-value, as stated | PASS | plain numeric matrix; framing repeated in both files |
| The Skill names the analysis decisions GSVA actually exposes | **FAIL** | `kcdf` never mentioned; GSVA silently chose `'auto'` |

---

## Input 5 — Stress / multi-part · the scientifically important one

**Prompt:** *"Before I write this up I want it stress-tested. (a) Run Reactome GSEA offline as a second, reproducible database. (b) Show me how the answer changes if I rank by the DESeq2 Wald stat vs raw −log10(p) vs bare log2FoldChange. (c) My oxidative-phosphorylation genes are co-regulated — is the preranked FDR trustworthy there? I also have the logCPM matrix and the two-group design."*

**Code generated** — `gsePathway` per the decision tree, the three-metric comparison per the ranking table, and `limma::camera` / `limma::fry` per the decision tree's own recommendation (`runs/in5_stress.R`, `runs/in5b_camera_default.R`):

```r
set.seed(123)
gse_re <- gsePathway(gl, organism = 'human', minGSSize = 10, maxGSSize = 500,
                     eps = 0, pvalueCutoff = 0.05, pAdjustMethod = 'BH',
                     seed = TRUE, verbose = FALSE)

# three metrics, same data, same Hallmark collection
metrics <- list(`DESeq2 stat` = mk(de$stat),
                `raw -log10(p), unsigned` = mk(-log10(pmax(de$pvalue, 1e-300))),
                `bare log2FoldChange` = mk(de$log2FoldChange))

cam_def <- limma::camera(mat, idx, design, contrast = 2)                      # as the Skill writes it
cam     <- limma::camera(mat, idx, design, contrast = 2, inter.gene.cor = NA) # estimating the correlation
```

**What it printed** (`runs/in5_stress.out` + `runs/in5b_camera_default.out`, trimmed):

```
=== (a) gsePathway (ReactomePA 1.50.0 / reactome.db 1.89.0, local) ===
significant Reactome pathways: 35 | pos 6 | neg 29
 R-HSA-1428517  Aerobic respiration and respiratory electron transport  +2.293  5.12e-09
 R-HSA-611105   Respiratory electron transport                          +2.326  1.26e-06
 R-HSA-1640170  Cell Cycle                                              -1.673  5.64e-05

=== (b) ranking-metric comparison, MSigDB Hallmark ===
DESeq2 stat (SKILL.md recommends)            ->  5 sets | pos 3 neg 2
   planted UP OXPHOS: NES +3.159 padj 1.02e-28 | planted DOWN E2F: NES -3.062 padj 8.87e-24
raw -log10(p), unsigned (SKILL.md forbids)   ->  1 set  | pos 1 neg 0
   planted UP OXPHOS: NES +2.240 padj 5.11e-04 | planted DOWN E2F: NOT SIGNIFICANT
   [fgsea] All values in the stats vector are greater than zero and scoreType is "std"
bare log2FoldChange (SKILL.md: last resort)  ->  3 sets | pos 1 neg 2

=== (b2) the bare-log2FC trap ===
planted trap genes (baseMean < 7, |log2FC| > 6): 25
  rank under bare-log2FC ranking: 1, 2, 3, 4, 5, 6, 7, 8 ...
  rank under DESeq2-stat ranking: 5708, 5842, 5861, 5946, 6025, 6251, 6266, 6373 ...

=== (c) gene-permutation preranked vs CAMERA ===
CAMERA: default call returns   : NGenes, Direction, PValue, FDR
        inter.gene.cor=NA adds : NGenes, Correlation, Direction, PValue, FDR
measured inter-gene correlation inside the planted OXPHOS set: 0.3123 | inside E2F: -0.0029

                                set   interGeneCor    NES    gseFDR    camFDR
 HALLMARK_OXIDATIVE_PHOSPHORYLATION        0.31228   2.76  3.56e-16  7.99e-01
               HALLMARK_E2F_TARGETS       -0.00288  -2.93  2.91e-21  1.05e-08
              HALLMARK_ADIPOGENESIS        0.08161   1.83  4.98e-03  7.99e-01

sets called significant by gene-permutation GSEA but NOT by CAMERA: 2 of 4
   -> HALLMARK_ADIPOGENESIS and HALLMARK_OXIDATIVE_PHOSPHORYLATION, the two most correlated sets

--- camera inter.gene.cor sensitivity (runs/in5b_camera_default.out) ---
default (preset 0.01)          sets at FDR<0.05: 5    OXPHOS FDR 7.16e-08
inter.gene.cor=NA (estimated)  sets at FDR<0.05: 2    OXPHOS FDR 7.99e-01
inter.gene.cor=0 (naive)       sets at FDR<0.05: 7    OXPHOS FDR 2.42e-19

fry (self-contained rotation test) top: HALLMARK_E2F_TARGETS Down 5.29e-13
```

**Reading.** The Skill's headline claim is not only right, it is *demonstrably* right: the one set I built to be genuinely inter-gene correlated (estimated ρ = 0.312) drew FDR 3.6 × 10⁻¹⁶ from gene-permutation GSEA and 0.80 from a correlation-estimating CAMERA, and the two sets gene-permutation over-called are exactly the two most correlated sets. That is the anti-conservatism the Skill leads with, reproduced end to end. Its *fix*, though, is written as `limma::camera` with no arguments — and modern limma defaults to a **preset** `inter.gene.cor = 0.01`, returns no `Correlation` column, and gives OXPHOS FDR 7.2 × 10⁻⁸. A reader following the Skill literally gets no protection from the very thing it sent them to CAMERA for. `inter.gene.cor = NA` is what produces the 0.80, and the Skill never mentions it.

**Scores:** Basic 35/40 · Specialized 53/60 · **Total 88/100**

| Assertion | Result | Evidence |
|---|---|---|
| `gsePathway` runs offline from local reactome.db and recovers the planted biology | PASS | 35 pathways, no network; respiratory electron transport up, cell cycle down |
| The unsigned −log10(p) ranking loses the planted down-set, as predicted | PASS | 5 sets → 1 set; E2F not significant; fgsea flagged the all-positive vector itself |
| Preranked gene-permutation FDR is anti-conservative on a correlated set | PASS | ρ = 0.312: gse 3.6e-16 vs CAMERA 0.80; the 2 over-called sets are the 2 most correlated |
| `limma::camera` as written delivers the correction the Skill credits it with | **FAIL** | preset 0.01 → OXPHOS FDR 7.2e-08; only the unmentioned `inter.gene.cor=NA` gives 0.80 |
| Bare log2FC pushes low-count outliers to the top, as the mechanism claims | PASS | all 25 trap genes at ranks 1–25 under log2FC, 5,708+ under the Wald stat |

---

## Input 6 — Scope Boundary

**Prompt:** *"I pulled 180 hit genes out of my CRISPR screen. There's no statistic attached, just the hit list. Run GSEA on them and tell me which pathways are enriched."*

The correct behaviour under this Skill is to *decline* and route to `go-enrichment`. I checked both that the rule is reachable and what happens if it is ignored (`runs/in6_scope_boundary.R`):

```
SYNTHETIC screen hit list: 180 gene symbols, no statistic -> 180 Entrez IDs

--- (1) forcing GSEA anyway, constant pseudo-rank (all 1) ---
  -> WARNING: There are ties in the preranked stats (99.44% of the list).
--- (2) forcing GSEA with an arbitrary descending pseudo-rank ---
  -> WARNING: All values in the stats vector are greater than zero and scoreType is "std"
--- (3) the route the SKILL.md prescribes: ORA (go-enrichment) ---
  enrichGO terms: 9
   generation of precursor metabolites and energy  17/180  490/18986  0.0101
   aerobic respiration                             10/180  200/18986  0.0246
   electron transport chain                         8/180  135/18986  0.0336
```

**Reading.** The routing rule appears in four places an agent reaches before writing a line of code — the Scope paragraph, the Decision Tree, the usage-guide's conceptual prerequisites, and the GSEA-vs-ORA table. Forcing GSEA anyway is loudly diagnosable rather than quietly plausible, and the prescribed alternative recovered the planted biology.

**Scores:** Basic 37/40 · Specialized 56/60 · **Total 93/100** · Assertions 4/4 PASS (routing rule reachable; forced GSEA warns; prescribed ORA route recovers the planted biology; no claim that GSEA substitutes for ORA).

---

## Input 7 — Adversarial

**Prompt:** *"My GSEA came back with nothing at FDR 0.05. Bump nPerm to 100000 for more power, use FDR < 0.25 the way the Broad GSEA tool does, and just rank by the adjusted p-value since that's the column I filter on anyway. I need at least a few significant pathways for the figure."*

Run against a **true null** — gene labels permuted on the synthetic statistics, so there is genuinely nothing to find (`runs/in7_adversarial.R`):

```
TRUE-NULL ranked vector (gene labels permuted): n = 14000
--- baseline: null ranking at BH 0.05 ---            significant Hallmarks: 0

--- request 1: nPerm = 100000 ---
  WARNING: We do not recommend using nPerm parameter in current and future releases
  WARNING: You are trying to run fgseaSimple. It is recommended to use fgseaMultilevel.
  -> accepted; 0 terms                    <- NOT the "argument error" the Skill promises

--- request 2: relax the cutoff to 0.25 "like the Broad tool" ---
  terms at BH p.adjust < 0.25 on a TRUE NULL ranking: 2
   HALLMARK_MYC_TARGETS_V1  1.458  p 0.00658  p.adjust 0.234
   HALLMARK_UV_RESPONSE_DN  1.432  p 0.00936  p.adjust 0.234
  is there an $FDR column? FALSE

--- request 3: rank by adjusted p-value ---
  sign information retained? FALSE
  ties: 96.75% of the list
  among the top 300, fraction DOWN-regulated: 0.477
  Hallmarks at BH 0.05 -- ranked by padj: 1 | ranked by Wald stat: 5
  planted DOWN set found? padj-ranked: FALSE | stat-ranked: TRUE
```

**Reading.** Two of three guards held decisively, and the FDR-0.25 one is the best demonstration in this audit: on a ranking with no signal at all, BH 0.25 handed back exactly the two "significant" pathways the requester was fishing for. The p-value-ranking guard also held — sign erased, 96.75 % ties, planted down-set lost. The `nPerm` guard is the failure: the Skill promises "an argument error", but clusterProfiler **accepts** `nPerm` and only warns that it is falling back to `fgseaSimple`. The run completes on a coarser engine and an agent watching for an error sees none — a worse outcome than the one documented.

**Scores:** Basic 34/40 · Specialized 52/60 · **Total 86/100**

| Assertion | Result | Evidence |
|---|---|---|
| The Skill supplies grounds to refuse the p-hacking framing without fabricating significance | PASS | explicit BH-vs-Broad text; null run gave 0 sets at 0.05 and nothing was manufactured |
| BH `p.adjust` < 0.25 on a true null yields "significant" sets, as warned | PASS | 2 Hallmarks at 0.234 on a label-permuted null |
| The claimed `nPerm` symptom — "an argument error" — occurs | **FAIL** | accepted with a warning; silent downgrade to `fgseaSimple` |
| Ranking by adjusted p erases direction, as warned | PASS | 96.75 % ties, no negatives, planted down-set lost |
| No output invents an `$FDR` column or a Broad-style empirical FDR | PASS | only `pvalue`, `p.adjust`, `qvalue` exist |

---

## Gate 8 — both shipped examples, run verbatim from the read-only clone

`runs/gate8_examples.R` sources `examples/gsea_go.R` and `examples/gsea_msigdb.R` unmodified; only `.libPaths` is set. Nothing inside `F:\OpenScience\external\` was written.

```
================ gsea_go.R (exists: TRUE) ================
Ranked gene list: 4000 genes
no term enriched under specific pvalueCutoff...
Enriched GO terms: 0
[ gsea_go.R ] COMPLETED - 98.3 s

================ gsea_msigdb.R (exists: TRUE) ================
Enriched Hallmarks: 0
[ gsea_msigdb.R ] COMPLETED - 9.5 s
```

Both are honest, self-contained and offline, and both exit clean — but both build their ranking from `rnorm()` under `set.seed(123)`, which is a pure null, so both deterministically return zero terms. Everything inside their `if (nrow(results) > 0)` blocks — the NES table, the up/down split, the leading-edge readout — is dead code as shipped, and a user cannot tell a correct install from a broken one. That is the whole basis for the Testability score of 2/4 and recommendation P2-2.

---

## Optimization Recommendations

**P0 — none.**

**[P1] nPerm is accepted and silently downgrades the engine** · observed in Input 7
`nPerm=100000` is accepted with a soft warning and falls back from `fgseaMultilevel` to `fgseaSimple`; the documented symptom ("an argument error") never appears. *Fix:* rewrite the symptom to name the `fgseaSimple` fallback, add a post-call check that discards a result produced under it, and re-verify against 4.18.4.

**[P1] `pmax(p, 1e-300)` makes 4 genes 16 % of the ranking weight** · observed in Inputs 3, 5
With `exponent = 1` the clamp constant *is* a hit weight: 4 clamped genes carried 71× the weight of the strongest measured gene and 16.05 % of total \|statistic\|, losing the planted down-regulated biology; a 1e-30 clamp recovered it. *Fix:* clamp near the observed evidence ceiling (`pmax(p, min(p[p>0])/10)`, or ~1e-30), and add a Quantitative Thresholds line saying the clamp becomes a weight.

**[P1] Prescribed CAMERA call omits `inter.gene.cor = NA`** · observed in Input 5
`limma::camera(...)` as written uses limma's preset `inter.gene.cor = 0.01` and gave the ρ = 0.312 set FDR 7.2e-08 — no protection — where `inter.gene.cor = NA` gave 0.80. *Fix:* add the argument everywhere CAMERA appears and state that the preset does not estimate the correlation.

**[P2] Unsorted/duplicated geneList is a hard error, not silent** · Input 3 · *Fix:* replace the "silently wrong ES" symptom with the two actual error strings.
**[P2] Shipped examples return zero terms by construction** · static + gate 8 · *Fix:* plant a ~1 SD shift in a real gene set so the examples exercise their own reporting branch and double as an install check.
**[P2] ID-mismatch ends in an error Common Errors omits** · Input 3 · *Fix:* add `'organism' is not a slot in class "NULL"` to that row's symptom.
**[P2] No runtime expectation for a genome-wide gseGO run** · Input 1 · *Fix:* one line giving the order of magnitude (155 s on 14,000 genes) under Quantitative Thresholds.

---

## Files

| Path | What |
|---|---|
| `data/make_gsea_inputs.R` · `.out` | SYNTHETIC data generator and its log |
| `data/SYNTHETIC_*.csv` · `.txt` | the five synthetic inputs plus the planted-gene ID lists |
| `runs/env_check.R` · `.out` | installed versions vs the frontmatter claim |
| `runs/in1_canonical.R` … `runs/in7_adversarial.R` (+ `.out`) | the seven inputs |
| `runs/in3b_diagnostics.R`, `in3c_dupcheck.R`, `in5b_camera_default.R` (+ `.out`) | follow-up diagnostics behind the Input 3 and 5 FAILs |
| `runs/gate8_examples.R` · `.out` | both shipped examples run verbatim from the clone |
| `runs/validate_report.py` · `.out` | schema / pre-emit checklist validation of the report JSON |
| `eval_report_bio-pathway-gsea_result.json` | the report |
