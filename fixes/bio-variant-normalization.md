# bio-variant-normalization — fixes (2026-09-15)

Branch `fix/variant`. Runtime: bcftools 1.24 (MSYS2, candidate venv); audit data `audits/bio-variant-normalization/data`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Recommended atomize -> split order emits spurious `*` records | P1 | Split -> atomize -> left-align in the pipeline, both workflows, Quick Reference and `normalize_vcf.sh`; `--atom-overlaps '*'` explained; single-pass `-m-any --atomize` noted; Common Errors row | ran: edge_multiallelic 1/2 site, old order `A>C, A>*, A>G, A>*`; new order and single pass `A>C, A>G` | |
| csq advice omits `--phase` | P1 | `-p a|m|s` explained in the atomize caveat; Quick Reference and Common Errors rows | ran: callerA, default csq exits "Unphased heterozygous genotype at chr1:1026"; `-p a` exit 0, MNV at 1041 as 11L>11F | |
| Example hides bcftools errors behind `2>/dev/null` | P2 | stderr kept; `norm -c w` REF pre-check exits 1 with a count | ran: callerA exit 0 (11 -> 12 records); callerB exit 1 "1 REF allele(s) do not match"; edge file 1 -> 2 records | `bash -n` ok |
| `-m-both` described inconsistently | P2 | SKILL.md table: type string only matters for `-m+` | docs: bcftools norm manual; consistent with the usage guide | |

Left unfixed: none.

## Backlog pass — 2026-09-15

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| csq --phase m and s described wrongly | P2 | Replaced paraphrase with verbatim `bcftools csq` help semantics (a/m/s); recommend -p a for unphased input | ran: `bcftools csq --help` 1.24, matches corrected text | |
| Database-annotation block leaves an empty file on REF error | P2 | Added `set -o pipefail` + `bcftools norm -c w` MISMATCH pre-check to "Full Normalization for Caller Comparison" and "Before Database Annotation" blocks | ran on synthetic REF-mismatch VCF (bcftools 1.24): reproduced the 0-byte-file / "not BGZF compressed" masking without the fix; pre-check catches it with a clear message and exit 1 with the fix; also ran happy-path (matching VCF) to confirm no regression | |

Left unfixed: none (2/2 fixed).
