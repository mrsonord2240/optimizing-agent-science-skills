# bio-variant-annotation — fixes (2026-09-15)

Branch `fix/variant`. Runtime: bcftools 1.24 (MSYS2, candidate venv, plugins via BCFTOOLS_PLUGINS); audit data `audits/bio-variant-annotation/data`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Piped `annotate -a <vcf>` recipes fail | P1 | Basic, Clinical and Rare recipes and `annotate_vcf.sh` write indexed `-Oz` intermediates | ran on normalized callerA: all three recipes exit 0; example gnomAD branch exit 0 with `gnomAD_AF` populated | `bc` is missing in the Windows shell only (percentage line), not a Skill defect |
| `bcftools csq` lacks `--phase` | P1 | `-p a` in SKILL.md and usage guide; `-p a/m/s` semantics incl. merged haplotype consequences | ran: default exits on unphased het; `-p a` exit 0 | |
| Rare recipe clobbers cohort `INFO/AF` | P1 | Annotate into `INFO/gnomAD_FAF:=INFO/fafmax_faf95_max`, filter on the new tag (also `gnomAD_AF` in basic recipe/example) | ran on callerA + `fill-tags AF`: old recipe kept 500,1026,2000 (lost absent ClinVar P/LP 1101,1231); new kept 500,1026,1073,1101,1231,1420,1466,2000 | |
| `--pick` default outdated; pick_order drops MANE Plus Clinical | P2 | VEP 110+ default order stated; `mane_plus_clinical` added to both `--pick_order` lines | docs: VEP 114.2 `Config.pm` as checked in the audit | VEP not re-run |
| SIFT/PolyPhen/CADD calibration overstated | P2 | Qualified to developer thresholds; calibrated PP3 intervals cited | docs: Pejaver 2022 Table 2 values as quoted in audit Input 4 | |

Left unfixed: none.
