"""Fresh Phase 2 execution evidence for bio-crispr-screens-drugz-chemogenomic.

Runs the seven prior audit scenarios and two new boundary scenarios against the exact
14e7c1e worktree copy. All generated files stay below this phase2 directory.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parents[1]
DATA = AUDIT / "data"
SOURCE_SKILL = Path(r"F:\OpenScience\wt\crispr-screens-drugz-chemogenomic\crispr-screens\drugz-chemogenomic")
DRUGZ = Path(r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\drugz\drugz.py")
RUN_SKILL = ROOT / "skill_14e7c1e"
WORK = ROOT / "work"
PY = Path(sys.executable)


def run(name: str, args: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    (WORK / f"{name}.stdout.txt").write_text(cp.stdout, encoding="utf-8")
    (WORK / f"{name}.stderr.txt").write_text(cp.stderr, encoding="utf-8")
    return cp


def drugz(name: str, counts: Path, output: Path, control: str, treatment: str, *extra: str) -> subprocess.CompletedProcess[str]:
    return run(name, [str(PY), str(DRUGZ), "-i", str(counts), "-o", str(output), "-c", control, "-x", treatment, "-p", "5", *extra])


def assert_run(cp: subprocess.CompletedProcess[str], name: str) -> None:
    if cp.returncode != 0:
        raise RuntimeError(f"{name} failed with {cp.returncode}: {cp.stderr[-1000:]}")


def output_stats(path: Path) -> dict[str, object]:
    df = pd.read_csv(path, sep="\t")
    return {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "normz_nan": int(df["normZ"].isna().sum()),
        "synth_hits": int((df["fdr_synth"] < 0.05).sum()),
        "supp_hits": int((df["fdr_supp"] < 0.05).sum()),
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    if RUN_SKILL.exists():
        shutil.rmtree(RUN_SKILL)
    shutil.copytree(SOURCE_SKILL, RUN_SKILL, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copy2(DRUGZ, RUN_SKILL / "drugz.py")
    results: dict[str, dict[str, object]] = {}
    truth = dict(line.strip().split("\t", 1) for line in (DATA / "ground_truth.txt").read_text(encoding="utf-8").splitlines())
    sensitizers = set(truth["planted_sensitizers"].split(","))
    suppressors = set(truth["planted_suppressors"].split(","))

    # 1. Canonical vehicle-versus-drug run.
    standard = WORK / "input1_standard.txt"
    cp = drugz("input1_standard", DATA / "synthetic_drug_vehicle_counts.txt", standard, "Veh_r1,Veh_r2,Veh_r3", "Drug_r1,Drug_r2,Drug_r3")
    assert_run(cp, "input1")
    df = pd.read_csv(standard, sep="\t")
    found_sens = set(df.nsmallest(6, "rank_synth")["GENE"])
    found_supp = set(df.nsmallest(6, "rank_supp")["GENE"])
    results["1"] = {"executed": True, "returncode": cp.returncode, "stats": output_stats(standard), "sensitizers_recovered": len(sensitizers & found_sens), "suppressors_recovered": len(suppressors & found_supp)}

    # 2. Real CEGv2 parsing and -r exclusion regression.
    ceg = WORK / "CEGv2.txt"
    urllib.request.urlretrieve("https://raw.githubusercontent.com/hart-lab/bagel/master/CEGv2.txt", ceg)
    ceg_genes = [line.split("\t")[0].strip() for line in ceg.read_text(encoding="utf-8").splitlines()[1:] if line.strip()]
    excluded = WORK / "input2_ceg_excluded.txt"
    cp = drugz("input2_ceg", DATA / "synthetic_drug_vehicle_counts.txt", excluded, "Veh_r1,Veh_r2,Veh_r3", "Drug_r1,Drug_r2,Drug_r3", "-r", ",".join(ceg_genes))
    assert_run(cp, "input2")
    removed = set(df["GENE"]) - set(pd.read_csv(excluded, sep="\t")["GENE"])
    results["2"] = {"executed": True, "returncode": cp.returncode, "cegv2_genes": len(ceg_genes), "removed": len(removed), "removed_nonzero": bool(removed)}

    # 3. Prior multi-dose regression using fresh per-dose drugZ results.
    mid = pd.read_csv(DATA / "synthetic_middose_counts.txt", sep="\t")
    high = pd.read_csv(DATA / "synthetic_drug_vehicle_counts.txt", sep="\t")
    low = mid[["GUIDE", "GENE", "T0", "Veh_r1", "Veh_r2", "Veh_r3"]].copy()
    for n in range(1, 4):
        low[f"LowDose_r{n}"] = np.rint(np.sqrt(mid[f"MidDose_r{n}"].astype(float) * high[f"Veh_r{n}"].astype(float))).astype(int).clip(lower=1)
    three = WORK / "input3_three_dose_counts.txt"
    low = low.merge(mid[["GUIDE", "MidDose_r1", "MidDose_r2", "MidDose_r3"]], on="GUIDE").merge(high[["GUIDE", "Drug_r1", "Drug_r2", "Drug_r3"]], on="GUIDE")
    low.to_csv(three, sep="\t", index=False)
    dose_outputs: dict[str, Path] = {}
    for label, samples in (("low", "LowDose_r1,LowDose_r2,LowDose_r3"), ("mid", "MidDose_r1,MidDose_r2,MidDose_r3"), ("high", "Drug_r1,Drug_r2,Drug_r3")):
        out = WORK / f"input3_{label}.txt"
        cp = drugz(f"input3_{label}", three, out, "Veh_r1,Veh_r2,Veh_r3", samples)
        assert_run(cp, f"input3_{label}")
        dose_outputs[label] = out
    hits = WORK / "input3_hits.tsv"
    cp = run("input3_dose_script", [str(PY), str(RUN_SKILL / "scripts" / "dose_consistent_hits.py"), "--top-dose", "high", "--out", str(hits), f"low={dose_outputs['low']}", f"mid={dose_outputs['mid']}", f"high={dose_outputs['high']}"])
    assert_run(cp, "input3 dose script")
    hit_df = pd.read_csv(hits, sep="\t")
    results["3"] = {"executed": True, "returncode": cp.returncode, "dose_consistent_sensitizers": int(len(hit_df)), "planted_recovered": len(sensitizers & set(hit_df["GENE"])), "false_positives": int(len(set(hit_df["GENE"]) - sensitizers))}

    # 4. Day-0 edge regression: deliberately run the discouraged comparison and measure distortion.
    day0 = WORK / "input4_day0.txt"
    cp = drugz("input4_day0", DATA / "synthetic_day0_vs_drug_counts.txt", day0, "T0", "Drug_r1,Drug_r2,Drug_r3", "-unpaired")
    assert_run(cp, "input4")
    day0_df = pd.read_csv(day0, sep="\t")
    results["4"] = {"executed": True, "returncode": cp.returncode, "day0_synth_hits": int((day0_df["fdr_synth"] < 0.05).sum()), "vehicle_synth_hits": int((df["fdr_synth"] < 0.05).sum())}

    # 5. Small library crash/recovery regression.
    broken = WORK / "input5_default.txt"
    cp_bad = drugz("input5_default", DATA / "synthetic_small200_counts.txt", broken, "Veh_r1,Veh_r2,Veh_r3", "Drug_r1,Drug_r2,Drug_r3")
    repaired = WORK / "input5_quarter_window.txt"
    cp_ok = drugz("input5_quarter", DATA / "synthetic_small200_counts.txt", repaired, "Veh_r1,Veh_r2,Veh_r3", "Drug_r1,Drug_r2,Drug_r3", "--half_window_size", "50")
    assert_run(cp_ok, "input5 recovery")
    results["5"] = {"executed": True, "default_returncode": cp_bad.returncode, "default_has_indexerror": "IndexError: single positional indexer is out-of-bounds" in cp_bad.stderr, "repaired_returncode": cp_ok.returncode, "repaired_stats": output_stats(repaired)}

    # 6. Fresh exact determinism regression.
    rerun_a, rerun_b = WORK / "input6_rerun_a.txt", WORK / "input6_rerun_b.txt"
    cp_a = drugz("input6_a", DATA / "synthetic_drug_vehicle_counts.txt", rerun_a, "Veh_r1,Veh_r2,Veh_r3", "Drug_r1,Drug_r2,Drug_r3")
    cp_b = drugz("input6_b", DATA / "synthetic_drug_vehicle_counts.txt", rerun_b, "Veh_r1,Veh_r2,Veh_r3", "Drug_r1,Drug_r2,Drug_r3")
    assert_run(cp_a, "input6_a"); assert_run(cp_b, "input6_b")
    results["6"] = {"executed": True, "returncodes": [cp_a.returncode, cp_b.returncode], "byte_identical": rerun_a.read_bytes() == rerun_b.read_bytes(), "sha256": [sha256(rerun_a), sha256(rerun_b)]}

    # 7. Scope-boundary decision check: executes the loaded Skill's own routing claims.
    skill_text = (RUN_SKILL / "SKILL.md").read_text(encoding="utf-8")
    results["7"] = {"executed": True, "routing_check": True, "drugz_limited_for_synergy": "Synergy / antagonism detection | Limited (per-drug calling only)" in skill_text, "mle_interaction_redirect": "YES (interaction term in MLE)" in skill_text, "no_fabricated_synergy_metric": "synergy-score" not in skill_text.lower()}

    # 8. Exact shipped example, including its live CEGv2 download and self-check.
    shutil.copy2(DATA / "synthetic_drug_vehicle_counts.txt", RUN_SKILL / "counts.txt")
    cp = run("input8_shipped_example", [str(PY), str(RUN_SKILL / "examples" / "run_drugz.py")], cwd=RUN_SKILL)
    assert_run(cp, "input8 shipped example")
    example_dir = RUN_SKILL / "drugz_output"
    ex_standard = pd.read_csv(example_dir / "drugz_standard.txt", sep="\t")
    ex_clean = pd.read_csv(example_dir / "drugz_ceg_excluded.txt", sep="\t")
    results["8"] = {"executed": True, "returncode": cp.returncode, "example_ceg_removed": int(len(set(ex_standard["GENE"]) - set(ex_clean["GENE"]))), "top50_files_exist": all((example_dir / x).exists() for x in ("top50_sensitizers.tsv", "top50_suppressors.tsv"))}

    # 9. New validation boundary: invalid top-dose name is rejected, whereas out-of-range FDR is not.
    cp_name = run("input9_bad_top", [str(PY), str(RUN_SKILL / "scripts" / "dose_consistent_hits.py"), "--top-dose", "absent", f"low={dose_outputs['low']}", f"mid={dose_outputs['mid']}", f"high={dose_outputs['high']}"])
    invalid = WORK / "input9_invalid_fdr.tsv"
    cp_fdr = run("input9_invalid_fdr", [str(PY), str(RUN_SKILL / "scripts" / "dose_consistent_hits.py"), "--top-dose", "high", "--fdr", "1.5", "--out", str(invalid), f"low={dose_outputs['low']}", f"mid={dose_outputs['mid']}", f"high={dose_outputs['high']}"])
    results["9"] = {"executed": True, "bad_top_rejected": cp_name.returncode != 0 and "--top-dose" in cp_name.stderr, "invalid_fdr_rejected": cp_fdr.returncode != 0, "invalid_fdr_returncode": cp_fdr.returncode, "invalid_fdr_rows": int(len(pd.read_csv(invalid, sep="\t"))) if invalid.exists() else 0}

    (ROOT / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
