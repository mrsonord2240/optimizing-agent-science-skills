"""Inputs 4 and 9: independent execution checks for the shipped comut workflow."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys

import matplotlib
import pandas as pd
from PIL import Image


CLASS_MAP = {
    "Missense_Mutation": "Missense",
    "In_Frame_Ins": "Missense",
    "In_Frame_Del": "Missense",
    "Nonsense_Mutation": "Truncating",
    "Frame_Shift_Ins": "Truncating",
    "Frame_Shift_Del": "Truncating",
    "Nonstop_Mutation": "Truncating",
    "Translation_Start_Site": "Truncating",
    "Splice_Site": "Splice",
}


def png_metrics(path: Path) -> tuple[tuple[int, int], float]:
    image = Image.open(path).convert("RGB")
    pixels = list(image.getdata())
    nonwhite = sum(pixel != (255, 255, 255) for pixel in pixels) / len(pixels)
    return image.size, nonwhite


def expect_error(label: str, fn) -> str:
    try:
        fn()
    except Exception as exc:  # noqa: BLE001 - evidence captures exact public error
        print(f"{label}: REJECTED {type(exc).__name__}: {exc}")
        return "REJECTED"
    print(f"{label}: ACCEPTED")
    return "ACCEPTED"


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: audit_comut.py <skill-copy> <public-data> <run-dir>")
    skill = Path(sys.argv[1]).resolve()
    public = Path(sys.argv[2]).resolve()
    run = Path(sys.argv[3]).resolve()
    out = run / "out"
    data = run / "data"
    out.mkdir(parents=True, exist_ok=True)

    script = skill / "scripts" / "comut_plot.py"
    spec = importlib.util.spec_from_file_location("fixed_comut_plot", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load shipped comut_plot.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    print("ENV pandas", pd.__version__, "matplotlib", matplotlib.__version__)

    # Input 4: the archived TCGA-LAML comut request, now through the shipped CLI.
    maf = pd.read_csv(public / "mutations" / "tcga_laml.maf.gz", sep="\t", comment="#", low_memory=False)
    clinical = pd.read_csv(public / "mutations" / "tcga_laml_annot.tsv", sep="\t")
    mapped = maf["Variant_Classification"].map(CLASS_MAP)
    mutations = pd.DataFrame({
        "sample": maf.loc[mapped.notna(), "Tumor_Sample_Barcode"].astype(str),
        "category": maf.loc[mapped.notna(), "Hugo_Symbol"].astype(str),
        "value": mapped.dropna().astype(str),
    }).drop_duplicates()
    cohort = clinical["Tumor_Sample_Barcode"].astype(str).tolist()
    clinical_long = clinical.rename(columns={
        "Tumor_Sample_Barcode": "sample", "FAB_classification": "value"
    }).assign(category="FAB")[['sample', 'category', 'value']].dropna()
    tmb_counts = maf.groupby("Tumor_Sample_Barcode").size().reindex(cohort, fill_value=0)
    tmb = pd.DataFrame({"sample": cohort, "category": "TMB", "value": tmb_counts.to_numpy()})

    plot, top_genes, tmb_max = module.build_comut(mutations, cohort, clinical_long, tmb, top=20)
    expected_order = sorted(cohort, key=lambda sample: (-float(tmb_counts[sample]), sample))
    ticks = [tick.get_text() for tick in plot.axes["Mutations"].get_yticklabels()]
    assert plot.samples == expected_order
    assert len(plot.samples) == len(cohort) == 200
    assert ticks[-1] == top_genes[0]
    assert tmb_max == float(tmb_counts.max())
    direct = out / "i4_laml_comut_direct.png"
    plot.figure.savefig(direct, dpi=120, bbox_inches="tight")
    size, nonwhite = png_metrics(direct)
    assert direct.stat().st_size > 1_000 and nonwhite > 0.01

    mutation_path = data / "i4_mutations.tsv"
    cohort_path = data / "i4_cohort.tsv"
    clinical_path = data / "i4_clinical.tsv"
    tmb_path = data / "i4_tmb.tsv"
    cli_output = out / "i4_laml_comut_cli.png"
    mutations.to_csv(mutation_path, sep="\t", index=False)
    pd.DataFrame({"sample": cohort}).to_csv(cohort_path, sep="\t", index=False)
    clinical_long.to_csv(clinical_path, sep="\t", index=False)
    tmb.to_csv(tmb_path, sep="\t", index=False)
    subprocess.run([
        sys.executable, str(script), "--mutations", str(mutation_path),
        "--cohort", str(cohort_path), "--clinical", str(clinical_path),
        "--tmb", str(tmb_path), "--output", str(cli_output), "--top", "20",
    ], check=True)
    cli_size, cli_nonwhite = png_metrics(cli_output)
    assert cli_output.stat().st_size > 1_000 and cli_nonwhite > 0.01
    print("INPUT4 PASS samples", len(cohort), "top", top_genes[0], "tmb_max", tmb_max,
          "direct", size, round(nonwhite, 4), "cli", cli_size, round(cli_nonwhite, 4))

    # Input 9 (new): minimal CLI path without clinical/TMB, including zero-mutation cohort members.
    cohort9 = ["Z1", "Z2", "Z3", "Z4", "Z5", "Z6", "Z7", "Z8"]
    mutations9 = pd.DataFrame([
        ("Z1", "TP53", "Missense"), ("Z1", "TP53", "Truncating"),
        ("Z2", "TP53", "Missense"), ("Z2", "KRAS", "Missense"),
        ("Z3", "KRAS", "Splice"), ("Z4", "MYC", "Amp"),
        ("Z5", "CDKN2A", "HomDel"), ("Z6", "ALK", "Fusion"),
    ], columns=["sample", "category", "value"])
    plot9, genes9, tmb_max9 = module.build_comut(mutations9, cohort9, top=10)
    burden9 = mutations9.drop_duplicates().groupby("sample").size().reindex(cohort9, fill_value=0)
    expected9 = sorted(cohort9, key=lambda sample: (-float(burden9[sample]), sample))
    assert plot9.samples == expected9
    assert plot9.samples[-2:] == ["Z7", "Z8"]
    assert tmb_max9 == 0.0
    assert [tick.get_text() for tick in plot9.axes["Mutations"].get_yticklabels()][-1] == genes9[0]
    output9 = out / "i9_new_minimal_comut.png"
    plot9.figure.savefig(output9, dpi=140, bbox_inches="tight")
    size9, nonwhite9 = png_metrics(output9)
    assert output9.stat().st_size > 1_000 and nonwhite9 > 0.01
    print("INPUT9 PASS minimal path samples", plot9.samples, "genes", genes9,
          "image", size9, round(nonwhite9, 4))

    # New validation probes: report rather than presuppose behavior.
    bad_sample = mutations9.copy()
    bad_sample.loc[0, "sample"] = "OUTSIDE"
    assert expect_error("VALIDATION unknown mutation sample", lambda: module.build_comut(bad_sample, cohort9)) == "REJECTED"
    bad_class = mutations9.copy()
    bad_class.loc[0, "value"] = "Gain"
    assert expect_error("VALIDATION unknown alteration class", lambda: module.build_comut(bad_class, cohort9)) == "REJECTED"
    assert expect_error("VALIDATION duplicate cohort ID", lambda: module.build_comut(mutations9, cohort9 + ["Z1"])) == "REJECTED"
    empty_id_result = expect_error("VALIDATION empty cohort ID", lambda: module.build_comut(mutations9, cohort9 + [""]))
    negative_tmb = pd.DataFrame({"sample": cohort9, "category": "TMB", "value": [-1, 0, 1, 2, 3, 4, 5, 6]})
    negative_tmb_result = expect_error("VALIDATION negative TMB", lambda: module.build_comut(mutations9, cohort9, tmb=negative_tmb))
    print("INPUT9 VALIDATION OBSERVATION empty_id", empty_id_result, "negative_tmb", negative_tmb_result)
    print("ALL PYTHON REGRESSIONS PASS")


if __name__ == "__main__":
    main()
