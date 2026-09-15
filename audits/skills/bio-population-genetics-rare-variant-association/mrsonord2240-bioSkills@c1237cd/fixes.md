# bio-population-genetics-rare-variant-association — fixes (2026-09-15)

Branch `fix/variant`. Runtime: WSL `agents` distro, regenie 4.1.3, plink2 a6.9, r-saige 1.3.1 (audit envs under /tmp/vaca); audit data copied to /tmp/vacafix/rv.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| SAIGE-GENE+ `--annotation_in_groupTest` separators reversed | P1 | `"lof,missense;lof,missense;lof;synonymous"`; comment now says comma = test, semicolon = annotations joined within a test | help: `step2_SPAtests.R --help` (SAIGE 1.3.1) states this; ran step 2 on audit data: groups `lof`, `missense;lof`, `missense;lof;synonymous` + Cauchy, exit 0, G21 Cauchy p 4.3e-8 | step 1 null reused from audit run in4 |
| regenie step-1 block omits `--bt` | P1 | `--bt` added, with note to fit step 1 on common array variants | ran (via example step 1): exit 0 | |
| `rare_variant_test.sh` runs step 1 on rare-variant genotypes | P1 | Separate `<array_prefix>` and `<exome_prefix>` arguments | ran: array/wes audit data, exit 0; G21 LoF SKAT-O LOG10P 7.93, G01 LoF+missense ACAT-O 4.01 | `bash -n` ok |
| "implicit singleton mask" | P2 | `.all` mask added; singleton masks need `--singleton-carrier` | audit regenie 4.1.3 output (`.all` masks, no singleton) | |
| SAIGE bgen step-2 command incomplete | P2 | `--bgenFileIndex`, `--sampleFile` added | help: both flags listed in `step2_SPAtests.R --help` | bgen form not run (no bgen/bgi built) |

Left unfixed: none.
