> **Audit record for `bio-alignment-msa-statistics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@7c5cb44](https://github.com/mrsonord2240/bioSkills/tree/7c5cb44b27b2edaabdf5129fdd541523f4b9ef27/alignment/msa-statistics) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-alignment-msa-statistics (re-audit of the fixed Skill)

Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@7c5cb44b27b2edaabdf5129fdd541523f4b9ef27:alignment/msa-statistics` (worktree `F:\OpenScience\wt\al-msastats`, read only; copied byte-identical to `run\skill\`, `diff -r` clean, no `__pycache__` written by this audit)
Pre-fix audit: 66, Beta Only, not deployable (archived at `F:\OpenScience\audits\_pre-fix-20260920\bio-alignment-msa-statistics\`). Re-auditor: a different agent from the first auditor and from the fixer.
Category: Data Analysis (Research Veto applies) | Mode: D (SKILL.md patterns + 8 runnable examples + selftest) | Complexity: Complex, N = 9 (7 first-audit inputs re-run as regression + 2 new)
Env: `F:\OpenScience\audit-envs\alignment` (Windows venv Biopython 1.88, numpy 2.0.2, scipy 1.18.1; R 4.4.3 via `r.sh` with pwalign 1.2.0 / Biostrings 2.74.1; WSL `alignment` env numpy 2.5.3; WSL `aln-mtng` ModelTest-NG 0.1.7, iqtree3, EMBOSS distmat).
Every script is in `run\`; every check asserts on numeric content, never on an exit code. The fix log was read but not used as evidence.

## Result

| | Pre-fix | Now |
|---|---|---|
| Static (25 criteria) | 67 | **86** |
| Execution average | 65.9 | **89.4** |
| Assertion pass rate | 18/35 (51%) | **43/45 (96%)** |
| Final | 66 Beta Only | **88 Production Ready, deployable** |

**Executed 9/9 inputs.** 310 of 311 scripted checks pass; the one failure and two probe findings are P2. No veto, **no open P0, no open P1**. Production Ready floors: static 86 >= 80, execution 89.4 >= 85, Layer 1 avg 35.1 >= 32, Layer 2 avg 54.3 >= 48, assertions 96% >= 90%: all met.

## Skill Veto (Step 1)

| Dim | Result | Basis |
|---|---|---|
| T1 Stability | PASS | 8/8 examples and selftest.py exit 0 with the expected output on real and synthetic data; 12 non-stub SKILL.md blocks run verbatim; no loops or crashes |
| T2 Contract | PASS | frontmatter name, description, tool_type, primary_tool (now `Bio.AlignIO`, matches the code), license |
| T3 Determinism | PASS | no randomness in the Skill; identical numbers across repeated runs, and selftest.py passes on numpy 2.0.2 (Windows) and 2.5.3 (WSL) |
| T4 Security | PASS | grep for eval/exec/subprocess/os.system/urllib/socket/requests over the Skill: none; read-only |

Shipped-means-present: `SKILL.md`, `usage-guide.md`, all 8 `examples/*.py` (incl. `msa_utils.py`, `selftest.py`) and `examples/data/example_{protein,dna}.fasta` exist; cross-referenced `alignment/msa-parsing/examples/{henikoff_weights,neff,mi_apc}.py` exist (`a01`). No `references/` folder is referenced.

## Static score (Step 2): 86 / 100

| Category | Score | Note |
|---|---|---|
| Functional Suitability | 11/12 | Every promised use covered; all numbers checked against independent implementations; minor: `average_conservation` crash on all-NaN alignment, Kimura inf from p = 0.85 though the formula is finite to 0.854 |
| Reliability | 10/12 | Normalise step, `check_alphabet`, NaN for undefined values, skipped-pair counts; gaps: ZeroDivisionError edge, `is_nucleotide` silent misclassification above 10% IUPAC |
| Performance/Context | 6/8 | 484-line SKILL.md, 17 python blocks (5 stubs); inline SP is O(N^2 L) (28 s at 300 x 300); identity matrix vectorized (2000 x 300 in 30 s) |
| Agent Usability | 14/16 | Clear goal/approach, normalise-first, "Higher means" column, Common Errors keyed to silent symptoms; no NaN-ranking guidance |
| Human Usability | 6/8 | Natural prompts; case/gap variants handled; CLI `guess_format` FASTA/Stockholm only; ragged A2M has no loader |
| Security | 11/12 | Read-only, no secrets, alphabet and method validation |
| Maintainability | 10/12 | Shared `msa_utils.py`, hand-derived selftest (16/20 mutants caught); inline SKILL.md functions duplicate example code and are untested |
| Agent-Specific | 18/20 | On-target trigger, layered disclosure, pointers to msa-parsing/multiple-alignment/phylogenetics, twilight-zone and distance-model escape hatches |

## Test inputs (Step 4)

```
Skill: bio-alignment-msa-statistics | Category: 3 Data Analysis | Mode: D | Complexity: Complex -> 9 inputs (7 regression + 2 new)
Input 1 (Canonical)      : Pfam PF00042 globin seed (real, 73x141): identity, conservation, entropy/IC, gaps, SP, PSSM, JSD  [dashed + dotted copies]
Input 2 (Variant A)      : real tool output: MAFFT 7.526, Clustal Omega 1.2.4, hmmalign AFA (lowercase inserts + dots), Pfam seed re-aligned by MAFFT
Input 3 (Edge)           : PID1-4 vs pwalign::pid on 169 OWN real pairwise alignments (not the fixer's) + 6 hand-computed cases
Input 4 (Variant B)      : six real HBB CDS, MAFFT default (lowercase): Ti/Tv, DNA IC, conservation, identity
Input 5 (Stress)         : synthetic 300x300 and 2000x300 protein alignments (first-audit data, seed 20260920/21)
Input 6 (Scope Boundary) : publication-grade distances: ModelTest-NG / IQ-TREE / distmat hand-off + DistanceCalculator
Input 7 (Adversarial)    : messy collaborator alignment (synthetic) + degenerate alignments + probes of the fix's new behaviours
Input 8 (Variant B, NEW) : Rfam RF00050 FMN riboswitch seed (real RNA, 146x221, U, 38% gaps, Stockholm) + lowercase/dotted FASTA copy
Input 9 (Edge, NEW)      : Pfam PF00069 kinase seed (real protein, 37x419, 36% dots, staggered fragments)
```

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 35 | 55 | 90 | 5/5 | OK |
| 2 | Variant A | 35 | 55 | 90 | 5/5 | OK |
| 3 | Edge | 36 | 56 | 92 | 5/5 | OK |
| 4 | Variant B | 36 | 55 | 91 | 5/5 | OK |
| 5 | Stress | 35 | 55 | 90 | 5/5 | OK |
| 6 | Scope Boundary | 36 | 54 | 90 | 5/5 | OK |
| 7 | Adversarial | 33 | 50 | 83 | 4/5 | OK (one defect) |
| 8 | Variant B (new) | 35 | 55 | 90 | 5/5 | OK |
| 9 | Edge (new) | 35 | 54 | 89 | 4/5 | OK (one hazard) |

**Execution Average: 89.4 / 100** (Layer 1 avg 35.1/40, Layer 2 avg 54.3/60). **Assertion Pass Rate: 43/45.**
**Static 86 x 0.4 = 34.4 + Dynamic 89.4 x 0.6 = 53.6 = FINAL 88 -> Production Ready. Deployable: yes.**

## Research Veto

| Dim | Result |
|---|---|
| M1 Scientific Integrity | PASS. Numeric claims re-verified: 37.9% -> 34.3% mean conservation, Ti/Tv 1.21, PID1-4 vs `pwalign::pid`, Robinson table equals the published NCBI values and sums to 1.0, Capra-Singh Spearman 0.979 / top-10 9/10 against the authors' script (`b10`) |
| M2 Practice Boundaries | PASS (no clinical content) |
| M3 Methodological Ground | PASS (PID definitions, KL IC against an empirical background, occupancy-aware conservation, hand-off of publication-grade distances) |
| M4 Code Usability | PASS (all code parses and runs; the only exception found is an all-NaN edge case, P2) |

---

## Independent look at what the fix changed

### Do the new self-tests test anything? (`a01`, mutation testing)
`selftest.py` passes on Windows numpy 2.0.2 and WSL numpy 2.5.3 (11 OK lines). It is not vacuous: 20 breaks were planted in scratch copies (each replacement asserted present, so none is a no-op) and `selftest.py` failed on 16.

```
CAUGHT   PID1 old denominator (function) | PID1 vectorized span mask removed | PID4 uses min | undefined identity -> 0 |
         IC back to background.get(r,1e-9) | entropy in nats | min_occupancy removed | profile window uncentred |
         normalize: no upper-case | no '.'->'-' | no U->T | Ti/Tv transitions set wrong | N pairs counted as transversions |
         PSSM n counts unknown letters | PSSM pseudocount unweighted | Kimura 0.2 -> 0.25
SURVIVED is_nucleotide always False | Capra-Singh gap penalty removed | Capra-Singh lambda smoothing removed | gap_statistics.py logic
```
The gap/gap = 0 convention and the SP skip semantics live only in SKILL.md (`alignment_score`, `sum_of_pairs`), so no shipped test covers them; my own runs do (P2 #4).

### PID1 terminal-overhang exclusion (`b03_*`)
Own data, not the fixer's: 84 globin pairs (8 UniProt globins x global/local/overlap, BLOSUM62 10/0.5), 40 random Pfam-seed pairs (random fragment truncation, BLOSUM45 12/1, five pairwise modes incl. global-local and local-global) and 45 HBB CDS pairs (DNA 1/-3, gap 5/2). `pwalign::pid` (R, pwalign 1.2.0) supplies PID1-4.
```
V0 pwalign's aligned strings as returned (22 carry end gaps): Skill PID1/PID2 == pwalign on 169/169 (max diff 0.00000); PID3/PID4 == pwalign where no flank exists
V1 same pairs rebuilt as MSA rows with unaligned flanks staggered in (88 pairs): PID1, PID2, PID3, PID4 == pwalign, max diff 0.00000
   old any-residue denominator would have disagreed on 22/169 (V0) and 88/88 (V1), up to 34.1 points
   per-sequence "internal gap" definition (the first audit's reference) disagrees with pwalign on 35 of the 88: the span definition is the right one
hand (derived before running): s1/s2 = 80/100/80/66.7; XXABC--/--ABCYY = 100/100/60/60; AB-CD/A-XCD = 60/100/75/75; no aligned pair = NaN,NaN,0,0; all-gap row = NaN x4  -> all equal
```
Discovery worth recording: `pwalign::pid` PID3/PID4 use the full input sequence lengths, not the aligned region (`b03b`), so aligned-region-only strings cannot test PID3/PID4 for local/overlap alignments; my first comparison was wrong for that reason and the test was corrected, not the Skill.

### Gap/gap scoring, IC renormalisation (`b01`, `b02`, `b07`)
`alignment_score` on the real Pfam seed: -215960 == count-based textbook SP (gap/gap = 0); it was -330976. `information_content` (example and SKILL.md block) equals `scipy.special.rel_entr` KL with the published Robinson background to 8.9e-16 on the seed (27 B/Z residues dropped; pre-fix +0.58 bits), stays <= 6.23 bits on the messy alignment (pre-fix 21.3), and equals 2.000 bits max for DNA (pre-fix 29.90).

### min_occupancy = 0.5 NaN default: does it silently change results or break documented use?
It changes gappy-alignment means on purpose and says so: Pfam globin seed 37.93% -> 34.29% (118 of 141 columns), kinase seed 45.1% -> 40.9% (262 of 419), RNA riboswitch 69.1% -> 72.0% (139 of 221). `min_occupancy=0` restores the old numbers. Two things break, both P2 (`b07`, `b11`):
- SKILL.md `average_conservation` raises `ZeroDivisionError` when no column reaches `min_occupancy` (4-fragment alignment, every column 25% occupied); `conservation_profile.py` on the same file prints `nan% over 0 of 16 columns` plus a numpy RuntimeWarning.
- Ranking column scores that now contain NaN is silently wrong. The shipped prompt "Which columns are most conserved?" answered with `sorted(range(L), key=lambda i: -cons[i])[:10]` on the Pfam seed returns values 0.37-1.00 where the NaN-free top-10 is 0.63-1.00 (columns [17, 11, 7, ...] vs [17, 77, 11, ...]); kinase seed: 10th value 0.70 vs 0.97. Pre-fix the ranking was also wrong (5-6 of the top 10 were sparse columns scoring 100%), so the NaN default is an improvement that still needs one sentence of guidance.

### usage-guide.md dedup: was anything the agent needs lost?
Compared line by line with the pre-fix guide (`git show 354b499:...usage-guide.md`). Prerequisites -> "Version Compatibility" (install line); Key Metrics table -> "Quick Reference" (new "Higher means" column); Tips 1-7 -> "Percent Identity Definitions", `ignore_gaps` text, "Alignment Quality Metrics" approach (BLOSUM62 / DNA match-mismatch), "When to Worry" table (guide-tree artifacts, twilight zone), "Quantifying Alignment Uncertainty" (topology sensitivity). The example prompts, the quick start and "What the agent will do" (with the normalise step) remain. **Nothing lost.** The "Build a substitution matrix" prompt was removed together with the claim (the Skill only produces counts).

---

## Detailed outputs

### Input 1 - Canonical (real Pfam PF00042 seed, 73 x 141)
**Prompt:** "Here is the Pfam globin seed alignment. Give me the pairwise identity matrix, conservation per column, Shannon entropy / information content, gap statistics, and the sum-of-pairs score."
**Code:** `run\b01_input1_seed.py` (copies the examples, runs the SKILL.md blocks verbatim, compares 20+ statistics with independent references). Run on `seed_norm.fasta` ("-") and `seed_dot.fasta` (1943 "." gaps, as Pfam writes).
```
[block 0] OK  WARNING: letters outside the alphabet: {'Z': 12, 'B': 15}     [block 13] Alignment score: -215960
[block 4] Average conservation: 34.3% over 118 columns                    [block 1] pid1: 47.3%
CHECK identity PID1-4 (vectorized + function) == independent, all 2628 pairs: PASS  max diff 0
CHECK information_content == scipy rel_entr KL: PASS  max diff 8.9e-16; max IC 5.507 bits
CHECK capra_singh_score == scipy JSD x occupancy + smoothing: PASS 1.1e-16
CHECK sum_of_pairs == reference PASS 186187.0 ; alignment_score == count-based textbook SP PASS -215960 (charging gap/gap: -330976)
CHECK PSSM == independent (B/Z dropped from n) PASS ; Kimura == reference PASS (2023 finite, 605 saturated) ; substitutions 227180 == brute force PASS
CHECK dash vs dot variants give identical statistics: PASS      SUMMARY 40 of 40 checks PASS
```
**Scores:** Basic 35 (9/9/8/9) | Specialized 55 (validity 18, code 14, QC 9, repro 9, security 5) | Total 90
**Assertions:** [PASS] PID1-4 == reference, identical for "-" and "." | [PASS] IC == KL reference, <= 6.23 bits | [PASS] alignment_score gap/gap = 0 | [PASS] mean conservation 34.29% over 118 columns | [PASS] all blocks and examples run

### Input 2 - Variant A (real MAFFT, Clustal Omega, hmmalign AFA, Pfam seed via MAFFT)
**Prompt:** "I aligned the 8 globins to the Pfam globin HMM with hmmalign (and separately with MAFFT). Give me per-column conservation, entropy, information content, PSSM, identity and the BLOSUM62 sum-of-pairs score."
**Code:** `run\b02_input2_real_tool_outputs.py` on the first audit's tool outputs (`_first_audit_data_provenance\s01_wsl_make_data.sh`; MAFFT 7.526, Clustal Omega 1.2.4, HMMER 3.4). `battery.py` holds the reusable checks.
```
mafft_default 8x155      SP 8607   PID1-4 exact  IC max 6.232 (bound 6.23)      12/12 checks
clustalo      8x155      SP 8403   exact                                          12/12
hmmalign_afa  8x161      lowercase 284, dots 68: IC max 5.507 (pre-fix 29.35), SP 6976 (pre-fix 6539), mean PID1 39.3%   12/12
seed_mafft_default 73x142 Kimura: 92 pairs in 0.85 <= p < 0.854 are inf in the Skill, finite in the formula (documented cut-off)   12/12
A2M: `AlignIO.read(globins_hmmalign.a2m,'fasta')` -> ValueError: Sequences must all be the same length (hmmalign A2M leaves insert columns unpadded)
DistanceCalculator SKILL.md block runs on all four (pre-fix: ValueError Bad letter 'm' / '.')      SUMMARY 82 of 82 checks PASS
```
**Scores:** Basic 35 (9/8/9/9) | Specialized 55 (18/14/9/9/5) | Total 90
**Assertions:** [PASS] MAFFT/Clustal exact | [PASS] hmmalign IC within bound | [PASS] SP and alignment_score on hmmalign | [PASS] DistanceCalculator block runs | [PASS] identity on hmmalign equals reference

### Input 3 - Edge (PID1-4 vs pwalign::pid, terminal overhangs)
**Prompt:** "Give me PID1-4 for these pairs (terminal gaps, an internal gap, a gap-only column) and tell me which identity definition you used."
**Code:** `run\b03_pid_pwalign.R` (via `r.sh`), `run\b03_pid_compare.py`, `run\b03b_pid4_probe.py`, `run\b03c_debug.py`. Results in the section above.
**Scores:** Basic 36 (9/9/9/9) | Specialized 56 (19/14/9/9/5) | Total 92
**Assertions:** [PASS] PID1/PID2 == pwalign on 169 alignments | [PASS] flank-staggered PID1-4 == pwalign | [PASS] six hand cases | [PASS] vectorized == function | [PASS] test discriminates (old denominator disagrees)

### Input 4 - Variant B (real DNA, MAFFT default lowercase)
**Prompt:** "Here is my MAFFT nucleotide alignment of beta-globin CDS from six mammals. What is the Ti/Tv ratio, the per-column conservation and information content (DNA), gap statistics and pairwise identity?"
**Code:** `run\b04_input4_dna_mafft.py` on `hbb6_mafft_default.fa` (2658 lowercase letters) and `hbb6_mafft_upper.fa`.
```
substitution_counts.py hbb6_mafft_default.fa:  Transitions: 428   Transversions: 355   Ambiguity-code pairs: 0   Ti/Tv ratio: 1.21   (pre-fix 0.00)
DNA IC max 2.0000 (pre-fix 29.90); entropy_analysis.py: "Treating as DNA (uniform background)", max entropy 2.000
lower == upper: Ti/Tv, IC max, mean PID1 identical to 1e-15                                SUMMARY 36 of 36 checks PASS
```
**Scores:** Basic 36 (9/9/9/9) | Specialized 55 (18/14/9/9/5) | Total 91
**Assertions:** [PASS] Ti/Tv 428/355 | [PASS] IC <= 2 bits | [PASS] case-invariance | [PASS] DNA detected, PSSM DNA background | [PASS] SKILL.md IC block with DNA_UNIFORM

### Input 5 - Stress (synthetic 300 x 300, 2000 x 300)
**Prompt:** "I have a 300-sequence protein alignment. Compute the full identity matrix, average conservation profile, sum-of-pairs score against BLOSUM62 and the Kimura distance matrix."
**Data:** SYNTHETIC (first audit, numpy seed 20260920/21, 8 clades, terminal gap runs, internal gap blocks). **Code:** `run\b08_input5_stress.py`.
```
300x300: PID1-4 == numpy reference on 4000 pairs; sum_of_pairs 18093751 == count-based BLOSUM62 SP; alignment_score -3140959 == textbook; blocks 142 s
CLI at 300x300: identity 1.1 s, conservation 0.5 s, entropy 0.5 s, Kimura 3.9 s
2000x300 identity matrix: PID1 30 s, PID4 27 s, symmetric, 3000 sampled pairs == reference     SUMMARY 19 of 19 checks PASS
```
**Scores:** Basic 35 (9/9/8/9) | Specialized 55 (18/14/9/9/5) | Total 90
**Assertions:** all 5 PASS (PID1-4, SP, alignment_score + Kimura, 2000 x 300 completes, CLI runs)

### Input 6 - Scope Boundary (publication-grade distances)
**Prompt:** "I need distances for tree building from this protein alignment; which substitution model fits and how do I correct the distances?"
**Code:** `run\b09_wsl_distance_tools.sh` (WSL), `run\b09_input6_distance_py.py`.
```
modeltest-ng -d nt -t ml   exit 0  Best BIC K80+I (2658.68)         modeltest-ng -d aa -t ml -p 4  exit 0  Best BIC DAYHOFF+G4 (3268.87)
iqtree3 -m LG writes .mldist (claim true); closest pair HBB_HUMAN/HBB_PANTR agrees with Skill Kimura
Skill Kimura == EMBOSS distmat -protmethod 2: 28/28 pairs, worst diff 0.00005; DistanceCalculator(blosum62) == hand formula, max diff 0
SKILL.md: "do NOT pick a model by rule of thumb", ModelTest-NG hand-off, hand-coded corrections exploratory only      SUMMARY 5 of 5
```
**Scores:** Basic 36 (9/9/9/9) | Specialized 54 (18/14/8/9/5) | Total 90
**Assertions:** all 5 PASS (the pre-fix stale `.get` claim is gone from SKILL.md)

### Input 7 - Adversarial (messy collaborator alignment + new-behaviour probes)
**Prompt:** "Here's the alignment my collaborator sent (mixed case, dots, X/B/Z/U, one empty-looking sequence). What is the percent identity, conservation and information content?"
Alignment (synthetic): `MKV.LAAGXW / mkvALAAGVw / MKVBLAZGVW / MKVULAA*VW / ---------- / MKV-LAAGVW`. **Code:** `run\b07_input7_messy_and_edges.py`.
```
row0 vs row1 PID2 88.89% (pre-fix 40.0%); all-gap row identity NaN, diagonal NaN, 10 undefined pairs counted, average 81.36%
IC per column [5.48, 4.12, 3.96, 3.68, 3.47, 3.68, 3.68, 3.76, 3.96, 6.23] == drop-and-renormalise reference (pre-fix max 21.3)
check_alphabet: WARNING 5 of 48 residues outside the alphabet: {'*','B','U','X','Z'}
sum_of_pairs 388 == reference; "WARNING: 2 residue pairs outside the matrix alphabet were skipped"; alignment_score -45 (all-gap row leaves it textbook)
SKILL.md DistanceCalculator block: ValueError Bad letter 'U' -- documented verbatim in Common Errors
degenerate: 1 sequence -> NaN, no warning; 2 identical -> 1.0; unequal lengths -> ValueError "Sequences must all be the same length"; all-gap columns -> NaN conservation
PROBE  4 fragments (every column 25% occupied): all 16 columns NaN (was 100% conserved) ; SKILL.md average_conservation -> ZeroDivisionError ; conservation_profile.py prints "nan% over 0 of 16" with a RuntimeWarning
PROBE  DNA + 5% IUPAC (synthetic): is_nucleotide True ; DNA + 12% IUPAC: is_nucleotide False -> "protein (Robinson 1991 background)", IC max 5.70 bits, check_alphabet silent (R/Y/S/W/K/M are amino-acid letters)
SUMMARY 15 of 16 checks PASS
```
**Scores:** Basic 33 (8/7/9/9) | Specialized 50 (17/12/8/8/5) | Total 83
**Assertions:** [PASS] normalisation, PID2 88.9%, IC | [PASS] all-gap NaN and counted | [PASS] SP warns with count | [PASS] check_alphabet names dropped letters | [FAIL] `average_conservation` returns on a fully sparse alignment (ZeroDivisionError)

### Input 8 - NEW, real RNA (Rfam RF00050 FMN riboswitch seed)
**Prompt:** "Here is the Rfam FMN riboswitch seed alignment. Give me the Ti/Tv ratio, per-column conservation and information content for the RNA, the average pairwise identity, and gap statistics."
**Data:** downloaded from `https://rfam.org/family/RF00050/alignment/stockholm` on 2026-09-20 (146 x 221, U, 38.5% gaps). `data\derived\RF00050_lower_dotgaps_SYNTHETIC_TRANSFORM.fasta` is a lowercase/dot-gapped rewrite of the same real alignment. **Code:** `run\b05_new_rna_rfam.py`.
```
Ti/Tv after U->T (load_alignment): ti=216522 tv=189758 ratio 1.141 == independent count; Stockholm == lowercase/dot FASTA on Ti/Tv, IC max, PID1, conservation
82 of 221 columns < 50% residues -> NaN; average conservation 72.0% over 139 columns (69.1% with all occupied columns)
inline block without u_to_t: check_alphabet WARNS ("4217 of 19855 residues outside the alphabet: U"); Ti/Tv would be 126591/71147 with 208542 unclassified pairs
gap_statistics.py: total gaps 12411 and 82 columns > 50% gaps == independent counts        SUMMARY 34 of 34 checks PASS
```
**Scores:** Basic 35 (9/8/9/9) | Specialized 55 (18/14/9/9/5) | Total 90
**Assertions:** all 5 PASS

### Input 9 - NEW, real gappy protein (Pfam PF00069 kinase seed)
**Prompt:** "Here is the Pfam kinase seed alignment. Which columns are conserved, what is the average conservation, how similar are the sequences (report the identity definition), and what is the BLOSUM62 sum-of-pairs score?"
**Data:** InterPro `https://www.ebi.ac.uk/interpro/api/entry/pfam/PF00069/?annotation=alignment:seed`, 2026-09-20 (37 x 419, 5603 "." gaps). **Code:** `run\b06_new_kinase_pfam.py`, `run\b11_nan_ranking_probe.py`.
```
PID1-4 == reference on 666 pairs; mean identity by definition PID1 23.43 / PID2 28.04 / PID3 26.27 / PID4 25.49 (PID2 highest, as SKILL.md says)
SP 186874, alignment_score -137507, IC max 5.507, Kimura, PSSM, JSD == references; Stockholm == dotted FASTA        SUMMARY 40 of 40 checks PASS
average_conservation: 40.9% over 262 of 419 columns (45.1% with min_occupancy=0; 36 sparse columns would score 100%)
b11: naive sorted(key=-cons)[:10] -> values [1,1,1,1,0.89,0.89,0.86,0.81,0.7,0.7]; NaN-free top-10 -> nine 1.0 and 0.97
```
**Scores:** Basic 35 (8/9/9/9) | Specialized 54 (17/14/9/9/5) | Total 89
**Assertions:** [PASS] PID1-4 and variant equality | [PASS] IC/PSSM/JSD/Kimura/SP references | [PASS] occupancy-aware mean | [PASS] blocks run verbatim | [FAIL] ranking the most conserved columns in the presence of NaN is correct following SKILL.md (no NaN guidance)

---

## Other verifications (no score impact beyond the above)

- **Capra-Singh claims** (`b10`): Skill raw JSD equals a Python-3 port of the authors' script to 3.4e-7 on columns without B/Z; Skill vs the authors' default (BLOSUM62 background + Henikoff weights) Spearman 0.979, top-10 overlap 9/10, top-30 25/30: "effectively equivalent ranking, Spearman 0.98, 9/10" holds and the omission of sequence weights is now stated.
- **Factual claims** (`b12`): BLOSUM62 `Array` has B/Z/X/`*`, raises IndexError for U, J, lowercase and "."; `Bio.Align.read()` alignment lacks `get_alignment_length` (exact message in Common Errors); `.substitutions` snippet prints no "-" row/column; Robinson table sums to 1.0 and Trp 1.3% / Leu 9.0% match; max IC 6.23 bits protein, 2 DNA; `identity_matrix.py <file> pid1` prints 19.6% and `pid9` raises a clear ValueError.
- **WSL** (`b12_wsl_selftest.sh`): selftest.py, identity_matrix.py pid1 and substitution_counts.py on numpy 2.5.3 give the same numbers (Ti/Tv 428/355/1.21).
- The fixer's worktree contains gitignored `__pycache__` directories under `examples/` (untracked, not in the commit); no `.pyc` was written by this audit.

## Key strengths
- Every pre-fix silent-wrong result is fixed and verified against independent implementations (numpy, scipy, pwalign, EMBOSS distmat, the authors' Capra-Singh formula, hand computation).
- PID1 equals `pwalign::pid` on 169 own pairwise alignments and 88 staggered-flank MSA rows.
- Normalise-first import, `check_alphabet` and skipped-pair warnings turn silent failures into visible messages; every example runs with no arguments; selftest.py is not vacuous (16/20 mutants).
- usage-guide dedup lost nothing.

## Optimization recommendations (all P2; no P0, no P1)

[P2] `average_conservation` raises ZeroDivisionError when no column qualifies (Input 7)
  Problem: fully sparse alignment; SKILL.md block crashes, the example prints "nan% over 0 columns" with a RuntimeWarning.
  Fix: return (nan, 0) with an explicit message in both places.

[P2] NaN conservation default with no NaN-aware ranking guidance (Inputs 9, 1)
  Problem: `sorted(key=-score)` over NaN-bearing scores silently misorders the "most conserved columns".
  Fix: add a two-line NaN-safe ranking beside Per-Column Conservation and say NaN must be filtered before sort/max.

[P2] `is_nucleotide()` 0.9 threshold misclassifies IUPAC-rich DNA silently (Input 7)
  Problem: 12% R/Y/S/W/K/M -> protein background, IC 5.70 bits, no warning.
  Fix: count the full IUPAC nucleotide set, or print composition and allow an override; document the threshold.

[P2] selftest.py leaves the gap/gap fix, `is_nucleotide` and JSD smoothing untested (Inputs 1, 7)
  Problem: 4 of 20 mutants survive; `alignment_score` / `sum_of_pairs` are SKILL.md-only.
  Fix: move them into a shipped module, assert -12 / 78 / all-gap-column-unchanged, one JSD value and `is_nucleotide` on the DNA example.

[P2] Minor: `guess_format()`, A2M route, Kimura 0.85 band (Inputs 2, 5)
  Problem: non-Stockholm extensions read as FASTA; A2M named with no loader (ragged hmmalign A2M fails in AlignIO); Kimura inf for 0.85 <= p < 0.854 (92 of 2628 seed pairs).
  Fix: extension map or format argument, point A2M loading to alignment-io, state that inf means p >= 0.85 by convention.

## Files
- Report: `F:\OpenScience\audits\bio-alignment-msa-statistics\eval_report_bio-alignment-msa-statistics_result.json`
- Scripts and data: `F:\OpenScience\audits\bio-alignment-msa-statistics\run\` (`a01` shipped examples + mutation tests, `b01`-`b12` inputs and probes, `battery.py` shared checks, `ref.py` independent references, `skill_blocks.py` verbatim SKILL.md runner, `b99_build_report.py` JSON builder, `skill\` the audited copy, `data\` real public files + `derived\` + `new\`, `out_*.txt` raw outputs, `_first_audit_data_provenance\` scripts that made the first audit's tool-output data). Synthetic files are labelled `synthetic_*`, `SYNTHETIC_TRANSFORM` or described above.
