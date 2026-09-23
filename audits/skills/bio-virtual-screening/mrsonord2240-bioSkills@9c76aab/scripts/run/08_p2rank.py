import shutil
import subprocess
from pathlib import Path

data = Path(r"F:\OpenScience\audits\bio-virtual-screening\data\p2rank")
data.mkdir(parents=True, exist_ok=True)
fixture = Path(r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\smoke\dock\3ptb.pdb")
receptor = data / "receptor.pdb"
shutil.copy2(fixture, receptor)
p2rank = Path(r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\tools\p2rank\p2rank_2.5.1")
cmd = ["java", "-cp", str(p2rank / "bin" / "p2rank.jar") + ";" + str(p2rank / "bin" / "lib" / "*"),
       "cz.siret.prank.program.Main", "predict", "-f", str(receptor), "-o", str(data / "pockets")]
result = subprocess.run(cmd, capture_output=True, text=True, check=True)
csvs = list((data / "pockets").rglob("*.csv"))
assert csvs, result.stdout + result.stderr
assert any("center" in item.read_text(errors="replace").lower() for item in csvs)
print(f"P2RANK=PASS csvs={len(csvs)}")
