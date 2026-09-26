# bio-single-cell-cell-annotation fix pass

## Source

- Repository worktree: `F:\OpenScience\worktrees\bio-single-cell-cell-annotation-fixpass`
- Branch: `fix/bio-single-cell-cell-annotation-audit-20260924`
- Exact commit: `b7fc90e69bdf4839b958a13b37581945ba694413`
- Changed file: `single-cell/cell-annotation/SKILL.md`

## Fixes

- Corrected CellTypist’s current raw-count and gene-ID failure modes while retaining the genuinely silent scale-mismatch case.
- Made CellTypist majority voting consume an explicit, seeded upstream `leiden` over-clustering.
- Scoped SingleR pruning to label-score ambiguity and required marker/reference-domain triangulation for confidently wrong calls.
- Replaced confidence-first novel-cluster screening with QC-first, all-cluster triage; confidence is retained as secondary evidence.
- Normalized the Seurat object before marker `DotPlot` validation.

## Exact-commit re-audit

- Final score: **94 / 100 — Production Ready**
- Assertions: **20 / 20 PASS**
- Focused executable validation: **15 / 15 PASS**
- No remaining P0, P1, or P2 findings.

The focused run verifies the exact Git SHA before reading the source, executes the corrected CellTypist path on the existing audit fixture, verifies current hard errors for raw-count and Ensembl-ID input, and executes the QC-first triage fence. The SingleR caveat and Seurat `NormalizeData` precondition are source-checked against retained prior execution evidence. An Azimuth end-to-end rerun was not performed because this host has no `Rscript`; this is explicitly disclosed in the viewer.

## Artifacts

- Canonical report: `F:\OpenScience\audits\bio-single-cell-cell-annotation\eval_report_bio-single-cell-cell-annotation_result.json`
- Canonical viewer: `F:\OpenScience\audits\bio-single-cell-cell-annotation\eval_viewer_bio-single-cell-cell-annotation.md`
- Focused test: `F:\OpenScience\audits\bio-single-cell-cell-annotation\run\exact-commit-b7fc90e\reaudit_focused.py`
- Focused log: `F:\OpenScience\audits\bio-single-cell-cell-annotation\run\exact-commit-b7fc90e\reaudit_focused.log`
- Report builder: `F:\OpenScience\audits\bio-single-cell-cell-annotation\run\exact-commit-b7fc90e\build_reaudit_report.py`

## Marketplace pilot follow-up (2026-09-25)

Exact source: `mrsonord2240/optimized-scientific-skills@2dee47f80dac6f3ba5c78b53ea9ec132a87cf5db:skills/bio-single-cell-cell-annotation`.

- Hardened the bundled CellTypist CLI to require raw counts, seeded Leiden over-clustering, and UMAP;
  restore CP10K/log1p input; resolve only an existing explicit or cached model path; and accept
  configurable output paths without implicit model acquisition.
- Independent re-audit scored **91/100, Production Ready, deployable**. Five of seven inputs completed
  with clean exits; 33/35 assertions passed; no veto or P0.
- Open P1: obtain an exit-0 Linux smoke for SingleR and Azimuth. Both Windows routes completed and
  validated their scientific outputs but returned exit 2816 during teardown, so they remain partial.
- Open P2s: align the inline CellTypist block with the executable's offline model contract; add runnable
  scANVI and scmap examples.
