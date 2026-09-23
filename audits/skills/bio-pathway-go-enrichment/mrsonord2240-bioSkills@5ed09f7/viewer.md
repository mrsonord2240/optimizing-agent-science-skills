> **Audit record for `bio-pathway-go-enrichment`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@5ed09f7](https://github.com/mrsonord2240/bioSkills/tree/5ed09f789aed05537c7899553ac6ebc005fe7e93/pathway-analysis/go-enrichment) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pathway-go-enrichment

Generated: 2026-09-23 · rendered from `report.json` by `tools/render_viewer.py`.

> This viewer is **generated from the audit report**, not written by the auditor. It restates the report's own recorded scores, notes and assertions and adds nothing to them. Where a hand-written viewer would argue from the runs, this one points at the scripts in [scripts/](scripts/) instead.

Source: `mrsonord2240/bioSkills@5ed09f789aed05537c7899553ac6ebc005fe7e93:pathway-analysis/go-enrichment`
Audit type: Phase 2 final-pass audit of the exact requested source tip. The previous canonical JSON and viewer were archived at F:\OpenScience\audits\_pre-fix-20260923\bio-pathway-go-enrichment\ before this report was written.
Category: Data Analysis · Execution mode: A · Complexity: Complex · N = 7 · Executed: 7/7

## What the Skill claims to do

Gene Ontology over-representation analysis of a selected gene list using clusterProfiler enrichGO, with explicit background-universe selection, ID conversion, GO-DAG redundancy handling, and an optional GOseq length-bias branch.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 56 | **94** | 4/4 | yes | ✅ |
| 2 | Regression | 38 | 57 | **95** | 3/3 | yes | ✅ |
| 3 | Variant A | 39 | 57 | **96** | 5/5 | yes | ✅ |
| 4 | Variant B | 38 | 56 | **94** | 3/3 | yes | ✅ |
| 5 | Edge | 37 | 57 | **94** | 3/3 | yes | ✅ |
| 6 | Adversarial | 20 | 30 | **50** | 1/3 | yes | ❌ |
| 7 | Scope Boundary | 38 | 54 | **92** | 3/3 | yes | ✅ |

**Execution Average: 87.9 / 100** · **Assertion Pass Rate: 22/24**

**Static: 87/100** · Static weighted 34.8 + dynamic weighted 52.7 = **88/100** → ⛔ Reject, not deployable. **Veto override applied.**

---

## Veto gates

### Skill veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| stability | PASS |  |
| contract | PASS |  |
| determinism | PASS |  |
| security | PASS |  |

### Research veto — **FAIL**

| Check | Result | Detail |
|---|---|---|
| scientific integrity | PASS | Executed results use only local, versioned GO annotations. The foreground/universe membership used for audit probes is synthetic and labeled as such; no clinical or individual-level claims were made. |
| practice boundaries | PASS | The Skill frames ORA as hypothesis generation and routes ranked-list analyses to GSEA. |
| methodological ground | PASS | The explicit-universe, adjusted-p, FoldEnrichment, per-ontology simplification, groupGO, ID-conversion, and custom-enricher claims reproduced on the pinned isolated stack. |
| code usability | FAIL | The GOseq code block was executed verbatim after installing both its documented dependency (goseq 1.58.0) and geneLenDataBase 1.42.0. nullp(de_genes, 'hg38', 'ensGene') reported that no hg38/ensGene length data were available, attempted a UCSC download, then halted: 'Length information for genome hg38 and gene ID ensGene is not available. You will have to specify bias.data manually.' The Skill neither declares this additional TxDb/bias.data requirement nor supplies a runnable fallback. |

## Static score

| Category | Score | Note |
|---|---|---|
| functional suitability | 10/12 | Core ORA, all-ontology, ID-conversion, redundancy, and custom-set paths are runnable; the advertised RNA-seq GOseq path is not. |
| reliability | 10/12 | Strong explicit-universe and conversion-loss guidance, but no preflight for the GOseq length-data dependency or fallback bias.data path. |
| performance context | 7/8 | The examples are self-contained and complete; simplify() cost scales sharply with an unfiltered all-ontology result, which the normal thresholded examples avoid. |
| agent usability | 14/16 | Clear execution order and failure modes; the runnable-looking GOseq fence is a misleading dead end on the declared dependency set. |
| human usability | 7/8 | Readable prompts, result-column definitions, and caveats; the missing GOseq prerequisite is material. |
| security | 11/12 | No credentials or destructive operations; local OrgDb route is safe. The failing GOseq route attempts a network download without saying so. |
| maintainability | 11/12 | Self-contained shipped examples and explicit package-version guidance are strong. The GOseq integration needs a verified, version-pinned data source. |
| agent specific | 17/20 | Good routing boundaries and explicit statistical defaults, reduced by an optional branch that cannot execute as written. |

## Input 1 — Canonical: Run shipped go_enrichment_basic.R unchanged

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Execution: Executed the actual source file at pathway-analysis/go-enrichment/examples/go_enrichment_basic.R in a fresh environment; no substitutions.
- Finding: Exit 0. The self-contained BP example returned 135 terms. Its result frame included RichFactor, FoldEnrichment, and zScore.

| Assertion | Result | Evidence |
|---|---|---|
| Shipped basic example runs without unshipped input | PASS | Exit 0; it constructs foreground and universe from org.Hs.eg.db. |
| Explicit BP ORA returns results | PASS | 135 terms. |
| Fixed enrichResult column list is present | PASS | RichFactor, FoldEnrichment, and zScore present. |
| Example uses a matched universe | PASS | universe_ids is supplied to enrichGO. |

## Input 2 — Regression: Run shipped go_all_ontologies.R unchanged

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Execution: Executed the actual source file at pathway-analysis/go-enrichment/examples/go_all_ontologies.R in a fresh environment; no substitutions.
- Finding: Exit 0. The per-ontology loop produced a combined 85-row result with the expected enrichResult columns. Counts differ from older audit evidence because the isolated stack uses its locally pinned annotation release, not because the source was altered.

| Assertion | Result | Evidence |
|---|---|---|
| Shipped all-ontology example runs end to end | PASS | Exit 0; no external de_results.csv is needed. |
| Example simplifies each ontology explicitly | PASS | lapply over BP/MF/CC. |
| Combined output preserves enrichment columns | PASS | RichFactor, FoldEnrichment, zScore present. |

## Input 3 — Variant A: Canonical ORA contract, pvalueCutoff semantics, and universe effect

- Status: ✅ COMPLETED · Basic 39/40 · Specialized 57/60 · **Total 96/100**
- Execution: Executed enrichGO with the Skill's BP arguments on synthetic membership over real org.Hs.eg.db annotations, then compared matched-universe and omitted-universe calls.
- Finding: Canonical BP call returned 135 rows and exactly the documented 12 columns. Omitting universe changed the parsed annotated background denominator from 2,496 to 18,986. With cutoffs relaxed, 250 terms had raw p < 0.05 but adjusted p >= 0.05; strict output fell from 2,565 to 135 rows, reproducing adjusted-p filtering.

| Assertion | Result | Evidence |
|---|---|---|
| Canonical enrichGO argument pattern executes | PASS | BP call returned 135 rows. |
| Column contract matches documentation | PASS | Exact documented 12-column order. |
| Omitting universe changes the null | PASS | N 2,496 to 18,986. |
| pvalueCutoff acts on adjusted p | PASS | 250 raw-significant but adjusted-nonsignificant rows were excluded by strict cutoffs. |
| enrichGO default ontology is MF | PASS | formals(enrichGO)$ont == 'MF'. |

## Input 4 — Variant B: Corrected simplify(ont='ALL') claim and groupGO boundary

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Execution: Executed ont='ALL' enrichGO at the shipped threshold, then simplify(..., measure='Wang'), and executed groupGO on the same foreground.
- Finding: ont='ALL' returned 194 terms; simplify returned 85 spanning BP 54, CC 5, and MF 26. This directly verifies the 5ed09f7 correction: no ontology is silently dropped. groupGO returned 476 classification rows and no pvalue column.

| Assertion | Result | Evidence |
|---|---|---|
| simplify collapses an all-ontology object without dropping MF or CC | PASS | 194 to 85; BP54/CC5/MF26. |
| Corrected simplify_ALL dispatch explanation matches behavior | PASS | All three ONTOLOGY values remain after simplification. |
| groupGO is descriptive rather than a significance test | PASS | 476 rows; no pvalue column. |

## Input 5 — Edge: UniProt conversion and custom TERM2GENE enrichment

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 57/60 · **Total 94/100**
- Execution: Executed bitr(UNIPROT -> ENTREZID) and a two-term local TERM2GENE enricher call against the same explicit universe.
- Finding: The sampled 25 UniProt keys mapped to 25 rows and four unique Entrez IDs (the sample includes isoforms, so it is a mapping-mechanics probe rather than a representative conversion rate). The custom enricher returned two rows and the shared RichFactor/FoldEnrichment/zScore columns.

| Assertion | Result | Evidence |
|---|---|---|
| Documented bitr route executes | PASS | 25 input keys, 25 mapped rows. |
| Custom enricher accepts the same explicit universe | PASS | Two local TERM2GENE terms returned. |
| Custom enrichResult shares documented effect-size columns | PASS | RichFactor, FoldEnrichment, zScore present. |

## Input 6 — Adversarial: GOseq RNA-seq length-bias block executed verbatim

- Status: ❌ COMPLETED · Basic 20/40 · Specialized 30/60 · **Total 50/100**
- Execution: Executed the exact library/nullp/goseq/BH sequence from SKILL.md with a synthetic named Ensembl 0/1 vector after installing goseq and geneLenDataBase in the isolated runtime.
- Finding: The block halted at nullp(de_genes, 'hg38', 'ensGene'). goseq reported no hg38/ensGene length data, attempted UCSC retrieval, then stopped because length information was unavailable. The source contains no required TxDb installation, supplied bias.data, or working fallback.

| Assertion | Result | Evidence |
|---|---|---|
| The documented goseq dependency loads | PASS | goseq 1.58.0 and geneLenDataBase 1.42.0 loaded. |
| nullp(..., 'hg38', 'ensGene') executes from documented prerequisites | FAIL | No length data available; downloaded fallback also failed. |
| The full code block reaches BH correction | FAIL | Execution halted before goseq() and p.adjust(). |

## Input 7 — Scope Boundary: Source, contract, and scientific-scope audit

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 54/60 · **Total 92/100**
- Execution: Read the exact source at the verified clean tip and inspected the front matter, routing, stated statistical model, threshold caveats, and references.
- Finding: Front matter is parseable; scope cleanly distinguishes ORA, GSEA, other pathway databases, and descriptive groupGO. It properly treats enrichment as hypothesis generation and contains no clinical inference or secret-handling path.

| Assertion | Result | Evidence |
|---|---|---|
| Front matter and basic contract are valid | PASS | name, description, tool_type, primary_tool, and license are present. |
| Method boundary is scientifically appropriate | PASS | ORA versus GSEA and hypothesis-generation boundary are explicit. |
| No unsafe operational or clinical path is introduced | PASS | Local annotation analysis only. |
