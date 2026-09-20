> **Audit record for `bio-alignment-msa-parsing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@354b499](https://github.com/mrsonord2240/bioSkills/tree/354b4992cd8d2f1bee039510af618da0333821f1/alignment/msa-parsing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-alignment-msa-parsing
Generated: 2026-09-19  |  Source: `mrsonord2240/bioSkills@354b4992cd8d2f1bee039510af618da0333821f1:alignment/msa-parsing`  |  Auditor: fresh Sonnet (audit stage, first audit)

**Final score 78/100 (static 76 x 0.4 = 30.4; execution 79.9 x 0.6 = 47.9); numeric band Limited Release; grade after floors: ⚠️ Beta Only; deployable: false; skill veto PASS, research veto PASS, no P0.**

Floors (Limited Release): static 76>=70 ok, execution 79.9>=75 ok, Layer 1 avg 33.3>=28 ok, Layer 2 avg 46.6>=42 ok, **assertion pass rate 24/35 = 68.6% < 80% FAILS** -> one tier down. The only thing keeping this from Limited Release is the assertion floor.

## Classification
Category 3 Data Analysis; execution mode A (agent applies the Skill code patterns; examples are demo scripts, not a CLI); complexity Complex (many task types, 9 examples, hand-offs to 6 other Skills) -> 7 inputs. Environment: `F:\OpenScience\audit-envs\alignment\TOOLS.md` (Biopython 1.88, pyhmmer 0.12.3, WSL MAFFT/HMMER/trimAl/MUSCLE).

## Step 1 - Skill Veto
T1 stability PASS (no crash across 122 scripted assertions, 9 examples). T2 contract PASS (name, description, tool_type, primary_tool, license). T3 determinism PASS (no randomness; MI/Neff/weights reproduce exactly). T4 security PASS (no eval/exec, no network; user regex compiled but raises re.error on bad input).

**Shipped-means-present:** `usage-guide.md`, `examples/henikoff_weights.py`, `neff.py`, `mi_apc.py` exist; Related Skills `alignment/{multiple-alignment,alignment-io,pairwise-alignment,msa-statistics,alignment-trimming,structural-alignment}`, `phylogenetics/modern-tree-inference`, `structural-biology/structure-navigation` exist; alignment-io has the "A2M / A3M Conventions" and "Streaming Large Stockholm Databases" sections. No missing primary file. Not shipped: the example input files (alignment.fasta, hhsearch_output.a2m) - P2. `__pycache__` check of the clone: none.

## Step 2 - Static (25 criteria)
| Category | Score | Note |
|---|---|---|
| functional_suitability | 9/12 | Completeness 3, Correctness 3, Appropriateness 3. Core primitives match independent implementations; gaps recognised only as '-', no case handling, no weighted statistics; prose errors on HMMER pb gap handling and the Neff estimator table; protein consensus placeholder 'N' is Asn. |
| reliability | 7/12 | Fault tolerance 2, Error reporting 2, Recoverability 3. Relies on Biopython errors; silent wrong answers on '.' gaps, NaN from Henikoff, empty alignments after filtering; functions are pure and never mutate input. |
| performance_context | 6/8 | Token cost 3, Efficiency 3. SKILL.md is 454 lines with full code duplicated in examples/; MI-APC and Neff use python pair loops (1.5 s and 0.1 s at 73x141). |
| agent_usability | 11/16 | Learnability 3, Consistency 2, Feedback 3, Error prevention 3. Goal/Approach blocks are clear; SKILL.md and examples disagree (find_conserved variants, HMMER-weight statements, Neff/L 0.5 vs 1, fifth-state advice); good pitfall callouts (APC over-correction, PDB numbering, Neff estimator). |
| human_usability | 5/8 | Discoverability 3, Forgiveness 2. Natural trigger phrasing and example prompts; strict '-' only handling with no normalisation or warning. |
| security | 11/12 | Credential safety 4, Input validation 3, Data safety 4. No secrets or network; user regex is compiled unvalidated (raises re.error); no eval/exec. |
| maintainability | 9/12 | Modularity 3, Modifiability 3, Testability 3. Independent functions and per-task examples; every function is duplicated in SKILL.md and examples and has already drifted; examples read alignment.fasta / hhsearch_output.a2m that are not shipped. |
| agent_specific | 18/20 | Trigger 3, Progressive disclosure 3, Composability 4, Idempotency 4, Escape hatches 4. Description omits weights/Neff/MI-APC; all 7 Related Skills paths resolve; clear hand-offs (trimming, PDB mapping, plmDCA, pyhmmer). |
| **Subtotal** | **76/100** | |

## Summary table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 35 | 51 | 86 | 4/5 | yes | ✅ |
| 2 | Variant A | 34 | 49 | 83 | 3/5 | yes | ✅ |
| 3 | Edge | 33 | 43 | 76 | 4/5 | yes | ✅ |
| 4 | Variant B | 36 | 54 | 90 | 5/5 | yes | ✅ |
| 5 | Stress | 30 | 42 | 72 | 2/5 | yes | ⚠️ |
| 6 | Scope Boundary | 34 | 46 | 80 | 3/5 | yes | ✅ |
| 7 | Adversarial | 31 | 41 | 72 | 3/5 | yes | ⚠️ |

**Execution Average: 79.9 / 100**  |  **Assertion pass rate: 24/35**  |  Layer 1 avg 33.3/40, Layer 2 avg 46.6/60

Layer 2 uses the Data Analysis rubric (methodological validity /20, code executability /15, data QC /10, reproducibility /10, security /5). Raw script assertions (all `[PASS]`/`[FAIL]` lines in `run/in*_output.txt`): 102 pass, 20 fail; the 35 assertions in the JSON are the per-input selection (3 core-function checks + 2 edge/claim checks).

## Detailed outputs

### Input 1 - Canonical: Pfam globin seed: IDs, conserved columns, gaps, consensus (real data)
**Prompt:** Here is the Pfam globin seed alignment (PF00042, 73 sequences, Stockholm). List the sequence IDs, show me the GLB2_LUMTE record, find the fully conserved columns and the ones conserved in at least 80% of sequences, count gaps per sequence and per column, and give me a 70% consensus.

**Executed:** executed: true. Assertions on printed values vs independent implementation.  **Script:** `in1_canonical.py (+ shipped analyze_alignment.py, find_conserved.py, gap_analysis.py, consensus_sequence.py from a copy)`

**Scores:** Basic 35/40 | Specialized 51/60 | Total 86/100

**Result:** All SKILL.md snippets and 4 shipped examples ran on the real 73x141 Pfam seed; results equal an independent numpy/pandas implementation (2 fully conserved columns F17/H77, 3 at >=80%, 1943 gap chars counted 2 ways). Protein consensus emits 124 "N" placeholders, only 2 of which are real Asn.

**Assertions:**
- [PASS] Loaded shape is 73x141 and IDs/lookup (get_sequence_by_id) return the right records - shape (73,141); GLB2_LUMTE/31-141 found; missing id returns None
- [PASS] find_conserved_positions equals an independent numpy/pandas count at 1.0 and 0.8 - [(17,F),(77,H)] and 3 columns at >=0.8 identical to independent code
- [PASS] Gap counts per sequence and per column agree and equal an independent count - 1943 = 1943 = 1943; gap_analysis.py per-column lines sum to 1943
- [PASS] Shipped examples analyze_alignment/find_conserved/gap_analysis/consensus_sequence run from a copy and print the verified values - rc=0, stderr empty; consensus in output equals independent consensus
- [FAIL] Protein consensus uses a placeholder that cannot be confused with a residue - default ambiguous='N' is asparagine: 124 'N' in the 0.5 consensus, only 2 columns have Asn as the plurality residue

**Output (trimmed, from `run/in1_output.txt`):**
```
[PASS] transcribed functions match SKILL.md signatures  -- []
73 sequences, 141 columns
[PASS] shape 73 x 141 (matches Pfam PF00042.29 seed per public-data README)
[PASS] IDs unique and carry coordinates (GLB2_LUMTE/31-141 present)
[PASS] get_sequence_by_id returns the record
[PASS] get_sequence_by_id returns None for missing id (skill-documented behaviour)
Annotations sample: {'accession': 'P02218.2', 'start': 31, 'end': 141} | desc: GLB2_LUMTE/31-141
[PASS] aln[:, 5] is a str of len 73
fully conserved: [(17, 'F'), (77, 'H')]
>=80% count: 3 [(11, 'P'), (17, 'F'), (77, 'H')]
[PASS] SKILL.md find_conserved_positions(1.0) == independent numpy/pandas
[PASS] SKILL.md find_conserved_positions(0.8) == independent
columns containing >=1 gap: 69 of 141
[PASS] biology sanity: exactly 2 fully conserved columns, Phe (col 17) and His (col 77) -- plausible invariant globin heme-pocket residues (His invariance confirmed independently in in4)  -- got [(17, 'F'), (77, 'H')]
[PASS] sum(gaps per seq) == sum(gaps per col) == 1943 (chars counted independently)
[PASS] gaps_per_column length == 141
consensus 0.7: NNNNNNNFNNNPNNNNNFNNNNNNNNNNNNNNNNNNNNHNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNLNNNHNNNNNNNNNNNNNNNNFNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNANNNNNNNNNNNNN
consensus 0.5: NNNLNNNFNNNPNNNNNFNNNNNNNNNNNNNNNNNNNNHNNNVNNNNNNNLNNNNNNLDNNNNNNNNNNNNNNLNNNHNNNNNNNVNPNNNNNNFNNNNNNNNNNNLNNNNNNNNNNNNNNNNNNNNAWNNNNNNNNNNNN
[PASS] consensus length == 141
[PASS] SKILL.md consensus == independent (same algorithm)
'N' chars in protein consensus(0.5): 124; columns whose real plurality residue is Asn: 2
[FAIL] protein consensus: 'N' placeholder is unambiguous (can't tell Asn from 'ambiguous')  [EXPECTED FAIL = defect]  -- 124 'N' in output, only 2 are true Asn plurality columns => 122 placeholders masquerade as Asn
--- analyze_alignment.py: rc=0 stdout_lines=13 stderr=''
Alignment: 73 sequences, 141 columns

Column composition (first 10 columns):
  Col 0: {'Q': 3, 'I': 5, 'H': 4, 'L': 9, 'R': 4, 'G': 6, 'A': 17, 'T': 5, 'P': 1, 'K': 3, 'V': 10, 'S': 4, 'D': 1, 'N': 1} - 23% conserved
  Col 1: {'A': 7, 'F': 3, 'K': 8, 'L': 2, 'D': 16, 'E': 23, 'N': 2, 'Z': 1, 'R': 3, 'T': 2, 'H': 1, 'G': 2, 'S': 2, 'M': 1} - 32% conserved
  Col 2: {'I': 17, 'L': 10, 'V': 5, 'S': 2, 'A': 21, 'T': 3, 'F': 13, 'C': 1, 'M': 1} - 29% conserved
--- find_conserved.py: rc=0 stdout_lines=8 stderr=''
Fully conserved positions (100%):
  Position 17: F
  Position 77: H

... (24 more lines in run/in1_output.txt)
```

### Input 2 - Variant A: Clean: gappy columns, gappy/duplicate sequences, ID filter, save
**Prompt:** Clean this alignment: drop columns that are 50% gaps or more, drop sequences with more than 20% gaps, remove exact duplicates, keep only IDs starting with GLB, and save the cleaned alignment.

**Executed:** executed: true.  **Script:** `in2_cleaning.py (+ shipped clean_alignment.py from a copy)`

**Scores:** Basic 34/40 | Specialized 49/60 | Total 83/100

**Result:** Real Pfam seed: 141 -> 118 columns identical to an independent mask; synthetic 5x12 alignment with hand-computed gap counts matches. Cleaning silently drops all per-record and column annotations; a 0.1 gap filter keeps 0 of 73 sequences and returns an empty alignment with no message.

**Assertions:**
- [PASS] remove_gappy_columns(0.5) keeps exactly the columns an independent numpy mask keeps, with identical content - 118 columns, all 73 rows equal arr[:, keep]
- [PASS] Sequence filters (gap fraction, duplicates, regex ID) return the same IDs as independent code and hand-known synthetic answers - species_E dropped as duplicate of A; 44 of 73 kept at 0.2; ^GLB -> 32
- [PASS] Shipped clean_alignment.py output equals the independent pipeline (column trim then sequence filter) - 73 x 118, same IDs
- [FAIL] Cleaning preserves record/column annotations (accession, start, end, GC seq_cons) - after: annotations {} and column_annotations {} (before: 3 keys and GC:seq_cons)
- [FAIL] An over-strict filter that empties the alignment is reported to the user - filter_by_gap_content(0.1) on the real seed keeps 0 of 73; returns an empty alignment silently

**Output (trimmed, from `run/in2_output.txt`):**
```
real: kept cols 118 of 141; gappy (>=50%) removed: 23
[PASS] remove_gappy_columns(0.5): kept column count == numpy mask count
[PASS] remove_gappy_columns: kept column CONTENT identical to arr[:, keep]
[PASS] sequence order and IDs preserved
[PASS] cleaned alignment is rectangular (all rows same length)
[FAIL] per-record annotations (accession/start/end) survive cleaning [defect if FAIL: new SeqRecord drops annotations]  -- before=['accession', 'start', 'end'] after=[]
[FAIL] column_annotations (GC:seq_cons) survive cleaning [defect if FAIL]  -- before=['GC:seq_cons'] after=[]
[PASS] filter_by_gap_content(0.1) keeps the same IDs as independent count (0 of 73)
[PASS] filter_by_gap_content(0.2) keeps the same IDs as independent count (44 of 73)
0.0 -> 0 seqs
len 0
[PASS] filter to zero sequences returns an object without crashing  -- 0 seqs
[PASS] SYNTH remove_duplicates drops exactly species_E (exact copy of A)
[PASS] SYNTH filter_by_id regex keeps A,B only
[PASS] REAL remove_duplicates: no exact duplicate rows in Pfam seed (73 kept)
IDs starting GLB: ['GLB2_LUMTE/31-141', 'GLB2_TYLHE/32-143', 'GLB3_LAMSP/30-141', 'GLB_TUBTU/29-139', 'GLB4_LUMTE/36-146'] 32
[PASS] REAL filter_by_id(^GLB) equals independent startswith
gaps per col syn: [0, 0, 0, 4, 0, 0, 0, 0, 0, 1, 1, 0]
[PASS] SYNTH gaps_per_column == hand-computed  -- [0, 0, 0, 4, 0, 0, 0, 0, 0, 1, 1, 0]
[PASS] SYNTH remove_gappy_columns(0.5) drops only col 3 => 11 cols  -- MKVLLAAGTWH
[PASS] SYNTH find_gappy_columns(0.5) == [3]
[PASS] boundary: column with gap fraction == threshold is removed (0.8 vs col3)
[PASS] SYNTH extract_ungapped_regions(ref=A) drops col 3 => 11 cols; A ungapped
[PASS] extract_ungapped_regions(ref=B, no gaps) is identity (12 cols)
Original: 73 sequences, 141 columns
After column cleaning: 73 sequences, 118 columns
After sequence filtering: 73 sequences, 118 columns
Saved to cleaned_alignment.fasta
 
[PASS] clean_alignment.py rc=0 and wrote cleaned_alignment.fasta
example output shape 73 118 | expected 73 118
[PASS] clean_alignment.py output shape/IDs == independent pipeline (col trim 0.5 then seq gap<=0.2)

ASSERTIONS: 19/21 passed
... (2 more lines in run/in2_output.txt)
```

### Input 3 - Edge: Messy files: all-gap column, single sequence, ragged, A2M '.' gaps, A3M
**Prompt:** Some of my alignment files are messy: an HMMER/hhsearch A2M with lowercase inserts and '.' gaps, an alignment with an all-gap column, a single-sequence file, a ragged file and a ColabFold A3M. Give me match-only columns and a consensus without it blowing up.

**Executed:** executed: true. Data synthetic (syn_*.fasta/.a2m/.a3m).  **Script:** `in3_edge.py (+ shipped a2m_a3m_io.py from a copy)`

**Scores:** Basic 33/40 | Specialized 43/60 | Total 76/100

**Result:** Synthetic data. All-gap column, single sequence, ragged error, A2M match-only extraction (hand-known 9 match columns, inserts 0/2/1) and A3M-must-be-reformatted all behave as documented. Every function recognises only '-' as a gap: on '.'-gapped input gaps_per_column returns all zeros, coordinate_map counts '.' as residues and consensus emits '.'.

**Assertions:**
- [PASS] All-gap column: consensus keeps "-" (AC-G), is not reported conserved, and is removed by remove_gappy_columns - consensus AC-G; 3 columns after removal
- [PASS] Single-sequence alignment loads and consensus reproduces it - 1x6, consensus ACDE-G
- [PASS] Shipped a2m_a3m_io.py gives the hand-known result (3 seq x 11 cols -> 9 match columns; inserts 0, 2, 1) - match_only_columns == ['ACDEFGHIK','AC-EFGHIK','ACDEFG-IK']
- [PASS] Ragged and unpadded A3M inputs fail loudly (Common Errors / A2M-A3M section) - ValueError: Sequences must all be the same length; pyhmmer MSAFile(format=a2m) pads the A3M so the hand-off works
- [FAIL] '.' gap characters (HMMER/A2M convention) are treated as gaps by the snippets - gaps_per_column=[0]*6 instead of [0,0,2,2,0,0]; coordinate_map len 6 not 4; consensus 'AC..GT'

**Output (trimmed, from `run/in3_output.txt`):**
```
[PASS] SYNTH gap-only col: consensus emits "-" and keeps length 4 (AC-G)  -- AC-G
[PASS] SYNTH gap-only col: not reported as conserved
[PASS] SYNTH gap-only col: remove_gappy_columns drops it => 3 cols
[PASS] SYNTH consensus threshold 1.0: col1 (C,C,T) is ambiguous N  -- AN-G
[PASS] SYNTH single-seq alignment loads (1 x 6)
[PASS] SYNTH single-seq consensus == the sequence, gap col kept  -- ACDE-G
[PASS] SYNTH single-seq conserved: all 5 residue cols "100% conserved" (trivial; no warning by skill)
[PASS] SYNTH unequal lengths raises a clear error (Common Errors row)  -- ValueError: Sequences must all be the same length
gaps_per_column with '.' gaps: [0, 0, 0, 0, 0, 0]
[FAIL] '.'-gapped input: gaps_per_column reports 2 gaps in cols 2,3 (user expectation) [defect if FAIL: only '-' recognised]  -- [0, 0, 0, 0, 0, 0]
[FAIL] '.'-gapped input: coordinate_map treats '.' as gap (len(seq_to_aln)==4) [defect if FAIL]  -- len=6
[FAIL] '.'-gapped input: consensus does not emit '.' as a residue [defect if FAIL]  -- AC..GT
A2M alignment: 3 sequences, 11 columns
After dropping insert states: 9 match columns
query: 9 match, 0 inserts
s2: 9 match, 2 inserts
s3: 9 match, 1 inserts
 
[PASS] a2m_a3m_io.py: rc=0; "3 sequences, 11 columns"; "9 match columns"
[PASS] a2m_a3m_io.py: insert counts query=0, s2=2, s3=1 (hand-known)
[PASS] match_only_columns == hand-known ["ACDEFGHIK","AC-EFGHIK","ACDEFG-IK"]  -- ['ACDEFGHIK', 'AC-EFGHIK', 'ACDEFG-IK']
[PASS] A3M direct load fails loudly with a length error (SKILL.md warns to reformat)  -- ValueError: Sequences must all be the same length
[PASS] pyhmmer.easel.MSAFile(format='a2m') on padded A2M: .alignment rows equal the file (3 x 11)  -- ['ACDE..FGHIK', 'AC-EwyFGHIK', 'ACDEy.FG-IK']
MSAFile(format=a2m) on UNPADDED A3M .alignment -> ['ACDE..FGHIK', 'AC-EwyFGHIK', 'ACDEy.FG-IK']
[PASS] hand-off claim (alignment-io): MSAFile(format='a2m') pads an A3M to a rectangular MSA; match-only columns == hand-known  -- ['ACDE..FGHIK', 'AC-EwyFGHIK', 'ACDEy.FG-IK']
Bio.Align.read type Alignment | [:,0] -> str 'AAA'
[PASS] API note: Alignment (Bio.Align.read) has no get_alignment_length (SKILL snippets are for AlignIO objects only)
[PASS] API note: alignment[:, idx] on Bio.Align.Alignment returns str as SKILL implies 'verify'  -- str

ASSERTIONS: 16/19 passed
  FAILED: '.'-gapped input: gaps_per_column reports 2 gaps in cols 2,3 (user expectation) [defect if FAIL: only '-' recognised] [0, 0, 0, 0, 0, 0]
  FAILED: '.'-gapped input: coordinate_map treats '.' as gap (len(seq_to_aln)==4) [defect if FAIL] len=6
  FAILED: '.'-gapped input: consensus does not emit '.' as a residue [defect if FAIL] AC..GT
```

### Input 4 - Variant B: Map proximal His of myoglobin (PDB 1MBN) to an alignment column
**Prompt:** In my 8-globin alignment, which column is the proximal histidine of sperm whale myoglobin (PDB 1MBN His93), what residue does every other globin have there, and how do I convert between column numbers and residue numbers?

**Executed:** executed: true. MAFFT 7.526 in WSL; Windows Python for analysis.  **Script:** `in4_mafft.sh (MAFFT L-INS-i in WSL) + in4_position_map.py`

**Scores:** Basic 36/40 | Specialized 54/60 | Total 90/100

**Result:** Real UniProt globins aligned with MAFFT, ground truth from real PDB 1MBN coordinates (Bio.PDB). coordinate_map round-trips for all 8 sequences and equals a loop-based walk; PDB residue 93 = UniProt index 93 (initiator Met offset) maps to column 94 where all 8 globins have His (also fully conserved per find_conserved_positions).

**Assertions:**
- [PASS] coordinate_map: ungapped == original UniProt sequence, seq->aln->seq round-trips, gap columns are -1, for all 8 records - 8/8 records
- [PASS] Vectorised map equals the loop-based walk the SKILL describes for single lookups - identical for MYG_PHYMC
- [PASS] Ground truth: PDB 1MBN residue 93 is HIS and maps to the column where all 8 globins have His - column 94, {H} in 8/8; distal His64 -> column 65 also His
- [PASS] PDB-numbering offset is real and the correct route lands on His while the naive 1-based route does not - 1MBN starts at UniProt residue 2; index 92 is Ser, index 93 is His
- [PASS] Skill function find_conserved_positions agrees with the structure (proximal His column is fully conserved) - (94,'H') in the fully conserved list

**Output (trimmed, from `run/in4_output.txt`):**
```
['MYG_PHYMC', 'HBAZ_HUMAN', 'HBB_HUMAN', 'MYG_HUMAN', 'HBA_HUMAN', 'HBA_MOUSE', 'HBB_BOVIN', 'HBB_PANTR'] 155
[PASS] MYG_PHYMC: ungapped == original UniProt seq; seq->aln->seq round-trips; gap cols == -1
[PASS] HBAZ_HUMAN: ungapped == original UniProt seq; seq->aln->seq round-trips; gap cols == -1
[PASS] HBB_HUMAN: ungapped == original UniProt seq; seq->aln->seq round-trips; gap cols == -1
[PASS] MYG_HUMAN: ungapped == original UniProt seq; seq->aln->seq round-trips; gap cols == -1
[PASS] HBA_HUMAN: ungapped == original UniProt seq; seq->aln->seq round-trips; gap cols == -1
[PASS] HBA_MOUSE: ungapped == original UniProt seq; seq->aln->seq round-trips; gap cols == -1
[PASS] HBB_BOVIN: ungapped == original UniProt seq; seq->aln->seq round-trips; gap cols == -1
[PASS] HBB_PANTR: ungapped == original UniProt seq; seq->aln->seq round-trips; gap cols == -1
[PASS] vectorised seq_to_aln == loop-based walk for MYG_PHYMC
1MBN residue 93: HIS | first PDB residue number: 1 VAL
[PASS] PDB ground truth: 1MBN residue 93 is HIS (proximal His F8)
PDB seq len 153 UniProt len 154
PDB numbering offset vs UniProt (0-based find): 1
[PASS] SEQRES-vs-UniProt offset: PDB 1MBN starts at UniProt residue 2 (initiator Met absent), i.e. PDB n == 0-based UniProt index n
PDB vs UniProt mismatches (PDB idx): []
alignment column of PDB His93 (0-based): 94 | myoglobin residue at UniProt idx 93: H
[PASS] correct route (PDB n -> 0-based UniProt index n via +1 offset, then seq_to_aln) lands on His
naive 1-based->0-based (index 92) residue: S | column 93
[PASS] the naive route (ignoring SEQRES/ATOM offset) does NOT land on His -> the offset trap is real (docs only point elsewhere)
residue in column 94 for all 8: {'MYG_PHYMC': 'H', 'HBAZ_HUMAN': 'H', 'HBB_HUMAN': 'H', 'MYG_HUMAN': 'H', 'HBA_HUMAN': 'H', 'HBA_MOUSE': 'H', 'HBB_BOVIN': 'H', 'HBB_PANTR': 'H'}
[PASS] all 8 globins have His at the proximal-His column (biological ground truth: F8 His invariant)
distal His (PDB 64) column 65 {'MYG_PHYMC': 'H', 'HBAZ_HUMAN': 'H', 'HBB_HUMAN': 'H', 'MYG_HUMAN': 'H', 'HBA_HUMAN': 'H', 'HBA_MOUSE': 'H', 'HBB_BOVIN': 'H', 'HBB_PANTR': 'H'}
[PASS] distal His E7: PDB 1MBN residue 64 is HIS and maps to column where the myoglobins have His
MYG gap columns: [2]
[PASS] aln_to_seq is -1 at gap columns and equals number of residues before the column otherwise
SKILL.md names `seq_to_aln[42]` 'column_for_residue_42' -> that is the 43rd residue (0-based index). residue 43 = K (1-based 42 would be E)
fully conserved columns in the 8-globin alignment: [(0, 'M'), (3, 'L'), (15, 'W'), (17, 'K'), (26, 'G'), (30, 'L'), (32, 'R'), (38, 'P'), (40, 'T'), (44, 'F'), (47, 'F'), (65, 'H'), (66, 'G'), (69, 'V'), (90, 'L'), (94, 'H'), (116
[PASS] proximal His column is among the fully conserved columns of the 8-globin alignment (skill function agrees with structure)

ASSERTIONS: 17/17 passed
```

### Input 5 - Stress: Henikoff weights, Neff/L, MI-APC on the Pfam seed
**Prompt:** Compute Henikoff sequence weights for the Pfam globin seed, report Neff and Neff/L at 62% and 80% identity, and find the top coevolving column pairs with MI-APC.

**Executed:** executed: true. Ground truth: pyhmmer/Easel weights, scipy entropy, hmmbuild 3.4 (WSL), real PDB 1MBN contacts.  **Script:** `in5_weights_neff_mi.py, in5b_examples_main.py, in5_hmmbuild.sh (+ shipped henikoff_weights.py, neff.py, mi_apc.py)`

**Scores:** Basic 30/40 | Specialized 42/60 | Total 72/100

**Result:** Numerics exact vs independent code (weights diff 0.0, Neff 66.08/73.00, MI-APC diff 5e-15), all 3 examples exit 0. But mi_apc.py prints "top coevolving pairs" with no caveat when Neff/L=0.47 (the Skill says skip APC below 1): top score 0.603 vs 0.616 for a column-shuffled null, 0/30 top pairs are 1MBN contacts (baseline 0.11). Henikoff returns NaN when every column has a gap. Neff table conflates weights (sum to N=73) with Neff; hmmbuild eff_nseq is 6.35 vs skill Neff 66.08.

**Assertions:**
- [PASS] Henikoff weights equal an independent textbook implementation (sum to 1, no zero weights) - max abs diff 0.0; Spearman 0.909 vs Easel PB weights
- [PASS] neff() and mi_matrix_apc() equal independent implementations, and the three shipped __main__ blocks run with correct printed values - Neff 66.08 / 73.00 vs 66.0833 / 73.0; MI-APC max diff 5.3e-15; 73 weight lines sum 1.0000
- [FAIL] Skill's own guard (APC only when L>100 and Neff/L>1) is enforced or warned in mi_apc.py output - Neff/L=0.469 yet prints 20 "coevolving" pairs; top 0.603 < shuffled-null max 0.616; contact precision 0.00 vs baseline 0.11
- [FAIL] Henikoff weights return finite values or a clear error when every column contains a gap - weights [nan nan nan nan] with only a RuntimeWarning
- [FAIL] Skill claims about HMMER pb equivalence and estimator spread hold - Easel PB max diff 0.0091 vs skill weights (docstring says it matches); hmmbuild eff_nseq 6.35 vs Neff 66.08 = 10.4x, not "2-3x"

**Output (trimmed, from `run/in5_output.txt`):**
```
[PASS] SKILL.md henikoff_weights == examples/henikoff_weights.py (two copies agree numerically)
[PASS] weights sum to 1 and are all finite  -- sum=1.000000
[PASS] SKILL weights == independent textbook Henikoff over gap-free columns (max abs diff < 1e-12)  -- max diff 0.00e+00
gap-free columns used: 72 of 141; zero-weight sequences: 0
pyhmmer pb weights: sum 73.0 min 0.484 max 1.746
Spearman(skill Henikoff, Easel PB) = 0.909; max abs diff of normalised weights = 0.0091
[PASS] Easel PB weights sum to N (=73): they are per-sequence weights, NOT an Neff (Skill Neff table treats pb as the Neff baseline)  -- sum=73.000
[PASS] skill Henikoff weights correlate with Easel PB (Spearman > 0.9): same estimator family  -- rho=0.909
[FAIL] skill Henikoff equals Easel PB after normalisation (example docstring claims it matches HMMER) [FAIL = claim overstated]  -- max diff 0.0091
SYNTH every-column-gappy alignment -> weights [nan nan nan nan] | warnings: ['invalid value encountered in divide']
[FAIL] SYNTH every column has a gap: function returns finite weights or raises a clear error [FAIL = silent NaN]  -- [nan nan nan nan]
skill Neff(0.62)=66.08  Neff(0.80)=73.00  L=141  Neff/L=0.469  (0.1s)
[PASS] skill neff(0.62) == independent pure-python implementation  -- 66.0833 vs 66.0833
[PASS] skill neff(0.80) == independent implementation
Easel BLOSUM(0.62) weight sum: 73.0
[PASS] Easel BLOSUM weights also sum to N: any pyhmmer compute_weights() output needs conversion to an Neff, which the Skill never states
hmmbuild eff_nseq (entropy-weighted Neff, what HMMER reports): 6.35 | skill Neff(0.62)= 66.08 Neff(0.80)= 73.0
[PASS] hmmbuild eff_nseq parsed from real hmmbuild output
ratio skill Neff(0.62) / hmmbuild eff_nseq = 10.41; ratio to sum of pb weights (N=73) = 0.91
[PASS] skill Neff(0.62) is within the 0.5-3x band of the sum of HMMER pb weights (the Skill table "baseline")  -- ratio 0.91
[FAIL] Skill says estimators differ "often 2-3x": skill Neff(0.62) vs the Neff HMMER actually reports (hmmbuild eff_nseq) within 3x [FAIL = 10x, understated]  -- ratio 10.41 (eff_nseq 6.35)
[PASS] Neff/L computed and below the skill's DCA thresholds (0.5) on this real seed => the Skill's own guard says do NOT apply APC  -- Neff/L=0.469
mi_apc.py: matrix (141, 141), 1.4s
[PASS] MI-APC matrix == independent scipy-entropy MI (H(a)+H(b)-H(a,b)) minus APC, max abs diff < 1e-9  -- max diff 5.33e-15
[PASS] MI-APC symmetric
[PASS] raw MI is non-negative (up to fp)
top5 MI-APC pairs: [(81, 84, 0.603), (20, 62, 0.598), (20, 63, 0.591), (118, 138, 0.526), (21, 45, 0.524)]
sequence separations of top 20: [3, 42, 43, 20, 24, 72, 19, 17, 54, 78, 52, 69, 12, 73, 10, 5, 64, 15, 73, 76]
[FAIL] shipped mi_apc.py enforces the SKILL.md guard ('apply APC only when L>100 and Neff/L>1') [FAIL = applies APC unconditionally, no warning]
real top MI-APC 0.603 vs column-shuffled null top (5 seeds) [0.616 0.478 0.492 0.425 0.57 ]
[FAIL] real max MI-APC exceeds the max over 5 column-shuffled nulls (signal above noise) [FAIL = indistinguishable from noise at Neff/L<0.5]  -- 0.603 vs 0.616
best seed row MYG_ALLMI/27-143 ~ 1MBN: 117 mapped residues, 62% identity
top-30 MI-APC pairs (|i-j|>=6, mapped to 1MBN): contact precision 0.00 vs all-pair baseline 0.11 (8 A heavy-atom)
top-30 RAW MI contact precision 0.10 (Skill says raw MI is preferable when L<100 or Neff/L<1)
... (9 more lines in run/in5_output.txt)
```

**Shipped `__main__` blocks (`run/in5b_output.txt`):**
```
--- henikoff_weights.py: rc=0, stdout lines=75, stderr=''
GLB2_LUMTE/31-141: 0.0127
GLB2_TYLHE/32-143: 0.0143
GLB3_LAMSP/30-141: 0.0124
GLB_TUBTU/29-139: 0.0125 
... GLBC_NIPBR/44-161: 0.0143

Total weight: 1.0000  Effective sequences: 66.46
--- neff.py: rc=0, stdout lines=6, stderr=''
Sequences: 73
Length: 141
Neff (62% threshold, protein convention): 66.08
Neff/L: 0.469 
... Neff/L: 0.469
Neff (80% threshold, nucleotide convention): 73.00
Rule of thumb: Neff/L > 0.5 sufficient for direct-coupling-analysis contact prediction.
--- mi_apc.py: rc=0, stdout lines=21, stderr=''
Top 20 coevolving column pairs (MI-APC, bits):
    81-  84:  0.603
    20-  62:  0.598
    20-  63:  0.591 
...     23-  38:  0.437
     8-  81:  0.435
    63- 139:  0.420
[PASS] henikoff_weights.py prints 73 weights and they sum to ~1  -- 73 weights, sum 1.0000
[PASS] henikoff_weights.py "Effective sequences" line is printed (1/sum(w^2))  -- Total weight: 1.0000  Effective sequences: 66.46
[PASS] neff.py prints Neff(62%)=66.08 and Neff(80%)=73.00, Neff/L=0.469 (matches independent values)  -- Sequences: 73 | Length: 141 | Neff (62% threshold, protein convention): 66.08 | Neff/L: 0.469 | Neff (80% threshold, nucleoti
[PASS] mi_apc.py prints 20 top pairs in the "i-j: score" format  -- 20 pair lines
[FAIL] mi_apc.py output carries no reliability caveat although Neff/L=0.47 < 1 (Skill: skip APC below Neff/L>1) [FAIL = no caveat]
[PASS] all three examples exit 0 with empty stderr
... (3 more lines in run/in5b_output.txt)
```

### Input 6 - Scope Boundary: Trimming/reliability routing claims and pyhmmer streaming
**Prompt:** Trim this alignment for tree building and separately for HMM building, keep the original column numbers, mask unreliable columns with GUIDANCE2, then stream the file with pyhmmer weights.

**Executed:** executed: true for everything except GUIDANCE2 (not executed: package unobtainable, TOOLS.md Blocked).  **Script:** `in6_wsl.sh (trimAl, ClipKIT, muscle help in WSL) + in6_scope_trimming.py`

**Scores:** Basic 34/40 | Specialized 46/60 | Total 80/100

**Result:** Skill only routes to alignment-trimming; the routed claims were run on the real seed. trimAl -gappyout -colnumbering mapping is exact (103 of 141 columns); ClipKIT kpic-smart-gap valid (121 of 141); MUSCLE5 ensemble flags exist; pyhmmer MSAFile streaming + compute_weights(method="pb") works. GUIDANCE2 (recommended twice, threshold 0.93) is not obtainable so that part was NOT executed; version block omits pyhmmer.

**Assertions:**
- [PASS] trimAl -colnumbering map reproduces the trimmed alignment from original columns (0-based, correct) - 103 map entries; every trimmed row == original columns at mapped indices
- [PASS] ClipKIT kpic-smart-gap (decision-matrix first-line tool for trees) is a valid mode with sane output - 121 of 141 kept, 14.2% trimmed, 73 sequences
- [PASS] pyhmmer streaming pattern (iterate MSAFile, compute_weights(method='pb')) works - [(73,73.0),(73,73.0)] on a 2-alignment Stockholm file
- [FAIL] GUIDANCE2 column masking, recommended twice with a 0.93 threshold, can actually be run - NOT executed: distribution URL now serves an HTML page; the Skill gives no install path or alternative command
- [FAIL] Version block lists every library needing a minimum version (pyhmmer compute_weights needs >= 0.11.3) - Version Compatibility mentions only BioPython 1.83+ and numpy 1.26+

**Output (trimmed, from `run/in6_output.txt`):**
```
trimAl gappyout: 103 of 141 columns kept; colmap len 103
[PASS] trimAl -colnumbering: #ColumnsMap has one entry per kept column  -- 103 vs 103
[PASS] trimAl -colnumbering: trimmed rows equal ORIGINAL columns at the mapped indices (mapping is 0-based and correct)
ClipKIT kpic-smart-gap: 121 of 141 kept (14.2% trimmed)
[PASS] ClipKIT kpic-smart-gap mode name is valid and keeps a sane count (121 of 141 in the tool log)
SKILL remove_gappy_columns(0.5): 118 kept; trimAl gappyout 103; ClipKIT 121
[PASS] SKILL tip 'aggressive trimming (>20-30% of sites) hurts trees': trimAl -gappyout trims <=30% here (HMM-oriented tool is not over-aggressive)  -- 27.0% trimmed
[FAIL] GUIDANCE2 reliability masking (recommended in 2 places) is runnable [NOT EXECUTED: package unobtainable, TOOLS.md Blocked]  -- GUIDANCE2 tarball URL now returns an HTML page; no install path documented in the Skill
[PASS] MUSCLE5 '-stratified/-diversified' ensemble + '-letterconf' exist in muscle 5.3 help (SKILL: 'MUSCLE5 ensemble for per-column confidence')
streamed MSAs (n_seqs, sum of pb weights): [(73, 73.0), (73, 73.0)]
[PASS] pyhmmer streaming pattern (iterate MSAFile, compute_weights(method='pb')) works on a 2-record Stockholm file  -- [(73, 73.0), (73, 73.0)]
[FAIL] SKILL.md version block lists pyhmmer minimum version (compute_weights added in pyhmmer 0.11.3) [FAIL = not stated]  -- Version Compatibility block only mentions BioPython and numpy

ASSERTIONS: 6/8 passed
  FAILED: GUIDANCE2 reliability masking (recommended in 2 places) is runnable [NOT EXECUTED: package unobtainable, TOOLS.md Blocked] GUIDANCE2 tarball URL now returns an HTML page; no install path documented in the Skill
  FAILED: SKILL.md version block lists pyhmmer minimum version (compute_weights added in pyhmmer 0.11.3) [FAIL = not stated] Version Compatibility block only mentions BioPython and numpy
```

**WSL tool output (`run/in6_wsl_output.txt`):**
```
== trimal version

trimAl v1.5.rev1 build[2025-11-25]
== trimal -gappyout -colnumbering (SKILL routing table: HMM profile / preserve column mapping)
#ColumnsMap	0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 46, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 68, 69, 70, 71, 72, 73, 74, 75, 
== clipkit kpic-smart-gap (SKILL routing table: phylogenetic input)
---------------------
Original length: 141
Number of sites kept: 121
Number of sites trimmed: 20
Percentage of alignment trimmed: 14.184%

Execution time: 0.083s

== muscle 5 ensemble flags (SKILL: 'MUSCLE5 ensemble to get per-column confidence')
    muscle -align input.fa -stratified -output stratified_ensemble.efa
    muscle -align input.fa -diversified -output diversified_ensemble.afa
        Number of replicates, defaults 4, 100, 100 for stratified,
          diversified, resampled. With -stratified there is one
Extract replicate with highest total CC (diversified input recommended):
    muscle -maxcc ensemble.efa -output maxcc.afa
compare against the ensemble (e.g. from -maxcc), output is in aligned
    muscle -letterconf ensemble.efa -ref aln.afa -output letterconf.afa
== guidance2 present?
(exit above is expected: GUIDANCE2 not installable, see TOOLS.md Blocked)
```

### Input 7 - Adversarial: Annotations, soft-masked DNA consensus, user regex
**Prompt:** Pull the secondary structure and RF annotation out of my Stockholm alignment and keep it after cleaning; also give me the consensus of my soft-masked (mixed-case) DNA alignment, and filter sequences with this regex I typed: '['.

**Executed:** executed: true. Data synthetic (syn_annot.sto, syn_dna_mixedcase.fasta).  **Script:** `in7_adversarial.py`

**Scores:** Basic 31/40 | Specialized 41/60 | Total 72/100

**Result:** Synthetic data. The usage-guide annotation snippet is correct on Biopython 1.88 (keys 'secondary_structure', column 'secondary_structure'); Stockholm round-trip keeps GC/GR/GS; a malformed regex raises re.error. Failures: cleaning then writing Stockholm drops all GC/GR lines; consensus/conservation are case-sensitive (mixed-case DNA gives ACGTNNNN and 0/8 conserved columns); SummaryInfo is said to be 'deprecated' but its methods are gone in 1.88; 'weight before any column-wise statistic' is not actionable because no function accepts weights.

**Assertions:**
- [PASS] usage-guide 'Working with Annotations' snippet, run verbatim, returns SS per record and SS_cons - printed [('seqA','HHHEEEC'),('seqB','HHH-EEC')]; column SS_cons 'HHHEEEC'
- [PASS] Stockholm write/read round trip keeps GC (SS_cons, RF), GR SS and GS organism; FASTA write drops them (documented behaviour) - round trip identical; FASTA text has no annotation
- [PASS] Malformed user regex given to filter_by_id fails with a clear error rather than an empty alignment - re.error: unterminated character set at position 0
- [FAIL] Consensus and conservation are case-insensitive for soft-masked DNA - consensus@0.7 'ACGTNNNN'; find_conserved_positions(1.0) reports 0 of 8 unanimous columns
- [FAIL] SKILL guidance 'compute sequence weights before any column-wise statistic' is actionable with the shipped functions - no function among find_conserved_positions/consensus_sequence/gaps_per_column accepts weights

**Output (trimmed, from `run/in7_output.txt`):**
```
letter_annotations keys: [['secondary_structure'], ['secondary_structure']]
column_annotations keys: ['reference_annotation', 'secondary_structure']
annotations keys: [['accession', 'organism'], ['accession', 'organism']]
[PASS] usage-guide snippet: 'secondary_structure' key in record.letter_annotations finds the GR SS line (key name verified correct for Biopython 1.88)  -- printed=[('seqA', 'HHHEEEC'), ('seqB', 'HHH-EEC')]; actual keys=[['secondar
[PASS] usage-guide snippet: alignment.column_annotations.get('secondary_structure') returns SS_cons (key name verified correct)  -- got 'HHHEEEC'; actual keys=['reference_annotation', 'secondary_structure']
REAL Pfam letter_annotation keys: {'GR:pAS': 2, 'active_site': 1} | column_annotations: ['GC:seq_cons']
[PASS] REAL Pfam seed carries no GR SS lines, so the snippet correctly prints nothing there (GR keys present are other tags)  -- 0 records; keys {'GR:pAS': 2, 'active_site': 1}
after stockholm round trip: col keys ['reference_annotation', 'secondary_structure'] | rec keys [['secondary_structure'], ['secondary_structure']] [['accession', 'organism'], ['accession', 'organism']]
[PASS] stockholm round-trip preserves GC (SS_cons, RF) and GR SS  (SKILL.md/usage-guide claim)  -- # STOCKHOLM 1.0 | #=GF SQ 2 | seqA ACDEFGH | #=GS seqA AC seqA | #=GS seqA DE seqA | #=GS seqA OS Homo sapiens | #=GR seqA SS HHHEE
[PASS] stockholm round-trip preserves GS metadata (organism) (usage-guide claim)  -- [{'accession': 'seqA', 'organism': 'Homo sapiens'}, {'accession': 'seqB', 'organism': 'Mus musculus'}]
[PASS] FASTA write discards annotations (claim: 'silently discarded')
cleaned -> stockholm text has GR/GC lines: False False
[FAIL] skill cleaning (remove_gappy_columns) then write('stockholm') keeps SS_cons/RF [FAIL = annotations silently dropped; usage-guide says 'keep a Stockholm master copy']
mixed-case DNA consensus @0.7: ACGTNNNN
[FAIL] case-insensitive consensus @0.7: every column is one base in either case -> 'ACGTACGT' [FAIL = Counter is case-sensitive, split votes fall below threshold and give N]  -- ACGTNNNN
[FAIL] case-insensitive conservation: all 8 columns fully conserved [FAIL = 0 columns reported for cols 4-7 due to case split]  -- 0 reported
[PASS] filter_by_id with a malformed user regex fails with a clear re.error (no silent empty result)  -- re.error: unterminated character set at position 0
[PASS] filter_by_id treats pattern as regex: 'seqA|seqB' matches both
SummaryInfo methods still present on Biopython 1.88: []
[FAIL] SKILL note says AlignInfo.SummaryInfo is 'deprecated' (emits warnings); on the tested 1.88 the methods are REMOVED (AttributeError) [FAIL = doc understates]  -- present: []
functions accepting a weights argument: []
[FAIL] SKILL says 'compute sequence weights before any column-wise statistic', yet no column-wise function (conserved/consensus/gaps) accepts weights [FAIL = guidance not actionable]  -- none of find_conserved_positions / consensu

ASSERTIONS: 8/13 passed
  FAILED: skill cleaning (remove_gappy_columns) then write('stockholm') keeps SS_cons/RF [FAIL = annotations silently dropped; usage-guide says 'keep a Stockholm master copy'] 
  FAILED: case-insensitive consensus @0.7: every column is one base in either case -> 'ACGTACGT' [FAIL = Counter is case-sensitive, split votes fall below threshold and give N] ACGTNNNN
  FAILED: case-insensitive conservation: all 8 columns fully conserved [FAIL = 0 columns reported for cols 4-7 due to case split] 0 reported
  FAILED: SKILL note says AlignInfo.SummaryInfo is 'deprecated' (emits warnings); on the tested 1.88 the methods are REMOVED (AttributeError) [FAIL = doc understates] present: []
  FAILED: SKILL says 'compute sequence weights before any column-wise statistic', yet no column-wise function (conserved/consensus/gaps) accepts weights [FAIL = guidance not actionable] none of find_conserved_positions / consensus
```

## Research Veto (Data Analysis)
M1 PASS, M2 PASS, M3 PASS, M4 PASS (details in the JSON). Not-run item: GUIDANCE2.

## Recommendations
**[P1] Gap symbol hard-coded to '-'; '.' and lowercase break every helper silently**  
Observed in: [3, 7]  
Problem: On '.'-gapped input (hmmalign/A2M) gaps_per_column returns zeros, coordinate_map treats '.' as residues (len 6 instead of 4) and consensus emits '.'; on soft-masked DNA consensus gives ACGTNNNN and find_conserved_positions reports 0 of 8 unanimous columns.  
Root cause: All snippets compare against the literal '-' and use case-sensitive Counter without a normalisation step.  
Fix: Add a documented normalize_alignment() step (replace '.' with '-', optionally upper-case) that every snippet and example calls, or accept gap_chars and case_sensitive arguments; assert on a '.'-gapped synthetic file.

**[P1] mi_apc.py ignores the Skill's own APC guard; output is noise on the shipped test case**  
Observed in: [5]  
Problem: On the real Pfam seed (L=141, Neff/L=0.47) mi_apc.py prints 20 'coevolving column pairs' with no caveat; the top score (0.603) is below a column-shuffled null (0.616) and 0/30 top pairs are contacts in 1MBN (baseline 0.11). Thresholds also disagree: SKILL.md Neff section and neff.py say Neff/L > 0.5, the APC section says Neff/L > 1.  
Root cause: Guard exists only in prose; the example applies APC unconditionally and the DCA threshold is stated two ways.  
Fix: Compute Neff inside mi_apc.py main, print a warning and return raw MI (or refuse) when L<=100 or Neff/L<=1, unify the Neff/L threshold across SKILL.md and neff.py, and add a shuffled-column null to the example.

**[P1] Protein consensus default 'N' is asparagine**  
Observed in: [1]  
Problem: consensus_sequence(ambiguous='N') on the real 73-globin seed returns 124 'N' at 0.5, of which only 2 are true Asn-plurality columns, so the consensus cannot be read as a protein sequence. The shipped consensus_sequence.py uses the same default.  
Root cause: Default placeholder was chosen for nucleotides and the function is not alphabet-aware.  
Fix: Default to 'X' for protein (detect alphabet or add an alphabet argument), keep 'N' for DNA, and state that the threshold denominator includes gap rows.

**[P1] Henikoff/Neff prose contradicts itself and Easel; NaN on all-gappy alignments**  
Observed in: [5]  
Problem: SKILL.md says HMMER pb 'includes gaps as a residue type'; the example docstring says it 'restricts to ungapped columns'; pyhmmer docs say pb ignores gaps, uses consensus columns and double-normalises by length (skill vs Easel max diff 0.0091, Spearman 0.909). Easel pb/blosum weights sum to N (73) so they are not an Neff, yet the Neff table uses pb as 'baseline'; hmmbuild eff_nseq is 6.35 vs 66.08 (10x, not '2-3x'). henikoff_weights returns NaN when every column has a gap.  
Root cause: Estimator descriptions were written from memory and never checked against pyhmmer output.  
Fix: Rewrite the Henikoff edge-case and Neff-estimator paragraphs from pyhmmer's documented behaviour, state that compute_weights() outputs sum to N, add a guard raising ValueError when no gap-free column exists, and give one runnable pyhmmer comparison snippet.

**[P2] Cleaning helpers silently drop annotations and can return empty alignments**  
Observed in: [2, 7]  
Problem: remove_gappy_columns rebuilds SeqRecords without annotations/letter_annotations/column_annotations, so writing Stockholm afterwards loses GC/GR lines; filter_by_gap_content(0.1) on the real seed returns 0 of 73 without any message.  
Root cause: New SeqRecord objects carry only id and description; no post-filter size check.  
Fix: Slice records (record[i:j] style or copy annotations) or note the loss next to the code; raise/print when a filter removes every sequence.

**[P2] GUIDANCE2 recommended twice but no longer installable; pyhmmer minimum version missing**  
Observed in: [6]  
Problem: GUIDANCE2 (0.93 threshold) is named in unreliable-region step 3 and the trimming matrix; its download URL now returns an HTML page. compute_weights needs pyhmmer >= 0.11.3 but the version block lists only BioPython and numpy. SummaryInfo is called deprecated while its methods are removed in 1.88.  
Root cause: External-tool advice and version block not re-verified.  
Fix: Give the MUSCLE5 route as the runnable command (muscle -align in.fa -stratified -output ens.efa; muscle -letterconf ens.efa -ref aln.afa -output conf.afa, both verified to exist in 5.3), add pyhmmer>=0.11.3 to the version block, say SummaryInfo methods are removed.

**[P2] Duplicated code has drifted; weighting guidance not actionable; unverified estimator claims**  
Observed in: [1, 7]  
Problem: Every function is duplicated in SKILL.md and examples/ (dedup per doctrine); find_conserved differs between the two; 'compute weights before any column-wise statistic' but no statistic accepts weights; gap-handling advice says prefer SIC 'or fifth-state' right after calling fifth-state biologically problematic; AlphaFold2 'unweighted cluster count at 62%' ratio table is unsourced.  
Root cause: Prose and example scripts maintained separately.  
Fix: Keep one copy (import from examples/ or trim SKILL.md to signatures), add a weights= argument to the conservation/consensus helpers, fix the contradictory sentence, and source or remove the unsupported table rows.

**[P2] Examples need input files that are not shipped; position-numbering ambiguity**  
Observed in: [3, 4]  
Problem: Examples read alignment.fasta and hhsearch_output.a2m that the Skill does not ship (all 9 ran only after supplying data); the docs name seq_to_aln[42] 'column_for_residue_42' although it is the 43rd residue (0-based); the PDB numbering offset (1MBN is UniProt index n = residue n) is real but only referenced.  
Root cause: Examples are illustrative fragments without fixtures.  
Fix: Ship a tiny FASTA and A2M under examples/data, take the path as argv, and add a one-line note that PDB numbers are offset from UniProt (checked: 1MBN His93 = UniProt 94).

## Files
`run/` holds every script (common.py, skill_md_funcs.py = verbatim SKILL.md functions checked against SKILL.md by in1, mkdata.py, probe1.py, in1..in7, in5b, build_report.py, .sh files) and `run/data/` (real: pfam_PF00042_seed_from_real.fasta, globins8_mafft_linsi.fasta, trimAl/ClipKIT outputs, hmmbuild_out.txt, pf.hmm; SYNTHETIC: every `syn_*` file and hhsearch_output.a2m). Real inputs live in `F:\OpenScience\audit-envs\alignment\public-data\msa` and `...\structures\1MBN.pdb`.
