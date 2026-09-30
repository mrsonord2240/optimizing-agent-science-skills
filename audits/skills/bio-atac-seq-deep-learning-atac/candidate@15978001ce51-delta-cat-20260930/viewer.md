> **Audit record for `bio-atac-seq-deep-learning-atac`**
> - Audited working candidate `15978001ce517f446bdd6f331a174092bb1d05fe18575cdd38d536d772ea4bd5`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/deep-learning-atac), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-deep-learning-atac`**
> - Audited working candidate `15978001ce517f446bdd6f331a174092bb1d05fe18575cdd38d536d772ea4bd5`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/deep-learning-atac), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-atac-seq-deep-learning-atac (delta re-audit)

Generated: 2026-09-30  
Audit type: independent delta re-audit (auditor did not make these changes; no candidate bytes edited)  
Exact candidate: sha256-manifest-v1 `15978001ce517f446bdd6f331a174092bb1d05fe18575cdd38d536d772ea4bd5` (10 files, 47,858 bytes), verified before and after execution. Carried forward from certified `3a9d1b4c...` (88/100, Production Ready).

## Result

**Final 89/100, Production Ready, candidate-ready.** Static 89 (x0.4 = 35.6), execution average 88.6 (x0.6 = 53.2), assertions 23/23. No veto. No open findings.

| Input | Type | Total /100 | Assertions | Change |
|---|---|---:|---:|---|
| 1 | Canonical (pipeline, RESUME, guards) | 88 | 5/5 | guard note updated; score carried |
| 2 | Variant A (log2FC) | 93 | 5/5 | carried |
| 3 | Edge (pred_bw, Enformer REF) | 88 | 4/4 | carried |
| 4 | Variant B (attributions, MoDISco) | 88 | 4/4 | carried |
| 5 | Stress (scBasset, Enformer, prerequisites) | 86 (was 84) | 5/5 (was 4/5) | prerequisites assertion now PASS |

Static changes: reliability 10 -> 11 (DLA-015), agent usability 14 -> 15 (DLA-016). Other six categories carried.

## Delta (shelf `3a9d1b4c...` -> candidate)

Exactly the listed changes; nothing else (`logs/identity_delta.log`):

- `SKILL.md`: frontmatter `category: Data Analysis`, `author: GPTomics`; env table `chrombpnet` row adds bedtools and UCSC `bedGraphToBigWig` (conda `bedtools`, `ucsc-bedgraphtobigwig`).
- `scripts/chrombpnet_pipeline.sh`: header now cites SKILL.md step 6; step 0 loops over `chrombpnet bedtools bedGraphToBigWig`.

All files LF; frontmatter parses as YAML; `marketplace_manifests.skill_category` accepts `Data Analysis`.

## Finding dispositions

| ID | Disposition | Evidence |
|---|---|---|
| DLA-015 P2 | Resolved | `logs/step0_tools.log`: the unmodified candidate script, run under `env -i` in WSL `science` (user `sci`). All three present: step 0 passes and the next guard fires (`missing input: atac.dedup.bam`). A single filtered-PATH shim withholding each tool in turn: rc=1, `<tool> not on PATH (activate the chrombpnet env)`, under 0.1 s, no files created. Both bedtools and bedGraphToBigWig withheld: reports bedtools first. `logs/static_checks.log`: both packages are in the env's conda-meta (bedtools 2.31.1, ucsc-bedgraphtobigwig 482), and chromBPNet's call sites (`CHROMBPNET.py` `os.system("bedtools ...")`, `reads_to_bigwig.py`) confirm the need. |
| DLA-016 P2 | Resolved | `logs/static_checks.log`: SKILL.md step 6 is "Motifs" (attributions, `contribs_bw`, MoDISco); the header now says step 6. The only other pointer (`tool-decision-tree.md` -> step 8, footprinting) is correct. |
| DLA-001..014 | Carried closed | Bytes on every other surface are unchanged. |

## Caveats

- The Skill's `chrombpnet` env is realised here as micromamba env `dlatac-tf` (TOOLS.md). No env is literally named `chrombpnet`.
- The WSL system has its own `/usr/bin/bedtools`. A first attempt that kept `/usr/bin` on PATH masked the withheld tool. The logged test puts one shim dir on PATH, holding every env and `/usr/bin` binary except the withheld ones.
- Nothing was trained or re-run beyond step 0; all other execution evidence is carried from the certified run with the same environment fingerprint (`06fc2798...`).

Scripts: `scripts/dc_identity_delta.py`, `dc_step0_tools.sh`, `dc_static.sh`, `dc_build.py`, `dc_identity_after.py`, `validate_report.py` (the prior run's, unchanged; `logs/schema_validation.log` ok).
