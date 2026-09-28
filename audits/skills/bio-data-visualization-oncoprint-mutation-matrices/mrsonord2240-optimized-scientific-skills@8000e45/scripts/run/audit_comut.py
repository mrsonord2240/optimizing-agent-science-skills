"""Inputs 4, 9, 10, and 11: independent checks of the comut workflow."""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path
import subprocess
import sys

import matplotlib
from matplotlib import pyplot as plt
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


def rendered_texts(text_artists, figure) -> list[str]:
    """Return visible, non-empty text with a non-zero rendered bounding box."""
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    return [
        artist.get_text()
        for artist in text_artists
        if artist.get_visible()
        and artist.get_text()
        and artist.get_window_extent(renderer).width > 0
        and artist.get_window_extent(renderer).height > 0
    ]


def run_cli_expect_error(command: list[str], expected: str, label: str) -> str:
    """Run a deliberately invalid CLI request and retain its exact transcript."""
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    transcript = f"[{label}] returncode={result.returncode}\nSTDOUT\n{result.stdout}\nSTDERR\n{result.stderr}\n"
    if result.returncode == 0:
        raise AssertionError(f"{label} unexpectedly succeeded")
    if expected not in result.stderr:
        raise AssertionError(f"{label} did not report {expected!r}: {result.stderr}")
    print(f"{label}: REJECTED returncode={result.returncode} expected={expected!r}")
    return transcript


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
    legend = plot.axes["Mutations"].get_legend()
    assert legend is not None
    legend_text = set(rendered_texts(legend.get_texts(), plot.figure))
    assert {"Mutations", "Clinical"}.issubset(legend_text)
    assert set(mutations["value"]).issubset(legend_text)
    assert set(clinical_long["value"].dropna().astype(str)).issubset(legend_text)
    assert not rendered_texts(plot.axes["Mutations"].get_xticklabels(), plot.figure)
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
    assert empty_id_result == "REJECTED"
    assert negative_tmb_result == "REJECTED"
    print("INPUT9 VALIDATION OBSERVATION empty_id", empty_id_result, "negative_tmb", negative_tmb_result)

    # Input 10 (genuinely new): exact 50/51 auto-label boundary, override, and
    # a mixed mutation/clinical legend. This probes policy edges not used by
    # the shipped test's 30/61 cohorts.
    cohort10 = [f"B{index:02d}" for index in range(1, 52)]
    mutations10 = pd.DataFrame(
        [
            (sample, gene, alteration)
            for index, sample in enumerate(cohort10[:20])
            for gene, alteration in [
                ("TP53", "Missense" if index % 2 == 0 else "Truncating"),
                ("KRAS", "Splice" if index % 3 == 0 else "Missense"),
            ]
        ],
        columns=["sample", "category", "value"],
    )
    clinical10 = pd.DataFrame(
        {
            "sample": cohort10,
            "category": "Subtype",
            "value": ["Alpha", "Beta", "Gamma", "Delta"] * 12 + ["Alpha", "Beta", "Gamma"],
        }
    )
    plot10_50, _, _ = module.build_comut(
        mutations10, cohort10[:50], clinical=clinical10.iloc[:50], top=2
    )
    labels10_50 = rendered_texts(
        plot10_50.axes["Mutations"].get_xticklabels(), plot10_50.figure
    )
    assert labels10_50 == plot10_50.samples and len(labels10_50) == 50
    legend10 = plot10_50.axes["Mutations"].get_legend()
    assert legend10 is not None
    legend_text10 = set(rendered_texts(legend10.get_texts(), plot10_50.figure))
    assert {"Mutations", "Clinical", "Missense", "Truncating", "Splice"}.issubset(legend_text10)
    assert {"Alpha", "Beta", "Gamma", "Delta"}.issubset(legend_text10)
    output10_50 = out / "i10_boundary_50_labels.png"
    plot10_50.figure.savefig(output10_50, dpi=120, bbox_inches="tight")

    plot10_51, _, _ = module.build_comut(
        mutations10, cohort10, clinical=clinical10, top=2
    )
    assert not rendered_texts(
        plot10_51.axes["Mutations"].get_xticklabels(), plot10_51.figure
    )
    output10_51 = out / "i10_boundary_51_hidden.png"
    plot10_51.figure.savefig(output10_51, dpi=120, bbox_inches="tight")

    plot10_forced, _, _ = module.build_comut(
        mutations10,
        cohort10,
        clinical=clinical10,
        top=2,
        sample_label_threshold=51,
    )
    forced_labels = rendered_texts(
        plot10_forced.axes["Mutations"].get_xticklabels(), plot10_forced.figure
    )
    assert forced_labels == plot10_forced.samples and len(forced_labels) == 51
    output10_forced = out / "i10_boundary_51_forced.png"
    plot10_forced.figure.savefig(output10_forced, dpi=120, bbox_inches="tight")

    plot10_zero, _, _ = module.build_comut(
        mutations10, cohort10[:50], top=2, sample_label_threshold=0
    )
    assert not rendered_texts(
        plot10_zero.axes["Mutations"].get_xticklabels(), plot10_zero.figure
    )
    for output in [output10_50, output10_51, output10_forced]:
        image_size, image_nonwhite = png_metrics(output)
        assert output.stat().st_size > 1_000 and image_nonwhite > 0.01
        print("INPUT10 IMAGE", output.name, image_size, round(image_nonwhite, 4))
    print("INPUT10 PASS exact 50 visible; 51 hidden; override 51 visible; zero hides; unified legend rendered")

    # Input 11 (genuinely new): normalization collisions plus CLI-level empty
    # IDs and non-finite burden values. Previous probes called build_comut
    # directly; these cases verify file parsing reaches the same guardrails.
    cohort11 = ["N01", "N02", "N03"]
    mutations11 = pd.DataFrame(
        [(" N01 ", "TP53", "Missense"), ("N02", "KRAS", "Splice")],
        columns=["sample", "category", "value"],
    )
    clinical11 = pd.DataFrame(
        [("N01", "Group", "A"), (" N02 ", "Group", "B"), ("N03", "Group", "A")],
        columns=["sample", "category", "value"],
    )
    tmb11 = pd.DataFrame(
        [(" N01", "TMB", 2.5), ("N02 ", "TMB", 1.0), ("N03", "TMB", 0.0)],
        columns=["sample", "category", "value"],
    )
    plot11, _, tmb_max11 = module.build_comut(
        mutations11, cohort11, clinical=clinical11, tmb=tmb11, top=2
    )
    assert plot11.samples == ["N01", "N02", "N03"] and tmb_max11 == 2.5
    output11 = out / "i11_normalized_ids.png"
    plot11.figure.savefig(output11, dpi=140, bbox_inches="tight")
    size11, nonwhite11 = png_metrics(output11)
    assert output11.stat().st_size > 1_000 and nonwhite11 > 0.01

    assert expect_error(
        "INPUT11 duplicate after stripping",
        lambda: module.build_comut(mutations11, ["N01", " N01 ", "N03"]),
    ) == "REJECTED"
    for bad_value in [float("nan"), float("inf"), float("-inf"), -0.01]:
        bad_tmb11 = tmb11.copy()
        bad_tmb11.loc[0, "value"] = bad_value
        assert expect_error(
            f"INPUT11 invalid TMB {bad_value!r}",
            lambda bad_tmb11=bad_tmb11: module.build_comut(
                mutations11, cohort11, tmb=bad_tmb11
            ),
        ) == "REJECTED"

    i11 = data / "i11"
    i11.mkdir(parents=True, exist_ok=True)
    mutation11_path = i11 / "mutations.tsv"
    clinical11_path = i11 / "clinical.tsv"
    tmb11_path = i11 / "tmb.tsv"
    cohort11_path = i11 / "cohort.tsv"
    mutations11.to_csv(mutation11_path, sep="\t", index=False)
    clinical11.to_csv(clinical11_path, sep="\t", index=False)
    tmb11.to_csv(tmb11_path, sep="\t", index=False)
    pd.DataFrame({"sample": cohort11}).to_csv(cohort11_path, sep="\t", index=False)
    output11_cli = out / "i11_normalized_ids_cli.png"
    base_command = [
        sys.executable,
        str(script),
        "--mutations",
        str(mutation11_path),
        "--cohort",
        str(cohort11_path),
        "--clinical",
        str(clinical11_path),
        "--tmb",
        str(tmb11_path),
    ]
    subprocess.run(base_command + ["--output", str(output11_cli)], check=True)
    cli11_size, cli11_nonwhite = png_metrics(output11_cli)
    assert output11_cli.stat().st_size > 1_000 and cli11_nonwhite > 0.01

    transcripts = []
    duplicate_cohort_path = i11 / "cohort_duplicate_after_strip.tsv"
    pd.DataFrame({"sample": ["N01", " N01 ", "N03"]}).to_csv(
        duplicate_cohort_path, sep="\t", index=False
    )
    duplicate_command = base_command.copy()
    duplicate_command[duplicate_command.index(str(cohort11_path))] = str(duplicate_cohort_path)
    duplicate_output = out / "i11_should_not_exist_duplicate.png"
    transcripts.append(
        run_cli_expect_error(
            duplicate_command + ["--output", str(duplicate_output)],
            "unique after normalization",
            "INPUT11 CLI duplicate-after-strip cohort ID",
        )
    )

    blank_cohort_path = i11 / "cohort_blank.tsv"
    pd.DataFrame({"sample": ["N01", "   ", "N03"]}).to_csv(
        blank_cohort_path, sep="\t", index=False, quoting=csv.QUOTE_ALL
    )
    blank_command = base_command.copy()
    blank_command[blank_command.index(str(cohort11_path))] = str(blank_cohort_path)
    blank_output = out / "i11_should_not_exist_blank.png"
    transcripts.append(
        run_cli_expect_error(
            blank_command + ["--output", str(blank_output)],
            "must not be empty or NA",
            "INPUT11 CLI whitespace-only cohort ID",
        )
    )

    invalid_tmb_path = i11 / "tmb_infinite.tsv"
    invalid_tmb11 = tmb11.copy()
    invalid_tmb11.loc[0, "value"] = "inf"
    invalid_tmb11.to_csv(invalid_tmb_path, sep="\t", index=False)
    invalid_tmb_command = base_command.copy()
    invalid_tmb_command[invalid_tmb_command.index(str(tmb11_path))] = str(invalid_tmb_path)
    invalid_tmb_output = out / "i11_should_not_exist_tmb.png"
    transcripts.append(
        run_cli_expect_error(
            invalid_tmb_command + ["--output", str(invalid_tmb_output)],
            "finite and non-negative",
            "INPUT11 CLI infinite TMB",
        )
    )
    assert not any(
        path.exists() for path in [duplicate_output, blank_output, invalid_tmb_output]
    )
    (out / "i11_validation_cli.log").write_text("\n".join(transcripts), encoding="utf-8")
    print(
        "INPUT11 PASS normalized IDs",
        plot11.samples,
        "direct",
        size11,
        round(nonwhite11, 4),
        "cli",
        cli11_size,
        round(cli11_nonwhite, 4),
        "and invalid file-level values rejected",
    )

    for figure in [
        plot.figure,
        plot9.figure,
        plot10_50.figure,
        plot10_51.figure,
        plot10_forced.figure,
        plot10_zero.figure,
        plot11.figure,
    ]:
        plt.close(figure)
    print("ALL PYTHON REGRESSIONS PASS")


if __name__ == "__main__":
    main()
