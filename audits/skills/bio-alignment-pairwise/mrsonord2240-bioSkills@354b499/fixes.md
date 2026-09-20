# bio-alignment-pairwise fix log (2026-09-19)

Skill `alignment/pairwise-alignment`, branch `fix/al-pairwise` (worktree `F:\OpenScience\wt\al-pairwise`, from staging main 354b499), commit 9c811ae. Fixer only; not scored.

Tool versions run: Biopython 1.88, Python 3.12 (Windows venv); parasail 1.3.4, edlib 1.3.9.post1; WSL env `alignment`: pywfa 0.5.1, mappy 2.31, EMBOSS 6.6.0 (`water`, `needle`), BLAST+ 2.17.0; R 4.4.3 with pwalign 1.2.0 and Biostrings 2.74.1. Data: audit `run\data` (HBA/HBB UniProt, HBB CDS), all other data synthetic and labelled in the run.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| `aligner.max_alignments` raises AttributeError | P1 | SKILL.md "Iterating" rewritten around `itertools.islice`; OverflowError explained; Common Errors row fixed; usage-guide mention deleted | ran: attribute assignment raises AttributeError; `islice(alignments, 5)` works; the 5-block iteration snippet executed from SKILL.md | OverflowError reproduces only with zero gap penalties on repetitive input (auditor's case); wording says so |
| "Default gaps are 0" false | P1 | section rewritten: defaults are match 1 / mismatch 0 / gaps -1/-1 (`print(aligner)`); always set gaps | ran: `print(PairwiseAligner())`; HBA vs HBB BLOSUM62 default gaps -> 55 gap positions in 37 blocks, -11/-1 -> 9 in 5 | Replaces the auditor's "gaps cost nothing" mechanism with the measured fragmentation |
| "BLASTP defaults -11/-1" off by one | P1 | convention table (Biopython/EMBOSS/parasail vs BLAST/pwalign), conversion rule, BLASTP = -12/-1; Protein config comment; Affine section text | ran: `blastp -comp_based_stats 0` raw 285, HSP q3-141; `water` 11/1 = 288, 12/1 = 285; `needle` 11/1 = 286; Biopython local -12/-1 285, -11/-1 288, global -11/-1 286; pwalign local gapOpening 11/1 285, 10/1 288, global 10/1 286 | Two independent methods per number (EMBOSS and BLAST, plus pwalign). BLASTP default (comp-based stats on) reports 286, noted |
| Output block wrong | P2 | replaced with printed output; the block now sets its aligner explicitly (it used whichever aligner the previous block left) | ran: block executed from SKILL.md, prints `\|\|\|\|.\|\|\|\|\|.\|\|` | `len(alignments)` print removed from that block (see Iterating) |
| Semiglobal snippet: order, deprecated names, no scoring | P2 | complete runnable examples, `end_gap_score` first, one-sided form uses `open/extend_left/right_deletion_score`, argument order stated, old names mentioned | ran: 40.0 and `[[300, 320]]`; swapped order -279; block runs with warnings as errors | Old names accepted on 1.88 with DeprecationWarning; the version that introduced the new names was not determined |
| No off-spec input guidance | P2 | new "Input Checks" section | ran each: lowercase/newline/J/U/empty -> ValueError, `*`/X/B/Z/SeqRecord accepted, match-mismatch aligner treats lowercase and U as mismatches, reverse complement 0 vs 60, rabbit HBB2 CDS (NM_001314043.1) flagged by the internal-stop expression, the 6 others not | PAL2NAL empty-output-on-inconsistency is from the tooling notes (`TOOLS.md` note 12), not re-run |
| parasail/edlib table has no code, no saturation warning, unrealistic speeds | P2 | measured speedups replace literature ranges; saturation warning with `_sat` variants; snippets for parasail, edlib, pywfa, mappy; edlib alphabet "DNA only" -> "any alphabet" | ran: parasail `nw_striped_sat` 7003 == Biopython 7003 (4 kb); 16-bit returns 0 with `.saturated` on 20 kb, `_sat` 35565 == Biopython; edlib 118 == -Levenshtein 118; edlib protein distance 3 == 3; pywfa -802 == Biopython -802; mappy locus 3502 (planted 3500, mapq 60); SKILL.md snippets executed by extraction | Speeds measured on Windows: 300 nt x1000: parasail 1.9x (`striped_sat`) to 3.9x (`scan_sat`), auditor 5-11x with fixed 16-bit; edlib 15x vs Levenshtein, 26x vs affine; 20 kb: parasail 3-8x, edlib 415x-625x here (1356x in audit). Ranges quoted accordingly; timings vary |
| R bullet outdated, convention unmapped | P2 | bullet now `pwalign::pairwiseAlignment()` with the gap convention mapped in the Gap Penalties section | ran: pwalign 1.2.0 scores listed above | Exact Bioconductor release of the move not checked; text says "Bioc 3.20 moved it" (checked there) |
| `alignment_from_file.py` needs unshipped FASTA | P2 | script takes argv[1]; small `examples/sequences.fasta` shipped | ran: prints score 26.0 and alignment | |
| Affine-vs-linear demo prints equal scores | P2 | demo uses a pair with a 3-residue deletion | ran: affine 86.0 vs linear 84.0; parasail 86 / 84 | |
| Doc drift, Version banner "1.83+" untested | P2 | banner now "Checked on Biopython 1.88" with cross-check tool versions | see above | |

## Redundancy pass (dedup)

| deleted passage | where the content lives now |
|---|---|
| usage-guide "Prerequisites" (`pip install biopython`) | SKILL.md Version Compatibility |
| usage-guide "What the Agent Will Do" (6 steps) | SKILL.md Creating an Aligner / Performing Alignments / Alignment Counts |
| usage-guide "Supported Alignment Modes" table | SKILL.md Core Concepts / Choosing the Right Mode |
| usage-guide "Tips" (11 bullets: DNA/protein scoring, local mode, affine gaps, twilight zone, PID definitions, significance, MMseqs2 for databases, `max_alignments`) | SKILL.md Common Scoring Configurations, Substitution Matrix Selection, Statistical Significance, When Alignment Is NOT Appropriate, Percent Identity; the `max_alignments` bullet was wrong and is deleted |
| SKILL.md failure-mode bullet "NUC.4.4 IUPAC partial matches" | merged into the DNA matrices line in Substitution Matrix Selection |
| SKILL.md `len(alignments)` print in Performing Alignments | replaced by the Iterating section (single home for the count/OverflowError note) |

usage-guide.md now has Overview, Quick Start prompts, Example Prompts and a pointer to SKILL.md. Nothing the agent needs left the Skill.
Disagreements between copies: usage-guide "set `max_alignments`" vs the run (attribute absent) -> the run wins, deleted.

## Left unfixed

- `examples/empirical_pvalue.py` and `examples/*.py` keep protein gaps -11/-1 (EMBOSS 11/1). They never claim to be BLASTP-equivalent, so no defect; the SKILL.md comment says so.
- `examples/local_alignment.py` still prints `len(alignments)`; it works on its input (1 alignment) and the Iterating section covers the failure case.
- pywfa/mappy snippets were run in WSL only (no Windows builds).
