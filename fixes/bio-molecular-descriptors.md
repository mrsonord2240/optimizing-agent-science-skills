# bio-molecular-descriptors — fix pass (2026-09-24)

Worktree `F:\OpenScience\wt\bio-molecular-descriptors`, branch `fix/bio-molecular-descriptors`, based on staging `main` at `d4f4651`. Source commit: `77387c83238ced7d8e6bae147002918c0dd11116` (`Fix molecular descriptor 3D and chemistry boundaries`).

| finding | priority | change | verified |
|---|---|---|---|
| MMFF status `1` discarded every flexible 3D ensemble | P1 | 3D ensemble pattern now uses 2,000 iterations, excludes only individual non-converged conformers, and fails only when none converge | Atenolol 20/20 and verapamil 20/20 converged in the shared RDKit 2026.03.6 environment |
| MAP4 was claimed as a tested PyPI dependency though no distribution was obtainable | P1 | Removed the false version pin; documented MAP4 as an external source/platform validation boundary; constrained MHFP6 to NumPy 1.x | Exact-commit boundary assertions passed |
| Shipped 3D helper was unseeded | P1 | Added `random_seed=42` and `max_iters=2000`; `__main__` executes atenolol | Three runs produced asphericity `0.787643` identically |
| Gasteiger heavy-atom charges did not balance | P2 | Explicit-H helper sums all atom charges and verifies the formal-charge total | Aspirin: 21 charges, sum `-0.000000` |
| Metals returned misleading finite Gasteiger values | P2 | Conservative organic-element guard rejects unsupported atoms | `[Fe+2].[Fe+2]` raises a named `Fe` validation error |
| QED caveat reversed fragment behavior | P2 | Documents fragment over-ranking and natural-product/peptide under-ranking separately | Indole `0.544`; imatinib `0.389` |

All 6 authoritative findings are fixed. Exact-commit re-audit: **93/100, Production Ready, 31/31 assertions**. Evidence and refreshed report: `F:\OpenScience\audits\bio-molecular-descriptors\`.

No P0/P1/P2 remains. MAP4 needs the documented external source/platform validation if a future task requires it; this is intentionally not presented as a ready-to-run dependency.
