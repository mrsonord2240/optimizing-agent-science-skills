# Handoff: ca-bio-pathway-go-enrichment / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Lane: n/a (context-aware recut batch)
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-pathway-go-enrichment` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-pathway-go-enrichment`
- Branch/worktree: records repo working tree; no git writes made
- Candidate identity (preflight `--shape`, PASS): `dcc4851f835427a0105c42c35cd22a0beafb58b9916ada11868e492cdb77f7ad`, 13 files
- Applicable audit: none
- Warn carried: no Skill-root LICENSE (the shelf had none; frontmatter `license: MIT`, `author: GPTomics` kept).

## Structural summary

- SKILL.md 36 lines, 7 routes (ora, de-table, length-bias, custom-sets, groupgo, other-skills, errors). references/background.md, citations.md. Dropped: usage-guide.md, the two toy example scripts (replaced by ora_go.R), taxonomy/threshold essays (to background).

## Scripts written

scripts/ora_go.R (enrichGO/enricher; foreground+universe files or a DE table), scripts/goseq_ora.R (the pinned hg38 GOseq recipe), scripts/groupgo.R. All unexecuted after the recut (shelf scripts copied unchanged keep whatever shelf execution evidence they had).

## Open ambiguities for audit

- Version: source says clusterProfiler 4.18.4+, org.Hs.eg.db 3.22+ while the GOseq recipe pins Bioconductor 3.20 (goseq 1.58.0, org.Hs.eg.db 3.20.0). Mixed releases left as in the source; not reconciled.
- ora_go.R defaults `simplify=true` (cutoff 0.7, Wang) because the source recommended it and its all-ontology example used it; the source's bare enrichGO call did not simplify.
- ora_go.R in `de=` mode uses padj<0.05 and |log2FoldChange|>1 (the source's example cutoffs) as defaults.
- Idea for audit: stop when the foreground is not a subset of the universe; enrichGO intersects silently.

## Worktree safety

- Run-owned: `skills\ca-bio-pathway-go-enrichment\`, this handoff, one row in `skills\README.md`.
- Pre-existing/user-owned: `test/validate.bats` untouched; sibling `skills/ca-*` folders of the other worker untouched.
- Product commits/pushes: none. Tooling impact: none.

## Transition assertion

- Next-phase prerequisites met: yes.
