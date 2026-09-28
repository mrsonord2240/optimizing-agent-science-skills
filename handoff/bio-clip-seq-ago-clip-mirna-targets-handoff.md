# Handoff: bio-clip-seq-ago-clip-mirna-targets / independent final re-audit

- Updated: 2026-09-28T16:02:00-07:00
- Lane: 4
- Status: rejected; repair required
- Owner leaving: reaudit-scientific-skill (fresh independent worker)
- Next role: fix-scientific-skill

## Source identity

- Origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:clip-seq/ago-clip-mirna-targets`; origin subtree `6326a423789826240d0840be6897ddd69b21d940`.
- Worktree/branch: `F:\OpenScience\wt\opt10-ago-clip` / `optimize/ten-20260928-lane4-ago-clip`; unchanged product HEAD `0bc0b31fc52742dbec1034f698103434cc9460c3`.
- Exact re-audited identity: `21c6ba09ec3580896c35adbe5175ac2e7bf161870e912e46d2bbca42190cfebc` (nine files; 886-byte ordinal manifest).
- Identity was independently regenerated before and during report validation; candidate bytes were not changed.
- Applicable initial audit: `F:\OpenScience\audits\bio-clip-seq-ago-clip-mirna-targets\initial-opt10-20260928\report.json`, SHA-256 `ebe0e70aeb3d781470e8a2ae69fdc4a242235e0afdc2a1f4b7b5bc44a3ac23e2`.

## Completed this phase

- Read the full current audit protocol/rubric and independently audited only the exact fixed candidate.
- Re-ran the shipped suite: 5/5 pass.
- Ran an independent nine-assertion parser/wrapper adversarial matrix: 9/9 pass across both 16-column orientations, expression provenance, reason codes, malformed schemas, path quoting, overwrite refusal, status 42, failed-replacement preservation, and stage cleanup.
- Executed two fresh complete wrapper batches on pinned Hyb `028ab63` official input, two clean single-thread replicates per batch. Every underlying run produced 111 non-empty 16-column rows; each batch retained 94 and excluded 17.
- Compared the two complete batches at read-id and normalized-assignment level: seven accepted-only ids on each side plus four changed assignments among shared ids; `sites.tsv` and `targets.tsv` differ.
- Executed the pinned targeted-Yeo script on bounded paired FASTQ: default output appended ten R2 bases; source script default is 10, CWL prose says 9, and CWL supplies no override.
- Re-executed TargetScan plus/minus exon-spanning conversion, `bedtools intersect -split -s`, wrong-release rejection, and out-of-range rejection; all passed.
- Produced a strict final report: static 88, dynamic 86.0, weighted 87, assertions 23/25, final **Reject** because skill determinism and research methodological-ground vetoes fail.

## Required next actions

1. Fix AGO-004 with a prospectively fixed workflow-level ambiguity policy across more independent runs or a deterministic upstream tie-selection rule; record per-read cross-run support and prove exact repeated-workflow equality.
2. Fix AGO-005 by removing the unsupported exact 9-nt operational statement or by requiring and explicitly passing a protocol-declared UMI length through a pinned targeted route, with 9-nt and 10-nt fixtures tied to provenance.
3. Prepare delta tooling only for the changed executable/claim surfaces.
4. Route the next exact candidate to a new independent re-auditor; do not publish this rejected audit as candidate-ready.

## Open findings and blockers

| Finding | Priority | Disposition |
|---|---:|---|
| AGO-004 | P0 | **Open.** Two-run agreement is not workflow-level deterministic: pair A and B both report 94 retained/17 excluded but accept different read ids and assignments. This fails the determinism and methodological-ground vetoes. |
| AGO-005 | P1 | **Open.** Candidate says targeted Yeo uses a 9-nt R2 UMI; live pinned executable defaults to 10, CWL does not override, and the bounded run extracts 10. |
| AGO-001, AGO-002, AGO-003 | closed | Current Hyb contract, orientation-aware schema, and strict atomic/failure boundaries pass independent execution. |
| AGO-006, AGO-007, AGO-008 | closed | Tool identity, evidence interpretation, structured reporting, and regression surfaces are corrected. |
- Full Yeo remains resource-infeasible without a real library and matched indices; HEAP and reporter validation require biological material; DIANA remote execution is unavailable. None blocks fixing or re-auditing the shipped candidate.

## Environment and evidence

- Raw final run root: `F:\OpenScience\audits\bio-clip-seq-ago-clip-mirna-targets\reaudit-opt10-20260928`.
- Strict report SHA-256 `00f55371ad11cdac36c64fca764cff9fa991baa449074fb0a031efbe45426bde`; viewer `edbb658a068c00234db0639e682f6d2e04fdec6eb645dea9397af8abbcc33c2b`; source identity `e89c7b9e0f571fbc1f510819874368afd85fbb5e65851aba2785fd33054878fa`.
- Schema validation is valid with zero errors; SHA-256 `7a3572356d659243fa5d64e19727ca036586baa4b3be94bc42245e8c69c17a04`.
- Cross-batch Hyb evidence: `evidence/hyb-repeatability.json`, SHA-256 `409c04b2648e334d16086bcf171a28145a4f75bbe8c647b3474ea257510a4026`.
- Targeted-Yeo evidence: `evidence/yeo-targeted-contract.json`, SHA-256 `86a478d6797fc2b59e89327bcd005dfaad7b1685b7d9e6698a69d1cf2f4bf4b2`.
- TargetScan evidence: `evidence/targetscan-contract.json`, SHA-256 `97d9477d56fdcef0a561da1732e17cf8232115c4efccbcd0d32576aeb88c6bb8`.
- Tooling root: `F:\OpenScience\audit-envs\bio-clip-seq-ago-clip-mirna-targets`; `TOOLS.md` SHA-256 `939c5ce0a3c765711c4ba4a38e1895308c5457470c3836789a5b9172860cb810`; environment fingerprint `fcd7556256ce1a32f3473718ad2f0fa3d1821039dc4994ecf4aa626fe97d7e5c`.

## Worktree safety

- Product status remains only `?? skills/bio-clip-seq-ago-clip-mirna-targets/`; the nine candidate files were read but never edited.
- Audit outputs are confined to the raw final run root; heavy Hyb intermediates remain under its `work/` subtree.
- This canonical handoff replacement is the only control-repository write in this phase; unrelated orchestrator, relay, Mercury, and other lane files were not staged or changed.
- The exact rejected re-audit was published locally as `candidate@21c6ba09ec35-reaudit-opt10-20260928` with 24 explicit scripts/inputs; generated views were refreshed. The matching record/view/handoff changes await the run-owned control commit. No product commit, push, pull request, release, submission, or Marketplace action occurred.

## Transition assertion

- Independent final re-audit complete: yes — exact identity reproduced, all accessible changed surfaces executed, restricted surfaces classified, strict report and evidence hashes validated.
- Candidate-ready: **no**. Numerical score 87 is overridden by failed determinism and methodological-ground vetoes.
- Next owner must be a fresh `fix-scientific-skill` worker addressing only AGO-004 and AGO-005 before delta tooling and another independent re-audit.
