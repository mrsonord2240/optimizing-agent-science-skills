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


---

# bio-microbiome-functional-prediction — P2 batch fix, 2026-09-21

Branch `fix/microbiome-functional-prediction` off staging `main` @ `431aa55`, worktree
`F:\OpenScience\wt\microbiome-functional-prediction`. Commits: fix `37ff715`, scripts `ea6cfef` (see also git log on
the branch). Env `microbiome-metagenomics-analyst` (R via `rr.sh`, MicrobiomeStat 1.4, Python 3.12).
Audit at upstream `47a62df`: 90 Production Ready, 1 open P2.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `linda()` aborts the whole run on a predicted pathway table under the default `prev.filter = 0` | P2 | Added a `prev.filter = 0.1` caveat (checked on MicrobiomeStat 1.4) to the "DA without compositional correction" failure mode and a new Common Errors row | ran | Re-ran on the audit's fresh PICRUSt2 pathway table (503 pathways), gut vs left palm, 16 samples: `prev.filter = 0` -> "contrasts can be applied only to factors with 2 or more levels", no results; `prev.filter = 0.1` -> 34 features filtered, 469 fit; manual drop of rows with `rowSums(x > 0) < 2` then `prev.filter = 0` -> 469 fit (independent confirmation of the cause) |

Scripts pass (`refactor(...)` commit): SKILL.md "Report NSTI" inline Python block -> `scripts/nsti_report.py`
(args: PICRUSt2 output dir, ASV TSV, `--max-nsti`). Ran as SKILL.md invokes it on the audit's 751-ASV
PICRUSt2 2.6.3 output: mean NSTI 0.077, median 0.001, 3/751 dropped, 0.0% reads (matches the audit);
`--max-nsti 0.5` -> 13/751, 0.1%. `examples/run_picrust2.sh` still carries its own inline copy of the
NSTI logic as part of the whole-pipeline example; left untouched (`examples/` stays as is).

Redundancy pass: already done on 2026-09-19 (usage-guide.md holds only overview, prompts, related
Skills); nothing further to remove. Length: SKILL.md 204 -> 206 (fix) -> 196 lines (scripts); under
300, no split.

## Left unfixed

Nothing from this Skill's audit. Noted outside this Skill: `differential-abundance/examples/aldex2_analysis.R`
line 62 calls `linda(..., prev.filter = 0)`, the same setting that crashes here on sparse tables; that
Skill owns it.

## Deleted passage -> new home

| passage | new home |
|---|---|
| SKILL.md "Report NSTI" inline Python block | `scripts/nsti_report.py` (invoked from the same section) |
