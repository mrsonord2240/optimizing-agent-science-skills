# bio-vcf-statistics — fixes (2026-09-15)

Branch `fix/variant`. Runtime: bcftools 1.24 (MSYS2, candidate venv); audit data `audits/bio-vcf-statistics/data`. No P1 in the audit; the het allele-balance one-liner was named in the dispatch as result-changing.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Het allele-balance one-liner mixes all samples (0.729) | P2 | `-f '[%SAMPLE\t%GT\t%AD\n]'`, mean alt/(ref+alt) per sample over 0/1 genotypes (SKILL.md and usage guide) | ran on cohort.vcf: 0.419-0.489 per sample; identical to an independent Python parse of the VCF | |
| plot-vcfstats needs pdflatex/tectonic | P2 | Usage-guide tip and Common Errors row | audit Input 1 (exit 2 at PDF step, PNGs written) | not re-run |

Left unfixed:
- P2 peddy/somalier site-panel requirements: would add new content (site panels, `somalier find-sites`), out of scope for a correction.
