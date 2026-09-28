# Handoff: bio-chipseq-allele-specific-binding / fresh final re-audit 2

- Updated: 2026-09-28T16:25:00-07:00
- Lane: 5
- Status: fresh final re-audit complete; candidate-ready; local records publication pending
- Owner leaving: independent `audit-scientific-skill`
- Next role: optimization orchestrator for explicit local records publication, then park exact candidate

## Source identity

- Origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:chip-seq/allele-specific-binding`; read-only source subtree `3674e1603cbc7a17731f9f5ea652ae7aa9f6e1e5`.
- Candidate: `F:\OpenScience\wt\opt10-chipseq-asb\skills\bio-chipseq-allele-specific-binding`; branch `optimize/ten-20260928-lane5-chipseq-asb`, base HEAD `0bc0b31fc52742dbec1034f698103434cc9460c3`.
- Exact identity: `03415aabaa66de0ef1b747e3fc664dae6d2868e42bf52a2c104d990db5e6057f`; eight ordinal relative-POSIX-path `path<TAB>sha256` rows, LF joined without trailing LF, 750 manifest bytes.
- Strict source record: `F:\OpenScience\audits\bio-chipseq-allele-specific-binding\reaudit2-opt10-20260928\source-identity.json`; candidate identity independently reproduced before scoring and during schema validation.

## Completed this phase

- Fresh independent audit: **95/100 Production Ready**, static 96, dynamic 94.4, 25/25 assertions, both veto gates PASS, no recommendations or open findings.
- Independently closed `CBA-009`: official Bioconductor 3.22 index and BaalChIP 1.36.0 DESCRIPTION/source, exact tar SHA-256 `f3d0339...`, candidate constants, runner gate/status and tests coherently bind R 4.5 / Bioconductor 3.22 / BaalChIP 1.36.0. Every candidate-used constructor, correction, getter and named-report API matches the exact source.
- Independently closed `CBA-010`: read-only checkout remote/HEAD is exactly `https://github.com/trgaleev/AlleleSeq2.git@cfe8acf88989922da841e71238b360f8f57e813a`; candidate names that implementation and retains Rozowsky et al. separately as the canonical method.
- Live passed: R parse/helper/version gates, Python 3/3, real indexed-BAM RAF and gDNA preflights, ten fail-closed negatives, owned-staging cleanup, paired WASP, provider WASP HDF5, interval filters, and public two-feature RASQUAL prepare/run with overwrite refusal.
- Strict report schema and source hashes validate; no audit-local repair or candidate edit occurred.

## Required next actions

1. Publish the raw final audit locally through modular records mode, naming `inputs/test-inputs.md`, `scripts/run_reaudit2.sh`, and `scripts/hash_core_artifacts.py` as explicit artifacts.
2. Regenerate and validate `audits/STATUS.md` and `audits/STATUS.html`; bind the publication to exact candidate identity `03415a...` only.
3. Record the local publication name/hash in this handoff, commit only the explicit run-owned records/view files, and park this exact worktree for later ten-skill batch assembly.
4. Do not rerun fixes or tooling unless publication validation exposes a real record defect; no product commit, remote push, PR, release, submission, or Marketplace action is authorized in this lane.

## Open findings and blockers

- Open product findings: **none**. `CBA-001` through `CBA-010` are closed in `finding-ledger.md`.
- BaalChIP full statistical-model execution and actual all-excluded/no-call publication remain `RESOURCE_INFEASIBLE_BOUNDED_NOT_CREDITED`: BaalChIP, Rsamtools, GenomicAlignments and rtracklayer are absent; a fresh exact-source probe stops on those compiled dependencies, consistent with the retained bounded Rhtslib build limit.
- AlleleSeq full-toolchain execution remains `UNAVAILABLE_EXTERNAL_ONLY_NOT_CREDITED`: Python 2, STAR, Picard, official `vcf2diploid.jar`, and matching legacy assets are unavailable. This is the documented routing boundary, not an open defect.
- Local records publication is pending the orchestrator; audit artifacts themselves are complete and schema-valid.

## Environment and evidence

- Raw root: `F:\OpenScience\audits\bio-chipseq-allele-specific-binding\reaudit2-opt10-20260928`; strict report SHA-256 `9cc9d70f221d02fc17bd4d300550a467a95912f62a18b431c41570c09c6d03da`; viewer SHA-256 `afd451ae68c8cc50014e6834fc91895f6793788add4ad415d1ac246a583066d4`; source-identity SHA-256 `3345ecf42f4cefa0be4004c8ca6034b043baf43caab781be8707b026a303b5d3`.
- Schema record: `evidence/schema-validation.json` reports v4.0 valid, identity `03415a...`, static 96, dynamic 94.4, final 95, 25/25, research veto PASS, candidate-ready.
- Core integrity manifest: `evidence/artifact-hashes.tsv`, 26 artifacts. Complete fresh transcript: `evidence/execution.log`; exit/result record: `evidence/execution-status.tsv`; orchestrator: `scripts/run_reaudit2.sh`.
- Durable tooling: `F:\OpenScience\audit-envs\bio-chipseq-allele-specific-binding`; `TOOLS.md` SHA-256 `59fa3d4ff6e88eeb717f2b312a1b2ade4594944f6a06981ef895aaa83077ace9`; delta fingerprint `0032bf762101dada0b00cc047935e6bd0ef528579fae355ac1a2eec22fd27b44`.
- Environment: Python 3.10.21, R 4.5.3, Bioconductor 3.22, samtools 1.21, pinned WASP/RASQUAL/AlleleSeq source identities; exact conda lock SHA-256 `5c1f84081967c537196e341afe8a3d5e0913258f0232b873af650dc2aebd9247`.

## Worktree safety

- Candidate worktree still contains only the expected untracked candidate tree; `git status --short` is `?? skills/bio-chipseq-allele-specific-binding/`.
- Exact candidate identity was unchanged before and after execution; no candidate cache artifact was written, and no candidate/source/tooling byte was edited by the auditor.
- Raw audit artifacts and this canonical handoff are the only phase outputs. The extracted `skill-auditor` rubric is retained under the raw run root as immutable method evidence.
- The exact final audit was published locally as `candidate@03415aabaa66-reaudit2-opt10-20260928` with 24 explicit scripts/inputs; generated views were refreshed. The matching record/view/handoff changes await the run-owned control commit. No product commit, push, PR, release, submission, Marketplace action, private-data use, dependency installation, or gated-asset bypass occurred.

## Transition assertion

- Candidate-ready: **yes**, for exact identity `03415aabaa66de0ef1b747e3fc664dae6d2868e42bf52a2c104d990db5e6057f`.
- Audit is independently complete: strict report, viewer, source identity, finding ledger, test inputs, execution evidence, hash manifest and schema validation are present.
- Next transition is local records publication by the optimization orchestrator, then immutable parking for the one-commit ten-skill assembly; do not send this lane back to a fixer.
