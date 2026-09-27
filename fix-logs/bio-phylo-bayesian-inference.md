# bio-phylo-bayesian-inference — Phase 2 final pass

Date: 2026-09-24  
Source commit: `4850b2c8c03bbbe86bf7fe5561bbb0a9df3c55c0`

## Fix

Hardened `examples/bayesian_convergence.py` so it rejects malformed MrBayes
`.p` files, chains with different parameter headers, invalid burn-in fractions,
and excess arguments before computing ESS or PSRF. Previously the helper used
only the overlap of two headers, which could silently omit a parameter from a
misconfigured second run and produce a false convergence result.

## Validation

Exact-commit evidence: `F:/OpenScience/audits/bio-phylo-bayesian-inference/runs/exact-commit-4850b2c/`.

- 12/12 exact-commit checks passed.
- Focused executable suite: 10/10 passed, including real matching traces,
  explicit self-test, one-file rejection, header mismatch, malformed header,
  malformed row, invalid burn-in, and excess-argument rejection.
- `git diff --check HEAD^..HEAD` passed.

`quick_validate.py` rejects pre-existing shelf frontmatter keys (`author`,
`primary_tool`, `tool_type`); this pass did not alter those inherited keys.
