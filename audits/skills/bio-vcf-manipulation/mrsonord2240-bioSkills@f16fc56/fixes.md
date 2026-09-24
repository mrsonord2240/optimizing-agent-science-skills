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

## Final pass — 2026-09-24

Source: `mrsonord2240__bioSkills` commit `f16fc56a854565e26d87a67d3de2df91e986b056` on `agent/finalpass-bio-vcf-manipulation-20260924`.

Final-pass disclosure: `auditor_independent=false`; final pass: fixed and audited under one brief, see CHECKPOINT.md.

| finding | priority | change | verified |
|---|---|---|---|
| Ambiguous `--naive` concat recovery | P2 | State the two valid paths precisely: plain concat after repairing one input's sample order, or `view -s <same-order>` on every input before `--naive`. Make the operation-choice table explicitly identify `--naive` with divergent headers/sample order as misuse. | Seven archived cases plus fresh reordered-sample case on bcftools 1.24: both valid paths generated 361 records and the joint tuple hash. |
| Header-only contig repair could be misapplied | P1 | Preserve and reverify the existing `annotate --rename-chrs` instruction against `reheader -f`. | Fresh contig-record case: header-only output retained body `1,2`; record rename then merge generated 361 sites x 8 samples equal to joint truth. |

Left unfixed: none. Score: 93/100, Production Ready (self-audited; not independent acceptance evidence). Canonical raw report/viewer: `F:\OpenScience\audits\bio-vcf-manipulation\`.
