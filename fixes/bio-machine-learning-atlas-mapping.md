# bio-machine-learning-atlas-mapping fix pass - 2026-10-03

The unknown-cell gate does not catch a missing cell type that is adjacent to a reference type: with monocytes removed from the reference, 96% of query monocytes were confidently labelled dendritic cells and under 3% were gated. No latent-space gate in scope fixed this, so the limitation is now stated with measured numbers, and a required curated-marker check (`scripts/label_marker_check.py`) flags the mislabelled group in both hold-outs and nothing at baseline; labels it cannot check are reported as unverified, never as a pass. The annotation script is seeded and writes its output, `predict(soft=True)` is documented as a DataFrame, snippets define what they use, and methods that were not run are labelled. Later text-only passes reduced the frontmatter description to a trigger that separates it from reference-based cell annotation.

- Final candidate audit: `audits/skills/bio-machine-learning-atlas-mapping/candidate@a579d86464c9-reaudit-delta3-20261003`
- Result: **87/100, Production Ready**; open P2 AM-008 (the marker check crashes when no label is checkable).
- Candidate identity: `a579d86464c9fd84579b6645107d0f6c72b87f091da33839966cc6b08c8a75ef`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
