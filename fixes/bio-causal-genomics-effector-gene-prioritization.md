# Fix log: bio-causal-genomics-effector-gene-prioritization

2026-09-18

Source: `GPTomics/bioSkills@d91ed3d:causal-genomics/effector-gene-prioritization`.
Fixed on `fix/cg-egp` (worktree `F:\OpenScience\wt\cg-egp`), off staging `main` in
`F:\OpenScience\external\mrsonord2240__bioSkills`. Commit `f4755df` (local to that fork/branch,
not pushed/merged by this fixer per the brief).

Prior audit: `F:\optimizing-agent-science-skills\audits\skills\bio-causal-genomics-effector-gene-prioritization\GPTomics-bioSkills@d91ed3d\` (score 84, Limited Release, deployable, no veto).

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| No explicit research-only / clinical-boundary language | P1 | Added `## Scope` section to `SKILL.md`: effector-gene calls are population-level/hypothesis-generating, not individual clinical decisions; instructs redirecting patient-specific treatment questions to a clinician | Docs-only change; reviewed against the audit's Input 6 (PCSK9 inhibitor vs. statin) transcript to confirm the added language matches the correct behavior already observed | The audit's Input 6 output was already correct (base-model safety behavior); this closes the gap that `SKILL.md` itself gave the agent no instruction supporting that refusal |
| MAGMA gene-set enrichment (`--set-annot`) has an undocumented minimum-gene-count requirement | P1 | Added a note to the MAGMA pipeline section of `SKILL.md` and to `examples/magma_genebased.sh` (counts genes in `.genes.raw`, skips Step 3 automatically under 200 genes, prints why); added a `Common Errors` row | Ran / reproduced myself: real MAGMA v1.10 run on a fresh 3-gene synthetic locus (chr1 PCSK9 window, real 1000G EUR SNPs) failed Step 3 with `no input variables to analyse` (gene-set variance check fails first at this scale); this matches, and is caused by the same root issue as, the audit's own real 5-gene run which failed with `insufficient degrees of freedom to run analyses` (`audits/.../run/magma_geneset.log`, already on disk) | Both failure messages are cited in `SKILL.md` since the exact one MAGMA raises depends on gene count |
| Undocumented Windows filename mismatch between MAGMA output (`<prefix>.genes.out.txt`) and PoPS input (`<prefix>.genes.out`) | P1 | Added a note to the PoPS section of `SKILL.md` (cites `mendelian-randomization-analyst/TOOLS.md` as prior independent confirmation) and a `Common Errors` row; new `examples/pops_run.py` auto-renames before invoking `pops.py` | Ran real MAGMA -> PoPS end-to-end twice on a fresh 3-gene fixture: without the fix, `pops.py` raised `FileNotFoundError: ... 'toy_gene.genes.out'`; with the copy/rename, exit 0 and real `.preds`/`.coefs`/`.marginals` written (PCSK9 ranked correctly, though scores are non-discriminating at this toy scale, as already documented) | Also found and fixed the same bug independently inside `examples/magma_genebased.sh` itself: its own Bonferroni/top-50 steps read `.genes.out` directly and crashed on Windows before ever reaching PoPS -- not one of the 6 flagged findings, fixed inline under "fix, don't report" |
| `SKILL.md` dense/un-layered relative to its size (Algorithmic Taxonomy, Quantitative Thresholds, Per-Method Failure Modes all inline) | P1 | Split those three tables into `references/algorithmic-taxonomy.md`, `references/quantitative-thresholds.md`, `references/failure-modes.md`; `SKILL.md` now carries a short summary + pointer for each, matching the `references/` progressive-disclosure convention already used by `bio-alignment-multiple` and `bio-alignment-trimming` in the published shelf | Diffed old vs. new content by hand; every row/subsection preserved verbatim in its new file; `SKILL.md` still states the load-bearing summary inline (L2G+PoPS baseline, coloc PP.H4 >= 0.7, >= 3-of-6 concordance) so routine use doesn't require opening a reference file | Citations in the `## References` section were left in `SKILL.md` (unlike the alignment-multiple precedent) because nearly every citation is also used by sections that stayed in `SKILL.md` (Common Errors, Tool Install Notes, Reconciliation, Anticipated Reviewer Pushback) |
| Thin file-level modularity: 10+ tools described, only 2 runnable examples (MAGMA CLI, R concordance scoring); PoPS, Open Targets GraphQL, cS2G, ABC/ENCODE-rE2G prose-only | P1 | Added `examples/pops_run.py` (Windows-safe PoPS CLI wrapper, handles the filename-rename fix automatically) and `examples/opentargets_l2g_query.py` (dependency-free, stdlib-only live L2G GraphQL query) | Both actually executed. `pops_run.py`: real end-to-end run against real MAGMA output (see above). `opentargets_l2g_query.py`: three real live calls against `api.platform.opentargets.org` -- auto-discovery of a real GWAS-type `studyLocusId`, an explicit GWAS-type lookup (NFE2L3 score 0.7509), and an explicit QTL-type lookup correctly reporting no L2G predictions | cS2G and ABC/ENCODE-rE2G were left prose-only per FIX_BRIEF's "delete the claim" option is not applicable here (both are legitimately referenced with correct usage instructions, not fabricated), but writing runnable examples for them was out of scope for this dispatch (not flagged) and cS2G is a static Zenodo lookup / ABC-ENCODE-rE2G is explicitly cross-referenced to `atac-seq/enhancer-gene-linking`'s own examples, so it is not an unbacked claim |
| No bundled toy/test fixture data | P1 | Added `examples/toy_gwas_sumstats.tsv`, `examples/toy_gene_loc.txt`, `examples/toy_snp_loc.txt` (~1,800 real 1000G-EUR SNPs across 3 gene bins spanning the real PCSK9 locus, chr1:55.4-55.6Mb hg19; only the GWAS p-values are synthetic) plus `examples/make_toy_fixture.py` to regenerate/rescale | Ran the real Steps 1-2 MAGMA pipeline against the fixture (via the updated `examples/magma_genebased.sh`, fully executed end-to-end): 100% of SNPs annotated; PCSK9 correctly recovered as the top gene (Z=9.84, p=3.86e-23) against both null decoy bins | Fixture is intentionally requires a real 1000G EUR PLINK reference (as MAGMA always does; documented already) rather than shipping a synthetic LD reference, since a genuine smoke test of this pipeline needs real LD structure |

Redundancy pass (FIX_BRIEF's standing rule, not one of the 6 flagged items): `usage-guide.md`
trimmed to Overview / Prerequisites-pointer / Quick Start / Example Prompts / Related Skills.
Deleted passages and where their content now lives:
- `Prerequisites` list (inputs) -> moved verbatim into `SKILL.md`'s new `## Prerequisites` section.
- `eQTL / pQTL Panel Selection` table -> moved verbatim into `SKILL.md`'s `## Prerequisites` (agent-needed content that existed only in the guide).
- `Install` code block's MAGMA-download gotcha (redirect trap) -> merged into `SKILL.md`'s existing `## Tool Install Notes` MAGMA bullet (the rest of that block duplicated what `## Tool Install Notes` already said).
- `What the Agent Will Do` (9 steps) -> deleted; fully covered by `SKILL.md`'s Decision Tree, MAGMA/L2G/PoPS sections, Multi-Evidence Integration Framework, and Reconciliation table already.
- `Tips` (10 bullets) -> deleted; each restated a fact already in `SKILL.md` (nearest-gene 30-50%, >=3-of-6 concordance, L2G/PoPS orthogonality, tissue-first sequencing, MAGMA window choice, HLA exclusion, multi-effector loci, cS2G aggregator semantics, CRISPRi-FlowFISH as gold standard).

## Left unfixed

Nothing from the 6 flagged findings was left unfixed. Not attempted (explicitly out of this
dispatch's scope, not a flagged finding): runnable examples for cS2G lookup and ABC/ENCODE-rE2G
(cross-referenced to their own Skill, `atac-seq/enhancer-gene-linking`, which is where their
executables belong); LDSC-SEG / S-MultiXcan tissue-prioritization code path (not installed in
this shared env, and out of scope -- the audit itself scored Input 4 lower for the same reason
without treating it as a defect).

## Needs Sam

Nothing. The `references/` restructuring follows the sanctioned progressive-disclosure exception
in `FIX_BRIEF.md`, matched against the existing `bio-alignment-multiple` / `bio-alignment-trimming`
convention in `optimized-scientific-skills`.
