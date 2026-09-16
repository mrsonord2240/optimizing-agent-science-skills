> **Audit record for `bio-pathway-go-enrichment`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/pathway-analysis/go-enrichment) (MIT).
> - Read from [mrsonord2240/bioSkills@575ab94](https://github.com/mrsonord2240/bioSkills/tree/575ab946989a7029d235eb0ab711e47b08edbcb0/pathway-analysis/go-enrichment), a fork in which this Skill's files are unchanged from upstream; the audited content is upstream's.
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pathway-go-enrichment

Generated: 2026-09-15 · rendered from `report.json` by `tools/render_viewer.py`.

> This viewer is **generated from the audit report**, not written by the auditor. It restates the report's own recorded scores, notes and assertions and adds nothing to them. Where a hand-written viewer would argue from the runs, this one points at the scripts in [scripts/](scripts/) instead.

Source: `mrsonord2240/bioSkills@575ab946989a7029d235eb0ab711e47b08edbcb0:pathway-analysis/go-enrichment`
Audit type: first audit (no fix applied; files identical to GPTomics/bioSkills@d91ed3d)
Category: Data Analysis · Execution mode: A · Complexity: Moderate · N = 5 · Executed: 5/5

## What the Skill claims to do

Runs Gene Ontology over-representation analysis (ORA) on a gene LIST with clusterProfiler enrichGO, the one-sided hypergeometric/Fisher 2x2 test phyper(k-1, M, N-M, n, lower.tail=FALSE). Covers why the BACKGROUND universe (not the gene list) is the null and decides significance, why omitting universe= is a bug, why enrichGO defaults to ont='MF' not 'BP', why pvalueCutoff filters p.adjust not raw p, why ORA discards effect magnitude and inherits GO-DAG true-path redundancy (simplify, topGO), why RNA-seq gene-length bias inflates long-gene terms (GOseq Wallenius), plus GeneRatio/BgRatio, bitr ID mapping, minGSSize/maxGSSize, groupGO.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 55 | **93** | 5/5 | yes | ✅ |
| 2 | Variant A | 36 | 53 | **89** | 3/4 | yes | ✅ |
| 3 | Edge | 36 | 53 | **89** | 4/4 | yes | ✅ |
| 4 | Variant B | 35 | 52 | **87** | 3/4 | yes | ✅ |
| 5 | Stress | 37 | 55 | **92** | 5/5 | yes | ✅ |

**Execution Average: 90.0 / 100** · **Assertion Pass Rate: 20/22**

**Static: 89/100** · Static weighted 35.6 + dynamic weighted 54.0 = **90/100** → ⭐ Production Ready, deployable.

---

## Veto gates

### Skill veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| stability | PASS |  |
| contract | PASS |  |
| determinism | PASS |  |
| security | PASS |  |

### Research veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| scientific integrity | PASS | All numbers come from executed runs; gene identities and GO annotations are real (org.Hs.eg.db 3.20.0, GO.db 3.20.0) while hit/universe membership is synthetic; the nine references are real papers. |
| practice boundaries | PASS | Functional annotation only; no individual-level or clinical content. |
| methodological ground | PASS | The hypergeometric framing, universe-as-null, effect-size-alongside-p and DAG-redundancy guidance all held in execution; the circularity warning (terms cannot validate the DE list) is stated. |
| code usability | PASS | All five R blocks used ran verbatim on clusterProfiler 4.14.6 / org.Hs.eg.db 3.20.0; the basic example exits 0. The GOseq block could not be executed because geneLenDataBase would not install on this machine (recorded, not scored as a defect). |

## Static score

| Category | Score | Note |
|---|---|---|
| functional suitability | 11/12 | Completeness 4: ORA, universe construction, simplify, GOseq, ont='ALL'/groupGO, enricher, other organisms. Correctness 3: every tested claim held, but the documented enrichResult column list is stale - clusterProfiler 4.14.6 also returns RichFactor, FoldEnrichment and zScore, so the fold enrichment the Skill tells the agent to compute is already in the table. Appropriateness 4. |
| reliability | 10/12 | Explicit recovery guidance (inspect with cutoffs at 1, report conversion rate, flag >15% ID loss); no code-level guards, which is acceptable for a Mode A analysis skill. |
| performance context | 7/8 | 230 dense lines in one file; enrichGO on a 3500-gene universe took 146 s, simplify 30 s, ont='ALL' 53 s. |
| agent usability | 16/16 | Unambiguous: set ont explicitly, pass universe, deduplicate after bitr, read fold enrichment with p.adjust, simplify per ontology; each instruction was directly executable. |
| human usability | 7/8 | Natural trigger ('which biological processes are enriched in my gene list?'); strict ENTREZ requirement handled by bitr guidance. |
| security | 11/12 | Local OrgDb only, no credentials or network; no input validation code. |
| maintainability | 9/12 | Two examples; the basic one is self-contained and runs, the ont='ALL' one needs an external de_results.csv that is not shipped. |
| agent specific | 18/20 | Precise trigger with routing to gsea/kegg/reactome/wikipathways/enrichment-visualization; reproducible given pinned annotation packages; small-list caveat is the main escape hatch. |

## Input 1 — Canonical: GO BP ORA on a proteomics hit list with the quantified proteome as universe

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 55/60 · **Total 93/100**
- Execution: runs/in1_canonical.R sourcing block b01 verbatim; SYNTHETIC hit/universe membership over REAL org.Hs.eg.db annotations (data/make_go_inputs.R); output runs/in1_canonical.out, terms in runs/in1_terms.csv.
- Finding: enrichGO block ran verbatim: 15 terms, the planted GO:0002181 cytoplasmic translation first (fold enrichment 11.66, p.adjust 3.4e-32, 40/146 genes), background N = 3363 annotated genes of the 3500-protein universe, Descriptions readable.

| Assertion | Result | Evidence |
|---|---|---|
| The enrichGO block runs as written on the installed clusterProfiler | PASS | 4.14.6, 146 s |
| The matched universe is used and N is reported | PASS | BgRatio denominator 3363 |
| The planted biology is recovered as the top term | PASS | GO:0002181 rank 1, fold enrichment 11.66 |
| ont is set explicitly rather than relying on the MF default | PASS | ont='BP' in the block |
| Fold enrichment is reported alongside p.adjust | PASS | (k/n)/(M/N) computed; matches the FoldEnrichment column |

## Input 2 — Variant A: Effect of omitting universe= on a null hit list

- Status: ✅ COMPLETED · Basic 36/40 · Specialized 53/60 · **Total 89/100**
- Execution: runs/in2_universe.R: block b01 verbatim, then the same call with the universe line removed; output runs/in2_universe.out.
- Finding: With the matched universe a 150-protein null list gave 0 significant terms; with universe omitted it gave 1 (cellular response to heat, p.adjust 0.033) and the background grew from 3363 to 18986. On the signal list, omission changed the table from 15 to 25 terms (13 shared) and moved the planted term from 3.4e-32 to 3.0e-46.

| Assertion | Result | Evidence |
|---|---|---|
| Omitting universe= changes the null (background N) | PASS | 3363 -> 18986 |
| Omitting universe= produces significant terms from a list with no biology | PASS | 1 term vs 0 with the matched universe |
| The Skill's stated symptom (a confident table dominated by tissue-restricted terms) is reproduced | FAIL | Only one extra term on the null list; the effect was real but far smaller than described |
| Scope: no claim that the enriched terms validate the hit list | PASS | Circularity caveat carried into the answer |

## Input 3 — Edge: UniProt accessions and a 15-protein hit list

- Status: ✅ COMPLETED · Basic 36/40 · Specialized 53/60 · **Total 89/100**
- Execution: runs/in3_uniprot_small.R (bitr UNIPROT->ENTREZID, then block b01 verbatim); output runs/in3_uniprot_small.out.
- Finding: bitr mapped all 15 foreground accessions (0% loss) and 3348 universe rows to 3331 unique ENTREZ (115 one-to-many rows deduplicated); the small list still returned 2 significant terms with the planted term first, and inspecting with cutoffs at 1 gave 466 terms with min raw p 4.9e-07 vs min p.adjust 2.3e-04 - confirming pvalueCutoff filters the adjusted p.

| Assertion | Result | Evidence |
|---|---|---|
| The documented bitr route maps proteomics accessions and the conversion rate is reported | PASS | 15/15 foreground, 0% loss |
| One-to-many maps are deduplicated before counting | PASS | 115 duplicate rows removed |
| A 15-gene list still yields the planted term | PASS | GO:0002181 p.adjust 2.3e-04 |
| pvalueCutoff filters the adjusted p, as the Skill states | PASS | 2 terms at defaults vs 466 with cutoffs at 1 |

## Input 4 — Variant B: GO-DAG redundancy: simplify per ontology, ont='ALL', groupGO

- Status: ✅ COMPLETED · Basic 35/40 · Specialized 52/60 · **Total 87/100**
- Execution: runs/in4_simplify_all.R sourcing blocks b03 and b05 verbatim, then simplify() on the ALL object; output runs/in4_simplify_all.out.
- Finding: simplify collapsed BP from 15 to 7 terms and the translation lineage from 7 to 2; ont='ALL' returned 36 terms with an ONTOLOGY column (BP 15 / CC 13 / MF 8); groupGO returned 476 classification rows with no p-values. simplify() on the ont='ALL' object did not error - it silently returned only the 15 BP terms, dropping CC and MF.

| Assertion | Result | Evidence |
|---|---|---|
| simplify collapses the redundant ancestor lineage | PASS | 15 -> 7 terms; translation lineage 7 -> 2 |
| ont='ALL' returns the three ontologies with an ONTOLOGY column | PASS | BP 15, CC 13, MF 8 |
| groupGO is a classification, not a test | PASS | 476 rows, no p-value column |
| The Skill describes what simplify() actually does to an ont='ALL' object | FAIL | Skill says 'redundancy not removed, or an error'; it silently returned BP only (15 of 36) |

## Input 5 — Stress: Direction-split ORA, fold enrichment, redundancy collapse and a custom gene set

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 55/60 · **Total 92/100**
- Execution: runs/in5_stress.R using blocks b01, b03 and b06 verbatim; output runs/in5_stress.out.
- Finding: Up (81) and down (69) proteins tested separately gave 11 and 2 terms with the planted term leading both (fold enrichment 12.39 and 10.80), simplify reduced them to 6 and 1, the mixed list gave 15 terms, and the enricher block ran on a 120-row TERM2GENE with the same universe.

| Assertion | Result | Evidence |
|---|---|---|
| ORA is run separately per direction as the Skill directs | PASS | up 11 terms, down 2 terms |
| Fold enrichment accompanies every reported term | PASS | 12.39 / 10.80 for the planted term |
| Redundancy is collapsed before reporting | PASS | simplify 11 -> 6 and 2 -> 1 |
| enricher runs on a custom TERM2GENE with the same universe | PASS | 1 term, p.adjust 1.0e-06 |
| Scope: ranked-list analysis is routed to gsea rather than faked with ORA | PASS | ORA/GSEA fork followed |

## Key strengths

- Every instruction is directly executable and was borne out: explicit ont, matched universe, deduplicated bitr mapping, fold enrichment with p.adjust, simplify per ontology
- The planted biology was recovered as the top term in every variant, including a 15-protein UniProt list
- Its documented traps reproduced exactly: pvalueCutoff filters the adjusted p (2 vs 466 terms), groupGO carries no p-values, omitting universe changes the null
- Reproducibility is addressed concretely (record org.Hs.eg.db and GO.db versions; annotation lives locally)

## Recommendations

### P2 — enrichResult column list is stale

- Observed in inputs: 1
- Problem: The Skill lists ID, Description, GeneRatio, BgRatio, pvalue, p.adjust, qvalue, geneID, Count; clusterProfiler 4.14.6 also returns RichFactor, FoldEnrichment and zScore, so the fold enrichment it tells the agent to compute is already provided.
- Root cause: Column list written against an older clusterProfiler.
- Fix: Add RichFactor, FoldEnrichment and zScore to the column list and say to use FoldEnrichment when present.

### P2 — simplify() on ont='ALL' silently drops two ontologies

- Observed in inputs: 4
- Problem: The Skill predicts 'redundancy not removed, or an error'; in practice it returned only the BP terms (15 of 36), silently discarding CC and MF.
- Root cause: The failure mode was written from the intent, not from the observed behaviour.
- Fix: State that simplify() on an ont='ALL' object returns only the first ontology's terms, so BP/MF/CC must be run and simplified separately.

### P2 — Second example is not self-contained

- Observed in inputs: —
- Problem: examples/go_all_ontologies.R stops immediately: it reads a de_results.csv that is not shipped, while the basic example runs offline.
- Root cause: Example written against a user file.
- Fix: Have the example simulate a small DE table (as the basic example does) or read one from tempdir().
