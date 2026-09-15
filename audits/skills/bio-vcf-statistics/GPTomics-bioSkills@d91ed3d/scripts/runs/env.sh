# Shared environment for the bio-vcf-statistics audit runs (2026-09-15). Windows side: MSYS2 bcftools 1.24.
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH
export PY=$E/Scripts/python.exe
export PYTHONIOENCODING=utf-8
# MSYS2 bcftools looks for plugins in its build prefix; point it at the shipped DLLs
export BCFTOOLS_PLUGINS=$(cygpath -w $E/msys/mingw64/libexec/bcftools)
