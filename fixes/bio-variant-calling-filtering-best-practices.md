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
