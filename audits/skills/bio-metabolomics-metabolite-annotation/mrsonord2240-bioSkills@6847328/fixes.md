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
