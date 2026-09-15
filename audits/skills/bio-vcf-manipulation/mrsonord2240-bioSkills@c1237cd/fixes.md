# bio-vcf-manipulation — fixes (2026-09-15)

Branch `fix/variant`. Runtime: bcftools 1.24 (MSYS2, candidate venv); audit data `audits/bio-vcf-manipulation/data`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `reheader` cannot fix chr1-vs-1 record naming | P1 | `bcftools annotate --rename-chrs` for records; `reheader -f` for header only (SKILL.md prose, reheader section, Common Errors row, usage-guide tip) | ran: cohort split into two 4-sample batches, batch 2 renamed to `1`/`2`, `--rename-chrs` then merge = 361 sites x 8 samples (joint callset 361) | |
| concat sample-order fix wrong | P2 | Reorder with `bcftools view -s <order>` first; plain concat also refuses | audit Input 2 output | not re-run |
| `-R` overlapping-region duplication claim | P2 | Qualified to older releases; 1.21/1.24 do not duplicate (SKILL.md, usage guide, Common Errors) | audit Input 4 output (1.21 and 1.24) | older-release behaviour not checked |

Left unfixed: none.
