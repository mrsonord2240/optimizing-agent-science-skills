> **Audit record for `bio-phylo-tree-visualization`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@4cc2487](https://github.com/mrsonord2240/bioSkills/tree/4cc2487c5f22541d9891e00ae9705793fd0135f8/phylogenetics/tree-visualization) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-phylo-tree-visualization (re-audit of the fixed Skill, round 3)
Generated: 2026-09-19 · Re-auditor: independent (fresh Sonnet), not the fixer · skill-auditor@1.0

Source: `mrsonord2240/bioSkills@4cc2487c5f22541d9891e00ae9705793fd0135f8:phylogenetics/tree-visualization`
Prior: 78 (pre-fix) -> 84 (Limited Release, ran against commit 966f838, which predates the
Backlog-pass fixes fa75880/00141d5/0f50878 that the 84-score audit's BACKLOG.md had
stale-listed as still open). This pass audits HEAD after those three fixes plus the new
fail-loud MRCA guard (4cc2487). Data Analysis · Mode A · N = 9 (all 9 of the 84-score
report's inputs re-run as regression; Inputs 2 and 5 rebuilt from scratch as direct
fix-verification rather than reusing prior auditor scripts). All data SYNTHETIC or public
reference fixtures (data/, reused from the prior audit).

## Static: 87/100 (prior 84)
Functional 11 · Reliability 11 · Performance 7 · Agent usability 14 · Human 6 · Security 11 · Maintainability 9 · Agent-specific 18. Gate 8 (shipped-means-present) PASS — all three examples (`ascii_tree.py`, `basic_tree_plot.py`, `labeled_tree.py`) run end to end.

## Summary
| Input | Type | Basic | Spec. | Total | Assertions | Executed |
|---|---|---|---|---|---|---|
| 1 | Canonical (regr.) | 38 | 57 | 95 | 5/5 | yes |
| 2 | Variant A — **fix verification** | 39 | 59 | 98 | 4/4 | yes |
| 3 | Edge (regr.) | 33 | 47 | 80 | 4/5 | yes |
| 4 | Variant B (regr.) | 34 | 50 | 84 | 3/4 | yes |
| 5 | Stress — **fix verification** | 38 | 57 | 95 | 5/5 | yes |
| 6 | Scope Boundary (regr.) | 34 | 48 | 82 | 3/4 | yes |
| 7 | Adversarial (regr.) | 33 | 46 | 79 | 3/4 | yes |
| 8 | Variant B (regr.) | 36 | 51 | 87 | 5/5 | yes |
| 9 | Edge (regr., corrected methodology) | 37 | 53 | 90 | 4/4 | yes |

**Execution average 87.8** · assertions 36/40 (90%). Research Veto PASS.
**Final: 87 × 0.4 + 87.8 × 0.6 = 34.8 + 52.7 = 88 → ⭐ Production Ready.**

## The fix, verified directly (Input 2)

`runs_v3/in2/in2_mrca_failloud.py` on the real `data/iq/primates16.treefile` (16-tip
primate tree, unrooted-as-stored, IQ-TREE SH-aLRT/UFBoot support):

- **Path A (bug reproduction, no rooting):** `common_ancestor(Homo_sapiens, Pongo_abelii)`
  on the raw parsed tree returns **all 16 tips** — the intended clade is 5 tips
  (Homo/Pan_troglodytes/Pan_paniscus/Gorilla/Pongo). This is *worse* than the 84-score
  audit's own finding (14/16, via a different, still-unrooted call), which makes the
  guard more consequential, not less. `ValueError` **raised**, exactly as designed.
- **Path B (the actual recipe: root_with_outgroup first):** MRCA returns **exactly the
  intended 5 tips**, no raise, clade coloured red.

Both directions verified by execution, not by reading the diff.

## The two "already correct" claims, independently reverified

**gheatmap** (`runs_v3/in8/in8_gheatmap.R`): plain `gheatmap(ggtree(tr), df)` → OK.
Composite (`geom_tippoint` + `new_scale_fill()` + `gheatmap`) →
`` `new_geom_point_g_gtree()` requires the following missing aesthetics: x `` — the exact
string quoted in the Version Compatibility block. `geom_fruit` fallback on the same
composite case → OK.

**ggtree rich-figure recipe** (`runs_v3/in5/in5_ggtree_recipe.R`): the SKILL.md
`## ggtree + treeio Recipe (R)` section run **verbatim** (only the file path and outgroup
names adapted) against the real primates16 IQ-TREE output: `read.iqtree` → `root_keep`
(`treeio::root(edgelabel=TRUE)` + index-based tip-label restore) → `geom_nodelab` dual
support → `geom_fruit` metadata ring. `ggplot_build` succeeds (7 layers), `ggsave` writes
a 6507-byte PDF, tip labels restore correctly (no leftover numeric labels), 13/13 internal
nodes carry non-NA UFboot after rooting, and `groupOTU` + `aes(color=grp)` produces 2
distinct segment colours confirming the stem-colouring caveat the Skill states.

## A methodology trap this auditor caught in its own testing

First pass on Input 6/8's layout claims used `ggplot_build()` only and got a **false
negative** — every layout including `daylight`/`equal_angle`/`slanted`/`ape` reported "OK".
Escalating to a full `ggsave()` render reproduced the documented
`` could not find function "is.waive" `` error exactly, because that error only fires at
the geom-to-grob conversion stage, not at `ggplot_build`. The Version Compatibility block
is accurate, not stale — but it is a reminder that `ggplot_build()` alone is not sufficient
evidence for ggtree rendering claims. Similarly, Input 9's first bipartition check used a
naive tip-set string comparison that produced false mismatches under rerooting (a split's
descendant tip-set can flip to its complement); corrected by canonicalising each
bipartition against a fixed reference tip. Both corrections are recorded in
`runs_v3/in8/in8_layouts_render.R` and `runs_v3/in4679/in9_fixed.R`.

## Regressions confirmed unchanged / still open
- Input 3: Bio.Phylo panel at 320 tips is still not legible even with the height cap — an
  inherent tool ceiling the Skill already routes around (P2, not new).
- Input 4: HPD centring code runs without error on both `center=` values; the exact Ma
  offset was not independently re-derived this pass (auditor extraction issue, not a Skill
  defect) — relying on the 2026-09-15 fix pass's number (auto 4.95 Ma error, height 0.00).
- Input 7: caption-visibility issue from the 84-score audit was not re-tested this pass
  (it was an artifact of the auditor's own figure code, not the Skill, previously).

## usage-guide.md redundancy check
Re-verified independently: `usage-guide.md` (65 lines) contains overview, prerequisites,
example prompts, "what the agent will do", and tips — no duplication of SKILL.md's recipes
or reference tables. The fix log's claim that this was already clean holds.

## Recommendations
[P2] reconcile fail-loud vs print-only severity between the MRCA guard and the
"no readable support" warning (Inputs 1, 2) · [P2] Bio.Phylo panel legibility ceiling near
300+ tips (Input 3) · [P2] give the ape unrooted fallback a full code recipe with a scale
bar (Input 6).
