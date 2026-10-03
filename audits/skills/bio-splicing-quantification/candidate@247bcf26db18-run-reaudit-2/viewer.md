> **Audit record for `bio-splicing-quantification`**
> - Audited working candidate `247bcf26db1833bc443dc9d651595ef84068f43a2593067f7c3bda72bd7e7adc`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/alternative-splicing/splicing-quantification), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) delta re-audit worker D2, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-splicing-quantification

Generated: 2026-10-03
Audit type: independent delta re-audit (text-only change to certified bytes), lane D2
Exact candidate content SHA-256: `247bcf26db1833bc443dc9d651595ef84068f43a2593067f7c3bda72bd7e7adc` (5 files, 42306 bytes; `skill_preflight --offline` PASS before and after, candidate bytes untouched)
Certified baseline: `0c0354add99b` (85, Production Ready), record `candidate@0c0354add99b-run-reaudit-1`
Scores carry forward from the certified report; only the dimension and assertions touched by the change were re-scored.

## Result

**Static 84/100; Execution average 86.4/100; Final 85.4 (85); assertion pass rate 35/37; Layer 1 34.9/40; Layer 2 51.6/60.**
Grade: Production Ready. Skill veto PASS; Research veto PASS. Decision: candidate-ready for exact identity `247bcf26db18`. The margin over the 85 gate remains narrow.

## Delta qualification

- Per-file sha256 against the certified source-identity: `references/failure-modes-and-errors.md`, `references/intron-retention-and-microexons.md`, `scripts/quantify_splicing.py` and `usage-guide.md` are byte-identical; only `SKILL.md` differs (23344 to 23571 bytes). No script or executable statement changed.
- Reversing the single SQ-13 sentence on a scratch copy reproduces SKILL.md sha256 `899e98ff...b622f` exactly, so the whole diff is that one sentence.
- The SKILL.md python block was re-run verbatim on the real rMATS JC output: 958 SE events, 20 reliable, rc 0 (scripts/rd_snippet_and_forms.py).

## Changed claim versus measured values

| Claim in new text | Measured (real chrX JC SE, rMATS 4.4.0, readLength 75; planted readLength 50) | Verdict |
|---|---|---|
| maxima 2*(readLength-1) and readLength-1; 98/49 at 50, 148/74 at 75 | planted 98/49; real max IncFormLen 148, max SkipFormLen 74 | correct |
| 719 of 958 chrX SE rows are 148/74 | 719 of 958 (58 distinct pairs) | correct |
| use the per-event lengths in each row | formula with row lengths reproduces IncLevel, maxabs 0.0005 over 1465 values (JC), 1549 (JCEC) | correct |
| JCEC adds exon-body positions (149 for the 100 nt planted exon) | planted JCEC 149/49 | correct, unchanged |
| PSI = (IJC/IncFormLen)/(IJC/IncFormLen + SJC/SkipFormLen) | same reproduction | still correct |
| maxima "reached only for exons at least read-length long; short exons shorten them" | SkipFormLen 74 in 958/958 rows incl. a 1 nt exon; a 74 nt exon gives 148; 710 exons of at least 75 nt all give 148 | inexact (SQ-14) |

## Finding dispositions

| ID | Verdict |
|---|---|
| SQ-13 | resolved: constants claim replaced by maxima plus per-event guidance |
| SQ-14 (P2, new, text only) | open: condition clause is inexact for SkipFormLen and off by one for IncFormLen |
| SQ-12 (P2) | open, untouched: header-only rMATS file raises KeyError in parse_rmats_output (script unchanged) |

All other certified dispositions (SQ-01 to SQ-11) are unchanged; no other part of SKILL.md changed.

## Not executed

Unchanged from the certified record: MAJIQ V3/VOILA, VAST-TOOLS, Shiba, MicroExonator, S-IRFindeR, iREAD, IRFinder-S 2.0; the Skill labels each as not executed. The IRFinder smoke was not run (not needed for a prose change).

## Evidence

Run root `F:\OpenScience\audits\bio-splicing-quantification\run-reaudit-2\` (scripts/rd_snippet_and_forms.py, logs/rd_snippet_and_forms.log). The rMATS outputs of `run-reaudit-1\out` were reused as inputs (Skill scripts and rMATS version unchanged).
