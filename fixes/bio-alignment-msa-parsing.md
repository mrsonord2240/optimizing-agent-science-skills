# Fix log: bio-alignment-msa-parsing (2026-09-20)

Skill `alignment/msa-parsing`, branch `fix/al-msaparse` (worktree `F:\OpenScience\wt\al-msaparse`), commit `53861ae` on staging main `354b499`.
First audit: 78, Beta Only, not deployable (24/35 assertions), no veto/P0. Fixer only; no scoring.
Tools checked 2026-09-19/20: Python 3.12.13, Biopython 1.88, numpy 2.0.2, pyhmmer 0.12.3 (Windows venv); MUSCLE 5.3, HMMER 3.4 (WSL `alignment`).
Verification: SKILL.md python blocks were extracted and executed **without** `examples/` on the path (23 of 25 blocks run; the other two are the `mi_matrix_apc` skeleton and a `column_5` illustration on a 5-column test file); every example was then run from a clean copy of the Skill, with defaults and on the real Pfam PF00042 seed. All `.py` files `py_compile`.

| finding | priority | change | verified (ran) | notes |
| --- | --- | --- | --- | --- |
| Gap symbol hard-coded to `-`; `.` and lowercase break helpers silently | P1 | New "Gap and Case Normalisation" section: `select_columns` + `normalize_alignment` (`.`->`-`, upper-case; `upper=False` for A2M). Every helper normalises internally; `coordinate_map` treats `.` as a gap. Same code in `examples/msa_utils.py`; examples load via `load_alignment` (Stockholm guessed from extension) | Hand-computed 4x5 protein with `.` and lowercase: gaps/column `[0,0,1,4,0]`, gaps/seq `[1,1,2,1]`, conserved 1.0 = cols 0,1, consensus `ACD-F`/`ACX-F`/`ACX-X`, `coordinate_map` `[0,1,4]`/`[0,1,-1,-1,2]`. Soft-masked 4x8 DNA: consensus `ACGTACGT`, 8/8 conserved (was `ACGTNNNN`, 0). Pfam seed (`.` gaps): gap total 1943 = independent numpy count, fully conserved cols 17 F / 77 H, consensus identical to independent pandas consensus | |
| `mi_apc.py` ignores APC guard; noise on the seed; thresholds disagree (0.5 vs 1) | P1 | `mi_matrix_apc` computes Neff and, unless L>100 and Neff/L>1 (or `force=True`), warns and returns raw MI; `main` prints the warning, a best-of-5 column-shuffled null, and flags pairs at or below it. Single rule Neff/L > 1 (`MIN_NEFF_PER_L` in `neff.py`, used by both scripts and SKILL.md); the 0.5 statement is deleted | Pfam seed: warning "L=141, Neff/L=0.47", top raw-MI pair 2.627 <= null 2.671, 0 of top 20 above null. Planted coupling (300x120, cols 10 and 60): guard passes with no warning, pair (10,60) ranked first, 1.958 > null 0.195. MI by hand: `[A,A,B,B]` vs `[C,C,D,D]` = 1 bit, vs `[C,D,C,D]` = 0, 3:1 split = 0.8113 bit (all exact) | Why 1 and not 0.5: it is the SKILL's own APC rule, and the audit run showed the seed at 0.47 gives noise. Literature cut-offs are estimator-specific; SKILL.md says so |
| Protein consensus default `N` is asparagine | P1 | `consensus_sequence(ambiguous=None)`: `N` for nucleotide (`is_nucleotide`, >= 90% ACGTUN), `X` for protein; docstring/prose state that the denominator includes gap rows | Seed at 0.5: 124 `X`, 0 `N` (audit: 124 `N` of which 2 real Asn columns); consensus equals independent pandas result | `gap_char` argument kept; `weights=` added (see below) |
| Henikoff/Neff prose wrong or contradictory; NaN on all-gap alignment | P1 | Henikoff edge-case paragraph and example docstring rewritten from pyhmmer's docstring and the runs (Easel pb ignores gaps column by column, consensus columns only, double-normalised, sums to N; ranks agree with `henikoff_weights`, values do not). `henikoff_weights` raises `ValueError` when no column is gap-free. Neff table replaced by three measured rows; ratio column and AF2/EVcouplings/HHsuite rows removed; runnable pyhmmer snippet added; "Effective sequences" label in `henikoff_weights.py` renamed Kish ESS | Hand Henikoff weights on the 4x5 file `[2/9,2/9,1/3,2/9]` exact; all-gap synthetic raises; pyhmmer pb sum 73.0 (ran); Neff 66.08 / 73.00 (0.62 / 0.80) reproduced; `hmmbuild` 3.4 rerun: eff_nseq 6.35 (73 seqs); `hmmbuild -h`: `--wid` default 0.62. Spearman 0.909 / max diff 0.0091 are the audit's measurements (I reproduced the Easel/skill weight difference of 0.0091 too) | I tried to write an Easel-equivalent `pb` (consensus-column, gap-ignoring, double-normalised) in numpy; it did not match Easel's numbers (max diff ~0.95 in sum-to-N units), so the Skill sends gappy alignments to pyhmmer rather than shipping an approximation |
| Cleaning drops annotations; filter can return empty alignment silently | P2 | `select_columns` copies record annotations, letter/column annotations; `remove_gappy_columns`, `extract_ungapped_regions` use it; `filter_by_id`, `filter_by_gap_content`, `remove_duplicates` go through `_require_kept` -> `ValueError` naming the threshold and lowest gap fraction | Stockholm `syn_annot.sto` after `remove_gappy_columns(0.5)`: SS letter annotation `HHEEEC`, column annotations `xx.xxx`/`HHEEEC` (col 2 removed by hand), written Stockholm still holds GC RF, GC SS_cons, GR SS, GS OS. `filter_by_gap_content(0.0)` and `filter_by_id('^zzz')` raise | |
| GUIDANCE2 recommended twice but not installable | P2 | **Wrote it with an installed tool**: MUSCLE 5.3 ensemble (`-stratified`, `-maxcc`, `-addconfseq`) plus new `examples/muscle5_column_confidence.py` (parse `_conf_` digit rows, list survivors per cut-off, mask). GUIDANCE2, TCS and the 0.93 cut-off deleted from the trimming matrix and Unreliable-regions step 3 | Chose write over delete because MUSCLE 5.3 is installed and the audit had verified the flags. Ran the exact commands on 8 UniProt globins (155 columns: 11 with CC < 0.9) and 73 Pfam sequences (162 columns, 60 at CC >= 0.9); independent replicate-agreement count (fraction of the 16 replicates containing the identical column) is a subset of the low-CC set in both runs (89 of 102 on Pfam; correlation 0.77) | The CC definition is MUSCLE's own; I only claim that its low-confidence set contains every column the agreement count flags. No calibrated cut-off, said so in the Skill |
| pyhmmer minimum version; `SummaryInfo` said "deprecated" | P2 | Version block: pyhmmer >= 0.11.3, checked versions, install line; SummaryInfo: only `get_column` remains in 1.88, others raise `AttributeError` | pyhmmer `compute_weights` docstring `versionadded:: 0.11.3`, installed 0.12.3; audit's Biopython 1.88 finding | |
| Duplicated code drifted; weighting advice not actionable; contradictory SIC/fifth-state sentence; unsourced AF2 ratios | P2 | `find_conserved_positions` unified (drop gaps, denominator all rows, 3-tuples); `weights=` on `find_conserved_positions` and `consensus_sequence`; sentence now "prefer SIC indel coding (fifth-state only as a sensitivity check)"; AF2 row deleted | SKILL.md functions vs example functions give identical output on the Pfam seed (`find_conserved` 0.5, `consensus` 0.3, `henikoff`); weighted consensus by hand (`weights=[1,1,0,0]` -> `ACD-F`) | Inline code kept beside `examples/` per the brief |
| Examples need unshipped input files; 0/1-based ambiguity | P2 | `examples/data/example_alignment.fasta` (6x20 protein) and `example.a2m`; every example takes an alignment path as argv[1]; `seq_to_aln[42]` renamed `column_of_residue_index_42` with 0-based comment; PDB-offset sentence added; `a2m_a3m_io.py` docstring states `.` vs `-` | All 9 original examples run with no arguments (rc 0); a2m example on the audit's real `hhsearch_output.a2m` and the shipped one gives hand-known match-only counts (9 columns, inserts 0/2/1); `1MBN` PDB residue 93 is HIS and UniProt P02185 index 93 (0-based) is H, index 92 is S | |
| Redundancy (brief: every pass) | - | See "Deleted passages" | | |

## Deleted passages and where the content lives

| deleted | now |
| --- | --- |
| usage-guide `Prerequisites` (pip install) | SKILL.md Version Compatibility ("Install") |
| usage-guide `What the Agent Will Do` | dropped (procedure restated the SKILL.md sections) |
| usage-guide `Key Concepts` table (Column, Conservation, Consensus, Gap = '-') | SKILL.md intro: conservation definition and 0-based convention; Gap and Case Normalisation (the "Gap = '-'" row was wrong for `.` input) |
| usage-guide `Working with Annotations` (code + Stockholm-survives paragraph); SKILL.md pointed to it | SKILL.md `Working with Annotations` (moved in full, plus a line on which helpers keep annotations) |
| usage-guide `Tips`: >50% gaps, guide-tree gaps, ClipKIT kpic-smart-gap, GUIDANCE2/MUSCLE5, gap handling downstream, Stockholm keeps annotations | already in SKILL.md (Identifying Unreliable Alignment Regions, Alignment Trimming, Gap Handling, Annotations) |
| usage-guide `Tips`: ">20-30% trimming hurts trees" | SKILL.md Alignment Trimming |
| usage-guide `Tips`: conservation depends on diversity; 0-based numbering | SKILL.md intro conventions |
| SKILL.md `Quick Reference` table | Loading comment (`alignment[i]`), Column-wise Analysis, Gap Analysis, Consensus already covered each row |
| SKILL.md Neff estimator table ratio column and AF2/EVcouplings/HHsuite rows; Hopf/Marks "calibrated against a specific estimator" specifics; "0.62 traces to BLOSUM62, 0.80 is HHsuite's cd-hit default for BFD"; "Neff/L > 0.5 for DCA" (also in `neff.py`) | Measured three-row table and single Neff/L > 1 rule in SKILL.md Neff section; references Marks 2011 and Jumper 2021 dropped (no longer cited) |
| SKILL.md GUIDANCE2/TCS mentions (matrix row, step 3) | MUSCLE5 route in step 3 and matrix row |
| SKILL.md two loop versions of gappy-column logic (`find_gappy_columns` and `remove_gappy_columns` each with own loop) | `remove_gappy_columns` reuses `find_gappy_columns` |

## Left unfixed

- Description does not list weights / Neff / MI-APC (audit note, not wrong; left).
- MI-APC and Neff are pure-Python pair loops (9 s for the 73x141 seed with the 5-shuffle null); not vectorised, out of scope for a correctness pass.
- Raw-MI null cannot catch coupling from singleton residues on very small alignments (the 6-sequence example shows one such pair above its null); the warning line already tells the user the output is noise below the guard.
- Easel-equivalent `pb` weights not re-implemented (see Henikoff row); pyhmmer is the route.
- The "2-3x" estimator-ratio claims: replaced by measurements, no attempt to characterise EVcouplings/HHsuite Neff (not installed).

---

# 2026-09-21: P2 fixes, split, scripts/

Skill `alignment/msa-parsing`, branch `fix/alignment-msa-parsing` (worktree `F:\OpenScience\wt\alignment-msa-parsing`) from staging main `431aa55`. Commits: `7d81f81` fix, `e83c870` split, `fea02de` scripts/. Audit: 6 P2s. Tools: Python 3.12.13, Biopython 1.88, numpy 2.0.2 (env `alignment`), MUSCLE 5.3 (WSL). SKILL.md 505 -> 245 lines (fix commit 505 -> 517, split 517 -> 287, scripts 287 -> 245).

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| `select_columns` / `normalize_alignment` quadratic | P2 | `str(record.seq)` hoisted once per record, full-width fast path (`msa_utils.py`; the inline copy is now an import, see scripts section) | ran: 10 x 100,000 columns normalise 11.34 s -> 0.02 s, output equals independent `upper().replace('.', '-')`; column subset unchanged | all other examples' no-arg output byte-identical before/after |
| `remove_duplicates` does not normalise | P2 | compares normalised rows, keeps original records (now `scripts/filter_sequences.py`) | ran: `AC-GT`/`AC.GT`/`ac-gt`/`ACGGT` -> 2 rows; `syn_dotgaps.fasta` dedup keeps a,c | |
| `a2m_a3m_io.py` fails on HMMER A2M | P2 | reads with `SeqIO.parse`, prints padded/unpadded, warns if match-column counts differ; SKILL.md (a2m reference) says HMMER 3.4 writes unpadded A2M and points to `pyhmmer.easel.MSAFile(format='a2m')` | ran on the audit's `hmmalign_globins8.a2m`: row lengths [149..161], 117 match columns per row; padded `example.a2m` still works | `alignment-io` says A2M is padded: other Skill, not touched (see left unfixed) |
| all-zero weights silent | P2 | `ValueError('weights must sum to a positive value')` in both weighted helpers (`find_conserved.py`, `consensus_sequence.py`), Common Errors row | ran: weights `[0,0,0,0]` raises; `[1,1,1,1]` and `None` unchanged | |
| description omits weights, Neff, MI-APC, MUSCLE5; SKILL.md over 500 lines | P2 | description extended; split into 7 `references/` files; runnable duplicates replaced by pointers | line counts, fence parse | |
| doc (a) structure-navigation pointer | P2 | names the sections that exist ("Reading the Declared (SEQRES) Sequence and Locating Gaps", "Reading mmCIF with an Explicit Numbering Scheme") and residue-number/SIFTS mapping; `_pdbx_poly_seq_scheme` dropped | docs: headings read in `structural-biology/structure-navigation/SKILL.md` | |
| doc (b) "stderr ends best <name>" and bare IndexError | P2 | reworded to the "CC min .., best <name>" line; `muscle5_column_confidence.py` prints a usage line and exits 1 without arguments | ran `muscle -maxcc` (5.3): line `CC min 148, avg 150, max 152, best acb.2`; script no-arg prints usage; with `ens_cc.efa acb.2 0.9` masked output byte-identical to the audit's | position of the line vs the URL varied with how stderr was captured, so the wording no longer claims "last" |
| doc (c) Stockholm round trip drops tags | P2 | annotation paragraph states Biopython 1.88 keeps only recognised tags | ran on PF00042 seed: raw `GC seq_cons`, `GR pAS`, GS AC x73; written: `GS AC`, `GS DE` (added), `GR AS`; seq_cons and pAS gone | |
| doc (d) Cocco 2018 attribution unverified | P2 | claim now "reasoning, not a measured cited result"; audit's measured top-30 contact precision (raw MI 0.13, MI-APC 0.00, baseline 0.09) added; Cocco kept only as background reading | audit run in8 (not re-run) | |

## Left unfixed

- `alignment/alignment-io` describes A2M as padded (audit note): different Skill, outside this fix's folder scope. It needs the same "HMMER writes unpadded" caveat there.
- Cocco 2018 was not checked against the paper (no access); the claim is softened, not confirmed.
- `henikoff_weights` (14 lines) stays inline in `references/weighting-neff.md` next to `examples/henikoff_weights.py`: under the 15-line threshold.

## Redundancy pass

Already done on 2026-09-20 (see above); `usage-guide.md` holds overview, prompts and a pointer only. No change this pass.

## Split (`SKILL.md` 517 -> 287 lines), verbatim moves

| SKILL.md section | new home |
| --- | --- |
| Alignment Trimming; Gap Handling for Phylogenetics; Identifying Unreliable Alignment Regions | `references/trimming-and-reliability.md` |
| Consensus Sequence | `references/consensus.md` |
| Sequence Filtering | `references/sequence-filtering.md` |
| Working with Annotations; Position Mapping | `references/annotations-and-position-mapping.md` |
| Sequence Weighting and Neff | `references/weighting-neff.md` |
| Coevolution: Mutual Information with APC | `references/coevolution-mi-apc.md` |
| A2M / A3M Conventions; Streaming Large Alignments | `references/a2m-a3m-streaming.md` |

Verified: no non-blank line lost (two lines edited to add pointers), 26 fences, python fences `ast.parse`, bash fences `bash -n`.

## Runnable code -> scripts/ (old location -> new)

| old location | new |
| --- | --- |
| `references/sequence-filtering.md` code block (26 lines: `_require_kept`, `filter_by_id`, `filter_by_gap_content`, `remove_duplicates`) | `scripts/filter_sequences.py` (adds CLI; imports `msa_utils` from `examples/`) |
| SKILL.md `select_columns`/`normalize_alignment` block (27 lines) | duplicate of `examples/msa_utils.py`: replaced by prose signature plus import line |
| SKILL.md `find_conserved_positions` block (23 lines) | duplicate of `examples/find_conserved.py`: replaced by import and usage |
| `references/consensus.md` `is_nucleotide` + `consensus_sequence` block (27 lines) | duplicate of `examples/consensus_sequence.py` and `msa_utils.is_nucleotide`: replaced by import, usage and signature note |

Ran as SKILL.md invokes them (from the Skill directory): `filter_sequences.py` CLI with `--dedup`, `--id-pattern`, `--max-gap-fraction`, the all-removed error, and Pfam PF00042 Stockholm (44 of 73 rows kept at gap fraction 0.2, equal to an independent count, output re-read as Stockholm); the import snippets and `remove_gappy_columns` from SKILL.md.

---

# 2026-09-21: final pass, phase 1 (fixer+auditor same agent)

Skill `alignment/msa-parsing`, branch `fix/alignment-msa-parsing` (worktree `F:\OpenScience\wt\alignment-msa-parsing`), tip `fea02de` -- unchanged. Env `alignment`. Full checkpoint:
`F:\OpenScience\audits\_final_pass\bio-alignment-msa-parsing\CHECKPOINT.md`.

Walked every runnable block in `SKILL.md`, every `references/*.md` code fence, all 11 `examples/*.py` and `scripts/filter_sequences.py`, from a clean scratch copy, on the real Pfam PF00042 seed, a real HMMER A2M, a fresh synthetic dataset and (for MUSCLE5 column confidence) a from-scratch WSL run on the 8 UniProt globins. Every block reproduced the prior fix log's numbers exactly (Neff 66.08/73.00, gap total 1943, conserved cols 17/77, MI-APC top pair 2.627 <= null 2.671, `filter_sequences.py` 44/73 kept, MUSCLE5 "CC min 148, avg 150, max 152, best acb.2" and 11/155 columns below CC 0.9); no regression found.

One open item resolved without a text change: the Cocco et al 2018 citation (previously "not checked against the paper, no access") is confirmed accurate against IOPscience/PubMed (Reports on Progress in Physics 81(3):032601, Jan 2018) -- the Skill already cites it only as background, so nothing needed correcting.

No code or prose change made this phase; no commit (nothing changed on the branch).

## Left unfixed (out of this Skill's scope, not blocked)

- `alignment/alignment-io`'s A2M-padding note: a different Skill's file; needs that Skill's own fixer.
- MI-APC/Neff pure-Python pair loops (not vectorised) and the raw-MI null's blind spot on singleton-residue coupling in very small alignments: documented, inherent properties, not incorrect output.
