"""Fresh Phase 2 syntax check for every shipped R fence and runnable file."""
from pathlib import Path
import re
import subprocess

root = Path(r"F:/OpenScience/wt/causal-genomics-genomic-sem/causal-genomics/genomic-sem")
run = Path(r"F:/OpenScience/audits/bio-causal-genomics-genomic-sem/run")
rwrap = r"F:/OpenScience/audit-envs/mendelian-randomization-analyst/r_gsem.sh"
sources = [root / "SKILL.md", *sorted((root / "references").glob("*.md"))]
fences = []
for source in sources:
    for i, block in enumerate(re.findall(r"```r\s*\n(.*?)```", source.read_text(encoding="utf-8"), re.S), 1):
        target = run / f"phase2_parse_{source.stem}_{i}.R"
        target.write_text(block, encoding="utf-8")
        fences.append(target)
targets = fences + [root / "examples/genomic_sem_commonfactor.R", root / "scripts/commonfactor_gwas_qsnp.R"]
for target in targets:
    probe = run / "phase2_parse_probe.R"
    probe.write_text(f"parse({target.as_posix()!r}); cat('PARSE PASS: {target.name}\\n')\n", encoding="utf-8")
    result = subprocess.run(["C:/Program Files/Git/bin/bash.exe", rwrap, probe.as_posix()], capture_output=True, text=True)
    if result.returncode != 0 or "PARSE PASS:" not in result.stdout:
        raise SystemExit(f"parse failed for {target}: rc={result.returncode} stdout={result.stdout} stderr={result.stderr}")
subprocess.run(["C:/Program Files/Git/bin/bash.exe", "-n", (root / "examples/mtag_pipeline.sh").as_posix()], check=True)
print(f"PARSE_ALL_PASS r_fences={len(fences)} r_files=2 bash_files=1")
