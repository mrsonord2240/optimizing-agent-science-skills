# Fix log: bio-alignment-io (alignment/alignment-io), 2026-09-19

Branch `fix/al-io` (worktree `F:\OpenScience\wt\al-io`), commit `0f10851`, from staging main `354b499`.
First audit: 74, Beta Only (score band), no veto, no P0. Checked on Biopython 1.88, pyhmmer 0.12.3, HMMER 3.4,
HH-suite `reformat.pl`/`hhfilter` (WSL `bio`), IQ-TREE 3.1.3. Verification script: `F:\OpenScience\scratch-al-io\verify.py`
(47 assertions, 0 failures; it extracts the code blocks from the edited SKILL.md and executes them, and runs the four examples
from a clean copy).

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| MAF helper wrong for minus strand (66 vs 60) | P1 | Test `strand == -1`, state that strand is an int, add revcomp ground-truth loop | ran the SKILL block on the audit's synthetic MAF + genome: minus row -> 60; loop passes for every row; negative control with the old `== '-'` test raises AssertionError | |
| convert_formats.py ValueError at NEXUS write, 0-byte file | P1 | Set `record.annotations['molecule_type']` (2nd argv, default DNA); SKILL section "NEXUS Output Needs a Molecule Type" | clean copy: output.fasta/.phy/.nex re-read 4x21 with identical ids and sequences; real Pfam clustal + `protein` -> nexus re-reads 73 | |
| slice_alignment.py / convert_formats.py need unshipped `alignment.aln`; slice writes 0-column FASTA | P1 | Default input is shipped `sample_alignment.aln` (or argv); slice bounds 5:15, exits non-zero when out of range; SKILL notes silent 0-column slices | clean copy: 4x10 output equals source columns 5:15; 10-col input exits non-zero; real Pfam gives 5x10 | |
| batch_convert.py exits 0 having converted nothing | P1 | Default dir = examples dir, `sys.exit` when no `*.aln` | clean copy: 1 file converted; empty dir exits 1 with message | |
| pyhmmer streaming snippet AttributeError | P1 | `len(msa.sequences)`, `len(msa.alignment[0])`, `msa.name` (str); pyhmmer version stamped | ran snippet on a 3-family Stockholm: `Globin_copyN 73 141 sum_w=73.0` x3 | |
| A2M/A3M claims (pyhmmer `a3m`; "A2M loads rectangular") | P1 | Table: A3M unsupported by all three; hmmalign A2M documented as ragged; match-column snippet now `SeqIO.parse` | real hmmalign A2M: `AlignIO.read` raises, snippet gives 8 rows x 117 (= HMM LENG); reformat.pl-padded A2M: `AlignIO` 73x141, `Align.read(...,'a2m')` 73x141, snippet 111 match cols; `format='a3m'` -> InvalidParameter | |
| `hhfilter -id 100 ...` offered as fix for non-query first A3M record | P1 (found while verifying) | Replaced by "move the query record first" | ran `hhfilter` on a reordered A3M: output order unchanged. Ran `reformat.pl a3m a2m` on original vs reordered A3M: the rows differ, so the first-record pitfall is real | Not in the audit; found by testing the claim I was editing |
| Bio.Align recommended but fails on real Stockholm; format tables stale | P1 | Recommend AlignIO for Stockholm/NEXUS; table rewritten (MSF R, A2M R, PSL/chain/BED/SAM as Bio.Align pairwise formats, removed from "NOT in BioPython"); Common Errors gains TypeError / AttributeError / molecule-type rows; error strings now the real ones | `Align.read/parse` real Pfam -> TypeError; `Align.write(stockholm)` -> AttributeError; `Bio.Align.formats` and per-module reader/writer listing; `Align.read` clustal + `.counts()`; `Align.parse` MAF 2 blocks; `Align.read` padded A2M | Bio.Align also raises AssertionError on the synthetic RNA Stockholm (GR names); not written up, covered by "plain files only" |
| PHYLIP guidance overstated | P2 | Strict write raises on collisions (silent only when reading foreign files); `phylip-sequential` truncates and raises on collision; shorten ids first; writer turns `:` into `\|`; codeml message quoted; `--check` -> `iqtree3 -s f.phy -n 0 -m LG -redo -pre check` | asserted in Biopython 1.88; IQ-TREE 3.1.3 on real Pfam: "Alignment has 73 sequences with 141 columns"; wrong-length file: `ERROR: Line 3: Sequence z_1 has wrong sequence length 7`; IQ-TREE accepts `:` names with a rename WARNING (row rewritten from "not a valid PHYLIP file") | codeml message comes from the audit's run (i5c), not rerun |
| Pfam id / GF statements inaccurate | P2 | Pfam id paragraph: start/end/accession already filled; `#=GF` lines dropped; IQ-TREE accepts `/` | real PF00042: annotations `{'accession','start':31,'end':141}`, id keeps suffix; round trip lacks `#=GF ID/AC/DE` | |
| Direct-conversion example used strict `phylip` against the Skill's own "prefer relaxed" | P2 | `phylip-relaxed` | ran the corresponding example path (convert_formats output.phy) | |
| usage-guide.md duplicates SKILL.md | P2 | See "Deleted passages" | file read | |

## Deleted passages and where the content lives

| deleted | now |
| --- | --- |
| usage-guide.md "Prerequisites" (pip install) | SKILL.md "Version Compatibility" |
| usage-guide.md "Format Selection for Downstream Tools" table | SKILL.md "Format Selection for Downstream Tools" (guide points to it) |
| usage-guide.md "Tips" (7 bullets) | SKILL.md "Format-Specific Notes" > PHYLIP, "Annotation Preservation", "Round-trip caveat". Dropped: "parse() is more memory efficient than read()" (both stream the same file; unsupported) and "PHYLIP layout mismatch fails silently" (audit showed it raises) |
| SKILL.md "Get Alignment Properties" + "Slice Alignments" | Merged into "Accessing Alignment Data" (one slice block; `seq_ids` line kept) |
| SKILL.md "Clustal Format" snippet | Clustal marks not parsed is in the Format Coverage Map and Annotation Preservation table |
| SKILL.md Round-trip caveat sentence "write fasta discards every Stockholm annotation" | Annotation Preservation paragraph |
| SKILL.md `Bio.Align` "Recommend over AlignIO" sentence | Format Coverage Map closing paragraph + "When to Use Which" |
| SKILL.md `AlignIO.parse(..., stockholm)` example inside the Bio.Align section | Replaced by a MAF `Align.parse` example (Stockholm fails) |
| SKILL.md `hhfilter` renormalise option (b) | Wrong; replaced by "move the query first" |

## Left unfixed

- RAxML-NG `*` and PhyML 100-character claims in the PHYLIP dialect table: RAxML-NG and PhyML are not installed here, could not be verified. Left as is.
- `#=GS` details in the Stockholm table and the WUSS paragraph: not contradicted by any audit run.
- No `references/` layer (audit P2 note): splitting the file is restructuring beyond the dedup rule; SKILL.md grew 446 -> 459 lines (corrections and new checks outweigh the deletions); usage-guide.md shrank 78 -> 54.
- `read_alignment.py` unchanged (ran clean; still needs cwd = examples dir, prints "bp" for protein).

# Round 2 (2026-09-20)

Branch `fix/al-io2` (worktree `F:\OpenScience\wt\al-io2`), commit `00ddbb3`, from staging main `818f049`. Re-audit of round 1: 85, Limited Release,
deployable, 32/39 assertions. Checked on Biopython 1.88, RAxML-NG 1.2.2 and 2.0.3, PhyML 3.3.20220408 and 3.3.20260528, MrBayes 3.2.7, IQ-TREE 3.1.3
(the re-auditor's WSL envs `aln-raxml1`, `aln-treetools`, `aln-phyml-old`, used read-only; scratch in `F:\OpenScience\scratch-al-io2`).
All changed `.py` py_compile; all four examples re-run from a clean copy.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| convert_formats.py defaults DNA, protein NEXUS says `datatype=dna`; lower-case arg gives misleading error (fix-introduced) | P2 (silent-wrong) | Infers DNA/RNA/protein (>=90% ACGTUN = nucleotide, U without T = RNA), optional argv override normalized case-insensitively, unknown value or override contradicting the residues exits 1, asserts `datatype=` in output.nex; SKILL states the value is written unchecked | ran: shipped DNA -> dna; RNA -> rna; real Pfam via Clustal -> protein, fasta/phy/nex re-read 73x141 with identical ids and rows; `DNA` on protein, `protein` on DNA, `foo` -> exit 1 with message; `Protein` accepted | |
| RAxML-NG `*` row false | P1 | Row restated: DNA gives `Invalid character in sequence N at position P: *`; protein accepts `*` (undetermined, not scored) | ran 1.2.2 and 2.0.3: protein `--search1` finishes (lnL -2811.05); DNA `--check` error text as quoted | |
| PhyML 100-character row false | P1 | Row replaced with the real rejection (`:` and `,` not permitted; `(` `)` accepted and written into the Newick), plus RAxML-NG rejection of `:` `,` `(`; prose no longer says PhyML rejects parentheses | ran both PhyML builds: 138-char names kept in tree; `:` and `,` fail with the quoted message; `(` exits 0; RAxML-NG `--check` fails for all three | prior prose "PhyML rejects colons or parentheses" was half wrong |
| MrBayes rejects Biopython's quoted NEXUS ids | P1 | Recipe (`re.sub(r'[^A-Za-z0-9_]', '_', ...)` plus uniqueness assert) in "NEXUS Output Needs a Molecule Type"; MrBayes row of downstream table says quote-free ids | SKILL block extracted and exec'd on real Pfam: MrBayes 3.2.7 on Biopython's quoted file -> `Instead found ''' in command 'Matrix'`; on the recipe's output -> 12 taxa x 141 chars, `mcmc` completes. Biopython quoting tested on 20 punctuation characters: quotes `- + : ; , ( ) [ ] ' " =`, `*` and space; not `/ . \| _ # @ % & !` | |
| Batch Processing block lacked `mkdir` | P2 | Added `output_dir.mkdir(exist_ok=True)` | block extracted from SKILL.md and exec'd: `converted/a.fasta` re-reads 12 rows | |
| Bio.Align cells understated | P2 | PHYLIP cell: strict 10-char only; A2M: R and W (writer needs `column_annotations['state']`); PSL row adds exonerate/bigMaf/bigPsl/bigBed; new HHR/tabular row (R only) | `Bio.Align.formats` and reader/writer presence per module; A2M read/write/re-read 73x141 identical; phylip write truncates ids to 10, read of relaxed file raises `Expected all sequences to have length 121; found 128` | |
| read_alignment.py cwd-dependent, "bp" label | P2 | `Path(__file__).parent`, label "columns" (length includes gaps) | ran from another cwd: 4 sequences, 21 columns | |
| New sentence "RAxML-NG and IQ-TREE accept names of 138 characters" | - | Version line lists downstream tool versions | ran RAxML-NG `--check` and IQ-TREE 3.1.3 on 138-char names: `Alignment has 12 sequences with 121 columns` | |

Redundancy: nothing added twice; the MrBayes and datatype notes live once in the NEXUS section, tables point to it. No passages deleted.

## Left unfixed

- SKILL.md is one file (459 -> 472 lines) with no `references/` layer (re-audit P2): moving MAF, A2M/A3M and Pfam streaming out is restructuring beyond the dedup rule.
- Round-1 "left unfixed" RAxML-NG `*` and PhyML 100-character claims are now resolved (above).
