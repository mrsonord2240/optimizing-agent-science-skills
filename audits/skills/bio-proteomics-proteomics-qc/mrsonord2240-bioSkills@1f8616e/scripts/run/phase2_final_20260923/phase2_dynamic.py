#!/usr/bin/env python
"""Fresh Phase 2 dynamic audit for bio-proteomics-proteomics-qc.

Inputs: archived audit synthetic MaxQuant/TMT data and a public DIA-NN report.
Usage: python phase2_dynamic.py.  Writes phase2_dynamic_results.json beside this file.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RUN = Path(__file__).resolve().parent
DATA = RUN.parents[1] / "data"
sys.path.insert(0, str(RUN / "scripts"))

from raw_qc import contaminant_fraction, raw_sample_qc, strip_contaminant_rows
from matrix_metrics import (completeness_filter, cross_group_correlation,
                            median_cv_linear, missingness_profile,
                            replicate_correlation)
from pca_batch import pca_batch_check
from diann_level1 import diann_level1


def tmt_channel_balance(plex_matrices):
    """Verbatim runnable block from SKILL.md (apart from this audit docstring)."""
    rows = []
    for plex, m in plex_matrices.items():
        total = m.replace(0, np.nan).sum()
        for channel, fold in (total / total.median()).items():
            rows.append({'plex': plex, 'channel': channel, 'fold_vs_plex_median': fold})
    balance = pd.DataFrame(rows)
    balance['investigate'] = np.abs(np.log2(balance['fold_vs_plex_median'])) > 1
    return balance


def check(condition, detail):
    if not condition:
        raise AssertionError(detail)


def record(results, number, label, details):
    results[str(number)] = {"label": label, "details": details}
    print(f"INPUT {number} PASS: {label}")
    for detail in details:
        print(f"  - {detail}")


def matrix_from_pg(pg, prefix, samples):
    out = pg[[prefix + sample for sample in samples]].replace(0, np.nan).copy()
    out.columns = samples
    return out


def main():
    results = {}
    pg = pd.read_csv(DATA / "proteinGroups.txt", sep="\t", low_memory=False)
    info = pd.read_csv(DATA / "sample_annotation.csv").set_index("sample")
    samples = info.index.tolist()
    groups = info["condition"]
    clean = strip_contaminant_rows(pg)
    raw = matrix_from_pg(clean, "Intensity ", samples)
    lfq = matrix_from_pg(clean, "LFQ intensity ", samples)
    log2 = np.log2(lfq)

    # Input 1: canonical raw-first matrix QC regression.
    raw_out = raw_sample_qc(raw, groups)
    rc = replicate_correlation(log2, groups)
    cv = median_cv_linear(lfq, groups)
    profile = missingness_profile(log2)
    filtered = completeness_filter(log2, groups)
    coords, evr, tests = pca_batch_check(filtered, info)
    check(len(raw_out) == 8 and not raw_out["flag"].any(), "clean raw matrix unexpectedly flagged")
    check(set(rc["status"]) == {"measured"} and len(rc) == 12, "replicate correlation status/count changed")
    check(set(cv["status"]) == {"measured"}, "clean CV status changed")
    check(len(profile) >= 2 and len(filtered) > 500, "missingness/completeness output unavailable")
    check(set(tests["status"]) == {"tested"}, "balanced-batch PCA was not testable")
    record(results, 1, "Canonical raw-first MaxQuant matrix QC", [
        f"{len(clean)} contaminant-filtered rows; {len(rc)} measured replicate pairs",
        f"median CVs {cv.set_index('group')['median_cv_pct'].round(2).to_dict()}",
        f"PCA components {len(evr)}; batch tests {tests['status'].tolist()}",
    ])

    # Input 3: actual DIA-NN report compatibility plus a conformant report for code correctness.
    real_report = pd.read_parquet(DATA / "report.parquet")
    required = {"Run", "RT", "Predicted.RT", "FWHM", "Quantity.Quality", "Global.Q.Value"}
    missing = sorted(required - set(real_report.columns))
    try:
        diann_level1(real_report)
        real_result = "unexpectedly accepted"
    except KeyError as exc:
        real_result = f"clear KeyError: {exc}"
    check(missing == ["FWHM", "Predicted.RT", "Quantity.Quality"], f"unexpected archived DIA-NN columns: {missing}")
    # A minimal DIA-NN-shaped fixture tests the advertised implementation without relabeling the real report.
    fixture = real_report[["Run", "RT", "Global.Q.Value"]].copy()
    fixture["Predicted.RT"] = fixture["RT"] + 0.01 * np.sin(np.arange(len(fixture)))
    fixture["FWHM"] = 0.05
    fixture["Quantity.Quality"] = 0.90
    fixture_path = RUN / "diann_conformant_fixture.tsv"
    fixture.to_csv(fixture_path, sep="\t", index=False)
    diann = diann_level1(fixture)
    check(len(diann) == 8 and (diann["n_precursors"] > 100).all(), "conformant DIA-NN fixture did not yield eight substantive runs")
    check((diann["rt_fit_r2"] > 0.99).all() and not diann["flag"].any(), "conformant DIA-NN fixture unexpectedly failed")
    record(results, 3, "DIA-NN Level-1 report compatibility and execution", [
        f"archived real report missing required columns {missing}; direct CLI failure was {real_result}",
        f"conformant fixture: runs={len(diann)}, R2 range {diann['rt_fit_r2'].min():.4f}-{diann['rt_fit_r2'].max():.4f}; no flags",
    ])

    # Input 4: failed loading must be visible only in raw, and contaminant stripping must work.
    failed = pd.read_csv(DATA / "proteinGroups_failed.txt", sep="\t", low_memory=False)
    failed_clean = strip_contaminant_rows(failed)
    failed_raw = matrix_from_pg(failed_clean, "Intensity ", samples)
    failed_lfq = matrix_from_pg(failed_clean, "LFQ intensity ", samples)
    raw_flags = raw_sample_qc(failed_raw, groups).query("flag").index.tolist()
    lfq_flags = raw_sample_qc(failed_lfq, groups).query("flag").index.tolist()
    check(raw_flags == ["T4"], f"raw failure detection expected T4, got {raw_flags}")
    check(lfq_flags == [], f"normalised LFQ should hide the planted failure, got {lfq_flags}")
    check(len(failed_clean) < len(failed), "contaminant rows were not removed")
    fractions = contaminant_fraction(failed, ["Intensity " + s for s in samples])
    record(results, 4, "Raw loading failure versus MaxLFQ boundary", [
        f"raw flags={raw_flags}; LFQ flags={lfq_flags}",
        f"rows {len(failed)} -> {len(failed_clean)} after contaminant/decoy stripping",
        f"contaminant percent range {fractions.min():.2f}-{fractions.max():.2f}",
    ])

    # Input 5: the SKILL.md inline TMT balance block, including a planted underloaded channel.
    plex_a = pd.read_csv(DATA / "tmt_plexA.csv", index_col=0)
    plex_b = pd.read_csv(DATA / "tmt_plexB.csv", index_col=0)
    baseline_tmt = tmt_channel_balance({"A": plex_a, "B": plex_b})
    stressed_a = plex_a.copy()
    stressed_a.iloc[:, 2] *= 0.30
    stressed_tmt = tmt_channel_balance({"A": stressed_a, "B": plex_b})
    planted = stressed_tmt[(stressed_tmt["plex"] == "A") & (stressed_tmt["channel"] == stressed_a.columns[2])]
    check(not baseline_tmt["investigate"].any(), "baseline TMT plexes should not flag")
    check(len(planted) == 1 and bool(planted["investigate"].iloc[0]), "planted TMT channel was not flagged")
    record(results, 5, "TMT within-plex channel balance", [
        f"baseline flags={int(baseline_tmt['investigate'].sum())} across {len(baseline_tmt)} channel rows",
        f"planted A/{stressed_a.columns[2]} fold={planted['fold_vs_plex_median'].iloc[0]:.3f} flagged",
    ])

    # Input 6: fully confounded batch; PCA can describe it but the decision must be a stop.
    conf_info = info.copy()
    conf_info["batch"] = np.where(conf_info["condition"] == "Control", "day1", "day2")
    conf_coords, _, conf_tests = pca_batch_check(filtered, conf_info)
    cross = pd.crosstab(conf_info["batch"], conf_info["condition"])
    check((cross.to_numpy() == np.array([[4, 0], [0, 4]])).all(), "synthetic design is not fully confounded")
    check((conf_tests["status"] == "tested").all(), "confounded PCA association was not calculated")
    record(results, 6, "Fully confounded batch/condition stress boundary", [
        f"batch-by-condition table={cross.to_dict()}",
        f"PCA returned {len(conf_coords)} samples; skill guidance requires report-and-stop rather than correction/testing",
    ])

    # Input 7: swap detection function supplied by Phase 1 must find precisely the swapped pair.
    swapped = pg.copy()
    for family in ["Intensity ", "iBAQ ", "LFQ intensity ", "MS/MS count "]:
        a, b = family + "C2", family + "T3"
        swapped[a], swapped[b] = swapped[b].copy(), swapped[a].copy()
    swapped_clean = strip_contaminant_rows(swapped)
    swapped_log2 = np.log2(matrix_from_pg(swapped_clean, "LFQ intensity ", samples))
    swaps = cross_group_correlation(swapped_log2, groups)
    flagged_swaps = sorted(swaps.loc[swaps["possible_swap"] == True, "sample"].tolist())
    check(flagged_swaps == ["C2", "T3"], f"swap detection expected C2/T3, got {flagged_swaps}")
    record(results, 7, "Suspected sample-swap regression", [
        f"possible_swap samples={flagged_swaps}",
        "cross-group result is a relabel candidate, not an automatic exclusion",
    ])

    # Input 8: repeated identical PCA calls must produce identical numerical artefacts.
    first = pca_batch_check(filtered, info)
    second = pca_batch_check(filtered, info)
    check(first[0].equals(second[0]) and np.array_equal(first[1], second[1]) and first[2].equals(second[2]),
          "identical fixed-seed PCA calls differed")
    record(results, 8, "PCA reproducibility adversarial regression", [
        "two pca_batch_check calls returned byte-identical frames and variance ratios",
        "full SVD with random_state=0 remains deterministic on the audit matrix",
    ])

    # Input 9 (new): mixed replicate/singleton design must expose machine-readable statuses.
    mixed_samples = ["C1", "C2", "T1", "T2"]
    mixed_groups = pd.Series(["Control", "Control", "Treated", "Treated_drug"], index=mixed_samples)
    mixed_lfq = lfq[mixed_samples]
    mixed_log2 = np.log2(mixed_lfq)
    mixed_raw = raw[mixed_samples]
    mixed_rc = replicate_correlation(mixed_log2, mixed_groups)
    mixed_cv = median_cv_linear(mixed_lfq, mixed_groups)
    mixed_info = pd.DataFrame({"batch": mixed_groups}, index=mixed_samples)
    _, _, mixed_tests = pca_batch_check(mixed_log2.dropna(how="any"), mixed_info)
    mixed_raw_qc = raw_sample_qc(mixed_raw, mixed_groups)
    check((mixed_rc["status"] == "not_measurable_n1").sum() == 2, "singleton correlation statuses missing")
    check((mixed_cv["status"] == "not_measurable_n1").sum() == 2, "singleton CV statuses missing")
    check((mixed_tests["status"] == "not_testable").all(), "mixed singleton PCA status missing")
    check((mixed_raw_qc.loc[["T1", "T2"], "loading_rule"] == "fallback_all_samples").all(), "fallback rule missing")
    record(results, 9, "New mixed 2/1/1 replicate-design edge case", [
        f"correlation statuses={mixed_rc['status'].tolist()}; CV statuses={mixed_cv['status'].tolist()}",
        f"PCA statuses={mixed_tests['status'].tolist()}; singleton loading rules fall back to ALL",
    ])

    # Input 10 (new): all-singleton design must hard-stop correlation/CV and label PCA untestable.
    one_samples = ["C1", "T1", "T2"]
    one_groups = pd.Series(["A", "B", "C"], index=one_samples)
    one_lfq = lfq[one_samples]
    one_log2 = np.log2(one_lfq)
    one_info = pd.DataFrame({"batch": one_groups}, index=one_samples)
    errors = []
    for function, matrix in [(replicate_correlation, one_log2), (median_cv_linear, one_lfq)]:
        try:
            function(matrix, one_groups)
        except ValueError as exc:
            errors.append(str(exc))
    one_qc = raw_sample_qc(raw[one_samples], one_groups)
    _, _, one_tests = pca_batch_check(one_log2.dropna(how="any"), one_info)
    check(len(errors) == 2 and all("not measurable" in message or "needs >=2" in message for message in errors),
          "all-singleton correlation/CV did not hard-stop with a clear message")
    check((one_qc["loading_rule"] == "fallback_all_samples").all(), "all-singleton loading fallback missing")
    check((one_tests["status"] == "not_testable").all(), "all-singleton PCA not labelled untestable")
    record(results, 10, "New all-singleton no-replicate boundary", [
        "replicate correlation and linear CV both raise explicit not-measurable errors",
        f"PCA statuses={one_tests['status'].tolist()}; all loading rules use fallback_all_samples",
    ])

    with (RUN / "phase2_dynamic_results.json").open("w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2)


if __name__ == "__main__":
    main()
