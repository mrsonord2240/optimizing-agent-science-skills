> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@2f38178](https://github.com/mrsonord2240/optimized-scientific-skills/tree/2f381782596c6569fe5a8357556856512b7fbb6c/skills/bio-atac-seq-differential-accessibility) match audited candidate `dfc879ea543a99d857d53f2556d8b09660006d27a8dda23ede8b03b4ff5b9b1b` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-atac-seq-differential-accessibility`**
> - Audited working candidate `dfc879ea543a99d857d53f2556d8b09660006d27a8dda23ede8b03b4ff5b9b1b`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/differential-accessibility), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-differential-accessibility`**
> - Audited working candidate `dfc879ea543a99d857d53f2556d8b09660006d27a8dda23ede8b03b4ff5b9b1b`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/differential-accessibility), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Delta re-audit viewer (delta-cat2): bio-atac-seq-differential-accessibility

Candidate: sha256-manifest-v1 `dfc879ea543a99d857d53f2556d8b09660006d27a8dda23ede8b03b4ff5b9b1b` (5 files, 46,766 bytes). Previous run: delta-cat-20260930 (`678737f8...`), score 87. Independent auditor; no Skill bytes edited.

**Decision: candidate-ready. Final 88 (Production Ready), static 89, execution average 86.8 (carried), assertions 28/29, no veto, no open P0.**

## Delta verified

Relative to delta-cat, only `references/method-reference.md` changed (logs/delta2_diff.log). The change is a single line, 149: "does this inside DiffBind" became "does this in DESeq2 directly on the DiffBind counts (limits: SKILL.md step 5)". No other occurrence of "inside DiffBind" remains.

The new wording matches `fit_sva`, which calls `DESeqDataSetFromMatrix` on the `dba` counts. SKILL.md step 5, which the line now cites, was verified in delta-cat and is unchanged.

## Findings

| ID | Status |
|---|---|
| R-002 reference contradicts SKILL.md | Documentation part resolved. The runtime part stays open as P2 "--method silently ignored with --sva" (needs a code change) |
| R-001 SVA skips blacklist, no runtime warning | Open P2 (needs a code change) |
| R-004 non-human TxDb untested | Open P2 |

## Re-scored

Static: agent_usability 15 -> 16 (88 -> 89). Execution unchanged, because the script is byte-identical. Final = 0.4 x 89 + 0.6 x 86.8 = 87.7.

Scripts: `scripts/identity_diff.py`, `delta2_diff.py`, `build_delta2.py`. Logs: `logs/`.
