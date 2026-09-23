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

# 2026-09-21 fix pass (P2s from the 86-point re-audit, plus the split)

Worktree `F:\OpenScience\wt\alignment-pairwise-alignment`, branch `fix/alignment-pairwise-alignment` from staging main 431aa55. Commits: `9255f81` (fixes), `9d72c41` (split). Tools run: Biopython 1.88, Python 3.12 (Windows venv); WSL env `alignment`: EMBOSS 6.6.0, MMseqs2 18.8cc5c, HMMER 3.4, PAL2NAL 14, MAFFT 7.526; edlib 1.3.9. Data: audit `run\data` (HBA/HBB UniProt, 8 UniProt globins, human/cow/rabbit HBB CDS, HBB mammal CDS). Copied to a scratch dir, removed afterwards.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| SKILL.md 449 lines, no references/ split | P2 | 475 -> 299 lines (after the fixes below added 26). Six files in `references/` (see the move table); Reference Files index; three pointers appended to existing lines | ran: multiset of non-blank lines before/after: only 5 pointer/xref lines and added headings differ; every python/bash fence in SKILL.md and references/ parses (ast / `bash -n`) | Audit suggested moving Significance, Library Selection, When-NOT; also moved Substitution Matrix Selection, Percent Identity and export/substitution counts to reach 300. Gap-convention table and aligner recipes stay |
| Routed-to tools named without command lines | P2 | Added: `needle`/`water` block (Gap Penalties), PAL2NAL block with the empty-output-exit-0 trap (DNA vs Protein), `mmseqs easy-search --num-iterations 3` / `jackhmmer -N 3` / `hhsearch` block (When NOT appropriate) | ran: needle 11/1 = 286.0, water 11/1 = 288.0 on HBA vs HBB (equal to the log's Biopython numbers); needle default on DNA = EDNAFULL 10/0.5; MAFFT + pal2nal.pl human/cow HBB: 441 codon columns, re-translation equals the protein alignment; rabbit NM_001314043.1: exit 0, 0 bytes; mmseqs and jackhmmer on HBA vs 8 globins: HBB_HUMAN 115 bits, E 3e-34 (mmseqs), all 8 hit (jackhmmer) | `hhsearch` shown from `--help` only: it needs a downloaded HH-suite database that is not on this machine (a toy db would test the wrapper, not the claim). Block says so |
| DNA dinucleotide shuffle points at `ushuffle` (does not build) | P2 | `examples/empirical_pvalue.py`: pure-Python Altschul-Erickson `dinuc_shuffle`, `preserve='di'` (previously `NotImplementedError`); SKILL.md significance text updated | ran: 200 shuffles of a 444-nt CDS keep dinucleotide counts, first and last letter (200 distinct); uniform over all 3240 Eulerian paths of a 16-mer (300 draws each: chi2 3152, df 3239); protein alphabet works; `empirical_pvalue(..., preserve='di')` deterministic (seed 42), p 0.005 for human vs cow HBB CDS (score 885), p 0.48 for random DNA; mono example unchanged; py_compile | Replaces the "Missing referenced executables" gap by writing it |
| Strand bullet: "reverse complement 0" | P2 | "far lower ... median 18, never above 29 over 300 random pairs; palindromic or low-complexity queries score higher" | ran: 300 random 30-mers in 100-nt flanks, local 2/-1/-10/-0.5: forward 60 every time, reverse complement median 18, max 29 | The audit's median 17.5 / max 29 reproduced |
| "edlib returns edit distance only" | P2 | reworded: unit-cost edit-distance scoring only, `task='path'` returns alignment and CIGAR | ran: `edlib.align('ACGTACGT','ACGTTCGT', task='path')` gives distance 1, cigar `4=1X3=`, nice alignment | |
| Description omits trigger phrases | P2 | Needleman-Wunsch, Smith-Waterman, semiglobal, percent identity, reverse-complement strand, EMBOSS needle/water, BLAST scores added | n/a (text) | frontmatter `name` unchanged |

## Split: moved sections (verbatim) -> new home

| section in SKILL.md (pre-split) | now in |
|---|---|
| Pairwise Library Selection (table, caveats, parasail/edlib and pywfa/mappy snippets, `aligner.algorithm` note) | `references/library-selection.md` (with its 4 citations) |
| Substitution Matrix Selection, incl. Affine Gap Penalties: Biological Rationale | `references/substitution-matrices.md` |
| Percent Identity: Definitions Matter | `references/percent-identity.md` |
| Statistical Significance: Karlin-Altschul | `references/significance.md` (with its 4 citations) |
| When Alignment Is NOT Appropriate (incl. the new MMseqs2/jackhmmer/hhsearch block) | `references/when-not-appropriate.md` (with its 3 citations) |
| Substitution Matrix from Alignment; Export Alignment to Different Formats | `references/alignment-export.md` |
| References (11 citations) | distributed to the files that cite them; SKILL.md has no References section now |

Two moved lines changed wording, nothing else: percent-identity.md "the `counts()` method above" -> "(SKILL.md, Alignment Counts)"; substitution-matrices.md "see Gap Penalties" -> "see SKILL.md Gap Penalties". Pointers appended to three existing SKILL.md lines (Common mistake bullet, Protein Alignment config comment, Alignment Counts approach line).

## Redundancy pass

Already done 2026-09-19 (table above); usage-guide.md is overview, prompts and a pointer. No repeat found in the new text; skipped.

## Scripts step

No fenced block reaches 15 lines (largest: 14-line Accessing Alignment Data illustration, 12-line semiglobal pair, 11-line counts recipe, all API-shape snippets with user variables), so nothing moved to `scripts/`. The one substantial new code, `dinuc_shuffle`, lives in the existing `examples/empirical_pvalue.py`.

## Left unfixed

- `hhsearch` command not run (no HH-suite database on this machine; a download is tens of GB). Checked against `hhsearch -h` (`-i`, `-d`, `-o`); the block says so.

# 2026-09-21 final pass, phase 1 (fixer+auditor, same agent; see AUDITOR PHASE below for phase 2)

Worktree `F:\OpenScience\wt\alignment-pairwise-alignment`, branch `fix/alignment-pairwise-alignment`, at
9d72c41. Commit: `d45a647`. Env `alignment` (`F:\OpenScience\audit-envs\alignment\TOOLS.md`), no install
(everything used was already present). Data: audit `run/data` (HBA/HBB, 8 UniProt globins, HBB CDS
mammals), copied to `F:\OpenScience\scratch-pairwise-finalpass\` and removed afterwards.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| hhsearch line above ("checked against `--help` only, not run") was the one open item from the 2026-09-19 pass | P2 | built a toy HH-suite database from the 8 test globins (`hhmake`, `ffindex_build` x2, `cstranslate -f`, all present in WSL `bio`, no install) and ran `hhsearch -i query.a3m -d toydb -o query.hhr` as written | ran: HBA_HUMAN self-hit Prob 100.0/E 1.8e-93; other alpha globins 100.0 (E 4.6e-77, 6.4e-46); beta-globin orthologs 99.7 (E ~1e-25); myoglobins 96-97 (E ~1e-9) -- probability tracks phylogenetic distance | Resolves the item; text now points at a real database (`pdb70`/`uniclust30`) for actual use, not the toy one |

Also re-ran, with no change needed: every SKILL.md and `references/*.md` inline Python block (Required
Import through Iterating/`max_alignments`, `.substitutions`/export formats, substitution-matrix loads
and the NUC.4.4 `R,A==1.0` claim, `empirical_pvalue(preserve='di')`, parasail/edlib/pywfa/mappy in
library-selection.md), all 5 `examples/*.py` scripts, and the `needle`/`water`/MAFFT+PAL2NAL (both the
441-column success case and the rabbit exit-0/0-byte case)/MMseqs2/jackhmmer bash blocks on the audit's
real data. All values matched what SKILL.md and references already claim; nothing else needed a change.

## Left unfixed (this pass)

None. The single open item carried over from the prior pass (hhsearch) is resolved above.
