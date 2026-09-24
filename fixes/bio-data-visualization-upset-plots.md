# Fix log: bio-data-visualization-upset-plots

## 2026-09-23 — backlog correction

Skill `data-visualization/upset-plots`, branch
`fix/data-visualization/upset-plots`, corrective commits
`722b632f950c2e5ab9405781d4f2fd236281c5b3` and
`cbf68034488c0a367703d34eb22b2931d0283fee` from staging `8c75e1f4`.
Validated with ComplexUpset 1.3.3, UpSetR, upsetplot 0.9.0, pandas 2.x, and
the data-visualization R/Python environments.

| finding | priority | change | verification |
| --- | --- | --- | --- |
| Python route crashed on `show_counts`, pandas 3, and `.to_frame()` misuse | P1 | Documented the compatible pandas 2.x/upsetplot 0.9 stack, disabled broken automatic counts and added manual labels, kept metadata on the MultiIndex frame, removed stray axes, and used `max_subset_rank`. | Exact Python example exits 0, writes three PNG/PDF pairs, and focused labels/rank/metadata assertions pass. |
| ComplexUpset queries targeted empty intersections or over-highlighted ranges | P1 | Kept one valid exclusive query, documented the multi-query limitation on the tested stack, supplied attribute columns, and require present plus absent sets for exact styles. | Query and exact-highlight assertions pass without an empty-target crash. |
| Empty sets, blank/NA IDs, and UpSetR `nsets=4` silently lost data | P1 | Added a preflight that trims/deduplicates, warns on dropped blank/NA IDs, stops on empty sets, prints cleaned sizes/union, and passes `nsets=length(sets)`. | Empty-set, dirty-ID, and seven-set preservation tests pass. |
| Sorting, inclusive-mode, degree, version, possibility-count, and API claims were false | P1 | Corrected each claim to the observed ComplexUpset/UpSetR behavior and qualified package calls to avoid masking. | Focused semantic tests and static checks pass; Hallmark regression retains 10 sets, union 1,211, 137 observed combinations, and the independent top-20 counts. |
| Toy data, exports, and guide structure did not demonstrate the promised behavior | P2 | Replaced the toy with deterministic unequal exclusives, added valid attributes, Cairo/Type-42 exports, and reduced the guide to nonduplicated operational pointers. | R example writes three PDFs; Python exports contain compliant fonts; expected exclusive counts `12,9,7,6,4,4,2,2` pass. |
| `max_subset_rank` was described as an unconditional hard bar-count cap | P2 | Documented that the value limits intersections by rank, that ties at the cutoff can retain more bars, and that exact-count outputs require pre-filtering. | The exact pandas-2 guard rendered 3 bars without a tie and 6 bars at a tied rank-3 boundary; the final report has 23/23 passing assertions and no recommendations. |

## Findings left unfixed

None. Upstream plotting packages emit known ggplot deprecation warnings; these
do not alter the checked outputs.
