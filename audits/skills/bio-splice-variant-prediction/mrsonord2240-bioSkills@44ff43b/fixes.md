# bio-splice-variant-prediction fix log

## 2026-09-20 (fixer: Sonnet; branch `fix/as-spvp`, worktree `F:\OpenScience\wt\as-spvp`, base staging `main` 70b5873)

First audit: 66, Reject (Research Veto M4 code usability; open P0s). Evidence:
`F:\OpenScience\audits\bio-splice-variant-prediction\` (report JSON, viewer, `run\`).

Verification data: a new GRCh38 panel built from the auditor's variants (lifted with Ensembl REST, REF asserted against the
hg38 FASTA, 0 mismatches): TP53 c.673-2A>G, DMD c.9563+1G>A, DMD c.31+1G>A, OTC c.386+5G>A, GLA c.370-1G>A, GLA c.639+919G>A
(X:101399747 C>T), three ClinVar-benign GLA. Real GENCODE v45 (chr17+chrX GTF, hg38 chr17/chrX upper-cased). Scratch:
`F:\OpenScience\as-spvp-scratch\` (not shipped).

### Envs created (new, no existing env or version touched; not yet in TOOLS.md)

| env | contents | smoke test |
|---|---|---|
| `as-spvp` | py3.10, pysam 0.24.1, bcftools, pandas 2.3.3, numpy 2.2.6, pyfaidx 0.9.0.4; pip: torch 2.14.0+cpu, sinkhorn-transformer 0.11.4, axial-positional-embedding 0.2.1, PyVCF3 1.0.0, pyensembl 2.10.15, gffutils 0.14, gdown | SpliceVault remote-tabix lookup; SpliceTransformer CPU: panel of 9 in 3 min 52 s |
| `as-cispliceai` | py3.10, tensorflow-cpu 2.15.1, keras 2.15.0, cispliceai 1.2.2 (PyPI; 1.2.1 from GitHub gave identical output) | `cis-vcf -a grch37 -d 500 --all` on the GRCh37 panel, 23 s |
| `as-spvp-gpu` | py3.10, **torch 2.11.0+cu128**, same SpliceTransformer deps, Pangolin 1.0.2 (copy of the clone) | `torch.cuda` True on the RTX 5070 Ti, arch list has `sm_120`, matmul OK; SpliceTransformer panel in 12 s, scores identical to CPU; Pangolin GPU output equals CPU except |score| <= 0.01 noise |

Blackwell: a CUDA 12.8 PyTorch wheel (`--index-url https://download.pytorch.org/whl/cu128`) runs on the 5070 Ti; cheap to add in a
new env, verified for SpliceTransformer and Pangolin (torch). TensorFlow tools (SpliceAI, MMSplice, CI-SpliceAI) were not tried on GPU.
Tool data fetched publicly: SpliceTransformer weights (Google Drive, 120 MB, `gdown`), SpliceVault index (Ensembl FTP), GENCODE v45,
UCSC hg38 chr17/chrX. `TOOLS.md` was not edited (orchestrator records it).

### Findings

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| Pangolin recipe unrunnable (deps, `create_db`, mask) | P0 | Install section lists torch/gffutils/pyfaidx/pyfastx/biopython/PyVCF3==1.0.0 and the GitHub clone; DB via Pangolin's `create_db.py` (GTF, canonical default; `--filter None` for all transcripts); the GFF3 `gffutils.create_db` line removed with the `Duplicate ID CDS` error documented; default command now `-m False` | ran: `create_db.py` on GENCODE v45 chr17+X GTF (32 s canonical, 86 s all); Pangolin on the 9-variant panel with both DBs x mask True/False; Skill's `-d 500 -m True -s 0.2` command; audit's GFF3 error read from `out/pang38.log` (not re-run) | see mask table below |
| `-m True` erases the GLA pseudoexon gain; mask trade-off with numbers | P0 | Pangolin section: measured table (below), recommendation `-m False`, Failure Modes entry | ran (GPU/CPU Pangolin 1.0.2, GENCODE v45) | GLA gain 0.23 -> 0.00 with the all-transcript DB (pseudoexon is exon of NMD transcripts ENST00000493905.6/ENST00000674127.2 in v45, checked in the GTF). New finding beyond the audit: canonical-DB mask erases losses at sites annotated only in non-canonical transcripts (5 of 5 DMD sites tested), and an overlapping gene erases OTC c.386+5G>A's -0.72 in both DBs (OTC-only DB keeps -0.72; cause: `process_variant` masks the shared `loss`/`gain` arrays in place per gene) |
| Concordance snippet fails on real outputs | P0 | new `examples/splice_parsers.py` (`parse_spliceai_vcf`, `parse_pangolin_vcf`, `parse_mmsplice_csv`, `build_concordance`): normalised `chrom:pos:ref>alt` key, gene reduction, outer join keeps every input variant, `n_scored` shown; SKILL.md block replaced by a 4-line use | ran on real SpliceAI/Pangolin/MMSplice output; `test_splice_parsers.py` 5/5 PASS (from a clean copy in WSL and on Windows Python 3.14/pandas 2.3.3) | audit's failures (KeyError chrom, 25 rows for 10 variants, 9 of 10 survive inner merge) do not recur; the GLA c.639+919G>A row survives with `n_scored` 2 because MMSplice returns no row |
| Classifier mislabels exactly 0.20/0.50/0.80 | P1 | `classify_delta` (np.select, inclusive) in `splice_parsers.py`; same function used by the shipped example and SKILL.md; boundary assertions in the test | ran: old `pd.cut` bins reproduce the bug (0.20 -> inconclusive, 0.50 -> PP3_supporting, 0.80 -> prec0.5); new function: 0.10 BP4, 0.20 PP3, 0.50/0.80 tiers, 11 boundary cases asserted | |
| `.` scores become BP4; records without INFO vanish | P1 | `.` -> NaN -> `not_scored` (never BP4); `unscored_report` and the example's left join to the input VCF list skipped records; SKILL.md says SpliceAI exits 0 on them | ran on real SpliceAI output for a wrong-REF record (no tag), an N-only allele (`.`) and a multi-allelic record; example prints `WARNING SpliceAI: no score for ...` | |
| Pangolin "per-tissue predictions" claim | P1 | text corrected (CLI prints tissue maximum; ALT[0] only; Ensembl gene IDs); new `examples/pangolin_tissue.py` for heart/liver/brain/testis | ran: TP53 tissue max +0.72/-0.90 = CLI `-m False` output; OTC -0.72 = CLI; REF-mismatch guard fires on soft-masked FASTA | Pangolin `bcftools norm -m-` note added |
| Usage-guide TP53 variant wrong REF | P1 | prompt now TP53 c.673-2A>G (GRCh38 chr17:7674292 T>C) with "check REF against the FASTA first" | ran: SpliceAI DS_AL 1.00 at -2, Pangolin -0.90 at -2, MMSplice -2.57, SpliceVault ES/CA events; old REF asserted wrong (hg38 base is G, Pangolin/SpliceAI skip the record) | |
| `-D` mechanism mis-stated; helper never flags 0.00 | P1 | `-D` = variant-to-site distance; measured GLA case in text; `flag_extend_window_candidates` flags everything < 0.20 including 0.00; example re-runs at `--extended 500` by default and keeps the higher delta | ran: GLA c.639+919G>A D50 DS_DG 0.30 at variant, D500 adds DS_AG 0.22 at +53, delta_max 0.30 both; DMD c.31+1G>A DS_DG 0.08 -> 0.40 at +69; example on panel flagged the 3 benign (<0.2), wide run executed | 0.00 no longer skipped |
| `high_concordance_pathogenic` label; no research-use statement | P1 | labels renamed (`all_predict_disruption`, `majority_predict_disruption`, `discordant`, `none_predict_disruption`, `insufficient_tools`); Scope paragraph at top; usage-guide states research-use; test asserts no label contains "pathogenic" | ran | Practice Boundaries M2 |
| ASO step 3 not executable; SpliceVault stub | P1 | ASO section relabelled a checklist (SpliceAI-on-N-mask step removed, off-target step re-worded to a sequence search, "score the sequence change, not the oligo"); SpliceVault: runnable `examples/splicevault_lookup.py` | SpliceVault ran: remote tabix on the Ensembl file, TP53 c.673-2A>G ENST00000269305 Top1 CA +47, Top2 CA -50, Top3 ES 7, Top4 CA -70; independent check: SpliceAI DS_AG 0.85 at DP +47 = Top1; Dawes 92/96/86 % numbers verified against the PubMed abstract 36747048 | SpliceVault bulk SQL is requester-pays (not used); "92% overall, 96%/86%" reworded as measured in 140 clinical cases |
| Un-noted behaviours, install notes | P2 | example takes build/paths/distances as arguments; multi-gene rows reduced (max) with MANE note; unreproducible `chrom not in reference` row replaced by the chr-prefix observation; pyensembl dropped from prerequisites (only SpliceTransformer needs it); Install section has setuptools<81, PyVCF3, cyvcf2 notes; soft-masked FASTA trap found and documented | ran: Pangolin `Mismatch ... (ref base: c)` on UCSC soft-masked hg38 for a correct REF; GENCODE FASTA is upper-case (first 24 Mb checked) | setuptools<81 / cyvcf2 statements are from TOOLS.md traps 21/23, not re-tested by me |
| No test VCF; privacy note | P2 | `examples/test_data/` (9-variant GRCh38 panel + 3 edge records, real SpliceAI/Pangolin/MMSplice outputs) and `test_splice_parsers.py`; data-handling paragraph (remote tabix, CADD API, VariantValidator send coordinates) | ran | |
| SpliceVault, CADD-Splice, SpliceTransformer, CI-SpliceAI never run | Missing executables | SpliceVault: written and run (above). CADD-Splice: public API `curl` block, run (PHRED: DMD c.31+1G>A 33, c.9563+1G>A 34, GLA c.370-1G>A 35, GLA c.639+919G>A 14.9, benign 10.7 (GRCh37-v1.7); TP53 c.673-2A>G 34 on GRCh38-v1.7). SpliceTransformer: installed (new env), run block written; CI-SpliceAI: installed, run block written | ran (panel scores: SpliceTransformer TP53 1.00, DMD 0.99/0.56, OTC 0.89, GLA c.370-1 0.98, GLA c.639+919 0.38, benign 0.01-0.07; CI-SpliceAI GRCh37 D500 canonical 0.64-1.00, GLA pseudoexon 0.05) | CADD X:193062 (PLCXD1, PAR1) got PHRED 9.1 despite SpliceAI DS_DL 1.00, cause not investigated, not put in the Skill |
| TrASPr, BPHunter, LaBranchoR / BPP / SVM-BPfinder claims never run | Missing executables | **deleted/hedged**: TrASPr removed everywhere (repo `xuyunfan9991/TrASPr_model` README covers pre-training/fine-tuning on example data, no checkpoint or variant-scoring command); BPHunter: its reference data page redirects to a GitHub repo that 404s (2026-09-20), so the script cannot run: Skill states "none was run here", keeps the citations, drops the "use BPHunter" instruction; LaBranchoR/BPP/SVM-BPfinder kept only as citations | checked (network): `hgidsoft.rockefeller.edu/BPHunter/standalone.html` -> 302 -> 404; repo `casanova-lab/BPHunter` has scripts, no data | |

Pangolin mask measurements (GENCODE v45, `-d 50`; the DMD sites are the five highest-SpliceAI of 53 alternative-only internal sites; the losses are Pangolin scores):

| variant | `-m False` | `-m True` canonical DB | `-m True` all-transcript DB |
|---|---|---|---|
| GLA c.639+919G>A (gain) | +0.23 at -3 | +0.23 | 0.00 |
| DMD alt sites chrX:31146355, 31266809, 32342851, 33078185, 33078348 (loss) | -0.38, -0.81, -0.60, -0.70, -0.73 | 0.00 x5 | -0.38, -0.81, -0.60, -0.70, -0.73 |
| OTC c.386+5G>A (loss) | -0.72 | 0.00 | 0.00 |
| TP53 c.673-2A>G (loss) | -0.90 | -0.90 | -0.90 |

### Tool versions used

SpliceAI 1.3.1 (TF 2.21, keras 3.12, setuptools 80.10.2), Pangolin 1.0.2 (torch 2.13.0 cpu; 2.11.0+cu128 in `as-spvp-gpu`; gffutils 0.14, pyfastx 2.3.1, PyVCF3 1.0.0),
MMSplice 2.4.0 (TF 2.21, kipoiseq 0.7.1, cyvcf2 0.34.0), CI-SpliceAI 1.2.2 (tensorflow-cpu 2.15.1, keras 2.15.0), SpliceTransformer GitHub main (torch 2.14.0+cpu / 2.11.0+cu128, sinkhorn-transformer 0.11.4, axial-positional-embedding 0.2.1),
pysam 0.24.1, GENCODE v45, CADD API v1.7, SpliceVault table `SpliceVault_data_GRCh38.tsv.gz` (Ensembl current_variation, read 2026-09-20).
SpliceTransformer needs `axial-positional-embedding==0.2.1` (0.2.x newer names `pos_emb.weights.N` and `load_state_dict` fails).

### Deleted or moved passages (nothing the agent needs left the Skill)

SKILL.md:
- Python `parse_spliceai_vcf` + `pd.cut` block -> `examples/splice_parsers.py` (`parse_spliceai_vcf`, `classify_delta`), 3-line use in SpliceAI Workflow. The example's own copies of both functions were deleted and import the module.
- Concordance snippet and its `{0..3}` label map -> `build_concordance()` in `splice_parsers.py`; labels table rewritten in SKILL.md "Concordance Across Predictors".
- Pangolin `gffutils.create_db(...gff3...)` line and the "VCF with per-tissue predictions" sentence -> Pangolin section (`create_db.py`, tissue-maximum note, `pangolin_tissue.py`).
- SpliceVault import-plus-comments block -> `examples/splicevault_lookup.py` + SpliceVault section.
- "Quality Thresholds" section (7 rows) deleted: PP3/BP4/0.5/0.8 -> ClinGen table + operational rules; -D 50 / -D 500-2000 -> SpliceAI Workflow and Extended-Window table; ASO off-target <=16/20 -> ASO checklist step 4; "2/3 predictors" -> Concordance table.
- Common Pitfalls bullets "50nt window for deep intronic variants", "Tissue-agnostic prediction", "Branchpoint variants", "In-silico-only PVS1" deleted as repeats of the Extended-Window, SpliceAI failure-mode, Branchpoint and ClinGen operational-rules text; the first bullet's PVS1 clause likewise.
- Common Errors rows `spliceai: tensorflow not found` (folded into Install), `spliceai: chrom not in reference` (did not reproduce; replaced by the chr-prefix row), `pangolin: no annotations found` (replaced by the observed message), `mmsplice: variant outside any cassette event` and `SpliceVault: variant not found` (messages not observed; replaced by the observed silent behaviours).
- TrASPr row/mentions (matrix, decision tree, failure modes, description); BPHunter/LaBranchoR fix instructions in Branchpoint and Failure Modes (see above); ASO steps 3 and the "whole-transcriptome SpliceAI scan" wording; "-D 500 captures most pseudoexon-creating variants" (contradicted by the GLA measurement).

usage-guide.md (each fact now once, in SKILL.md):
- Prerequisites (pip/Pangolin/MMSplice/SpliceVault/reference lines) -> SKILL.md Install.
- "What the Agent Will Do" (7 steps) deleted: SKILL.md Decision Tree + workflow sections cover it.
- Tips (8 bullets): ClinGen thresholds/weights -> ClinGen table and rules; 50nt/500-2000 and 5-15% -> Extended-Window; tissue-agnostic -> SpliceAI Tissue Agnosticism; RNA validation, log version/window, SpliceAI-not-PVS1 -> ClinGen operational rules; branchpoint -> Branchpoint section; concordance -> Concordance section.
- Overview description copy shortened to two sentences plus a pointer. Disagreements between the two copies: only the wrong TP53 example (usage guide), fixed to the audited variant.

### Not fixed

- P2 "no references/ layer": moving ASO/branchpoint/HGVS into `references/` is a restructuring beyond dedup; SKILL.md is now 443 lines (was 450). Left.
- Pangolin `-m True` itself is a Pangolin 1.0.2 defect (shared in-place arrays); documented and worked around, not patchable from the Skill.
- TF-based tools on the Blackwell GPU were not tried; only torch (SpliceTransformer, Pangolin).
- MMSplice: the audit's GRCh37 multi-transcript rows and GLA c.639+919G>A (row present on GRCh37 Ensembl, absent on GRCh38 GENCODE basic) differ by annotation; documented as "no row" behaviour, not investigated further.
- BPHunter/LaBranchoR/BPP/SVM-BPfinder/TrASPr could not be run (see table).
- Claims taken from TOOLS.md and not re-tested here: MMSplice `setuptools<81`/cyvcf2 numpy note; SpliceAI needing `setuptools<81` (the `pkg_resources` import is visible in the audit log).

## 2026-09-24 final pass (fixer and final auditor: Codex; not independent)

2026-09-24, source commit `4b731c929804830dee9ea5862ce8d1ec340f7f78`:

- Filter `*` and symbolic ALT alleles before invoking SpliceAI, retaining supported alleles from the same record and returning excluded alleles as `not_scored`.
- Emit `top_score_gene` and `annotated_genes` so a maximum score is not mistaken for clinical-transcript selection.
- Bound long allele displays in warnings and document the limits of extended-window rescue, predictor concordance, BPHunter availability, and CPU/Git provenance.

Evidence: canonical audit report and viewer in `F:\OpenScience\audits\bio-splice-variant-prediction\`; raw execution logs are in `run\final_pass_20260924`.

