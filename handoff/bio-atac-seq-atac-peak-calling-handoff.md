# Handoff: bio-atac-seq-atac-peak-calling / fix-scientific-skill

- Updated: 2026-09-30
- Lane: 1
- Status: ready-for-phase
- Owner leaving: audit-scientific-skill agent (Sonnet 5.5)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills @ d91ed3d563019e649dc854c56ccd62551359488a : atac-seq/atac-peak-calling
- Working tree: F:\OpenScience\wt\atac-atac-peak-calling (skills\bio-atac-seq-atac-peak-calling)
- Branch/worktree: fix/atac-atac-peak-calling (starting 3186916)
- Candidate tree hash: sha256-manifest-v1 e8bc49ba345f27792466c23bfee96faa4898937641d32bd266c7e58f0f3a7658 (5 files; re-verified after audit, unchanged)
- Applicable audit: F:\OpenScience\audits\bio-atac-seq-atac-peak-calling\initial-audit-20260930\report.json (same identity). Score 76, Beta Only, no veto, static 75, execution avg 76.4, assertions 14/21. Not published to records repo yet (orchestrator does it).

## Completed this phase

- Static review of all 5 files; 5 executed workflows (script, MACS3/MACS2, Genrich, hmmratac, NFR/blacklist/bigWig) with independent assertions; report.json validated by scripts\validate_report.py (schema checklist, P0-P2 only).
- Key result: script pseudoreps share 50% of reads; disjoint pseudoreps give ratios 1.09-1.16 (pass) vs script 2.066.
- Findings ledger: initial-audit-20260930\findings.json; viewer.md, source-identity.json, scripts\, out\ alongside.

## Required next actions

1. Fix ATACPC-001, -002 together in scripts\call_atac_peaks.sh plus SKILL.md, usage-guide.md and method-reference.md wording: disjoint pseudoreps (`samtools view -s SEED.5 -o a -U b`), per-rep and pooled pseudoreps, one IDR threshold, rescue = Np/Nt, self = N1/N2, pass/borderline/fail. Recheck with scripts\a2_disjoint_pseudoreps.sh (expect Nt 1197, N1 1143, N2 1249, Np 1036).
2. ATACPC-003 install line (conda-forge + bioconda, idr with numpy<1.24 separate env) and ATACPC-004 macs binary variable defaulting to macs3 (tooling delta pass needed for the idr env if instructions change).
3. ATACPC-005 to -011: genome-size default/comment, validation claim, blacklist/final outputs, Genrich name-sort command and q advice, hmmratac command/outputs, ENCODE-exactness wording, single-sample -q.
4. P3 ATACPC-012 (ROSE), -013 (quoting) at fixer discretion.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| ATACPC-001 | P1 | open | out\a1.log, out\a2_disjoint_pseudoreps.log | disjoint pseudoreplicates |
| ATACPC-002 | P1 | open | out\a1.log, out\a2_disjoint_pseudoreps.log | ENCODE ratios (N1,N2,Np,Nt) |
| ATACPC-003 | P1 | open | evidence\dryrun_documented_install.log | solving install; idr numpy pin |
| ATACPC-004 | P2 | open | out\a4_misc_snippets.log | macs3 default / binary var |
| ATACPC-005 | P2 | open | script line 9; method-reference lines 27-34 | genome size default and comment |
| ATACPC-006 | P2 | open | SKILL.md, script | add validation or drop claim |
| ATACPC-007 | P2 | open | out\a1.log | final blacklisted set / bigWig or state QC-only |
| ATACPC-008 | P2 | open | out\a3_genrich_checks.log | tested Genrich command, fix -q advice |
| ATACPC-009 | P2 | open | evidence\check_callers.log | hmmratac command, output names |
| ATACPC-010 | P2 | open | method-reference line 132 | ENCODE-style wording or --call-summits |
| ATACPC-011 | P2 | open | method-reference 98-104, 191 | one -q; cite or remove rotation method |
| ATACPC-012 | P3 | open (static-only) | method-reference 121-128 | GFF step or mark illustrative |
| ATACPC-013 | P3 | open | script | quote variables |

Deferred/blocked surfaces: ROSE (not installed), HOMER/nf-core/chromap/khmer (prose only), whole-genome and mm10 runs, bigWig signal readback.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-atac-seq-atac-peak-calling\TOOLS.md (sha256 86d6679d9ffe162870f2c94965c50f2ae62d42b1d115749efadbe694b07edc25); env fingerprint 08bd20dfc98af31b1acf5751fd307372decbc33017586ea9a5e80e8677a902b6
- Run evidence: F:\OpenScience\audits\bio-atac-seq-atac-peak-calling\initial-audit-20260930\ (report.json, findings.json, viewer.md, source-identity.json, scripts\, out\) and ...\evidence\
- Run with `MSYS_NO_PATHCONV=1 wsl.exe -d science -u sci --cd /home/sci -- bash /mnt/openscience/audits/.../scripts/<x>.sh`
- Restricted-access items: none
- Tooling impact: none from audit; fix may change idr/macs install (tooling delta pass)

## Worktree safety

- Run-owned changes: F:\OpenScience\audits\bio-atac-seq-atac-peak-calling\initial-audit-20260930\; run outputs under F:\OpenScience\audit-envs\bio-atac-seq-atac-peak-calling\run\{disjoint,genrich_audit,misc_audit}; this handoff
- Pre-existing/user-owned changes: tools\run_mercury_worker.py, tools\test_run_mercury_worker.py (untouched); candidate still staged (5 A files)
- Records state: uncommitted, unpublished
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
- If no: n/a
