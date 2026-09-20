# bio-blast-searches fixes (2026-09-19)

Worktree `F:\OpenScience\wt\db-blast`, branch `db-blast`, based on staging `main` @ `a93661e`.
Fixer: Claude Opus 5 (1M context). Runtime: shared venv `F:\OpenScience\audit-envs\database-access\
Scripts\python.exe`, `biopython==1.88` (no install needed). Commit: `664c664`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| SKILL.md's "Short peptide search" pattern (PAM30, no `gapcosts`) crashes: NCBI defaults gap costs to BLOSUM62's (11,1), which PAM30 rejects | P1 | Added `gapcosts='9 1'` to the code pattern, matching the Skill's own word-size/gap-cost table; added a Common Errors row for the exact NCBI error text | ran | Live `qblast()` call against real NCBI (12-aa hemoglobin-beta peptide fragment, `swissprot`, PAM30, word=2, CBS=3): confirmed succeeds with `gapcosts='9 1'`, 100 alignments returned, top hits real hemoglobin-beta Swiss-Prot records at E~9 (permissive range as documented). Independent of the audit's own run (different peptide, same fix) |
| `megablast`/`dc-megablast` documented as `program=` values; `NCBIWWW.qblast()` only accepts blastn/blastp/blastx/tblastn/tblastx -- the real form (`program='blastn', megablast=True`) was undocumented anywhere in the Skill | P1 | Added a new "Requesting megablast / dc-megablast" code pattern with the real form (plus `template_type`/`template_length` for dc-megablast) and a note under the Program table pointing at it; added a Common Errors row for the exact NCBI `ValueError` text | ran | Live `qblast()` call against real NCBI (`program='blastn', megablast=True`, human HBB partial CDS, `refseq_select_rna`): confirmed succeeds, 5 alignments (human + 2 mouse), matching the audit's own result (5 vs. 11 for plain blastn on the identical query) |
| Missing FASTA defline documented as producing `record.query=None`; audit found the real placeholder is the string `'No definition line'` plus a confirmed 12.7x latency penalty (781s vs. 61.6s), undocumented | P1 | Corrected the Failure Modes symptom to the real placeholder string and the latency penalty; added a defline pointer to Required Setup and a Common Errors row ("Stuck > 5 min" now names a missing defline as a cause) | docs (audit's own live evidence, not re-run) | Per dispatch instructions, did not re-run the ~13-minute slow path; the fix states the audit's confirmed numbers (781s vs 62s) rather than re-deriving them |
| Failure Modes' megablast cross-species "zero hits" symptom overstated -- a real query found 2 of 3 species, not zero | P2 | Softened the symptom to "reduced or missing cross-species hits, worse for more diverged sequences -- not necessarily zero," citing the audit's 2-of-3 result | docs (audit's own live evidence) | Cheap, folded into the same Failure Modes edit as the P1 above |
| No `references/` split despite genuine quantitative content (Karlin-Altschul derivation, CBS mode table) | P2 | Added `references/statistics.md`: moved the full E-value formula/table and CBS mode table there, leaving condensed decision-relevant summaries + pointers in `SKILL.md`. Matches the precedent in `alignment/alignment-trimming/references/` elsewhere in this corpus (no `database-access` sibling had one) | n/a (doc restructure) | Also folded in the Rost 1999 "twilight zone" note, previously only in `usage-guide.md`, as new reference content rather than dropping it |

All 5 dispatched findings fixed (3 P1, 2 P2). Nothing left unfixed. Nothing needs Sam.

## Redundancy pass (2026-09-19)

Scope: `SKILL.md` and `usage-guide.md`, per the brief's "Remove redundancy, every pass" rule (not
separately flagged by the audit beyond the missing-`references/` P2).

**Deleted passage -> new home:**

| Deleted from usage-guide.md | New home | Note |
|---|---|---|
| "What the Agent Will Do" 8-step list (program/db/word-size/CBS/hitlist_size/entrez_query/XML-parse/bit-score choices) | `SKILL.md`'s Program decision, Database decision, and Code patterns sections (already there) | Replaced with a one-line pointer |
| Tips bullet 1 (bit-score vs E-value) | `SKILL.md`'s E-value interpretation section (already there, now condensed there) | Verbatim restatement, no new fact |
| Tips bullet 2 (dc-megablast vs megablast) | `SKILL.md`'s Program decision table + Failure Modes (already there) | Verbatim restatement |
| Tips bullet 3 (profile methods for marginal E) | `SKILL.md`'s E-value interpretation section (already there) | Verbatim restatement |
| Tips bullet 4 (`entrez_query` pre-filter) | `SKILL.md`'s "Protein search with organism restriction" pattern (already there) | Verbatim restatement |
| Tips bullet 5 (nt/nr reproducibility) | `SKILL.md`'s Database decision table (already there) | Verbatim restatement |
| Tips bullet 6 (>5/min, >1000-sequence thresholds) | `SKILL.md`'s opening paragraph, merged alongside its existing >50-sequence threshold | Genuinely new numbers (not in `SKILL.md`), moved rather than dropped -- not a contradiction, a finer-grained two-step escalation (>50 -> local-blast, >1000 -> DIAMOND/MMseqs2) |
| Tips bullet 7 (Rost 1999 twilight zone) | `references/statistics.md` (new) | New content, moved not dropped; also added the citation to `SKILL.md`'s References list |
| Tips bullet 8 (CBS/SEG) | `SKILL.md`'s Composition-Based Statistics section (already there) | Verbatim restatement |

Untouched: "Overview", "Prerequisites", "Quick Start", "Example Prompts", "Related Skills" -- the
brief's allowed usage-guide.md categories. `usage-guide.md`: 74 -> 59 lines. `SKILL.md`: 312 -> 339
lines (net +27: three P1 fixes/notes, one P2 sentence, minus the E-value/CBS content moved to
`references/`).

Shipped `examples/*.py` were not touched -- none of the three (`basic_blast.py`,
`blastp_filtered.py`, `save_and_parse.py`) exercises the PAM30 or megablast patterns (confirmed by
the audit-env `TOOLS.md`'s tooling notes), so no P1 applies to them, and no unrelated defect was
found in them during this pass.
