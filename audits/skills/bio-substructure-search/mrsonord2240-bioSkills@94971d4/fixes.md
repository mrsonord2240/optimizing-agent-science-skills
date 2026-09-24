# bio-substructure-search fix pass — 2026-09-24

## Source

- Repository/worktree: `F:\OpenScience\worktrees\bio-substructure-search-fixpass`
- Branch: `agent/fix-bio-substructure-search`
- Base: `4d483d0451fcd60cb3ab62dfa4cd047ec59b3615`
- Final source commit: `94971d4a4427eb5c682cd860eee91e8d9e41adc7`

## Resolved findings

- **P1 ester SMARTS:** normalized the Skill and example on `[CX3](=[OX1])[OX2][#6]`; regression probes cover both isopropyl and phenyl acetate.
- **P1 invalid SMARTS:** added `compile_smarts()` to reject empty, malformed, and zero-atom user queries; routed the Skill’s basic, filtering, and reactive patterns through it.
- **Audit assertion recovery:** `pains_filter()` now returns invalid zero-based input positions instead of silently dropping unparsed molecules.
- **P2 PAINS scope:** replaced the false curcumin claim with RDKit-covered rhodanine/catechol wording and explicitly notes RDKit has no curcumin-specific PAINS entry.
- **P2 performance:** replaced the unsupported 10–100x recursion claim with the measured 1.6x/3.7x reference costs.
- **P2 filter interpretation:** documented collection-specific BRENK attrition and reactive-filter false positives; custom reactive SMARTS now compile once and remain flag-not-delete signals.

## Exact-commit validation

- Source worktree was clean at `94971d4`; `git diff --check HEAD^ HEAD` passed.
- Exact fenced snippets matched both isopropyl acetate and phenyl acetate with the new ester pattern.
- Empty, malformed, and unsupported SMARTS raised named `ValueError`s; an empty include query cannot silently return an empty library.
- `pains_filter([valid, None])` returned invalid position `[1]`.
- Precompiled reactive filters flagged an enone as `Michael_acceptor`; `exclude_warheads=False` suppressed it.
- Generic skill validation reports the upstream legacy frontmatter keys (`tool_type`, `primary_tool`, `author`) as unsupported; they predate this focused repair and were intentionally retained.

## Re-audit result

- **94/100 — Production Ready**
- **Assertions: 30/30**
- **Open P0/P1/P2: 0/0/0**

## Artifacts

- Canonical JSON: `F:\OpenScience\audits\bio-substructure-search\eval_report_bio-substructure-search_result.json`
- Canonical viewer: `F:\OpenScience\audits\bio-substructure-search\eval_viewer_bio-substructure-search.md`
- Focused evidence: `F:\OpenScience\audits\bio-substructure-search\re-audit-20260924\run-focused\focused_validation.out`
- Preserved pre-fix report/viewer: `F:\OpenScience\audits\bio-substructure-search\re-audit-20260924\pre-fix\`

No P0, P1, or P2 findings remain.
