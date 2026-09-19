# bio-protac-degraders fixes (2026-09-19)

Worktree `F:\OpenScience\wt\cg-protac`, branch `fix/cg-protac`, off fork `main`
(`F:\OpenScience\external\mrsonord2240__bioSkills`). Fresh audit at 90/Production Ready,
deployable, no P0, 1 P1 + 2 P2 open. Runtime: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\`
(RDKit 2026.03.6, numpy 2.5.3, scipy 1.18.1, Python 3.12.13). Commit `bfcde6d`.

## Findings

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `primary_tool` (PRosettaC) and every named ternary predictor (DeepTernary, AlphaFold3, Boltz-1/2, HADDOCK) are unexecutable locally -- web service, licence-gated, or GPU/weights-gated | P1 | Added an explicit per-tool "how to invoke" table to SKILL.md's "Ternary Complex Prediction Tools" (submission URL/account, turnaround, what you get back) so these read as external/manual steps, not something this Skill runs. Replaced the dead pseudo-code in "Ternary Complex Modeling Workflow" (`predict_ternary()` returning an undefined `ternary_poses`) with the real local step (linker-reach screening) vs. the external step (structure prediction). Wrote `examples/ternary_geometry_screen.py`: a pure-RDKit conformer-based linker-reach screen implementing the Skill's own pre-existing but unimplemented `attachment_distance()`/"sample conformers, retain candidates without severe strain" text | ran: all 11 named linkers screened; monotonic-reach-vs-chain-length and all-trans-zigzag-theoretical-bound assertions both pass at runtime; `py_compile` clean; runs correctly both from the `examples/` dir and from repo root | Chose "reframe as external" (per fix brief's own guidance for this case) over inventing a fake local ternary predictor; the one thing genuinely installable and already RDKit-scoped (linker geometry, already documented in SKILL.md) was written, not a new tool the Skill never mentioned |
| No shipped example for cooperativity-alpha / DC50/Dmax/hook-effect workflows | P2 | Added `examples/cooperativity_dc50.py`: `cooperativity_alpha()` (SKILL.md's `Kd_binary/Kd_ternary` formula) and a 3-parameter Hill DC50/Dmax fit with hook-effect flagging (>15pp downturn) and ascending-arm-only fitting when a hook is flagged | ran: alpha correctly labels positive/negative/no cooperativity on 3 synthetic Kd pairs; seeded synthetic bell-shaped curve correctly flagged hook-affected; ascending-arm fit recovers the curve's own planted DC50 (40 nM, 10.7% relative error) and Dmax (80%, 7.4pp absolute error) -- checked against known generating parameters, not just exit code | matches audit's suggested fix almost exactly |
| Version Compatibility pin (RDKit 2024.09+) stale vs. audited RDKit 2026.03.6 | P2 (cosmetic) | Same Version Compatibility edit now states the shipped scripts were checked on RDKit 2026.03.6, keeping 2024.09+ as the documented floor via the existing introspect-and-adapt escape hatch | n/a (doc-only, "cheap" per brief) | |

## Redundancy pass (applied on this touch, not audit-flagged)

- Deleted usage-guide.md's "Tips" section: 5 of 6 bullets restated SKILL.md verbatim (E3 choice
  criteria -> E3 Ligase Choice; linker-length guidance -> Linker Design Principles;
  cooperativity -> Cooperativity (Alpha); hook effect -> DC50/Dmax Characterization;
  permeability -> "Insufficient cell permeability" failure mode). Each fact's only home is now
  its existing SKILL.md section.
- The 6th bullet (linker-enumeration dummy attachments must be single-bond) existed only in
  usage-guide.md but documents `build_protac()`'s real, agent-relevant error contract -- moved
  into SKILL.md's Common Errors table as a new row, not deleted.
- usage-guide.md Prerequisites: dropped the three external-tool `pip install` placeholder
  comments (misleading -- none of PRosettaC/DeepTernary/AlphaFold3 actually installs that way)
  in favor of a one-line pointer to SKILL.md's new invocation table.

## Unfixed

None. All 3 findings (1 P1, 2 P2) addressed.
