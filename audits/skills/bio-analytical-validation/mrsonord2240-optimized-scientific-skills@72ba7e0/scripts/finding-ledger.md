# Independent re-audit finding ledger

Candidate identity:
`bd66239b9133b70a7522d0d99e3bc4ebbed1b8c1291c74fad26367dfa339b2ab`.

| Order | ID | Priority | State | Independent evidence | Disposition |
|---:|---|---|---|---|---|
| 1 | ADV-001 | P0 | resolved | Input 4; `evidence/execution-summary.json`; `scripts/panel_integrated_lod.py` | Misleading APIs are absent. Every returned threshold is structured as a theoretical sampling-only bound with all four assumptions and an explicit non-assay-LoD95 interpretation. |
| 2 | ADV-002 | P1 | resolved | Input 3; eighteen independent invalid probes | All exercised finite/range/type/shape/replicate/binary/k-of-N/grid/target failures raise stable actionable `ValueError` messages without warnings or misleading results. |
| 3 | ADV-003 | P1 | resolved | Input 2; inherited aggregate, two fresh replicated fits, separation and non-bracketing probes | Identified fits return ordered inverse-prediction CI and diagnostics without warnings. Separated and non-bracketing series are refused. |
| 4 | ADV-004 | P1 | resolved | Input 5; fresh 2,400-outcome parameter contrasts and exact replay | `true_lod_vaf` changed 833 outcomes and detection totals in the expected direction; slope changed 181 outcomes; exact same-seed replay matched. |
| 5 | ADV-005 | P2 | resolved | Input 1; static source check; `scientific-source-notes.md` | The default conversion is dimensionally exact and overridable; HCC1395/HCC1395BL and Sample A/B provenance are separated with stable identifiers. |
| 6 | ADV-006 | P2 | open, non-blocking | Static source check; `SKILL.md`; `usage-guide.md`; `scientific-source-notes.md` | Replace the exact `130–170 bp` wording with the cited primary method's 110–190 bp size-selection range and approximately 165 bp average, or add a directly supporting primary source. |

`ADV-006` does not trigger a veto, reduce the grade below Production Ready,
or violate the canonical candidate-ready gate, which forbids open P0 findings.
No audit-local repair was made because the candidate bytes are fixed for this
independent phase.
