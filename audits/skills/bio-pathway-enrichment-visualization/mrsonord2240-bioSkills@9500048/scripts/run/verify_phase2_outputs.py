"""Validate Phase 2 isolated-run exit markers, artifacts, and behavior evidence."""
from pathlib import Path


RUN = Path(__file__).resolve().parent
CORE = [
    "prep_data.R", "input1_canonical.R", "input2_variantA.R", "input3_edge.R",
    "input4_variantB.R", "input5_stress.R", "input6_scope.R",
    "input7_redundancy_check.R", "check_single_term.R", "check_treeplot_current_api.R",
    "shipped_visualization_ora_phase2.R", "shipped_visualization_gsea_phase2.R",
]
PDFS = ["input1_output.pdf", "input2_output.pdf", "input3_output.pdf", "input4_output.pdf", "input5_output.pdf", "input7_output.pdf"]
REQUIRED_LOG_TEXT = {
    "input1_canonical.R": ["Raw significant terms:", "After simplify(cutoff=0.7):", "Wrote input1_output.pdf"],
    "input2_variantA.R": ["GSEA significant sets:", "barplot method exists for gseaResult: FALSE", "Wrote input2_output.pdf"],
    "input3_edge.R": ["n terms available for similarity map:", "Wrote input3_output.pdf"],
    "input4_variantB.R": ["compareCluster rows:", "Wrote input4_output.pdf"],
    "input5_stress.R": ["GeneRatio vs computed FoldEnrichment", "Plots produced:", "Wrote input5_output.pdf"],
    "input6_scope.R": ["CONCLUSION: SKILL.md's Decision Tree redirect to REVIGO", "cannot be coerced from a flat data.frame"],
    "input7_redundancy_check.R": ["Are these Entrez IDs (all-numeric)? TRUE", "Are these still all-numeric (i.e. fix failed)? FALSE", "Wrote input7_output.pdf"],
    "check_single_term.R": ["n terms forced to: 1"],
    "check_treeplot_current_api.R": ["enrichResult nCluster SUCCEEDED", "compareClusterResult nCluster SUCCEEDED", "cluster.params ERROR: unused argument"],
    "shipped_visualization_ora_phase2.R": ["Wrote /tmp/"],
    "shipped_visualization_gsea_phase2.R": ["Wrote /tmp/"],
}


def must(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


for script in CORE:
    marker = RUN / f"{script}.phase2.exit"
    must(marker.is_file(), f"exit marker exists for {script}")
    must(marker.read_text(encoding="utf-8").strip() == "0", f"{script} exited 0")

for pdf_name in PDFS:
    artifact = RUN / pdf_name
    payload = artifact.read_bytes()
    must(payload.startswith(b"%PDF"), f"{pdf_name} is a PDF")
    must(len(payload) > 1000, f"{pdf_name} is non-trivial ({len(payload)} bytes)")

for script, snippets in REQUIRED_LOG_TEXT.items():
    log = (RUN / f"{script}.phase2.log").read_text(encoding="utf-8", errors="replace")
    for snippet in snippets:
        must(snippet in log, f"{script} log contains {snippet!r}")

input4_log = (RUN / "input4_variantB.R.phase2.log").read_text(encoding="utf-8", errors="replace")
must("treeplot ERROR:" not in input4_log, "compareCluster treeplot did not report an error")

overlay_install = RUN / "install_phase2_ggupset.exit"
overlay_run = RUN / "input5_stress.R.phase2_overlay.exit"
must(overlay_install.read_text(encoding="utf-8").strip() == "0", "private ggupset overlay installed cleanly")
must(overlay_run.read_text(encoding="utf-8").strip() == "0", "stress route exited 0 with the private overlay")
overlay_log = (RUN / "input5_stress.R.phase2_overlay.log").read_text(encoding="utf-8", errors="replace")
must("upsetplot" in overlay_log and "upsetplot ERROR:" not in overlay_log, "upsetplot rendered after the documented private install")
print("PHASE2_OUTPUT_VALIDATION_PASS")
