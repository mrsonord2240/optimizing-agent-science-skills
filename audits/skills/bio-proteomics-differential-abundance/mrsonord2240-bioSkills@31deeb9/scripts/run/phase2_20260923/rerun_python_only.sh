#!/usr/bin/env bash
# Re-run Python evidence after adding the explicit scope-boundary assertion.
set -euo pipefail
RUN='F:/OpenScience/audits/bio-proteomics-differential-abundance/run/phase2_20260923'
SK='F:/OpenScience/wt/proteomics-differential-abundance/proteomics/differential-abundance'
DD='F:/OpenScience/audits/bio-proteomics-differential-abundance/data'
ENV='F:/OpenScience/audit-envs/mass-spec-proteomics-analyst'
"$ENV/Scripts/python.exe" -m py_compile "$RUN/phase2_python_regressions.py"
"$ENV/Scripts/python.exe" "$RUN/phase2_python_regressions.py" "$SK" "$DD" "$RUN" | tee "$RUN/input4_6_7_13.log"
