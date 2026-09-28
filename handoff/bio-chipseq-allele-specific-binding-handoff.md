# Handoff: bio-chipseq-allele-specific-binding / final re-audit

- Updated: 2026-09-28T15:17:00-07:00
- Lane: 5
- Status: needs-fix
- Owner leaving: `reaudit-scientific-skill`
- Next role: `fix-scientific-skill`

## Source identity

- Origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:chip-seq/allele-specific-binding`; source subtree `3674e1603cbc7a17731f9f5ea652ae7aa9f6e1e5` stayed read-only.
- Working tree: `F:\OpenScience\wt\opt10-chipseq-asb\skills\bio-chipseq-allele-specific-binding`; branch `optimize/ten-20260928-lane5-chipseq-asb`, base HEAD `0bc0b31fc52742dbec1034f698103434cc9460c3`.
- Exact audited content SHA-256: `944f852224538df92c581ab4a42889202ab10639f54974130f841782f5c90ead`; eight ordinal `path<TAB>sha256` rows, LF joined without trailing LF.
- Strict report: `F:\OpenScience\audits\bio-chipseq-allele-specific-binding\reaudit-opt10-20260928\report.json`, SHA-256 `20d66f97efe8d3092788f679dc53187ab6acf19963cbe4a29a830bb97e6c1b2d`.

## Completed this phase

- Independently verified exact candidate identity before and after execution; no candidate bytes changed.
- Live-ran paired WASP v0.3.4 and provider chr22 HDF5 construction; mate names, six/six remap records, four/four paired final alignments, count invariants, and all four HDF5 shapes passed.
- Live-ran candidate RASQUAL `prepare` and `run` on the public two-feature chr11 cohort; binary sizes, exactly-once feature rows, 25-column contract, finite phi/p/q, convergence zero, BH family, and overwrite refusal passed.
- Passed BaalChIP R parse/helper tests, RAF and gDNA real-BAM preflights, ten structured negative probes, live interval controls, and existing-output refusal.
- Independently closed `CBA-008`: missing-BaalChIP exit 1 left no final output or matching partial and preserved an unrelated sentinel.
- Retained honest boundaries: full BaalChIP statistical/terminal paths are not live-verified; AlleleSeq remains external-only and uncredited.
- Strict schema validation passed: final score 92/100, 23/25 assertions, both veto gates PASS. Numeric grade is Production Ready, but workflow readiness is **needs-fix** because an open P1 remains.

## Required next actions

1. Fresh `fix-scientific-skill` worker must resolve `CBA-009`: choose one coherent BaalChIP binding—Bioconductor 3.23 plus a compatible R/tooling environment for version 1.38.0, or the actual package version supplied by Bioconductor 3.22—and align `SKILL.md`, reference installation text, runner version check, and tooling.
2. In the same narrow fix, resolve `CBA-010` by linking the exact AlleleSeq2 implementation repository used for commit `cfe8acf`, separately from the method paper/canonical project.
3. Route to `prepare-scientific-skill-tooling` delta. Rebuild the affected R environment as needed and run package load, a bounded full-model case, all-excluded/no-variant publication, no-call publication, and the existing cleanup regression.
4. Route exact post-fix bytes to a fresh independent re-audit. Do not publish this report as candidate-ready.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| CBA-001/002 | P0 | fixed | helper suite; fresh RAF/gDNA preflights | Preserve official constructor/report and measured correction contracts. |
| CBA-003 | P0 | fixed | `evidence/wasp-live.tsv`, `wasp-hdf5-live.tsv` | Preserve paired filenames, pairing, counts, and provider shapes. |
| CBA-004 | P1 | fixed | `evidence/rasqual-cohort.tsv` | Preserve public cohort iteration, convergence, and BH family. |
| CBA-005 | P1 | fixed | `evidence/alleleseq-dryrun-boundary.tsv` | Preserve external-only boundary until the complete official stack exists. |
| CBA-006 | P1 | fixed | ten failures; interval/helper outputs | Preserve validation, exclusion, empty/report, and rerun behavior. |
| CBA-008 | P1 | fixed | atomic-cleanup stderr plus sentinel | Preserve owned staging cleanup on package-load failure. |
| CBA-009 | P1 | open | `evidence/source-binding-check.tsv` | BaalChIP 1.38.0 source is `RELEASE_3_23`; candidate says Bioconductor 3.22 while prepared library is 3.22.0. |
| CBA-010 | P2 | open | source table and checkout remote | Bind `cfe8acf` to tested `trgaleev/AlleleSeq2`, not only `gersteinlab/AlleleSeq`. |

## Environment and evidence

- Tool record: `F:\OpenScience\audit-envs\bio-chipseq-allele-specific-binding\TOOLS.md`, SHA-256 `2e78be8ac6a7c5bc6e777c78ef46f83ead28244c757da78ccc0fd275381fc767`; delta fingerprint file SHA-256 `76aa74812b8f73deff029a01fc64407e03019f64e9aa328c7741ab7ee8ff421a`.
- Explicit environment lock SHA-256: `5c1f84081967c537196e341afe8a3d5e0913258f0232b873af650dc2aebd9247`; R package inventory SHA-256 `2facdaed4d0b50854506d79161341114dda38f9fea4000601ef6f3cf4282734b`.
- Viewer: `...\reaudit-opt10-20260928\viewer.md`, SHA-256 `2500ce76589d4911067bba35618daa1e514eaf7dd9ef3fabd65fef63b3a2f03a`.
- Source identity: `...\source-identity.json`, SHA-256 `4b5c862c3c440027c7bd0e6103e3d580ef6beea5976394c286a4eb7ce96bf8a7`.
- Schema validation: `...\evidence\schema-validation.json`, SHA-256 `dda06b08a2e8f36e5f09447856b1c5e690e9198869324b94bdd14fd68d5a3bc0`, `valid: true`.
- Full/secondary transcripts: `execution.log` SHA-256 `d9c5842f501c6149182d01afb69f6ca38d8c0c9e9dd828e6684b059f0c0c284a`; `secondary-execution.log` SHA-256 `205ec9adfdaaba3c955af482f41836ff9145d9f24b50ff7620d4ab879b109531`.
- Tooling impact: `changed`: the audit exposed a package-release/environment binding defect that invalidates the previous final-readiness assumption.

## Worktree safety

- Product worktree remains one expected untracked candidate tree and no other changes; candidate contains no auditor cache artifacts.
- Re-audit owns only `F:\OpenScience\audits\bio-chipseq-allele-specific-binding\reaudit-opt10-20260928\` and this canonical handoff update.
- Prepared source checkouts were read-only; large HDF5 builds and all execution outputs stayed under the owned re-audit root.
- The exact re-audit was published locally as `candidate@944f85222453-reaudit-opt10-20260928` with 46 explicit scripts/inputs; generated views were refreshed. The matching record/view/handoff changes await the run-owned control commit. No candidate repair, product commit, push, PR, Marketplace action, private-data use, or restricted-access bypass occurred.

## Transition assertion

- Next-phase prerequisites met: yes, for a narrow fixer on `CBA-009` and `CBA-010`.
- Candidate-ready: no; `CBA-009` is an open P1 reproducibility contract defect.
