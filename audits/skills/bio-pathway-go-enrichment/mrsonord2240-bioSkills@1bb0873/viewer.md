> **Audit record for `bio-pathway-go-enrichment`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@1bb0873](https://github.com/mrsonord2240/bioSkills/tree/1bb08737d3b24d54f00f5d35aa096f9fd2e04b79/pathway-analysis/go-enrichment) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pathway-go-enrichment

Generated: 2026-09-23
Source: `mrsonord2240/bioSkills@1bb08737d3b24d54f00f5d35aa096f9fd2e04b79:pathway-analysis/go-enrichment`

Final-pass metadata: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.
Environment: isolated WSL R 4.4.3 / Bioconductor 3.20 (clusterProfiler 4.14.0, org.Hs.eg.db 3.20.0, goseq 1.58.0, GenomicFeatures 1.58.0, TxDb.Hsapiens.UCSC.hg38.knownGene 3.20.0). The shared Windows environment was not changed.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---|---|
| 1 | Canonical | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 2 | Regression | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 3 | Variant A | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 4 | Variant B | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 5 | Edge | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 6 | Adversarial | 39 | 57 | 96 | 4/4 PASS | ✅ |
| 7 | Scope Boundary | 38 | 56 | 94 | 4/4 PASS | ✅ |

**Execution Average: 94.9 / 100**
**Assertion Pass Rate: 28/28**

## Detailed Outputs

### Input 1 — Shipped basic BP enrichment example

**Prompt:** Run the supplied self-contained BP GO ORA example without modifying it.

**Saved code/output:** `run/phase2_inputs_1_5.R`, `run/phase2_inputs_1_5.out`; the runner sourced the exact `examples/go_enrichment_basic.R`.

**Observed output:** `Found 135 enriched GO BP terms`; the asserted `enrichResult` columns included `GeneRatio`, `BgRatio`, `FoldEnrichment`, `p.adjust`, and `Count`.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100.

**Assertions:**

- [PASS] Unchanged shipped example executed — source completed in a fresh environment.
- [PASS] Result is an `enrichResult` with required ORA columns — assertion passed.
- [PASS] Explicit tested-gene universe is used — exact example passes `universe_ids`.
- [PASS] Output stays non-clinical — GO hypotheses only.

### Input 2 — Shipped per-ontology simplification example

**Prompt:** Run the supplied BP/MF/CC example and simplify each ontology.

**Saved code/output:** `run/phase2_inputs_1_5.R`, `run/phase2_inputs_1_5.out`; the runner sourced exact `examples/go_all_ontologies.R`.

**Observed output:** `BP : 54 terms after simplify`, `MF : 26 terms after simplify`, `CC : 5 terms after simplify`; combined total `85`.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100.

**Assertions:**

- [PASS] No unshipped DE input was required — example generated OrgDb-based input.
- [PASS] BP, MF, and CC all completed — output reported each ontology.
- [PASS] Simplification was nonempty — combined data frame had 85 terms.
- [PASS] The example did not mislabel group classification as significance — it used enrichment plus simplify only.

### Input 3 — Explicit-universe ORA and cutoff inspection

**Prompt:** Run BP ORA with a matched 3,000-gene tested universe and inspect all terms before applying a significance threshold.

**Saved code/output:** `run/phase2_inputs_1_5.R`, `run/phase2_inputs_1_5.out`.

**Observed output:** `INPUT3_OK explicit_universe_terms=2565 annotated_universe=2496` with asserted `FoldEnrichment`, `pvalue`, `p.adjust`, and `Count` columns. The script verified `p.adjust >= pvalue` (allowing missing values).

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100.

**Assertions:**

- [PASS] Explicit-universe ORA returned terms — 2,565 rows.
- [PASS] Effect size and adjusted significance columns were present.
- [PASS] BH adjusted values satisfied the checked relationship to raw p-values.
- [PASS] The annotated tested background was reported — 2,496 genes.

### Input 4 — `ont='ALL'` simplify and `groupGO` boundary

**Prompt:** Test all three ontologies, simplify their redundancy, and ensure `groupGO` remains a classification rather than a significance test.

**Saved code/output:** `run/phase2_inputs_1_5.R`, `run/phase2_inputs_1_5.out`.

**Observed output:** `INPUT4_OK simplify_terms=85 ontologies=BP,CC,MF groupGO_rows=476`; `groupGO` had no `p.adjust` column.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100.

**Assertions:**

- [PASS] Simplified output retained BP, CC, and MF labels.
- [PASS] Simplified enrichment was nonempty — 85 terms.
- [PASS] `groupGO` did not expose `p.adjust` — it was not treated as a test.
- [PASS] The all-ontology enrichment used an explicit universe.

### Input 5 — UniProt conversion and custom local gene sets

**Prompt:** Map UniProt IDs to Entrez IDs and run a custom local `TERM2GENE` over-representation test.

**Saved code/output:** `run/phase2_input5_custom.R`, `run/run_phase2_input5_custom.sh`, `run/phase2_input5_custom.out`.

**Observed output:** `INPUT5_OK uniprot_mapped=126 custom_terms=1`; the planted `FOREGROUND_TERM` was returned by `enricher`.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100.

**Assertions:**

- [PASS] UniProt identifiers were converted and deduplicated — 126 Entrez IDs.
- [PASS] Custom enrichment used an explicit local universe.
- [PASS] The planted foreground category was recovered.
- [PASS] The complete TERM2GENE input was created locally by the saved runner.

### Input 6 — Literal hg38 GOseq length-bias route

**Prompt:** Run the current documented hg38 Ensembl GOseq fence without replacing its code.

**Saved code/output:** `run/phase2_goseq_prelude.R`, `run/run_phase2_goseq_literal.sh`, `run/phase2_goseq_literal.out`. The shell runner concatenated the saved prelude with exact current `SKILL.md` lines 132–174.

**Observed output:**

```text
ENSEMBL -> ENTREZID: 300/300 (100.0%)
TxDb-mapped genes with GO annotations: 294/298 (98.7%)
Using manually entered categories.
Calculating the p-values...
INPUT6_OK literal_rows=3346padj=TRUE
```

The PWF issued the non-fatal numerical message `initial point very close to some inequality constraints`; all postconditions passed.

**Scores:** Basic 39/40 | Specialized 57/60 | Total 96/100.

**Assertions:**

- [PASS] No implicit `hg38`/`ensGene` lookup was invoked — local `bias.data` and `gene2cat` were supplied.
- [PASS] Conversion and local GO-coverage preflight were reported and passed.
- [PASS] Wallenius GOseq returned 3,346 rows with BH `padj`.
- [PASS] The run used the isolated prefix and did not change the shared environment.

### Input 7 — Source contract and research-scope boundary

**Prompt:** Verify the exact source tip’s front matter, files, routing, executable choices, and non-clinical boundary.

**Saved code/output:** `run/phase2_input7_scope.py`, `run/run_phase2_input7_scope.sh`, `run/phase2_input7_scope.out`.

**Observed output:** all ten checks returned `True`, ending with `INPUT7_OK static_checks= 10`.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100.

**Assertions:**

- [PASS] Correct front matter, usage guide, and two examples exist.
- [PASS] ORA code specifies both `universe` and BP ontology.
- [PASS] The GOseq code fence uses TxDb plus local `gene2cat`, not the deprecated implicit lookup.
- [PASS] The source routes ranked inputs to GSEA and contains no diagnostic or prescriptive wording.

## Gates and Static Review

Structural veto: PASS (stability, contract, determinism, security).
Research veto: PASS (scientific integrity, practice boundaries, methodological ground, code usability).
Static score: 91/100. The main issue is an internal reproducibility statement conflict: the global compatibility text names clusterProfiler 4.18.4+/org.Hs.eg.db 3.22+, but the usage guide and executable hg38 route pin Bioconductor 3.20 and this re-audit verified clusterProfiler 4.14.0/org.Hs.eg.db 3.20.0.

## Final

Static weighted: 36.4
Dynamic weighted: 56.9
**Final score: 93/100 — ⭐ Production Ready — deployable: true.**

Recommendations are one P1 (reconcile the conflicting compatibility statements) and one P2 (move the expanded GOseq recipe into a parameterized script). The report metadata explicitly sets `auditor_independent: false` for this final-pass exception.
