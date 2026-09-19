# bio-microbiome-qiime2-workflow fixes (2026-09-19)

Worktree `F:\OpenScience\wt\mb-qiime2`, branch `fix/mb-qiime2`, off fork `main`
(`F:\OpenScience\external\mrsonord2240__bioSkills`). Runtime: QIIME2 2024.10.1
(`qiime2-amplicon-2024.10`, WSL `science` distro) per
`F:\OpenScience\audit-envs\microbiome-metagenomics-analyst\TOOLS.md`. Fresh audit
(not re-audit), score 92/Production Ready, deployable, no P0/P1 — only the 2 P2s
below were open.

## Findings

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Phred-offset error described as "silently mis-decoded quality scores" in 3 places (Common Errors, Manifest-Phred failure-mode section, Quantitative Thresholds) when the audit's real `PairedEndFastqManifestPhred64V2`-on-Phred33-data run threw a hard `ValueError: Decoded Phred score is out of range [0, 62]` at import time | P2 | Reworded all 3 mentions to state the hard-crash outcome is at least as likely as the silent mis-decode, and name the exact `ValueError` text | docs: exact error string cross-checked byte-for-byte against `eval_viewer_bio-microbiome-qiime2-workflow.md` lines 101-102 (auditor's captured real QIIME2 output) | no code to re-run — prose-only fix; the auditor already produced the real error text this fix quotes |
| No explicit guard in SKILL.md against hand-editing a classifier `.qza`'s embedded `metadata.yaml` to bypass the scikit-learn version-pin check (audit Input 7, adversarial) | P2 | Added one sentence to the "Classifier / artifact version break across releases" failure-mode section naming the pinned pickled model object (not just the metadata string) as the real incompatibility, and reiterating retrain/redownload | matches audit recommendation's proposed fix text verbatim in intent | |

## Redundancy check

No SKILL.md/usage-guide.md duplication found worth collapsing. The audit itself
scored the split 11/12 ("Clean SKILL.md / usage-guide.md / examples/ separation");
usage-guide.md's Tips section restates points at human-prompt level rather than
duplicating agent-executable content, so left untouched per the brief's "do not
restructure" instruction for a P2-only pass.

## Unfixed

None. Both open P2s addressed.

Commit `3ca92d8` on `fix/mb-qiime2`.
