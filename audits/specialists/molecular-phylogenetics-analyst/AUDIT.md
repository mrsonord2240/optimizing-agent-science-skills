# molecular-phylogenetics-analyst — audit

## Re-audit of the fixed Skills (2026-09-15)

Source: `mrsonord2240/bioSkills@966f838b0ba32918310bd223a34f71d78f190560` (branch `openscience-fixes`). This section
replaces the pre-fix verdict (archived reports: `audits/_pre-fix-20260915/`). Each fixed Skill was re-run on its 7 pre-fix
inputs as regression tests plus 2 new inputs (N = 9). `bio-alignment-multiple` is byte-identical between `d91ed3d` and
`966f838` (`git diff` empty); its 85 report was reused and only its `source` string updated. No sub-agents; core Skills first.
All data synthetic, simulated from known trees.

### Scores, pre-fix → post-fix
- bio-alignment-multiple: 85 ⭐ → 85 ⭐ (unchanged bytes, report reused)
- bio-phylo-modern-tree-inference: 86 ⭐ → 88 ⭐
- bio-alignment-trimming: 75 ⚠️ Beta (assertion floor) → 83 ✅
- bio-phylo-bayesian-inference: 84 ⚠️ Beta (assertion floor) → 87 ⭐
- bio-phylo-species-trees: 82 ⚠️ Beta (assertion floor) → 86 ⭐
- bio-phylo-divergence-dating: 83 ✅ → 87 ⭐
- bio-phylo-distance-calculations: 82 ⚠️ Beta (assertion floor) → 87 ⭐
- bio-phylo-tree-manipulation: 80 ✅ → 86 ⭐
- bio-phylo-tree-io: 84 ⚠️ Beta (assertion floor) → 88 ⭐
- bio-phylo-tree-visualization: 78 ⚠️ Beta (assertion floor) → 84 ✅

### Audited Skills
| Skill ID | Role | Category | Mode | N | Executed | Static | Exec avg | Final | Grade | Veto | Top open issue |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bio-alignment-multiple | core | Data Analysis | A | 7 | 7/7 | 80 | 89.0 | 85 | ⭐ Production Ready | none | see its report (reused) |
| bio-phylo-modern-tree-inference | core | Data Analysis | A | 9 | 8/9 | 86 | 88.6 | 88 | ⭐ Production Ready | none | P2 false `--alrt`/`-bb`/`-nt` warnings |
| bio-phylo-bayesian-inference | core | Data Analysis | A | 9 | 8/9 | 86 | 87.2 | 87 | ⭐ Production Ready | none | P2 example self-tests on a single .p file |
| bio-phylo-species-trees | core | Data Analysis | A | 9 | 9/9 | 85 | 87.0 | 86 | ⭐ Production Ready | none | P2 no leaf-name consistency check |
| bio-alignment-trimming | supporting | Data Analysis | A | 9 | 9/9 | 80 | 85.0 | 83 | ✅ Limited Release | none | P2 trimAl overlap filter drops full-length sequences |
| bio-phylo-divergence-dating | supporting | Data Analysis | A | 9 | 8/9 | 87 | 87.2 | 87 | ⭐ Production Ready | none | P2 no root-to-tip / randomization code |
| bio-phylo-distance-calculations | supporting | Data Analysis | A | 9 | 9/9 | 86 | 87.3 | 87 | ⭐ Production Ready | none | P2 no alpha-estimation / gap-strip code |
| bio-phylo-tree-manipulation | supporting | Data Analysis | A | 9 | 8/9 | 86 | 86.3 | 86 | ⭐ Production Ready | none | P2 outgroup code skips ingroup monophyly |
| bio-phylo-tree-io | supporting | Data Analysis | A | 9 | 9/9 | 86 | 88.6 | 88 | ⭐ Production Ready | none | P2 stale "truncates or chokes" sentence |
| bio-phylo-tree-visualization | supporting | Data Analysis | A | 9 | 9/9 | 84 | 83.1 | 84 | ✅ Limited Release | none | **P1** colour recipe on unrooted tree colours the wrong clade |

Inputs executed: 84 of 88 (the 4 not executed are routing answers). No P0 anywhere.

### Read but not chosen
No other Skill in `alignment`, `phylogenetics` or `sequence-io` was re-audited this round; the pre-fix selection stands.

### Verdict: VIABLE
- **Gate 2 (every bundled Skill audited, deployable):** PASS. 10/10 deployable, no veto, no P0, all ≥ 83.
- **Gate 3 (core ≥ 85):** PASS. alignment-multiple 85, modern-tree-inference 88, bayesian-inference 87, species-trees 86.
- **Gate 4 (≥ 3 core covering framing, central step, validation/reporting):** PASS. Framing: alignment strategy and
  ModelFinder model selection. Central step: ML, Bayesian and coalescent species trees. Validation: joint SH-aLRT/UFBoot rule,
  concordance factors, MCMC convergence gates, stepping-stone model comparison. Reporting is supported by tree-io and
  tree-visualization.
- **Gate 7 (research scope):** PASS. No output concerns an individual.
- **Gate 8 (shipped means present):** PASS. No Skill points at missing `references/`, `scripts/` or `templates/`; every
  example runs or passes compile checks.

Caveats for the builder: alignment-multiple sits exactly at the core bar (85). tree-visualization has an open P1: rooting
must happen before colouring clades. IQ-TREE 3 and RAxML-NG were not run on this machine (IQ-TREE 2.4.0 was), and BEAST 2
was not re-run (dating Input 4 reused the pre-fix MCC trees).
