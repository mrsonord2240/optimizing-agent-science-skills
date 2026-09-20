# Syntax + install-line checks (M4 evidence): parse every code block / the example, dry-run solve the Skill's conda lines, check the git URLs exist
source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN
echo "== py_compile / ast.parse"
micromamba run -n as-core python - <<'PY'
import ast, glob, py_compile, sys, tempfile, os
for f in sorted(glob.glob('blocks/*.py')):
    ast.parse(open(f, encoding='utf-8').read()); print('ast ok', f)
c = os.path.join(tempfile.mkdtemp(), 'x.pyc')
py_compile.compile('skill/examples/plot_sashimi.py', cfile=c, doraise=True); print('py_compile ok skill/examples/plot_sashimi.py')
PY
echo "== bash -n on shell blocks"
for f in blocks/*.sh; do bash -n $f && echo "bash -n ok $f"; done
echo "== conda lines: dry-run solve (one env, both install lines together, as a user would run them)"
micromamba create -n _dryrun_sashimi --dry-run -y -c conda-forge -c bioconda rmats2sashimiplot pygenometracks pysam bedtools regtools samtools r-base=4.2 r-ggplot2=3.4.4 r-data.table r-gridextra r-gtable seaborn scikit-learn > dry.log 2>&1; echo "dry-run rc=$?"; grep -a -E "r-base|r-ggplot2|rmats2sashimiplot|pygenometracks|regtools|Could not solve|nothing provides|conflict" dry.log | head -12
echo "== names that must NOT exist on conda / PyPI (Skill says so)"
micromamba search -c conda-forge -c bioconda ggsashimi 2>&1 | tail -2
micromamba search -c conda-forge -c bioconda jutils 2>&1 | tail -2
echo "== git URLs"
git ls-remote https://github.com/guigolab/ggsashimi HEAD 2>&1 | head -1
git ls-remote https://github.com/splicebox/Jutils HEAD 2>&1 | head -1
git ls-remote https://github.com/davidaknowles/leafcutter HEAD 2>&1 | head -1
