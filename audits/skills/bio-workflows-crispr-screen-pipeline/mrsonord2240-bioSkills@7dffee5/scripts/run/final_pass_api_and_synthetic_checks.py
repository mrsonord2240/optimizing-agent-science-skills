"""Final-pass checks for archived Inputs 4, 5, and 7 plus fresh inputs.

Usage: python final_pass_api_and_synthetic_checks.py
Writes: final_pass_api_and_synthetic_checks.json beside this script.
"""
from __future__ import annotations

import inspect
import json
import subprocess
from pathlib import Path


ROOT = Path(r"F:\OpenScience")
RUN = Path(__file__).parent
SKILL = ROOT / "worktrees" / "bio-workflows-crispr-screen-pipeline-finalpass" / "workflows" / "crispr-screen-pipeline" / "SKILL.md"
GUIDE = SKILL.parent / "usage-guide.md"
EXAMPLE = SKILL.parent / "examples" / "crispr_pipeline.sh"
PYTHON = ROOT / "audit-envs" / "crispr-screen-analyst" / "Scripts" / "python.exe"
JACKS = ROOT / "audit-envs" / "crispr-screen-analyst" / "tools" / "dl" / "JACKS" / "jacks" / "run_JACKS.py"
CHRONOS_PYTHON = ROOT / "audit-envs" / "crispr-screen-analyst" / "tools" / "chronos-venv" / "Scripts" / "python.exe"


def main() -> None:
    skill = SKILL.read_text(encoding="utf-8")
    guide = GUIDE.read_text(encoding="utf-8")
    jacks_help = subprocess.run([str(PYTHON), str(JACKS), "--help"], check=True, capture_output=True, text=True).stdout
    flags = ["--rep_hdr", "--sample_hdr", "--ctrl_sample_hdr", "--sgrna_hdr", "--gene_hdr", "--outprefix", "--apply_w_hp"]
    missing = [flag for flag in flags if flag not in jacks_help]
    assert not missing, missing

    chronos_probe = (
        "import chronos, inspect, json; "
        "print(json.dumps({'constructor': str(inspect.signature(chronos.Chronos)), "
        "'has_alternate_CN': hasattr(chronos, 'alternate_CN')}))"
    )
    chronos_text = subprocess.run(
        [str(CHRONOS_PYTHON), "-c", chronos_probe], check=True, capture_output=True, text=True
    ).stdout.strip()
    chronos = json.loads(chronos_text)
    assert "sequence_map" in chronos["constructor"] and "guide_gene_map" in chronos["constructor"]
    assert "readcounts" in chronos["constructor"] and chronos["has_alternate_CN"]

    # Archived Input 7 and two fresh documentation inputs.
    assert "Step 0: Confirm Made-Once Commitments" in skill
    assert "If baseline, library control classes" in guide
    assert "examples/crispr_pipeline.sh" in skill and EXAMPLE.is_file()
    assert "--permutation-round 10" in skill

    # Archived Input 5's synthetic drug-screen output remains non-degenerate and has the documented FDR field.
    drugz = RUN / "drugz_vs_vehicle.txt"
    header = drugz.read_text(encoding="utf-8").splitlines()[0].split("\t")
    assert "fdr_synth" in header
    assert len(drugz.read_text(encoding="utf-8").splitlines()) > 50

    payload = {
        "jacks_flags": flags,
        "chronos": chronos,
        "input_7_preflight": "present in SKILL.md and usage-guide.md",
        "fresh_example_discovery": "SKILL.md points to existing examples/crispr_pipeline.sh",
        "fresh_mle_guard": "SKILL.md uses --permutation-round 10",
        "synthetic_drugz_rows": len(drugz.read_text(encoding="utf-8").splitlines()) - 1,
    }
    (RUN / "final_pass_api_and_synthetic_checks.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
