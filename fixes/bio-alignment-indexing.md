# Fix log: bio-alignment-indexing (alignment-files/alignment-indexing)

## 2026-09-20 (fixer: Sonnet, branch `fix/af-index`, worktree `F:\OpenScience\wt\af-index`, base c206dff)

Tools checked on: samtools 1.24 / htslib 1.24, pysam 0.24.1, Python 3.12.14, bc/awk in WSL `science` env `alignment-files`. First audit: 75, Beta Only, not deployable (assertion pass 15/25). Scratch tests: `F:\OpenScience\scratch\af-index\` (not in any repo).

Findings fixed: 9/9 (4 P1, 5 P2).

| Finding | Priority | Change | Verified (ran) | Notes |
| --- | --- | --- | --- | --- |
| Staleness snippet and batch loop break for CSI-indexed BAMs | P1 | `-nt x.bam.bai` snippet replaced by `ensure_index()` (bash): checks every index in htslib order (`.csi`, `x.csi`, `.bai`, `x.bai`, `.crai`), re-indexes if none or any stale, deletes all first, keeps CSI if a `.csi` existed; batch loop is `for f in *.bam; do ensure_index "$f"; done`. Python twin `ensure_indexed()` in SKILL.md and the example | Extracted from the shipped SKILL.md and run: none -> BAI; fresh -> mtime unchanged; stale BAI -> count 150098 == full-scan awk truth; **stale CSI** -> only `.csi` left, count == truth (before fix: `error closing`); fresh BAI + stale CSI -> fixed; alt `x.bai` kept; CRAM -> `.crai`; batch over BAI/BAI/CSI files left types as they were | Precedence order verified pairwise (12 combos): `x.bam.csi` > `x.csi` > `x.bam.bai` > `x.bai` |
| CRAM: no reference guidance, pysam idxstats silently 0, helpers ignore .crai | P1 | New `## CRAM` section: `samtools view -T`, `pysam.AlignmentFile(..., 'rc', reference_filename=)`, REF_PATH / `@SQ UR:`, failure messages, `samtools idxstats` or `pysam.idxstats()` for counts. `.crai` handled in both helpers and the example | Public CRAM (unreachable UR): `-T` region 5642 == BAM 5642; no `-T` records 0 with `Failed to populate reference`; `view -c` still 5642; pysam without reference `OSError: truncated file`; with reference count 5642; `get_index_statistics` -> 0, `pysam.idxstats` -> `chr22 40001 5642 0` | Removed the CRAM stub from usage-guide |
| Large-genome section wrong in four places | P1 | Rewrote: BAI fails loudly (no `.bai`); default `-c` auto-sizes depth; `-m` only sets smallest bin, not reach; contigs >2^31-1 not storable in BAM (split reference). Table row and "2^(18+15)" block and "silently truncates" row deleted | CSI header parsed: 830 Mbp default `-c` min_shift 14 depth 6 (2^32); `-m 18` depth 4 (2^30); 2.0 Gbp default depth 6, `-m 18` depth 5; BAI on 594/830/2000 Mbp exits 1, no `.bai`; 3 Gbp SAM -> BAM `Positional data is too large for BAM format` | Species row now "up to 2^31-1 bp"; I did not verify real pine/axolotl contig sizes, row tells the user to check the largest contig |
| `-L bed` shown as index access | P1 | `samtools view --region-file regions.bed` (same as `-M -L`) shown as index access; plain `-L` documented as whole-file filter. Same fix in usage-guide (section deleted, see below). Also `-M` for overlapping multi-regions | 600k-read BAM: `-L` 1851 / `--region-file` 1851 / `-M -L` 1851 == awk full-scan truth 1851; 0.75-0.82 s vs 0.02 s; damaged tail: `-L` rc 1, `--region-file` rc 0. Overlap: 6071 without `-M`, 4555 with `-M` == union 4555 | |
| Common Errors strings do not match tools | P2 | One table in SKILL.md with exact samtools 1.24 / pysam 0.24.1 messages: missing index, `Unsorted positions ... failed to create index`, unknown contig (rc 0, 0 reads; pysam `invalid contig`), stale index, BAI too large, positional too large, CRAM reference, idxstats slow method. Contig-naming paragraph fixed | Each message reproduced in this session | usage-guide Troubleshooting deleted |
| fetch_regions.py rejects region forms samtools accepts; no CRAM; no staleness | P2 | Rewritten: own `parse_region()` (commas, bare contig, `chr:start-`, contigs containing `:`, `{braced}`), `--reference` for CRAM (mode `rc`), `ensure_indexed()`, clean `sys.exit` messages | From a clean copy, counts == `samtools view -c`: `chr22:1952-4700`, `chr22:1,952-4,700`, `chr22`, `chr22:1952-` (all 5642), `HLA-A*01:01:01:01:1-1500` (2), bare HLA (3), braced (2), CRAM with `--reference` 5642; bad contig / bad coords exit 1 with message; CRAM without reference gives the hint. `py_compile` ok | **Audit's suggested `fetch(region=...)` does not work**: pysam 0.24.1 raises ValueError on all of those forms (parser is Python-side), so the fix parses the region itself |
| `is_indexed()` misses `input.bai`, `.crai`; sibling false positives | P2 | Replaced by `index_candidates()` + `ensure_indexed()` with per-format candidate lists | Alt `a.bai` treated as index (not rebuilt); CRAM gets `.crai`; no sibling `.bam.bai` lookup for CRAM | |
| usage-guide mito awk hard-codes `chrM`; X/Y prompt has no code | P2 | Awk moved into SKILL.md (idxstats section), matches `^(chr)?(M\|MT)$`, guards `total==0`. **X/Y ratio prompt deleted** | chrM 50.00%; `MT` 33.33% (true); real BAM with contigs `1` and `MT` 33.33% (true); empty input prints nothing, no error | X/Y: chose deletion (FIX_BRIEF option 3); needs a sex-chromosome BAM and PAR handling to verify, none on this machine |
| `-F 2304` primary recipe, FASTA off-by-one, threads claim, duplication | P2 | `-F 2308` for primary mapped; SKILL FASTA `fetch('chr1', 999, 2000)` with comment; `-@` claim replaced with measurement; usage-guide de-duplicated | `-F 2308` chrA 4 == awk truth 4 (`-F 2304` gave 5); FASTA fetch(999,2000) == faidx chr22:1000-2000 (1001 bp), fetch(1000,2000) not equal; `-@ 0/4/8` on 86 MB BAM 3.1-3.2 / 3.0 / 3.1-3.3 s | |

Also added (small, verified): non-standard index name (`samtools index in.bam out.bai`) needs `-X` / `index_filename=` (verified: default `Could not retrieve index file`, `-X` and `index_filename` both count 2); `@HD` is not proof of sort order (failed index is); `samtools idxstats` on a stale index reports old totals; install line moved into SKILL.md.

## Findings left unfixed

None of the report's nine. Not verified (stated in table): real pine/axolotl contig sizes.

## Deleted passages and where the content now lives

From `SKILL.md`:

| Deleted | Now |
| --- | --- |
| "For polyploid plants..." block with `-m 18` and the `2^(14+5*3)` / `2^(18+15)` comments | Large-genome bullets under "Which Index for Which Genome" (corrected) |
| "Index file precedence" paragraph | "Index File Locations" (full order, `.csi` beats `.bai`, htsjdk note) |
| pysam `is_indexed()` | `ensure_indexed()` under "Check if Indexed (and Fresh)" |
| `-nt input.bam.bai` staleness snippet | `ensure_index()` under "Index Staleness" |
| Common Errors rows: `file is not sorted`, `chromosome not found`, "BAI silently truncates" | New Common Errors table |
| Table row "multi-Gbp / CSI with larger -m" | Rewritten row |

From `usage-guide.md` (now overview, prompts, "what the agent will do" only; everything below was a duplicate of SKILL.md):

| Deleted | Now |
| --- | --- |
| Prerequisites (conda/pip) | SKILL.md "Version Compatibility" (Install line) |
| Index Types (BAI, CSI, CRAI) | SKILL.md "Index Types" |
| Common Commands: creating indices, region queries, idxstats | SKILL.md "samtools index", "Using Indices for Region Access", "idxstats" |
| Batch Indexing loop (`.bai` only, CSI-unsafe) | SKILL.md `ensure_index` loop |
| `-L targets.bed` line | SKILL.md `--region-file` / plain `-L` note |
| Mito awk (`/^chrM/`) | SKILL.md "Mitochondrial Fraction" (fixed) |
| Python: region queries, index statistics, FASTA access (`fetch('chr1', 999, 2000)`) | SKILL.md "pysam Python Alternative", "FASTA Index" |
| Troubleshooting (4 entries incl. wrong strings) | SKILL.md "Common Errors", "Contig-Naming Sanity Check" |
| Tips list (7 items) | Covered by SKILL.md sections; the `-@` tip replaced by the measured note; nothing unique lost |
| Prompt "Check X/Y ratio for sex determination" | Deleted with its claim (no code) |
| Prompts added: "skip ones that already have a fresh index", "index my CRAM ... reference ref.fa" | new, point at `ensure_index` and CRAM sections |

The usage-guide and SKILL.md disagreed on the unsorted-BAM message (`file is not coordinate sorted` vs `file is not sorted`); both wrong, replaced by the message printed by samtools 1.24.
