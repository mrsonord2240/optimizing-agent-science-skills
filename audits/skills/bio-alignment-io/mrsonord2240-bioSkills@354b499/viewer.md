> **Audit record for `bio-alignment-io`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@354b499](https://github.com/mrsonord2240/bioSkills/tree/354b4992cd8d2f1bee039510af618da0333821f1/alignment/alignment-io) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-alignment-io

Generated: 2026-09-19
Source: `mrsonord2240/bioSkills@354b4992cd8d2f1bee039510af618da0333821f1:alignment/alignment-io` (first audit, read-only clone; nothing written under `external\`, no `__pycache__` left)
Category: Data Analysis | Mode: A (shipped examples also run from a copy) | Complexity: Complex (N=7)
Env: Windows venv Biopython 1.88 / pyhmmer 0.12.3; WSL `alignment` (MAFFT 7.526, HMMER 3.4, PAML 4.10.10, Foldmason 4.dd3c235); WSL `bio` (HH-suite reformat.pl, IQ-TREE 3.1.3)
All scripts: `run\` (Skill copy at `run\skill\`, data at `run\data\`). Every input executed: 7/7.

## Result

Skill Veto PASS (T1-T4). Static 77/100. Execution average 71.7/100. Research Veto PASS (M4 noted below).
**Final 74 - Beta Only, not deployable (score band). No open P0, no veto.**
Floors: Layer 1 avg 29.6/40, Layer 2 avg 42.1/60, assertion pass rate 20/34 (59%).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical: shipped examples, Clustal -> fasta/phylip/nexus/slice/batch | 27 | 39 | 66 | 2/5 | crashes |
| 2 | Variant A: Stockholm + annotations (real Pfam, synthetic RNA) | 31 | 45 | 76 | 3/5 | mostly good |
| 3 | Edge: PHYLIP pitfalls, real IQ-TREE load | 33 | 47 | 80 | 3/5 | good |
| 4 | Variant B: MAF strand (synthetic ground truth), A2M/A3M | 26 | 37 | 63 | 3/5 | silent wrong result |
| 5 | Stress: multi-alignment I/O, codeml, pyhmmer streaming | 30 | 42 | 72 | 3/5 | partial |
| 6 | Scope boundary: PSL/chain/GFA, format tables, Foldmason | 29 | 42 | 71 | 2/4 | tables stale |
| 7 | Adversarial: bad inputs, error table, direct conversion | 31 | 43 | 74 | 4/5 | good |

Execution Average 71.7. Static 77 x 0.4 = 30.8; Dynamic 71.7 x 0.6 = 43.0; Final 73.8 -> 74.

## Step 1 Skill Veto

T1 Stability PASS (repeat runs identical). T2 Contract PASS (frontmatter has name, description, tool_type, primary_tool, license). T3 Determinism PASS (pure file I/O; the one random element, the synthetic genome, is seeded). T4 Security PASS (no eval/exec, no network, no credentials).

Shipped-means-present: SKILL.md / usage-guide.md point at no `examples/` file; `msa-parsing/examples/neff.py` and every Related Skill exist in the clone. Nothing missing.

## Step 2 Static (25 criteria)

| Category | Score | Note |
|---|---|---|
| Functional suitability | 8/12 | core AlignIO right; MAF helper wrong; pyhmmer snippet fails; Bio.Align recommended but fails on real Stockholm; format tables stale |
| Reliability | 8/12 | error table accurate; examples crash or silently do nothing |
| Performance/context | 6/8 | ~330-line single file; niche sections always loaded; usage-guide duplicates it |
| Agent usability | 12/16 | clear Goal/Approach; AlignIO vs Bio.Align inconsistency; strand string vs int |
| Human usability | 7/8 | natural triggers; no format-detection guidance |
| Security | 11/12 | clean; unvalidated paths; silent overwrite in batch |
| Maintainability | 8/12 | 3 of 4 runnable examples cannot run from a clean copy |
| Agent-specific | 17/20 | precise trigger, good cross-refs; no references/; partly wrong escape-hatch table |
| **Subtotal** | **77/100** | |

## Detailed Outputs

### Input 1 - Canonical (executed)
**Prompt:** "Here is a Clustal alignment. Read it, tell me how many sequences and columns it has, convert it to FASTA, PHYLIP and NEXUS for MrBayes, slice out columns 50-150 of the first 5 sequences, and batch-convert a folder of .aln files."
**Code:** the four shipped scripts unchanged (`run\i1_examples_asis.py`), then again with a REAL alignment (Pfam PF00042 seed, 73 x 141, written as `alignment.aln` in the copy; `run\i1b_examples_realdata.py`), then on the shipped 4-seq DNA sample (`run\i1c_sample_dna.py`), then the molecule_type workaround (`run\i1d_nexus_workaround.py`).
**Output (trimmed):**
```
read_alignment.py  exit=0  Alignment length: 21 columns / Number of sequences: 4 / seq1: 21 bp ...
convert_formats.py exit=1  FileNotFoundError: 'alignment.aln'         (not shipped)
slice_alignment.py exit=1  FileNotFoundError: 'alignment.aln'
batch_convert.py   exit=0  "Converted all files to fasta format"      (0 files converted; alignments/ absent)
-- with real Pfam alignment.aln --
convert_formats.py: Wrote output.fasta, output.phy, then ValueError: Need the molecule type to be defined
PASS output.fasta re-read 73x141 ids+seqs identical      PASS output.phy re-read 73x141 identical
FAIL output.nex re-read: No records found in handle      (file is 0 bytes)
PASS trimmed_subset.fasta 5x91 (alignment has 141 cols; slice hard-codes 50:150)
-- shipped 21-col sample --
slice_alignment.py exit=0  "Columns 50-150: 0 columns"  -> writes 4 empty records to trimmed_subset.fasta
-- workaround --
PASS AlignIO.convert(..., molecule_type="DNA") clustal->nexus re-read 4x21
PASS record.annotations['molecule_type']='protein' before write -> 73x141 nexus
```
**Scores:** Basic 27/40 | Specialized 39/60 | Total 66/100
**Assertions:**
- [PASS] read_alignment.py prints 4 x 21 on the shipped sample
- [FAIL] convert_formats.py completes and every output re-reads - NEXUS write raises ValueError, 0-byte file
- [PASS] FASTA and PHYLIP-relaxed conversions of real Pfam re-read identical
- [FAIL] slice and batch run from a fresh copy without extra files - alignment.aln / alignments/ not shipped, batch no-ops with exit 0
- [FAIL] Slicing beyond the alignment is refused or warned - silently writes 0-column FASTA

### Input 2 - Variant A: Stockholm with annotations (executed)
**Prompt:** "Load this Pfam Stockholm file, show me the secondary-structure and consensus annotations, tell me what survives conversion to FASTA, and use the modern Bio.Align API."
**Code:** `run\i2_stockholm.py`. Data: real `PF00042_seed.sto`; SYNTHETIC `run\data\synthetic_rna.sto` (2 sequences with GS, GR SS, GC SS_cons, GC RF).
**Output (trimmed):**
```
PASS AlignIO.read stockholm -> 73x141 ; first id GLB2_LUMTE/31-141 ; record.annotations keys ['accession','end','start']
FAIL Align.read(real Pfam, stockholm): TypeError: Any per-letter annotation should be a Python sequence ... 
FAIL Align.parse(real Pfam, stockholm): same TypeError
PASS letter_annotations['secondary_structure'] and column_annotations['secondary_structure'] = '<<<<___.>>>>.....' (RF under 'reference_annotation')
PASS Stockholm round trip keeps '#=GC SS_cons' and '#=GR seqA/1-16 SS'; FASTA drops them
PASS stockholm->nexus with molecule_type='RNA' / 'protein' re-reads ; FAIL without molecule_type (ValueError)
PASS SKILL says Biopython does not split name/start-end; it DOES: annotations start/end = 31/141 (id keeps suffix)
PASS real Pfam '#=GF ID/AC/DE' lines are NOT written back by AlignIO (dropped silently)
```
(Lines marked PASS in the script that describe a defect are assertions that the defect exists; the verdict per claim is in the list below.)
**Scores:** Basic 31/40 | Specialized 45/60 | Total 76/100
**Assertions:**
- [PASS] AlignIO.read real Pfam -> 73 x 141
- [PASS] Annotation snippet keys return the SS strings
- [PASS] Stockholm keeps GC/GR on round trip, FASTA discards them
- [FAIL] Recommended Bio.Align.read/parse works on real Pfam Stockholm
- [FAIL] "Biopython does not split name/start-end" is accurate

### Input 3 - Edge: PHYLIP pitfalls (executed)
**Prompt:** "I need PHYLIP for IQ-TREE and PAML. My names are Homo_sapiens_chr1, Homo_sapiens_chr2, Mus_musculus_chr1 and some contain colons. Which format string, and will anything get corrupted?"
**Code:** `run\i3_phylip_edge.py` (SYNTHETIC 3-seq alignment), `run\i7_iqtree_check.sh` (REAL Pfam written as phylip-relaxed into IQ-TREE 3.1.3).
**Output (trimmed):**
```
strict 'phylip' write, colliding prefixes -> ValueError: Repeated name 'Homo_sapie' (originally 'Homo_sapiens_chr2'), possibly due to truncation
strict write, unique prefixes -> 'Homo_sapie','Mus_muscul','Bos_taurus' (truncated, as SKILL says)
phylip-relaxed round trip exact ; phylip-sequential write with long names -> same ValueError
READING a foreign strict file with identical first 10 chars -> ids ['Homo_sapie','Homo_sapie'] accepted silently
interleaved text read with phylip-sequential -> ValueError: Found a record of length 145, should be 120 (loud)
sanitised ids ['a_1','b_2_','c_3'] survive ; unsanitised 'x:y' is written by the writer as 'x|y'
IQ-TREE 3.1.3: "Input data: 73 sequences with 141 amino-acid sites" (phylip-relaxed, real ids with '/')
iqtree3 -s file.phy --check  -> Invalid "--check" option.
```
**Scores:** Basic 33/40 | Specialized 47/60 | Total 80/100
**Assertions:**
- [PASS] phylip-relaxed round-trips long ids exactly
- [PASS] strict phylip truncates to 10 characters
- [FAIL] Strict write "silently merges" colliding prefixes - it raises ValueError; silence is on reading foreign files
- [PASS] Real Pfam phylip-relaxed loads in IQ-TREE
- [FAIL] `iqtree2 -s file.phy --check` is a valid validate-only command

### Input 4 - Variant B: MAF strand and A2M/A3M (executed)
**Prompt:** "Convert this UCSC MAF block's minus-strand rows to plus-strand genome coordinates, and load the HMMER A2M alignment and my ColabFold A3M as normal MSAs."
**Code:** `run\i4_maf.py` (SYNTHETIC seeded 200-nt genome + hand-built MAF; ground truth: plus-strand start 60 for the minus-strand row, checked against the genome by reverse complement), `run\i4b_hmmalign.sh` + `i4b_a2m.py` (REAL hmmalign output, 8 UniProt globins vs an HMM built from the Pfam seed, LENG 117), `run\i6b_a3m.sh` + `i6b_a3m.py` (REAL Pfam -> A3M -> A2M with HH-suite reformat.pl). The SKILL function was run verbatim:
```python
def maf_to_plus_strand_coords(row_anno):
    if row_anno['strand'] == '-':
        return row_anno['srcSize'] - row_anno['start'] - row_anno['size']
    return row_anno['start']
```
**Output (trimmed):**
```
1 mm.chr2 {'start': 66, 'size': 24, 'strand': -1, 'srcSize': 150}          <- strand is int -1
0 hg.chr1 skill fn -> 20  genome fragment == row text: True (plus strand rows fine)
1 mm.chr2 skill fn -> 66  genome fragment (revcomp) == row text: False
FAIL SKILL function on minus-strand row returned 66; ground truth 60
PASS corrected function (strand in ('-', -1)) returns 60
PASS Bio.Align maf: 2 blocks parsed, s-lines written
hmmalign A2M row lengths [149,150,151,160,161], no '.' -> AlignIO.read(...,'fasta'): ValueError Sequences must all be the same length
PASS match-state filter (upper or '-') on raw rows -> 117 = HMM LENG
reformat.pl a3m: 14 distinct row lengths (ragged); a2m: 73 x 141 rectangular, 1749 '.' pads
PASS SKILL match-only snippet -> all 73 rows 111 columns = first-sequence residues
```
**Scores:** Basic 26/40 | Specialized 37/60 | Total 63/100
**Assertions:**
- [PASS] AlignIO maf exposes start, size, strand, srcSize
- [FAIL] SKILL helper returns the true plus-strand start for a minus-strand row (66 vs 60)
- [PASS] Bio.Align maf parse/write works
- [FAIL] Real hmmalign A2M loads with AlignIO 'fasta'
- [PASS] reformat.pl a3m -> a2m is rectangular and the match-only snippet recovers 111 match columns

### Input 5 - Stress: multi-alignment I/O, PAML route, pyhmmer streaming (executed)
**Prompt:** "Stream every family from this multi-family Stockholm file and print size and weights; write all alignments to PHYLIP; then convert my 6-species HBB CDS alignment for codeml and run it."
**Code:** `run\i5b_multi_io.py`, `run\i5_pyhmmer_stream.py`, `run\i5c_prep.py`, `run\i5c_align.sh` (MAFFT), `run\i5c_paml_io.py`, `run\i5c_run_codeml.sh`. Data: `Pfam-mini.sto` = REAL PF00042 seed concatenated 3x with distinct IDs; REAL RefSeq HBB CDS x 6.
**Output (trimmed):**
```
PASS AlignIO.parse -> 3 alignments of 73x141 ; write(3) ; re-parse 3 ; phylip-relaxed multi round trip 3 ; clustal via handle identical
verbatim SKILL pyhmmer snippet -> AttributeError: 'pyhmmer.easel.DigitalMSA' object has no attribute 'nseq'
  (dir(msa) has no nseq/alen; msa.name is str; len(msa.sequences)=73 ; compute_weights(method='pb') exists, weights sum 73.0)
phylip-sequential with real NCBI headers -> ValueError: Repeated name 'lcl|NM_001' ...
ids shortened (human, chimp, cow, pig, macaque, horse): phylip-sequential -> codeml M0: omega 0.28303, lnL -1251.532237
phylip-relaxed (interleaved, single-space names) -> codeml: "Error in sequence data file ... separate the sequence from its name by 2 or more spaces"
```
**Scores:** Basic 30/40 | Specialized 42/60 | Total 72/100
**Assertions:**
- [PASS] Multi-alignment parse/write round trips 3 alignments
- [FAIL] Verbatim pyhmmer streaming snippet runs (nseq, alen, name.decode())
- [PASS] codeml accepts phylip-sequential (omega 0.28303)
- [PASS] codeml rejects phylip-relaxed, as the SKILL states
- [FAIL] A user with NCBI headers can follow the SKILL to phylip-sequential for PAML (no advice to shorten ids)

### Input 6 - Scope boundary: formats outside the Skill, tables, Foldmason (executed)
**Prompt:** "Load this PSL and chain file as alignments, read the HAL/GFA pangenome, and give me a pyhmmer A3M reader; also load the Foldmason MSA from these three structures."
**Code:** `run\i6_scope_formats.py` (SYNTHETIC one-line PSL, chain, padded A2M), `run\i6c_foldmason.sh` + `i6c_foldmason_read.py` (REAL 1MBN, 1A6M, 1EMY; Foldmason easy-msa).
**Output (trimmed):**
```
Bio.Align.formats = (a2m, bed, bigbed, bigmaf, bigpsl, chain, clustal, emboss, exonerate, fasta, hhr, maf, mauve, msf, nexus, phylip, psl, sam, stockholm, tabular)
PASS Align.parse(psl)   coordinates [[100,130],[5,35]]   (SKILL: PSL "NOT in BioPython")
PASS Align.parse(chain) works                            (SKILL: chain/net "NOT in BioPython")
padded A2M via Align.read: shape (2,7) ; hmmalign (ragged) A2M: AssertionError
gfa/hal/axt/gaf/rgfa in Bio.Align.formats: False x5      (SKILL correct)
pyhmmer format='a3m' -> InvalidParameter: expected 'stockholm','pfam','a2m','psiblast','selex','afa','clustal','clustallike','phylip' or 'phylips'
Foldmason result_aa.fa / result_3di.fa: 3 x 153 each ; AlignIO.read ok ; 1A6M vs 1MBN identity 1.0
```
**Scores:** Basic 29/40 | Specialized 42/60 | Total 71/100
**Assertions:**
- [FAIL] "Formats NOT in BioPython" is accurate for PSL and chain
- [PASS] GFA/HAL/AXT/GAF are correctly out of scope
- [PASS] Foldmason aa/3Di MSAs load with AlignIO
- [FAIL] pyhmmer supports A3M read/write as the table says

### Input 7 - Adversarial / ambiguous (executed)
**Prompt:** "Convert this alignment. (Empty file / unaligned FASTA / wrong format string / Stockholm with several alignments given to read().)" plus "convert my Clustal to PHYLIP" on the real 73-sequence file.
**Code:** error section of `run\i5b_multi_io.py`, `run\i7b_direct_convert.py`, `run\i7_iqtree_check.sh`.
**Output (trimmed):**
```
empty file      : ValueError: No records found in handle
read() on multi : ValueError: More than one record found in handle
ragged fasta    : ValueError: Sequences must all be the same length      (SYNTHETIC 2-record file)
unknown format  : ValueError: Unknown format 'a2m'
wrong format    : ValueError: # is not a known CLUSTAL header ...
nonexistent     : FileNotFoundError
Direct Conversion (strict phylip) on real Pfam: 73 unique ids after truncation, 0 prefix collisions
```
**Scores:** Basic 31/40 | Specialized 43/60 | Total 74/100
**Assertions:**
- [PASS] Common Errors table reproduces in Biopython 1.88
- [PASS] Unaligned FASTA gives a clear error, not silent output
- [PASS] Direct strict-phylip conversion works on the real alignment
- [FAIL] Suggested validate-only command works (`--check` invalid)
- [PASS] Output stays in file-format scope

## Research Veto (Data Analysis)

- M1 Scientific integrity: PASS. No invented identifiers or statistics.
- M2 Practice boundaries: PASS. Nothing clinical.
- M3 Methodological baseline: PASS. The MAF helper is an implementation defect, recorded P1.
- M4 Code usability: PASS with a caveat. Core snippets and the codeml route ran and were asserted. The pyhmmer streaming snippet (AttributeError) and `convert_formats.py` (ValueError at NEXUS) fail as written but are one-line adaptations under the Skill's own "introspect and adapt" note. A stricter reader could call this an M4 FAIL; the orchestrator should look at Inputs 1 and 5 before promotion.

## Final

Static 77 x 0.4 = 30.8; Dynamic 71.7 x 0.6 = 43.0; **Final 74, Beta Only.** Assertion pass rate 20/34 (59%), below the 80% Limited-Release floor; Execution average 71.7 below the 75 floor.

Key strengths:
- Core AlignIO read/write/convert/slice/parse-multiple patterns work and round-trip real Pfam data exactly.
- PHYLIP advice verified end to end with real IQ-TREE 3.1.3 and real codeml (omega 0.28303).
- Common Errors table reproduces exactly; A3M/reformat.pl guidance correct on real output.
- Covers hazards other Skills omit: annotation loss, MAF strand, A3M reference sequence, Pfam id convention.

## Recommendations

[P1] maf_to_plus_strand_coords is silently wrong for minus strand (Input 4)
  Problem: Biopython's strand is int -1; `== '-'` never matches; 66 returned, truth 60.
  Fix: test `in ('-', -1)`; state the int type; add the revcomp ground-truth check.

[P1] Shipped examples do not run from a clean copy; canonical convert crashes (Input 1)
  Problem: convert_formats.py ValueError at NEXUS (0-byte file left); alignment.aln / alignments/ not shipped; batch_convert exits 0 having done nothing; slice_alignment writes 0-column FASTA.
  Fix: use the shipped sample; set molecule_type before NEXUS; fail loudly on no matches; guard slice bounds.

[P1] pyhmmer snippet and A3M/A2M claims wrong for pyhmmer 0.12.3 / HMMER (Inputs 4, 5, 6)
  Problem: nseq/alen absent, name is str, no 'a3m' format, hmmalign A2M is ragged.
  Fix: `len(msa.sequences)`, `len(msa.alignment[0])`, `msa.name`; drop A3M from pyhmmer; document match-state extraction; pin the pyhmmer version tested.

[P1] Bio.Align recommended but fails on real Stockholm; format tables stale (Inputs 2, 6)
  Problem: Align.read/parse stockholm TypeError on Pfam; Align.write stockholm AttributeError; PSL/chain/A2M/MSF exist in Bio.Align 1.88 but tables say otherwise.
  Fix: recommend AlignIO for Stockholm; correct the tables; add the failure to Common Errors.

[P2] PHYLIP guidance overstated (Inputs 3, 5): strict write raises, not silent; ':' becomes '|'; shorten ids before phylip-sequential; `--check` is not an IQ-TREE option.
[P2] Pfam id / GF statements inaccurate (Input 2): annotations start/end already filled; #=GF headers dropped by AlignIO.
[P2] usage-guide.md duplicates SKILL.md; no references/ layer.
