# bio-single-cell-batch-integration fix pass

## 2026-09-24

Source: `mrsonord2240/bioSkills@8edc49ca40e7eab8a24c1d9555a176ae894e16ac:single-cell/batch-integration`.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| Seurat RPCA exceeds its default future globals limit | P1 | Added the 4 GiB `future.globals.maxSize` setting before `IntegrateLayers`, a recovery row, and a runnable Seurat script. | R parse; focused exact-commit script run | The limit is intentionally documented as memory-dependent. |
| FastMNNIntegration and scVIIntegration are not bare Seurat symbols | P2 | Named the SeuratWrappers boundary, its scVI dependency, and usable fallbacks; the script now fails with that actionable message. | R parse; installed-package boundary checked in audit env | No SeuratWrappers installation was added. |
| Harmony theta wording did not give a useful scale | P2 | Added the audited 0.5--5 starting range, default-near-2 guidance, and `theta = 0` caveat. | Prior synthetic theta sweep; static review | Tuning still requires paired batch/bio checks. |
| Scanorama requires contiguous batches | P2 | Added stable-sort requirement to method selection and Common Errors. | Prior synthetic Scanorama regression | Preserve original-order mapping for joins and plotting. |
| Confounded-design cluster check was insufficient alone | P2 | Made condition-by-batch metadata the first stop test; kept cluster cross-tabs only for effect sizing. | Prior confounded synthetic regression; static review | A mixed cluster never rescues a confounded design. |
| No copied code pattern set reproducibility controls | P2 | Added seeded Python scripts, `scvi.settings.seed`, explicit epochs, and seeded Seurat steps. | Python compile; R parse; focused exact-commit executable runs | Scripts are now the canonical runnable paths. |

### Left unfixed

None. All six audited P1/P2 findings were corrected without adding packages or changing the skill frontmatter name.

### Deleted passage to new home

| old location | new home |
|---|---|
| SKILL.md inline Harmony pipeline | `scripts/harmony_integration.py`; invocation in `SKILL.md` Integrate with Harmony |
| SKILL.md inline scVI/scANVI pipeline | `scripts/scvi_scanvi_integration.py`; invocation in `SKILL.md` Integrate with scVI / scANVI |
| SKILL.md inline Seurat v5 pipeline | `scripts/seurat_v5_integration.R`; invocation in `SKILL.md` Integrate with Seurat v5 |
| SKILL.md advanced Harmony/scVI/Seurat detail | `references/harmony.md`, `references/scvi-scanvi.md`, and `references/seurat-v5.md`, linked from the Method Selection table and Reference Files index |
| usage-guide prerequisites, workflow, and tips | Canonical sections in `SKILL.md`; guide now retains overview, prompts, and related skills |
