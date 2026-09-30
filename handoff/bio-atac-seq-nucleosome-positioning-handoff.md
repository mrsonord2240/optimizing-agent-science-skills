# Handoff: bio-atac-seq-nucleosome-positioning / fix-scientific-skill

- Updated: 2026-09-30
- Lane: 5
- Status: ready-for-phase
- Owner leaving: audit-scientific-skill worker (lane 5)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/nucleosome-positioning
- Working tree: `F:\OpenScience\wt\atac-nucleosome-positioning\skills\bio-atac-seq-nucleosome-positioning`
- Branch/worktree: `fix/atac-nucleosome-positioning`, starting commit 3186916 (uncommitted candidate)
- Candidate tree hash: `sha256-manifest-v1 ce9a8a0618678bc71ab7afa41b98c37beab513e9b0c599d5a83197d31b879cd7` (7 files; re-verified live after audit; no `__pycache__`; Skill unmodified)
- Applicable audit: `F:\OpenScience\audits\bio-atac-seq-nucleosome-positioning\initial-audit-20260930\report.json` (identity above; not yet published to records)

## Completed this phase

- Initial audit: score 57, Reject (research veto M4 FAIL); static 65, execution avg 52.0, assertions 12/23. Diagnostic, not certification.
- Ran V-plot, NRL, R/ATACseqQC (verbatim + scratch-patched), NucleoATAC run, py3.7 pip recipe, DANPOS3 differential on a planted +40 bp pair.
- Diagnosed the empty NucleoATAC `nucpos` (NUCPOS-006): uninitialised accumulator in `calculateCov` gives NaN z-scores.
- Record: `report.json`, `viewer.md`, `findings.json`, `source-identity.json`, `scripts/`, `logs/`, `out/` in the audit dir; report validated against the pinned schema (P0/P1/P2 only, sorted).

## Required next actions

1. Fix P0 first: NUCPOS-001 (`estimate_nrl.py`, distance in bins + guard), NUCPOS-002 and -003 (`nucleosome_analysis.R`: `readBamFile(asMates=TRUE)`, load ChIPpeakAnno). A tested patched R copy is `scripts/a2_patched_nucleosome_analysis.R` in the audit dir.
2. Then P1: NUCPOS-004/-005 (`vplot.py` centre and strand), NUCPOS-006/-007 (NucleoATAC py2.7 install, nucpos non-empty check, execute any workaround such as a source build with `value = 0` before documenting it).
3. Then P2 NUCPOS-008 to -013 and P3 NUCPOS-014, -015; rerun the affected surfaces; classify tooling impact (R env needs ChIPpeakAnno already present).

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| NUCPOS-001 | P0 | open | `logs/a1_py_checks.log` | fix estimate_nrl peak spacing and empty-result guard |
| NUCPOS-002 | P0 | open | `logs/a2_r_script.log` | fix shift input in R script |
| NUCPOS-003 | P0 | open | `logs/tooling_probe_fas.log` | load ChIPpeakAnno, update install |
| NUCPOS-004 | P1 | open | `logs/a1_py_checks.log` | correct fragment centre |
| NUCPOS-005 | P1 | open | `out/a1_vplot_compare.png` | strand-aware V-plot |
| NUCPOS-006 | P1 | open | `logs/na_debug_z.log`, `logs/na_cov_probe2.log` | document/test workaround, add check |
| NUCPOS-007 | P1 | open | `logs/a5_pip_install.log` | correct install recipe and Python claims |
| NUCPOS-008 | P2 | open | `logs/a2_check_bams.log` | apply MAPQ filter consistently |
| NUCPOS-009 | P2 | open | `logs/a2_r_script.log` | TSS set filtering, heatmap check |
| NUCPOS-010 | P2 | open | `logs/a4_danpos.log` | name DANPOS columns |
| NUCPOS-011 | P2 | open | `logs/tooling_danpos_dpos_help.txt` | update DANPOS install/executable |
| NUCPOS-012 | P2 | open | Skill references | cite or drop claims |
| NUCPOS-013 | P2 | open | `SKILL.md`, `usage-guide.md` | replace unverified-version caveats |
| NUCPOS-014 | P3 | open | `logs/a1_py_checks.log` | vplot.py output hardening |
| NUCPOS-015 | P3 | open | `TOOLS.md` | scPrinter example or removal |

Deferred/static-only: scPrinter and single-cell route (no command); whole-genome scale (data are chr1:1-30 Mb, ~0.5M pairs); H2A.Z ground truth.

## Environment and evidence

- Tool inventory: `F:\OpenScience\audits\bio-atac-seq-nucleosome-positioning\TOOLS.md` (sha256 `fdbc099f2395d3116692305b8ecae9249a3a639f5128e1741b8b90e2be743925`)
- Environment fingerprint: `0972fade33110926b7f703a40c83aaf07b4072b4ef027cde196890e22f08f866`; rubric zip sha256 `e54e9ff8b0c3677abcfe657ad6ed92ba34dbdb8ad205c7157ad881f25afcf0de`
- Run evidence: `F:\OpenScience\audits\bio-atac-seq-nucleosome-positioning\initial-audit-20260930\`; rerun via `F:\OpenScience\audit-envs\bio-atac-seq-nucleosome-positioning\wsl_env.sh`
- Minor repair: none (no audit-local edits)
- Restricted-access items: none
- Tooling impact: none (audit used prepared envs; shared envs read-only; scratch work under `audit-envs\...\work\{a2,a3,a4}`)

## Worktree safety

- Run-owned changes: `F:\OpenScience\audits\bio-atac-seq-nucleosome-positioning\initial-audit-20260930\`, this handoff
- Pre-existing/user-owned changes (untouched): `F:\optimizing-agent-science-skills\tools\run_mercury_worker.py`, `tools\test_run_mercury_worker.py`
- Records state: uncommitted; not published (orchestrator publishes)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
