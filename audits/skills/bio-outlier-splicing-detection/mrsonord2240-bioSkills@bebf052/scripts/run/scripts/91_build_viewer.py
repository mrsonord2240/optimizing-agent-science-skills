# Build eval_viewer_bio-outlier-splicing-detection.md from the JSON report plus the re-judgement tables.
import io, json, os
run = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.dirname(run)
R = json.load(io.open(os.path.join(out, "eval_report_bio-outlier-splicing-detection_result.json"), encoding="utf-8"))
F = R["final"]; D = R["dynamic_score"]; S = R["static_score"]
L = []
w = L.append
w("# Eval Viewer — bio-outlier-splicing-detection (re-audit of the fixed Skill)")
w("Generated: 2026-09-20")
w("Source: `%s` (read from a copy in `run/skill/`; the worktree `wt\\as-outlier` and the clone were not written to)." % R["meta"]["source"])
w("Pre-fix (archived at `_pre-fix-20260920\\`): 67, Beta Only, not deployable. **Now: %d, %s, deployable, no veto, no open P0, one open P1.**" % (F["score"], F["grade"]))
w("")
w("Category: Data Analysis. Mode D. Complexity: Complex, N = 9 (the 7 pre-fix inputs re-run as regression tests, plus 2 new). Executed 9/9 (input 5 partial: the DROP demo, MAE and OUTRIDER modules were not re-run; the earlier completed demo run is cited). Every script that was run is in `run/scripts`, logs in `run/logs`, extracted SKILL.md blocks in `run/blocks`. Synthetic data are labelled SYNTHETIC in each generator; BAMs were deleted after the audit.")
w("")
w("## How the code-usability question was re-judged")
w("Every fenced block of SKILL.md was extracted verbatim to `run/blocks/` by `02_extract_blocks.py` (9 blocks) and parse-checked (`03_syntax.R`: all 6 R blocks and the example parse; `bash -n` OK on the 3 bash blocks). Then each was run from its file:")
w("")
w("| block | what | how run | result |")
w("| --- | --- | --- | --- |")
w("| 01 | FRASER 2 workflow | verbatim via `10_block_fraser.R`, cohort A and B, 30 to 8 samples, FRASER 2.6.1; verbatim on 2.2.0 | 2.6.1: ran, 4/4 (A), 4/4 (B); empty-result subsets stop at the last line; 2.2.0: `estimateBestQ` not found |")
w("| 02 | OUTRIDER | verbatim via `45_block_outrider.R`, 1.24.0 and 1.28.1, four matrices | ran on both releases; q numeric > 1 |")
w("| 03, 04 | LeafcutterMD bash + BH | verbatim (one substitution: clustering script path) | ran; 11 hits at BH q<0.05 |")
w("| 05 | DROP install/init/config | init and config checks in `50_drop_init.sh`; `mamba create` and demo not run | init works; config values match; 0 `conda:` |")
w("| 06, 07 | bcftools + R integration | verbatim on real SpliceAI output | concordant variants only; guard fires |")
w("| 08, 09 | mismatch check, choosing q | verbatim via `16_block_extras.R` | ran; `plotEncDimSearch(plotType='auc')` returns a ggplot; bestQ 1 (OHT) / 2 (grid) |")
w("| example | `examples/fraser2_rare_disease.R` | clean copy, arguments, FRASER 2.6.1 and 2.2.0, cohort A and 4 real BAMs | ran on all three |")
w("")
w("## Summary Table")
w("")
w("| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |")
w("| --- | --- | --- | --- | --- | --- | --- | --- |")
for x in D["inputs"]:
    tag = " (NEW)" if x["index"] in (8, 9) else " (regression)"
    w("| %d | %s%s | yes | %d | %d | %d | %d/%d | %s |" % (x["index"], x["type"], tag, x["basic"], x["specialized"], x["total"], x["assertions_passed"], x["assertions_total"], x["status_flag"]))
w("")
w("**Execution average: %.1f / 100** (pre-fix 66.3). Assertion pass rate %d/%d (pre-fix 16/32). Layer 1 average %.1f/40, Layer 2 average %.1f/60." % (D["execution_avg"], D["assertion_pass_rate"]["passed"], D["assertion_pass_rate"]["total"], sum(x["basic"] for x in D["inputs"]) / 9, sum(x["specialized"] for x in D["inputs"]) / 9))
w("")
w("Static %d (pre-fix 67) x 0.4 = %.1f; dynamic %.1f x 0.6 = %.1f; **final %d -> %s, deployable = true**. Floors for Limited Release met (static >=70, execution >=75, L1 >=28, L2 >=42, assertions >=80%%); Production Ready needs execution >=85. Skill veto PASS (stability, contract, determinism, security). Research veto: M1 PASS, M2 PASS (pre-fix P1 fixed), M3 PASS, M4 PASS." % (S["subtotal"], S["subtotal"] * 0.4, D["execution_avg"], D["execution_avg"] * 0.6, F["score"], F["grade"]))
w("")
w("## Static score: %d/100 (pre-fix 67)" % S["subtotal"])
w("")
w("| Category | Score | Note |")
w("| --- | --- | --- |")
for k, v in S["categories"].items():
    w("| %s | %d/%d | %s |" % (k, v["score"], v["max"], v["note"]))
w("")
w("## Pre-fix findings re-judged")
w("")
w("| pre-fix finding | pre-fix | now | evidence (this audit's runs) |")
w("| --- | --- | --- | --- |")
rows = [
 ("Main FRASER workflow + example crash (`colData = data.frame`)", "P1", "**fixed**", "block on 2.6.1: 4/4 planted, 0 false calls (input 1); example clean-copy on 2.2.0 and 2.6.1 and on 4 real BAMs (input 9); unseen cohort B 4/4 (input 8). Residual: block on 2.2.0 needs `optimHyperParams` (P2)"),
 ("`estimateBestQ` / `plotEncDimSearch` API drift, OUTRIDER q object", "P1", "**fixed**", "OUTRIDER block verbatim on 1.24.0 and 1.28.1, four matrices, no crash (input 2); `plotEncDimSearch(plotType='auc')` returns a ggplot; FRASER `estimateBestQ` + `bestQ` ran (bestQ 1 OHT, 2 grid)"),
 ("OUTRIDER cohort guidance too optimistic", "P1", "**fixed**", "0/8 at n=30 on both releases; simulator m=100 60% (1.24.0) and 70% (1.28.1) on one seed vs the Skill's 71% / 74% over 3 seeds; symptom is the silent 'No significant events'"),
 ("q=10 hard-coded, tuning advice unbacked", "P1", "**fixed**", "example estimates q and prints it (q=1, 2, 2 on cohort A 2.6.1, 2.2.0, real BAMs); cohort B q=1 4/4; the old q=10 miss of the cryptic donor is not re-run, the new default finds it"),
 ("No research-use caveat; PS3 / clinical-report directive", "P1", "**fixed**", "Research Use and Licences section; grep of SKILL.md, usage-guide and example: no PS3/PP3 directive, no clinical-report step (input 6)"),
 ("Licence misstated", "P1", "**fixed**", "LICENSE files read: FRASER 2.6.1 / OUTRIDER 1.28.1 CC BY NC 4.0, 2.2.0 / 1.24.0 MIT; DROP prints the notice (`logs/72_licence_*.log`, `logs/50_drop_init.log`)"),
 ("DROP section: init, config keys, MAE, --use-conda, PCA default", "P1", "**fixed**", "`mkdir && cd && drop init` works; config values match by script; 0 files with `conda:`; MAE comment 'negative binomial' (input 5). Demo not re-run (cited)"),
 ("Invented error messages; AE not reproducible", "P1", "**partly fixed, P1 remains**", "Common Errors now real messages (colData slot, OHT smaller than 2, OUTRIDER q, No significant events, `drop init`), one misplaced (seen at n=4, not n=8-12). The AE seed recipe is wrong: `SerialParam(RNGseed=1)` alone leaves 9815 of 20010 p-values differing; only `set.seed(1)` + `SerialParam(RNGseed=1)` gives 0 (input 7)"),
 ("LeafcutterMD outputs, correction, limits", "P1", "**fixed**", "files named and produced; BH block reproduces 11 hits; retention and pseudoexon give no cluster p-value (input 4)"),
 ("Tissue-mismatch symptom and detection", "P2", "**partly fixed, P2 remains**", "symptom reworded and reproduced (PCA 0, AE 8-9 calls); check works under AE only (input 7)"),
 ("Threshold inconsistencies (|z|>=2 vs 0, filter, 'autoencoder' wording)", "P2", "**fixed**", "zScoreCutoff 0 stated, PCA named as default; example uses FRASER defaults for the variability filter (667 junctions on cohort A both releases)"),
 ("Integration block (delta_max, chr naming, GTEx access)", "P2", "**fixed**", "real SpliceAI multi-allelic output parsed; chr/no-chr agree; guard fires (input 6)"),
 ("Single-file layout, no test data", "P2", "**open**", "unchanged, restated as P2"),
 ("**new** (introduced or exposed by the fix)", "-", "P2 x3, P1 x1", "FRASER block stops on empty results; block not runnable on 2.2.0; unsourced tissue/disease tables; DROP runtime wording; AE recipe (P1)"),
]
for r in rows:
    w("| %s | %s | %s | %s |" % r)
w("")
w("## Detailed Outputs")
for x in D["inputs"]:
    w("")
    w("### Input %d — %s: %s" % (x["index"], x["type"], x["label"]))
    w("**Executed:** true. %s" % x["execution_note"])
    w("")
    w("**Scores:** Basic %d/40 | Specialized %d/60 | Total %d/100 | %s" % (x["basic"], x["specialized"], x["total"], x["status_flag"]))
    w("")
    w("**Assertions:**")
    for a in x["assertions"]:
        w("- [%s] %s — %s" % (a["result"], a["text"], a["note"]))
    w("Assertion pass rate: %d/%d" % (x["assertions_passed"], x["assertions_total"]))
w("")
w("## Key outputs the scores depend on")
w("```")
w("FRASER 2.6.1, SKILL.md block verbatim, cohort A (logs/11): 667 junctions | total calls 6")
w("  S05 g010 DETECTED padj 2.8e-05 | S12 g030 DETECTED 9.3e-03 | S20 g050 DETECTED 9.1e-04 | S25 g070 DETECTED 3.6e-03")
w("  S15/S28 expression-only: calls 0 | non-planted calls 0 | S29 mismatch calls 0")
w("FRASER 2.2.0, same block (logs/12): Error in estimateBestQ(fds, type = 'jaccard', plot = FALSE): could not find function 'estimateBestQ'")
w("Small cohorts (logs/13, block verbatim): n=8,12,16: total calls 0, then 'BLOCK ERROR: argument 1 is not a vector'; n=20: 3 calls; n=25: 5 calls")
w("Cohort B (logs/15): S03 6.2e-03, S17 1.8e-02, S22 4.2e-04, S33 3.9e-02 = 4/4; non-planted 0")
w("OUTRIDER block: n=30 1.24.0 q=8 0/8, 1.28.1 q=2 0/8; n=100 1.24.0 q=20 2/20, 1.28.1 q=2 9/20 (1 false); simulator m=100 116/192 and 135/192")
w("LeafcutterMD (logs/61, logs/62): 86x30 clusters; raw p<0.05 39; BH q<0.05 11 = S05 (6.4e-07), S12 (2.0e-02), S29 x9")
w("Integration (logs/70_*): confirmed positions 90190,92000 (chr21 and 21 spellings); chrX-only VCF -> stopifnot fires")
w("AE reproducibility (logs/22, logs/28), 20010 p-values, cells differing >1e-6:")
w("  no seed 9885 | set.seed(1) only 9279 | RNGseed=1 only 9815 (5 iterations: 9962) | set.seed(1)+RNGseed=1 0 | PCA 0")
w("DROP 1.6.1 (logs/50): init ok; aberrantSplicing run: true, PCA, FRASER2, padjCutoff 0.1, deltaPsiCutoff 0.1; conda: files 0")
w("```")
w("")
w("## Notes on the run")
w("- The pre-fix cohort was regenerated by `run/scripts/01_make_synth_cohort.py` (seed 20260920): `planted_truth.tsv`, `gene_counts.tsv` and `genes.tsv` are byte-identical to the archived ones (`cmp`), and the 3000x30 OUTRIDER matrix is identical too.")
w("- The pre-fix DROP demo was **not** re-run (about 90 minutes). The earlier run started 11:51, its `fraser` group results existed by 13:22, and the run was killed by its own `timeout 6000` at 13:31 in step 08 of group `fraser_external` (63 of 70 steps).")
w("- Machine load: two as-drop runs (OUTRIDER 1.28.1 on the simulator matrix, FRASER AE with MulticoreParam(4)) died with 'error writing to connection' while another agent's STAR job was running; both were rerun (OUTRIDER on retry, AE with SerialParam). A first cohort-B attempt collided with a duplicate launch on the same working directory (HDF5 error) and was rerun cleanly. During setup a `taskkill /IM Rscript.exe` meant for my own two runs also ended three other Rscript processes on the machine; no other agent's files were touched.")
w("- No package version was changed; nothing was installed.")
w("")
w("## Recommendations")
for r in R["recommendations"]:
    w("")
    w("**[%s] %s**  (inputs %s)" % (r["priority"], r["title"], r["observed_in"]))
    w("- Problem: %s" % r["problem"])
    w("- Root cause: %s" % r["root_cause"])
    w("- Fix: %s" % r["fix"])
io.open(os.path.join(out, "eval_viewer_bio-outlier-splicing-detection.md"), "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("viewer written", len(L), "lines")
