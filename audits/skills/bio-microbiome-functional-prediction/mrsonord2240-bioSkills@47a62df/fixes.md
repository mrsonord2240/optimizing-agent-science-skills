# bio-microbiome-functional-prediction — fix pass, 2026-09-19

Branch `fix/mb-functional-pred` off staging `main` (`mrsonord2240/bioSkills` @ `7644996`),
worktree `F:\OpenScience\wt\mb-fp`. Commit `47a62df`.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| Mandatory NSTI snippet hardcodes `marker_predicted_and_nsti.tsv.gz`, which does not exist in real PICRUSt2 2.6.3 output | P1 | Fixed to `combined_marker_predicted_and_nsti.tsv.gz` in SKILL.md (Run the Pipeline output list, Report NSTI section + code, Common Errors row, Version Compatibility note) and `examples/run_picrust2.sh` | ran | Ran the corrected snippet against the audit's real 751-ASV PICRUSt2 2.6.3 output (`work/picrust2_out_real/combined_marker_predicted_and_nsti.tsv.gz`): reproduced the audit's exact numbers (mean NSTI 0.077, median 0.001, 3/751 ASVs dropped, 0.0% reads dropped) |
| Standard `biom convert --to-tsv` export crashes `picrust2_pipeline.py` after ~9 min of real compute, no warning in docs | P1 | Added an input-format trap note to SKILL.md's Run the Pipeline section and a new Common Errors row (strip the leading `# Constructed from biom file` line with `tail -n +2`, or pass `.biom` directly); added a matching comment to `examples/run_picrust2.sh` | ran | Reproduced the crash from the audit's own log (`differing number of fields` on the `# Constructed from biom file` first line). Confirmed `tail -n +2` on the raw biom export is byte-for-byte identical to the audit's working `asv_table_fixed.tsv`, whose full run (`picrust2_out_real`) is the same output validated above |
| "Report ≥2 CoDA tools, intersection" guidance silently returns an empty/wrong consensus because MaAsLin2 sanitizes MetaCyc IDs (hyphens→dots via `make.names()`) and ALDEx2 does not | P1 | Added a normalize-IDs-first note to the "DA without compositional correction" failure mode, a new Common Errors row, and the Quantitative Thresholds "DA: ≥2 CoDA tools" row | ran | Ran real ALDEx2 + MaAsLin2 (R env, real packages) on the audit's real 503-pathway PICRUSt2 output, gut(8) vs tongue(9) from the real moving-pictures metadata. Naive `intersect()` of raw hit names: 0. `intersect()` after `make.names()` on both sides: 160 (audit's own run reported 162 — same phenomenon, minor MC-sampling variance in ALDEx2) |
| Common Errors "near-empty output" row conflates post-hoc NSTI-drop with a hard `--min_align` placement abort (no output dir at all) | P2 | Split into two Common Errors rows with distinct symptoms/fixes | docs | Matches the audit's Input 3 finding directly; not independently re-run (tooling pass already reproduced the hard-abort case) |
| Frontmatter description promises "16S/ITS" support the body never substantiates (PICRUSt2 has no ITS/fungal reference) | P2 | Removed "/ITS" from the frontmatter `description` and from usage-guide.md's Overview | docs | No runtime to verify; textual-only claim removed per the audit's simpler fix option |

## Redundancy pass (required every fix, not audit-flagged)

`usage-guide.md`'s **Prerequisites**, **What the Agent Will Do**, and **Tips** sections restated
SKILL.md verbatim: mandatory NSTI reporting, activity-vs-potential framing, `--hsp_method mp`
default, ALDEx2 input shape, strain-level ceiling, and (in Tips) a second copy of the now-fixed NSTI
filename bug. All three sections deleted. The one fact unique to `usage-guide.md` — the
`conda create`/`conda install q2-picrust2` install commands — moved into SKILL.md's "Run the
Pipeline" section (it wasn't in SKILL.md before). `usage-guide.md` now holds only Overview, Quick
Start, Example Prompts, and Related Skills.

## Left unfixed

Nothing from the audit's P1/P2 list. Not attempted: broader ITS support (would require a different
reference database entirely — out of scope, the audit's own fix explicitly offered "remove the
claim" as the correct option here, not "add the capability").
