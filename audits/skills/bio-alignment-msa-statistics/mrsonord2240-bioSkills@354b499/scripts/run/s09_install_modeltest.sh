#!/bin/bash
# Side env for ModelTest-NG (referenced by SKILL.md 'Distance Correction Models'); separate env so no existing env changes.
micromamba create -y -n aln-mtng -c conda-forge -c bioconda modeltest-ng </dev/null 2>&1 | tail -5
micromamba run -n aln-mtng modeltest-ng --version </dev/null 2>&1 | head -5
