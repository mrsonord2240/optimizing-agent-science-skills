# fixes/

One file per Skill, `<skill-id>.md`, recording every fix pass that Skill has had.

Each pass gets a dated heading and a table:

| finding | priority | change | verified (ran / help / docs) | notes |

followed by the findings left unfixed and why — usually because the fix would be new content rather
than a correction, which is out of scope for a fixer.

These logs say what was *intended and verified by the fixer*. They are not evidence that the Skill is
good: only a re-audit's own runs are. A re-auditor reads the log to know what changed, then ignores it
and scores what the code does.

The same changes also travel with the audit record as `audits/<skill-id>/<version>/fixes.md`, so
anyone reading a published record sees them without needing this directory.

## Revisit list (noticed during fix passes, not fixed)

Items a fixer saw and left because the pass was scoped to something else. Added 2026-09-21; delete a row when it is fixed or ruled out.

| Skill | what | why left |
| --- | --- | --- |
| bio-proteomics-peptide-identification | MSFragger, MaxQuant, MetaMorpheus, X!Tandem, pFind are named in the taxonomy with no commands | FIX_BRIEF says write, install or delete named tools; MSFragger jars need the pending licences, the rest were not judged findings. Decide per tool |
| bio-crispr-screens-prime-editing-screens | ePRIDICT is named with no runnable code and is not installed | install barred in the batch; deleting the claim changes scope |
| bio-microbiome-functional-prediction | `differential-abundance/examples/aldex2_analysis.R` line 62 calls `linda(..., prev.filter = 0)`, which crashes on pathway tables | belongs to the differential-abundance Skill |
| bio-causal-genomics-colocalization-analysis | `examples/coloc_abf_pipeline.R` `harmonise` lacks the strand-complement branch | `examples/` left alone in a structure-only pass |
| bio-crispr-screens-base-editing-analysis | library-design "Approach" line promises predicted amino-acid changes that `find_be_spacers` does not return | structure-only pass |
| bio-reference-operations | `python-consensus.md` says "5 and 4" at `-d 1`; the majority-vote script gives 6 | structure-only pass changes no claims |
| bio-metabolomics-xcms-preprocessing | Skill says to align to a pooled QC, but the `ObiwarpParam` example shows no `centerSample` | outside the audited finding |
| bio-sra-data | `examples/download_batch.sh` exits 0 when accessions fail (only `failed.txt` shows it) | SKILL.md now says to check the file; script unchanged |
| bio-alignment-msa-parsing | `alignment-io` also calls A2M padded | different Skill |
| bio-proteomics-quantification | `silac_labeling_efficiency` reads low on pilots with Pro-containing peptides (Arg->Pro) | logged, not a corrected claim |
| bio-single-cell-perturb-seq | env `TOOLS.md` line ~206 carries a wrong `sceptre` claim | outside the fork |
| bio-differential-expression-deseq2-basics | description lacks the pseudobulk trigger; "what to report" block | needs Sam's call (recommended: add) |
| bio-workflows-proteomics-pipeline | FragPipe route deleted until MSFragger/IonQuant/diaTracer jars arrive | licences requested |
| bio-experimental-design-multiple-testing | `scripts/ihw_safe.R` has no timeout; one IHW child hung (130 s CPU) and the wrapper would wait forever | a timeout changes behaviour; structure-only pass |
| bio-sam-bam-basics | DRAGEN MAPQ row -- Illumina-licensed hardware/software, no public install path | needs a licence/instance or a real DRAGEN BAM |
| bio-sam-bam-basics | Cell Ranger itself (STARsolo now stands in for its MAPQ/CB/UB behavior) -- 10x gates the download behind account registration | needs that registration or a real Cell Ranger BAM |
| bio-sashimi-plots | MAJIQ/VOILA commands checked against --help only | MAJIQ is licence-gated (academic/commercial), not on PyPI/conda, no test credential |
| bio-causal-genomics-colocalization-analysis | eCAVIAR/PWCoCo CLI recipes need compiled C++ binaries not built here (multi-hour build) | out of scope for a fix pass; moloc also blocked transiently by another session's install.lock, retry |
| bio-covalent-design | MGLTools/AutoDockTools (prepare_receptor4.py) needed for new-target covalent-docking prep; the official Windows installer is a PECompact2/InstallShield self-extractor 7-Zip can't unpack, no silent-install flag | needs Sam: an interactive GUI install session, or accept the docking engine (now installed+verified) without turnkey new-target prep |
