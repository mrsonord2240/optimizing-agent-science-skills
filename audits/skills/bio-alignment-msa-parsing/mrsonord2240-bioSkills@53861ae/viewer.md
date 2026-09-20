> **Audit record for `bio-alignment-msa-parsing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@53861ae](https://github.com/mrsonord2240/bioSkills/tree/53861ae5dcb3ba770ab1dc6d8cf1582925b49004/alignment/msa-parsing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-alignment-msa-parsing (RE-AUDIT of the fixed Skill)
Generated: 2026-09-20  |  Source: `mrsonord2240/bioSkills@53861ae5dcb3ba770ab1dc6d8cf1582925b49004:alignment/msa-parsing`  |  Auditor: fresh Sonnet (third agent; not the first auditor, not the fixer)

**Pre-fix 78 (Beta Only, not deployable) -> 87/100 ⭐ Production Ready; deployable: true.** Static 84 x 0.4 = 33.6; execution 88.6 x 0.6 = 53.2. Skill veto PASS, research veto PASS, no open P0, no open P1, 6 P2. 9/9 inputs executed; assertions 42/45 (93.3%); raw script assertions 196/199.

Floors (Production Ready): static 84>=80 ok, execution 88.6>=85 ok, Layer 1 avg 35.7>=32 ok, Layer 2 avg 52.9>=48 ok, assertion pass rate 93.3%>=90 ok. No downgrade.

## Classification and inputs
Category 3 Data Analysis; Mode A (agent applies the Skill code patterns; examples/ are runnable demos); Complex -> 7 inputs. I re-ran the 7 first-audit inputs as regression (fresh scripts, the SKILL.md code exec'd from the file, no transcription) and added 2 new inputs (8, 9) on data and structure the fixer never used. The schema lists n_inputs 1-8; 9 is used because 7 regression + 2 new is what the brief requires.

Environment: `F:\OpenScience\audit-envs\alignment\` (Windows venv Biopython 1.88, numpy 2.0.2, pyhmmer 0.12.3; WSL `alignment` env: MAFFT 7.526, HMMER 3.4, MUSCLE 5.3, trimAl 1.5.1, ClipKIT 2.14). The Skill was copied from the worktree to `run/skill/` (byte-identical, `cmp` checked for SKILL.md, usage-guide.md and all 11 example modules) and run from there; the worktree and `external/` were never written (no `__pycache__`).

## Step 1 - Skill Veto
T1 stability PASS (9 inputs, 199 scripted assertions, no crash or hang; errors only where intended). T2 contract PASS (name, description, tool_type, primary_tool, license). T3 determinism PASS (no randomness except the seeded shuffled null; `mi_apc.py` printed identical output twice on the shipped example and on the Ras seed). T4 security PASS (grep of all shipped files: no eval/exec/subprocess/os.system/network; the user regex is compiled and raises `re.error` on bad input; paths come from argv).

**Shipped-means-present:** every file the SKILL.md/usage-guide.md name exists (`examples/{a2m_a3m_io,henikoff_weights,neff,mi_apc,muscle5_column_confidence}.py`, `examples/data/`); the 8 Related Skills folders exist; alignment-io has "A2M / A3M Conventions" and "Streaming Large Stockholm Databases" and the `reformat.pl` pitfall. Not present: the string `_pdbx_poly_seq_scheme` that SKILL.md says lives in structure-navigation (P2, wording). The first-audit examples needed unshipped input files: now all 9 path-taking examples run with no arguments on `examples/data/` (`run/examples_noargs_output.txt`, 11/11).

## Step 2 - Static (25 criteria)
| Category | Score | Note |
|---|---|---|
| functional_suitability | 10/12 | Completeness 4, Correctness 3, Appropriateness 3. Every promised use case (parse, conserved, gaps, annotations, manipulate) plus weights, Neff, MI-APC, position mapping and a MUSCLE5 reliability route works and equals independent ground truth. Small inaccuracies remain: remove_duplicates does not normalise, hmmalign A2M example fails, a pointer to _pdbx_poly_seq_scheme that is not in structure-navigation. Pure-Python MI-APC/Neff are slow. |
| reliability | 10/12 | Fault tolerance 3, Error reporting 3, Recoverability 4. Empty filters, all-gap Henikoff, wrong-length weights and the APC guard raise or warn with a named threshold and a next step; modern Bio.Align objects fail loudly. Still silent: all-zero weights. Helpers are pure and never mutate the input. |
| performance_context | 4/8 | Token cost 2, Execution efficiency 2. SKILL.md grew to 504 lines / 28.7 KB with full code duplicated in examples/. select_columns rebuilds str(record.seq) for every kept column, so every helper is quadratic in alignment length (10 x 100,000 columns: 7.2 s per normalisation, 9.0 s per gaps_per_column vs 1.95 s pre-fix); MI-APC and Neff are pure-Python pair loops (400 x 120: about a minute). |
| agent_usability | 14/16 | Learnability 3, Consistency 3, Feedback design 4, Error prevention 4. One Neff/L rule everywhere, alphabet-aware placeholder, printed null and survivor counts, ValueErrors that name the threshold, estimator-dependence table, PDB-numbering trap. Henikoff/Easel/Neff paragraph is dense; "every helper normalises" has one exception. |
| human_usability | 7/8 | Discoverability 3, Forgiveness 4. Natural prompts in usage-guide.md now cover weighting, coevolution and reliability; the frontmatter description still omits weights/Neff/MI-APC/MUSCLE5. Input variants ("." gaps, lowercase, mixed case) are handled, and strict rejection (ValueError) is used where continuing would give wrong numbers. |
| security | 11/12 | Credential safety 4, Input validation 3, Data safety 4. No secrets, network, eval/exec or subprocess in any shipped file (grep); user regex is compiled unvalidated (raises re.error); paths come from argv. |
| maintainability | 10/12 | Modularity 3, Modifiability 3, Testability 4. examples/ share msa_utils.py; SKILL.md still repeats the function bodies, but I checked SKILL.md and examples produce identical output on the seed. Every example runs with no arguments on shipped data and on a path argument; answers are hand-checkable. |
| agent_specific | 18/20 | Trigger 3, Progressive disclosure 3, Composability 4, Idempotency 4, Escape hatches 4. Related-skill paths all exist (8/8); hand-offs to trimming, structure-navigation, plmDCA/EVcouplings and pyhmmer are explicit; guard refuses instead of guessing. Description unchanged and undersells the Skill; SKILL.md is over 500 lines. |
| **Subtotal** | **84/100** (first audit 76) | |

## Summary table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 55 | 92 | 5/5 PASS | yes | ✅ |
| 2 | Variant A | 36 | 54 | 90 | 5/5 PASS | yes | ✅ |
| 3 | Edge | 34 | 49 | 83 | 4/5 PASS | yes | ✅ |
| 4 | Variant B | 37 | 56 | 93 | 5/5 PASS | yes | ✅ |
| 5 | Stress | 36 | 54 | 90 | 5/5 PASS | yes | ✅ |
| 6 | Scope Boundary | 36 | 53 | 89 | 5/5 PASS | yes | ✅ |
| 7 | Adversarial | 34 | 50 | 84 | 4/5 PASS | yes | ✅ |
| 8 (NEW) | Variant B | 34 | 50 | 84 | 4/5 PASS | yes | ✅ |
| 9 (NEW) | Stress | 37 | 55 | 92 | 5/5 PASS | yes | ✅ |

**Execution Average: 88.6 / 100**  |  **Assertion pass rate: 42/45**  |  Layer 1 avg 35.7/40, Layer 2 avg 52.9/60. Layer 2 uses the Data Analysis rubric (methodological validity /20, code executability /15, data QC /10, reproducibility /10, security /5).

## Verification of the fix log (my runs, not the log)
| fix-log claim | my result |
|---|---|
| "." gaps and lowercase handled by every helper | Confirmed for 11 helpers (in3, in7, in8); FAILED for remove_duplicates (P2). Note Biopython 1.88 already converts "." to "-" when reading Stockholm, so the trap bites FASTA/A2M input, not .sto via AlignIO. |
| normalize_alignment / select_columns keep annotations | Confirmed on real Pfam (accession/start/end, GC seq_cons, GR pAS, sliced correctly) and real hmmalign PP/RF. But quadratic in alignment length (probes/probe_scaling_output.txt): new P2. |
| mi_apc.py guard + shuffled null; single Neff/L > 1 rule | Confirmed: warning text, raw-MI fallback, null, `force=True`; MI and APC equal independent scipy code to 5e-15 on the seed and a 400 x 120 alignment; planted pairs ranked 1-2; L=100/101 and Neff/L=0.5 boundaries; no stale "0.5" anywhere. |
| protein consensus X, gap-row denominator stated | Confirmed (124 X / 0 N on the seed; DNA and RNA keep N; a peptide over A/C/G/T is misdetected as nucleotide but `ambiguous=` overrides). |
| Henikoff/Neff prose rewritten; henikoff_weights raises | Confirmed: ValueError on all-gap; hand-computed weights; Spearman 0.909 / 0.0091; Neff table three rows reproduced (66.08, 73.0, 6.35). Easel pb: I could reproduce it exactly (see below). |
| annotation-preserving cleaning; filters raise on empty result | Confirmed (in2, in7, in8). |
| GUIDANCE2 replaced by a MUSCLE5 ensemble route | Confirmed by running MUSCLE 5.3 (in6): commands as written, CC decode independent, masked output exact. Cosmetic: the best-replicate name is second to last in stderr, not last. |
| usage-guide.md dedup | Nothing lost: pip line -> SKILL Version block; Key Concepts -> intro conventions; annotations block and paragraph moved whole to SKILL.md (I ran it verbatim, in7); every Tips bullet is covered in SKILL.md (unreliable regions, trimming, gap handling, 0-based). usage-guide.md gained prompts for weighting/coevolution/reliability. |

**The two things the fixer left undone.** (1) *Easel-exact `pb` function*: does not matter for correctness, and I can say why. My independent 12-line function (probes/probe_pb_easel2.py: consensus columns with >= 50% residues, canonical residues only, per-sequence weight divided by its canonical-residue count in those columns, rescaled to sum N) matches pyhmmer to 7e-16, so the SKILL.md prose is exactly right and the fix log's "did not match" was an implementation slip, not an Easel property. The Skill correctly routes gappy alignments to pyhmmer; shipping the function would only remove that dependency (optional). (2) *Description unchanged*: a real but small trigger-precision cost (static 3/4), P2; it does not block deployment.

## Detailed outputs
Code: the Skill code is the SKILL.md blocks themselves, exec'd from the file by `run/skillns.py` (25/25 ran with no examples/ on the path, `run/skillns_output.txt`), plus the shipped examples run as subprocesses from `run/skill/examples/`. Every script is in `run/`; `run/run_all.sh` re-runs all of it.

### Input 1 - Canonical: Pfam globin seed PF00042 (real, 73 x 141): IDs, conserved, gaps, consensus  [regression of first-audit input 1]
**Prompt:** Here is the Pfam globin seed alignment (PF00042, 73 sequences, Stockholm). List the sequence IDs, show me the GLB2_LUMTE record, find the fully conserved columns and the ones conserved in at least 80% of sequences, count gaps per sequence and per column, and give me a 70% consensus.

**Executed:** true. **Script:** `in1_canonical.py, skillns.py`.  **Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

**Result:** Real data. All 25 python blocks of SKILL.md exec from the file without examples/ on the path; every value equals an independent parse of the raw Stockholm text. Protein consensus now uses X (0 spurious N; was 124).

**Assertions:**
- [PASS] All 25 python blocks of SKILL.md execute from the file (no examples/ on the path) - 25/25 blocks ran, no NameError/ImportError (skillns.py)
- [PASS] find_conserved_positions(1.0) and (0.8) equal an independent count from the raw Stockholm text - (17,F),(77,H) fully conserved; 3 columns at >= 0.8 incl. (11,P); fractions equal
- [PASS] Gaps per sequence and per column equal an independent raw-file count of the same 1943 cells - 1943 = 1943 = 1943; per-column list identical
- [PASS] Protein consensus uses a non-residue placeholder and equals an independent consensus at 0.7 and 0.5 - 124 X, 0 N, 0 true Asn-majority columns; identical to independent (was 124 N of which 2 real Asn)
- [PASS] Shipped analyze_alignment / find_conserved / gap_analysis / consensus_sequence run from a copy on the real .sto and print the verified values - rc 0, empty stderr; Col 0 composition dict, 1943 gap sums and 50% consensus equal independent values

**Output (trimmed, from `run/in1_output.txt`):**
```
gap characters in the raw file: [np.str_('.')] | chars Biopython returns for the same cells: ['-']
fully conserved: [(17, 'F', np.float64(1.0)), (77, 'H', np.float64(1.0))] | >=80%: [(11, 'P'), (17, 'F'), (77, 'H')]
sum gaps/seq 1943 | sum gaps/col 1943 | raw-file count 1943
consensus 0.7: XXXXXXXFXXXPXXXXXFXXXXXXXXXXXXXXXXXXXXHXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXLXXXHXXXXXXXXXXXXXXXXFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXAXXXXXXXXXXXXX
consensus 0.5: XXXLXXXFXXXPXXXXXFXXXXXXXXXXXXXXXXXXXXHXXXVXXXXXXXLXXXXXXLDXXXXXXXXXXXXXXLXXXHXXXXXXXVXPXXXXXXFXXXXXXXXXXXLXXXXXXXXXXXXXXXXXXXXAWXXXXXXXXXXXX
protein consensus 0.5: 124 X, 0 N; true Asn-majority columns: 0
--- analyze_alignment.py: rc=0 stdout_lines=13 stderr=''
Alignment: 73 sequences, 141 columns
Column composition (first 10 columns):
  Col 0: {'Q': 3, 'I': 5, 'H': 4, 'L': 9, 'R': 4, 'G': 6, 'A': 17, 'T': 5, 'P': 1, 'K': 3, 'V': 10, 'S': 4, 'D': 1, 'N': 1} - 23% conserved
  Col 1: {'A': 7, 'F': 3, 'K': 8, 'L': 2, 'D': 16, 'E': 23, 'N': 2, 'Z': 1, 'R': 3, 'T': 2, 'H': 1, 'G': 2, 'S': 2, 'M': 1} - 32% conserved
  Col 2: {'I': 17, 'L': 10, 'V': 5, 'S': 2, 'A': 21, 'T': 3, 'F': 13, 'C': 1, 'M': 1} - 29% conserved
  Col 3: {'W': 5, 'F': 14, 'L': 37, 'I': 
--- find_conserved.py: rc=0 stdout_lines=8 stderr=''
--- gap_analysis.py: rc=0 stdout_lines=147 stderr=''
--- consensus_sequence.py: rc=0 stdout_lines=10 stderr=''
ASSERTIONS: 19/19 passed
... (19 [PASS] lines omitted; full text in run/in1_output.txt)
```

### Input 2 - Variant A: Clean: gappy columns, gappy/duplicate rows, ID filter, keep annotations, save  [regression of first-audit input 2]
**Prompt:** Clean this alignment: drop columns that are 50% gaps or more, drop sequences with more than 20% gaps, remove exact duplicates, keep only IDs starting with GLB, and save the cleaned alignment. Keep the Stockholm annotations.

**Executed:** true. **Script:** `in2_cleaning.py, probes/probe_sto_roundtrip.py`.  **Scores:** Basic 36/40 | Specialized 54/60 | Total 90/100

**Result:** Real Pfam seed + hand-computed synthetic 5 x 12. Annotations now survive and are sliced correctly; over-strict filters raise. Biopython 1.88 own Stockholm writer drops unrecognised tags (GC seq_cons, GR pAS) even for the UNCLEANED alignment - not a Skill defect.

**Assertions:**
- [PASS] remove_gappy_columns(0.5) keeps exactly the columns an independent mask keeps, content identical - 118 of 141 columns, all 73 rows equal raw-file columns; boundary (gap fraction == threshold) removed
- [PASS] Record annotations, GC seq_cons and GR letter annotations survive cleaning and are sliced to the kept columns - accession/start/end on 73 records; seq_cons equals the original string at the kept columns; was {} before the fix
- [PASS] Over-strict filters raise ValueError naming the threshold and the lowest gap fraction instead of returning an empty alignment - filter_by_gap_content(0.0): 'max_gap_fraction=0.0 (lowest fraction 0.11) removes all 73 sequences'; filter_by_id('^zzz') same
- [PASS] Cleaned alignment written as Stockholm loses nothing that Biopython writes for the original - #=GS 146/146, #=GR 1/1 (active_site sliced); GC seq_cons absent in BOTH (Biopython writer limit, probe)
- [PASS] Shipped clean_alignment.py from a copy on the real .sto equals the independent column-then-row pipeline - 73 x 118, IDs/sequences identical, FASTA written with "-" gaps only

**Output (trimmed, from `run/in2_output.txt`):**
```
kept 118 of 141 columns (independent mask keeps 118)
record annotations before/after: {'accession': 'P02218.2', 'start': 31, 'end': 141} {'accession': 'P02218.2', 'start': 31, 'end': 141}
column_annotations keys: ['GC:seq_cons'] -> ['GC:seq_cons']
letter_annotation keys on the real seed: {'GR:pAS', 'active_site'}
Stockholm write, ORIGINAL vs CLEANED: #=GS 146/146, #=GR 1/1, #=GC 0/0
NOTE (Biopython 1.88 writer, see probes/probe_sto_roundtrip.py): the Pfam-specific tags GC seq_cons and GR pAS are held in memory but the Stockholm WRITER drops them for the uncleaned alignment too.
filter_by_gap_content(0.0) -> max_gap_fraction=0.0 (lowest fraction 0.11) removes all 73 sequences
Original: 73 sequences, 141 columns
After column cleaning: 73 sequences, 118 columns
After sequence filtering: 73 sequences, 118 columns
Saved to cleaned_alignment.fasta
ASSERTIONS: 21/21 passed
... (21 [PASS] lines omitted; full text in run/in2_output.txt)
```

### Input 3 - Edge: Messy files: all-gap column, single sequence, ragged, "." gaps, A2M/A3M, degenerate weights  [regression of first-audit input 3]
**Prompt:** Some of my alignment files are messy: an HMMER/hhsearch A2M with lowercase inserts and "." gaps, an alignment with an all-gap column, a single-sequence file, a ragged file and a ColabFold A3M. Give me match-only columns and a consensus without it blowing up.

**Executed:** true. **Script:** `in3_edge.py`.  **Scores:** Basic 34/40 | Specialized 49/60 | Total 83/100

**Result:** Synthetic, hand-known answers. All first-audit failures (".", lowercase) fixed. New defect found: all-zero weights give an all-placeholder consensus silently.

**Assertions:**
- [PASS] "."-gapped input: gaps_per_column, coordinate_map, consensus and filters treat "." as a gap - gaps [0,0,3,3,0,0] (was all 0); coordinate_map 4 residues (was 6); consensus ACXXGT without "."
- [PASS] All-gap column, single sequence and ragged file behave as documented - consensus ACD-EG keeps "-"; single sequence reproduced; ragged raises ValueError "same length"
- [PASS] A2M example gives the hand-known result on the shipped example.a2m and a hhsearch-style A2M; unpadded A3M fails loudly and the pyhmmer hand-off pads it - 9 match columns, inserts 0/2/1; A3M ValueError; MSAFile(format="a2m") gives the same match-only columns
- [PASS] normalize_alignment semantics and modern Bio.Align.Alignment handling - upper=False keeps case ("Ac-dE"); input not mutated; Alignment object raises AttributeError (loud), matching the SKILL API note
- [FAIL] Degenerate weights fail loudly (all-zero weights) - consensus_sequence(weights=[0,0,0,0]) returns 'XXXXXX' with only a RuntimeWarning (0/0); wrong length raises ValueError correctly

**Output (trimmed, from `run/in3_output.txt`):**
```
SKILL.md block 15:22: RuntimeWarning: invalid value encountered in scalar divide
'.'-gapped FASTA: raw col 2 = ..D. | gaps_per_column = [0, 0, 3, 3, 0, 0]
A2M alignment: 3 sequences, 11 columns
After dropping insert states: 9 match columns
query: 9 match, 0 inserts
s2: 9 match, 2 inserts
s3: 9 match, 1 inserts
A2M alignment: 3 sequences, 11 columns
After dropping insert states: 9 match columns
ref: 9 match, 0 inserts
hit_1: 9 match, 2 inserts
hit_2: 9 match, 1 inserts
helper on Bio.Align.Alignment -> AttributeError: 'Alignment' object has no attribute 'get_alignment_length'
is_nucleotide on a peptide made only of G/A/T/C letters: True | consensus@1.0: GNTTACAGN | forced ambiguous=X: GXTTACAGX
all-zero weights -> returned 'XXXXXX'
[FAIL] all-zero weights fail loudly rather than returning a consensus of garbage (ZeroDivisionError or ValueError)  -- returned 'XXXXXX'
ASSERTIONS: 21/22 passed
... (21 [PASS] lines omitted; full text in run/in3_output.txt)
```

### Input 4 - Variant B: Proximal His of myoglobin (PDB 1MBN) to an alignment column  [regression of first-audit input 4]
**Prompt:** In my 8-globin alignment, which column is the proximal histidine of sperm whale myoglobin (PDB 1MBN His93), what residue does every other globin have there, and how do I convert between column numbers and residue numbers?

**Executed:** true. **Script:** `in4_position_map.py, wsl_tools.sh mafft_globins`.  **Scores:** Basic 37/40 | Specialized 56/60 | Total 93/100

**Result:** Real data: 8 UniProt globins aligned with MAFFT 7.526 L-INS-i, ground truth from real 1MBN coordinates. The SKILL sentence about PDB numbering (His93 = UniProt residue 94) verified.

**Assertions:**
- [PASS] coordinate_map round-trips for all 8 records and equals the loop-based walk - ungapped == UniProt sequence, seq->aln->seq exact, gap columns -1, 8/8
- [PASS] PDB ground truth and the SKILL sentence about numbering hold - 1MBN starts at Val 1 = UniProt residue 2; index 93 is H, index 92 is S; residue 93 HIS, 64 HIS
- [PASS] The column reached from PDB residue 93 holds His in all 8 globins; distal His column too - column 94 {H} x 8; distal His column 65 H in both myoglobins
- [PASS] find_conserved_positions(1.0) lists the proximal His column (alignment and structure agree) - (94,H) in the fully conserved list
- [PASS] aln_to_seq is -1 exactly at gap columns; doc variable renamed with a 0-based comment - gap column [2]; column_of_residue_index_42 with "0-based index 42 is the 43rd residue"

**Output (trimmed, from `run/in4_output.txt`):**
```
['MYG_PHYMC', 'HBAZ_HUMAN', 'HBB_HUMAN', 'MYG_HUMAN', 'HBA_HUMAN', 'HBA_MOUSE', 'HBB_BOVIN', 'HBB_PANTR'] 155
1MBN first residue: 1 VAL | residue 93: HIS | residue 64: HIS
alignment column of PDB His93 (0-based): 94
residue in that column for all 8: {'MYG_PHYMC': 'H', 'HBAZ_HUMAN': 'H', 'HBB_HUMAN': 'H', 'MYG_HUMAN': 'H', 'HBA_HUMAN': 'H', 'HBA_MOUSE': 'H', 'HBB_BOVIN': 'H', 'HBB_PANTR': 'H'}
fully conserved columns: [(0, 'M'), (3, 'L'), (15, 'W'), (17, 'K'), (26, 'G'), (30, 'L'), (32, 'R'), (38, 'P'), (40, 'T'), (44, 'F'), (47, 'F'), (65, 'H')] ...
ASSERTIONS: 17/17 passed
... (17 [PASS] lines omitted; full text in run/in4_output.txt)
```

### Input 5 - Stress: Henikoff weights, Neff/L, MI-APC on the Pfam seed (real)  [regression of first-audit input 5]
**Prompt:** Compute Henikoff sequence weights for the Pfam globin seed, report Neff and Neff/L at 62% and 80% identity, and find the top coevolving column pairs with MI-APC (tell me if the alignment is deep enough).

**Executed:** true. **Script:** `in5_weights_neff_mi.py, wsl_tools.sh hmmbuild_pf, probes/probe_pb_easel*.py`.  **Scores:** Basic 36/40 | Specialized 54/60 | Total 90/100

**Result:** Real seed. Guard, null, ValueError, Neff table and prose all verified against independent code, pyhmmer, hmmbuild 3.4 and real 1MBN contacts. Easel pb reproduced exactly by a 12-line independent function (the fixer could not), confirming the SKILL prose.

**Assertions:**
- [PASS] henikoff_weights equals an independent Henikoff, matches the hand-computed 4 x 5 answer, and raises on an all-gap alignment - max diff 0.0; [7/30,7/30,3/10,7/30]; ValueError names pyhmmer/trimming (was NaN)
- [PASS] SKILL prose on Easel pb is correct (gap-ignoring, consensus columns >= 50% residues, / residue count, rescaled to N), Spearman 0.909, max diff 0.0091 - independent reimplementation matches pyhmmer to 7e-16; pb and blosum weights sum to 73.0
- [PASS] Neff table rows reproduced by own runs; Neff/L threshold stated one way - Neff 66.08/73.00 == independent; pb sum 73.0; hmmbuild eff_nseq 6.35; no stale "> 0.5" anywhere
- [PASS] mi_apc.py enforces the SKILL guard on the seed: warns, ranks raw MI, prints a null, calls no pair - WARNING L=141, Neff/L=0.47; raw MI == scipy MI to 4e-15; force=True MI-APC == independent APC; 0 of top 20 above null 2.671
- [PASS] SKILL figures reproduced: best MI-APC 0.603 < shuffled 0.616; none of top-30 pairs are 1MBN contacts - 0.6031 vs 0.6161 (seed 0, best of 5); contact precision 0.00 vs baseline 0.09

**Output (trimmed, from `run/in5_output.txt`):**
```
gap-free columns used: 72 | weights sum 0.9999999999999999 min/max 0.0061479370658038815 0.025312413931953878
pb sum 73.0 | blosum sum 72.99999999999999
Spearman(skill Henikoff, Easel pb) = 0.909; max abs diff after rescaling pb to sum 1 = 0.0091
my Easel-pb reimplementation (consensus columns, canonical residues, /residue count, sum N) vs pyhmmer: max abs diff 6.661338147750939e-16
examples/neff.py: Neff(0.62) = 66.0833, Neff(0.80) = 73.0000; independent 66.0833 / 73.0000
hmmbuild 3.4 eff_nseq: 6.35
Sequences: 73
Length: 141
Neff (62% threshold, protein convention): 66.08
Neff/L: 0.469
Neff (80% threshold, nucleotide convention): 73.00
Neff/L is below the Skill rule of thumb for MI-APC / DCA (Neff/L > 1).
GLB2_LUMTE/31-141: 0.0127
GLB2_TYLHE/32-143: 0.0143 ... Total weight: 1.0000  Kish effective sample size (1/sum w^2, not Neff): 66.46
mi_matrix_apc default on the seed: warnings = ['L=141, Neff/L=0.47: APC needs L > 100 and Neff/L > 1; returning RAW MI, not MI-APC']
WARNING: L=141, Neff/L=0.47: APC needs L > 100 and Neff/L > 1. Ranking raw MI; treat it as noise unless it beats the shuffled null.
Top 20 column pairs (raw MI, bits); column-shuffled null max = 2.671:
     4-  64:  2.627  (<= null)
     4-  23:  2.434  (<= null)
    26-  64:  2.380  (<= null)
    64- 135:  2.373  (<= null)
    23-  62:  2.364  (<= null)
ASSERTIONS: 25/25 passed
... (25 [PASS] lines omitted; full text in run/in5_output.txt)
```

### Input 6 - Scope Boundary: Trim for trees and HMMs, keep column numbers, mask unreliable columns (MUSCLE5 route), stream with pyhmmer  [regression of first-audit input 6]
**Prompt:** Trim this Pfam globin alignment for tree building and separately for HMM building, keep the original column numbers, mask unreliable columns, then stream the file with pyhmmer weights.

**Executed:** true. **Script:** `in6_scope_trimming.py, wsl_tools.sh trim/muscle_help/muscle_ens8/muscle_ens73`.  **Scores:** Basic 36/40 | Specialized 53/60 | Total 89/100

**Result:** The first audit could not run GUIDANCE2. The replacement, a MUSCLE 5.3 ensemble route, was run exactly as SKILL.md writes it on 8 UniProt globins and 73 Pfam sequences; CC decoded independently and compared with a replicate-agreement count computed from the raw .efa.

**Assertions:**
- [PASS] trimAl -colnumbering map reproduces the trimmed alignment; ClipKIT kpic-smart-gap valid - 103 map entries, every trimmed row == original columns at mapped indices; ClipKIT 121 of 141
- [PASS] MUSCLE5 route runs as written and the example script decodes CC correctly - ens8 best acb.2, 155 columns; 73 Pfam best bca.2, 156 columns; script survivor counts == my own digit decode; masked.fa == best replicate at CC >= 0.9 columns
- [PASS] CC reflects replicate agreement and the SKILL sentence about 8 globins holds - all 6 columns present in < 90% of the 16 replicates have CC < 0.9; 11 of 155 columns CC < 0.9; mean CC 0.990 vs 0.727 (agree vs disagree)
- [PASS] GUIDANCE2 / TCS / the 0.93 cut-off are no longer recommended - 2 mentions, both negative ("not offered", "0.93 does not transfer"); no TCS
- [PASS] pyhmmer streaming pattern works and the version block lists pyhmmer >= 0.11.3 - 2-alignment Stockholm: [(73,73.0),(73,73.0)]; block states >= 0.11.3, checked 0.12.3, install line

**Output (trimmed, from `run/in6_output.txt`):**
```
trimAl -gappyout: 103 of 141 columns kept, colmap 103
GUIDANCE2 mentions in SKILL.md: 2 | TCS: 0 | 0.93: 1
--- 8 globins: muscle5_column_confidence.py acb.2 rc=0
8 sequences x 155 columns; mean CC 0.980
  CC >= 0.5: 155 columns
  CC >= 0.7: 150 columns
  CC >= 0.9: 144 columns
  CC >= 0.99: 144 columns
8 globins: 155 columns; corr(CC, replicate agreement) = 0.635; max |CC - agreement| = 0.380
--- 73 Pfam: muscle5_column_confidence.py bca.2 rc=0
73 sequences x 156 columns; mean CC 0.617
  CC >= 0.5: 95 columns
  CC >= 0.7: 73 columns
  CC >= 0.9: 60 columns
  CC >= 0.99: 58 columns
73 Pfam: 156 columns; corr(CC, replicate agreement) = 0.792; max |CC - agreement| = 0.820
muscle -maxcc stderr tail: 'CC min 148, avg 150, max 152, best acb.2\nhttps://drive5.com\n'
installed pyhmmer 0.12.3
ASSERTIONS: 22/22 passed
... (22 [PASS] lines omitted; full text in run/in6_output.txt)
```

**MUSCLE 5.3 commands as run (`run/wsl_tools.sh muscle_ens8`, `muscle_ens73`; output `run/wsl_tools_output.txt`):**
```
muscle -align seqs.fa -stratified -output ens.efa
muscle -maxcc ens.efa -output maxcc.afa        -> "CC min 148, avg 150, max 152, best acb.2" (8 globins); "best bca.2" (73 Pfam)
muscle -addconfseq ens.efa -output ens_cc.efa
python examples/muscle5_column_confidence.py ens_cc.efa acb.2 0.9 masked.fa
```
On the 73 Pfam sequences only 60 of 156 columns reach CC >= 0.9 (mean CC 0.617), so the example's 0.9 cut-off would discard 62% of a divergent family: SKILL.md says there is no calibrated cut-off and tells the user to look at the survivor table first.

### Input 7 - Adversarial: Annotations kept through cleaning, soft-masked DNA, weights, malformed regex  [regression of first-audit input 7]
**Prompt:** Pull the secondary structure and RF annotation out of my Stockholm alignment and keep it after cleaning; also give me the consensus of my soft-masked (mixed-case) DNA alignment, weight the sequences before computing conservation, and filter sequences with this regex I typed: "["

**Executed:** true. **Script:** `in7_adversarial.py`.  **Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100

**Result:** Synthetic, hand-known answers. Every first-audit failure fixed (annotations kept, case-insensitive, weights= accepted, SummaryInfo statement). New: remove_duplicates is the one helper that does not normalise, contradicting "every helper normalises internally".

**Assertions:**
- [PASS] The SKILL.md annotation block, run verbatim on a synthetic Stockholm, returns SS per record and SS_cons - seqA HHHEEEC, seqB HHH-EEC, ss_cons HHHEEEC
- [PASS] Cleaning keeps SS/RF/GS annotations, sliced by the hand rule, and the written Stockholm carries them - SS -> HHHEEC, RF -> xxxxxx; #=GR SS, #=GC SS_cons, #=GC RF, #=GS OS present; re-read equal
- [PASS] Soft-masked DNA consensus is case-insensitive; DNA/RNA get N, protein gets X - ACGTACGT and 8/8 conserved (was ACGTNNNN, 0); RNA (U) detected
- [PASS] weights= is actionable and consistent: hand-computed weighted consensus; malformed regex raises - col 3 A -> C as hand computed; weighted vs unweighted helpers agree on 400 random cases (0 mismatches); re.error "unterminated character set"
- [FAIL] SKILL.md claim "every helper normalises its input internally" holds (remove_duplicates) - remove_duplicates keeps AC-GT, AC.GT and ac-gt as 3 distinct rows (expected 1); it compares raw strings

**Output (trimmed, from `run/in7_output.txt`):**
```
F:\OpenScience\audit-envs\alignment\Lib\site-packages\Bio\Align\AlignInfo.py:32: BiopythonDeprecationWarning: The class SummaryInfo has been deprecated. Instead of
>>> align_info = AlignInfo.SummaryInfo(msa)
>>> sequence = align_info.get_column(1)
please use
>>> alignment = msa.alignment  # to get a new-style Alignment object
>>> sequence = alignment[:, 1]
Here, `msa` is a MultipleSeqAlignment object and `alignment` is an
`Alignment` object.
  warnings.warn(
block output: seqA HHHEEEC | seqB HHH-EEC | ss_cons = HHHEEEC
column_annotations: {'reference_annotation': 'xxx.xxx', 'secondary_structure': 'HHHEEEC'} | record annotations: [{'accession': 'A0001', 'organism': 'Homo sapiens'}, {'accession': 'B0002', 'organism': 'Mus musculus'}]
after remove_gappy_columns(0.5): 6 columns; column_annotations {'reference_annotation': 'xxxxxx', 'secondary_structure': 'HHHEEC'} | SS seqA HHHEEC
# STOCKHOLM 1.0
#=GF SQ 2
seqA ACDFGH
#=GS seqA AC A0001
#=GS seqA DE seqA
#=GS seqA OS Homo sapiens
#=GR seqA SS HHHEEC
seqB ACDFGH
#=GS seqB AC B0002
#=GS seqB DE seqB
[FAIL] SKILL.md says "every helper normalises its input internally": remove_duplicates should treat AC-GT / AC.GT / ac-gt as duplicates (keep a, d)  -- kept ['a', 'b', 'c', 'd']
ASSERTIONS: 16/17 passed
... (16 [PASS] lines omitted; full text in run/in7_output.txt)
```

### Input 8 - Variant B: NEW: real hmmalign Stockholm/A2M, real HBB CDS DNA (soft-masked), real Pfam Ras seed (EBI download)
**Prompt:** I have hmmalign output for 8 globins against the Pfam globin profile (Stockholm with "." gaps, lowercase inserts, PP lines) and its A2M version, a MAFFT alignment of six mammalian HBB coding sequences, softmasked in places, and the Pfam Ras seed. Give me match-only columns, conserved columns, a consensus per file, gap counts, weights, and keep the PP/RF annotation through cleaning.

**Executed:** true. **Script:** `in8_real_new.py, wsl_tools.sh hmmalign_globins/hmmalign_a2m/mafft_hbb`.  **Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100

**Result:** New input built from files the fixer never saw (HMMER 3.4 hmmalign output, MAFFT 7.526 DNA alignment, PF00071 from the EBI public API). 28 raw assertions pass; the one failure is real: HMMER own A2M output is not padded, so the shipped a2m example (AlignIO) raises.

**Assertions:**
- [PASS] hmmalign Stockholm (mixed case, "." and "-"): gaps, consensus, fully conserved columns equal an independent case-folded parse; proximal His column is H in all 8 - 8 x 161; 115 gap cells both ways; 14 conserved columns; coordinate_map(MYG idx 93) -> column 97, HHHHHHHH
- [PASS] PP letter annotations and RF/PP_cons survive remove_gappy_columns and equal the raw lines sliced to the kept columns - 147 of 161 columns kept; 8 #=GR PP lines and #=GC RF/PP_cons written
- [PASS] Real HBB CDS alignment: nucleotide detected, N placeholder, ATG start; 25% soft-masking changes nothing; Neff by hand - 6 x 444; consensus[:3] ATG; identical consensus/conserved/Henikoff on the lowercased copy; all six >= 0.845 identical -> Neff 1.000
- [PASS] Real Ras seed (new family): gaps, consensus, conserved, Henikoff equal independent; P-loop GxxxxGK recovered; guard fires with correct L and Neff/L - 60 x 229; GDXGVGKS; 19 columns >= 0.9; WARNING L=229, Neff/L=0.14 equals my own 32.57/229
- [FAIL] The shipped examples/a2m_a3m_io.py handles real `hmmalign --outformat a2m` output - rc 1: ValueError "Sequences must all be the same length": HMMER 3.4 writes its A2M unpadded (rows 149-161, no "." chars). match_only_columns itself is right (117 per row = profile LENG = RF x count) when fed records; pyhmmer padding also works

**Output (trimmed, from `run/in8_output.txt`):**
```
A. hmmalign: 8 seqs x 161 columns; raw chars: [np.str_('-'), np.str_('.'), np.str_('A'), np.str_('C'), np.str_('D'), np.str_('E'), np.str_('F'), np.str_('G'), np.str_('H'), np.str_('I'), np.str_('K'), np.str_('L'), np.str_('M'), n
   Biopython alphabet: -ACDEFGHIKLMNPQRSTVWYadefghiklmnpqrstvwy | column_annotations: ['posterior_probability', 'reference_annotation'] | letter_annotations of row 0: ['posterior_probability']
   MYG_PHYMC residue index 93 -> column 97 | residues in that column: HHHHHHHH
   remove_gappy_columns(0.5): 147 of 161 | column_annotations {'posterior_probability': '..........................89**', 'reference_annotation': '..........................xxxx'}
   hmmalign --outformat a2m row lengths: [161, 150, 151, 160, 149, 149, 149, 151] | "." characters: 0
   shipped examples/a2m_a3m_io.py on the real hmmalign A2M: rc = 1 | ValueError: Sequences must all be the same length
   pyhmmer MSAFile(format="a2m") padded widths: [161] | first row start: mvlsegewqlvlhvwakveadvaghgq-DILIRLFKSHPE
B. HBB CDS alignment 6 x 444; alphabet [np.str_('-'), np.str_('A'), np.str_('C'), np.str_('G'), np.str_('T')]
   soft-masked row 0: atGGtGCaTcTGACTCCTGAgGAGAAGTcTGcCGtTACTgCCCTGTGgGGCaAGGTGAAc
C. Ras seed: 60 x 229; raw gap chars [np.str_('.')]
   Ras consensus 0.5: KLVXXGDXGVGKSXLLXRFXXXXFXXXYXXTIGXDXXXXXFXXKXXXXDXXXXXXXXXXGXXXXLXIWDTAGQERFXXXXXXYYRXAXGXLLVYDITXXXSFXXXXXXWXXXXXXXXXXXXXXXXXXXXXXXXXLVGNKXDLXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXRXVXXXXGXXXAXXXXXXXXXXGXXXFXET
WARNING: L=229, Neff/L=0.14: APC needs L > 100 and Neff/L > 1. Ranking raw MI; treat it as noise unless it beats the shuffled null.
Top 20 column pairs (raw MI, bits); column-shuffled null max = 2.072:
   113- 213:  1.936  (<= null)
    76-  81:  1.900  (<= null)
    44- 113:  1.844  (<= null)
    80-  87:  1.831  (<= null)
    24-  76:  1.792  (<= null)
    24-  87:  1.792  (<= null)
   113- 220: 
[FAIL] A. the shipped examples/a2m_a3m_io.py handles real `hmmalign --outformat a2m` output (rc 0, prints 117 match columns)  [expected to FAIL: it reads with AlignIO, which needs padded rows]  -- rc 1: ValueError: Sequences must 
ASSERTIONS: 28/29 passed
... (28 [PASS] lines omitted; full text in run/in8_output.txt)
```

Real HMMER 3.4 A2M: `hmmalign --outformat a2m` row lengths 161/150/151/160/149/149/149/151, zero "." characters (`run/wsl_tools_output.txt`).

### Input 9 - Stress: NEW: redundant clade weighting and deep-alignment MI-APC with planted coupling (synthetic, seeded)
**Prompt:** My 35-sequence alignment is 30 near-identical clones plus 5 divergent sequences: weight it, tell me the effective number of sequences, and give me a consensus and conserved columns that do not just follow the over-represented clade. Separately, I have a deep alignment (400 sequences, 120 columns): find coevolving pairs with MI-APC and tell me when the tool refuses.

**Executed:** true. **Script:** `in9_weighting_coevolution.py`.  **Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

**Result:** New synthetic input with closed-form answers: the parts of the Skill the real seed cannot reach (weights= in practice, the guard passing, planted coupling recovered, guard boundaries).

**Assertions:**
- [PASS] Henikoff clone-group weight and Neff equal the closed-form hand values - clone group 0.3619 = (6/2 + 10/3 + 18/6 + 6*30/35)/40 (unweighted 0.857); Neff(0.62) = 6.000
- [PASS] Weighted consensus / conserved columns do not follow the clade - unweighted A x34; weighted X in columns 6-33 and only the 6 identical columns conserved (40 unweighted)
- [PASS] Deep alignment passes the guard silently and recovers the planted pairs; MI-APC equals independent scipy MI - APC - Neff/L 3.33, no warning; (10,60) 2.563 and (25,90) 2.136 rank 1-2 of 7140; max diff 5e-15; MI by hand 1 / 0 / 0.8113 bits
- [PASS] mi_apc.py CLI on the deep alignment: no WARNING, planted pairs > 5x the shuffled null, null at the right scale - null 0.155 vs independent shuffle 0.131; 2 of top 20 above null
- [PASS] Guard boundaries: L = 100 refuses, 101 passes; 400 rows / 60 distinct refuses (Neff/L 0.5) - L=100 warns and returns raw MI (== independent MI); force=True differs; redundant set Neff 60

**Output (trimmed, from `run/in9_output.txt`):**
```
clone weight each: 0.012063492063492061 | divergent weights: [0.1221 0.1221 0.1221 0.136  0.136 ] | clone group total: 0.3619047619047618
Neff(0.62) = 6.0
unweighted consensus @0.5: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWWWWWW
weighted   consensus @0.5: GGGGGGXXXXXXXXXXXXXXXXXXXXXXXXXXXXWWWWWW
deep alignment 400 x 120: Neff(0.62) = 400.0, Neff/L = 3.33
top 5 MI-APC pairs: [(10, 60, 2.563), (25, 90, 2.136), (17, 76, 0.129), (55, 94, 0.113), (15, 54, 0.109)]
Top 20 column pairs (MI-APC, bits); column-shuffled null max = 0.155:
    10-  60:  2.563
    25-  90:  2.136
    17-  76:  0.129  (<= null)
    55-  94:  0.113  (<= null) 
... 2 of the top 20 exceed the null. 
independent shuffled max MI-APC: 0.13082448980455158 | shipped null: 0.155
L=100: False L=100, Neff/L=4.00: APC needs L > 100 and Neff/L > 1 | L=101: True
redundant 400 = 60 x ~6.7 copies: L=120, Neff/L=0.50: APC needs L > 100 and Neff/L > 1
ASSERTIONS: 16/16 passed
... (16 [PASS] lines omitted; full text in run/in9_output.txt)
```

## Defects the fix introduced or left (own probes)
- **Quadratic `select_columns`** (`run/probes/probe_scaling_output.txt`): `normalize_alignment` 0.04 s / 0.38 s / 2.0 s / 7.2 s for 10 sequences x 5k / 20k / 50k / 100k columns; pre-fix `gaps_per_column` 1.95 s at 100k. Results correct, only slow on long alignments.
- `remove_duplicates` not normalised; all-zero weights silent; hmmalign A2M example; wording items (see Recommendations).
- Not defects (checked): the "GC seq_cons dropped on Stockholm write" is Biopython 1.88 (uncleaned alignment loses it too, `run/probes/probe_sto_roundtrip_output.txt`); Biopython converts "." to "-" on Stockholm read.

## Research Veto (Data Analysis)
M1 PASS (every SKILL-stated number reproduced; references are real, one attribution unverified), M2 PASS (no clinical content), M3 PASS (guard and null in code, estimators labelled), M4 PASS (code runs; details in the JSON).

## Recommendations
No P0, no P1.

**[P2] select_columns / normalize_alignment is quadratic in length**  
Observed in: static / probe  
Problem: select_columns does "".join(str(record.seq)[i] for i in keep), materialising the whole string for every kept column, and every helper calls it: 10 x 100,000 columns takes 7.2 s per normalisation (9.0 s for gaps_per_column) against 1.95 s for the pre-fix count; 1 M columns would take about 12 min per call.  
Root cause: The fix normalises by rebuilding the alignment column by column instead of once per record.  
Fix: Take text = str(record.seq) once per record and slice/translate it (for the full-width case use text.upper().replace(".", "-")); keep select_columns for real column subsets.

**[P2] remove_duplicates does not normalise (doc says every helper does)**  
Observed in: [7]  
Problem: remove_duplicates compares raw strings: AC-GT, AC.GT and ac-gt are kept as three distinct rows, contradicting the "Every helper below normalises its input internally" sentence.  
Root cause: The fix added normalisation to the column helpers but not to the row-comparison helper.  
Fix: Compare str(r.seq) of normalize_alignment(alignment) rows in remove_duplicates (keep the original records), or narrow the sentence.

**[P2] a2m_a3m_io.py fails on real HMMER A2M output**  
Observed in: [8]  
Problem: `hmmalign --outformat a2m` (HMMER 3.4) writes unpadded rows (149-161 characters, no "." characters), so AlignIO.read(..., "fasta") raises "Sequences must all be the same length"; the docstring and SKILL.md/alignment-io describe A2M as padded.  
Root cause: The example was written for padded (HH-suite style) A2M and only tested on the hand-made example.a2m.  
Fix: Read with SeqIO.parse (match_only_columns already accepts a list of records: 117 columns per row = profile LENG) or pad through pyhmmer MSAFile(format="a2m"), and say that HMMER writes A2M unpadded.

**[P2] All-zero weights return an all-placeholder consensus silently**  
Observed in: [3]  
Problem: consensus_sequence(weights=[0,0,0,0]) returns XXXXXX with only a RuntimeWarning (0/0); find_conserved_positions would return nothing.  
Root cause: No check on weights.sum().  
Fix: Raise ValueError("weights must sum to a positive value") next to the length check in both weighted helpers.

**[P2] SKILL.md over 500 lines; description omits weights, Neff, MI-APC, MUSCLE5**  
Observed in: static / probe  
Problem: SKILL.md is 504 lines / 28.7 KB with the function bodies repeated in examples/, and the frontmatter description (unchanged) does not mention weighting, Neff, MI-APC or the MUSCLE5 column-confidence route that the body now covers.  
Root cause: Fix added content without moving code out of SKILL.md or refreshing the trigger text.  
Fix: Point to examples/ for the longer functions (keep a signature and a one-line use), and add "sequence weights, Neff, MI-APC coevolution, MUSCLE5 column confidence" to the description.

**[P2] Small documentation inaccuracies**  
Observed in: [2, 5, 6]  
Problem: (a) SKILL.md sends the reader to structure-navigation for the "authoritative _pdbx_poly_seq_scheme mapping": that string is not in the Skill (it covers SEQRES/PPBuilder/auth vs label numbering). (b) "stderr ends best <name>": the line is second to last, a URL follows; muscle5_column_confidence.py with no argument dies with a bare IndexError and no usage line. (c) Biopython 1.88 writes only recognised Stockholm tags: Pfam GC seq_cons and GR pAS are dropped even from an uncleaned alignment, which the "GC ... survive read/write" sentence does not say. (d) The Cocco 2018 attribution for "APC underperforms raw MI below 100 columns" was not verified by me; on the seed both raw MI (top-30 contact precision 0.13) and MI-APC (0.00) sit near the 0.09 baseline.  
Root cause: Prose written from memory of related Skills and one tool run.  
Fix: Name the section that exists in structure-navigation, reword (b), add the recognised-tags caveat to the annotation paragraph, and cite or soften (d).

## Files
`run/`: `common.py`, `skillns.py` (exec the SKILL.md blocks), `mkdata.py`, `in1..in9_*.py` with `in*_output.txt`, `wsl_tools.sh` (+ `wsl_tools_output.txt`: MAFFT, hmmbuild/hmmalign, trimAl/ClipKIT, MUSCLE5 ensembles), `probes/` (Easel pb, Stockholm round trip, scaling), `build_report.py`, `run_all.sh`, `skill/` (byte-identical copy of the audited Skill), `data/` (REAL: public-data inputs, EBI PF00071 seed, tool outputs; SYNTHETIC: every `syn_*` file; see `data/SOURCES.txt`).
