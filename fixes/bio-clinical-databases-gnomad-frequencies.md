# bio-clinical-databases-gnomad-frequencies fix pass

## 2026-09-24

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| Constraint guidance was stale after gnomAD v4.1.1 | P1 | Updated release/version language; replaced the obsolete v4 `< 0.6` first-decile claim with v4.1.1 `< 0.36` first decile and gnomAD's recommended `< 0.45` constrained-gene cutoff; distinguished VEP 115 Hail downloads from browser display. | Official gnomAD v4.1.1 release page; `runs/re_audit_release_check.py` | v4.1 remains the validated site-frequency route; v4.1.1 changes current constraint interpretation. |

### Left unfixed

None. The previous rate-limit, build-ambiguity, and long-SKILL findings were already fixed in staging main and passed focused revalidation.
