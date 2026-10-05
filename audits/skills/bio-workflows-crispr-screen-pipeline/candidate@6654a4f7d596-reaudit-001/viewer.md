> **Audit record for `bio-workflows-crispr-screen-pipeline`**
> - Audited working candidate `6654a4f7d596c13a76b5b68b0346c9f521335f10e4d4a38ae7b58e2f3067d6dc`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/workflows/crispr-screen-pipeline), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-04 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Re-audit: bio-workflows-crispr-screen-pipeline (final, full mode, reaudit-001)

Candidate 6654a4f7d596c13a76b5b68b0346c9f521335f10e4d4a38ae7b58e2f3067d6dc (uncommitted recut, 19 files; `skill_preflight --offline --shape` PASS). Category Data Analysis, mode D, Complex, 7 inputs.

Static 83/100 (x0.4 = 33.2); execution average 87.0 (x0.6 = 52.2); final 85. Layer 1 35.3, Layer 2 51.7. Assertions 25/28 (89.3%).

**Decision: not candidate-ready.** Research veto methodological_ground FAIL (F-12, P0); two first-table routing cases FAIL; assertion rate under 90%. Route to `fix-scientific-skill`.

## Routing check (routing/, model cli:claude-haiku-4-5-20251001, 3 repeats, identity printed 6654a4f7d596...)

| Route | Result |
|---|---|
| count | PASS 3/3 |
| qc | PASS 3/3 |
| cn-correction | FAIL 0/3 (rerun 0/3) |
| rra | FAIL 0/3 (rerun 1/3) |
| bagel2 | PASS 3/3 |
| mle | PASS 3/3 |
| drugz | PASS 3/3 |
| jacks | PASS 3/3 |
| chronos | PASS 3/3 |
| consensus | PASS 3/3 |
| branches | PASS 3/3 |

The rerun (routing-rerun/) covered only cn-correction and rra and is diagnostic; the first full run is the record. In every failing repeat the agent opened the right route first and then stopped to ask the user for the four commitments (baseline, control classes, screen type, CN profile) that the request or data already supplied; no command was issued (F-13). Cases file: copy of the lane file in scripts/routing-cases.json. Against the initial audit's copy: no request changed except cn-correction (", then three day-14 replicates" added), data dirs changed for cn-correction and rra, and allow_before added for cn-correction, rra, mle and jacks (F-15).

## Prior findings, as verified

| ID | Disposition |
|---|---|
| F-01 chronos snippet | Resolved. Extracted verbatim from routes/chronos.md, run against the standard NEGv1.txt (header GENE): exit 0, 5 x 4,502, 0 NaN, ribosomal mean -2.72 to -2.95. |
| F-02 jacks command | Resolved. Route command as written: exit 0, 4,502 x 5, RPL/RPS mean -1.04 to -1.83. |
| F-03 count column order | Resolved. Route states id, sequence, gene; 100% mapped, 240 guides x 4 samples. |
| F-04 rra routing | Not resolved under Haiku (0/3, rerun 1/3); cause now the confirmation rule, not qc-first (F-13). |
| F-05 cn-correction routing | Not resolved under Haiku (0/3, 0/3); same cause (F-13). |
| F-06 mle routing | Resolved, 3/3. |
| F-07 jacks routing | Resolved, 3/3. |
| F-08 cn-correction text and header | Resolved. cn_correction.R ran in WSL (90,709 guides, 0 NA, non-integer), guard for non-integer input exits 1. |
| F-09 qc.py silent plasmid | Resolved. WARNING prints first. |
| F-10 drugz paired, real drug screen | Open (deferred). |
| F-11 Skill-root LICENSE | Open (deferred; preflight warns). |

## New findings

- **F-12 P0** qc.py Gini gate uses the wrong statistic. See the QC-gate question below.
- **F-13 P1** Confirm-four-commitments rule halts the agent before the route command (cn-correction, rra).
- **F-14 P2** qc.py does not enforce the guides>25 and skew gates; skew<2 attribution unverified.
- **F-15 P2** Tooling delta edited the cn-correction request text and widened allow_before.

## The QC-gate question

Real HAP1 (plasmid Gini 0.288) and Project Score A375 (0.342) fail the 0.1 plasmid gate because `scripts/qc.py` computes Gini on raw counts, while the cited MAGeCK-VISPR gate (Li 2015, Table 1: Gini at most 0.1 for plasmid or initial-state samples, at most 0.2 for negative selection) is on the Gini `mageck count` reports. MAGeCK computes it on ln(count+1) (`mageckCount.py`, `nrdcnt += [math.log(cval+1.0)]`). On the same columns (scripts/gini_mageck_def.py):

| Sample | qc.py (raw) | MAGeCK (ln) |
|---|---|---|
| HAP1 T0 | 0.288 | 0.057 |
| HAP1 T18 A-C | 0.34-0.38 | 0.091-0.101 |
| Project Score plasmid | 0.342 | 0.089 |
| A375 endpoints | 0.46-0.48 | 0.155-0.174 |

Both "plasmid" columns pass 0.1 and all endpoints pass 0.2 on MAGeCK's own definition. The same disagreement is visible inside the Skill: `routes/count.md` sends the user to countsummary.txt (Plasmid 0.074) while qc.py reports 0.269 for that column. Two side findings: HAP1 T0 is not a plasmid pool (Hart 2017 G3: gDNA collected at day 0 after selection), so passing it as `plasmid=` is a labelling error by the staging README and by the Skill's "Day-0" baseline wording; and the endpoint gate 0.3 is looser than the cited 0.2. The Skill is at fault; the simulated QC-passing inputs were a workaround for a script bug, not evidence that real plasmids fail. The Project Score column's true provenance (library plasmid vs early sample) cannot be settled from the staged files and does not change the verdict, since it passes either way on the correct statistic. Replicate Pearson on HAP1 (0.789) still fails the 0.8 floor after the fix, as background.md already says.

## Execution map

| Surface | Class |
|---|---|
| count, qc (real, simulated, no-plasmid, normalized, bad-label), rra (real HAP1, qc-pass, guards), bagel2 (seeded twice), consensus (3, 2, 1 methods; real three-method inputs), mle, drugz (unpaired), jacks, chronos, cn-correction (WSL) | executed this run |
| cn_correction guide drop count (86,881 of 90,709) | reused (tooling-delta evidence, script body unchanged) |
| drugz paired mode, real drug screen | static-only (no staged data) |
| branches, references/install.md | not-applicable |

## Per-input scores

| # | Type | Label | Basic | Spec | Total |
|---|---|---|---|---|---|
| 1 | Canonical | HAP1: qc.py then rra.py | 35 | 48 | 83 |
| 2 | Variant A | BAGEL2 + consensus | 36 | 56 | 92 |
| 3 | Edge | count route | 36 | 52 | 88 |
| 4 | Variant B | cn_correction.R + rra on corrected | 35 | 52 | 87 |
| 5 | Variant B | mle, drugz -unpaired | 33 | 48 | 81 |
| 6 | Stress | jacks + chronos on the panel | 36 | 54 | 90 |
| 7 | Adversarial | guards and trap trips | 36 | 52 | 88 |

Evidence: run root `F:\OpenScience\fix-evidence\recut-crispr-pipeline\reaudit-001\` (native.log, chronos.log, cn.log, inspect_outputs.log, gini_mageck_def.log, routing/, routing-rerun/, work/).
