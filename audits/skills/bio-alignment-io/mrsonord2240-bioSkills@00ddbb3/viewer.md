> **Audit record for `bio-alignment-io`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@00ddbb3](https://github.com/mrsonord2240/bioSkills/tree/00ddbb34e81668b221fb96daa59530e7432495fa/alignment/alignment-io) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-alignment-io (SECOND RE-AUDIT of the fixed Skill)

Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@00ddbb34e81668b221fb96daa59530e7432495fa:alignment/alignment-io` (worktree `F:\OpenScience\wt\al-io2`, branch `fix/al-io2`, read-only; `run\skill\` is a copy, `diff -r` identical; every example ran from a copy under `run\scratch`, removed afterwards).
Previous: first re-audit 85, Limited Release, 32/39 assertions (archived at `_pre-fix-20260920\bio-alignment-io\`). Auditor: a fourth agent, different from the first auditor, the first re-auditor and both fixers.
Category: Data Analysis | Mode: A (shipped examples run) | Complexity: Complex, 8 inputs (6 regression areas, 2 NEW: inputs 5 and 8)

## Result

| | First re-audit | This re-audit |
|---|---|---|
| Static | 85 | **86** |
| Execution average | 85.2 | **86.9** |
| Final | 85 | **87** (34.4 + 52.1 = 86.5) |
| Grade | Limited Release, deployable | **Limited Release, deployable** |
| Assertions | 32/39 (82%) | **33/39 (85%)** |
| Vetoes | none | none (Skill veto PASS, Research veto PASS) |
| Open P0 / P1 / P2 | 0 / 2 / 5 | **0 / 0 / 6** |

Grade note: 87 is numerically Production Ready, but the assertion pass rate (84.6%) is below the 90% floor for Production Ready (scoring_rubric section 5), so it drops one tier. Other floors met: L1 avg 35.1/40, L2 avg 51.8/60, static 86, execution 86.9.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression + round-2 targets) | 36 | 53 | 89 | 4/5 PASS | ✅ |
| 2 | Variant A (regression: Stockholm, Rfam, Infernal/HMMER) | 36 | 54 | 90 | 5/5 PASS | ✅ |
| 3 | Edge (regression: PHYLIP, every code block verbatim) | 36 | 54 | 90 | 5/5 PASS | ✅ |
| 4 | Variant B (regression: real MAF, A2M/A3M) | 37 | 54 | 91 | 5/5 PASS | ✅ |
| 5 | Stress (**NEW**: end-to-end real data through the examples to MrBayes/IQ-TREE/RAxML-NG/codeml) | 33 | 48 | 81 | 3/5 PASS | ✅ |
| 6 | Scope Boundary (regression: format table cell by cell) | 36 | 54 | 90 | 4/4 PASS | ✅ |
| 7 | Adversarial (regression: corrected tool claims on real tools) | 35 | 51 | 86 | 4/5 PASS | ✅ |
| 8 | Edge (**NEW**: alphabet-inference stress, 15 cases; RNA in MrBayes) | 32 | 46 | 78 | 3/5 PASS | ✅ |

**Execution Average: 86.9 / 100** | **Assertion Pass Rate: 33/39** | Executed 8/8. Each `run\i*.out` holds the raw output and its `ASSERTIONS: k/n` line (probes are finer-grained than the 3-5 scored assertions per input); all scripts are in `run\`.

Run order to reproduce: `i0`, `i1`, `i2`, `i2b` (+ `i2b_infernal.sh`), `i3`, `i3b`, `i3c`, `i4`, `i4b_a2m.sh` then `i4b_a2m.py`, `i6`, `i6c_*` (i2b needs `data\pf.clustal` from `i6`), `i5_mafft.sh`, `i5_e2e_prep.py`, `i5_tools.sh`, `i5_check.py`, `i7_prep.py`, `i7b_prep.py`, `i7_recipe.py`, `i7_tools.sh`, `i7_check.py`, `i8_infer.py` (needs `data\e2e` from input 5), `i8_mb_prep.py`, `i8_mb.sh`, `i8_mb_check.py`, `finalize_report.py`. WSL scripts run with `MSYS2_ARG_CONV_EXCL='*' wsl.exe -d science -- bash -lc 'bash /mnt/openscience/audits/bio-alignment-io/run/<script>.sh'`.

## Round-2 targets and my own verdict on each

| Round-2 change | Verdict | Evidence |
|---|---|---|
| convert_formats.py alphabet inference (protein NEXUS said datatype=dna) | **Fixed for normal data**; edge holes remain | Real Pfam and UniProt -> `datatype=protein`, real HBB (lower case) -> dna, real Rfam 954 seqs -> rna, RNA/protein/DNA overrides validated case-insensitively, wrong-alphabet override exits 1 (i1, i8_infer). Holes: >10% IUPAC or X -> protein; mixed T+U -> unreadable NEXUS; RNA-vs-DNA override -> traceback + 0-byte output.nex (P2s). |
| RAxML-NG `*` row | **Correct** | 1.2.2 and 2.0.3: DNA `ERROR: Invalid character in sequence 5 at position 4: *`; protein search lnL -2826.143822 / -2826.143824, identical with `*`, `-` and `X` at that site (i7.out) |
| PhyML 100-char row replaced | **Correct** | 3.3.20220408 and 3.3.20260528 keep 138-char names; `:` and `,` -> "Character ... is not permitted in sequence name"; `(1)` accepted and written into the Newick (`GLB(1):0.5138`) |
| MrBayes quote-free id recipe | **Works** | Block executed verbatim: 73 Pfam ids -> `[A-Za-z0-9_]+`, unique; collision assertion fires; MrBayes 3.2.7 "Analysis completed" on DNA (HBB), protein (Pfam, globins) and RNA (Rfam subset, "Data is Rna") NEXUS; original quoted file: "Instead found ''' in command 'Matrix'" |
| Batch block mkdir | **Fixed** | Verbatim block with no pre-existing `converted/` writes g1.fasta, g2.fasta (i3b) |
| Bio.Align table cells | **Correct** | A2M R/W (writer AttributeError on FASTA-read alignment, read-write-read identical 73x141), PHYLIP strict-only (relaxed file raises `Expected all sequences to have length 141; found 148`), PSL/chain/BED/SAM/exonerate/bigMaf/bigPsl/bigBed R/W, HHR/tabular R-only (i6.out, 70/70) |
| read_alignment.py cwd + label | **Fixed** | Runs from an unrelated cwd, prints "columns" (i1) |
| New sentence "RAxML-NG and IQ-TREE accept 138-char names" | **True** | RAxML-NG 1.2.2/2.0.3 `--check` and IQ-TREE 3.1.3 (i7.out) |

## Detailed Outputs

### Input 1 - Canonical (regression + round-2 targets): shipped examples from a clean copy
**Prompt:** "Read this Clustal alignment, convert it to FASTA / PHYLIP / NEXUS, slice columns, batch-convert a directory" with the four shipped examples, no arguments, then real Pfam PF00042 (73x141) as Clustal, then bad overrides.
**Ran:** `run\i1_examples.py`.
```
sample, no args:  convert_formats.py -> "Molecule type: DNA" ... "Checked: output.nex says datatype=dna"; fasta/phy/nex re-read 4x21 identical
real Pfam, DEFAULT / protein / Protein:  "Molecule type: protein", NEXUS "format datatype=protein", re-read 73x141 identical (x3)
override foo | protein | Protein on DNA sample: exit 1, no NEXUS ; "Unknown molecule type 'foo': use DNA, RNA or protein"
synthetic RNA (T->U): inferred RNA, datatype=rna, re-reads identical; override DNA -> exit 1, no usable NEXUS
override RNA / rna on the DNA sample: exit 1 "ValueError: seq1 contains T, but RNA alignment"; output.fasta and output.phy written, output.nex size 0
read_alignment.py / slice / batch / convert from an unrelated cwd: exit 0, 4 sequences
```
**Scores:** Basic 36 | Specialized 53 | Total 89
**Assertions:**
- [PASS] All four examples run from a clean copy and outputs re-read identically.
- [PASS] Real protein alignment is labelled protein by default; NEXUS says datatype=protein.
- [PASS] Contradicting protein/nucleotide overrides exit non-zero with a message and write no NEXUS.
- [PASS] Every example resolves its input regardless of cwd.
- [FAIL] Nucleotide-vs-nucleotide override (RNA on T, DNA on U) is refused cleanly - traceback, two files already written, 0-byte NEXUS.

### Input 2 - Variant A (regression): Stockholm, real Pfam and Rfam, downstream rebuild
**Prompt:** "Parse this Pfam and this RNA Stockholm, show me the secondary structure, convert to NEXUS, and make sure Infernal and HMMER can still build from what I write."
**Ran:** `run\i2_stockholm.py`, `run\i2b_rfam_real.py`, `run\i2b_infernal.sh`. Real: Pfam seed, Rfam RF00005 (954 x 118). SYNTHETIC: `data\synthetic_rna.sto`.
```
Pfam GLB2_LUMTE/31-141 annotations {'accession': 'P02218.2', 'start': 31, 'end': 141}; round trip #=GF 56 -> 1 (Rfam 40 -> 1)
Align.read(real Pfam,'stockholm') -> TypeError: Any per-letter annotation should be a Python sequence ...
Align.write(FASTA-read,'stockholm') -> AttributeError: ... no attribute 'column_annotations'
snippet on Rfam: ss_cons length 118 == source '#=GC SS_cons'; stockholm->nexus molecule_type='RNA' 954x118 datatype=rna
cmbuild original: tRNA 954 seqs clen 71 ACC RF00005 | round trip: rfam_roundtrip 954 seqs clen 71, ACC/DESC lost
hmmbuild original Globin 73x141 LENG 117 | round trip pf_rt 73x141 LENG 117
```
**Scores:** Basic 36 | Specialized 54 | Total 90
**Assertions:** all 5 PASS (annotation snippet; GF-drop claim; Bio.Align Stockholm errors; RNA NEXUS route; rebuild with metadata lost).

### Input 3 - Edge (regression): PHYLIP pitfalls, every code block verbatim, Common Errors
**Ran:** `run\i3_phylip.py`, `i3b_blocks.py`, `i3c_streaming.py` (51 probes, all pass). Real Pfam/NCBI ids; SYNTHETIC collision alignment.
```
strict phylip / phylip-sequential write of Homo_sapiens_chr1/chr2 -> ValueError: Repeated name 'Homo_sapie'
phylip-relaxed writer: 'a:1' -> 'a|1', 'b(2)' -> 'b2', 'c,3' -> 'c3'
Batch Processing block (verbatim, converted/ absent): converted/g1.fasta + g2.fasta written, re-read 73 records     <-- was FileNotFoundError in the first re-audit
MrBayes recipe block (verbatim): GLB2_LUMTE/31-141 -> GLB2_LUMTE_31_141, 73 unique; a-1 / a+1 -> AssertionError 'ids collide after sanitizing'
streaming block (verbatim): Globin_copyN 73 141 sum_w=73.0 x3
Common Errors 5/5 messages reproduce; z.nex 0 bytes after the molecule-type failure
```
**Scores:** Basic 36 | Specialized 54 | Total 90
**Assertions:** all 5 PASS.

### Input 4 - Variant B (regression + real data): MAF strand helper, A2M, A3M
**Ran:** `run\i4_maf.py` (real Biopython `ucsc_mm9_chr10.maf`, genome bases from api.genome.ucsc.edu), `run\i4b_a2m.sh`, `run\i4b_a2m.py` (real hmmalign A2M, HH-suite reformat.pl/hhfilter).
```
real MAF vs UCSC genome: minus 40/40, plus 12/12, old '== "-"' helper 0/40 (22 rows skipped: assembly not served by the API)
hmmalign A2M: ragged, AlignIO fasta -> ValueError; SeqIO snippet 8 rows x 117 = HMM LENG 117; reformat.pl A2M rectangular 73x141
reordered A3M -> A2M residues differ at 104 positions (first-record pitfall real); hhfilter keeps first record
AlignIO 'a3m' -> Unknown format; pyhmmer format='a3m' -> InvalidParameter
```
**Scores:** Basic 37 | Specialized 54 | Total 91
**Assertions:** all 5 PASS.

### Input 5 - Stress (NEW): real data end to end through the examples and the downstream tools
**Prompt:** "I have 6 HBB CDS and 8 UniProt globins aligned with MAFFT. Convert them with the Skill's example, then run MrBayes, IQ-TREE, RAxML-NG and codeml."
**Ran:** `run\i5_mafft.sh` (MAFFT 7.526; ids kept as `lcl|NM_000518.5` and `sp|P02185|MYG_PHYMC`), `i5_e2e_prep.py`, `i5_tools.sh`, `i5_check.py`. Real: RefSeq HBB CDS x6 (NM_001314043.1 with an internal stop excluded), UniProt globins x8.
```
convert_formats.py: hbb6 -> Molecule type DNA, datatype=dna ; globins8 -> protein, datatype=protein ; fasta/phy/nex re-read identical
MrBayes 3.2.7, example NEXUS: "Unrecognized DNA/RNA character '|'" / "Unrecognized Protein character '|'"  (Biopython did NOT quote these ids: 0 quote chars)
MrBayes 3.2.7, after the SKILL recipe (lcl|NM_000518.5 -> lcl_NM_000518_5): "Analysis completed" for hbb6 (dna) and globins8 (protein)
IQ-TREE 3.1.3 -n 0: "Alignment has 6 sequences with 444 columns" / "8 sequences with 155 columns"; RAxML-NG 2.0.3 --check: "successfully read" (DNA and AA, ids with | and .)
codeml (phylip-sequential, ids N518 ...): omega (dN/dS) = 0.28841, lnL -1255.056744 ; phylip-relaxed: "Error in sequence data file: X at 51 seq 1. Make sure to separate the sequence from its name by 2 or more spaces."
phylip-sequential with real NCBI ids: ValueError Repeated name 'lcl|NM_001'
Clustal writer probe: ids 'lcl|NM_000518.5_cds_NP_000509.1_1' and '..._2' -> both come back as 'lcl|NM_000518.5_cds_NP_000509.' (30 chars, no error)
```
(An earlier attempt with full-length NCBI ids exposed the Clustal truncation; the final run trims ids to the accession so the pipeline is meaningful and the truncation is asserted as its own probe.)
**Scores:** Basic 33 | Specialized 48 | Total 81
**Assertions:**
- [PASS] The example labels real MAFFT alignments correctly and its outputs re-read identical.
- [FAIL] The NEXUS the example writes for real NCBI/UniProt ids loads in MrBayes - it does not (pipe); the SKILL's quoted-id explanation does not describe this.
- [PASS] After the SKILL recipe MrBayes loads and completes for DNA and protein.
- [PASS] IQ-TREE, RAxML-NG and codeml accept the files the SKILL says to write; codeml rejects relaxed with the quoted message.
- [FAIL] The SKILL warns about id truncation for every text format it tells the agent to write - Clustal 30-char truncation (silent, duplicates) is not mentioned.

### Input 6 - Scope Boundary (regression + round-2 cells): Format Coverage Map cell by cell
**Ran:** `run\i6_format_table.py` (70 probes), `i6c_foldmason.sh`, `i6c_foldmason_read.py` (5). Real: Biopython test MSF/Mauve, Pfam, hmmalign/reformat.pl A2M from input 4, 1MBN/1A6M/1EMY Foldmason. SYNTHETIC: one-line PSL/chain.
```
Bio.Align.formats: a2m bed bigbed bigmaf bigpsl chain clustal emboss exonerate fasta hhr maf mauve msf nexus phylip psl sam stockholm tabular
a2m (True, True); hhr and tabular (True, False); psl/chain/bed/sam/exonerate/bigmaf/bigpsl/bigbed reader+writer present
Align.write(FASTA-read,'a2m') -> AttributeError 'column_annotations'; A2M read (reformat.pl padded) -> write -> re-read identical (73,141), annotation keys ['state']
Align.read('pf.phy' = phylip-relaxed real ids,'phylip') -> ValueError Expected all sequences to have length 141; found 148
Foldmason result_aa.fa/result_3di.fa: AlignIO 3x153, 1MBN vs 1A6M identity 1.000; result.html not parseable
```
**Scores:** Basic 36 | Specialized 54 | Total 90
**Assertions:** all 4 PASS (Bio.Align cells exact; NOT-in-Biopython table accurate; pyhmmer column exact; Foldmason MSAs load).

### Input 7 - Adversarial (regression): corrected tool claims on real RAxML-NG, PhyML, IQ-TREE, MrBayes
**Ran:** `run\i7_prep.py`, `i7b_prep.py`, `i7_recipe.py`, `i7_tools.sh`, `i7_check.py` (26 checks) in WSL private envs `aln-raxml1`, `aln-treetools`, `aln-phyml-old`, `bio` (versions in the report). Real Pfam rows; SYNTHETIC injected names/characters.
```
RAxML-NG 1.2.2 / 2.0.3: DNA '*' -> ERROR: Invalid character in sequence 5 at position 4: * ; protein '*' lnL -2826.143822 / -2826.143824 == '-' == 'X'
PhyML 3.3.20260528: ':' and ',' -> "Character ':' is not permitted in sequence name" ; '(1)' accepted, Newick has GLB(1):0.51379855 ; 138-char names kept (both builds)
RAxML-NG rejects ':' ',' '(' '[' : "Following taxon name contains invalid characters"
PhyML on a name containing '[': exit 139 (crash after the initial tree)
IQ-TREE 3.1.3: -n 0 -m LG -> "Alignment has 12 sequences with 141 columns"; wrong length -> "ERROR: Line 39: Sequence MYG_HETPO/23-138 has wrong sequence length 137"; --check -> Invalid "--check" option; ':' name -> WARNING names changed
MrBayes 3.2.7: Biopython NEXUS (quoted Pfam ids) -> "Instead found ''' in command 'Matrix'"; recipe output -> "Analysis completed"
Biopython NEXUS id quoting, per character: quoted - + : ; , ( ) [ ] ' " = * space ; plain / . | _ # @ % & !
```
**Scores:** Basic 35 | Specialized 51 | Total 86
**Assertions:**
- [PASS] Corrected RAxML-NG row right on 1.2.2 and 2.0.3.
- [PASS] Replaced PhyML row right on two builds.
- [PASS] IQ-TREE guidance and 138-char acceptance hold.
- [PASS] MrBayes quoted-id failure and the recipe hold.
- [FAIL] Names sanitised with the table's regex `[():,]` are accepted by PhyML and RAxML-NG - `[` is not covered (PhyML crash, RAxML-NG error).

### Input 8 - Edge (NEW): alphabet-inference stress and RNA NEXUS in MrBayes
**Prompt:** "Convert these alignments with the shipped script, whatever they are: real HBB/Rfam/Pfam/UniProt, a degenerate-primer alignment with lots of ambiguity codes, masked sequences, lower case, mostly gaps, mixed T/U, nothing but gaps."
**Ran:** `run\i8_infer.py`, `i8_mb_prep.py`, `i8_mb.sh`, `i8_mb_check.py`. SYNTHETIC cases are substitutions into the real HBB alignment (labelled in the script).
```
case                          nuc-fraction  truth      label     NEXUS datatype  exit  re-read
real_HBB_CDS_lowercase        1.0           DNA        DNA       dna             0     True
real_Rfam_tRNA_954            1.0           RNA        RNA       rna             0     True (954x118)
real_Pfam_PF00042             0.267         protein    protein   protein         0     True
real_UniProt_globins          0.269         protein    protein   protein         0     True
HBB_5pct_IUPAC                0.951         DNA        DNA       dna             0     True
HBB_12pct_IUPAC               0.881         DNA        protein   protein         0     True    <-- silent mislabel
HBB_12pct_N                   1.0           DNA        DNA       dna             0     True
HBB_12pct_X_mask              0.881         DNA        protein   protein         0     True    <-- silent mislabel
HBB_lowercase_RNA             1.0           RNA        RNA       rna             0     True
HBB_90pct_gaps                1.0           DNA        DNA       dna             0     True
mixed_1DNA_5RNA_rows          1.0           ambiguous  DNA       dna             0     ERR NexusError   <-- unreadable file, exit 0
all_gap                       -             n/a        -         -               1     "No residues in the alignment"
tiny_DNA_3x4                  1.0           DNA        DNA       dna             0     True
protein_only_ACGTN_letters    1.0           protein    DNA       dna             0     True    (inherently ambiguous; not asserted)
glob_with_terminal_stop       0.269         protein    protein   protein         0     True
MrBayes 3.2.7, Rfam subset (12 x 90): example NEXUS -> "Instead found ''' in command 'Matrix'" ; recipe NEXUS -> "Data is Rna", 12 taxa 90 characters, Analysis completed
```
**Scores:** Basic 32 | Specialized 46 | Total 78
**Assertions:**
- [PASS] Real data labelled correctly and NEXUS re-reads with the same shape.
- [PASS] Lower case, 90% gaps, 12% N, lower-case RNA, terminal star, tiny DNA labelled correctly; all-gap exits cleanly.
- [PASS] datatype=rna loads in MrBayes 3.2.7 after the recipe.
- [FAIL] Nucleotide alignment with >10% ambiguity codes or X masks is labelled nucleotide - labelled protein.
- [FAIL] Mixed T+U alignment fails loudly or gives a readable file - exit 0, `datatype=dna`, NEXUS unreadable.

## Static score (25 criteria, 8 categories)

| Category | Score | Note |
|---|---|---|
| Functional Suitability | 11/12 | Both false tool claims corrected and verified; MrBayes recipe added; MrBayes explanation covers quoted ids only, sanitiser regex leaves `[ ]`, Clustal truncation unmentioned |
| Reliability | 9/12 | Common Errors exact, guards on bad input; inference/override holes (P2) |
| Performance/Context | 6/8 | 472 lines, single file, no references/ |
| Agent Usability | 14/16 | Goal/Approach, version stamps, ground-truth loop, IQ-TREE check, datatype assert; error prevention gaps |
| Human Usability | 7/8 | Natural prompts, table-driven format choice |
| Security | 11/12 | No credentials/eval/network; silent overwrite in cwd |
| Maintainability | 10/12 | Version-stamped, every changed claim re-verified; one file |
| Agent-Specific | 18/20 | Precise trigger, cross-refs exist, safe re-runs; no references layer |
| **Subtotal** | **86** | |

## Vetoes

- Skill veto: T1 PASS (20 of 20 Python blocks and 4 of 4 examples run; the Batch block that failed before now runs), T2 PASS, T3 PASS (no random elements in the Skill's code; re-runs of i2b, i3c, i5_e2e_prep and i6 gave identical assertion counts; MAF ground-truth counts 40/40, 12/12, 0/40 identical to the first re-audit), T4 PASS (no eval/exec of user strings, no shell).
- Research veto: M1 PASS, M2 PASS, M3 PASS (heuristic edge cases are P2, not a fallacy), M4 PASS.

## Recommendations (all P2; no open P0/P1)

1. **Inference holes** (input 8): count ACGTUNRYKMSWBDHV as nucleotide, refuse mixed T+U, re-read `output.nex` before printing the datatype check.
2. **RNA/DNA override mismatch** (input 1): refuse before writing; today a traceback and a 0-byte NEXUS after fasta/phy exist.
3. **Clustal 30-char id truncation** (input 5): document; silent, produces duplicate ids.
4. **MrBayes ids** (input 5): say "characters outside [A-Za-z0-9_]" fail (quoted or not, `|` too), apply the recipe in `convert_formats.py` or warn.
5. **Sanitiser regex** (input 7): `[():,]` leaves `[ ]`; point the table at `[^A-Za-z0-9_]`.
6. **SKILL.md structure**: one 472-line file, no `references/`.

## Checked and found fine (no finding)

- Everything the fixer's Round 2 changed, listed in the table above, reproduced on the real tools. The two claims I was told to distrust (RAxML-NG `*`, PhyML 100 chars) are now stated correctly.
- MAF strand helper, A2M/A3M text, pyhmmer streaming block, Common Errors rows, GF/GC annotation statements: unchanged since the first re-audit and still exact.
- `usage-guide.md` untouched in Round 2 (`git diff 818f049 00ddbb3` lists only SKILL.md, convert_formats.py, read_alignment.py).
- No `__pycache__` in `F:\OpenScience\wt\al-io2`, in the external clone, or in `run\skill`.

## What was not exercised

`iqtree2` (only IQ-TREE 3.1.3), PAUP*, Pfam-A.full streaming (three seed copies stand in), MAF rows from assemblies the UCSC API does not serve (22 skipped), MrBayes runs beyond 200 generations (loading and completion only, not convergence).
