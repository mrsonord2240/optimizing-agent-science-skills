# Fix log: bio-single-cell-perturb-seq (2026-09-19)

Fixer for `single-cell/perturb-seq`. Source audit: `F:\OpenScience\audits\bio-single-cell-perturb-seq\`
(`eval_report_bio-single-cell-perturb-seq_result.json`, score 75, Beta Only, deployable: false, no
veto). Fork: `mrsonord2240/bioSkills-Improved@main`, worktree `F:/OpenScience/wt/sc-perturb`, branch
`fix/sc-perturb`. Env: `F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\` (pertpy 1.3.0,
scanpy 1.12.4, R 4.4.3). Verified against the real `pt.dt.papalexi_2021()` dataset (20,729 cells,
downloaded fresh from `https://exampledata.scverse.org/pertpy/papalexi_2021.h5mu`, public/
unauthenticated), not synthetic data — same dataset the audit used.

| Finding | Priority | Change | Verified | Notes |
|---|---|---|---|---|
| `assign_mixture_model` needs undocumented JAX extra | P1 | Added `pip install 'pertpy[jax]'` to Prerequisites (moved into SKILL.md, with the real fallback signature for `assign_by_threshold`) | ran: `ImportError` reproduced exactly as the audit found (confirmed via `pip show`: `optax` absent, `jax` 0.11.1 present); confirmed `pertpy[jax]` extra pulls `optax`+`flax`+`numpyro`+`ott-jax` via package metadata | |
| Shipped `pertpy_analysis.py` `KeyError` (perturbation columns on `mdata.obs`, not `adata.obs`) | P1 | Added `mdata.push_obs(columns=['perturbation','gene_target','replicate'], mods=['rna'])` before Mixscape calls, in both SKILL.md and the example | ran end-to-end on real papalexi_2021 data: mixscape_class_global NP 13645 / KO 4698 / NT 2386 — matches the audit's own real run (13644/4699/2386) to within 1 cell | Also fixed a second real bug hit during verification: `gdo.X` ships as CSC and both `assign_mixture_model`/`assign_by_threshold` require CSR/dense (`NotImplementedError` otherwise) — added `gdo.X = gdo.X.tocsr()`. Also fixed a real internal inconsistency: SKILL.md used `pert_key='target_gene'` in the Mixscape snippet but `'gene_target'` in the shipped example, for the same dataset; `gene_target` is the column that actually exists (verified against the real MuData) — standardized on `gene_target` everywhere (Mixscape, Pseudobulk `target_col`, Milo `design`) |
| Milo example structurally incompatible with pooled Perturb-seq design | P1 | Replaced `sample_col='replicate'` / `design='~ gene_target'` with a per-(replicate x target) pseudo-sample column and a per-target-vs-NT subset; added the missing `sc.pp.neighbors()` call `make_nhoods` needs | ran end-to-end on real data: STAT1 vs NT, 22/194 neighborhoods DA at SpatialFDR<0.1 via `da_nhoods(..., solver='pydeseq2')` — no AssertionError | Confirmed the original design is a hard structural mismatch (per `da_nhoods`'s own docstring/example), not a flag issue, matching the audit's diagnosis |
| scMAGeCK: decision-table entry with zero code anywhere | P2 | Reframed rather than wrote a worked example: added a note that scMAGeCK is Bioconductor-staging-only (not CRAN/Bioc release), needs a compiled C++ component, and is absent from this Skill's tested env; pointed to the real upstream repos and named its two real entry points (`scmageck_lr`, `scmageck_rra`, per Yang et al. 2020, already in References) | checked docs: confirmed via `available.packages()` (not found on CRAN/Bioc release repos) and r-universe search (found only under Bioconductor's `biocstaging` index, topic `cpp`) | Chose "delete/reframe the claim" over "write it" or "install it": the FIX_BRIEF's own "Verify every change" section bars installing into the shared R env as a fixer, and scMAGeCK's own GitHub README defers to a separate Bitbucket repo for real usage docs, so a fabricated code block would not be genuinely verified. Kept the (accurate) decision-table row rather than deleting it outright |
| `sceptre` needs R>=4.5, undocumented | P2 | Added the R>=4.5 requirement and the silent-no-op behavior to SKILL.md's Prerequisites and the SCEPTRE section | checked docs: corroborates `TOOLS.md`'s independent finding (`available.packages()` filters it out under R 4.4.3; no `sceptre` folder in R-lib) and the audit's own directory-listing confirmation — two independent sources, not executed further (cannot install R>=4.5 here) | |
| E-test permutation has no documented/exposed seed | P2 | Added `np.random.seed(0)` before the `etest(...)` call, with a comment that `DistanceTest` exposes no seed of its own | checked API: `inspect.signature` on `DistanceTest.__init__`/`__call__` confirms no seed/random_state parameter anywhere | |

## Redundancy pass (per FIX_BRIEF, every pass)

- Deleted `usage-guide.md`'s **Decision Guidance** and **Tips** sections: both restated
  SKILL.md's Governing Principle / Method Decision Tables / Common Errors verbatim or near-verbatim.
- One fact found only in the deleted text and needed by the agent: the GSFA/scMAGeCK-LR mention
  for high-MOI deconvolution (`Decision Guidance > Guide assignment`) — moved into SKILL.md's
  Governing Principle (MOI paragraph). The "non-targeting controls define the null" tip was folded
  into the same paragraph's NT/contamination-floor sentence.
- Moved the actual `pip`/`install.packages` commands (previously only in `usage-guide.md`'s
  Prerequisites) into SKILL.md's Prerequisites, since these are commands the agent acts on;
  `usage-guide.md`'s Prerequisites now points to SKILL.md instead of repeating them.
- `usage-guide.md`'s Overview, Quick Start, Example Prompts, "What the Agent Will Do", and Related
  Skills are unchanged (human-facing, not restated elsewhere).

## Left unfixed

None of the 6 findings were left unfixed. scMAGeCK (P2) was resolved by reframing rather than by
shipping a new worked example — see the table above for why installing/writing it was not the
right call here.

## Deployability

All three P1 defects were real, reproducible execution failures (Inputs 1, 4-adjacent, and 5 in the
audit) and all three now run clean against the same real dataset the audit used, producing sensible,
checkable output (cell-type-split counts matching the audit's own run to within 1 cell; a real DA
result with an interpretable SpatialFDR). Whether this clears the skill-auditor's execution-avg /
assertion-pass-rate deployability floor is for the re-auditor to confirm.
