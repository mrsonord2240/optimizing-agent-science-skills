#!/bin/bash
# Does the Python package the Skill names ("pyLollipop (limited maintenance)") exist on PyPI? Read-only index query, nothing installed.
for n in pyLollipop pylollipop lollipop-plot; do echo "--- $n"; /f/OpenScience/audit-envs/data-visualization/py.sh -m pip index versions $n 2>&1 | head -3; done
curl -s -o /dev/null -w "pypi.org/pypi/pyLollipop/json -> HTTP %{http_code}\n" https://pypi.org/pypi/pyLollipop/json
