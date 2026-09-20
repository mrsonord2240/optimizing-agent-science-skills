> **Audit record for `bio-alignment-io`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@0f10851](https://github.com/mrsonord2240/bioSkills/tree/0f108510cff2e116434514f4514c1184837d3020/alignment/alignment-io) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-alignment-io (RE-AUDIT of the fixed Skill)

Generated: 2026-09-19
Source: `mrsonord2240/bioSkills@0f108510cff2e116434514f4514c1184837d3020:alignment/alignment-io` (worktree `F:\OpenScience\wt\al-io`, read-only; a byte-identical copy lives in `run\skill\`, verified with `diff -r`).
Pre-fix: 74, Beta Only (archived at `_pre-fix-20260919d\bio-alignment-io\`). Auditor: a third agent, different from the first auditor and from the fixer.
Category: Data Analysis | Mode: A (shipped examples also run from copies) | Complexity: Complex, 8 inputs (6 regression areas + 2 NEW inputs)

## Result

| | Pre-fix | Re-audit |
|---|---|---|
| Static | 77 | **85** |
| Execution average | 71.7 | **85.2** |
| Final | 74 | **85** (34.0 + 51.1) |
| Grade | Beta Only, not deployable | **Limited Release, deployable** |
| Assertions | 20/34 | **32/39 (82%)** |
| Vetoes | none | none (Skill veto PASS, Research veto PASS) |
| Open P0 / P1 / P2 | 0 / 4 / 3 | **0 / 2 / 5** |

Grade note: 85 sits at the Production Ready boundary, but the assertion pass rate (82%) is below the 90% floor for Production Ready (scoring_rubric section 5), so the grade drops one tier. Layer floors otherwise met: L1 avg 34.9/40, L2 avg 50.4/60, static 85, execution 85.2 (Limited floors 28/42/70/75 all met).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 35 | 50 | 85 | 3/5 PASS | ✅ |
| 2 | Variant A (regression) | 36 | 52 | 88 | 5/5 PASS | ✅ |
| 3 | Edge (regression) | 35 | 51 | 86 | 4/5 PASS | ✅ |
| 4 | Variant B (regression, real MAF + real A2M/A3M) | 37 | 54 | 91 | 5/5 PASS | ✅ |
| 5 | Stress (regression) | 36 | 52 | 88 | 5/5 PASS | ✅ |
| 6 | Scope Boundary (regression + extension) | 35 | 50 | 85 | 3/4 PASS | ✅ |
| 7 | Adversarial (**NEW**: downstream tools) | 28 | 40 | 68 | 2/5 PASS | ⚠️ |
| 8 | Variant B (**NEW**: real Rfam + Infernal/HMMER) | 37 | 54 | 91 | 5/5 PASS | ✅ |

**Execution Average: 85.2 / 100** | **Assertion Pass Rate: 32/39** | Executed 8/8.

## Regression of the first audit's findings (each re-tested by my own run)

| First-audit finding | Now | Evidence (run\) |
|---|---|---|
| MAF helper wrong for minus strand (66 vs 60) | **Fixed.** Synthetic: 60 == 60. Real UCSC MAF: 40/40 minus rows and 12/12 plus rows equal the genome sequence fetched from the UCSC API; the old `== '-'` test matches 0/40. The new ground-truth loop raises AssertionError when the old test is substituted. | i4.out |
| convert_formats.py NEXUS ValueError / 0-byte file | **Fixed** (set molecule_type). New side effect: default `DNA` silently mislabels protein NEXUS. | i1.out |
| Examples need unshipped alignment.aln; slice writes 0 columns; batch converts nothing | **Fixed.** Guards fire (exit 1) and nothing is written on refusal. `read_alignment.py` still cwd-dependent. | i1.out |
| pyhmmer streaming AttributeError | **Fixed.** Verbatim block prints `Globin_copyN 73 141 sum_w=73.0` x3. | i5.out |
| A2M/A3M claims (pyhmmer a3m; "A2M rectangular") | **Fixed.** Ragged hmmalign A2M (149-161), snippet gives 117 = LENG; reformat.pl A2M rectangular, 111 match columns; a3m rejected by AlignIO/pyhmmer. | i4b.out |
| Bio.Align recommended but fails on real Stockholm; tables stale | **Fixed** (AlignIO recommended; Common Errors rows reproduce). Two small understatements left (Bio.Align A2M writer; PHYLIP strictness). | i2.out, i6.out |
| PHYLIP overstated; `--check` invalid | **Fixed** (raises on collision; iqtree3 `-n 0 -m LG` check verified). | i3.out, i7_check.out |
| Pfam id / GF statements | **Fixed** (annotations filled; GF dropped: 56 -> 1 lines on Pfam, 40 -> 1 on Rfam). | i2.out, i8.out |
| usage-guide duplicates SKILL.md | **Fixed**; nothing the agent needs was lost (old guide compared line by line; install, downstream table, tips all in SKILL.md; section names the guide cites exist). | i0.out |
| RAxML-NG `*` and PhyML 100-char claims (fixer left unverified) | **Judged: both FALSE on current builds** (see input 7). | i7_check.out |

## Detailed Outputs

### Input 1 - Canonical (regression): shipped examples from a clean copy
**Prompt:** "Read this Clustal alignment, convert it to FASTA / PHYLIP / NEXUS, slice columns, and batch-convert a directory" using the four shipped examples, first on the shipped 4x21 DNA sample with no arguments, then on real Pfam PF00042 (73x141) as Clustal.
**Ran:** `run\i1_examples.py` (copies of `examples/` under `run\scratch`, removed afterwards).
```
convert_formats.py -> Wrote output.fasta / output.phy / output.nex ; all three re-read 4x21 identical ids+residues
slice_alignment.py -> trimmed_subset.fasta 4x10 == source cols 5:15
batch_convert.py   -> sample_alignment.aln -> sample_alignment.fasta (4 seqs)
Real Pfam, `convert_formats.py pfam.aln protein` -> fasta/phylip-relaxed/nexus re-read 73x141 identical ids+rows
batch_convert.py empty_dir -> exit 1 "No *.aln files found in empty_dir" ; slice on 10-col alignment -> exit 1 "Columns 5-15 are outside the 10-column alignment"
convert_formats.py pfam.aln (defaults) -> NEXUS line: format datatype=dna missing=? gap=-;      <-- protein labelled DNA
convert_formats.py x.aln dna -> ValueError: Need the molecule type to be defined
read_alignment.py from another cwd -> FileNotFoundError: 'sample_alignment.aln'
```
**Scores:** Basic 35/40 | Specialized 50/60 | Total 85
**Assertions:**
- [PASS] All four examples run from a clean copy and outputs re-read identically - 4x21 identical; slice = source 5:15; batch 1 file.
- [PASS] convert_formats.py on real Pfam with `protein` re-reads 73x141 identical.
- [PASS] slice/batch refuse bad input with non-zero exit and no 0-column file.
- [FAIL] convert_formats.py is safe for a protein alignment with default arguments - writes `datatype=dna`.
- [FAIL] Examples resolve their own inputs regardless of cwd - `read_alignment.py` traceback; prints "bp" for protein.

### Input 2 - Variant A (regression): Stockholm
**Prompt:** "Parse this Pfam and this RNA Stockholm, show me the secondary structure annotations, and convert to NEXUS."
**Ran:** `run\i2_stockholm.py`; the SKILL.md annotation block and the NEXUS block are extracted and exec()d verbatim. Real: Pfam seed. SYNTHETIC: `data\synthetic_rna.sto`.
```
AlignIO.read(real Pfam) 73x141 ; GLB2_LUMTE/31-141 annotations {'accession': 'P02218.2', 'start': 31, 'end': 141}
round trip: source 56 #=GF lines -> 1 ; #=GF ID/AC/DE absent
Align.read(real Pfam,'stockholm') -> TypeError: Any per-letter annotation should be a Python sequence ...
Align.write(FASTA-read Alignment,'stockholm') -> AttributeError: 'Alignment' object has no attribute 'column_annotations'
snippet -> "SS: <<<<___.>>>>....." ; ss_cons '<<<<___.>>>>.....'
stockholm->nexus molecule_type="RNA" -> re-reads 2x17, datatype=rna ; without it -> ValueError
```
**Scores:** Basic 36 | Specialized 52 | Total 88
**Assertions:**
- [PASS] Annotation snippet returns per-record SS and column SS equal to the file - `RF` is exposed as `reference_annotation`.
- [PASS] "AlignIO drops #=GF ID/AC/DE even Stockholm->Stockholm" - 56 -> 1 lines.
- [PASS] Pfam-id paragraph (start/end/accession filled; id keeps suffix).
- [PASS] Common Errors rows for Bio.Align Stockholm reproduce (TypeError / AttributeError).
- [PASS] RNA NEXUS route re-reads 2x17; missing molecule_type raises the documented error.

### Input 3 - Edge (regression): PHYLIP pitfalls, every plain SKILL code block, Common Errors
**Prompt:** "Export to PHYLIP for IQ-TREE and PAML; my names are long and some share a prefix" plus a run of each plain code block in SKILL.md on real Pfam.
**Ran:** `run\i3_phylip.py`, `run\i3b_blocks.py`. SYNTHETIC: 3-name collision alignment. Real: Pfam ids, NCBI HBB ids.
```
phylip / phylip-sequential write, Homo_sapiens_chr1 + chr2 -> ValueError: Repeated name 'Homo_sapie' (originally 'Homo_sapiens_chr2'), possibly ...
reading a foreign strict file with colliding names -> 2 records, both id 'Homo_sapie' (silent)
phylip-relaxed writer: 'a:1' -> 'a|1', 'b(2)' -> 'b2', 'c,3' -> 'c3'
real NCBI ids 'lcl|NM_001164428...' in phylip-sequential -> ValueError Repeated name 'lcl|NM_001'
Common Errors: 5/5 messages reproduce; z.nex size 0 after the molecule-type failure
alignment[:, 200:300] -> 73 records, 0 columns; FASTA written from it has 73 empty records
Batch Processing block (verbatim) -> FileNotFoundError: 'converted\\g1.fasta'   (block has no mkdir; batch_convert.py has it)
```
**Scores:** Basic 35 | Specialized 51 | Total 86
**Assertions:**
- [PASS] Strict writes raise on colliding 10-char prefixes; reading foreign strict files is the silent case.
- [PASS] Writer rewrites ":" to "|", drops "(" ","; NCBI ids collide in phylip-sequential as the Skill says.
- [PASS] Common Errors table reproduces message-for-message.
- [FAIL] Every plain code block runs verbatim - the Batch Processing block raises FileNotFoundError.
- [PASS] "Column slices past the alignment length silently return 0 columns" is accurate.

### Input 4 - Variant B (regression + real data): MAF strand helper, A2M, A3M
**Prompt:** "Lift these MAF blocks to plus-strand genome coordinates" and "load this HMMER/HH-suite alignment".
**Ran:** `run\i4_maf.py`, `run\i4b_a2m.sh`, `run\i4b_a2m.py`. Real: Biopython `Tests/MAF/ucsc_mm9_chr10.maf` (48 blocks, 270 rows, 190 minus), genome bases from `api.genome.ucsc.edu`, Pfam seed via hmmbuild/hmmalign (HMMER 3.4), HH-suite reformat.pl/hhfilter. SYNTHETIC (labelled): seeded 200-nt genome + hand-built MAF.
```
synthetic: fixed helper on minus row -> 60 (truth 60), strand annotation -1 (int); old '== "-"' -> 66
SKILL ground-truth loop: passes; with the old test substituted -> AssertionError
real MAF vs UCSC genome: minus 40/40 match, plus 12/12 match, old helper 0/40 (22 rows skipped: assembly not served by the API)
hmmalign A2M: row lengths [149,150,151,160,161]; AlignIO.read(...,'fasta') -> ValueError Sequences must all be the same length
SeqIO snippet: 8 rows x 117 (HMM LENG 117); reformat.pl A2M: 73x141, 111 match columns
reordered A3M (identical rows) -> A2M residues differ at 104 positions; hhfilter keeps first record, order unchanged
AlignIO 'a3m' -> Unknown format; pyhmmer format='a3m' -> InvalidParameter
```
**Scores:** Basic 37 | Specialized 54 | Total 91
**Assertions:**
- [PASS] Fixed helper correct on synthetic ground truth AND 40/40 real minus rows (old: 0/40).
- [PASS] The SKILL's ground-truth loop detects a wrong helper.
- [PASS] hmmalign A2M ragged; match-column snippet gives 117 = model length.
- [PASS] reformat.pl output rectangular; first-record pitfall real (104 residue positions change).
- [PASS] A3M has no reader anywhere; hhfilter does not reorder.

### Input 5 - Stress (regression): multi-alignment, pyhmmer streaming, PAML route
**Prompt:** "Stream the families in Pfam-A.full, and prepare 6 HBB CDS for codeml."
**Ran:** `run\i5_multi_pyhmmer.py`, `i5_align.sh` (MAFFT 7.526), `i5_paml.py`, `i5_run_codeml.sh` (PAML 4.10.10). Real: Pfam seed x3 (multi-family file), 6 RefSeq HBB CDS.
```
Globin_copy0 73 141 sum_w=73.0   (x3)          # verbatim streaming block
pyhmmer formats: afa, clustal, phylip, phylips, stockholm read Biopython-written files (73 seqs each)
codeml (phylip-sequential): omega (dN/dS) = 0.28303, lnL -1251.532237     # identical to the first audit
codeml (phylip-relaxed): Error in sequence data file: I at 53 seq 1. Make sure to separate the sequence from its name by 2 or more spaces.
```
**Scores:** Basic 36 | Specialized 52 | Total 88
**Assertions:** all [PASS] - streaming block runs verbatim; multi-alignment round trips (3 x 73x141); codeml result reproduces; codeml rejects relaxed with the quoted message; pyhmmer format cells exact.

### Input 6 - Scope Boundary (regression + extension): the Format Coverage Map cell by cell
**Prompt:** "Which formats can Biopython read/write; what about PSL, chain, MSF, Mauve, A3M, HAL, GFA?" and "load Foldmason MSAs".
**Ran:** `run\i6_format_table.py` (61 probe assertions, 60 pass), `i6c_foldmason.sh`, `i6c_foldmason_read.py`. Real: Biopython test MSF/Mauve files, Pfam seed, 1MBN/1A6M/1EMY. SYNTHETIC: one-line PSL/chain.
```
Bio.Align.formats: a2m bed bigbed bigmaf bigpsl chain clustal emboss exonerate fasta hhr maf mauve msf nexus phylip psl sam stockholm tabular
msf (R only) matches; mauve R/W matches; psl/chain/bed/sam R/W match; a2m is (reader, writer) = (True, True) but the table says R
Align.read('pf.phy' = AlignIO phylip-relaxed with real ids, 'phylip') -> ValueError: Expected all sequences to have length 141; found 148
Align.write(...,'phylip') -> ids silently cut to 10 chars ('GLB2_LUMTE')
Align.read plain Stockholm OK (2,9); synthetic annotated RNA -> AssertionError; real Rfam OK (954,118)
Foldmason result_aa.fa / result_3di.fa: AlignIO 3x153, 1MBN vs 1A6M identity 1.000; result.html not parseable
```
**Scores:** Basic 35 | Specialized 50 | Total 85
**Assertions:**
- [PASS] NOT-in-Biopython table (HAL, net, AXT, GFA/rGFA, GAF) is accurate.
- [FAIL] Every Bio.Align cell exact - A2M writer exists; Bio.Align PHYLIP strictness unstated.
- [PASS] pyhmmer column exact.
- [PASS] Foldmason MSAs load; report is HTML.

### Input 7 - Adversarial (NEW): does what the Skill tells the agent to write load in the tools it names?
**Prompt:** "Export the alignment for RAxML-NG / IQ-TREE / PhyML / MrBayes as the Skill's table says; my protein alignment has a stop `*` and some very long names."
**Ran:** `run\i7_prep.py`, `i7_tools.sh`, `i7b_tools2.sh`, `i7c_tools3.sh`, `i7d_phyml.sh`, `i7_check.py`. New private WSL envs (`env_treetools.sh`, `env_raxml1.sh`): RAxML-NG 1.2.2 and 2.0.3, PhyML 3.3.20260528 and 3.3.20220408, MrBayes 3.2.7; IQ-TREE 3.1.3 from env bio. Real Pfam ids/sequences; SYNTHETIC injections (`*`, 138-char names, colon name, cut row) are labelled in `i7_prep.py`.
```
RAxML-NG 1.2.2 / 2.0.3, protein alignment with '*': "Alignment can be successfully read by RAxML-NG."; --search1 Final LogLikelihood -2826.14  (claim: "bad alphabet" exception) -> NOT reproduced
RAxML-NG, nucleotide alignment with '*': ERROR: Invalid character in sequence 5 at position 4: *
PhyML 3.3.20260528 and 3.3.20220408, 12 names of 138 chars: tree taxon-name lengths [138] (claim: truncation at 100) -> NOT reproduced
PhyML, name 'GLB:colon(1)': ". Character ':' is not permitted in sequence name"          (claim holds)
IQ-TREE 3.1.3: -n 0 -m LG -> "Alignment has 12 sequences with 141 columns"; wrong length -> "ERROR: Line 39: Sequence MYG_HETPO/23-138 has wrong sequence length 137"; --check -> Invalid "--check" option; ':' name -> "WARNING: Some sequence names are changed"
MrBayes 3.2.7, Biopython NEXUS (molecule_type='protein', ids 'GLB2_LUMTE/31-141' quoted): Instead found ''' in command 'Matrix'
MrBayes, same file with ids sanitised (/ and - -> _): "Analysis completed" (200 generations)
```
**Scores:** Basic 28 | Specialized 40 | Total 68
**Assertions:**
- [PASS] IQ-TREE validation guidance accurate (zero-iteration check, error text, `--check` invalid, rename warning).
- [FAIL] RAxML-NG "*" -> "bad alphabet" exception reproduces - it does not (v1.2.2 and v2.0.3).
- [FAIL] PhyML silently truncates names >100 chars - it keeps 138 (two builds).
- [PASS] PhyML rejects colons in names.
- [FAIL] NEXUS written for MrBayes loads in MrBayes - quoted ids rejected; loads after sanitising.

### Input 8 - Variant B (NEW, real data): Rfam RF00005 tRNA seed, mislabelled formats, downstream builds
**Prompt:** "Read this Rfam seed, show me the consensus structure, convert it for MrBayes/PHYLIP, and make sure Infernal and HMMER can still build from what I write; the format may be wrong."
**Ran:** `run\i8_rfam_real.py`, `run\i8_infernal.sh`. Real: Rfam RF00005 (954 x 118, downloaded from rfam.org), Pfam seed.
```
AlignIO.read -> 954 x 118 ; all ids name/start-end ; annotations start/end == id suffix
snippet ss_cons length 118 == source '#=GC SS_cons' ; column_annotations keys: reference_annotation, secondary_structure
round trip: #=GF lines 40 -> 1 ; #=GC SS_cons kept
Align.read(real Rfam,'stockholm') works (954,118)   [no per-residue GR lines]
stockholm->nexus molecule_type='RNA': 954x118, datatype=rna ; strict phylip write: Repeated name 'AB031211.1'
cmbuild original: tRNA 954 seqs, clen 71 ; cmbuild AlignIO round trip: rfam_roundtrip 954 seqs, clen 71, ACC/DESC lost
hmmbuild original: Globin 73 x 141 -> LENG 117 ; round trip: pf_rt 73 x 141 -> LENG 117, ACC/DESC lost
Stockholm as clustal / phylip / nexus / fasta and clustal as Stockholm -> ValueError each (loud)
```
**Scores:** Basic 37 | Specialized 54 | Total 91
**Assertions:** all [PASS] - snippet SS_cons equals the file; GF lines dropped and GC kept; RNA NEXUS re-reads 954x118; Infernal/HMMER rebuild the same model from the round trip (metadata lost, as the Skill says); mislabelled inputs fail loudly.

## Static score (25 criteria, 8 categories)

| Category | Score | Note |
|---|---|---|
| Functional Suitability | 10/12 | Core paths and the rewritten sections correct and re-verified; two false tool claims, no MrBayes name guidance |
| Reliability | 9/12 | Common Errors exact; examples guard bad input; default-DNA mislabel, batch block lacks mkdir, cwd dependence |
| Performance/Context | 6/8 | 459 lines / ~3,200 words, single file; usage-guide now a pointer |
| Agent Usability | 14/16 | Goal/Approach, version stamp, MAF ground-truth check, IQ-TREE check; no NEXUS id-sanitising step |
| Human Usability | 7/8 | Natural prompts; table-driven format choice |
| Security | 11/12 | No credentials/eval/network; silent overwrite of converted/ |
| Maintainability | 10/12 | Version-stamped, examples verified; two unverified claims stayed; one file |
| Agent-Specific | 18/20 | Precise trigger, cross-refs exist, safe re-runs; no references layer |
| **Subtotal** | **85** | |

## Vetoes

- Skill veto: T1 PASS (18 of 19 blocks and 4 of 4 examples run), T2 PASS (frontmatter name + description), T3 PASS (repeat runs identical: codeml omega 0.28303 both audits), T4 PASS (no eval/exec of user strings, no shell).
- Research veto: M1 PASS (no fabricated data; two refuted tool claims are P1 accuracy defects), M2 PASS, M3 PASS, M4 PASS (Batch block needs one mkdir; recorded P2).

## Recommendations

- **P1** Two PHYLIP dialect-table claims are false on current builds (RAxML-NG `*`, PhyML 100 chars): delete or restate.
- **P1** MrBayes route: Biopython NEXUS ids are quoted and MrBayes 3.2.7 rejects them; add a one-line id-sanitising step.
- **P2** convert_formats.py defaults to DNA and silently mislabels protein NEXUS; validate the argument.
- **P2** Batch Processing block lacks `output_dir.mkdir(exist_ok=True)`.
- **P2** Bio.Align cells understated (A2M writer exists; PHYLIP strict-only).
- **P2** read_alignment.py depends on cwd and prints "bp" for protein.
- **P2** SKILL.md is one 459-line file; move MAF, A2M/A3M and streaming to `references/`.

## Checked and found fine (no finding)

- Dedup of `usage-guide.md`: compared against the staging copy line by line; nothing the agent needs was lost.
- Rewritten MAF helper, NEXUS write, pyhmmer snippet, A2M/A3M text and format table: correct apart from the two small Bio.Align understatements above.
- Cross-references: `msa-parsing/examples/neff.py` and all seven Related Skills exist in the worktree.
- No `__pycache__` was created in `external\`, in `F:\OpenScience\wt\al-io` or in `run\skill\`.

## What was not exercised

`iqtree2` (only IQ-TREE 3.1.3 present), PAUP*, Pfam-A.full streaming (three seed copies stand in), MAF rows from assemblies the UCSC API does not serve (22 skipped).
