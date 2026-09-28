# Optional package boundary

- `trialr 0.1.6`: documented in `usage-guide.md`, not invoked by the shipped
  script. Its exact retained CRAN source reached `R CMD INSTALL` and stopped
  before compilation because dependency `MASS` was unavailable. Exact evidence:
  `cran-install.log` lines 34097-34100.
- `escalation 0.2.3`: documented in `usage-guide.md`, not invoked by the shipped
  script. Its exact retained CRAN source was not installed because it depends on
  `trialr`; continuing the optional Stan-heavy dependency chain exceeded the
  bounded install ceiling. Exact bounded-skip evidence: `cran-install.log` lines
  34109-34110.
- Re-run only if the independent auditor elects to exercise these alternatives:
  add a compatible `MASS` and the remaining declared `trialr` dependencies to
  the pinned environment, install retained `trialr_0.1.6.tar.gz`, then install
  retained `escalation_0.2.3.tar.gz`.
- This classification does not make either package executable and does not
  classify their scientific claims.
