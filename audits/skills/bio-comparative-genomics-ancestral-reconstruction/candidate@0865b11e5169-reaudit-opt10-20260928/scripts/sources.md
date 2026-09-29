# Sources and provenance

## Candidate and prior-phase references

- Candidate tree: `F:\OpenScience\wt\opt10-ancestral-reconstruction\skills\bio-comparative-genomics-ancestral-reconstruction`.
- Canonical phase handoff and initial rejected report were read before testing. The original, fix-phase, and tooling-delta reference materials used to identify hypotheses are retained under `initial-evidence-reference/`, `fix-evidence-reference/`, and `delta-evidence-reference/` where copied.
- Current tool inventory: [`evidence/TOOLS.md`](evidence/TOOLS.md), copied from candidate `TOOLS.md` on the audit date.
- Current audit method package: `_method/skill-auditor/` from `skill-auditor.zip`, SHA-256 `E54E9FF8B0C3677ABCFE657AD6ED92BA34DBDB8AD205C7157AD881F25AFCF0DE`; relevant schema/rubric/veto documents preserved there.

## Official documentation checked

- PAML codeml example control file (documents `RateAncestor=1`, sequence type values): [PAML examples/codeml.ctl](https://github.com/abacus-gene/paml/blob/master/examples/codeml.ctl).
- IQ-TREE command reference (seed behavior and ancestral `.state` fields): [IQ-TREE Command Reference](https://iqtree.github.io/doc/Command-Reference).
- OUwie 3.0.3 reference manual (fitted-object `OUwie.anc`, `knowledge` argument and cautionary interpretation): [CRAN OUwie manual](https://cran.r-project.org/web/packages/OUwie/refman/OUwie.html).
- GRASP upstream source/readme: [bodenlab/GRASP](https://github.com/bodenlab/GRASP); exact runtime CLI help and artifacts are saved locally in `evidence/grasp-current/`.
- corHMM GitHub package metadata (version 2.10.5 and RTMB import): [corHMM DESCRIPTION](https://github.com/thej022214/corHMM/blob/master/DESCRIPTION). This version was inspected, not run or supported by the skill.

## Tools/environment

Runs used the prepared `science` WSL environment under its recorded boundary and current pinned tool inventory. Captured R package versions are in `evidence/r-sessionInfo.txt`; PAML, IQ-TREE, GRASP, and environment details are in `evidence/TOOLS.md`, `evidence/tooling-delta-reference/`, and run logs. No missing tooling was installed.
