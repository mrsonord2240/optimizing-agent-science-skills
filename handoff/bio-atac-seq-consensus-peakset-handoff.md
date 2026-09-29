# Handoff: bio-atac-seq-consensus-peakset / initial audit

- Updated: 2026-09-28
- Lane: 1
- Status: ready-for-local-record-publication-and-fix
- Owner leaving: audit-scientific-skill
- Next role: fix-scientific-skill

## Source identity

- Origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/consensus-peakset`; origin checkout remained clean and read-only.
- Candidate: `F:\OpenScience\wt\mercury-pilot-consensus-peakset\skills\bio-atac-seq-consensus-peakset` at base `4cc6cabc39ee01dcf3e828e3f8a164b7e155f4fb`, branch `optimize/mercury-pilot-consensus-peakset`.
- Exact canonical content identity: SHA-256 `238e6dfd2a0a5da05cf1c37ceba3de899a1f298927e49ddc5c9bb668eb8eda5c` (5 files; 27,093 bytes; sorted POSIX-path/byte-count/file-SHA manifest, LF-separated, no trailing LF). See [source-identity.json](F:/OpenScience/audits/bio-atac-seq-consensus-peakset/initial-mercury-pilot-20260928/source-identity.json).
- The tooling handoff's prior expected digest `4778d035fcabb3f8e9f94760a80eb65228ec3482593058455597dfc8f0aab11e` used a noncanonical path-and-file-hash recipe with a trailing LF. The canonical manifest supersedes that digest; candidate bytes did not change.

## Completed this phase

- Read the complete audit contract, tooling inventory, and candidate tree; verified the candidate remained unmodified.
- Direct Linux Bash invocation fails on CRLF (`$'\r': command not found`; `pipefail\r: invalid option name`). A disposable LF-normalized copy completed the public hg19 fixture workflow: 3,000 inputs, 2,927 after greedy overlap, 2,886 after blacklist; all final intervals were 501 bp, and SAF coordinates matched BED across all 2,886 rows.
- A distinct two-file case pooled 400 public narrowPeak rows, retained 393 after greedy overlap and 388 after blacklist.
- A targeted 9-column case silently completed with an absent summit offset and emitted a start-centered interval. Official rtracklayer source confirms NarrowPeak import metadata uses `peak` for column 10; the installed environment did not contain rtracklayer for execution.
- Produced a schema-valid report, viewer, identity, two-item ordered finding ledger, evidence, saved audit runner, and bounded inputs under [raw audit root](F:/OpenScience/audits/bio-atac-seq-consensus-peakset/initial-mercury-pilot-20260928).
- No audit-local repair was made. Report: [report.json](F:/OpenScience/audits/bio-atac-seq-consensus-peakset/initial-mercury-pilot-20260928/report.json); validation: [schema-validation.json](F:/OpenScience/audits/bio-atac-seq-consensus-peakset/initial-mercury-pilot-20260928/evidence/schema-validation.json); ledger: [finding-ledger.md](F:/OpenScience/audits/bio-atac-seq-consensus-peakset/initial-mercury-pilot-20260928/finding-ledger.md).

## Required next actions

1. Complete local records publication for the raw audit and regenerate/check the records index and status outputs before dispatching the fixer.
2. Route `BAP-001` and `BAP-002` to `fix-scientific-skill`; preserve the exact candidate identity and do not treat normalized-copy success as validation of the shipped bytes.
3. After fixes, rerun the exact Bash launch, the 3,000-row matched hg19 workflow, the two-file case, and the focused missing-summit regression.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| BAP-001 | P0 | open | Input 3; `evidence/9col-rerun.txt`; `inputs/adversarial-9col.bed` | Validate narrowPeak row width and summit offset before arithmetic; reject malformed rows with filename/line context and handle `-1` explicitly. |
| BAP-002 | P0 | open | Input 1; `evidence/direct-crlf-rerun.txt`; candidate shell script | Normalize the shipped Bash script to LF and verify direct execution under the prepared Linux runtime. |

- The research veto fails on Methodological Ground and Code Usability; diagnostic final score is 60/100 with veto override, grade Reject.
- Assembly mismatch was reviewed but not raised as a separate finding: the Skill explicitly requires matching assembly/chromosome naming, and the tested fixture used matching hg19 references. Same-named assembly provenance cannot be reliably inferred from coordinates alone.
- DiffBind, pybedtools, IDR, liftOver, and featureCounts downstream surfaces remain static-only or blocked by unavailable packages/assets and lack of BAM inputs. No optional packages were installed.

## Environment and evidence

- Prepared environment: WSL2 `science`, user `sci`; Bash 5.3.9; Python 3.12.14; bedtools 2.31.1; R 4.4.1. Interop is disabled; execution and public fixture reads used `/mnt/openscience`.
- Tool inventory: `F:\OpenScience\audit-envs\bio-atac-seq-consensus-peakset\TOOLS.md`, SHA-256 `0895f658996fcf5dd5fafc16e63083f21619e94c809205ec836db898fb761a81`. Rubric: current `skill-auditor.zip`, SHA-256 `e54e9ff8b0c3677abcfe657ad6ed92ba34dbdb8ad205c7157ad881f25afcf0de`.
- Public fixture: GEO GSM7854725, GM12878 ATAC-seq replicate 1, hg19; matching UCSC hg19 chromosome sizes and Boyle-Lab hg19 blacklist v2 were already cached.
- Environment limitation: `rtracklayer` and `GenomicRanges` are unavailable; no package was installed.
- No restricted-access blocker. No product commit, push, pull request, release, or remote publication occurred.

## Worktree safety

- Candidate status remained the run-owned untracked Skill subtree only at the recorded base; all five candidate file hashes are in `source-identity.json`.
- Candidate files and origin checkout were not edited. Audit artifacts were written only under the raw audit root, except this canonical handoff.
- Audit-local repair details: none. Local records publication remains the next operational action; no remote state was changed.

## Transition assertion

- Exact candidate bytes are pinned to `238e6dfd2a0a5da05cf1c37ceba3de899a1f298927e49ddc5c9bb668eb8eda5c`: yes.
- Evidence and report schema validation complete: yes; validator result is in `evidence/schema-validation.json`.
- Open findings routed in priority order to `fix-scientific-skill`: yes; `BAP-001`, `BAP-002`.
- Deferred surfaces and environment limitations recorded: yes.
- Next phase: local records publication, then `fix-scientific-skill`.
