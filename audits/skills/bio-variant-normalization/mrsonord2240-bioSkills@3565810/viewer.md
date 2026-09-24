> **Audit record for `bio-variant-normalization`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@3565810](https://github.com/mrsonord2240/bioSkills/tree/356581080738dee60b613812b35fd4b99d217527/variant-calling/variant-normalization) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0 final-pass exact-commit.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-variant-normalization — final-pass exact-commit audit

Generated: 2026-09-24 · source: `356581080738dee60b613812b35fd4b99d217527`

Final-pass exception: `auditor_independent: false`; one agent fixed and exact-commit audited under one brief.

## Outcome

**95/100 — Production Ready.** No P0, P1, or P2 finding remains open.

The corrected source is the isolated worktree branch `agent/finalpass-bio-variant-normalization-20260924`; it has not been merged, pushed, or promoted.

## Changes verified

- The primary route now explicitly splits, atomizes, then left-aligns; the companion guide uses the same canonical route and preflights REF mismatches before it can leave a broken output for indexing.
- The guide no longer claims that `-m-both` differs from `-m-any` when splitting.
- The repeat example now contains genuinely equivalent homopolymer deletion representations.
- `bcftools csq -p s` is described as skipping unphased hets, without the false global claim that it emits no consequences; the skill tells readers to inspect BCSQ on the installed version.

## Exact-commit evidence

The raw harness and log are in `runs/finalpass_20260924/`. It ran under WSL with **bcftools 1.24** and passed **17/17 assertions**:

| Coverage | Result |
| --- | --- |
| Archived 1: REF detection, atomization artifacts, idempotence | PASS |
| Archived 2: homopolymer canonical key | PASS |
| Archived 3: multiallelic field splitting | PASS |
| Archived 4: MNP representation reconciliation | PASS with vt limitation |
| Archived 5: csq phase behavior | PASS |
| Fresh A: mixed SNP/indel split/join behavior | PASS |
| Fresh B: guide mismatch preflight | PASS |

`vt` was not available in this host. The archived input-4 logical claim was therefore re-executed with the documented bcftools atomization equivalent, rather than represented as a vt run. The raw log makes that limitation explicit.

## Audit result

Skill Veto: PASS. Research Veto: PASS. The source route and all documented safety boundaries that were executable in this environment passed. The retained limitation is environmental audit coverage only, not an open source finding.
