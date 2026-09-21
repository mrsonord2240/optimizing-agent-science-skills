#!/bin/bash
# Input 5: run the shipped example from a scratch copy, then inspect its PDFs
cd "$(dirname "$0")"; rm -rf scratch; mkdir scratch; cp skill/data-visualization/matplotlib-fundamentals/examples/matplotlib_phd.py scratch/
cd scratch && bash F:/OpenScience/audit-envs/data-visualization/py.sh -W always matplotlib_phd.py
cd .. && bash F:/OpenScience/audit-envs/data-visualization/py.sh i5a_check.py
