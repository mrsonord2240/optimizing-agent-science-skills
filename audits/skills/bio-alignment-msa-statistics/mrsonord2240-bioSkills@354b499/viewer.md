> **Audit record for `bio-alignment-msa-statistics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@354b499](https://github.com/mrsonord2240/bioSkills/tree/354b4992cd8d2f1bee039510af618da0333821f1/alignment/msa-statistics) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-alignment-msa-statistics

Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@354b4992cd8d2f1bee039510af618da0333821f1:alignment/msa-statistics` (first audit; staging HEAD has moved but `git diff 354b499 HEAD -- alignment/msa-statistics` is empty)
Category: Data Analysis (Research Veto applies) | Mode: D (SKILL.md patterns + 8 runnable example scripts) | Complexity: Complex, N = 7
Env: `F:\OpenScience\audit-envs\alignment` (Windows venv, Biopython 1.88, numpy 2.0.2, scipy 1.18.1; WSL `alignment` env; R 4.4.3 + pwalign 1.2.0; modeltest-ng 0.1.7 in a new side env `aln-mtng`).
All scripts are in `run\`; the Skill was copied to `run\skill\` and run from there. The clone was checked with `find -name __pycache__` and `git status`: untouched.

## Skill Veto (Step 1)

| Dim | Result | Basis |
|---|---|---|
| T1 Stability | PASS | 8/8 examples exit 0 on real data; no loops or crashes; degenerate inputs raise clear errors or return values |
| T2 Contract | PASS | frontmatter has name, description, license, tool_type, primary_tool |
| T3 Determinism | PASS | no randomness anywhere |
| T4 Security | PASS | no eval/exec, no network, read-only |

Shipped-means-present: `SKILL.md`, `usage-guide.md` and all 8 files in `examples/` exist. Cross-references checked: `alignment/msa-parsing/examples/{henikoff_weights,neff,mi_apc}.py`, `alignment/multiple-alignment` ("Confidence Assessment" section), `phylogenetics/{modern-tree-inference,distance-calculations}`, `sequence-manipulation/sequence-properties` all exist. No `references/` folder is referenced. No P0 from missing files.

## Static score (Step 2): 67 / 100

| Category | Score | Note |
|---|---|---|
| Functional Suitability | 8/12 | Broad and correct on clean input; PID1 code contradicts its definition, `alignment_score` charges gap/gap, IC blow-up, Ti/Tv for protein; "substitution matrix" = counts only |
| Reliability | 5/12 | No handling of lowercase / "." / ambiguity: silent wrong numbers; stale Common Errors table |
| Performance/Context | 6/8 | 450-line SKILL.md with stubs to examples; acceptable runtime |
| Agent Usability | 10/16 | Clear goals and pick-a-method tables; internal inconsistencies (gap/gap, PID1 vs PID4, Bio.Align vs AlignIO) |
| Human Usability | 4/8 | Natural prompts; off-spec input neither rejected nor handled |
| Security | 10/12 | Nothing risky; no alphabet validation |
| Maintainability | 8/12 | 8 focused examples; copy-pasted background table; no tests/expected outputs |
| Agent-Specific | 16/20 | Good disclosure, composability, escape hatches |

## Test inputs (Step 4)

```
Skill: bio-alignment-msa-statistics | Category: 3 Data Analysis | Mode: D | Complexity: Complex -> 7 inputs
Input 1 (Canonical)      : Pfam PF00042 seed (real, 73x141): identity matrix, conservation, entropy/IC, gaps, SP, PSSM, JSD
Input 2 (Variant A)      : alignments as real tools write them: MAFFT/Clustal Omega, hmmalign AFA (lowercase inserts + dots), Pfam seed with "." gaps
Input 3 (Edge)           : tiny hand-computed alignment (terminal gaps, internal gap, ambiguity, all-gap column) [synthetic] + pwalign::pid on real globin pairs
Input 4 (Variant B)      : six real HBB CDS, MAFFT nucleotide alignment (lowercase): Ti/Tv, DNA IC, PSSM, identity
Input 5 (Stress)         : synthetic 300x300 and 2000x300 protein alignments [synthetic, seed 20260920/21]
Input 6 (Scope Boundary) : publication-grade distances: ModelTest-NG / IQ-TREE / distmat hand-off + DistanceCalculator snippet
Input 7 (Adversarial)    : messy collaborator alignment + degenerate inputs [synthetic]
```

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 32 | 46 | 78 | 3/5 PASS | OK |
| 2 | Variant A | 22 | 29 | 51 | 1/5 PASS | WARN |
| 3 | Edge | 28 | 44 | 72 | 3/5 PASS | WARN |
| 4 | Variant B | 21 | 28 | 49 | 2/5 PASS | WARN |
| 5 | Stress | 32 | 48 | 80 | 4/5 PASS | OK |
| 6 | Scope Boundary | 34 | 52 | 86 | 4/5 PASS | OK |
| 7 | Adversarial | 19 | 26 | 45 | 1/5 PASS | WARN |

**Execution Average: 65.9 / 100** (Layer 1 avg 26.9/40, Layer 2 avg 39.0/60)
**Assertion Pass Rate: 18/35 (51%)**
**Executed: 7/7 inputs** (Input 6 in WSL + Windows); 8/8 shipped examples run from a copy; 12 non-stub SKILL.md python blocks executed verbatim (`run\skill_blocks.py`), 5 stubs (`...`) skipped because their full code is in `examples/`.

**Static 67 x 0.4 = 26.8 + Dynamic 65.9 x 0.6 = 39.5 = FINAL 66 (rounded from 66.3) -> Beta Only. Deployable: no.**
Floors: Static < 70, Execution < 75, assertion rate < 80%: all miss the Limited Release floor (grade already at Beta Only). No veto fired, no P0.

## Research Veto

| Dim | Result |
|---|---|
| M1 Scientific Integrity | PASS. Raghava & Barton 2006 claims (11.5%, 22%, PID4 best r = 0.86) match the paper; PID1-4 definitions match `pwalign::pid`; Capra-Singh claims checked against the authors' script. Minor: "Robinson" table deviates from the published values by up to 5% relative (P2) |
| M2 Practice Boundaries | PASS (no clinical content) |
| M3 Methodological Ground | PASS (advice is sound; defects are implementation errors) |
| M4 Code Usability | PASS (all code parses and runs; imports exist in 1.88; modeltest-ng / iqtree3 / distmat commands run) |

---

## Detailed Outputs

### Input 1 - Canonical (real Pfam PF00042 seed, 73 x 141)
**Prompt:** "Here is the Pfam globin seed alignment. Give me the pairwise identity matrix, conservation per column, Shannon entropy / information content, gap statistics, and the sum-of-pairs score."
**Code:** `run\s04_input1_seed.py` (runs the 8 examples, the SKILL.md blocks, and 16 numeric checks). Note: Biopython's Stockholm reader converts "." to "-", so the FASTA copy has "-" only (`seed_norm.fasta`); the "." case is Input 2.
**What ran:** `capra_singh_jsd, conservation_profile, entropy_analysis, gap_statistics, identity_matrix, kimura_protein_distance, pssm, substitution_counts`: rc 0, 6-238 lines each. SKILL.md blocks: `pairwise_identity` pid1 47.3%; average conservation 37.9%; average gap fraction 18.9%; `alignment_score` -330976.
**Checks against independent implementations (from `out_s04.txt`):**
```
C1a vectorized identity matrix == pairwise_identity(pid1)                       PASS
C1b identical-residue count == numpy elementwise count (all 2628 pairs)          PASS
C1c PID3, PID4 == definitional reference (all 2628 pairs)                        PASS
C1d Skill PID1 == internal-gap PID1                                              PASS on this seed (no terminal-overhang pairs)
C2a per-column conservation == reference                                         PASS
C3a Shannon entropy == scipy.stats.entropy(base 2)                               PASS (diff 1.3e-15)
C3b information_content == KL reference (same background)                        FAIL: max +0.581 bits (27 B/Z residues, 25 columns)
C4  capra_singh_score == scipy JSD + own smoothing                               PASS (0.0049)
C5  gap_statistics total gaps 1943 (18.9%), gap-free columns                     PASS
C6a sum_of_pairs BLOSUM62 186187 == reference                                    PASS
C6b alignment_score == textbook SP                                               FAIL: Skill -330976, textbook (gap/gap = 0) -215960
C7a PSSM == reference (0.0)   C7b Kimura (2023 finite pairs)   C7c substitution total 227180 = brute force    PASS
```
Other observations: average conservation 37.9% (34.3% when >50%-gapped columns are dropped; 5 such columns report 100% conserved from 2-33 residues); `substitution_counts.py` on this PROTEIN alignment prints `Transitions: 5186 / Transversions: 221994 / Ti/Tv ratio: 0.02`; 605 of 2628 pairs are "saturated" (p >= 0.85) for Kimura, expected for a diverse family.
**Scores:** Basic 32 (8/8/8/8) | Specialized 46 (validity 14, code 13, QC 6, repro 8, security 5) | Total 78
**Assertions:**
- [PASS] PID2/PID3/PID4 equal the definitional value for all 2,628 pairs
- [PASS] conservation, entropy, JSD, PSSM, Kimura and substitution totals equal independent implementations
- [FAIL] `alignment_score` equals textbook sum-of-pairs - gap/gap pairs charged
- [FAIL] `information_content` correct with ambiguity letters present - up to +0.58 bits
- [PASS] all shipped examples exit 0 with checked output

### Input 2 - Variant A (real tool output)
**Prompt:** "I aligned the 8 globins to the Pfam globin HMM with hmmalign (and separately with MAFFT). Give me per-column conservation, entropy, information content, PSSM, identity and the BLOSUM62 sum-of-pairs score."
**Code:** `run\s01_wsl_make_data.sh` (MAFFT 7.526, Clustal Omega, hmmbuild/hmmalign in WSL), `run\s07_input2_realtools.py`.
```
mafft_upper        8x155  alphabet -ACDEFGHIKLMNPQRSTVWY  0/155 columns differ, IC/PSSM/SP/identity exact (SP 8607)
clustalo_upper     8x155  same alphabet                     0/155 differ, exact (SP 8403)
hmmalign_afa       8x161  lowercase=284, dots=68
    conservation: 14/161 columns differ from reference (max err 0.375); entropy max err 0.954 bits
    IC: max err 26.24 bits (Skill max IC 29.35 vs reference 5.48); PSSM max err 8.25 log2 units
    BLOSUM62 sum_of_pairs: Skill 6539 vs reference 6976; mean identity 40.3% vs 38.6%
    SKILL.md block 16 (DistanceCalculator): ValueError: Bad letter 'm' in sequence ...
pfam_seed_dot_gaps 73x141 dots=1943 (raw Stockholm text via pyhmmer, "." gaps kept)
    conservation: 69/141 columns differ, avg 44.7% vs 37.9%; IC max 29.46 vs 5.48
    mean pair identity Skill 32.0% vs 19.6% (max pair error 18.4 points)
    SKILL.md block 16: ValueError: Bad letter '.'
```
Note: `hmmalign --outformat A2M` output is ragged (line lengths 29-60) and cannot be read by `AlignIO` as fixed-width: not a Skill defect, recorded only.
**Scores:** Basic 22 (4/5/6/7) | Specialized 29 (validity 8, code 7, QC 2, repro 7, security 5) | Total 51
**Assertions:** [PASS] uppercase MAFFT/Clustal Omega exact | [FAIL] conservation on lowercase inserts | [FAIL] IC within physical maximum | [FAIL] identity on "."-gapped seed | [FAIL] DistanceCalculator snippet runs on these inputs

### Input 3 - Edge (hand-computed, synthetic) + real pairs vs pwalign::pid
**Prompt:** "For this 3-sequence protein alignment (terminal gaps, an internal gap, a gap-only column) give PID1-4 for seq1 vs seq2, per-column conservation and entropy, gap stats, the simple SP score, BLOSUM62 SP score and Kimura distance."
Alignment (synthetic): `s1 AC-DEF--`, `s2 -CGDEFHK`, `s3 ACGN-FHR`. Hand derivations (done before running):
- s1/s2: 4 identical (C, D, E, F); both-residue columns 4; internal gap column 1 (col 3); ungapped lengths 5 and 7. PID1 (aligned + internal gaps) = 4/5 = 80%; PID1 as coded (any column with a residue) = 4/8 = 50%; PID2 = 4/4 = 100%; PID3 = 4/5 = 80%; PID4 = 4/6 = 66.7%.
- Conservation [1,1,1,2/3,1,1,1,1/2], mean 0.8958; entropy [0,0,0,0.9183,0,0,0,1.0]; gap fraction 1/3 in columns 1,3,5,7,8 (first hand value of 2/3 for column 8 was wrong; recounted).
- Simple SP (match +1, mismatch -1, gap -2) = -3+3-3-1-3+3-3-5 = -12; adding an all-gap column adds 3 gap/gap pairs x -2 = -6 under the Skill's rule, 0 under the textbook rule.
- BLOSUM62 SP = 4+27+6+8+5+18+8+2 = 78. Kimura(s2, s3): 6 both-residue columns, 4 identical, p = 1/3, d = -ln(1 - 1/3 - 0.2/9) = 0.4393. Substitutions {D-N: 2, K-R: 1}.
**Skill output:** PID1 50.0%, PID2 100.0%, PID3 80.0%, PID4 66.7%; conservation/entropy/gaps equal hand values; average conservation 0.8958 (0.7963 with one all-gap column added); `alignment_score` -12 (-18 with the all-gap column); `sum_of_pairs` 78.0; Kimura 0.43937; substitution counts equal.
**Real pairs vs `pwalign::pid`** (`run\s03_pid_ref.R`, BLOSUM62, open 10 / ext 0.5, human/whale globins; overlap and local pairs rebuilt as MSA rows with terminal overhang):
```
pair                          Skill pid1 | R PID1   pid2/3/4 (Skill == R in all pairs)
HBA vs HBB global (149 cols)  43.62      | 43.62    46.43 / 45.77 / 44.98
MYG vs HBB global (155 cols)  24.52      | 25.50    26.03 / 25.85 / 25.25
HBA full vs HBB fragment      25.00      | 40.66    43.53 / 40.66 / 31.76   (overlap, 148 cols with overhang)
HBB fragment vs HBA (local)   24.50      | 42.05    45.12 / 40.66 / 31.76
```
**Scores:** Basic 28 (7/7/7/7) | Specialized 44 (validity 12, code 14, QC 5, repro 8, security 5) | Total 72
**Assertions:** [PASS] PID2-4 hand values | [FAIL] PID1 = 80% | [PASS] conservation/entropy/gap profile hand values | [PASS] SP 78 / -12, Kimura 0.4393, substitutions | [FAIL] all-gap column leaves mean conservation and SP unchanged

### Input 4 - Variant B (real DNA, MAFFT default lowercase)
**Prompt:** "Here is my MAFFT nucleotide alignment of beta-globin CDS from six mammals. What is the Ti/Tv ratio, the per-column conservation and information content (DNA), gap statistics and pairwise identity?"
**Code:** `run\s08_input4_dna.py` on `hbb6_mafft_default.fa` (alphabet `-acgt`) and an upper-cased copy.
```
lower (MAFFT default): reference ti=428 tv=355 ratio 1.21 | Skill prints Transitions: 0 / Transversions: 783 / Ti/Tv ratio: 0.00
                       DNA IC Skill max 29.90 bits (max possible 2.00); entropy_analysis.py header: "Treating as DNA (uniform background)"; DNA PSSM max error 4.64
upper                  Ti/Tv 428/355 = 1.21 exact; IC 2.000; PSSM exact
both                   conservation avg 0.926; mean identity 87.8% (PID2 88.2%, PID4 88.0%)
```
**Scores:** Basic 21 (4/4/6/7) | Specialized 28 (validity 7, code 8, QC 2, repro 6, security 5) | Total 49
**Assertions:** [PASS] uppercase Ti/Tv correct | [FAIL] lowercase Ti/Tv | [FAIL] DNA IC within 0-2 bits | [FAIL] DNA PSSM on lowercase | [PASS] conservation and identity unaffected by consistent case

### Input 5 - Stress (synthetic 300 x 300 and 2000 x 300)
**Prompt:** "I have a 300-sequence protein alignment. Compute the full identity matrix, average conservation profile, sum-of-pairs score against BLOSUM62 and the Kimura distance matrix."
**Data:** SYNTHETIC (`run\data\synthetic_stress_*.fasta`, numpy seed 20260920/21: 8 clades, 20% N-terminal and 20% C-terminal gap runs, 15% internal gap blocks). **Code:** `run\s12_input5_stress.py`.
```
S1 identity_matrix_vectorized == numpy 3-D broadcast reference (300x300)      PASS  1.6 s
S2 Skill PID1 == internal-gap PID1                                            FAIL  mean -1.42 pts, worst -11.77 pts
   naive pairwise_identity: 0.16 s per 4,950 pairs -> N=2000 approx 1 min
S3 conservation_profile == mean(cols[i-5..i+4])                               PASS  1.5 s
S4 sum_of_pairs == count-based reference 18,093,751                           PASS  28 s (13M residue pairs)
   alignment_score -3,205,453 (2 s); Kimura all pairs 4 s
S5 Kimura == reference (435 sampled pairs)                                    PASS
S6 2000x300 identity matrix completes, spot check exact                       PASS  66 s
```
**Scores:** Basic 32 (8/8/8/8) | Specialized 48 (validity 14, code 14, QC 6, repro 9, security 5) | Total 80
**Assertions:** [PASS] identity matrix | [PASS] SP equals count-based reference | [PASS] Kimura and profile | [PASS] 2000x300 completes | [FAIL] PID1 equals internal-gap definition

### Input 6 - Scope Boundary (publication-grade distances)
**Prompt:** "I need distances for tree building from this protein alignment; which substitution model fits and how do I correct the distances?"
**Code:** `run\s09_install_modeltest.sh` (new side env, no existing env changed), `run\s10_wsl_distance_tools.sh`, `run\s11_input6_distance_py.py`.
```
modeltest-ng -i alignment.fasta -d nt -t ml            exit 0  Best BIC K80+I (BIC 2658.68, weight 0.40); AIC TPM2uf+I
modeltest-ng -i alignment.fasta -d aa -t ml -p 4       exit 0  Best BIC DAYHOFF+G4; AIC LG+I+F
iqtree3 -s alignment_aa.fasta -m LG                    writes .mldist (SKILL.md ".mldist output" claim true)
EMBOSS distmat -protmethod 2 (Kimura) vs kimura_protein_distance.py: 28/28 pairs, worst diff 0.0001
DistanceCalculator('blosum62') == hand formula (28 pairs)   PASS
closest pair (HBB_HUMAN / HBB_PANTR) agrees with IQ-TREE   PASS
```
The Skill stays in scope: it explicitly says not to hand-code models for publication and points to ModelTest-NG / IQ-TREE.
Stale statement found: SKILL.md says `.get((c1, c2), 0)` on a BLOSUM `Array` silently returns 0; in Biopython 1.88 `BL.get(('A','A'), 0)` returns 4.0 (`run\s14_blosum_get.py`).
**Scores:** Basic 34 (9/8/8/9) | Specialized 52 (validity 18, code 13, QC 7, repro 9, security 5) | Total 86
**Assertions:** [PASS] modeltest-ng commands run | [PASS] DistanceCalculator == formula | [PASS] Kimura == distmat | [PASS] .mldist claim + closest pair | [FAIL] Biopython Array API statement accurate

### Input 7 - Adversarial / messy (synthetic)
**Prompt:** "Here's the alignment my collaborator sent (mixed case, dots, X/B/Z/U, one empty-looking sequence). What is the percent identity, conservation and information content?"
Alignment (synthetic): `MKV.LAAGXW / mkvALAAGVw / MKVBLAZGVW / MKVULAA*VW / ---------- / MKV-LAAGVW`. **Code:** `run\s13_input7_messy.py`.
```
row0 vs row1 PID2: Skill 40.0%, case/gap-normalised reference 88.9%
all-gap row vs row0: pid1..pid4 = 0 (no NaN, no warning); identity-matrix diagonal for that row is 0.0
IC per column Skill  [9.64, 8.51, 8.41, 21.34, 3.44, 3.68, 8.2, 8.27, 8.41, 10.24]
IC per column ref    [5.48, 4.07, 3.94, 3.68, 3.44, 3.68, 3.68, 3.76, 3.94, 6.23]
sum_of_pairs Skill 288 vs reference 388 (lowercase, U, ".", "*" pairs silently skipped)
BLOSUM62: U, J, lowercase and "." raise IndexError (caught and skipped by the Skill's except clause); X -> 0.0, "*" -> -4.0
degenerate: 1 sequence -> average identity NaN (numpy warning); 2 identical -> 1.0; unequal lengths -> ValueError "Sequences must all be the same length"; all-gap columns -> average identity -1.0
entropy_analysis.py guesses DNA for a valid protein alignment whose first row lacks E/F/I/L/P/Q/Y/W
```
**Scores:** Basic 19 (4/4/5/6) | Specialized 26 (validity 6, code 8, QC 1, repro 6, security 5) | Total 45
**Assertions:** [FAIL] case-insensitive identity | [FAIL] all-gap sequence flagged | [FAIL] IC bounded | [PASS] degenerate input fails clearly or sane | [FAIL] protein background chosen for a protein alignment

---

## Other verifications (no score impact beyond the above)

- **Capra-Singh JSD vs the authors' script** (`run\s16_capra_reference.py`; authors' `score_conservation.py` downloaded to `run\data\`, Python 2, four functions re-typed): Skill raw JSD equals the authors' formula (max diff 0.0016, Spearman 1.0). Skill (Robinson background, unweighted) vs authors' default (BLOSUM62 background + Henikoff weights): Spearman 0.979, top-10 overlap 9/10, top-30 25/30. The Skill's "effectively equivalent ranking" claim holds; it omits sequence weighting, which the text does not mention.
- **Percent-identity definitions** (Raghava & Barton 2006, BMC Bioinf 7:415, fetched from PMC1592310, and the `pwalign::pid` docs): PID1 = identical / (aligned + internal gap positions); PID2 = / aligned; PID3 = / shorter length; PID4 = / mean length. Skill's PID2-4 correct; PID1 code counts terminal-overhang columns.
- **Modern API** (`run\s15_align_api.py`): frontmatter `primary_tool: Bio.Align`, but `Bio.Align.read()` objects raise `AttributeError: 'Alignment' object has no attribute 'get_alignment_length'` in `gap_profile`, `sum_of_pairs`, etc. `AlignIO` still works in 1.88 with no deprecation warning.
- **Bio.Phylo `DistanceCalculator('identity')`** is not a usable second implementation for PID2: with no scoring matrix it does not skip gaps ("-" == "-" counts) and divides by alignment length (`run\s05_dc_probe.py`). Recorded so no fixer tries it.
- Robinson table in the Skill sums to 1.0036 and differs from the published NCBI Robinson frequencies by up to 0.0022 absolute (N 0.0427 vs 0.04487, K 0.0596 vs 0.05744). Rank correlation of IC with either table 0.974.

## Key strengths
- Core statistics are exact on clean uppercase input and were confirmed by independent implementations (numpy, scipy, pwalign, EMBOSS distmat, authors' Capra-Singh script, hand computation).
- Unusually careful prose on PID definitions, IC background, SP bias and hand-off to ModelTest-NG / IQ-TREE; the hand-off commands run.
- Small, deterministic, read-only, complete, with cross-references that resolve.

## Optimization recommendations

[P1] No case / gap-glyph / ambiguity normalisation (silent wrong output)
  Observed in: Inputs 2, 4, 7
  Problem: lowercase (MAFFT nucleotide default, hmmalign inserts), "." gaps and B/Z/X/U letters are distinct "residues": Ti/Tv 0.00 vs 1.21, DNA IC 29.9 vs 2.0 bits, dot-gapped Pfam identity 32.0% vs 19.6%, SP drops pairs, DistanceCalculator raises.
  Root cause: every function assumes uppercase A-Z plus "-" and never validates the alphabet.
  Fix: add a normalise step (upper-case, "." and "~" to "-") plus an alphabet check to Required Import and every example; note that MAFFT nucleotide output is lowercase.

[P1] PID1 code does not implement its stated definition
  Observed in: Inputs 3, 5
  Problem: terminal-overhang columns are counted: 50% vs 80% (hand), 25.0% vs 40.7% (pwalign::pid on a fragment pair), up to -11.8 points on a 300-sequence alignment; `identity_matrix.py` uses it while the text recommends PID4.
  Root cause: denominator is `a != '-' or b != '-'` with no terminal-gap exclusion.
  Fix: exclude columns outside each sequence's residue span (or rename the metric), add a method argument to `identity_matrix.py` and default it to PID4.

[P1] `alignment_score` charges gap/gap pairs
  Observed in: Inputs 1, 3
  Problem: -330,976 vs textbook -215,960 on the Pfam seed; an all-gap column changes the score; inconsistent with `sum_of_pairs`.
  Root cause: the gap branch does not exclude the both-gap case.
  Fix: score gap/gap pairs 0 and state the convention.

[P1] `information_content` 1e-9 fallback inflates IC by about 26 bits per unknown letter
  Observed in: Inputs 1, 2, 4, 7
  Problem: B/Z/X/U/lowercase/N letters push IC to 29 bits on real alignments; +0.58 bits on the Pfam seed.
  Root cause: `background.get(r, 1e-9)`.
  Fix: drop letters outside the background (report the count) and renormalise before the KL sum.

[P2] `substitution_counts.py` prints Ti/Tv for protein and misses lowercase/RNA (Inputs 1, 4): detect nucleotides, upper-case, map U to T, print Ti/Tv only for DNA/RNA.
[P2] Conservation ignores occupancy (Inputs 1, 3): columns with 2 residues of 73 score 100%; all-gap columns score 0 and dilute the mean; add `min_occupancy` or NaN.
[P2] Stale statements (Inputs 6, 1): `.get` on Array claim; `primary_tool: Bio.Align` vs `AlignIO`; Robinson table approximate; "Laplace add-one" mislabel; Common Errors table (ZeroDivisionError, Negative IC) does not match the code.
[P2] Minor (Inputs 1, 3, 7): "build a substitution matrix" yields counts only; the pairwise-substitutions snippet puts "-" in the matrix; `conservation_profile` window is [i-5, i+4]; all-gap sequence gives 0% not NaN; no shipped expected outputs.

## Files
- Report: `F:\OpenScience\audits\bio-alignment-msa-statistics\eval_report_bio-alignment-msa-statistics_result.json`
- Scripts and data: `F:\OpenScience\audits\bio-alignment-msa-statistics\run\` (`ref.py` independent implementations, `skill_blocks.py` verbatim SKILL.md runner, `s00`-`s16`, `s99_build_report.py`; `data\` real public files plus files labelled `synthetic_*` and `data_tiny_synthetic` in `work_in3\`; `out_s*.txt` raw outputs).
