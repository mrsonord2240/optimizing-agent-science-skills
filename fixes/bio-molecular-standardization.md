# bio-molecular-standardization fix pass

Source commit: 5fcd1a11abb2c0aad63845773334160c287a1d1a
Branch: agent/fix-bio-molecular-standardization
Worktree: F:\OpenScience\worktrees\bio-molecular-standardization-fixpass

## Fixed audit findings

- P1: ChEMBL parents with multiple retained fragments are now flagged by default;
  a named RDKit largest-organic-fragment fallback is available only by opt-in.
- P1: QSAR preparation returns a complete status tally and the bundled demo
  prints it.
- P2: Aggregation exposes activity_range and replicate_disagreement, with a
  documented 1.0 log-unit review threshold and optional drop policy.
- P2: RDKit QSAR preparation accepts a validated boolean keep_isotopes_col for
  per-record isotope retention and records the decision.
- P2: Required input columns and optional isotope column are validated with
  actionable ValueError messages.

## Validation

- The bundled example byte-compiled and its demonstration ran.
- Exact-commit audit: F:\OpenScience\audits\bio-molecular-standardization\run\reaudit_fixed_findings.py
  exited 0.
- Focused re-audit passed salt policy, status accounting, replicate QC,
  per-row isotopes, and column validation.
- The original 3,966-row ChEMBL hERG fixture yielded 3,208 identities,
  379 replicated groups, 47 replicate-disagreement flags, and maximum
  activity range 3.69.

## Audit result

- Static: 96/100
- Execution: 96.4/100
- Assertions: 24/24 PASS
- Final: 96/100, Production Ready
- Open P0/P1/P2: none

Canonical artifacts:

- F:\OpenScience\audits\bio-molecular-standardization\eval_report_bio-molecular-standardization_result.json
- F:\OpenScience\audits\bio-molecular-standardization\eval_viewer_bio-molecular-standardization.md
