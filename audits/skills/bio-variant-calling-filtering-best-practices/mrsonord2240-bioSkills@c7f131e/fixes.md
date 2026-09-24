# bio-variant-calling-filtering-best-practices — fixes (2026-09-15)

Branch `fix/variant`, worktree `F:\OpenScience\external\bioSkills-wt-variant`. Runtime: bcftools 1.24 (MSYS2, candidate venv), audit data `audits/bio-variant-calling-filtering-best-practices/data`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `filter_variants.sh` fails at `bcftools concat` on multi-contig input | P1 | Index both filtered files; `bcftools concat -a` | ran: cohort.vcf, exit 0; PASS set 240/240 true SNP, 25/25 hom-alt, 20/20 indel, 4/60 artifact SNP (same as GATK VariantFiltration) | `bash -n` ok |
| Somatic post-filter `FMT/AF[0]` rejected; obvious `AF[0:0]` tests the normal | P1 | Tumor column index from `##tumor_sample` + `bcftools query -l`; `FMT/AF[$T:0]`, `FMT/DP[$T]`; states that only the tumor column is tested | ran: audit mutect_syn.vcf, T=1, kept 5100/5200/5300 (+5500, germline het also high in tumor) | FilterMutectCalls itself not run (needs Mutect2 tables) |
| Usage-guide allele-balance expression does not parse | P2 | `FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1])` | ran: exit 0, 262 records | |
| cyvcf2 block not equivalent to the hard filter | P2 | Labelled a minimal pattern; names the missing QD/SOR/RankSum terms | text | not extended (would be new code) |
| Common Errors misses the Skill's own failures | P2 | Rows for concat contiguity and `[sample:subfield]` | error strings from audit runs | |

Left unfixed: none.

## Backlog pass — 2026-09-15

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Tumor-column block has no guard for a missing header | P2 | Added `[ -n "$TUMOR" ] && [ "$T" -ge 0 ] \|\| { echo 'tumor sample not found; pass it explicitly'; exit 1; }` before the filter | ran: synthetic Mutect2-style VCF, no `##tumor_sample` header, bcftools 1.24 -- reproduced segfault (exit 139) without guard, clean exit 1 with guard | |
| Usage-guide allele-balance recipe deletes hom-alt sites | P2 | Switched `-i 'GT="het" & ...'` (site include) to `-S . -e 'GT="het" & (...<=0.2 \| ...>=0.8)'` (genotype-level exclude) | ran: 3-site synthetic VCF (hom-alt, balanced het, skewed het), bcftools 1.24 -- old form kept 1/3 sites, new form kept 3/3 sites and nulled only the skewed genotype | |
| cyvcf2 block is still only a partial filter | P2 | Added QD, SOR, None-guarded MQRankSum/ReadPosRankSum terms, mirroring the bcftools expression term for term | py_compile OK (Python 3.12, candidate venv); cyvcf2 itself absent from candidate venv and WSL agents distro (ModuleNotFoundError both places), not installed per no-install rule -- terms verified by direct correspondence to the already-verified bcftools expression, not by running cyvcf2 | cyvcf2 unavailable on this machine; flagging for Sam if end-to-end run is needed |

Left unfixed: none (3/3 fixed; cyvcf2 change verified by py_compile + logical equivalence only, not by execution, because the package is absent here).

## Final pass — 2026-09-24

| finding | priority | change | verified | source commit |
|---|---|---|---|---|
| Zero-valued `DP` or `MQ` in the cyvcf2 example was coerced by `or 1e9` and passed as though missing | P2 | Preserve the raw values and use explicit `is None` pass-through checks (`dp_ok`, `mq_ok`) | Exact-current predicate body executed against VCF-shaped cases: `DP=0` and `MQ=0` rejected; missing DP/MQ and missing rank-sums retained. The live cyvcf2 package is absent in the available runtimes, so this is a documented predicate test, not an integration claim. | `c7f131e61134fb550457f761e76bd07dc0a840a8` |

Final-pass audit: `F:\OpenScience\audits\bio-variant-calling-filtering-best-practices\eval_report_bio-variant-calling-filtering-best-practices_result.json`. Final result: 91/100, Production Ready; scoped open P0/P1/P2: none.
