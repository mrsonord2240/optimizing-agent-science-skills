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

## Final pass — 2026-09-24

Source commit `356581080738dee60b613812b35fd4b99d217527` on isolated branch `agent/finalpass-bio-variant-normalization-20260924`.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| Canonical and companion-guide routes disagreed about atomization and REF preflight | P1 | Made the primary route and all complete guide routes split -> atomize -> left-align; added mismatch preflight before output/index creation | exact-commit harness, archived inputs 1-2 and fresh input B | MNP-preserving route remains explicitly limited to consumers that require it |
| Guide claimed `-m-both` differs while splitting | P2 | Documented that it is identical to `-m-any` for `-m-`; type distinction is for joining | archived input 3 and fresh mixed SNP/indel input | `-m+both` separation also executed |
| Primary repeat illustration used inequivalent deletion alleles | P1 | Replaced with valid shifted homopolymer deletion representations | source review plus archived homopolymer normalization | chr1:506 `AA>A` reaches canonical `500 GA>G` |
| `csq -p s` claimed no consequence is emitted globally | P2 | Limited wording to documented skip behavior and tells users to inspect emitted BCSQ on the installed version | archived input 5, bcftools 1.24 | unphased MNP consequence omitted; isolated-site output is version-sensitive |

Final exact-commit audit: `F:\OpenScience\audits\bio-variant-normalization\runs\finalpass_20260924\exact_commit_audit.log` — 5 archived logical inputs plus 2 fresh inputs, 17/17 assertions passed. `vt` was unavailable; the input-4 logical reconciliation used the documented bcftools atomization equivalent and is labeled accordingly in the evidence. Final report: 95/100, Production Ready, no open P0/P1/P2; `auditor_independent=false` because the fixer performed this exact-commit audit under one brief. No merge, push, publish, or promotion was performed.
