# Shared environment for the bio-variant-calling-filtering-best-practices audit runs (2026-09-15).
# Paths in /f/ form: a drive colon inside PATH would split the entry.
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH
export GATKJAR=$E/gatk/gatk-4.6.1.0/gatk-package-4.6.1.0-local.jar
export PY=$E/Scripts/python.exe
export PYTHONIOENCODING=utf-8
GATK="java -jar $(cygpath -w $GATKJAR)"
_S=../../data
if [ ! -f $_S/ref.dict ]; then
  $GATK CreateSequenceDictionary -R $(cygpath -w $_S/ref.fa) -O $(cygpath -w $_S/ref.dict) --QUIET true >/dev/null 2>&1
fi
# MSYS2 bcftools looks for plugins in its build prefix; point it at the shipped DLLs
export BCFTOOLS_PLUGINS=$(cygpath -w $E/msys/mingw64/libexec/bcftools)
