# `bio-metabolomics-metabolite-annotation` fix log (2026-09-16)

Branch `fix/r2-metab-b`, commit `0bc7319`. Score 86 (Limited Release, PASS all vetoes) —
the only core metabolomics Skill that cleared its floor. Scope: every P0/P1/P2 in
`eval_report_bio-metabolomics-metabolite-annotation_result.json` plus anything AUDIT.md
names for this Skill (only the precursor_mz P1 is named there). No P0s were reported.

| Finding | Priority | Change | Verified | Notes |
| --- | --- | --- | --- | --- |
| Common Errors table + Version Compatibility note + code comment claim missing `precursor_mz` makes ModifiedCosine "score all zero"; matchms 0.33+ actually raises `AssertionError: Precursor_mz missing` | P1 | Rewrote the table row, the Version Compatibility paragraph, and the `prepare()` comment to state the real exception; added `AssertionError` to the introspect-on-exception list | Ran — isolated `ModifiedCosine` on a no-precursor spectrum against matchms 0.33.1, got the same `AssertionError` the audit reported | Two independent confirmations (this fix's run + the audit's own two runs) |
| MetFrag named as one of three annotation routes with zero executable guidance (no params.txt skeleton, unlike SIRIUS's full bash block) | P1 | Added "Run MetFrag for Explainable Structure Ranking" section: params.txt template, CSV-quoting gotcha (unquoted InChI comma silently drops a row, exit 0), CLI line | Ran — `java -jar MetFragCommandLine-2.6.1.jar params.txt` end to end, reproduced citrate/isocitrate tie at Score 1.0 vs. glucose at 0.12 | Checked on MetFragCommandLine 2.6.1 |
| matchms library-matching code takes `max(pairs, ...)`, so a tied library match (the isomer wall the prose warns about) can never be surfaced by the shipped pattern | P1 | Extended the loop to keep all hits within a small margin (`TIE_MARGIN=0.02`) of the top score and report >1 passing hit as a tie -> Level 3, instead of picking a single winner | Ran — built a synthetic citrate/isocitrate reference pair; old logic picks one winner at Level 2a, new logic correctly reports both tied at Level 3 | matchms 0.33.1 |
| `examples/annotate_features.py` docstring says `query_promiscuous` is rejected by the matched-peak floor, but its actual score (0.69) is already below the 0.7 score floor too | P2 | Retuned `query_promiscuous` intensities so score clears 0.7 (0.78) while matches stay at 2, isolating the matched-peak floor as the documented rejection reason | Ran — script now prints `score=0.78 matches=2 level=3` | matchms 0.33.1 |
| Shipped example has no self-check; a future matchms bump could silently change output | P2 | Added `assert results['query_strong'] == '2a'` / `assert results['query_promiscuous'] == 3` | Ran — script exits 0, both asserts pass | |

No findings left unfixed.

Tooling used: `F:\OpenScience\audit-envs\untargeted-metabolomics-analyst\Scripts\python.exe`
(matchms 0.33.1), `F:\OpenScience\audit-envs\untargeted-metabolomics-analyst\tools\metfrag\MetFragCommandLine-2.6.1.jar`,
system JDK 17. No packages installed or changed in the shared venv or R library.

---

# 2026-09-21 fix batch (Production Ready Skill, 2 open P2s)

Branch `fix/metabolomics-metabolite-annotation` from staging `431aa55`. Commits: `2bbb6f3` (fix + dedup), `52cdec6` (scripts/). Env `untargeted-metabolomics-analyst` (matchms 0.33.1, MetFragCommandLine 2.6.1, JDK 17). Nothing installed.
SKILL.md: 282 -> 235 lines (under the 300 split threshold; no `references/` split needed).

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| `prepare()` comment says `add_precursor_mz` raises AssertionError | P2 | Comment reworded: the filter only warns, the AssertionError fires later in `calculate_scores()` | Ran: `add_precursor_mz` on a spectrum with no precursor returned with a warning, the next `calculate_scores` raised `AssertionError: Precursor_mz missing` | Comment now lives in `scripts/match_library.py` |
| MetFrag section has template but no worked data | P2 | Added `examples/metfrag/peaklist.txt` and `candidates.csv` (citrate/isocitrate/glucose, from the audit's run); SKILL.md points at them | Ran: MetFragCommandLine 2.6.1 on the shipped data, 3 candidates stored, citrate = isocitrate = 1.0, glucose 0.12 | Run both verbatim from the old SKILL.md block and via the new script |
| (found while running) matchms loop crashes on a query with no shared peak | not in audit | `scripts/match_library.py` reports it as Level 5 | Ran: synthetic noise query gave `IndexError` on `pairs[0]` before, "no confident candidate -> Level 5" after | matchms stores no scores for zero-overlap pairs |
| (found while running) MetFrag exits 0 on 0 stored candidates | not in audit | `scripts/run_metfrag.sh` exits 1 when the result has 0 rows | Ran on the audit's unquoted-comma CSV: exit 1 with message; shipped CSV: exit 0, 3 rows | Prose warning kept |

## Left unfixed

None of the 2 P2s. Not moved to scripts/: the SIRIUS bash block (12 lines, needs `sirius login`, not runnable here) and `assign_level` (13 lines, short helper); both stay inline.

## Redundancy pass

| deleted passage | new home |
| --- | --- |
| SKILL.md Version Compatibility: AssertionError paragraph | Common Errors row 1 (unchanged); Version Compatibility now points there |
| SKILL.md Version Compatibility: "Level 1 needs an authentic standard ... no software output can substitute" | Insight paragraph and Level 1 taxonomy row |
| usage-guide Prerequisites (pip / SIRIUS / MetFrag install) | SKILL.md Version Compatibility "Install:" line |
| usage-guide Prerequisites (ion families collapsed) | SKILL.md failure mode "In-source fragments and adduct cascades" |
| usage-guide Tips: name needs a level | SKILL.md Insight |
| usage-guide Tips: high cosine on few peaks | SKILL.md "Cosine score is not identity" |
| usage-guide Tips: isomers, top-1 structure Level 3 | "The isomer wall"; Quantitative Thresholds COSMIC row |
| usage-guide Tips: only an in-house standard earns Level 1, literature/external RT does not | SKILL.md Level 1 taxonomy row (literature/external library RT clause added; the only content that was guide-only) |
| usage-guide Tips: database choice biases the answer | SKILL.md SIRIUS block comment on `--database` |
| usage-guide Tips: network edges mean "related to" | SKILL.md Tool Roles FBMN row; `assign_level` `network_propagated` |
| usage-guide "What the Agent Will Do" (6 steps) | Restates the SKILL.md sections; guide now points at SKILL.md |

## scripts/ moves

| old location | script |
| --- | --- |
| SKILL.md "Match MS/MS Against a Spectral Library" python block (44 lines) | `scripts/match_library.py REFERENCES.mgf QUERIES.mgf [--tolerance]` (verified on synthetic MGFs with assertions: tie -> 3, single -> 2a, no overlap -> 5) |
| SKILL.md MetFrag params heredoc + `java -jar` | `scripts/run_metfrag.sh JAR PEAKLIST CANDIDATES NEUTRAL_MASS SAMPLE [OUTDIR]` |

`examples/annotate_features.py` untouched (it does not duplicate the moved blocks: it uses argmax, not the tie loop).
