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
