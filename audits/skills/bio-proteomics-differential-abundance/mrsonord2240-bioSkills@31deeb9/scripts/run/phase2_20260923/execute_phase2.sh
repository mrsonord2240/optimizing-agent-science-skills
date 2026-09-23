#!/usr/bin/env bash
# Master fresh execution driver; preserves every invoked command as evidence.
set -euo pipefail
RUN='F:/OpenScience/audits/bio-proteomics-differential-abundance/run/phase2_20260923'
SK='F:/OpenScience/wt/proteomics-differential-abundance/proteomics/differential-abundance'
DD='F:/OpenScience/audits/bio-proteomics-differential-abundance/data'
ENV='F:/OpenScience/audit-envs/mass-spec-proteomics-analyst'
"$ENV/Scripts/python.exe" -m py_compile "$RUN/phase2_python_regressions.py"
bash -n "$RUN/phase2_cli.sh"
"$ENV/r.sh" "$RUN/phase2_r_regressions.R" "$SK" "$DD" "$RUN" | tee "$RUN/input1_3_5_8_10_11.log"
"$ENV/Scripts/python.exe" "$RUN/phase2_python_regressions.py" "$SK" "$DD" "$RUN" | tee "$RUN/input4_7_13.log"
bash "$RUN/phase2_cli.sh" | tee "$RUN/input9_12_driver.log"
echo 'ALL_PHASE2_EXECUTIONS_PASS'
