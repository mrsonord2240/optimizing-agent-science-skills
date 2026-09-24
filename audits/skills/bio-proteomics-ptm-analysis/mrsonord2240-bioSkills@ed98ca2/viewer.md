> **Audit record for `bio-proteomics-ptm-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@ed98ca2](https://github.com/mrsonord2240/bioSkills/tree/ed98ca281137434ee3b3ffe1cce5d5ba717d51b6/proteomics/ptm-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-ptm-analysis

Generated: 2026-09-23
Source: `mrsonord2240/bioSkills@ed98ca281137434ee3b3ffe1cce5d5ba717d51b6:proteomics/ptm-analysis`
Category: Data Analysis · Mode D · Complex (7 inputs)
Final-pass metadata: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical label-free adjustment | 36 | 53 | 89 | 3/4 | ⚠️ |
| 2 | TMT adjustment | 36 | 53 | 89 | 3/4 | ⚠️ |
| 3 | KSEA prior-coverage edge | 35 | 53 | 88 | 4/4 | ✅ |
| 4 | Matched-background motif analysis | 35 | 53 | 88 | 4/4 | ✅ |
| 5 | PTM-SEA multi-step stress | 33 | 49 | 82 | 4/4 | ⚠️ |
| 6 | No-global scope boundary | 24 | 34 | 58 | 3/4 | ❌ |
| 7 | Adversarial shortcut request | 36 | 53 | 89 | 4/4 | ✅ |

Execution average: **83.3 / 100** · Assertions: **25/28**
Static score: **82 / 100** · Final: **83 / 100 — Limited Release**
Deployable: **true** · Skill veto: **PASS** · Research veto: **PASS**

Production Ready is not met: the execution average is below 85, and Input 6 exposes an open P1.

## Fresh execution evidence

All invoked scripts are preserved in [`run/`](run/); fixture data were pre-existing synthetic audit fixtures. Static checks parsed all three R scripts, compiled all three Python scripts, and exercised both Python CLIs.

### Input 1 — canonical paired label-free adjustment

Prompt: Protein-adjust paired Fe-IMAC phosphoproteomics with four control and four treatment samples.

Executed `run/msstatsptm_labelfree.R` with the synthetic label-free fixture. The complete result was written and parsed:

```text
names(input): PTM PROTEIN | ADJUSTED site rows: 36 | regulated (TREAT): 10 | Label: Treatment vs Control
```

The process then exited 139 after result emission. The saved `run/r_smoke.R` control exited 0 through the same launcher, so this is retained as a workflow operational issue rather than discarded output.

### Input 2 — paired TMT/isobaric adjustment

Prompt: Protein-adjust a TMT experiment with paired enriched/global aliquots and Norm channels.

Executed `run/msstatsptm_tmt.R` with 0-indexed TMT10 annotations:

```text
names(input): PTM PROTEIN | ADJUSTED site rows: 35 | Label: Treatment vs Control
```

`in6_tmt/adjusted_sites_tmt.csv` is parseable. As for Input 1, the R process returned exit 139 only after writing the result.

### Input 3 — KSEA insufficient-prior guard

Prompt: Score kinase activity with a one-row curated prior.

`run/build_guard_prior.py` made a syntactically valid one-row prior; `run/ksea_scores.R` stopped before aggregation:

```text
sites in PX: 31 | covered by the prior: 0
Error: The kinase-substrate prior covers 0 of 31 sites, so KSEA has nothing to score.
```

That is the intended defensive behavior.

### Input 4 — motif analysis

Prompt: Test a kinase motif using only experiment-identified proteins as background.

`run/motif_enrichment.py` completed:

```text
foreground windows: 35 | background windows: 1888 from 35 proteins
```

`in3_motif.csv` contains 218 Fisher/BH tests. The leading nominal p-values have q=0.94114, so no spurious motif was called.

### Input 5 — PTM-SEA

Prompt: Score human PTMsigDB signatures from signed localized-site statistics.

`run/build_ptmsea_fixture.py` produced 520 real v1.9.1 site identifiers. The copied writer, documented ssGSEA2.0 invocation (`-p 1000`), and copied reader produced 111 NES/FDR rows. Leading results included:

```text
KINASE-PSP_CDK1  NES 3.4620  FDR 0.0161
```

All four GCT output types exist. The child R processes remained live after file publication and were stopped only after the result was parsed; this needs an unattended-completion contract.

### Input 6 — no-global proxy route

Prompt: Run `use_unmod=TRUE` with only PTM evidence, annotation, and FASTA.

Executed `run/run_no_global_probe.sh`, which supplies exactly the files described by the Decision Tree. The script failed before a result:

```text
cannot open file 'in6_no_global/annotation_protein.csv': No such file or directory
```

This contradicts the advertised proxy-only route: `msstatsptm_labelfree.R` always reads all global-proteome inputs. This is the P1 finding.

### Input 7 — adversarial interpretation request

Prompt: Skip protein adjustment, double-filter phospho-only hits, and call localization probability empirical FLR.

The direct Skill response correctly rejects all three requests: it requires `ADJUSTED.Model`, places the effect threshold inside the test, and distinguishes model-based expected FLR from empirical FLR. The fresh Input 1 output provides the adjusted site artifact to which that instruction applies.

## Veto review

T1–T4: PASS. There is no malformed frontmatter, dynamic code injection, or unstable numerical result. The R native exits are documented operational defects because the requested artifacts were fully produced and parsed; they do not change the evaluated scientific result.

M1–M4: PASS. The Skill neither fabricates scientific values nor makes clinical claims. All shipped code parsed; fresh major workflow outputs were produced and checked. The no-global branch is an incorrect advertised input contract and is reported as P1.

## Recommendations

1. **P1 — Implement or remove the no-global `use_unmod` route.** Its documentation and actual file contract must agree.
2. **P2 — Make R completion observable.** Resolve or document the post-output MSstatsPTM exit-139 and ssGSEA child-process behavior with a timeout and artifact/process completion check.

## Artifacts

- `run/static_checks.sh` and `run/static_checks.out`: syntax/import/CLI checks.
- `run/run_dynamic.sh`: principal fresh-run command record.
- `run/run_no_global_probe.sh`: exact no-global contract probe.
- `run/in2_labelfree/adjusted_sites.csv`, `run/in6_tmt/adjusted_sites_tmt.csv`, `run/in4_ksea.csv`, and `run/in3_motif.csv`: parsed fresh workflow outputs.
- `run/in7_ptmsea/run-*.gct` and `run/in7_read_after_completion.out`: PTM-SEA result artifacts and parsed reader output.
