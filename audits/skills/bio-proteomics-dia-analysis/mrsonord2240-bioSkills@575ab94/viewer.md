> **Audit record for `bio-proteomics-dia-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@575ab94](https://github.com/mrsonord2240/bioSkills/tree/575ab946989a7029d235eb0ab711e47b08edbcb0/proteomics/dia-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Skill Audit Viewer — `bio-proteomics-dia-analysis` (re-audit)

**Date:** 2026-09-15 · **Source:** `mrsonord2240/bioSkills@575ab946989a7029d235eb0ab711e47b08edbcb0:proteomics/dia-analysis`
**Pre-fix report:** `F:\OpenScience\audits\_pre-fix-20260915\bio-proteomics-dia-analysis\` (2026-09-11 — static 77, execution 77.2, final 77, ⚠️ Beta Only, not deployable)

| | Pre-fix (2026-09-11) | Re-audit (2026-09-15) |
|---|---|---|
| Static | 77 | **85** |
| Execution average | 77.2 (N=5) | **87.0 (N=7)** |
| Assertions | 16/23 (69.6%) | **30/34 (88.2%)** |
| Final | 77 ⚠️ Beta Only | **86.2 ✅ Limited Release** |
| Deployable | no | **yes** |

Raw 86.2 maps to ⭐ Production Ready; the assertion pass rate (88.2%) is below the 90% floor, so the grade is downgraded exactly one tier. Every other floor is met (static 85 ≥ 80, execution 87.0 ≥ 85, Layer 1 36.0 ≥ 32, Layer 2 51.0 ≥ 48).

**Category:** 3 — Data Analysis. **Execution mode:** A (the agent writes code and commands by following the Skill's patterns). **Complexity:** Moderate → N = 5 by the complexity rule; 7 were run (5 pre-fix inputs as regression + 2 new public-data inputs).

---

## Environment

DIA-NN 2.6.1 Academia · ProteoWizard msconvert 3.0.26253 · EasyPQP 0.1.59 · Sage 0.14.6 · pyOpenMS 3.5.0 · pandas 3.0.5 · numpy 2.5.3
(`F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\`)

**Data.** *Synthetic* (labelled as such everywhere): an 8-run DIA-NN-style `report.parquet` with 60 `LOWCONF` groups that pass run-level q-values but fail `Global.PG.Q.Value`; a seeded 600-run cohort report (3,046,139 rows, 142 MB); a 252-spectrum staggered-window mzML built for this audit. *Public:* PXD070049 (CC0, Van Puyvelde et al. 2026) — Orbitrap Astral 5-min 250 pg HYE benchmark, three DIA and three DDA `.raw` plus the HYE FASTA, using the **submitter** SDRF. One replicate per condition, so within-condition CV is not computable from it and no assertion depends on one.

---

## Veto gates

**Skill veto (T1–T4): PASS.** The filter block completed on every dataset (23k rows, 3.05M rows, two real DIA-NN reports) with no crash and no loop; repeated runs give identical matrix shapes and counts. The example script quotes its `--f` arguments and exits 1 on an empty directory. No injection surface.

**Research veto (M1–M4): PASS.** References real and correctly cited; the checkable quantitative claims were checked against a public benchmark with a known ground truth. No diagnostic, prescriptive or triage content. The q-value level/context method is sound and was confirmed at 8 and 600 runs. Code ran as written in all seven inputs.

---

## Input 1 — Canonical: predicted-library route → 1% FDR protein matrix ✅ 87/100 (5/6 assertions)

The Skill's filter block, run verbatim (only the parquet path substituted):

```python
report = pd.read_parquet('diann_out/report.parquet')  # NOT report.tsv on 1.9+
filt = report[(report['Q.Value'] <= 0.01) &
              (report['PG.Q.Value'] <= 0.01) &
              (report['Global.Q.Value'] <= 0.01) &
              (report['Global.PG.Q.Value'] <= 0.01)]
pg = filt.pivot_table(index='Protein.Group', columns='Run', values='PG.MaxLFQ', aggfunc='first')
pg = np.log2(pg.replace(0, np.nan))
```

```
report rows 23020 | runs 8 | groups 947
filtered rows 20170 | matrix (887, 8) | -inf 0 | NaN cells 589 (8.3%)
run-level-only groups: 947 | LOWCONF surviving run-level-only: 60 | LOWCONF surviving Skill filter: 0
groups >=3 valid in both conditions: 803 of 887 | absent in one condition: 26
```

The Skill's `diann` command was then run with the **real DIA-NN 2.6.1 binary** on the three public Astral DIA runs, verbatim apart from the file paths, the Skill's own Astral mass accuracies (10/4) and `--threads`:

```
Mass accuracy will be fixed to 1e-05 (MS2) and 4e-06 (MS1)
WARNING: incorrect settings, the in silico-predicted library must be generated in a separate
pipeline step and then used to process the raw data, now without activating FASTA digest
...
[49:25] Saving the library to diann_out/report-lib.predicted.speclib
[50:49] File #1/3
ERROR: hostfxr init failed: 0x80008096      <- environment, not the Skill (.NET 8 absent)
```

Two things fall out of this. **Every flag was accepted** — DIA-NN 2.6.1 names unrecognised options in its log (a deliberate `--help` produced `WARNING: unrecognised option [--help]`) and named none of the Skill's 23. And **the command form itself is wrong for 2.x**: DIA-NN says the prediction must be its own pipeline step. That is the P1 below. The `.raw` read failure is this machine's missing .NET 8, unrelated to the Skill; the run was repeated against msconvert-produced mzML and completed (Input 6).

The Skill's example script was exercised against a stub `diann` in three cases: a normal two-run directory (exit 0, 40 argv entries), a filename containing a space (`run A.mzML` arrived as **one** argument — the pre-fix word-splitting defect is fixed), and an empty directory (`No .mzML files in ...`, exit 1).

**FAIL:** the one-command predicted-library route on DIA-NN 2.x.

## Input 2 — Variant A: cohort matrix and the matrix-vs-report count ⚠️ 86/100 (4/5)

The global filter does its job (0/60 `LOWCONF` survive versus 60/60 under a run-level-only filter) and `Global.Q.Value` — the pass-1 P2 — is now in the block.

The count guidance, however, is inverted for this version. On real 2.6.1 output:

```
protein groups: report run-level filter 4376 | report + global (Skill b03) 4375 | report.pg_matrix.tsv rows 4440
Skill claim 'matrix count can be LOWER than the report count' holds here: False
```

Confirmed twice (pandas `nunique` = 4440; `wc -l` = 4441 lines with header). DIA-NN 2.6.1's own log calls the matrices *"1% precursor and protein group FDR"* and never mentions `--matrix-spec-q`. The Skill tells the agent the matrix will be smaller and to "not panic" — which would make the agent explain a real discrepancy backwards.

**FAIL:** matrix-vs-report explanation.

## Input 3 — Edge: staggered overlapping windows ✅ 90/100 (4/4)

The pre-fix audit could not judge this: its synthetic staggered file had 5 spectra and msconvert aborted with *"Too few spectra to determine the number of precursor windows"*. A proper file was built for this re-audit — 12 cycles × (1 MS1 + 20 MS2), 8 Th physical windows, odd cycles offset by 4 Th (`rerun/in3_make_staggered.py`, synthetic).

The Skill's command, filters verbatim:

```bash
msconvert staggered_cycles.mzML --mzML \
  --filter "peakPicking vendor msLevel=1-" \
  --filter "demultiplex optimization=overlap_only massError=10ppm" -o demux
```

```
[SpectrumList_PeakPicker]: one or more spectra have undeclared profile/centroid status, assuming profile data
writing output file: demux\staggered_cycles.mzML
exit=0

input  : MS levels {1: 12, 2: 240} | isolation widths(Th) {8.0: 240} | distinct centres 40
demuxed: MS levels {1: 12, 2: 480} | isolation widths(Th) {4.0: 480} | distinct centres 41
```

8 Th → 4 Th, 240 → 480 MS2 scans: exactly the Amodei-2019 halving the Skill describes. The ordering advice was tested too, by running the same two filters **in the reverse order**:

```
[SpectrumList_PeakPicker] Warning: vendor peakPicking requested, but peakPicking is not the first
filter. Since the vendor DLLs can only operate directly on raw data, this filter will likely not
have any effect.
```

Both pre-fix FAILs on this input are now demonstrated PASSes rather than asserted ones. The "DIA-NN handles overlapping windows natively, demultiplexing is optional" claim stays documentation-checked: the public Astral data is not staggered (20.01 Th windows stepping 20.005 Th — abutting, not interleaved).

## Input 4 — Variant B: EasyPQP empirical library ⚠️ 77/100 (3/4)

The rewritten route is real. `easypqp 0.1.59 --help` confirms `convert` takes `--pepxml --spectra --psms --peaks`, and `library`'s own help documents its positional inputs as *"PSM and Peak pickle files generated from an `easypqp convert` command"* — the missing step that made the pre-fix snippet exit 1. A library was then built from the three real Astral DDA runs:

```
In total 7063 PSMs loaded.
2327 modified peptides identified (q-value < 0.01)
977 proteins identified (q-value < 0.01)
RT alignment: overlap with reference 469 / 1111 / 562 peptides
Library successfully generated.
```

Deviation from verbatim: no pepXML exists here (the DDA search used Sage), so `convertsage` stood in for `convert`, and the FragPipe artefacts the Skill's step 2 names (`psm.tsv`, `peptide.tsv`, `irt.tsv`) are absent — without them the same binary built the library successfully.

The remaining defect is what the Skill does **not** say: the EasyPQP `library.tsv` was not loadable by DIA-NN 2.6.1 until `FragmentCharge`, `FragmentType` and `FragmentSeriesNumber` were added by hand. The Skill's caveat ("compatibility should be verified") does not name the failure an agent will actually hit.

**FAIL:** third-party-library caveat too vague to act on.

## Input 5 — Stress: 600-run cohort ✅ 90/100 (5/5)

```
SYNTHETIC cohort report: rows 3046139 | runs 600 | groups 4000 | MB 142.4
Skill block: 1.5 s | matrix (2000, 600) | -inf 0 | missing 17.2%
false (FALSE*) groups in matrix: 0
per-run groups: median 1667, MAD 43, min 1541, max 1771, flagged (>3 MAD low): 0
```

The large-cohort decision-tree row now matches DIA-NN's guidance (empirical library from 20–100 high-quality runs, search all runs with it, MBR off, fixed mass accuracies, filter on `Global.*`) — the pre-fix FAIL is fixed. Nothing in the output diagnoses or triages an individual.

## Input 6 — New, public data: predicted-library route end to end ✅ 91/100 (5/5)

Real DIA-NN 2.6.1 output from the Skill's own route (prediction step, then search against the predicted library — the two-step form P1 asks the Skill to document), run on the three Astral DIA mzML.

```
real DIA-NN 2.6.1 report | rows 46485 | runs 3
columns the filter needs -> all 9 present (incl. Global.Q.Value, Lib.PG.Q.Value)
[b03 verbatim] OK in 0.1 s | matrix (4375, 3) | -inf 0 | NaN 1715
Skill-listed output files present: all 5
species of protein groups: HUMAN 2975, YEAST 937, ECOLI 421, OTHER 40, MIXED 2
A/B log2 | HUMAN n=2489 median +0.02 (exp +0.00) | YEAST n=753 +1.04 (exp +1.00) | ECOLI n=233 -1.77 (exp -2.00)
C/A log2 | HUMAN n=2466 median -0.02 (exp +0.00) | YEAST n=486 -3.22 (exp -3.32) | ECOLI n=238 +2.43 (exp +2.68)
```

The Skill's route recovers the known three-species mixing design. Ratio compression at the E. coli end is expected at a 250 pg load and is not a Skill defect. The Skill's note that a predicted library lands as `*.predicted.speclib` regardless of `--out-lib` was confirmed exactly.

## Input 7 — New, public data: library-based route ✅ 88/100 (4/5)

The Skill's `b02` command with the EasyPQP library from Input 4 (fragment columns added) against the same three runs:

```
DIA-NN report | rows 4851 | runs 3
[dia-analysis b03] verbatim block OK | matrix (771, 3) | -inf 0 | NaN 12
all 786 protein-group accessions present in the shipped FASTA (0 unmatched); genes filled 4845/4851 rows
A/B log2 | HUMAN n=542 -0.04 (exp 0) | YEAST n=126 +0.98 (exp +1.00) | ECOLI n=92 -1.92 (exp -2.00)
C/A log2 | HUMAN n=542 +0.03 (exp 0) | YEAST n=122 -3.33 (exp -3.32) | ECOLI n=91 +2.65 (exp +2.68)
```

Smaller library, fewer groups, ratios if anything closer to truth. `--fasta` alongside `--lib` annotates as the fix claims.

**FAIL:** same third-party-library caveat gap as Input 4.

---

## What pass 1 fixed, verified by execution

| Pre-fix finding | Priority | Now |
|---|---|---|
| easypqp library snippet fails as written | P1 | **Fixed** — two-step route; a library was built from real DDA data |
| Staggered-window guidance overstated and incomplete | P1 | **Fixed** — command demultiplexes 8 Th → 4 Th, exit 0; reversed order reproduces pwiz's own warning |
| Mass-accuracy advice contradicts DIA-NN docs | P1 | **Fixed** — fixed per-instrument values; 10/4 accepted and echoed back by 2.6.1 |
| Large-cohort route diverges from DIA-NN guidance | P1 | **Fixed** — matches the docs; 600-run run clean |
| Report filter omits `Global.Q.Value` | P2 | **Fixed** — present and exercised |
| Library-based route lacks FASTA and caveat | P2 | **Fixed for `--fasta`** (0 unmatched accessions); caveat still too vague (new P2) |
| Version drift in output and default claims | P2 | **Partly** — `.parquet`, `--qvalue` default and naming fixed; output listing and matrix-count claim still drifted |
| Example script fragile, missing promised filter | P2 | **Fixed** — three smoke cases pass |

## Open recommendations

- **P1** — Split the predicted-library route into the two commands DIA-NN 2.x requires; add a Common Errors row for the `incorrect settings` warning.
- **P1** — Replace the inverted matrix-vs-report count claim with a version-aware statement and point at `report.log.txt`.
- **P2** — Name the three fragment-annotation columns DIA-NN needs from a TSV library that EasyPQP does not write.
- **P2** — Extend the output-file listing with the five files 2.6.1 also writes.
- **P2** — De-duplicate the DIA-NN command between `SKILL.md` and `examples/`, and ship a tiny synthetic `report.parquet` so the filter block is self-testing.

## Evidence on disk

`F:\OpenScience\audits\bio-proteomics-dia-analysis\rerun\` — `blocks/` (Skill code extracted verbatim), `in12_filter.py/.out`, `in5_cohort.py/.out`, `in3_make_staggered.py`, `stagger/` (`demux_skillcmd.out`, `demux_reversed.out`, `check_demux.out`), `in6_public_predlib.py/.out`, `public_hye_check.py`, `public_libbased.out`, `check_annot.py/.out`, `easypqp_help.out`, `diann_2.6.1_help.txt`, `smoke/`, `msconvert_synth/`.
Real DIA-NN runs: `F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\public-work\` (`diann_libfree`, `diann_predlib_mzml`, `diann_libbased_mzml`, `sage/easypqp`).
