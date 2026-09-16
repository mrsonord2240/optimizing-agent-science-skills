# bio-vcf-manipulation — fixes (2026-09-15)

Branch `fix/variant`. Runtime: bcftools 1.24 (MSYS2, candidate venv); audit data `audits/bio-vcf-manipulation/data`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `reheader` cannot fix chr1-vs-1 record naming | P1 | `bcftools annotate --rename-chrs` for records; `reheader -f` for header only (SKILL.md prose, reheader section, Common Errors row, usage-guide tip) | ran: cohort split into two 4-sample batches, batch 2 renamed to `1`/`2`, `--rename-chrs` then merge = 361 sites x 8 samples (joint callset 361) | |
| concat sample-order fix wrong | P2 | Reorder with `bcftools view -s <order>` first; plain concat also refuses | audit Input 2 output | not re-run |
| `-R` overlapping-region duplication claim | P2 | Qualified to older releases; 1.21/1.24 do not duplicate (SKILL.md, usage guide, Common Errors) | audit Input 4 output (1.21 and 1.24) | older-release behaviour not checked |

Left unfixed: none.

## Backlog pass — 2026-09-15

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Sample-reorder advice does not make --naive work | P2 | Common Errors `--naive` row corrected: `view -s` reorder adds INFO/AC and INFO/AN header lines so `--naive` still refuses; recommend plain `concat` after reorder, or re-running `view -s` on every file so headers match | ran: bcftools 1.24, synthetic cohort split into chr1.bcf/chr2.bcf; reproduced `Cannot use --naive, incompatible headers, the tag INFO/AC not present in chr1.bcf` after `view -s` reorder; plain concat -> 361 records = joint truth; `view -s` on both files -> `--naive` succeeds, 361 records = joint truth | commit `924d204`, supersedes the prior pass's unverified P2 row above (that row was checked against plain concat only, not --naive) |

Left unfixed: none.
