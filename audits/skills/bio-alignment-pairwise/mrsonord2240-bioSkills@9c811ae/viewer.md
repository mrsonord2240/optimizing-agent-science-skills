> **Audit record for `bio-alignment-pairwise`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@9c811ae](https://github.com/mrsonord2240/bioSkills/tree/9c811aed171970a7188fa0a62396373dfd9a428d/alignment/pairwise-alignment) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-alignment-pairwise (re-audit of the fixed Skill)

Generated: 2026-09-19 | Source: `mrsonord2240/bioSkills@9c811aed171970a7188fa0a62396373dfd9a428d:alignment/pairwise-alignment` | Pre-fix: 80 (Limited Release, `_pre-fix-20260919d`)
Category: Data Analysis (3) | Mode: A (the agent writes code from the Skill's patterns; the 5 `examples/` are templates) | Complexity: Complex -> 7 regression inputs + 2 NEW = N 9

The Skill was read from a byte-identical copy in `run\skill\` (`diff -r` against the worktree: identical; no `__pycache__` in the worktree, the clone or the copy). Every script and log is in `run\` and `run\logs\`. Ground truth was independent of the Skill: an own pure-Python Gotoh DP (`ref_gotoh.py`), EMBOSS needle/water, BLAST+ blastp `-comp_based_stats 0`, pwalign (R), parasail, edlib, pywfa, mappy, MMseqs2, PAL2NAL, planted coordinates. Synthetic data is labelled SYNTHETIC in the scripts; real data is UniProt globins, RefSeq HBB CDS and PDB SEQRES from `audit-envs\alignment\public-data`. The fix log was read but not used as evidence.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical - [regression] Global BLOSUM62 alignment of real human HBA vs HBB with the Skill's gap-convention section | 36 | 55 | 91 | 5/5 PASS | OK |
| 2 | Variant A - [regression] Local DNA alignment of a mutated real HBB segment inside a 1.15 kb synthetic sequence, plus strand recovery | 35 | 54 | 89 | 4/4 PASS | OK |
| 3 | Edge - [regression] Semiglobal fragment placement, length mismatch, and every 'Input Checks' bullet | 35 | 53 | 88 | 4/5 PASS | OK |
| 4 | Variant B - [regression] Is HBA/HBB significant? Empirical p-values with the Skill's own example on related, distant and unrelated real pairs | 35 | 53 | 88 | 4/4 PASS | OK |
| 5 | Stress - [regression] Library-selection table re-measured: parasail, edlib, pywfa, mappy on long synthetic DNA, saturation, every Skill snippet | 36 | 54 | 90 | 5/5 PASS | OK |
| 6 | Scope Boundary - [regression] Human vs cow HBB CDS for dN/dS (protein first, back-translate), the internal-stop trap, and a many-vs-many request | 33 | 48 | 81 | 4/5 PASS | OK |
| 7 | Adversarial - [regression] pairwise2, aligner.max_alignments, EMBOSS-style percent identity, IUPAC DNA, algorithm names, R, printed output block | 36 | 54 | 90 | 5/5 PASS | OK |
| 8 | Variant B - [NEW] PKA (1ATP) vs CDK2 (1HCK): distant real kinase pair, gap convention verified on a pair the fixer never used | 37 | 56 | 93 | 5/5 PASS | OK |
| 9 | Edge - [NEW] Six real mammal HBB CDS: DNA global scores vs EMBOSS needle, DNA-vs-protein table, unknown-strand read placement | 35 | 54 | 89 | 4/4 PASS | OK |

**Execution average: 88.8 / 100** | Layer 1 avg 35.3/40 | Layer 2 avg 53.4/60 | **Assertions 40/42 (95.2%)** | **Executed 9/9**

## Step 1 - Skill Veto: PASS
T1 stability PASS (16/16 python blocks of SKILL.md run in one namespace in WSL with DeprecationWarning as error; Windows 15/16, the pywfa/mappy block is Linux-only as the Skill states; 5/5 shipped examples run from a copy). T2 contract PASS (frontmatter `name`, `description`, `tool_type`, `primary_tool`, `license`). T3 determinism PASS (aligner deterministic; `empirical_pvalue.py` seeded, identical null on rerun). T4 security PASS (grep for eval/exec/subprocess/requests/urllib/api key/token in SKILL.md, usage-guide.md, examples: none).

## Step 2 - Static: 82 / 100  (pre-fix 76)
| Category | Score | Note |
|---|---|---|
| functional_suitability | 10/12 | Every operation the guide teaches was executed and matched independent ground truth (own Gotoh, EMBOSS needle/water, BLAST+ 2.17, parasail, edlib, pywfa, mappy, pwalign): scores, coordinates, gap convention, semiglobal, input checks, saturation. Completeness gap: PAL2NAL, MMseqs2, needle/water, HHsearch are named without command lines; DNA dinucleotide shuffle points to ushuffle with no code. One sequence-specific number ('reverse complement 0') and the 'edlib returns edit distance only' wording are imprecise. |
| reliability | 9/12 | Version-drift fallback ('introspect and adapt') kept; new Input Checks section documents ValueError cases (lowercase, newline, J/U, empty), silent acceptances (*, X/B/Z, SeqRecord), strand and internal-stop traps, all reproduced. Biopython's ValueError does not name the offending letter; alignment_from_file.py still has no missing-file handling. |
| performance_context | 5/8 | SKILL.md grew from 402 to 449 lines (28 KB) with no references/ split; library table, gap-convention table, significance theory and BLAST flags all load up front. The workflow itself is linear with a score-only fast path. |
| agent_usability | 14/16 | Goal/Approach pairs with copy-pasteable snippets; 16/16 python blocks run in one namespace in WSL (15/16 on Windows, the pywfa/mappy block is Linux-only as the Skill says). Expected values sit in the snippets' comments (score 40, span [[300, 320]]) and all reproduce. Strong pitfall coverage: gap defaults, BLAST vs EMBOSS convention, argument order, saturation, off-spec input. Minor: snippets use undefined user variables (query, target, reference) without saying so; -10/-0.5 vs -11/-1 conventions coexist. |
| human_usability | 6/8 | Description matches natural requests but omits Needleman-Wunsch, Smith-Waterman, percent identity, semiglobal and needle/water trigger words. Input requirements are now explicit in Input Checks (uppercase alphabet, no whitespace, no empty sequence). |
| security | 11/12 | No credentials, network calls, eval/exec/subprocess anywhere in SKILL.md, usage-guide.md or examples (grep clean); local computation only; the example takes a user-supplied FASTA path as given. |
| maintainability | 9/12 | One dense SKILL.md, a slimmed usage-guide.md that points at it (dedup verified: every removed item is still in SKILL.md), five single-purpose examples that all run from a copy (alignment_from_file.py now takes argv and ships sequences.fasta). Version-specific facts are still scattered through one file; examples print no expected values. |
| agent_specific | 18/20 | Escape hatches are the strongest part (identity-based 'when NOT appropriate' table, routing to MMseqs2/jackhmmer/Foldseek; all 7 Related Skills exist in the repo); deterministic and idempotent; every file the guide points at exists. Statistical theory and library routing could live in references/. |

Shipped-means-present: every file SKILL.md/usage-guide.md points at exists (`examples/empirical_pvalue.py`, the shipped `examples/sequences.fasta`, all 7 Related Skills resolve in the repo). No `references/` folder is referenced. No P0.

## Regression: what the pre-fix audit found, re-run on the fixed Skill

| Pre-fix defect | Now | Evidence |
|---|---|---|
| `aligner.max_alignments` raises AttributeError (P1) | Fixed: Skill says the attribute does not exist; islice recipe; OverflowError explained | input7: AttributeError, OverflowError, islice OK; grep clean |
| 'Default gap penalties are 0' false (P1) | Fixed: defaults 1/0/-1/-1, fragmentation numbers reproduce (55/37 vs 9/5) | input1 |
| 'BLASTP defaults -11/-1' off by one (P1) | Fixed: convention table; BLASTP = -12/-1; verified twice (HBA/HBB 285, PKA/CDK2 222) with identical HSPs | input1, input8 |
| Output block wrong (P2) | Fixed: equals real output line for line | input7 |
| Semiglobal snippet order/names (P2) | Fixed: both snippets run with warnings as errors; -279 reproduces | input3, harness |
| No off-spec input guidance (P2) | Fixed: Input Checks section accurate bullet by bullet (one number imprecise) | input3 |
| parasail/edlib table: no code, no saturation warning (P2) | Fixed: snippets for parasail, edlib, pywfa, mappy reproduce; saturation real | input5, harness |
| R bullet outdated (P2) | Fixed: pwalign named, gap convention mapped, numbers reproduce | input7 R, input8 R |
| alignment_from_file.py needs unshipped FASTA; affine-vs-linear demo identical (P2) | Fixed: sequences.fasta ships, argv used; demo 86.0 vs 84.0 | run_examples.py |

### Independent look for defects the fix introduced
- **pywfa/mappy snippets**: ran in WSL only (Skill says Windows builds failed; `pip install pywfa` has no Windows wheel per TOOLS.md). pywfa -802 == Biopython -802; mappy locus 3500 mapq 60 and 2000 mapq 60. No defect.
- **Convention table** (Biopython/EMBOSS/parasail vs BLAST/pwalign): verified on two pairs by score and HSP coordinates; parasail 10/1 == Biopython -10/-1 in the harness. No defect.
- **Speed numbers**: within the stated ranges except parasail striped at 1.7x on Windows (Skill '2-10x'); timings vary run to run and the Skill says so. No defect.
- **usage-guide.md dedup**: read the pre-fix file; Prerequisites, agent steps, modes, all Tips (including twilight zone, PID definitions, MMseqs2/GPU, significance) are still in SKILL.md; the deleted `max_alignments` tip was wrong. Nothing the agent needs was lost.
- **New nits** (P2): 'reverse complement 0' is sequence-specific; 'edlib returns edit distance only' wording; SKILL.md grew to 449 lines with no references/ split; routed-to tools have no command lines; ushuffle not installable here.

## Detailed Outputs

### Input 1 - Canonical: [regression] Global BLOSUM62 alignment of real human HBA vs HBB with the Skill's gap-convention section
**Prompt:** Globally align human hemoglobin alpha (P69905) and beta (P68871) with BLOSUM62 and give me the score and percent identity. I will also compare against BLASTP, EMBOSS and R.
**Code:** `run\input1_real_global.py`, `run\input1b_blast_equiv.py`, `run\input1d_global_conv.py`, `run\input1_emboss_blast.sh`, `run\input1c_blast_default.sh`, `run\input7_R_biostrings.R`
**Executed:** true. Executed 100% (run/input1*.py, input1_emboss_blast.sh, input1c_blast_default.sh, input7_R_biostrings.R). Every score matched three independent tools.
**Output (trimmed):**
```
global BLOSUM62 -11/-1: Biopython 286.0 == own Gotoh 286.0 == parasail 286 == needle 11/1 286.0; -10/-0.5: 292.5 == Gotoh == needle 292.5; re-score of returned strings == reported score; counts 65/75/9
local -12/-1 = 285.0 with HSP q3-141 s4-146 == blastp -gapopen 11 -gapextend 1 -comp_based_stats 0 raw 285 (same HSP); local -11/-1 = 288.0 == water 11/1 288; blastp default (comp-based stats on) reports 286
R: Biostrings::pairwiseAlignment warns 'has moved to the pwalign package'; pwalign global 10/1 = 286, local 11/1 = 285, local 10/1 = 288, global 11/1 = 282 (= Biopython global -12/-1)
PairwiseAligner() defaults (1, 0, -1, -1); with BLOSUM62 defaults: 55 gap positions in 37 blocks vs 9 in 5 at -11/-1
```
**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100
**Assertions:**
- [PASS] Global scores equal independent ground truth: -11/-1 = 286 (own Gotoh, parasail, needle 11/1) and -10/-0.5 = 292.5 (Gotoh, needle) - all four tools agree; re-scoring the returned alignment strings gives the reported score
- [PASS] The Skill's BLASTP mapping holds: Biopython -12/-1 local = blastp raw 285 with the identical HSP; -11/-1 = water 11/1 = 288 - blastp -comp_based_stats 0 raw 285, HSP 3-141 / 4-146; water 288 (11/1) and 285 (12/1)
- [PASS] pwalign gap convention in the Skill is right (gapOpening = BLAST gapopen; global 10/1 = 286, local 11/1 = 285) - R via r.sh; Biostrings warning text matches the Skill's 'still works but warns'
- [PASS] PairwiseAligner() defaults and the '55 gap positions in 37 blocks vs 9 in 5' claim reproduce - (1.0, 0.0, -1.0, -1.0); (55, 37, 9, 5)
- [PASS] counts() recipe and percent-identity caveat are correct - identities/mismatches/gaps 65/75/9 == manual recount; PID1 43.6 (needle) vs PID2 46.4, and the Skill says the recipe is 'similar to PID2'

### Input 2 - Variant A: [regression] Local DNA alignment of a mutated real HBB segment inside a 1.15 kb synthetic sequence, plus strand recovery
**Prompt:** Find where this 147-nt HBB fragment sits in my 1.15 kb sequence (local DNA alignment). The read might be on the other strand.
**Code:** `run\input2_local_dna.py`
**Executed:** true. Executed 100% (input2_local_dna.py). Flanks SYNTHETIC (seed 7); the 150-nt segment is real NM_000518.5 with 5 planted substitutions and a 3-nt deletion.
**Output (trimmed):**
```
local 2/-1 open -10/-0.5: score 268.0 == own Gotoh 268.0 == hand sum 142*2 - 5 - (10 + 0.5*2); aligned target [[600,685],[688,750]] (planted 600..750); counts 142/5/3; parasail sw 10/1 267 == Biopython 267
reverse-complemented read: forward 268.0 vs reverse complement 34.5; the Skill's recipe (score seq and its reverse complement, keep the higher) recovers 268.0 from the flipped read
shipped local_alignment.py example: 26.0, [[5, 18]]
```
**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100
**Assertions:**
- [PASS] Local score equals independent Gotoh DP and the hand-derived planted-alignment score (268) - 268.0 == 268.0 == 142*2 - 5 - 11
- [PASS] Aligned span and counts match the planted segment - target 600..750; identities 142, mismatches 5, gaps 3
- [PASS] Biopython local 10/1 equals parasail sw_scan 10/1 - 267.0 vs 267
- [PASS] The Skill's strand recipe works on a flipped read - revcomp 34.5 vs forward 268.0; best-of-both recovers 268.0

### Input 3 - Edge: [regression] Semiglobal fragment placement, length mismatch, and every 'Input Checks' bullet
**Prompt:** Align this 20-nt primer inside a 620-nt template without penalising the flanks; also my lowercase protein, an RNA read, an empty record, a SeqRecord, and a rabbit CDS that may have a stop.
**Code:** `run\input3_edge_semiglobal.py`
**Executed:** true. Executed 100% (input3_edge_semiglobal.py). Reference SYNTHETIC (seed 11); CDS data real. One assertion fails: the '30-nt exact match 60, reverse complement 0' numbers.
**Output (trimmed):**
```
snippet 1 (end_gap_score=0): 40.0, target [[300,320]], order-independent; snippet 2 (open/extend_left/right_deletion_score, warnings as errors): 40.0, [[300,320]]; align(fragment, reference) = -279.0; mutated fragment 25.0 == independent semiglobal DP 25
global -279.0 | local 40.0 | semiglobal 40.0
ValueError 'sequence contains letters not in the alphabet' for lowercase, trailing newline, J, U (and NUC.4.4 + U); empty -> 'sequence has zero length'; '*', X/B/Z, SeqRecord accepted (SeqRecord scores 286.0 = its .seq); match/mismatch aligner: 'acgt' vs 'ACGT' = -4
50 random 30-mers, local 2/-1: forward always 60.0; reverse complement median 17.5, max 29.0 (Skill: 'reverse complement 0')
internal-stop expression flags only NM_001314043.1 of 7 real CDS; old query_* names accepted with DeprecationWarning, same score
```
**Scores:** Basic 35/40 | Specialized 53/60 | Total 88/100
**Assertions:**
- [PASS] Both semiglobal snippets run as written (warnings as errors) and give 40.0 / [[300, 320]]; swapped order gives the -279 the Skill quotes - mutated fragment 25.0 == independent semiglobal DP
- [PASS] Every Input Checks ValueError / silent-accept bullet reproduces on Biopython 1.88 - lowercase, newline, J, U, NUC.4.4+U, empty; *, XBZ, SeqRecord accepted; match/mismatch aligner four mismatches
- [PASS] The internal-stop expression flags NM_001314043.1 and none of the six clean CDS - 1 of 7 flagged
- [PASS] The deprecated query_left/right_* names are accepted with a DeprecationWarning and give the same result - score 40.0; 'was renamed' warning
- [FAIL] The strand bullet's numbers reproduce ('30-nt exact match scored 60, reverse complement 0') - 60 reproduces; reverse complement does not score 0 in local mode (median 17.5, max 29 over 50 random 30-mers). Qualitatively right (strand-specific), number sequence-specific

### Input 4 - Variant B: [regression] Is HBA/HBB significant? Empirical p-values with the Skill's own example on related, distant and unrelated real pairs
**Prompt:** Is the HBA/HBB alignment significant? Compare it with myoglobin and with a kinase.
**Code:** `run\input4_significance.py`, `run\ushuffle_attempt.sh`
**Executed:** true. Executed 100% (input4_significance.py imports a copy of examples/empirical_pvalue.py). ushuffle (DNA dinucleotide shuffle named by the Skill) not executed: pip build fails on Windows and in WSL.
**Output (trimmed):**
```
HBA vs HBB: local raw 288, K-A bits 115.5, empirical p 0.0010 (floor 1/1001), null mean 28.9 max 51
MYG_HUMAN vs HBB: raw 111, bits 47.4, p 0.0010 (global pid2 26.0%)
PKA 1ATP vs HBB: raw 33, bits 17.3, p 0.2478 (global pid2 29.0%, identity alone misleading)
seed=42 rerun identical for all three; Gumbel fit of the null lambda 0.262 vs NCBI 0.267; demo pair p 0.1449; preserve='di' -> NotImplementedError 'Use the ushuffle library'
```
**Scores:** Basic 35/40 | Specialized 53/60 | Total 88/100
**Assertions:**
- [PASS] Skill's empirical_pvalue.py is deterministic (identical p and null on rerun, seed 42) - 3 of 3 pairs identical
- [PASS] Results fall in the Skill's bit-score bands: related 115 bits likely homology, distant 47 possible, unrelated 17 not significant (p 0.248) - p 0.001 / 0.001 / 0.248
- [PASS] Karlin-Altschul bits agree with BLASTP and the shuffled null agrees with NCBI lambda - 115.5 bits vs blastp 114; lambda 0.262 vs 0.267
- [PASS] The DNA path is honest: preserve='di' refuses and points to ushuffle rather than faking a dinucleotide shuffle - NotImplementedError raised

### Input 5 - Stress: [regression] Library-selection table re-measured: parasail, edlib, pywfa, mappy on long synthetic DNA, saturation, every Skill snippet
**Prompt:** Score 1000 read pairs and one 20 kb pair; which library should I use? Show me code for parasail, edlib, pywfa and mappy.
**Code:** `run\input5_libs.py`, `run\snippets_harness.py`, `run\edlib_path_check.py`
**Executed:** true. Executed 100% on Windows (parasail, edlib) and WSL (all four, plus the SKILL.md extraction harness). All DNA SYNTHETIC (seeds 4/5/9/3/21) except the real HBB CDS used by the harness.
**Output (trimmed):**
```
parasail nw_striped_sat 7003 == Biopython 7003 (4 kb, 118 injected edits); sw_striped_sat 7006 == 7006; edlib NW 118 == -Levenshtein 118; edlib HW 2 == Biopython free-target-end Levenshtein 2; edlib protein 15 == 15
WSL: pywfa -802 == Biopython gap-affine -802; mappy locus 3500..4500 mapq 60 (planted 3500)
1000 pairs: Biopython == parasail striped_sat == scan_sat 1000/1000; Levenshtein == -edlib 1000/1000
300 nt x1000 (Windows): parasail striped 1.7x, scan 3.9x (Skill 2-10x); edlib 14x vs Levenshtein, 27x vs affine (Skill 15x / 26x). WSL: 2.6-4.9x, 15x / 36x
20 kb (Windows): parasail 2.4x (WSL 3.7-4x) (Skill 3-8x), edlib 437x (WSL 808-822x) (Skill 400x+); nw_striped_16 returns 0 with saturated=True (true 35644), _sat variant 35644
SKILL.md harness: WSL 16/16 blocks OK with DeprecationWarning promoted to error, all six snippet assertions pass; Windows 15/16 (pywfa/mappy block, no Windows build, as the Skill states)
```
**Scores:** Basic 36/40 | Specialized 54/60 | Total 90/100
**Assertions:**
- [PASS] Every Verified snippet reproduces its own comment: parasail == Biopython, edlib == -Levenshtein, pywfa == Biopython gap-affine, mappy hits the planted locus - harness 6/6 assertions PASS in WSL
- [PASS] Cross-library agreement at scale: 1000/1000 pairs for parasail and edlib - 1000 == 1000
- [PASS] Measured speed ranges hold within run-to-run variation (parasail 1.7-3.9x at 300 nt, edlib 14-27x, 20 kb edlib 437x) - Windows and WSL, min of 3 runs
- [PASS] The saturation warning is real: fixed-width nw_striped_16 silently returns 0 on a 20 kb pair; the _sat variant is correct - 0 with saturated=True vs 35644
- [PASS] edlib alphabet and mode claims: works on protein; HW mode = query anywhere in target - 15 == 15; HW 2 == 2

### Input 6 - Scope Boundary: [regression] Human vs cow HBB CDS for dN/dS (protein first, back-translate), the internal-stop trap, and a many-vs-many request
**Prompt:** Align human and cow HBB coding sequences for a dN/dS analysis, include the rabbit HBB2 record, and separately align one query against a whole database.
**Code:** `run\input6_scope.py`, `run\input6_pal2nal.py`, `run\input6_pal2nal_mafft.py`, `run\input6_mmseqs.sh`
**Executed:** true. Executed 100% (input6_scope.py, input6_pal2nal.py, input6_pal2nal_mafft.py, input6_mmseqs.sh). Real RefSeq CDS and UniProt. The Skill names PAL2NAL and MMseqs2 but ships no command, so the auditor wrote both.
**Output (trimmed):**
```
human/cow nucleotide pid2 87.0% (gaps 6) vs protein 84.8% (gaps 2); protein-guided codon alignment 441 columns, human row re-translates to the protein row; 46 of 147 codons differ
PAL2NAL 14: human+cow -> 2 records (910 B); after MAFFT protein alignment of human+cow+rabbit(NM_001314043.1) pal2nal exits 0 with EMPTY output and '#--- ERROR: inconsistency between the following pep and nuc seqs' (also with stop->X); control without rabbit -> 2 records
(a hand-built pairwise protein alignment that keeps '*' does not fail: the trap needs the MAFFT route, which strips '*')
MMseqs2 easy-search all-vs-all on 8 globins: 54 rows; HBA->HBB raw 280, bits 115, pident 43.4, E 3e-34
```
**Scores:** Basic 33/40 | Specialized 48/60 | Total 81/100
**Assertions:**
- [PASS] DNA-vs-protein routing is right on real orthologs (nucleotide identity 87% > 70% -> DNA is fine) and protein-first back-translation is frame-consistent - 441 codon columns; re-translation equals the protein row
- [PASS] The internal-stop warning is correct on the realistic MAFFT + PAL2NAL route (rabbit NM_001314043.1 gives empty output, exit 0) - 0 records vs 2 records for the control
- [PASS] The many-vs-many route (MMseqs2) is supported by a real run and the Skill does not loop DP over a database - 54 rows; HBA->HBB bits 115
- [PASS] Skill's escape hatch is correct: 'alignment exists' is not the homology gate, E-value/bit score is - MMseqs2 E 3e-34 for the true homolog
- [FAIL] The Skill supplies runnable commands for the tools it routes to (PAL2NAL, MMseqs2, needle/water, HHsearch) - names only, no command lines or flags; the auditor wrote all three

### Input 7 - Adversarial: [regression] pairwise2, aligner.max_alignments, EMBOSS-style percent identity, IUPAC DNA, algorithm names, R, printed output block
**Prompt:** Use pairwise2, cap alignments with max_alignments, give percent identity like EMBOSS, score IUPAC DNA, tell me which algorithm Biopython picked, and do it in R.
**Code:** `run\input7_adversarial.py`, `run\input7_R_biostrings.R`, `run\run_examples.py`
**Executed:** true. Executed 100% (input7_adversarial.py, input7_R_biostrings.R, run_examples.py). Every pre-fix defect in this input is gone.
**Output (trimmed):**
```
pairwise2: DeprecationWarning, score 292.5 == PairwiseAligner 292.5
aligner.max_alignments = 100 -> AttributeError (the Skill now says so); len(alignments) with zero gap scores on repetitive input -> OverflowError; islice(alignments, 5) works
PID1 43.6 PID2 46.4 PID3 45.8 PID4 45.0 (== needle 65/149 and pwalign pid())
NUC.4.4 R/A +1, hand sum 35.0 == score; 30 matrices; algorithm names: exactly the six the Skill lists; printed 'Alignment Output Format' block equals real output line for line; fasta/clustal/psl/sam OK; substitutions['G','T'] == 1
shipped examples (from the copy): alignment_from_file.py 26.0 (independent 26.0), global_alignment.py affine 86.0 vs linear 84.0, local 26.0 [[5,18]], protein 377.0, empirical_pvalue 23.0 p 0.1449; no __pycache__ written
```
**Scores:** Basic 36/40 | Specialized 54/60 | Total 90/100
**Assertions:**
- [PASS] pairwise2 is flagged deprecated but present and agrees with PairwiseAligner - 292.5 == 292.5
- [PASS] max_alignments handling is correct: attribute absent (AttributeError), OverflowError on len(), islice works; the guide no longer tells the agent to set it - grep of SKILL.md and usage-guide.md clean
- [PASS] Percent-identity definitions match EMBOSS and pwalign - 43.6 / 46.4 / 45.8 / 45.0
- [PASS] NUC.4.4 IUPAC claims, 30-matrix listing, six algorithm names and the printed output block are accurate - score 35.0 == hand sum; name sets equal; output block equals real output
- [PASS] All five shipped examples run from a copy and print checked values; the affine-vs-linear demo now differs (86.0 vs 84.0) - alignment_from_file.py 26.0 == independent 26.0

### Input 8 - Variant B: [NEW] PKA (1ATP) vs CDK2 (1HCK): distant real kinase pair, gap convention verified on a pair the fixer never used
**Prompt:** Align PKA and CDK2 with BLOSUM62 and tell me whether the alignment means anything; I want the number to match BLASTP and EMBOSS.
**Code:** `run\input8_kinase_conv.py`, `run\input8_ground_truth.sh`, `run\input8_R_pwalign.R`
**Executed:** true. Executed 100% (input8_kinase_conv.py, input8_ground_truth.sh, input8_R_pwalign.R). Real PDB SEQRES from public-data; nothing synthetic.
**Output (trimmed):**
```
1ATP:E 350 aa, 1HCK:A 298 aa. Biopython vs own Gotoh: global -11/-1 124, -10/-0.5 186.5, -12/-1 110, local -11/-1 228, -12/-1 222 (all equal)
EMBOSS: needle 11/1 124, 10/0.5 186.5, 12/1 110; water 11/1 228, 12/1 222
blastp -gapopen 11 -gapextend 1 -comp_based_stats 0: raw 222, bits 90.1, HSP q40-244 s1-209, identical to Biopython local -12/-1 (K-A bits 90.1); blastp default (comp-based stats) 223
pwalign: global 10/1 124, local 11/1 222, local 10/1 228
BLOSUM45/62/80 local: 317/222/380 (not comparable across matrices); global pid2 29.1% (Skill band 25-40%); empirical p at floor 0.001
```
**Scores:** Basic 37/40 | Specialized 56/60 | Total 93/100
**Assertions:**
- [PASS] Global -11/-1 = 124 equals needle 11/1, pwalign 10/1 and an independent Gotoh; -10/-0.5 = 186.5 equals needle - four tools agree
- [PASS] The Skill's central fix holds on a new pair: BLASTP 11/1 = Biopython -12/-1 (local 222 = blastp raw 222, same HSP) and water 12/1 = 222 - blastp 222 q40-244 s1-209
- [PASS] -11/-1 is EMBOSS 11/1, not BLASTP: local -11/-1 = 228 = water 11/1 = pwalign 10/1 - 228 == 228 == 228
- [PASS] pwalign conversion (gapOpening = BLAST gapopen) is right - global 10/1 124, local 11/1 222
- [PASS] Identity band and significance guidance fit a real distant homolog pair: pid2 29.1% (25-40% row), 90 bits 'likely homology', empirical p at the floor - K-A bits 90.1 == blastp 90.1

### Input 9 - Edge: [NEW] Six real mammal HBB CDS: DNA global scores vs EMBOSS needle, DNA-vs-protein table, unknown-strand read placement
**Prompt:** Score human HBB CDS against each ortholog, tell me the identity, and place a 120-nt read of unknown orientation on the human CDS.
**Code:** `run\input9_real_dna.py`
**Executed:** true. Executed 100% in WSL (input9_real_dna.py). Real RefSeq CDS; rabbit HBB2 excluded here (covered in input 6).
**Output (trimmed):**
```
NUC.4.4 -10/-0.5 global vs needle EDNAFULL 10/0.5 (end gaps penalised): chimp 2211.0/2211.0, cow 1666.5/1666.5, rat 1612.0/1612.0, 2060.0/2060.0, 1673.0/1673.0; own Gotoh (human vs cow) 1666.5
nucleotide PID1 99.8, 85.3, 85.2, 96.2, 86.9 (all > 70) vs protein PID1 100.0, 83.7, 85.0, 94.6, 83.7
flipped cow 120-nt segment: as given 28.5, reverse complement 183.0 == un-flipped 183.0; placed at human 126..246; edlib HW same locus (126..245, distance 19)
```
**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100
**Assertions:**
- [PASS] NUC.4.4 global -10/-0.5 equals EMBOSS needle EDNAFULL 10/0.5 on all five ortholog pairs and an independent Gotoh DP - 5/5 equal
- [PASS] The Skill's DNA-vs-protein table fits real orthologs (all nucleotide identities > 70%) - min 85.2%
- [PASS] The Skill's strand recipe (score seq and its reverse complement, keep the higher) reproduces the un-flipped score and locus - 183.0 == 183.0; 126..246
- [PASS] The wrong orientation scores far lower and edlib HW independently finds the same locus - 28.5 vs 183.0; edlib 126..245

## Research Veto: PASS (M1 PASS, M2 PASS, M3 PASS, M4 PASS)

## Step 8 - Final
Static 82 x 0.4 = 32.8; Execution 88.8 x 0.6 = 53.3; **Final 86 - Production Ready, deployable, no veto, no open P0/P1.**
Floors for Production Ready: static 82 >= 80, exec 88.8 >= 85, L1 35.3 >= 32, L2 53.4 >= 48, assertions 95.2% >= 90: all met.

**P2**
1. SKILL.md is 449 lines / 28 KB with no references/ split. The guide grew from 402 to 449 lines; the gap-convention table, library table, significance theory and BLAST flags all load up front.
2. Routed-to tools are named without command lines. PAL2NAL, MMseqs2 (easy-search / --num-iterations), EMBOSS needle/water and HHsearch are named but no flags or invocations are shown, and the DNA dinucleotide shuffle points at ushuffle with no code (ushuffle failed to build via pip on Windows and in WSL here).
3. Strand bullet quotes a sequence-specific number. 'a 30-nt exact match scored 60, reverse complement 0' reproduces the 60 but not the 0: over 50 random 30-mers the local score of the reverse complement had median 17.5 and max 29.
4. 'edlib returns edit distance only' is misleading. edlib.align(..., task='path') returns a CIGAR and alignment (verified); its scoring is unit-cost edit distance, which is what the sentence means.
5. Description omits common trigger phrases. The description says 'pairwise sequence alignment' but not Needleman-Wunsch, Smith-Waterman, semiglobal, percent identity, needle/water, or 'reverse complement'.
