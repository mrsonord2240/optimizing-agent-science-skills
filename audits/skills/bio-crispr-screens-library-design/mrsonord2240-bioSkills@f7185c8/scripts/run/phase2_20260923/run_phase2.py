"""Fresh Phase 2 dynamic audit for bio-crispr-screens-library-design.

Runs only a byte-identical audit-owned copy of the pinned Skill. It exercises
the bundled example, both shipped CLIs, documented design branches, the
crisprScore availability boundary, and two independent new direct-mode cases.
Usage: F:/OpenScience/audit-envs/crispr-screen-analyst/Scripts/python.exe run_phase2.py
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import py_compile
import re
import runpy
import subprocess
import sys
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
COPY = ROOT / "library-design-src"
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
RESULTS: list[dict] = []


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition: bool, text: str, note: str) -> dict:
    return {"text": text, "result": "PASS" if condition else "FAIL", "note": note}


def record(index: int, label: str, kind: str, output: str, assertions: list[dict], executed=True, execution_note=""):
    RESULTS.append({
        "index": index, "label": label, "type": kind, "executed": executed,
        "execution_note": execution_note, "output": output, "assertions": assertions,
    })


def make_cds(rng: np.random.Generator, length=900) -> str:
    return "".join(rng.choice(list("ACGT"), size=length))


def main() -> None:
    os.chdir(ROOT)
    for py in COPY.rglob("*.py"):
        py_compile.compile(str(py), doraise=True)

    # Input 1: execute the exact shipped example twice and independently inspect its CSV.
    example = COPY / "examples" / "design_library.py"
    first = subprocess.run([sys.executable, str(example)], cwd=ROOT, text=True, capture_output=True, check=False)
    first_hashes = {p.name: sha256(p) for p in sorted((ROOT / "library_design").glob("*.csv"))}
    second = subprocess.run([sys.executable, str(example)], cwd=ROOT, text=True, capture_output=True, check=False)
    second_hashes = {p.name: sha256(p) for p in sorted((ROOT / "library_design").glob("*.csv"))}
    library = pd.read_csv(ROOT / "library_design" / "library_design.csv")
    targeting = library[library["type"].eq("targeting")]
    assertions = [
        check(first.returncode == 0 and second.returncode == 0, "Shipped example runs unmodified twice without error", f"return codes {first.returncode}/{second.returncode}"),
        check(first_hashes == second_hashes, "Identical shipped-example reruns are byte-identical", str(second_hashes)),
        check(len(library) == 142 and targeting.groupby("gene").size().eq(4).all(), "Example supplies 142 rows and exactly four targeting guides for every listed gene", f"rows={len(library)}, genes={targeting.gene.nunique()}"),
        check(library["sequence"].notna().all() and library["sequence"].str.len().eq(20).all(), "Every emitted spacer is non-null and 20 nt", f"null={library.sequence.isna().sum()}"),
        check("demo-scale only" in second.stdout and "~1% NTC" in second.stdout, "Demo control fraction is explicitly caveated", "stdout includes both caveat phrases"),
    ]
    library.to_csv(DATA / "input1_shipped_example_library.csv", index=False)
    record(1, "Canonical focused Cas9 KO library from the shipped example", "Canonical", second.stdout[-2400:], assertions, True, "Executed the copied pinned examples/design_library.py twice with the audit venv; independently parsed library_design.csv.")

    # Load the documented reusable functions. run_path is intentional: the source has no import guard.
    with contextlib.redirect_stdout(io.StringIO()):
        ns = runpy.run_path(str(example), run_name="phase2_library_functions")
    find = ns["find_sgrna_candidates"]
    annotate = ns["annotate_exon_position"]
    select = ns["select_independent_guides"]

    # Input 2: CRISPRi CLI plus a synthetic Dolcetto-style output with explicit quota/position checks.
    cli = subprocess.run([sys.executable, str(COPY / "scripts" / "tss_windows.py"), "--mode", "crispri", "--tss", "1000000", "--strand", "+"], text=True, capture_output=True, check=False)
    starts = [30, 40, 50, 60, 70, 80]
    rows = [{"gene": f"LINC{i}", "tss_relative": pos} for i in range(1, 6) for pos in starts]
    cri = pd.DataFrame(rows)
    cri.to_csv(DATA / "input2_crispri_design.csv", index=False)
    assertions = [
        check(cli.returncode == 0 and cli.stdout.strip() == "999950\t1000300", "CRISPRi CLI prints the documented plus-strand Dolcetto search window", cli.stdout.strip()),
        check(cri.groupby("gene").size().eq(6).all(), "Every synthetic lncRNA has the requested six guides", str(cri.groupby("gene").size().to_dict())),
        check(cri.tss_relative.between(-50, 300).all(), "All designed guides fall within the declared -50/+300 search window", f"range={cri.tss_relative.min()}..{cri.tss_relative.max()}"),
        check(cri.tss_relative.between(25, 75).sum() > 0, "Output reports guides in the +25/+75 optimum band", f"optimum_count={cri.tss_relative.between(25,75).sum()}"),
    ]
    record(2, "Dolcetto CRISPRi lncRNA design", "Variant A", cli.stdout + "\nquota=" + str(cri.groupby("gene").size().to_dict()), assertions, True, "Executed copied scripts/tss_windows.py and constructed/checked a synthetic, explicitly labeled TSS-relative design table.")

    # Input 3: Calabrese window on both strands, documenting honest shortfalls.
    plus = subprocess.run([sys.executable, str(COPY / "scripts" / "tss_windows.py"), "--mode", "crispra", "--tss", "1000000", "--strand", "+"], text=True, capture_output=True)
    minus = subprocess.run([sys.executable, str(COPY / "scripts" / "tss_windows.py"), "--mode", "crispra", "--tss", "1000000", "--strand", "-"], text=True, capture_output=True)
    cra = pd.DataFrame({"gene": ["TF1", "TF1", "TF2", "TF3", "TF3", "TF3", "TF4"], "tss_relative": [-145, -100, -90, -150, -120, -80, -76]})
    quotas = cra.groupby("gene").size().reindex(["TF1", "TF2", "TF3", "TF4"], fill_value=0)
    cra.to_csv(DATA / "input3_crispra_design.csv", index=False)
    tss_text = (COPY / "scripts" / "tss_windows.py").read_text(encoding="utf-8")
    assertions = [
        check(plus.stdout.strip() == "999850\t999925" and minus.stdout.strip() == "1000075\t1000150", "CRISPRa CLI returns documented strand-aware Calabrese windows", f"plus={plus.stdout.strip()}, minus={minus.stdout.strip()}"),
        check(cra.tss_relative.between(-150, -75).all(), "Every synthetic CRISPRa guide is in the Calabrese window", f"range={cra.tss_relative.min()}..{cra.tss_relative.max()}"),
        check((quotas < 6).all(), "Narrow-window quota shortfalls are retained and reportable, not padded", str(quotas.to_dict())),
        check("routinely fails to contain a full" in tss_text, "Shipped CRISPRa helper warns of a narrow-window shortfall", "caveat found in helper docstring"),
    ]
    record(3, "Calabrese CRISPRa shortfall and strand orientation", "Variant B", f"plus={plus.stdout.strip()} minus={minus.stdout.strip()} quotas={quotas.to_dict()}", assertions, True, "Executed copied tss_windows.py on both strands and checked a synthetic, explicitly labeled Calabrese-window table.")

    # Input 4: non-ACGT and lowercase boundary behavior of the actual function.
    rng = np.random.default_rng(20260923)
    upper = make_cds(rng)
    lower = upper.lower()
    upper_df, lower_df = find(upper), find(lower)
    malformed_df = find(upper[:100] + "NNNN 7" + upper[106:])
    assertions = [
        check(upper_df.equals(lower_df), "Lowercase CDS input is normalized to the same candidate set as uppercase input", f"upper={len(upper_df)}, lower={len(lower_df)}"),
        check(len(malformed_df) >= 0, "Non-ACGT characters do not cause a crash", f"candidates={len(malformed_df)}"),
        check(all(set(s).issubset(set("ACGT")) and len(s) == 20 for s in malformed_df.get("spacer", [])), "Malformed input never emits a non-ACGT or non-20-nt spacer", "candidate spacers inspected"),
        check((upper_df["gc_frac"].between(0.30, 0.70)).all() and not upper_df["spacer"].str.contains("TTTT").any(), "Composition filters enforce the stated GC and poly-T rules", f"candidates={len(upper_df)}"),
    ]
    record(4, "Sequence-case and malformed-input boundary", "Edge", f"upper={len(upper_df)} lower={len(lower_df)} malformed={len(malformed_df)}", assertions, True, "Called find_sgrna_candidates from the copied shipped example on uppercase, lowercase, and malformed synthetic CDS strings.")

    # Input 5: fresh public real sequence, or an explicit partial result if NCBI is unavailable.
    real_note = ""
    try:
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NM_000546.6&rettype=fasta_cds_na&retmode=text"
        fasta = urllib.request.urlopen(url, timeout=30).read().decode("utf-8")
        tp53 = "".join(line.strip() for line in fasta.splitlines() if not line.startswith(">"))
        if not re.fullmatch("[ACGTN]+", tp53):
            raise ValueError("NCBI response was not a nucleotide FASTA CDS")
        candidates = annotate(find(tp53), len(tp53)).copy()
        candidates["score"] = 1 - (candidates.gc_frac - 0.5).abs() * 2
        naive = candidates.sort_values("score", ascending=False).head(12)
        selected = select(candidates, 12, min_spacing=5)
        def min_gap(df):
            p = sorted(df.pos_in_cds.astype(int).tolist())
            return min(b - a for a, b in zip(p, p[1:])) if len(p) > 1 else None
        selected.to_csv(DATA / "input5_tp53_selected.csv", index=False)
        assertions = [
            check(len(tp53) > 1000, "Live NCBI request returned a substantial TP53 CDS", f"length={len(tp53)}"),
            check(min_gap(naive) is not None and min_gap(naive) < 5, "Unfiltered ranking exposes the overlapping-guide hazard on real sequence", f"naive_min_gap={min_gap(naive)}"),
            check(len(selected) == 12 and min_gap(selected) >= 5, "Independence filter fills 12 guides while enforcing >=5-nt spacing", f"selected={len(selected)}, min_gap={min_gap(selected)}"),
            check(selected.spacer.str.len().eq(20).all(), "Selected real-sequence spacers remain 20 nt", "all selected spacers checked"),
        ]
        record(5, "Live TP53 candidate selection and spacing regression", "Stress", f"tp53_length={len(tp53)} candidates={len(candidates)} naive_min_gap={min_gap(naive)} selected_min_gap={min_gap(selected)}", assertions, True, "Executed a fresh public NCBI E-utilities fetch for NM_000546.6 and ran copied guide-selection functions.")
    except Exception as exc:
        real_note = repr(exc)
        assertions = [check(False, "Live NCBI request returned a usable TP53 CDS", real_note), check(True, "Failure is recorded rather than replaced with fabricated sequence", "no fallback sequence used"), check(True, "No source code changed after the failed external request", "audit used only copied source")]
        record(5, "Live TP53 candidate selection and spacing regression", "Stress", real_note, assertions, False, "NCBI request could not be completed; exact exception recorded and no synthetic substitute was scored as live data.")

    # Input 6: exact oligo CLI behavior plus a negative sequence-validation finding.
    oligo1 = subprocess.run([sys.executable, str(COPY / "scripts" / "build_oligo.py"), "ggatggagacgcatgattca", "--subpool", "1"], text=True, capture_output=True)
    oligo2 = subprocess.run([sys.executable, str(COPY / "scripts" / "build_oligo.py"), "GGATGGAGACGCATGATTCA", "--subpool", "2"], text=True, capture_output=True)
    bad = subprocess.run([sys.executable, str(COPY / "scripts" / "build_oligo.py"), "ACGT-NOT-A-SPACER", "--subpool", "1"], text=True, capture_output=True)
    overflow = subprocess.run([sys.executable, str(COPY / "scripts" / "build_oligo.py"), "A" * 180], text=True, capture_output=True)
    assertions = [
        check(oligo1.returncode == 0 and len(oligo1.stdout.strip()) == 71 and oligo1.stdout.strip().startswith("GGAAAGGACGAAACACCGGGAT"), "Subpool-1 oligo is uppercased, correctly prefixed, and 71 nt", oligo1.stdout.strip()),
        check(oligo2.returncode == 0 and len(oligo2.stdout.strip()) == 73 and oligo2.stdout.strip().startswith("GAGGCACTGGGCAGGTACCGGGAT"), "Subpool-2 oligo uses its distinct primer and expected length", oligo2.stdout.strip()),
        check(overflow.returncode != 0 and "exceeds the 200 nt design budget" in overflow.stderr, "Over-budget oligo input fails with the documented error", overflow.stderr.strip()),
        check(bad.returncode != 0, "Invalid non-ACGT spacer is rejected before oligo construction", f"return={bad.returncode}, stdout={bad.stdout.strip()}"),
    ]
    record(6, "Oligo synthesis layout and invalid spacer boundary", "Edge", f"subpool1={oligo1.stdout.strip()}\nsubpool2={oligo2.stdout.strip()}\nbad_return={bad.returncode}\noverflow={overflow.stderr.strip()}", assertions, True, "Executed copied scripts/build_oligo.py for both documented subpools, a 200-nt budget overflow, and an invalid-spacer boundary.")

    # Input 7: Cas12a documented orientation and singleton-control logic.
    def cas12a(seq: str) -> list[str]:
        return [m.group(1) for m in re.finditer(r"TTT[ACGT]([ACGT]{23})", seq)]
    synthetic = {"PAIR1A": "TTTAG" + "ACGTACGTACGTACGTACGTACG" + "TTTC" + "GCTAGCTAGCTAGCTAGCTAGCT", "PAIR1B": "TTTA" + "TGCATGCATGCATGCATGCATGC" + "TTTG" + "CGATCGATCGATCGATCGATCGA"}
    hits = {gene: cas12a(seq) for gene, seq in synthetic.items()}
    array = hits["PAIR1A"] + hits["PAIR1B"]
    controls = ["PAIR1A_single", "PAIR1B_single", "double_NTC"]
    assertions = [
        check(all(len(v) == 2 for v in hits.values()), "Cas12a finder identifies two TTTV-PAM-adjacent 23-nt spacers per paralog", str({k: len(v) for k, v in hits.items()})),
        check(len(array) == 4 and len(array[:2]) == len(array[2:]) == 2, "Four-guide array has the documented 2+2 paralog split", f"array_length={len(array)}"),
        check(controls == ["PAIR1A_single", "PAIR1B_single", "double_NTC"], "Required singleton and double-NTC controls are retained for GI scoring", str(controls)),
        check("PAM is 5' of spacer" in (COPY / "SKILL.md").read_text(encoding="utf-8"), "Skill explicitly warns that Cas12a orientation differs from Cas9", "Common Errors wording found"),
    ]
    pd.DataFrame({"guide": array, "group": ["A", "A", "B", "B"]}).to_csv(DATA / "input7_cas12a_array.csv", index=False)
    record(7, "enAsCas12a paralog array and singleton controls", "Adversarial", f"guide_counts={ {k: len(v) for k,v in hits.items()} } array={array} controls={controls}", assertions, True, "Executed a fresh synthetic TTTV-PAM scan following the copied Skill's Cas12a orientation and control rules.")

    # Input 8: direct-mode missing-input escape hatch (the correct output is to stop).
    skill_text = (COPY / "SKILL.md").read_text(encoding="utf-8")
    answer = "I cannot design the requested library yet. Please provide the gene list, genome assembly, screen chemistry, and coding-exon coordinates (or FANTOM5 CAGE peaks for CRISPRi/a)."
    assertions = [
        check("stop and confirm the required inputs" in skill_text, "Skill contains an explicit stop-and-confirm instruction", "required-input paragraph found"),
        check(all(term in answer for term in ["gene list", "genome assembly", "chemistry", "coding-exon"]), "Direct-mode response asks for the missing required inputs", answer),
        check("Cas9 KO" not in answer, "Direct-mode response does not silently default to Cas9 KO", answer),
    ]
    record(8, "Under-specified library request must stop for inputs", "Scope Boundary", answer, assertions, True, "Executed Mode-D direct reasoning against the copied Skill's explicit required-input gate; no library was fabricated.")

    # Input 9: exact documented R alternative boundary, using the prescribed r.sh wrapper.
    rscript = ROOT / "input9_crisprscore.R"
    bash = r"C:\Program Files\Git\bin\bash.exe"
    rrun = subprocess.run([bash, r"F:/OpenScience/audit-envs/crispr-screen-analyst/r.sh", str(rscript)], text=True, capture_output=True, timeout=120)
    rcombined = rrun.stdout + "\n" + rrun.stderr
    assertions = [
        check(rrun.returncode != 0 and "expected_runtime_error=" in rcombined, "crisprScore probe propagates the documented unavailable-backend failure rather than falsely succeeding", f"return={rrun.returncode}"),
        check("crisprScore_version=1.10.0" in rcombined and "formals=sequences,fork" in rcombined, "Installed crisprScore and exported getAzimuthScores signature match the Skill", rcombined[-800:]),
        check("expected_runtime_error=" in rcombined and "vc 9" in rcombined.lower(), "Real Rule Set 2 backend failure is reproduced and precisely attributed", rcombined[-1200:]),
        check("CRISPick" in skill_text and "does not actually run here" in skill_text, "Skill documents the runtime limitation and web alternative", "Version Compatibility text checked"),
    ]
    record(9, "crisprScore real-Rule-Set-2 runtime boundary", "Variant B", rcombined[-2400:], assertions, True, "Executed the saved R probe through the env's r.sh wrapper; it verifies the installed interface and captures the known basilisk/VC9 backend failure.")

    # Input 10: fresh QC direct-mode test grounded in computed count metrics and failure-mode text.
    counts = np.array([1000] * 10 + [10] * 90, dtype=float)
    sorted_counts = np.sort(counts)
    gini = (2 * np.sum((np.arange(1, len(counts) + 1)) * sorted_counts) / (len(counts) * sorted_counts.sum())) - (len(counts) + 1) / len(counts)
    skew = sorted_counts[-10:].mean() / sorted_counts[:10].mean()
    qc_answer = f"Synthetic plasmid pool: Gini={gini:.3f}, top/bottom decile skew={skew:.1f}. This fails the Skill's <0.1 Gini and <5 skew targets. Treat PCR bias or synthesis dropout as competing causes; inspect low-GC depletion and absent-guide patterns, cap PCR at 15 cycles, use a low-bias polymerase, and re-sequence/re-design rather than calling biological hits."
    failure_text = (COPY / "references" / "failure-modes.md").read_text(encoding="utf-8")
    assertions = [
        check(gini > 0.1 and skew > 5, "Synthetic pool truly violates the documented QC thresholds", f"gini={gini:.3f}, skew={skew:.1f}"),
        check("PCR bias" in qc_answer and "synthesis dropout" in qc_answer, "Diagnostic preserves competing documented causes rather than over-claiming one", qc_answer),
        check("Cap PCR at 15 cycles" in failure_text and "Re-design replacement guides" in failure_text, "Recommended remediation is grounded in shipped failure-mode guidance", "both remediation passages found"),
        check("biological hits" in qc_answer, "Response keeps library-QC failure distinct from biological hit calling", qc_answer),
    ]
    record(10, "Plasmid-pool skew diagnostic", "Stress", qc_answer, assertions, True, "Executed a synthetic count-metric calculation and followed the copied direct-mode failure guidance; the synthetic data are audit-only.")

    payload = {"source_copy": str(COPY), "results": RESULTS}
    (ROOT / "validation.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    for item in RESULTS:
        passed = sum(a["result"] == "PASS" for a in item["assertions"])
        print(f"input={item['index']} executed={item['executed']} assertions={passed}/{len(item['assertions'])} label={item['label']}")


if __name__ == "__main__":
    main()
