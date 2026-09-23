# Fix log: bio-single-cell-lineage-tracing

2026-09-19. Fixer for `single-cell/lineage-tracing`. Audit: `F:\OpenScience\audits\bio-single-cell-lineage-tracing\`
(77/100, Skill Veto FAIL / T1 Stability, grade Reject, 9 findings). Fork commit
`563b098` on `main`. Fix branch `fix/sc-lineage`, worktree `F:\OpenScience\wt\sc-lineage`,
commit `31e9e7c`.

## Findings

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| `pip install cassiopeia-lineage cospar scanpy` installs a broken, wrong-API package | P0 | Replaced with bioconda install (`conda install -c bioconda cassiopeia`) in a new SKILL.md "Installation and Version Compatibility" section; usage-guide.md Prerequisites now points there | ran | Cassiopeia 2.0.0 installed via bioconda in a WSL science-distro conda env; every `cas.data`/`cas.solver`/`cas.pp`/`cas.critique` call in the Skill matches the installed API |
| Cassiopeia/CoSpar hard numpy conflict (numpy<2 vs numpy>=2) | P0 | Documented two-environment split + file handoff pattern | ran | Built both envs independently: Cassiopeia env at numpy 1.26.4 (bioconda), CoSpar+scanpy env at numpy 2.5.3 (pip venv); reproduced the conflict when combined (matches audit) |
| `NeighborJoiningSolver` raises `DistanceSolverError` as documented | P1 | Added required `add_root=True` to SKILL.md snippet + `examples/cassiopeia_reconstruction.py` | ran | Fails without `add_root=True`, succeeds with it, on audit's 60-cell/16-site synthetic data; `inspect.signature` confirms it's a constructor kwarg (default `False`) |
| `ILPSolver`/`HybridSolver` silently needs licensed Gurobi | P1 | Documented `gurobipy` prerequisite in Installation section, solver table, Common Errors, inline comments; changed example's `HybridSolver` default to greedy/greedy (license-free) | ran | `ILPSolver().solve(...)` reproduces the exact reported `ValueError`; greedy/greedy `HybridSolver` runs clean |
| No mtDNA clonal-grouping method/code anywhere | P1 | Wrote a hotspot-blacklist + hierarchical-clustering pattern (new SKILL.md section) | ran | Verified against audit's synthetic 40-cell/4-clone/1-hotspot heteroplasmy matrix: adjusted Rand index 1.0 vs ground truth; correctly blacklists the one planted hotspot variant (`chrM_8860`) |
| "Startle" named in frontmatter/solver table with zero actionable code | P1 | Installed Startle 1.0.0 from public bioconda channel `schmidt73` into this Skill's own dedicated env; wrote a real CLI usage pattern (new SKILL.md section) | ran | End-to-end on the Skill's own 60-cell/16-site synthetic scar matrix: seed tree (VanillaGreedySolver) at weighted parsimony ~7.5, refined to 6.59 over 20 NNI iterations by `startle large`; also confirmed against Startle's own published GitHub example (100-cell/30-character) |
| No escape-hatch for clinical/diagnostic misuse of tumor lineage output | P1 | Added a Common Errors row declining diagnostic/treatment claims, recommending clinical handoff | docs only, not re-run | Re-running the adversarial clinical probe against the new text is a re-auditor task |
| No CoSpar runtime-scaling guidance | P2 | Added one-line note (~10 min / 200 cells at default `smooth_array`) | n/a (restates audit's own measured runtime) | |
| Version-compatibility preamble never demonstrated introspect-and-adapt | P2 | Installation section's adaptation guidance now cites the NeighborJoiningSolver `add_root` gap as its own worked example | n/a (docs) | |

## Found while verifying, fixed inline (not in the audit's 9 findings)

- `(char_matrix == -1).mean():.2%` in SKILL.md's own snippet and
  `examples/cassiopeia_reconstruction.py` formats a pandas Series (not a scalar) under
  pandas 2.3.3/3.0.x and crashes with `TypeError`. Fixed to `(char_matrix.values == -1).mean()`.
  Ran: prints `missing 2.60%` correctly on the audit's synthetic data (matches what the
  audit itself reported, meaning the auditor's own run script differed from the literal
  shipped snippet).
- `cas.pl.plot_matplotlib(...)` in `examples/cassiopeia_reconstruction.py` does not exist
  in installed Cassiopeia 2.0.0 (`cas.pl` only exposes `upload_and_export_itol`, needing
  an iTOL API key). The audit never hit this because its own run script didn't include
  the plotting call. Removed the call, left a comment pointing at `ete3` (already a
  Cassiopeia dependency) or iTOL for external plotting.

## Dedup pass (per the 2026-09-17 rule, applied on every touch)

`usage-guide.md`'s "Tips" section (9 bullets) restated facts already present verbatim in
SKILL.md: state-vs-fate (Governing Principle), missing-vs-unedited and mtDNA clonal
grouping (Common Errors + Assay Decision Table), homoplasy and solver panel guidance
(Solver Decision Table), CoSpar behavior (CoSpar section). Nothing in Tips was unique to
the guide. Deleted the section; replaced with a one-line pointer to the SKILL.md sections
that hold those facts.

## Left unfixed

Nothing from the audit's 9 findings was left unfixed. The two P2s are documentation-only
additions restating the auditor's own measured evidence, not independently re-run.

## Root cause of the T1 veto

Resolved: the veto's evidence was (1) the only documented install command installing a
broken, wrong-API package, and (2) an unresolvable numpy conflict when the correct
install (bioconda) was combined with CoSpar/scanpy in one environment. Both are now
addressed with a verified-working install path (bioconda Cassiopeia + separate CoSpar
env, file-based handoff) rather than a single combined environment. Re-auditor confirms
whether this clears T1.

---

## 2026-09-21 second fix pass

Fixer for `single-cell/lineage-tracing`, from the re-audit (86/100, veto cleared, 1 P1 + 2 P2). Branch
`fix/single-cell-lineage-tracing`, worktree `F:\OpenScience\wt\single-cell-lineage-tracing`, commit
`c8a441f`. Checked on CoSpar 0.5.0, scanpy 1.12.4, numpy 2.5.3 (existing `cospar-venv`, run through WSL `science`).
SKILL.md is 293 lines, under the 300-line split threshold, so no `references/` split.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| CoSpar snippet crashes with `KeyError: 'X_emb'` (no PCA/UMAP before `initialize_adata_object`) | P1 | SKILL.md snippet and `examples/cospar_dynamics.py` build `X_pca`/`X_umap` on a log-normalized copy and pass them as `X_pca=`/`X_emb=`; comment explains the late, confusing crash | ran | Literal old snippet reproduced the KeyError. New snippet ran on the audit's 2-timepoint data (200 fate_bias rows) and 3-timepoint data (240 rows). Example ran end to end incl. plots (MPLBACKEND=Agg). Deliberately not the re-audit's suggestion of `sc.pp.log1p` on `adata` itself: CoSpar warns `adata.X` must NOT be log-transformed, so embedding comes from a copy |
| CoSpar 3-timepoint `ValueError: pre-computed similarity matrix does not have the right dimension` | P2 | Re-audit's diagnosis (timepoint limit) was wrong. Cause is a `data_des` cache collision: the default `data_des='cospar'` caches similarity matrices in `./data/` and the 3-timepoint run reused the 2-timepoint dataset's. Snippet now sets `data_des='my_dataset'`; one paragraph names the error, the cause and both fixes | ran | Reproduced the exact error by running the 2- then 3-timepoint data with default `data_des` in one directory; `compute_new=True` cleared it; a unique `data_des` on 3-timepoint data ran clean. The note states only that 2 and 3 time points were run |
| No consent/privacy note for mtDNA from primary human tissue | P2 | One sentence at the end of the mtDNA section | n/a (docs) | |

Found while verifying:

- "`infer_Tmap_from_multitime_clones` ~10 minutes for a 200-cell toy dataset" (added by the 2026-09-19 fix from the audit's timing) is
  contradicted by this pass: ~15 s (2-timepoint) and ~9 s (3-timepoint), similarity matrices included. Replaced with the measured
  figure, dated, and kept the "grows with cell number" advice. Superseded the older claim.

Dedup: `usage-guide.md` Prerequisites repeated "Do not `pip install cassiopeia-lineage` ..." which SKILL.md's Installation section
holds in full. Deleted the line; the guide still points at the SKILL.md section.

Left unfixed: none. (The re-audit's Input 3, raw-reads-to-character-matrix, stayed introspection-only: it is not a numbered
recommendation, and no barcode-read fixture exists to run it; not a Skill defect, so not touched.)
