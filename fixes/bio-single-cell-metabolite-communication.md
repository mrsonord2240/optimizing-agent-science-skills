# bio-single-cell-metabolite-communication fix pass

Source commit: 8409788111cfe93ffb118801c0104d1ddd7fd93f

- Added Windows-safe main guards to all MEBOCOST inference patterns and documented
  the multiprocessing RuntimeError.
- Linked the documented primary flow to prepare_data_for_mebocost().
- Added a deterministic 24-cell, 6-gene AnnData fixture generator, a portable
  config template, and expected smoke-test invariants.

Validation: the bundled fixture generator byte-compiled and produced a 24x6 h5ad;
the exact-commit re-audit exited 0 with three guards, QC routing, fixture, and
config template verified.

Result: static 96/100; execution 98.4/100; 21/21 assertions PASS; final 97/100
Production Ready; no open P0/P1/P2.

Canonical artifacts:

- F:\OpenScience\audits\bio-single-cell-metabolite-communication\eval_report_bio-single-cell-metabolite-communication_result.json
- F:\OpenScience\audits\bio-single-cell-metabolite-communication\eval_viewer_bio-single-cell-metabolite-communication.md
