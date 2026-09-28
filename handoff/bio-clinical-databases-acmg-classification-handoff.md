# Handoff: bio-clinical-databases-acmg-classification / independent final re-audit

- Updated: 2026-09-28
- Lane: 3
- Status: phase-complete / candidate-ready
- Owner leaving: `/root/lane3_acmg_reaudit2`
- Next role: orchestrator records publication, then exact-byte batch assembly

## Source identity

- Origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:clinical-databases/acmg-classification`; immutable source subtree `b4c1f4dd04a6a53f3eba2aa56da5d830ba325e1a`; read-only origin checkout is clean.
- Candidate: `F:\OpenScience\wt\opt10-acmg-classification\skills\bio-clinical-databases-acmg-classification` on `optimize/ten-20260928-lane3-acmg-classification`; product HEAD remains `0bc0b31fc52742dbec1034f698103434cc9460c3`.
- Exact audited identity: `sha256-manifest-v1:286df2647ef2e418d8302102c7522705f7b5ce4156cfaea6be5c8c36c6d55571`; seven files; 644-byte ordinal relative-POSIX-path/byte-count/SHA-256 manifest with TAB fields, LF records, and no trailing LF.
- Strict identity record: `F:\OpenScience\audits\bio-clinical-databases-acmg-classification\reaudit2-opt10-20260928\source-identity.json`, SHA-256 `ab5a82c4ff81fa1cfc13d933e112e937da72d368db2646b72b5ac3f08a0c369c`.

## Completed this phase

- Read and followed the complete audit-scientific-skill contract and the freshly extracted `skill-auditor.zip` rubric, veto, classification, and report-schema references. Candidate bytes were not changed.
- Independently recomputed the exact candidate identity and statically reviewed the complete seven-file tree, trigger/authority/practice boundaries, provenance/license, instructions, reference, implementation, and tests.
- Executed all accessible surfaces in isolated WSL `science`: 24/24 shipped tests; compilation; guarded standalone demo; 25 invalid probes; 26 predictor endpoints; nine PVS1 states; three contradictory NMD rejections; 14 OddsPath cases; two valid and four invalid ISO-date cases; six somatic tiers; GeneBe one-record response; CSpec six-version response.
- Closed ACMG-001, ACMG-002, and ACMG-006; independently preserved closure of ACMG-003/004/005/007/008/009. No new finding was opened.
- Final verdict: **Production Ready**, score **96/100**, static **95**, dynamic **97.3**, assertions **28/28**, Skill Veto **PASS**, Research Veto **PASS**, no open P0/P1/P2.
- Strict report, viewer, inputs, source identity, surface classifications, finding ledger, source notes, repeatable harness, candidate manifest, and artifact hashes were written and validated.

## Required next actions

1. Publish this exact raw run through the modular records publisher using explicit artifacts only; regenerate and validate the records indexes. Do not alter strict `report.json` or candidate bytes.
2. Bind publication to exact identity `286df2647ef2e418d8302102c7522705f7b5ce4156cfaea6be5c8c36c6d55571` and record the publication identifier in this handoff if the relay requires it.
3. Park this exact worktree as candidate-ready until the orchestrator assembles all ten audited candidates in the single authorized shelf batch commit. Do not push, open a PR, release, or submit remotely.

## Open findings and blockers

- Open findings: none. ACMG-001 through ACMG-009 are closed for the exact audited identity.
- No executable blocker. InterVar/ANNOVAR remains restricted/documented-only; AutoPVS1 remains unpinned/documented-only; VarSome, Franklin/Genoox, and ClinGen VCI remain restricted/manual; other named evidence sources have no shipped wrapper. The candidate states these boundaries accurately.
- No user action or credential is required for local records publication or later exact-byte shelf assembly.

## Environment and evidence

- Tool root: `F:\OpenScience\audit-envs\bio-clinical-databases-acmg-classification`; `TOOLS.md` SHA-256 `86a8fec1672e6a80907925ccd216f9f3d9e5e99ea7b40b70fdffbebd7185b893`.
- Runtime: WSL `science` / `sci`; Python 3.12.14; requests 2.32.5; exact 40-artifact lock SHA-256 `800ca0e5bf3c0dc2849f0e4797f1b2928ce9cf72ed1c4b5e2e605b5784b8b4e5`; fingerprint SHA-256 `f97acb4215b1958eb67f8ffb51b958780b09305575964e598c898633ed6f5881`.
- Isolation: private mount namespace, `/mnt/f` unmounted, `/mnt/openscience` only, `WSL_INTEROP` unset. Only a public GeneBe documentation coordinate and public GATM symbol were used; no patient/private data, PHI, proprietary database, or credential was used.
- Raw audit root: `F:\OpenScience\audits\bio-clinical-databases-acmg-classification\reaudit2-opt10-20260928`.
- Report: `report.json`, SHA-256 `a71432c78089958e8eb36ad9ef789d0e51e0d1de1d03b95e4d48e9f96ffb42c6`; viewer SHA-256 `58dd4726779f14a792f783c5cb3cb2de7810bb0af29457d831fa96ac7aa62c91`.
- Artifact manifest: `artifact-hashes.json`, SHA-256 `3dad02e9705556394d14695c85b3ef8ef9db966db9197997c396de4165bd9dd2`; 18 named artifacts; strict validator result: score 96, Production Ready, 28/28 assertions, all hashes valid.

## Worktree safety

- Candidate worktree remains only `?? skills/bio-clinical-databases-acmg-classification/`; no tracked or unrelated product path changed. Candidate subtree has zero `__pycache__`, `.pyc`, or `.pyo` artifacts.
- Origin checkout remains clean at the pinned commit. The only phase-owned control-repository mutation is this canonical handoff; concurrent worker and user changes were not staged or altered.
- The exact final audit was published locally as `candidate@286df2647ef2-reaudit2-opt10-20260928` with 15 explicit scripts/inputs; generated views were refreshed. The matching record/view/handoff changes await the run-owned control commit. No repair, product commit, push, PR, release, Marketplace action, credential action, or remote mutation occurred.

## Transition assertion

- Candidate-ready: **yes**, for exact identity `286df2647ef2e418d8302102c7522705f7b5ce4156cfaea6be5c8c36c6d55571` only.
- Publication route: orchestrator may publish the exact raw run, regenerate/check indexes, then leave these bytes parked for the single ten-skill shelf batch commit.
- Any candidate-byte change invalidates this audit and must restart from deterministic identity plus fresh tooling delta and independent re-audit.
