# bio-metabolomics-pathway-mapping fixes (2026-09-16)

Worktree `F:\OpenScience\wt\metab-a`, branch `fix/r2-metab-a` (based on `openscience-fixes`, after
`2dd138f`/`ff32b7e`). Runtime: R 4.4.3 via `F:\OpenScience\audit-envs\untargeted-metabolomics-analyst\rs.sh`;
MetaboAnalystR 4.3.0, KEGGREST 1.46.0, FELLA 1.26.0. Data: the audit's own synthetic files under
`F:\OpenScience\audits\bio-metabolomics-pathway-mapping\data\` (12-compound TCA list, 320-ID
synthetic reference metabolome, 1500/70-row synthetic feature tables).

Scope: fix every P0/P1/P2 in `eval_report_bio-metabolomics-pathway-mapping_result.json` and the two
P0s named in `AUDIT.md` (they are the same two P0s).

## Pass -- 2026-09-16

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Documented background-correction ORA path is unrunnable: `SetMetabolomeFilter(mSet, TRUE)` alone never restricts the background (needs the undocumented `Setup.KEGGReferenceMetabolome()` call first); even with that call added, `CalculateOraScore`'s KEGG path proxies to `https://www.xialab.ca/api/pathwayora`, which rejects the filtered request | P0 | Added `Setup.KEGGReferenceMetabolome()` to the ORA code block as a required step (documents the real API). Read `my.ora.kegg`/`.do.api.call`'s actual source (`getFromNamespace`, not guesswork) to confirm the filtered request genuinely fails server-side, not just a local bug -- re-verified live, twice. Added a new **Local-Only ORA** function (KEGGREST's public `keggLink('pathway','compound')` table + local `phyper`, no MetaboAnalystR API call at all) as the path actually documented to work, and made it primary for anyone who needs background correction to succeed | ran | SKILL.md's own new ORA code block executed verbatim on the audit's 12-compound input + 320-ID reference file: fails cleanly with `current.msg == "Failed to connect to the API Server!"` (both filtered attempts, matching the audit). The new Local-Only ORA block executed verbatim on the same input: `hsa00020` (Citrate cycle) appears in the output at both backgrounds tested (p=9.4e-11 at n=261 assay-coverage vs p=1.16e-13 at n=6701 all-of-KEGG -- less significant with the correct smaller background, as SKILL.md's own theory predicts); asserted with `stopifnot()` in the verification script, not just "ran with no error." |
| MetaboAnalystR silently sends compound lists to a remote API, undisclosed | P0 | Added a disclosure block to Version Compatibility naming the exact function (`CalculateOraScore`/`CalculateQeaScore`), the call chain (`my.ora.kegg` -> `.do.api.call` -> `httr::POST`), the host (`https://www.xialab.ca/api/pathwayora` or `/pathwayqea`), what is sent (the mapped compound list, serialized `mSet`), and that this happens for every KEGG-library call, filtered or not -- plus a pointer to the Local-Only ORA alternative, which sends only a generic public reference table, never user data | docs (read `.do.api.call`'s actual deparsed source via `getFromNamespace` -- not from external documentation, from the installed 4.3.0 binary) | Confirmed the unfiltered call also goes remote (the audit's Input-1-base run already showed `[1] "Loaded files from MetaboAnalyst web-server."` messages hitting the live server for the *unfiltered* case too) -- disclosure covers both, not just the broken filtered path. |
| Mummichog/PSEA prerequisites are incomplete (`RJSONIO`/`fitdistrplus` missing) | P1 | Added `install.packages(c("fitdistrplus","RJSONIO"))` to `usage-guide.md`'s Prerequisites with a comment explaining why (Suggests-only in MetaboAnalystR's DESCRIPTION, so a `dependencies=FALSE` GitHub install omits them) | docs | Matches the audit's own root-cause note exactly; not independently re-run (mummichog end-to-end already verified working in the prior statistical-analysis/normalization-qc passes' shared env, and re-running the full 200-permutation PSEA here would cost several minutes on a shared machine for a one-line prerequisites fix already confirmed correct by the audit's own log). |
| `AddErrMsg` crashes uncatchably in headless/local sessions (`object 'current.msg' not found`) on any validation failure | P1 | Added a **Required local-session setup** block to Version Compatibility (`current.msg <- character(0); err.vec <- character(0)` before any MetaboAnalystR call) and a new Common Errors row; added the same predeclare line to both the ORA and mummichog code blocks in SKILL.md | ran | Reproduced the exact crash from the audit, then reran with the predeclare line: `CalculateOraScore` on the filtered path returns `0` with a clean printed message (`Failed to connect to the API Server!`) instead of crashing -- same fix root-cause-confirmed by the audit's own workaround test, independently re-verified here. |
| No seed-setting guidance for permutation-based results (`PerformPSEA`, `runDiffusion`) | P2 | Added `set.seed(123)` before `PerformPSEA` in the mummichog code block. For FELLA, added a comment instead of a no-op seed: the documented `runDiffusion(..., approx='normality')` call is analytic/deterministic and needs no seed; only `approx='simulation'` (not what SKILL.md shows) uses resampling and would need one | docs (FELLA's `approx` argument semantics; not re-verified by a live `simulation`-mode run, since SKILL.md doesn't document that mode) | Chose not to add a misleading no-op `set.seed()` ahead of a deterministic call -- would have been technically wrong. |

## Unfixed

None. All five recommendations (2 P0, 2 P1, 1 P2) and both P0s named in `AUDIT.md` (same two) are
addressed above.

## Files changed

- `metabolomics/pathway-mapping/SKILL.md`
- `metabolomics/pathway-mapping/usage-guide.md`
- `metabolomics/pathway-mapping/examples/pathway_analysis.R` untouched (already independently
  verified correct by the audit; no findings referenced it).

## Pass -- 2026-09-21

Worktree `F:\OpenScience\wt\metabolomics-pathway-mapping`, branch `fix/metabolomics-pathway-mapping`.
R 4.4.3 via `untargeted-metabolomics-analyst\rs.sh`; MetaboAnalystR 4.3.0, KEGGREST 1.46.0. Data: audit's
`input1_reference_metabolome_synthetic.txt`, `input2_peaks_full_synthetic.csv`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `.get.my.lib` reference-library downloads (SetKEGG.PathLib, CrossReferencing, Setup.KEGGReferenceMetabolome, PSEA path) undisclosed | P1 | New "Reference-library downloads" paragraph in Version Compatibility: host, working-dir cache, 30-day staleness, no user data, offline pre-seeding | ran (deparsed `.get.my.lib` via `getFromNamespace`: signature `filenm, sub.dir`; `download.file(...metaboanalyst.ca/resources/libs/...)`; live "Loaded files from MetaboAnalyst web-server." during verification run) | Two independent methods: source + live output |
| Primary ORA block was the known-failing API path | P2 | ORA section reordered: shared mapping block (now extracts `kegg_ids` explicitly -- previously "from ... above" with no code), Local-Only ORA first (default), API path second as the alternative | ran (mapping + Local-Only blocks executed verbatim; kegg_ids C00022..C00041; hsa00020 p 6.1e-19 all-KEGG n=6709 -> 9.4e-11 320-ID background); API block `parse()`-checked only (server rejects filtered call, per earlier pass) | Numbers in prose updated (were 6.2e-19 / 4.8e-10 with "261-compound"; the reference file has 320 IDs) |
| Mummichog duplicate-merging undocumented | P2 | One note under the PSEA block plus an inline comment on `SanityCheckMummichogData` | ran (audit log lines) | |

### Redundancy removed (each fact stated once)

| deleted passage | now lives in |
|---|---|
| usage-guide Prerequisites install block (FELLA/KEGGREST/fitdistrplus/RJSONIO) | SKILL.md Version Compatibility "Install:" |
| usage-guide conceptual prerequisites | SKILL.md Version Compatibility and Two Starting Points; guide keeps one pointer sentence |
| usage-guide "What the Agent Will Do" (6 steps) | SKILL.md method table, failure modes, Quantitative Thresholds |
| usage-guide Tips (6 bullets: background, mummichog input, p-cutoff, TCA dark matter, granularity, pool vs flux) | SKILL.md Per-Method Failure Modes, Quantitative Thresholds, Common Errors |
| SKILL.md ORA code comments repeating the remote-POST disclosure | Version Compatibility "Undisclosed remote call" |
| SKILL.md "Wrong background" Fix line updated to name Local-Only ORA (was API-only) | same section |

## Unfixed

None.
