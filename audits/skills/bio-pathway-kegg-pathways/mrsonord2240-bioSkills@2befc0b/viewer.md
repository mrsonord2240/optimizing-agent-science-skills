> **Audit record for `bio-pathway-kegg-pathways`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@2befc0b](https://github.com/mrsonord2240/bioSkills/tree/2befc0bb138ea3b0a035402c78af1c62b8955522/pathway-analysis/kegg-pathways) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pathway-kegg-pathways

## Canonical final summary

**Final:** 90/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@2befc0bb138ea3b0a035402c78af1c62b8955522:pathway-analysis/kegg-pathways`

Final-pass metadata: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical | 37 | 55 | 92 | 3/3 | ✅ |
| 2 | Variant A | 38 | 56 | 94 | 3/3 | ✅ |
| 3 | Variant B | 38 | 57 | 95 | 3/3 | ✅ |
| 4 | Topology | 31 | 51 | 82 | 2/3 | ⚠️ |
| 5 | Organism Boundary | 38 | 57 | 95 | 3/3 | ✅ |
| 6 | Visualization | 38 | 56 | 94 | 3/3 | ✅ |
| 7 | Shipped-artifact Check | 38 | 57 | 95 | 3/3 | ✅ |

Execution average: **92.4 / 100**. Assertion pass rate: **20/21 (95.2%)**.

## Runtime and evidence

Every input ran in a private `kegg-phase2` micromamba environment (R 4.5.3; clusterProfiler 4.18.4; fgsea 1.36.2; SPIA 2.62.0; graphite 1.56.0; pathview 1.50.0; gson 0.2.1; org.Hs.eg.db 3.22.0). No shared environment was changed. Synthetic DE data is at `data/de_results.csv`; the exact scripts and unabridged outputs are in `run/`.

1. **ORA plus frozen snapshot:** `enrichKEGG` returned 169 live pathways. `gson_KEGG`, `write.gson`, `read.gson`, and generic `enricher` returned 169 pinned results with access date 2026-09-23. `enrichMKEGG` validly produced no significant module for this synthetic list.
2. **GSEA:** a decreasing named Entrez log2FC vector returned 169 KEGG GSEA terms. fgsea emitted expected precision warnings for extreme small p-values, rather than hiding them.
3. **Comparison:** up/down `compareCluster(fun='enrichKEGG')` produced 294 rows across two clusters with the explicit measured universe.
4. **Topology:** direct SPIA (`nB=10`) scored 117 pathways. Graphite conversion, relative name, and `ENTREZID:` prefixing worked and `runSPIA(..., nB=1)` structurally scored 193 pathways. The explicit one-bootstrap override is audit-only because the shipped source omits it.
5. **Bacterial IDs:** E. coli locus tags using `organism='eco', keyType='kegg'` returned 16 terms without an OrgDb.
6. **Overlay:** pathview downloaded hsa04110 KGML/PNG and wrote `hsa04110.pathview.png` under `run/`; its KEGG licensing notice was captured.
7. **Shipped files:** both R examples parse and `clusterProfiler::enrichKEGG` / `SPIA::spia` exports resolve.

## Detailed output evaluation

### Input 1 — Human KEGG ORA plus gson pinning

**Prompt:** Test an Entrez DE list against human KEGG pathways and modules with an explicit measured universe, then freeze the live KEGG release for repeatable enrichment.

**Output:** The live pathway call returned 169 terms; the snapshot-persisted generic ORA also returned 169 terms dated 2026-09-23. The module route completed but had zero significant modules for this synthetic signal.

- [PASS] Explicit-universe pathway ORA executed and returned 169 terms.
- [PASS] `gson_KEGG` was written/read and used in generic frozen ORA.
- [PASS] Both pathway and module APIs returned valid structured results.

### Input 2 — Ranked KEGG GSEA

**Prompt:** Use a decreasing named Entrez ranking for reproducible KEGG GSEA.

**Output:** `gseKEGG(..., seed=TRUE)` returned 169 terms. fgsea's small-p-value warning is expected and documents its numerical limit.

- [PASS] The seeded GSEA route completed with exit 0.
- [PASS] Live KEGG annotation and the stated organism/key type resolved.
- [PASS] Precision caveats were visible in captured output.

### Input 3 — Multi-condition comparison

**Prompt:** Compare enrichment between up- and down-regulated gene sets without dropping the shared measured background.

**Output:** `compareCluster` created 294 result rows with exactly two cluster labels.

- [PASS] Named lists executed through `compareCluster(fun='enrichKEGG')`.
- [PASS] Both condition labels were preserved.
- [PASS] The explicit universe was accepted.

### Input 4 — Direct SPIA and graphite topology

**Prompt:** Score signed signaling perturbation from DE fold changes through direct SPIA and graphite's converted KEGG graphs.

**Output:** Direct SPIA returned 117 rows and graphite returned 193 rows with `pG`, `pGFdr`, and `Status`. The source's graphite invocation was separately observed with its unmodified defaults for over eight minutes, then stopped only within this audit's positively identified process group; its partial output is preserved as `run/input4_nB10_interrupted.out`.

- [PASS] Direct SPIA produced required global and direction columns.
- [PASS] Graphite's `prepareSPIA`/relative-name workaround and `ENTREZID:` namespace route executed under an explicit audit `nB=1` override.
- [FAIL] The shipped `n_boot` setting does not govern graphite: `runSPIA()` omits `nB`, and `formals(SPIA::spia)$nB` is 2000.

### Input 5 — Prokaryotic locus-tag boundary

**Prompt:** Enrich E. coli locus tags directly, without forcing a human-style OrgDb translation.

**Output:** The documented `keyType='kegg'` route returned 16 terms.

- [PASS] Locus-tag KEGG enrichment executed.
- [PASS] No inappropriate OrgDb mapping was used.
- [PASS] A structured result was returned with exit 0.

### Input 6 — Pathview overlay

**Prompt:** Render fold changes on the KEGG cell-cycle map.

**Output:** pathview downloaded both map resources and rendered `hsa04110.pathview.png` in the audit directory.

- [PASS] The KGML and base PNG downloads completed.
- [PASS] A nonempty rendered overlay was produced.
- [PASS] The runtime printed KEGG's license-sensitive use notice.

### Input 7 — Shipped example integrity

**Prompt:** Verify that both shipped R examples parse and their core exports exist in the documented runtime.

**Output:** Both parsed successfully and their core functions resolved.

- [PASS] `kegg_enrichment.R` parsed.
- [PASS] `kegg_spia_topology.R` parsed.
- [PASS] Core clusterProfiler/SPIA exports exist.

## Veto assessment

Skill veto: PASS. Research veto: PASS. The private runtime supplied positive code-usability evidence for every claimed analytic route. The graphite bootstrap propagation issue is real and must be fixed, but it does not make the code syntactically unrunnable or invalidate the supplied statistical methods.

## Recommendation

**P1 — Forward `n_boot` into graphite `runSPIA`.** Change the shipped call to include `nB = n_boot`; update the reference timing after a rerun. Until then, the advertised interactive 200–500 bootstrap setting controls direct SPIA only and graphite silently uses 2,000 bootstraps.
