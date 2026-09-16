# bio-vcf-basics — fixes

## Backlog pass — 2026-09-15

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Wrong bcftools query -H tip in usage guide | P2 | Corrected tip: `bcftools view -H` skips the header, `bcftools query -H` adds a column header | ran `bcftools view --help` / `bcftools query --help` (1.24) and both commands on a synthetic VCF, confirming opposite behavior | |
| Update the bgzip error string | P2 | Listed current htslib messages ("not compressed with bgzip", "not BGZF compressed, cannot index") alongside the older "no BGZF EOF marker" | ran bcftools 1.24 (htslib 1.24) on a plain-gzip VCF: `bcftools index` and `bcftools view -r` reproduced the new messages | |
| Add a gVCF variant-site extraction recipe | P2 | Added `bcftools view -i 'N_ALT>1' sample.g.vcf` and a note that ALT string tests match any allele in the list | ran on audit's `sample.g.vcf` (bcftools 1.24): `N_ALT>1` isolated the 1 true candidate of 4 records; `ALT="<NON_REF>"` matched all 4 | |

Left unfixed: none (3/3 fixed).
