# Re-test the Skill's documented install: py3.7 env + `pip install nucleoatac` (lane env -nucleoatac37)
export MAMBA_ROOT_PREFIX=/home/sci/micromamba
$NPNA37/bin/python --version
$NPNA37/bin/pip install nucleoatac > /tmp/pipna.log 2>&1; echo "pip rc=$?"
grep -a -E "CRITICAL|Python version|error:|Failed" /tmp/pipna.log | head -5
