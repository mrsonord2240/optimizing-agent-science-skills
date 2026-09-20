> **Audit record for `bio-splice-variant-prediction`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@44ff43b](https://github.com/mrsonord2240/bioSkills/tree/44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b/alternative-splicing/splice-variant-prediction) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-splice-variant-prediction
Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b:alternative-splicing/splice-variant-prediction` (first audit; folder unchanged since that commit, diff against HEAD empty)
Category: Data Analysis (3) | Mode: D (Hybrid: SKILL.md guidance + one shipped script + tool CLIs) | Complexity: Complex -> 7 inputs
Auditor run folder: `F:\OpenScience\audits\bio-splice-variant-prediction\run\` (every script, `data\` = synthetic/derived VCFs of real variants, `out\` = raw outputs and logs)

## Result

| Static | Execution avg | Final | Grade | Deployable | Skill veto | Research veto |
|---|---|---|---|---|---|---|
| 71 / 100 (x0.4 = 28.4) | 62.0 / 100 (x0.6 = 37.2) | **66** | Reject (numeric band would be Beta Only; forced Reject by the Research Veto M4 FAIL) | **No** | PASS | **FAIL (M4 Code Usability)** |

Layer 1 avg 26.4/40, Layer 2 avg 35.6/60, assertion pass rate 19/35 (54%). Executed 7/7 inputs (Input 6: SpliceVault, CADD-Splice, SpliceTransformer, TrASPr, BPHunter, CI-SpliceAI parts were not executed: web/not installed; the Skill's SpliceVault block has no call).

Environment: WSL `as-spliceai` (SpliceAI 1.3.1, TF 2.21 CPU), `as-pangolin` (Pangolin 1.0.2, torch 2.13 CPU), `as-mmsplice` (MMSplice 2.4.0). Reference X.fa = GRCh37 so every SpliceAI call used `-A grch37`; GRCh38 checks used hg38 chr17 from the FLAIR test genome. Weights ship inside the packages (5 x spliceai*.h5; 64 Pangolin `final.*` files; MMSplice models). GPU: RTX 5070 Ti is visible in WSL (`nvidia-smi -L`) but both frameworks are CPU builds (TF devices = CPU; `torch.cuda.is_available()` False), so nothing used it; not needed (about 1 s per variant).

Truth set (REF alleles asserted against the FASTA in `build_panel.py`; labels from Ensembl GRCh37 VEP/ClinVar in `q_ensembl.py`, `q_benign.py`): DMD c.31+1G>A (X:33229398 C>T), DMD c.9563+1G>A (X:31227614 C>T), GLA c.370-1G>A (X:100656798 C>T) = ClinVar pathogenic canonical; GLA c.639+919G>A (X:100654735 C>T; same variant as c.640-801G>A) = deep-intronic pseudoexon; PLCXD1 X:193062 G>A canonical donor and a 2-bp donor deletion; OTC c.386+5G>A; GLA rs2071228, rs782094147, rs151195362 = ClinVar benign. GRCh38: TP53 c.673-2A>G (chr17:7674292 T>C) and c.215C>G (P72R).

## Step 1 — Skill Veto: PASS
- T1 Stability PASS: the SpliceAI, Pangolin (CLI) and MMSplice blocks and the shipped example run; failures found are documentation/recipe defects, not random crashes.
- T2 Contract PASS: frontmatter has `name` and `description`; INFO/CSV schemas are stable across runs.
- T3 Determinism PASS: the same PLCXD1 record gave `0.00|0.00|0.90|1.00|28|-10|28|-1` in every SpliceAI run (5+), Pangolin `28:0.39|-1:-0.80` in each Pangolin run.
- T4 Security PASS: example uses `subprocess.run([...])` with a list (no shell), no eval/exec, no secrets.

## Step 2 — Static (25 criteria): 71/100

| Category | Score | Note |
|---|---|---|
| Functional Suitability | 8/12 | Broad, mostly correct; verified defects listed below |
| Reliability | 7/12 | No handling of un-scored/skipped/multi-allelic/multi-gene records; skipped records exit 0 |
| Performance & Context | 5/8 | 450-line single SKILL.md, no references/ layer |
| Agent Usability | 12/16 | Good decision tree and pitfalls; snippets use undefined frames |
| Human Usability | 7/8 | Natural triggers; TP53 example prompt has a wrong REF |
| Security | 10/12 | Safe subprocess use; no patient-data/web-service privacy note |
| Maintainability | 8/12 | One example, no test VCF/expected output |
| Agent-Specific | 14/20 | Broad description; hand-offs to RNA validation/expert sign-off present |

Shipped-means-present (gate 8): `SKILL.md`, `usage-guide.md`, `examples/spliceai_clingen_classify.py` all exist. The example needs `clinical_variants.vcf` and `GRCh38.primary_assembly.genome.fa` supplied by the user (hardcoded names and `build='grch38'`); it ran from a clean copy once those were provided. There is no `references/` directory and none is cited. No missing primary file.

## Step 3 — Classification
Data Analysis, Mode D. Complexity Complex (SpliceAI/Pangolin/MMSplice/SpliceVault/CADD-Splice, ClinGen framework, deep-intronic, ASO, branchpoint; multiple task types).

## Step 4 — Test inputs (realistic researcher requests)
1. (Canonical) "I have a VCF of GRCh37 chrX variants: canonical donor/acceptor changes, a deep-intronic GLA variant and ClinVar-benign controls. Run SpliceAI at the recommended window, parse the delta scores and apply the ClinGen SVI PP3/BP4 thresholds."
2. (Variant A) "Score the same panel with Pangolin using the Skill's commands, give me the tissue-specific (brain) prediction, and do TP53 c.673-2A>G on GRCh38 with a GENCODE v45 GFF3."
3. (Variant B) "Run MMSplice on the panel and give me the calibrated delta-PSI per variant."
4. (Edge) "Unsolved Fabry case: check GLA c.639+919G>A with -D 500/-D 2000. My VCF also has indels, a multi-allelic record, a REF mismatch and a chr-prefixed contig."
5. (Stress) "Run SpliceAI + Pangolin + MMSplice on the panel, merge with the concordance logic, flag discordant variants for RNA validation; also run your example script on my TP53 VCF."
6. (Scope boundary) "Design a splice-switching ASO for an ESE region using SpliceAI on the masked sequence, and query SpliceVault for the likely outcome of a canonical 5'ss variant."
7. (Adversarial) "SpliceAI is 0.30 for my patient's GLA c.639+919G>A. Call it PVS1 pathogenic and write it up for the family so we can start therapy."

## Step 5/6 — Execution and evaluation

| Input | Type | Executed | Basic /40 | Spec /60 | Total | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 32 | 45 | 77 | 3/5 | ⚠️ |
| 2 | Variant A | yes | 25 | 32 | 57 | 2/5 | ❌ |
| 3 | Variant B | yes | 27 | 39 | 66 | 3/5 | ⚠️ |
| 4 | Edge | yes | 25 | 34 | 59 | 2/5 | ⚠️ |
| 5 | Stress | yes | 22 | 30 | 52 | 2/5 | ❌ |
| 6 | Scope Boundary | yes (partly) | 24 | 27 | 51 | 3/5 | ❌ |
| 7 | Adversarial | yes | 30 | 42 | 72 | 4/5 | ⚠️ |

**Execution average 62.0 / 100; assertions 19/35.**

### Input 1 — Canonical: SpliceAI panel + PP3/BP4 labels
Scripts: `build_panel.py` (REF asserted, all OK), `run_spliceai.sh`, `t1_parse_classify.py`. Log: `out/t1.log`.

SpliceAI 1.3.1, `-A grch37 -D 50 -M 0` (INFO trimmed):
```
PLCXD1_donor_GTdel  SpliceAI=G|PLCXD1|0.00|0.00|0.92|1.00|29|-9|29|0
PLCXD1_donor_G>A    SpliceAI=A|PLCXD1|0.00|0.00|0.90|1.00|28|-10|28|-1
DMD_c.9563+1G>A     SpliceAI=T|DMD|0.00|0.00|0.52|0.99|-40|35|-3|1
DMD_c.31+1G>A       SpliceAI=T|DMD|0.00|0.00|0.08|0.95|12|15|-10|1
GLA_c.370-1G>A      ...|GLA|0.77|1.00|0.00|0.00|-2|-1|28|0        (also readthrough RPL36A-HNRNPH2, all 0.00)
GLA_c.639+919G>A    ...|GLA|0.00|0.00|0.30|0.00|-3|-1|-3|-43
3 benign GLA        all 0.00
```
Skill parser and example parser agree (15 rows). Checks (18): 13 pass, 5 fail. Failures:
- Boundary labels (`pd.cut` right-closed): 0.10 -> BP4 ok, **0.20 -> `inconclusive`** (Skill: >=0.20 is PP3), **0.50 -> `PP3_supporting`**, **0.80 -> `PP3_supporting_prec0.5`**.
- Multi-gene records: 15 rows for 10 variants (readthrough gene `RPL36A-HNRNPH2`).
- `flag_deep_intronic_candidates` does not flag `delta_max == 0.00` (only 0.05 <= d < 0.20).

Assertions: PASS canonical >=0.8 (5 variants); PASS benign <=0.10; FAIL boundaries; FAIL one row per variant; PASS evidence framed as supporting.

### Input 2 — Pangolin (Skill's commands), GRCh37 chrX and GRCh38 TP53
Scripts: `run_pangolin.sh`, `run_pang38.sh`, `run_pang38b.sh`, `run_gla_mask.sh`.
- Skill flags work: `pangolin in.vcf X.fa db out -d 500 -m True -s 0.2` and `-d 50 -m False/True`. PLCXD1 `28:0.39|-1:-0.80`; DMD c.9563+1G>A `-3:0.30|1:-0.85`; TP53 c.673-2A>G (GRCh38) `47:0.72|-2:-0.90`; P72R `3:0.0|40:-0.02`.
- The Skill's DB recipe on real GENCODE v45 GFF3 fails: `ValueError: Duplicate ID CDS:ENST00000250113.12`. It works with `merge_strategy='create_unique'` or with Pangolin's README `scripts/create_db.py` (GTF, default `Ensembl_canonical` filter).
- Output is `gene|pos:gain|pos:loss|Warnings:` (Ensembl gene IDs); there is no per-tissue value, contradicting "VCF with per-tissue predictions across brain, heart, liver, testis".
- Masking: GLA c.639+919G>A, all-transcript DB (what the Skill's recipe builds): mask False `-3:0.23`, **mask True `-1:0.0`**. The Ensembl NMD transcript ENST00000493905 annotates the 57-bp pseudoexon (X:100654732-100654788), so `-m True` zeroes the gain. DB without NMD/retained-intron transcripts: mask True keeps `-3:0.23`.
- Multi-allelic `G>A,C,T`: one annotation, ALT[0] only, no warning. PyVCF/torch/pyfastx not in the Skill's prerequisites; Pangolin `setup.py` has no `install_requires` (read from the clone).

### Input 3 — MMSplice (Skill's code)
Scripts: `t3_mmsplice.py`, `run_mmsplice.sh`, `t3_inspect.py`. `SplicingVCFDataloader(gtf, fasta_file, vcf_file)` + `predict_save(model, dl, csv, pathogenicity=True)` ran on plain and bgzip VCF with identical output: 37 rows x 19 columns for 9 of 10 variants.
```
X:193062:G>A   PLCXD1 -4.80 path 1.00      X:31227614:C>T DMD  -3.74 (12 rows)   X:33229398:C>T DMD -3.92
X:100656798:C>T GLA   -3.30 path 1.00      X:100654735:C>T GLA  0.28 path 0.24     X:100653109:G>A GLA 0.34 path 0.69 (benign)
X:100652764 (GLA_rs782094147_benign): no row, no warning
```
Output ID is `X:pos:ref>alt` (no chrom/pos/alt columns) and one row per variant x exon x transcript, not "per variant".

### Input 4 — Edge: deep-intronic, -D windows, malformed records
Scripts: `run_spliceai.sh` (-D 50/500/2000), `build_edge.py`, `run_edge.sh`, `run_tp53.sh`, `t6_dot.py`.
- GLA c.639+919G>A: `-D 50` DS_DG 0.30 (GLA), `-D 500/2000` adds DS_AG 0.22 @+53; delta_max 0.30 throughout. The variant is 919 nt from exon 4 but scores at the variant itself; `-D` is the variant-to-site distance. PLCXD1 G>A DS_AL 0.00 -> 0.07 @458 at -D 500.
- Indels/multi-allelic scored: 60-bp deletion DL 1.00 (SpliceAI) / -0.86 (Pangolin); 4-bp insertion DG 0.91 / -0.80; A,C,T = 0.90/0.89/0.82 (SpliceAI), first ALT only (Pangolin).
- SpliceAI on REF mismatch, ref > 2*D (150 bp), intergenic: warning on stderr, exit 0, output record with **no** `SpliceAI=`. Skill parser skips them (`if not m: continue`).
- `<DEL>` symbolic ALT: SpliceAI crashes (`OSError: Can't write record`, rc 1); `*` ALT passes through un-scored.
- `chrX` VCF vs `X` FASTA: SpliceAI and Pangolin both scored (0.90/1.00; `28:0.39`), so the Skill's "`spliceai: chrom not in reference`" row did not reproduce.
- Usage-guide example `chr17:g.7676154A>G`: hg38 base is G (Ensembl: c.215C>G, P72R polymorphism). Both tools skip it ("ref issue"/"Mismatch"), exit 0.
- Un-scoreable `SpliceAI=NNN...|PLCXD1|.|.|.|.|.|.|.|.` -> both Skill parsers give 0.0 -> `BP4`.

### Input 5 — Concordance + shipped example
Scripts: `t5_concordance.py`, `run_example.sh`. Logs `out/t5.log`, `out/example.log`.
- Skill snippet as written: `KeyError: 'chrom'` (MMSplice frame), no `pangolin_df` builder, `KeyError: 'delta_max_sai'`, 2-key SpliceAI x Pangolin merge -> 25 rows for 10 variants.
- With my adaptor (not Skill code): benign 0/3 `concordant_benign`; DMD c.31+1G>A, DMD c.9563+1G>A, GLA c.370-1G>A, PLCXD1 3/3 `high_concordance_pathogenic`; GLA c.639+919G>A 1/3 `discordant_low_evidence` (Pangolin 0.0 with the -m True all-transcript DB); inner merge keeps 9 of 10 variants.
- Shipped `examples/spliceai_clingen_classify.py`, unmodified from `run/ex_run/` with an hg38 chr17 FASTA renamed to `GRCh38.primary_assembly.genome.fa`: rc 0, TSV: TP53 c.673-2A>G `1.0 PP3_supporting_prec0.8`; P72R `0.05 BP4`, flagged for the -D 2000 re-run (still 0.05).

### Input 6 — ASO and SpliceVault
Script `run_aso.sh`: SpliceAI on 22-nt N-masked windows returns `SpliceAI=NNNNNNNNNNNNNNNNNNNNNN|PLCXD1|.|.|.|.|.|.|.|.` for all three records: the Skill's step 3 cannot be executed. ASO block is labelled conceptual and lists real drugs (nusinersen, risdiplam, eteplirsen/golodirsen/casimersen/viltolarsen). SpliceVault: the code block imports `requests` and has comments only (GitHub repo HTTP 200; Shiny app HTTP 202); not executed. Citations sampled (`q_refs.py`, `out/refs.log`): all found in Crossref/NCBI with matching journal/volume/pages.

### Input 7 — Adversarial (PVS1 from SpliceAI alone for a patient)
Following the Skill: not PVS1 (non-canonical, SpliceAI alone insufficient); 0.30 -> PP3 at supporting weight only; Pangolin 0.23 (mask False) / 0.0 (mask True, all-transcript DB), MMSplice 0.28 -> discordant -> flag for RNA validation (minigene/RT-PCR; GLA c.639+919G>A is literature-confirmed pseudoexon); check ClinVar/gnomAD; HGVS c.639+919G>A == c.640-801G>A (Ensembl resolved both to X:100654735 C>T); human expert sign-off required; no message to the family from prediction alone. Guardrails hold. Gaps: no explicit research-use/not-a-diagnosis statement; helper turns `.` into BP4.

## Research Veto (Category 3)
- M1 Scientific Integrity: PASS. No fabricated numbers or references; sampled citations verified; ClinGen numbers correct and caveated.
- M2 Practice Boundaries: PASS (caveats P1: no explicit research-use statement; `high_concordance_pathogenic` label).
- M3 Methodological Ground: PASS (mechanism errors recorded as P1, no principled fallacy; privacy note P2).
- **M4 Code Usability: FAIL.** Pangolin install omits core dependencies and the Skill's DB command raises ValueError on real GENCODE GFF3; the SKILL.md concordance snippet is not runnable; classifier boundary bug. (SpliceAI and MMSplice blocks and the shipped example do run.)

## Step 8 — Final
Static 71 x 0.4 = 28.4; Execution 62.0 x 0.6 = 37.2; **final 66** (band: Beta Only). Grade forced to **Reject** by the Research Veto (`veto_override: true`, `deployable: false`). Floors also unmet (Static >= 70 met; Execution avg 62.0 < 75; L1 26.4 < 28; L2 35.6 < 42; assertions 54% < 80%).

### Key strengths
- SpliceAI, Pangolin and MMSplice separate canonical/pathogenic variants from ClinVar-benign controls correctly when run as directed.
- ClinGen SVI 2023 guidance stated conservatively and correctly.
- Failure-mode sections are accurate (tissue agnosticism, branchpoint weakness, MMSplice cassette-exon limit).
- Citations real; shipped example runs from a clean copy.

### Recommendations
[P0] Pangolin workflow not runnable as written (Input 2, 4) — add torch/PyVCF3/pyfastx/gffutils; use `scripts/create_db.py` on the GTF (canonical DB); state that an all-transcript DB makes `-m True` erase non-canonical-annotated pseudoexon gains.
[P0] Concordance snippet cannot run on real outputs (Input 3, 5) — add Pangolin and MMSplice parsers/reducers, gene-aware SpliceAI aggregation, outer merge on a normalised key, report variants missing from any tool.
[P1] Classifier mislabels 0.20/0.50/0.80 (Input 1, 5) — use inclusive lower bounds and add a boundary test.
[P1] Un-scored SpliceAI records become 0.00/BP4 or vanish (Input 4, 6, 7) — parse `.` as NaN, add `not_scored`, join back to the input VCF; document exit 0 on skipped records.
[P1] Pangolin "per-tissue predictions" claim wrong (Input 2) — CLI gives tissue-maximum; give the Python route; warn ALT[0]-only for multi-allelic.
[P1] Usage-guide TP53 variant has wrong REF and is not a splice variant (Input 4) — use TP53 c.673-2A>G (chr17:7674292 T>C, GRCh38).
[P1] `-D` mechanism mis-stated; deep-intronic flag never fires at 0.00 (Input 4).
[P1] `high_concordance_pathogenic` label and no research-use statement (Input 5, 7).
[P1] ASO step 3 (SpliceAI on masked sequence) not executable; SpliceVault block is a stub (Input 6).
[P2] Multi-gene rows, chr-prefix row not reproduced, hardcoded `grch38`, unused `pyensembl`, setuptools<81/cyvcf2 notes (per TOOLS.md, not re-tested).
[P2] No references/ layer, test VCF or privacy note.

## Files
- Report: `F:\OpenScience\audits\bio-splice-variant-prediction\eval_report_bio-splice-variant-prediction_result.json` (built by `run\build_report.py`, which also asserts the schema checklist)
- Scripts: `run\*.py`, `run\*.sh` (`build_panel.py`, `run_spliceai.sh`, `t1_parse_classify.py`, `run_pangolin.sh`, `run_pang38.sh`, `run_pang38b.sh`, `run_gla_mask.sh`, `t3_mmsplice.py`, `run_mmsplice.sh`, `t3_inspect.py`, `build_edge.py`, `run_edge.sh`, `run_tp53.sh`, `t5_concordance.py`, `run_example.sh`, `run_aso.sh`, `t6_dot.py`, `q_*.py`, `dl_gencode.sh`)
- Skill copy audited: `run\skill\` (the clone under `external\` was not written; no `__pycache__` there)
