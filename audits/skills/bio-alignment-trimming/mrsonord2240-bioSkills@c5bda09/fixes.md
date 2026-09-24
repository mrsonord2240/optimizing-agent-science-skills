# bio-alignment-trimming fixes (2026-09-15)

Worktree `F:\OpenScience\external\bioSkills-wt-phylo`, branch `fix/phylogenetics`. Runtime: ClipKIT 2.14.0, IQ-TREE 2.4.0, trimAl 1.4.1, BMGE 1.12 and 2.0 jars, MACSE 2.07, PAML 4.10.10, PhyIN v1.0. Data: audit synthetic sets (reps x10, prot15, unbal33, deep16 supermatrix, dna_super locus, cds10 MACSE-like).

## Verification re-run of the ClipKIT default (scratchpad `trim/`)

| dataset | mode | retention | RF to truth | wRF | notes |
|---|---|---|---|---|---|
| 10 replicate genes (mean) | untrimmed | 100% | 0 total | 0.852 | |
| | smart-gap | 75.4% | 0 total | 0.811 | 0/10 over 40% removed |
| | kpic-smart-gap | 51.9% | 0 total | 1.046 | 10/10 over 40% removed |
| | kpi-smart-gap | 35.0% | 2 total | 2.859 | |
| prot15 | smart-gap / kpic-smart-gap / kpi | 82.1% / 58.1% / 44.1% | 0 / 0 / 0 | 0.895 / 1.161 / 2.545 | kpi tree length 6.74 vs 4.74 untrimmed |
| deep16 supermatrix | smart-gap / kpic-smart-gap | 75.8% / 49.4% | 0 / 0 | 2.128 / 2.172 | |
| unbal33 (30 + 3 outgroups) | untrimmed / smart-gap / kpic-smart-gap | 100% / 96.1% / 72.3% | 30 / 30 / 28 | 0.206 / 0.204 / 1.757 | stem 0.44 / 0.44 / 1.20 (true 0.44); Out3 pendant 0.33 / 0.33 / 0.00 |

## Findings

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Default `kpic-smart-gap` breaks own 40%/0.7 rule; distorts outgroup branch lengths; kpi inflates lengths | P1 | `smart-gap` default for single genes and supermatrices; `kpic-smart-gap` topology-only, balanced data, mandatory branch-length check, not for dating/rates/rooting; kpi parsimony-only | ran (table above) | method change backed by the audit runs and this re-run |
| Inconsistent 20%/20-30%/40%/0.7 thresholds | P1 | One rule (>40% removed = too aggressive) scoped to gap/entropy trimming; kpi/kpic judged by trees + branch lengths; SKILL.md, usage-guide, `clipkit_trim.py` aligned | ran: `clipkit_trim.py` on prot15 (82.1%) | |
| `--output-format` | P1 | `-of phylip` | ran | |
| BMGE 2.0 silently no output; `-h 0.4` recommendation | P1 | 1.12 and 2.0 syntax + defaults table, `test -s`; `bmge_trim.py` version switch + output check; default threshold with deep-matrix warning | ran: both jars, AA and DNA; guard raised on 1.12 flags with 2.0 jar | |
| Gblocks `-b1=50% -b2=85%` | P1 | Integer counts, rule, N = 20 example | docs (Gblocks documentation) | no Windows binary |
| PhyIN flags | P1 | `python phyin.py -input -output -b 10 -d 2 -p 0.5`, DNA only | ran (891 -> 826 sites) | |
| HMMcleaner `--no-large-remove` | P1 | removed | docs (HmmCleaner.pl POD) | |
| TCS `+keep` (residues) and `-evaluate` stdout redirect | P1 | `-mode evaluate -output score_ascii` -> `aligned.score_ascii`; `+use_cons +keep '[5-9]'` | docs (T-Coffee manual) | no Windows T-Coffee |
| codeml reads `!` as missing | P1 | codeml 4.10.10 rejects `!` (exits 0); replace before every run; Common Errors row | ran | |
| MACSE export leaves `!` | P1 | `-codonForInternalFS --- -charForRemainingFS -`; sed restricted to sequence lines | ran: 0 `!` left; sed leaves headers alone | |
| ClipKIT issue #71/#88 citations; Steenwyk "consistently better trees"; Tan-vs-Steenwyk reconciliation | P2 | Removed; kept only the ClipKIT reference and the Tan 2015 finding as titled; kpic text = help-documented behaviour + simulated result | ClipKIT help; ClipKIT source has no sequence weighting; BMGE 2.0 help for `-w` | |
| Trimming a concatenation breaks charsets | P2 | Per-locus trimming note, Common Errors row | audit Input 2 run | |
| `--log` / `-colnumbering` formats | P2 | Real formats + two-line parsers | ran both parsers | |
| `-strictplus` for ML input | P2 | NJ-oriented per trimAl help; `-gappyout`/`-strict` for ML; stale trimAl 2.0 pin note removed | trimAl 1.4.1 help; audit replicates | |

## Unfixed

- Split tool-specific detail into `references/` (P2): restructuring, out of scope for a correction pass.
- `trimal_modes.py` docstring "~50% more aggressive than strict" and Divvier `.partial.fas` suffix: not flagged as defects, not verifiable here, left as is.

## Backlog pass — 2026-09-15

Worktree `F:\OpenScience\external\bioSkills-wt-p1`, branch `fix/backlog-p1`. Runtime: trimAl v1.4.rev15 (build 2013-12-17, matches SKILL.md's documented 1.4.1) at `audit-envs\molecular-phylogenetics-analyst\tools\trimal_v1.4.1\trimal.exe`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Caution on trimAl sequence-overlap thresholds (Input 9) | P2 | New "trimAl Sequence-Overlap Filtering" subsection in SKILL.md: thresholds are dataset-dependent, runnable diff recipe to list removed headers, relax `-seqoverlap` if a full-length sequence is among those dropped | ran: reproduced audit's own Input 9 data (its `make_frag.py` on `prot15_linsi.fasta`, P04/P10 truncated to fragments); `-resoverlap 0.8 -seqoverlap 75` dropped P04 P10 P12 P14 (4/15, matches audit exactly); stdout showed only all-gap-column warnings, no removed-sequence report; the doc's diff recipe correctly named all 4 dropped headers; `-seqoverlap 60` on the same data dropped only P04/P10, keeping P12/P14 | commit 3fa0caa |
| Remove remaining mixed messages: BMGE BLOSUM default stated flat, contradicting the version table; trimAl `-automated1` recommended for "publication-grade" in 3 places with no caveat, contradicting the doc's own "not for audit-grade reproducibility" note | P2 | Goal-Driven table row (BMGE) now says "Substitution-matrix entropy (BLOSUM62 in 1.12, BLOSUM30 in 2.0)"; Goal-Driven intro, Decision Tree single-gene branch, and the Column Mapping for Reproducibility example command now either caveat `-automated1` against audit-grade use or swap to an explicit mode (`-gappyout`), matching the pre-existing Reproducibility note | ran: `java -jar BMGE112.jar -?` shows `-m BLOSUM<n> ... default: BLOSUM62`; `java -jar BMGE200.jar -h` shows `-m BLOSUM<int> ... default: BLOSUM30` (JDK 17, both jars in `audit-envs/molecular-phylogenetics-analyst/tools/`) | commit b2ef9fc |
| Move tool-specific detail to references/ (330-line SKILL.md loaded TCS/MACSE/PhyIN/Gblocks/HMMcleaner detail for every request) | P2 | New `references/specialist-trimmers.md` (HMMcleaner, Gblocks, PhyIN, moved verbatim) and `references/selection-analysis-workflow.md` (TCS, MACSE, moved verbatim) -- first use of a `references/` dir in this repo. SKILL.md keeps ClipKIT/trimAl/BMGE/Divvier, the decision tree, 20%/40% rule, Common Errors and Related Skills/References, with a one-paragraph pointer to each new file in place of the moved sections. SKILL.md 344 -> 278 lines | verified by substring match: all 5 moved sections confirmed byte-for-byte present in the new files against the pre-edit SKILL.md (git show b2ef9fc); code-fence count 28 before = 18+6+4 after, none lost or orphaned | commit 3e9cdba |

All 15 findings in this backlog slice are now fixed (6 by the orchestrator, 6 by sibling sub-agents, 3 -- findings 13/14/15, all on this Skill -- by this lineage of sub-agents). Slice complete.

## Exact-commit schema re-audit — 2026-09-24

| finding | priority | change | verification | commit |
|---|---|---|---|---|
| Top-level `tool_type`, `primary_tool`, and `author` fail the current canonical skill-frontmatter schema | P1 | Preserved all three values under the supported `metadata` mapping | `quick_validate.py` PASS; source diff check PASS; focused 9-input command replay and shipped-example checks PASS | `c5bda09627a2d9f0bfc2222bfcef06249772f0a2` |

The exact-SHA re-audit is 96/100 with 30/30 assertions. It also rechecked the prior P2 overlap repair: `-seqoverlap 75` identifies P04/P10/P12/P14 through the documented header diff, while relaxing to 50 preserves P12/P14 and removes only the two fragment records.
