#!/bin/bash
# tiny launcher used for every WSL run: W.sh <script> <args...>  (cwd = run dir, env alignment-files)
R=/mnt/openscience/audits/bio-alignment-filtering/run
cd $R
"$@"
