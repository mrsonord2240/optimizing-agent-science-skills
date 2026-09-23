# Purpose: Syntax-check the SnapATAC2 alternative without writing bytecode into the source worktree.
# Inputs:   repository example path and audit-owned .pyc output path are hard-coded below.
# Usage:    python 08_compile_python.py
import py_compile

source = r'F:\OpenScience\wt\single-cell-scatac-analysis\single-cell\scatac-analysis\examples\scatac_workflow.py'
output = r'F:\OpenScience\audits\bio-single-cell-scatac-analysis\run\scatac_workflow.pyc'
py_compile.compile(source, cfile=output, doraise=True)
print('python_syntax=PASS')
