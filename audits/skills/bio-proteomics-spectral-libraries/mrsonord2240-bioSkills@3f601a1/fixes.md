# bio-proteomics-spectral-libraries fixes (2026-09-19)

Worktree `F:\OpenScience\wt\pt-speclib`, branch `fix/pt-speclib`, off fork `main` (`d91ed3d...` lineage).
Runtime: `F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\` -- deeplc 4.5.0 / ms2pip 4.2.0 /
psm_utils (`tools\ms2pip-deeplc-venv\`), OpenMS 3.5.0 (`tools\openms\bin\`), pyteomics 5.0.1.
Audit: `F:\OpenScience\audits\bio-proteomics-spectral-libraries\` (87, Production Ready, deployable,
0 P0, 3 P1, 2 P2).

## Findings

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| OpenSwathDecoyGenerator's real data requirements undocumented | P1 | New paragraph + runnable snippet in SKILL.md "Convert Library Formats": literal `Annotation` column and real theoretical fragment m/z (`pyteomics.mass.fast_mass`) are both required; placeholder `ProductMz` converts cleanly but yields 0 decoys. New "OpenSwathDecoyGenerator silently generates 0 decoys" entry under Per-Method Failure Modes, and a Common Errors row | ran: reproduced the audit's own failure on `TargetedFileConverter`+`OpenSwathDecoyGenerator` 3.5.0 with placeholder m/z (0 decoys, "below the threshold of 80.0%"), then success with the audit's `input4_library.tsv` (real y-ion m/z + `Annotation`) -- "Number of target peptides: 2 / decoy peptides: 2" | |
| Shuffle decoy generation non-deterministic, no documented seed control | P1 | Same SKILL.md section states `-method shuffle` has no seed flag and is non-reproducible; recommends `-method reverse` or `-method pseudo-reverse` instead; new Common Errors row; `-method shift` explicitly called out as broken (see Unfixed/notes) | ran: diffed two `-method shuffle` runs on identical TraML -> byte-level differences (matches audit); diffed two `-method reverse` and two `-method pseudo-reverse` runs -> 0-line diff each, both fully deterministic | `--helphelp` confirms no seed option exists anywhere in the tool |
| Reference DeepLC snippet stale against deeplc 4.5.0 (`DeepLC` class removed) | P1 | Replaced the class-based comment in `examples/build_library.py` line 17 and the equivalent lines in SKILL.md (Version Compatibility, overview bullet, Common Errors row) with the real module-level API: `deeplc.predict_and_calibrate(pred_psms, psm_list_reference=cal_psms)` via `psm_utils.PSM`/`PSMList`; also corrected the modification-notation claim (ProForma `Peptidoform`, not MS2PIP `location\|name`) | ran: full working script against deeplc 4.5.0 -- calibration on 11 IRT_PEPTIDES anchors, `predict_and_calibrate` returned real RT values for held-out peptides; `build_library.py` re-run end-to-end, unchanged output | `deeplc.calibrate()`+`deeplc.predict()` separately does NOT compose (`predict()` has no `calibration=` kwarg) -- `predict_and_calibrate()` is the correct one-shot call, used instead |
| MS2PIP first-run model retrieval can hang, no documented workaround | P2 | Investigated: this is a real Skill-level gap, not purely an environment quirk. Added a Common Errors row and a usage-guide.md Prerequisites note: default `model='HCD'` (=HCD2021) downloads two XGBoost files to `~/.ms2pip` on first use -- 66MB + **847MB** (confirmed via HTTP `Content-Length`, not the ~small size assumed) -- with no progress bar, no timeout, and no resume on interruption | ran: HEAD requests confirmed exact file sizes; a clean single-process `predict_batch(model='HCD')` run was still downloading after 4m40s (not stuck, just large+slow, ~1.4MB/s measured); `predict_batch(model='HCD2019', model_dir=<fresh dir>)` completed end-to-end in 44s with real per-fragment intensities returned, proving the mechanism itself works | root cause: reasonable person reads "Model hash not recognized." followed by silence and assumes a hang; it is a ~915MB silent download. Documented pre-fetch / smaller-model workarounds instead of treating it as a code defect |

## Also fixed while in the area (drift found during verification)

- `Common Errors` row for `ImportError: cannot import name Predictor from ms2pip` was already
  correct; left untouched.
- Version Compatibility header updated to name exact checked versions (koinapy 0.0.11, ms2pip
  4.2.0, deeplc 4.5.0) instead of open-ended "0.0.5+/4.0+/3.0+", since the 3.0+ deeplc floor was
  the direct cause of the stale-API finding.

## Unfixed / left as documentation

- `OpenSwathDecoyGenerator -method shift` is listed as an option by `--helphelp` but rejected
  every peptide as a duplicate in testing on this OpenMS 3.5.0 build (`shift` leaves the
  amino-acid sequence unchanged, and the tool's own target/decoy identity check then treats the
  unchanged sequence as "already present"). This looks like an OpenMS-side defect or
  version-specific quirk, not something this Skill can work around; documented as "do not rely
  on it" rather than recommended, since `reverse`/`pseudo-reverse` already cover the
  deterministic-decoy need with no caveats.
- Did not restructure Prerequisites/Tips between SKILL.md and usage-guide.md beyond the new
  findings -- no pre-existing duplication was found between the two files for this Skill, so the
  "remove redundancy" pass had nothing to collapse.

## Commit

`fix(proteomics/spectral-libraries): document OpenSWATH decoy requirements, decoy determinism, deeplc 4.5 API, ms2pip model download`
