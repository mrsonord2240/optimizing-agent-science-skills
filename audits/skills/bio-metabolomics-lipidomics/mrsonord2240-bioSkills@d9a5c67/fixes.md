# `bio-metabolomics-lipidomics` — fix record (2026-09-16)

Commit: `def23f4` on `fix/r2-metab-b` (worktree `F:\OpenScience\wt\metab-b`).
Scope: Sam's 2026-09-16 override — fix all four open findings for this Skill.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| Goslin honest-downgrade (`get_lipid_string(LipidLevel.MOLECULAR_SPECIES)`) raises unhandled `RuntimeException` for names parsed at or below `SPECIES` (sum composition, ether, plasmalogen) | P1 | Capped the requested target level at `min(MOLECULAR_SPECIES, claimed_level)` in the "Honest Annotation-Level Assignment" code block; added a Common Errors row | ran | pygoslin 2.2.5. Reproduced the crash on the audit's exact 7 names first (4/7 crashed, matching `eval_viewer`), then re-ran with the guard: 0/7 crash, each honest string correct (`PC P-34:1` sum-composes to `PC O-34:2`, demonstrating the Skill's own ether/plasmalogen mass-degeneracy point as a side effect) |
| `normalize_istd()` silently divides by factor=1 (no correction) for a class with zero recognized internal standards | P2, but treated as the dangerous one per Sam's instruction — a silent no-op must become loud | Read `lipidr:::normalize_istd` source directly (`if (length(istd_list[[i]]) == 0) f <- 1`) confirming the mechanism; added a pre-check (`table(Class, istd)`, `stop()` naming any zero-coverage class) to the Class-Based Internal-Standard code block, before the `normalize_istd()` call | ran | lipidr 2.20.0. On the audit's synthetic data (TG, LPC lack a standard): guard correctly `stop()`s naming both. On lipidr's own bundled `data_normalized` (9/9 classes covered): guard finds zero uncovered classes — no false positive |
| lipidr's importer can't parse the `;O2`/`;O1`/`;O3` sphingoid suffix this Skill's own hierarchy table documents; a name like `Cer 18:1;O2/16:0` imports with `Class = NA` and silently drops from every downstream step | P2 | Added a conversion snippet (`;O1`→`m`, `;O2`→`d`, `;O3`→`t` prefix) before the Load/Normalize code block, plus a Common Errors row | ran | lipidr 2.20.0 (`.clean_molecule_name()` inspected directly — no `;O#` match at all). Before: `Cer 18:1;O2/16:0` → `Class=NA`. After conversion → `Cer d18:1/16:0` → `Class="Cer"`, real `as_lipidomics_experiment()` call on the audit's synthetic CSV. Also spot-checked HexCer/SM and all three O-levels (m/d/t) |
| No explicit practice-boundary statement; the correct refusal of a patient-diagnosis question (audit Input 7) relied on general model judgment, not Skill content | P1 | Added a "Practice Boundaries" section: research/analytical use only, not clinical diagnosis, redirect patient-level questions to a clinician; also notes the sn-ratio-as-diagnosis premise is analytically unsound under CID regardless | docs | Matches the audit's own observed-correct refusal; now backed by SKILL.md content |
| Shipped example `normalize_istd(data_normalized, ...)` crashes with `"Area is already normalized"` — `data_normalized` ships PQN-normalized and `normalize_istd()`'s own `.prenormalize_check()` refuses already-normalized data | P1 (shipped example crashes — FIX_BRIEF scope; not one of the four audit findings, added per Sam's fix-every-known-deficiency instruction, commit `7327bfe`) | Swapped `data_normalized` for a fresh, un-normalized `LipidomicsExperiment` built from lipidr's own shipped raw Skyline export (`extdata/A1_data.csv`, `F1_data.csv`, `F2_data.csv` + `clin.csv`) | ran | Confirmed pre-existing by running the unmodified code from `git show HEAD~2` (fails identically). Ran the fixed block end to end: `normalize_istd()` completes (279 lipids x 56 samples), the ISTD-coverage guard finds 0 uncovered classes (real data, full 9/9-class coverage, no false positive), `plot_lipidclass(d_istd, 'sd')` renders and saves a real non-empty PNG (65861 bytes) — checked output content, not exit code |

## Unfixed

None.

---

# 2026-09-21 fix pass (P2 batch)

Branch `fix/metabolomics-lipidomics` (worktree `F:\OpenScience\wt\metabolomics-lipidomics`, from staging `431aa55`). Commits: `41ca37c` fix, `bfa3712` redundancy, `f84e29f` scripts. SKILL.md 251 -> 203 lines (under 300, no split needed). Env `untargeted-metabolomics-analyst`: R 4.4.3, lipidr 2.20.0, pygoslin 2.2.5.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| istd-coverage guard misses Class=NA rows (`table()` drops NA) | P2 | explicit `is.na(Class)` check before the `table()`; drops the rows with a warning naming them (a hard `stop()` would have broken the shipped example, since lipidr's own bundled export has one NA row) | ran | Reproduced 1/279 (`PI 34:1p`, rowname 82) on lipidr's bundled raw export; after the fix `normalize_istd` completes 278 x 56; coverage guard still stops naming `LPC` when the LPC standard is removed from the input |
| No detection for un-converted `;O#` names | P2 | post-import Class=NA check that warns naming each row and, when `;O` remains, says to run `to_lipidr_sphingoid()`; Common Errors row updated | ran | Audit synthetic table plus `Cer/SM ;O2` and `HexCer ;O1` rows: unconverted -> 4 flagged with the hint; converted -> 0 NA, classes Cer/HexCer/SM |

## Left unfixed

None.

## Scripts (FIX_BRIEF "Runnable code goes in scripts/")

| old location | new home | run |
| --- | --- | --- |
| SKILL.md Load/Normalize: `to_lipidr_sphingoid()` + Class=NA check | `scripts/lipidr_import_checks.R` | CLI and `source()` on the synthetic table, assertions on flagged/converted rows |
| SKILL.md ISTD block (raw load, NA drop, coverage guard, `normalize_istd`, plot) | `scripts/istd_normalize.R` | bundled data (278 x 56, CSV + PNG), explicit-args run (byte-identical CSV), LPC-standard-removed run (stops naming LPC) |
| SKILL.md Goslin block | `scripts/honest_level.py` | 7 names incl. sum-composition, ether, plasmalogen: 0 exceptions |
| SKILL.md `de_analysis` block | deleted, duplicated `examples/lipidomics_workflow.R` (pointer left) | example run, exit 0 |

## Redundancy pass: deleted passage -> new home

| deleted | new home |
| --- | --- |
| usage-guide Prerequisites (BiocManager, pip, inputs) | SKILL.md header bullet "Install: ... Inputs: ..." |
| usage-guide Tip "identified-lipid count is a vanity metric" | SKILL.md, end of Honest Annotation-Level Assignment |
| usage-guide Tip "single-software IDs need orthogonal validation (ECN/RT, second adduct, CCS, MS/MS)" | SKILL.md Quantitative Thresholds, ~half row |
| usage-guide Quick Start, What the Agent Will Do, other Tips | already in SKILL.md (hierarchy, thresholds, failure modes, Version Compatibility); deleted |
| SKILL.md pygoslin code comment (verified on four names) | Common Errors `RuntimeException` row |
| SKILL.md ISTD comments (factor=1, cross-class ratios) | prose bullets under Class-Based Internal-Standard Quantification; the guard text also lives in `scripts/istd_normalize.R` |

Noticed: `examples/lipidomics_workflow.R` prints `NA` among the lipid classes (the same unparsed `PI 34:1p`); harmless there, left as is.
