> **Audit record for `bio-alignment-pairwise`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@354b499](https://github.com/mrsonord2240/bioSkills/tree/354b4992cd8d2f1bee039510af618da0333821f1/alignment/pairwise-alignment) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-pairwise

Generated: 2026-09-19 | Source: `mrsonord2240/bioSkills@354b4992cd8d2f1bee039510af618da0333821f1:alignment/pairwise-alignment` (first audit)
Category: Data Analysis (3) | Mode: A (agent writes code from the Skill's patterns; the 5 `examples/` are templates) | Complexity: Complex (3 alignment modes, DNA/protein, significance, library routing, 6 files) -> N = 7

All scripts and logs are in `run\` (copy of the Skill in `run\skill\`, never the clone). Ground truth was independent of the Skill: an own pure-Python Gotoh DP (`ref_gotoh.py`), parasail, EMBOSS needle/water, BLASTP, MMseqs2, edlib, R pwalign, planted coordinates. Synthetic data is labelled SYNTHETIC in each script and lives in `run\data\`; real data is UniProt globins, RefSeq HBB CDS and PDB SEQRES from `audit-envs\alignment\public-data`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (real HBA vs HBB, global BLOSUM62) | 35 | 53 | 88 | 4/5 | ✅ |
| 2 | Variant A (local DNA, planted real segment) | 35 | 55 | 90 | 4/4 | ✅ |
| 3 | Edge (semiglobal, length mismatch, off-spec input) | 31 | 46 | 77 | 3/4 | ✅ |
| 4 | Variant B (empirical significance, real pairs) | 35 | 53 | 88 | 4/4 | ✅ |
| 5 | Stress (parasail/edlib/pywfa/mappy, long DNA) | 32 | 46 | 78 | 2/4 | ✅ |
| 6 | Scope boundary (CDS dN/dS route, MMseqs2 route) | 33 | 47 | 80 | 4/4 | ✅ |
| 7 | Adversarial (max_alignments, pairwise2, PID, IUPAC, R) | 30 | 44 | 74 | 3/5 | ❌ (PARTIAL) |

**Execution average: 82.1 / 100** | Layer 1 avg 33.0/40 | Layer 2 avg 49.1/60 | **Assertions 24/30 (80.0%)** | Executed 7/7

## Step 1 — Skill Veto: PASS
T1 stability PASS (13/14 SKILL.md python blocks run in one namespace, 5/5 examples run; `alignment_from_file.py` needs a user FASTA). T2 contract PASS (frontmatter has `name`, `description`, `tool_type`, `primary_tool`, `license`). T3 determinism PASS (aligner deterministic; `empirical_pvalue.py` seeded, identical null on rerun, input 4). T4 security PASS (grep for eval/exec/subprocess/requests/api key in the Skill: none).

## Step 2 — Static: 76 / 100
Functional 9/12, Reliability 7/12, Performance/Context 5/8, Agent usability 12/16, Human usability 5/8, Security 11/12, Maintainability 9/12, Agent-specific 18/20 (notes in the JSON).
Shipped-means-present: every file SKILL.md/usage-guide.md points at exists (`examples/empirical_pvalue.py`; all 7 Related Skills resolve in the repo). No `references/` folder is referenced. No P0.

## Claim checks against Biopython 1.88 (`claims_api.py`, `claims_defaults.py`, `snippets_harness.py`)

| SKILL.md claim | Observed | Result |
|---|---|---|
| Default `PairwiseAligner()` gaps are 0 | open -1.0, extend -1.0 (printed) | FALSE on 1.88 |
| `aligner.max_alignments = 100` (SKILL.md, usage-guide) | `AttributeError: 'PairwiseAligner' object has no attribute 'max_alignments'` | FAILS |
| `len(alignments)` "Found N optimal alignments" | `OverflowError` on repetitive input (gap 0 scoring) | fragile |
| Output block `\|\|\|\|\|.\|\|\|\|.\|\|` for the example pair | real output `\|\|\|\|.\|\|\|\|\|.\|\|` | off by one |
| `substitution_matrices.load()` lists 30 | 30 | ok |
| NUC.4.4 match +5 / mismatch -4, R vs A = +1 | 5, -4, 1 | ok |
| `aligner.algorithm` names | Needleman-Wunsch, Gotoh global/local, Waterman-Smith-Beyer (callable gap fn) | ok |
| fasta/clustal/psl/sam export; `alignment.substitutions`; `counts()` | all work; `substitutions['G','T']==1` correct | ok |
| `Bio.pairwise2` deprecated but present | imports with BiopythonDeprecationWarning | ok |
| Semiglobal `query_*_open_gap_score` names | work but warn "renamed to open_left_deletion_score" | deprecated |
| BLASTP defaults = open -11 / extend -1 in Biopython | reproduces EMBOSS 11/1 (288), not BLASTP (285); -12/-1 reproduces BLASTP | off by one |
| Karlin-Altschul: bit score, shuffle null | K-A bits 115.5 vs BLASTP 114; null lambda 0.262 vs 0.267 | ok |
| PID1-4 definitions | 43.6 / 46.4 / 45.8 / 45.0 = EMBOSS 65/149 and pwalign `pid()` | ok |
| "R: pairwiseAlignment() (Biostrings)" | works (286) but warns it moved to pwalign | outdated |
| Citations (Kallenborn 2025, Marco-Sola 2021/2023) | exist (Crossref, `refs_check.sh`) | ok |

`snippets_harness.py` output: block 12 (`aligner.max_alignments`) is the only failure; 13/14 executed.

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Globally align human hemoglobin alpha (P69905) and beta (P68871) with BLOSUM62 and give me the score and percent identity."
**Code:** `run\input1_real_global.py`, `run\input1b_blast_equiv.py`, `run\input1_emboss_blast.sh`.
**Output (trimmed):**
```
global BLOSUM62 11/1: Biopython 286.0 == independent Gotoh 286.0 == parasail nw 286
global BLOSUM62 10/0.5: 292.5 == Gotoh 292.5;  identities=65 mismatches=75 gaps=9  PID1(cols)=43.6%  PID2=46.4%
re-score of returned alignment strings == reported score
EMBOSS needle (-endweight Y) 11/1: Score 286.0, Identity 65/149 (43.6%);  10/0.5: 292.5
blastp -gapopen 11 -gapextend 1 raw score 285, HSP q3-141 s4-146
Biopython local -11/-1 = 288 (= water 11/1), local -12/-1 = 285 with identical HSP coordinates   [FAIL: Skill labels -11/-1 "BLASTP defaults"]
```
**Scores:** Basic 35 | Specialized 53 | Total 88
**Assertions:** [PASS] score equals Gotoh/parasail/needle | [PASS] counts() and re-score | [PASS] PID definition caveat | [FAIL] "BLASTP defaults -11/-1" reproduces BLASTP | [PASS] no homology overclaim (significance section)

### Input 2 — Variant A
**Prompt:** "Find where this 147-nt HBB fragment sits in my 1.15 kb sequence (local DNA alignment)."
**Code:** `run\input2_local_dna.py` (flanks SYNTHETIC seed 7; segment real NM_000518.5 CDS 30..180 with 5 substitutions and a 3-nt deletion).
**Output:** score 268.0 == Gotoh 268.0 == 142*2-5-(10+1); `aligned[0] = [[600,685],[688,750]]`; counts 142/5/3; parasail sw 10/1 267 == Biopython 267; Skill's `local_alignment.py` example 26.0, `[[5,18]]`. Reverse-complement query scores 34.5 (no strand advice in the Skill).
**Scores:** Basic 35 | Specialized 55 | Total 90
**Assertions:** 4/4 PASS.

### Input 3 — Edge
**Prompt:** "Align this 20-nt primer inside a 620-nt template without penalising the flanks, and also just align my lowercase protein."
**Code:** `run\input3_edge_semiglobal.py` (reference SYNTHETIC seed 11).
**Output:**
```
(a1) free-query-end-gaps, align(reference, fragment): score 40.0, target span [[300,320]]
(a1') align(fragment, reference) with the same aligner: -279.0
(a2) end_gap_score=0: 40.0 both orders;  mutated fragment 25.0 == independent semiglobal DP 25
(b) global -279.0 | local 40.0 | semiglobal 40.0
(c) lowercase protein, U, J, empty, trailing newline, NUC.4.4+U, NUC.4.4+lowercase -> ValueError (alphabet / zero length); '*' , X/B/Z, SeqRecord -> accepted
(d) SKILL "defaults are 0": observed -1/-1; default-gap aligner gives 40 gap segments vs 4 with -11/-1
```
**Scores:** Basic 31 | Specialized 46 | Total 77
**Assertions:** [PASS] semiglobal snippet 40/[300,320] | [PASS] end_gap_score matches DP | [PASS] global/local/semiglobal ordering | [FAIL] off-spec input anticipated by the Skill

### Input 4 — Variant B
**Prompt:** "Is the HBA/HBB alignment significant? Compare with myoglobin and with a kinase."
**Code:** `run\input4_significance.py` imports a copy of the Skill's `examples/empirical_pvalue.py`.
**Output:**
```
HBA vs HBB (related):      local raw 288  bits 115.5  empirical p 0.0010 (floor 1/1001)  null mean 28.9 max 51
MYG_HUMAN vs HBB (distant):local raw 111  bits 47.4   p 0.0010   (global pid2 26.0%)
PKA 1ATP vs HBB (unrelated):local raw 33  bits 17.3   p 0.2478   (global pid2 29.0% -- identity alone is misleading)
seed=42 rerun: identical p and null for all 3 pairs; Gumbel fit of null lambda 0.262 (NCBI 0.267)
```
**Scores:** Basic 35 | Specialized 53 | Total 88
**Assertions:** 4/4 PASS.

### Input 5 — Stress
**Prompt:** "Score 1000 read pairs and one 20 kb pair; which library should I use?"
**Code:** `run\input5_libs.py`, run in WSL env `alignment` (all data SYNTHETIC seeds 3/5/9).
**Output:**
```
Levenshtein: Biopython -118 == -edlib 118 (<= 118 injected edits);  affine 2/-1 10/1: Biopython 7003 == parasail 7003; local 7006 == 7006
pywfa score -802 == Biopython gap-affine -802;  mappy r_st 3502 vs planted 3500 (mapq 60)
1000 pairs: Biopython == parasail for 1000/1000; Levenshtein == -edlib for 1000/1000
1000 x 300 nt: Biopython 0.264 s | parasail nw_scan 0.024 s (11.2x), striped 0.048 s (5.4x) | edlib 0.0068 s (15x vs Levenshtein, 39x vs affine)
20 kb: Biopython 1.38 s | parasail 8x | edlib 1356x
parasail nw_striped_16 20 kb: score 0, saturated=True (true 36763; 32-bit correct)
```
**Scores:** Basic 32 | Specialized 46 | Total 78
**Assertions:** [PASS] cross-library agreement | [PASS] pywfa/mappy | [FAIL] speed ranges hold at 300 nt | [FAIL] parasail correct at scale without a silent failure

### Input 6 — Scope boundary
**Prompt:** "Align human and cow HBB coding sequences for a dN/dS analysis; separately, align one query against a whole database."
**Code:** `run\input6_scope.py`, `run\input6_mmseqs.sh` (real RefSeq CDS, real UniProt).
**Output:** nt pid2 87.0% (gaps 6) vs protein pid2 84.8% (gaps 2); protein-first back-translation gives 441 codon columns, human row re-translates to the protein row; 46 of 147 codons differ. Rabbit HBB2 CDS has 2 stops. MMseqs2 all-vs-all on 8 globins: 54 rows; HBA->HBB raw 280, bits 115, pident 43.4%, E 3e-34 (BLASTP 285).
**Scores:** Basic 33 | Specialized 47 | Total 80
**Assertions:** 4/4 PASS. Note: the Skill names PAL2NAL and MMseqs2 but ships no command or back-translation code; the auditor wrote both.

### Input 7 — Adversarial
**Prompt:** "Use pairwise2, cap alignments with the Skill's max_alignments, give percent identity like EMBOSS, score IUPAC DNA, and do it in R."
**Code:** `run\input7_adversarial.py`, `run\input7_R_biostrings.R` (via the env's `r.sh`).
**Output:**
```
pairwise2 deprecation warning: True, score 292.5 == PairwiseAligner 292.5
aligner.max_alignments = 100 -> AttributeError
len(alignments) on repetitive input -> OverflowError; islice(alignments, 5) still works
PID1 43.6  PID2 46.4  PID3 45.8  PID4 45.0  (== EMBOSS 65/149 and pwalign pid())
NUC.4.4: R/A +1, Y/G -4, N/C -2; 'ACGTRYNACGT' score 35.0 == hand sum
R: Biostrings::pairwiseAlignment warning "has moved to the pwalign package"; global gapOpening=10/ext=1 -> 286 (= Biopython -11/-1); local 11/1 -> 285 (= BLASTP)
```
**Scores:** Basic 30 | Specialized 44 | Total 74
**Assertions:** [PASS] pairwise2 flagged | [FAIL] max_alignments works | [PASS] PID definitions | [PASS] NUC.4.4 claims | [FAIL] R bullet current

## Research Veto: PASS (M1 PASS, M2 PASS, M3 PASS, M4 PASS)
M4 note: the one failing line (`aligner.max_alignments`) sits under the Skill's own "introspect and adapt on AttributeError" rule, so it is a P1, not a veto.

## Step 8 — Final
Static 76 x 0.4 = 30.4; Execution 82.1 x 0.6 = 49.3; **Final 80 (79.7) — ✅ Limited Release, deployable, no veto, no P0.**
Floors for Limited Release all met (static 76 >= 70, exec 82.1 >= 75, L1 33.0 >= 28, L2 49.1 >= 42, assertions 80.0% >= 80%). Production Ready is out of reach on the static floor (76 < 80) and the fixes below.

**P1**
1. `aligner.max_alignments` does not exist on Biopython 1.88 (SKILL.md, Common Errors, usage-guide); `len(alignments)` can raise OverflowError.
2. "Default gap penalties are 0" is false on 1.88 (-1/-1).
3. "BLASTP defaults open -11/extend -1" is off by one in Biopython's convention (BLASTP 11/1 = Biopython -12/-1, verified by raw score and HSP coordinates).

**P2** wrong output-format block; semiglobal snippet needs argument order and uses deprecated names; no off-spec-input/strand/internal-stop guidance; parasail/edlib lacks code, saturation warning and realistic speed numbers; R bullet outdated with unmapped gap convention; `alignment_from_file.py` needs an unshipped FASTA and the affine-vs-linear demo is gap-free (108.0 vs 108.0).
