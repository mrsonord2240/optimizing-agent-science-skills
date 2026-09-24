# bio-vcf-basics — fixes

## Backlog pass — 2026-09-15

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Wrong bcftools query -H tip in usage guide | P2 | Corrected tip: `bcftools view -H` skips the header, `bcftools query -H` adds a column header | ran `bcftools view --help` / `bcftools query --help` (1.24) and both commands on a synthetic VCF, confirming opposite behavior | |
| Update the bgzip error string | P2 | Listed current htslib messages ("not compressed with bgzip", "not BGZF compressed, cannot index") alongside the older "no BGZF EOF marker" | ran bcftools 1.24 (htslib 1.24) on a plain-gzip VCF: `bcftools index` and `bcftools view -r` reproduced the new messages | |
| Add a gVCF variant-site extraction recipe | P2 | Added `bcftools view -i 'N_ALT>1' sample.g.vcf` and a note that ALT string tests match any allele in the list | ran on audit's `sample.g.vcf` (bcftools 1.24): `N_ALT>1` isolated the 1 true candidate of 4 records; `ALT="<NON_REF>"` matched all 4 | |

Left unfixed: none (3/3 fixed).

## Final pass — 2026-09-24

Exact audited source: `mrsonord2240/bioSkills@7c665843f733a0833f21fe95a7c7199376159059:variant-calling/vcf-basics`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Valid `QUAL=0` rendered as missing by shipped viewer | P1 | Changed the viewer guard from truthiness to `is not None`, so zero renders as `0.0` and only missing QUAL renders as `.` | fresh two-record VCF through exact viewer; `py_compile` passed | |
| PL/GL transform and GQ derivation stated too universally | P1 | Documented rounded relative GL-to-PL scaling and made GQ-from-PL a caller-specific validation check | fresh GT/GQ/PL/GL VCF parsed with cyvcf2 0.34.0 | |
| VCF header contract overstated metadata as mandatory | P1 | Distinguished portable VCF recommendations from BCF dictionary requirements | checked current hts-specs VCF specification and exact guide text | |
| Plain-gzip index diagnostic omitted current bcftools wording | P2 | Added `in a format that cannot be usefully indexed` to Common Errors | archived convert/index stress input with bcftools 1.24 | |

Final validation: reran archived inputs 1--5 plus two fresh cases (28/28 assertions), `py_compile`, and `git diff --check`. Final self-audit: 95/100; `auditor_independent=false`; no open P0/P1/P2.
