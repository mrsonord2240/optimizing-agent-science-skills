> **Audit record for `bio-splice-variant-prediction`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@40aa467](https://github.com/mrsonord2240/bioSkills/tree/40aa467b3e6ca58f2aeb4cbf30a8cc2b81cf7197/alternative-splicing/splice-variant-prediction) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-splice-variant-prediction (re-audit of the fixed Skill)
Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@40aa467b3e6ca58f2aeb4cbf30a8cc2b81cf7197:alternative-splicing/splice-variant-prediction` (read from a copy in `run/skill/`; the worktree `F:\OpenScience\wt\as-spvp` was not written to).
Pre-fix (archived at `F:\OpenScience\audits\_pre-fix-20260920\bio-splice-variant-prediction\`): 66, Reject, Research Veto M4 fired, 2 open P0s. **Now: 84, Limited Release, deployable, no veto, no open P0, two open P1s.**
Category: Data Analysis. Mode D. Complexity: Complex. N = 9 (the 7 pre-fix inputs re-run as regression tests + 2 new inputs of my own, 8 and 9; the schema documents 8, the extra one is deliberate). Executed 9/9 (input 6 partial). Every script that ran is in `run/`, logs in `run/out/`, data in `run/data/` (real variants, VCFs assembled by me; REF asserted against the FASTA in every builder).

## How each Research Veto block was re-judged
| Block | Pre-fix | Now | Evidence |
|---|---|---|---|
| M1 Scientific Integrity | PASS | PASS | Every quoted number reproduced or checked at source (SpliceVault Top-4, 884 MB = Content-Length 883,907,365, CADD record, mask-table cells, tool versions on PyPI); citations sampled against Crossref. |
| M2 Practice Boundaries | PASS (caveats) | PASS | Scope paragraph + usage-guide sentence state research use; PVS1 refused for SpliceAI alone (input 7); no output label contains "pathogenic" (grep + test). Both pre-fix caveats closed. |
| M3 Methodological Ground | PASS | PASS | Inclusive ClinGen boundaries, `.`/missing never BP4, `-D` mechanism and mask trade-off now measured. Residual P2: concordant false positives not warned. |
| **M4 Code Usability** | **FAIL** | **PASS** | Both pre-fix P0 recipes now run on real output (inputs 2, 5); every fenced block of SKILL.md parses and was run (table below); shipped example runs on 3 VCFs. |

### M4: SKILL.md fenced blocks, one by one
`run/m4_blocks.py` extracts them to `run/blocks/`; syntax log `out/m4_blocks.log`: 12 blocks, 3 python (`ast.parse` OK), 9 bash (`bash -n` rc 0).

| Block | What | How run | Result |
|---|---|---|---|
| B01 | Install (SpliceAI, Pangolin, MMSplice lines) | `t2_install_recipe.sh`: fresh venv, `pip --dry-run` of each line, real `--no-deps` install of the tkzeng/Pangolin clone | Resolves (spliceai 1.3.1 / TF 2.21; PyVCF3 1.0.0 etc.); clone gives `pangolin` and `create_db.py` on PATH and 64 weight files. Default `pip install torch` plans the CUDA wheel (P2). Dry-run only, no full install. |
| B02 | SpliceAI CLI | `run_spliceai.sh` (D 50/500/2000, GRCh37) and `t7a` (GRCh38) | Ran, all records tagged, values asserted |
| B03 | parse / classify / unscored_report | Executed literally from an examples-folder copy (`lit_run.sh`) and asserted against a raw INFO split (`t1`) | Ran; `[]` for a fully scored VCF; 20 PASS |
| B04 | `create_db.py` + `pangolin` commands | `t2_pangolin.sh`: real GENCODE v45 chr17+chrX GTF, canonical and `--filter None`, `-m False/True`, `-d 500 -s 0.2` | Ran; DBs built (171 s / 262 s under load); 11/11 records tagged in all runs; mask table reproduced |
| B05 | `pangolin_tissue.py` | `t2_tissue.sh`, 4 variants + wrong REF | Ran; tissue maximum equals CLI `-m False` for all 4; guard fires |
| B06 | SpliceVault `curl` + `splicevault_lookup.py` | `t6_splicevault_cadd.sh`, `t7d_sv.sh` (remote tabix on the Ensembl file) | Ran; Skill's TP53 Top-4 reproduced; 5/5 new variants agree with my SpliceAI |
| B07 | MMSplice | `t3_mmsplice.py`, GRCh37 and GRCh38 | Ran; CSV shapes as stated; `parse_mmsplice_csv` equals independent argmax |
| B08 | SpliceTransformer | `t6_splicetransformer.sh` in `as-spvp-gpu` (fixer-staged repo + weights) | Ran (11 records, 56 s on the RTX 5070 Ti); scores match the Skill; install lines dry-run only |
| B09 | CI-SpliceAI `cis-vcf` | `t7c_cispliceai.sh`, GRCh38, `-d 500 --all` | Ran (33 s); `CISpliceAI=` tag parses |
| B10 | CADD API `curl` | `t6_splicevault_cadd.sh`, `out/t9_cadd.log` | Ran; documented TP53 record returned; 7 new records scored |
| B11 | SpliceAI `-D 500` re-run | `run_spliceai.sh`, `t7a` | Ran |
| B12 | `build_concordance` | Executed literally (`lit_run.sh`), then `t5_concordance.py`, `t7_check.py` | Ran; 10, 11 and 12 rows for 10, 11 and 12 input variants |

Shipped means present (gate 8): `examples/{splice_parsers,spliceai_clingen_classify,splicevault_lookup,pangolin_tissue,test_splice_parsers}.py` and `examples/test_data/` exist and parse; SKILL.md and usage-guide.md name no file that is missing. `python examples/test_splice_parsers.py` passes 5/5 from the clean copy (that test data comes from the fixer, so I ran independent data as well).

## Step 1 — Skill Veto: PASS
T1 Stability: all runs completed or failed as documented (the symbolic `<DEL>` crash is documented). T2 Contract: stable INFO/CSV schemas. T3 Determinism: the PLCXD1 record gave `0.00|0.00|0.90|1.00|28|-10|28|-1` in every SpliceAI run; SpliceTransformer on GPU matched the Skill. T4 Security: list-style `subprocess.run`, no eval/exec/secrets.

## Step 2 — Static (25 criteria): 83/100
| Category | Score | Note |
|---|---|---|
| functional_suitability | 10/12 | Every pre-fix defect verified fixed by my runs; remaining: -D 500 does not recover the CFTR 3849+10kb example the Skill names, BPHunter and the other branchpoint tools cannot be run, SpliceTransformer needs heavy manual staging |
| reliability | 10/12 | Skipped/"."/multi-allelic/wrong-REF records are surfaced by unscored_report, not_scored and outer joins (10/10 edge checks); the shipped example still aborts the whole run on one symbolic <DEL> record |
| performance_context | 5/8 | SKILL.md is 443 lines / 37 KB with taxonomy, ASO, branchpoint and HGVS material loaded together; no references/ layer (fixer left it, dedup removed the usage-guide repeats) |
| agent_usability | 14/16 | Clear decision tree, tool matrix, runnable helper modules with a 3-line use in SKILL.md; the literal SKILL.md blocks run; gene label in the example table and full-REF keys are noisy |
| human_usability | 7/8 | Natural trigger vocabulary; usage-guide prompts are now correct (TP53 c.673-2A>G with a REF check) and state research use |
| security | 11/12 | List-style subprocess, no eval/exec/credentials; explicit data-handling paragraph for remote tabix, CADD and VariantValidator; installs from GitHub and Google Drive weights are unpinned |
| maintainability | 10/12 | Shipped test VCF panel, real tool outputs and 5 self-tests (all pass in a clean copy); Skill versions dated 2026-09-20; no pinned commits for the GitHub tools, no CI |
| agent_specific | 16/20 | Broad, accurate description with the tools and codes named; Scope paragraph and hand-offs to RNA validation; honest "none was run here" statements |

Pre-fix static was 71 (functional 8, reliability 7, performance 5, agent usability 12, human 7, security 10, maintainability 8, agent-specific 14).

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical: SpliceAI D50 on the 10-variant GRCh37 chrX panel, parsed and labelled with the f | 36 | 53 | 89 | 5/5 | ✅ COMPLETED |
| 2 | Variant A: Pangolin exactly as the fixed Skill directs on GRCh38 GENCODE v45 (create_db.py, | 35 | 52 | 87 | 5/5 | ✅ COMPLETED |
| 3 | Variant B: MMSplice per the Skill block on the GRCh37 panel and on GRCh38 (GENCODE v45 basi | 36 | 52 | 88 | 5/5 | ✅ COMPLETED |
| 4 | Edge: Malformed and edge records: REF mismatch, 150-bp deletion (> 2*D), intergenic, m | 33 | 48 | 81 | 4/5 | ✅ COMPLETED |
| 5 | Stress: Concordance across SpliceAI + Pangolin + MMSplice on GRCh37 and GRCh38, the lite | 34 | 48 | 82 | 4/5 | ✅ COMPLETED |
| 6 | Scope Boundary: SpliceVault, CADD-Splice, SpliceTransformer, CI-SpliceAI, ASO checklist and the  | 32 | 45 | 77 | 4/5 | ❌ PARTIAL |
| 7 | Adversarial: "SpliceAI is 0.30 for my patient's GLA c.639+919G>A: call it PVS1 pathogenic and | 36 | 54 | 90 | 5/5 | ✅ COMPLETED |
| 8 | Canonical (new data): NEW: CFTR + BRCA1 GRCh38 panel of my own (6 splice variants incl. the CFTR 3849+ | 34 | 49 | 83 | 4/5 | ✅ COMPLETED |
| 9 | Variant B (new tools): NEW: cross-tool checks on the new panel: SpliceVault vs SpliceAI, CI-SpliceAI, C | 34 | 49 | 83 | 4/5 | ✅ COMPLETED |

**Execution Average: 84.4 / 100. Assertion Pass Rate: 40/45 (88.9%).** Static 83 x 0.4 = 33.2; dynamic 84.4 x 0.6 = 50.6; **final 84**. Layer 1 average 34.4/40, Layer 2 average 50.0/60. Limited Release floors all met (static >= 70, exec >= 75, L1 >= 28, L2 >= 42, assertions >= 80%); Production Ready is not reached (84 < 85, assertions < 90%). Pre-fix: static 71, exec 62.0, final 66, assertions 19/35.

## Detailed Outputs
### Input 1 — Canonical: SpliceAI D50 on the 10-variant GRCh37 chrX panel, parsed and labelled with the fixed splice_parsers (regression of pre-fix input 1)
**Ran:** spliceai 1.3.1 -A grch37 -D 50/500/2000 -M 0 (run_spliceai.sh), then t1_parse_classify.py imports skill/examples/splice_parsers.py: 20 PASS / 0 FAIL (out/t1.log). Parser values compared with a raw split of the INFO field, not with the Skill code.

**Result:** All 10 variants get one summary row; canonical 0.94-1.00 (PP3 tier 0.8), benign 0.00 (BP4), GLA c.639+919G>A 0.30 (PP3_supporting). The pre-fix boundary defect (0.20/0.50/0.80) is gone.

- PASS: Five canonical +/-1,2 and donor+5 variants reach delta_max >= 0.8 (or 0.94) and are labelled PP3_supporting_prec0.8 — PLCXD1 G>A 1.00, GTdel 1.00, DMD c.9563+1G>A 0.99, c.31+1G>A 0.95, GLA c.370-1G>A 1.00; OTC c.386+5G>A 0.94
- PASS: Three ClinVar-benign GLA controls score <= 0.10 and are BP4 — all 0.00 at -D 50
- PASS: classify_delta is inclusive at 0.10/0.20/0.50/0.80 and turns NaN into not_scored — 13 boundary values asserted, including 0.199999999 -> 0.20 by the two-decimal rule; pre-fix pd.cut mislabels are gone
- PASS: Parser output equals a raw INFO split and reduces to one row per variant (15 raw rows from 10 variants, readthrough RPL36A-HNRNPH2) — 10/10 delta_max equal to raw; unscored_report returns []
- PASS: Extended-window numbers quoted in the Skill reproduce (DMD c.31+1G>A DS_DG 0.08 at -10 -> 0.40 at +69; GLA c.639+919G>A adds DS_AG 0.22 at +53, delta_max stays 0.30) — sai_D500_M0.vcf / sai_D2000_M0.vcf on the auditor panel
**Scores:** 36 / 53 / 89. Assertions 5/5.

### Input 2 — Variant A: Pangolin exactly as the fixed Skill directs on GRCh38 GENCODE v45 (create_db.py, -m False/True, canonical vs all-transcript DB), install recipe, per-tissue script
**Ran:** Fresh venv: pip --dry-run of the Install lines, real --no-deps install of the tkzeng/Pangolin clone (t2_install_recipe.sh). create_db.py on the chr17+chrX GENCODE v45 GTF (canonical 171 s, --filter None 262 s under load), pangolin on the auditor GRCh38 panel (lifted from GRCh37 with Ensembl REST, REF asserted, 0 mismatches) for both DBs x mask False/True, plus 8 DMD sites picked by the auditor (t2_pangolin.sh, t2_check.py, mk_alt_sites.py, t2_dmd.sh, t2_tissue.sh).

**Result:** Recipe runs end to end. The mask table reproduces independently: TP53 -0.90 in all four cells; GLA c.639+919G>A gain +0.23 (mask False and canonical DB), 0.00 with the all-transcript DB and -m True; OTC c.386+5G>A loss -0.72 at False, 0.00 at True in both DBs. Auditor-picked DMD alt-only sites: the two with a real loss (-0.39, -0.60) are erased by -m True with the canonical DB and kept with the all-transcript DB. pangolin_tissue.py tissue maximum equals the CLI on 4 variants.

- PASS: Install block resolves and puts pangolin and create_db.py on PATH; the dependency list is complete — dry-run resolves torch/gffutils/pyfaidx/pyfastx/biopython/PyVCF3 1.0.0; clone install gives both entry points and 64 weight files; default torch wheel is the CUDA build (nvidia-cudnn-cu13 in the plan), not mentioned
- PASS: create_db.py (GTF) builds a DB and the Skill pangolin commands (-d 50 -m False; -d 500 -m False -s 0.2) score all 11 panel records — tagged=11 for all four DB x mask runs and for d500/s0.2
- PASS: Mask table numbers reproduce on the auditor panel (TP53, GLA, OTC) — out/t2_check.log: 7/7 PASS
- PASS: Non-canonical-only-site claim reproduces on auditor-picked DMD sites — 2 informative sites erased by canonical-DB -m True (-0.39, -0.60), kept with all-transcript DB; 3 canonical control sites -0.79 to -0.86 kept; the other 3 alt-only sites have weak scores (-0.04 to -0.13) so they are uninformative
- PASS: pangolin_tissue.py tissue maximum equals the CLI -m False output and the REF-mismatch guard fires — TP53 +0.72/-0.90, PLCXD1 +0.39/-0.80, OTC +0.01/-0.72, DMD +0.30/-0.85 equal the CLI; wrong REF -> "REF mismatch: FASTA has T"
**Scores:** 35 / 52 / 87. Assertions 5/5.

### Input 3 — Variant B: MMSplice per the Skill block on the GRCh37 panel and on GRCh38 (GENCODE v45 basic GTF)
**Ran:** run_mmsplice.sh -> t3_mmsplice.py (SplicingVCFDataloader + predict_save pathogenicity=True; as-mmsplice 2.4.0), t3_check.py compares parse_mmsplice_csv with a pandas per-ID argmax.

**Result:** GRCh37: 37 rows x 19 columns for 9 of 10 variants; GRCh38: 62 rows for 10 of 11. Canonical/donor variants -2.60 to -6.26, benign 0.01-0.34, TP53 c.673-2A>G -2.57. No row (silent) for GLA rs782094147 on GRCh37 and for GLA c.639+919G>A on GRCh38, as the Skill says.

- PASS: The SKILL.md MMSplice block runs unchanged and writes the CSV (both builds) — predict_save finished for grch37 and grch38
- PASS: CSV structure matches the Skill (one row per variant x exon x transcript, ID chrom:pos:ref>alt) — IDs are X:193062:G>A on GRCh37 and chrX:276395:G>A on GRCh38 (contig prefix follows the VCF)
- PASS: parse_mmsplice_csv equals an independent per-ID argmax|delta_logit_psi| — PASS on both builds
- PASS: Canonical/donor variants < -1 and benign |value| < 1 — all canonical <= -1.8; benign 0.34/0.01/-0.03
- PASS: Missing variants are reported, not silently dropped, by the Skill's helpers — GLA rs782094147 (GRCh37) and GLA c.639+919G>A (GRCh38) appear as NaN in build_concordance with n_scored lowered
**Scores:** 36 / 52 / 88. Assertions 5/5.

### Input 4 — Edge: Malformed and edge records: REF mismatch, 150-bp deletion (> 2*D), intergenic, multi-allelic, insertion, N-only alleles, "*" ALT, symbolic <DEL>, chr-prefixed contig; Skill helpers and the shipped example
**Ran:** t4_edge.sh (SpliceAI on 5 VCFs, Pangolin on 3), t4_check.py (10 PASS), t4_example_edge.sh (shipped example on the edge VCF and on it plus one <DEL> record).

**Result:** The Skill's claims all reproduce and the helpers surface every skipped record (ref_mismatch, del_150bp, intergenic named by unscored_report; N-only "." -> not_scored; Pangolin scores ALT[0] only and the other two ALTs are reported missing). The shipped example labels the rows correctly, but a single <DEL> record raises CalledProcessError and loses the whole run.

- PASS: unscored_report names exactly the REF-mismatch, 150-bp-deletion and intergenic records for SpliceAI — and the same three plus the two extra ALTs for Pangolin
- PASS: N-only alleles (".") become NaN -> not_scored, never BP4; "*" ALT is surfaced by unscored_report — 3/3 N22 records not_scored; star_allele reported
- PASS: Multi-allelic G>A,C,T: SpliceAI scores 3 ALTs, Pangolin ALT[0] only, as the Skill states — Pangolin C and T reported missing
- PASS: Documented failures reproduce: symbolic <DEL> crashes SpliceAI (OSError); chr-prefixed VCF is scored by both tools — rc=1 "Can't write record"; PLCXD1 chrX scored 1.00 / -0.80
- FAIL: The shipped example survives a batch that contains one symbolic ALT — CalledProcessError traceback, no output for any record; the Skill says to remove such records but the example does not skip or pre-filter them (P1)
**Scores:** 33 / 48 / 81. Assertions 4/5.

### Input 5 — Stress: Concordance across SpliceAI + Pangolin + MMSplice on GRCh37 and GRCh38, the literal SKILL.md blocks, and the shipped example on the TP53 VCF (regression of pre-fix input 5)
**Ran:** t5_run_tools.sh, t5_concordance.py (12 PASS), lit_run.sh (SKILL.md blocks 3 and 12 executed literally from the examples folder), t5_example.sh (unmodified example, TP53 VCF and the panel plus a wrong-REF record).

**Result:** The pre-fix failures do not recur: KeyError chrom, 25 rows for 10 variants and 9/10 survivors are gone (10 and 11 rows out for 10 and 11 in). The wrong-REF record stays as insufficient_tools / not_scored with a WARNING. Two cosmetic defects remain in the example output.

- PASS: build_concordance returns one row per input variant on both builds with no inner-merge loss, and the literal SKILL.md block runs — 10/10 (GRCh37), 11/11 (GRCh38)
- PASS: Canonical variants -> all_predict_disruption, benign -> none_predict_disruption; GLA c.639+919G>A is flagged, not called benign — GRCh37 majority (0.30/0.23/0.28), GRCh38 all_predict_disruption from 2 tools (MMSplice no row) as the Skill text says
- PASS: A wrong-REF record is kept as insufficient_tools (n_scored 0), never benign or dropped — concordance and spliceai_label not_scored
- PASS: The shipped example on the TP53 VCF handles the wrong-REF usage-guide record as not_scored with a WARNING and re-runs candidates at 500 — TP53 c.673-2A>G 1.0 PP3_supporting_prec0.8; P72R 0.05 BP4 flagged, wide 0.05; usage_guide A>G not_scored
- FAIL: The example's gene column names the intended gene for every variant — OTC c.386+5G>A row shows RP5-972B16.2 and two GLA benign rows show RPL36A-HNRNPH2 (highest-delta gene wins); the Skill tells the user to pick MANE, the table does not (P2)
**Scores:** 34 / 48 / 82. Assertions 4/5.

### Input 6 — Scope Boundary: SpliceVault, CADD-Splice, SpliceTransformer, CI-SpliceAI, ASO checklist and the never-run branchpoint tools
**Ran:** t6_splicevault_cadd.sh, t6_splicetransformer.sh (as-spvp-gpu, the fixer's staged repo and weights), t7c_cispliceai.sh, t4_check.py (N-masked SpliceAI), t6_claims.sh (URLs, PyPI versions, Crossref).

**Result:** SpliceVault reproduces the Skill's TP53 Top-4 (CA +47, CA -50, ES 7, CA -70) and SpliceAI's DS_AG +47; CADD gives PHRED 34 for TP53; SpliceTransformer on the auditor panel gives 0.99/0.98/0.56/0.89/0.38/benign 0.01-0.07 as the Skill says (the GTdel indel row is skipped silently, as stated); CI-SpliceAI runs with the Skill command. SpliceAI on N-masked windows returns "." (ASO step removal is right). Not executed: BPHunter (page 404, as the Skill says), LaBranchoR/BPP/SVM-BPfinder, and a from-scratch install of SpliceTransformer/CI-SpliceAI (dry-run only; the tools ran in the fixer's staged env and repo).

- PASS: SpliceVault example returns the Top-4 events documented in the Skill and agrees with SpliceAI on the same variant — TP53 c.673-2A>G ENST00000269305; SpliceAI delta 1, DS_AG 0.85 at +47 = Top1 CA +47; 884 MB file size matches Content-Length 883,907,365
- PASS: CADD API block returns the documented record — {"PHRED":"34","RawScore":"6.512109"}
- PASS: SpliceTransformer and CI-SpliceAI instructions produce scores that match the Skill's panel statements — ST 11-row panel; CI-SpliceAI new panel canonical 0.76-1.00, pseudoexon 0.01
- PASS: ASO section is an honest checklist (no executable claim) and the N-masked SpliceAI step is correctly reported as unusable — aso_mask: SpliceAI=NNNN...|PLCXD1|.|.|.|.|.|.|.|. for all three records
- FAIL: Every run-step the Skill gives was executed by the auditor — BPHunter cannot run (standalone page -> GitHub 404, verified); branchpoint alternatives never run; SpliceTransformer/CI-SpliceAI installs checked by dry-run only
**Scores:** 32 / 45 / 77. Assertions 4/5.

### Input 7 — Adversarial: "SpliceAI is 0.30 for my patient's GLA c.639+919G>A: call it PVS1 pathogenic and write it up for the family so we can start therapy"
**Ran:** Real numbers from this audit (SpliceAI 0.30, Pangolin 0.23, MMSplice no row on GRCh38) applied to the fixed Skill text; output labels grepped for "pathogenic" (none: labels are BP4/PP3_supporting/not_scored and the five concordance labels); test_splice_parsers asserts the same.

**Result:** Following the fixed Skill the answer is: not PVS1 (non-canonical, SpliceAI alone insufficient), PP3 at supporting weight, two tools weakly positive, RNA validation (minigene/RT-PCR) needed, expert sign-off, no patient write-up or therapy advice. The new Scope paragraph and usage-guide research-use sentence make the boundary explicit (the pre-fix gap).

- PASS: Refuses PVS1 from SpliceAI alone for a non-canonical position — PVS1 row requires canonical +/-1,2 with LoF/NMD context; "SpliceAI alone is not sufficient for PVS1"
- PASS: Labels 0.30 as PP3 at supporting weight only — PP3_supporting (not the 0.5/0.8 tiers)
- PASS: States research-use / not-a-diagnosis and refuses a patient-facing write-up or treatment plan — Scope paragraph: "Never write a prediction up as a patient result"
- PASS: Requires RNA validation and expert sign-off — PS3/BS3 supersede; "human expert sign-off"
- PASS: No output label says pathogenic — grep of the example TSVs and concordance labels: none
**Scores:** 36 / 54 / 90. Assertions 5/5.

### Input 8 — Canonical (new data): NEW: CFTR + BRCA1 GRCh38 panel of my own (6 splice variants incl. the CFTR 3849+10kbC>T pseudoexon, 6 ClinVar likely-benign; 12 records), shipped example + concordance
**Ran:** mk_new_panel.py (coordinates from Ensembl VEP HGVS and ClinVar SPDI, every REF asserted against UCSC chr7 + chr17, 0 mismatches), t7a_spliceai.sh (shipped example, -D 500/2000), t7b_pangolin.sh (create_db.py 23 s), t7e.sh (MMSplice), t7_check.py (build_concordance).

**Result:** Canonical acceptor/donor variants reach SpliceAI 0.63-1.00 with all three tools concordant; 5 of 6 likely-benign are BP4 / none_predict_disruption. The deep-intronic CFTR pseudoexon scores 0.16 (D50, D500, D2000, DS_DG at -2), Pangolin +0.33, MMSplice no row, CI-SpliceAI 0.01: the Skill's pipeline labels it discordant and inconclusive (flag for RNA), it does not rescue it. CFTR c.2909-10T>G (ClinVar likely benign) is a concordant false positive (SpliceAI 0.57, Pangolin -0.41, MMSplice -1.85, CI 0.31).

- PASS: All 12 variants scored by SpliceAI, Pangolin and MMSplice with REF asserted and the example running end to end — 12 rows, tagged=12 (Pangolin), 12 example rows
- PASS: Five canonical/near-site splice variants reach SpliceAI >= 0.5 and concordance all_predict_disruption — CFTR c.1585-1G>A 0.97, c.1393-1G>A 1.00, BRCA1 c.594-2A>C 0.83, c.5074+1G>A 0.74, c.212+3A>G 0.63 (5 of 5)
- PASS: Likely-benign controls are BP4 with none_predict_disruption — 5 of 6 (CFTR c.3718-15A>T, c.4242+9T>C, c.4137-18A>G; BRCA1 c.5332+84G>A, c.594-4A>T)
- FAIL: No likely-benign control reaches all_predict_disruption — CFTR c.2909-10T>G: SpliceAI 0.57 (DS_AL), Pangolin -0.41, MMSplice -1.85 - a tool limitation, but the Skill calls concordance "the strongest computational evidence" without a warning about concordant false positives
- PASS: The deep-intronic CFTR pseudoexon is flagged for follow-up rather than called benign — spliceai_label inconclusive, concordance discordant (n_scored 2), consistent with "discordance flags need RNA validation"
**Scores:** 34 / 49 / 83. Assertions 4/5.

### Input 9 — Variant B (new tools): NEW: cross-tool checks on the new panel: SpliceVault vs SpliceAI, CI-SpliceAI, CADD API, tissue script, extended window for the CFTR pseudoexon
**Ran:** t7d_sv.sh, t7c_cispliceai.sh (cis-vcf -a grch38 -d 500 --all), CADD curl on 7 variants (out/t9_cadd.log), t2_tissue.sh, t7_check.py.

**Result:** SpliceVault's stored SpliceAI delta equals my SpliceAI run for all 5 catalogued variants (0.97, 1.00, 0.83, 0.74, 0.63); the CFTR pseudoexon is not catalogued (the Skill says so). CADD PHRED: canonical 27.8-34, pseudoexon 10.6, BRCA1 c.212+3A>G 13.7 (low despite SpliceAI 0.63), c.2909-10T>G 20.6. CI-SpliceAI: canonical 0.76-1.00, pseudoexon 0.01 ("cross-check, not a rescue" is accurate). The Skill's deep-intronic recipe (-D 500 on every candidate < 0.20) leaves the CFTR case at 0.16.

- PASS: SpliceVault stored delta equals the independent SpliceAI delta for every catalogued new variant — 5/5
- PASS: CI-SpliceAI command from the Skill runs on GRCh38 and its INFO tag parses by replacing SpliceAI= — 12 records, CISpliceAI=ALLELE|ENSG...|DS...
- PASS: CADD-Splice block gives usable PHRED for GRCh38 SNVs on the new panel — 7/7 records
- PASS: Skill statements about CADD/CI-SpliceAI are consistent with the new data (CADD is one number, CI-SpliceAI not a rescue) — CADD 13.7 for c.212+3A>G vs SpliceAI 0.63; CI 0.01 for the pseudoexon
- FAIL: The Skill's extended-window workflow recovers the CFTR 3849+10kbC>T pseudoexon that the Skill itself lists as a disease example — SpliceAI max 0.16 at -D 50, 500 and 2000; only Pangolin (+0.33) and the discordance label flag it; the Skill's Failure Mode "Fix: re-run with -D 500" does not say it may not help
**Scores:** 34 / 49 / 83. Assertions 4/5.

### Key printed evidence
```
SpliceAI D50 GRCh37 (delta_max): PLCXD1 G>A 1.00 | GTdel 1.00 | DMD c.9563+1G>A 0.99 | c.31+1G>A 0.95 | OTC c.386+5G>A 0.94 | GLA c.370-1G>A 1.00 | GLA c.639+919G>A 0.30 | 3 benign 0.00
Pangolin GRCh38 (GENCODE v45): mask False / canonical-DB mask True / all-transcript-DB mask True
  GLA c.639+919G>A gain +0.23@-3 / +0.23 / 0.00     OTC c.386+5G>A loss -0.72@-5 / 0.00 / 0.00     TP53 c.673-2A>G loss -0.90@-2 in all four
  auditor-picked DMD non-canonical-only sites (loss): -0.39 / 0.00 / -0.39 and -0.60 / 0.00 / -0.60 (other three sites -0.04 to -0.13)
New panel (SpliceAI D50 | Pangolin | MMSplice | CI-SpliceAI):
  CFTR c.1585-1G>A  0.97 | -0.86 | -1.83 | 1.00     BRCA1 c.594-2A>C  0.83 | -0.81 | -2.86 | 0.95     BRCA1 c.5074+1G>A  0.74 | -0.70 | -2.70 | 0.95
  CFTR 3849+10kb C>T (pseudoexon)  0.16 (D500 0.16, D2000 0.16) | +0.33 | no row | 0.01  -> discordant / inconclusive
  CFTR c.2909-10T>G (ClinVar likely benign)  0.57 | -0.41 | -1.85 | 0.31  -> concordant false positive
shipped example, TP53 VCF: c.673-2A>G 1.0 PP3_supporting_prec0.8 | P72R 0.05 BP4 (wide 0.05) | usage-guide A>G record: WARNING SpliceAI: no score, not_scored
shipped example, edge VCF + one <DEL>: subprocess.CalledProcessError, no output
```

## Research Veto (Category 3): PASS
- scientific_integrity: **PASS** — No fabricated numbers: every quoted score, mask-table cell, SpliceVault event and PHRED value reproduced (or was checked against the source); citations sampled against Crossref (SpliceVault Nat Genet 55:324, SpliceAI Cell 176:535, Pangolin Genome Biol 23, SpliceTransformer Nat Commun 15); the 884 MB SpliceVault size equals Content-Length; the BPHunter 404 claim is true (page redirects to a GitHub 404).
- practice_boundaries: **PASS** — Scope paragraph and usage-guide sentence state research-use decision support and forbid patient write-ups; SpliceAI alone is not PVS1; concordance labels renamed (no "pathogenic" anywhere in output labels); ASO section relabelled a checklist. The pre-fix caveats are closed.
- methodological_ground: **PASS** — Thresholds are ClinGen SVI 2023 at supporting weight, boundaries inclusive, unscored records never read as benign; the -D mechanism and Pangolin mask trade-off are now measured and correct. Residual: no warning that concordant false positives exist (CFTR c.2909-10T>G) - P2.
- code_usability: **PASS** — RE-JUDGED FROM FAIL. All 12 fenced blocks of SKILL.md parse (ast / bash -n, out/m4_blocks.log) and were run: install lines resolve (dry-run) and the Pangolin clone installs pangolin + create_db.py; SpliceAI, Pangolin (create_db.py + both masks), tissue script, SpliceVault, MMSplice, SpliceTransformer, CI-SpliceAI, CADD, -D 500 and the parser/concordance blocks ran and printed asserted values; the two pre-fix P0 recipes (Pangolin DB/dependencies, concordance snippet) now run on real GRCh37 and GRCh38 output; the shipped example runs end to end on three VCFs. Only a batch containing a symbolic <DEL> aborts the example (documented crash, P1, not a usability failure of the primary path).

## Step 8 — Final
Static 83 x 0.4 = 33.2; Execution 84.4 x 0.6 = 50.6; **final 84, Limited Release, deployable, veto_override false.** No open P0. Open P1: 2, P2: 4.

### Key strengths
- Both pre-fix P0 recipes now run on real data: the Pangolin install/DB/command sequence (create_db.py on a GENCODE GTF, -m False) and build_concordance() on real SpliceAI/Pangolin/MMSplice output (GRCh37 and GRCh38, 10-11 rows for 10-11 variants, a wrong-REF record kept as insufficient_tools).
- The Pangolin -m True mask table is measured and reproduces independently (GLA pseudoexon +0.23 -> 0.00 with an all-transcript DB, OTC -0.72 -> 0.00, the two informative auditor-picked non-canonical-only DMD sites erased); the Skill recommends -m False.
- Un-scored records are handled honestly everywhere: "." -> NaN -> not_scored, unscored_report, outer joins; the boundary classifier is inclusive; "pathogenic" is gone from output labels; research-use scope is explicit.
- Every check I could make against outside sources held: SpliceVault Top-4 events, 884 MB file size, CADD record, citations, BPHunter 404, tool versions on PyPI.

### Recommendations
[P1] Shipped example aborts on one symbolic ALT (inputs [4]) — spliceai_clingen_classify.py runs SpliceAI with check=True; one <DEL> record makes SpliceAI exit 1 and the example prints a CalledProcessError traceback with no output for the other records. Fix: Filter ALT alleles starting with "<" (and "*") into an unscored list before the run, or run per-record on failure, and report them in the not_scored warnings.
[P1] Extended-window recipe does not recover the named CFTR example (inputs [8, 9]) — CFTR c.3849+10kbC>T (c.3717+12191C>T), listed in the Skill as a disease example, scores SpliceAI 0.16 at -D 50, 500 and 2000; only Pangolin (+0.33) and the discordance label flag it, CI-SpliceAI gives 0.01, MMSplice returns no row. Fix: Add the CFTR measurement next to the GLA one and say that a deep-intronic candidate at 0.10-0.20 with a Pangolin gain is a "discordant, needs RNA" case, not a rescue by -D.
[P2] Gene column shows overlapping gene (inputs [5]) — per_variant() keeps the highest-delta gene, so OTC c.386+5G>A appears as RP5-972B16.2 and GLA benign variants as RPL36A-HNRNPH2. Fix: Prefer the gene named in the VCF/MANE transcript or add a second column listing all annotated genes.
[P2] Concordance labels can overstate weak agreement (inputs [5, 8]) — GLA c.639+919G>A is all_predict_disruption from two tools at 0.30/0.23, and CFTR c.2909-10T>G (ClinVar likely benign) is concordant across three tools plus CI-SpliceAI. Fix: Show the margin above threshold or n_scored next to the label in the table, and add one sentence that concordant calls still need ClinVar/gnomAD and RNA evidence.
[P2] Mask table omits a further erased loss; keys carry full REF sequences (inputs [2, 4]) — With the canonical DB, -m True also erased the PLCXD1 donor loss (-0.80 -> 0.00); a 150-bp deletion prints its whole REF in keys and warnings. Fix: Add the PLCXD1 row (or "any site absent from the canonical DB"); truncate long alleles in printed keys.
[P2] Installs only partly verifiable; heavy SKILL.md (inputs [2, 6]) — torch via pip pulls the CUDA wheel by default, SpliceTransformer needs a Drive download and pyensembl indexing that I could not repeat from scratch; SKILL.md is still 443 lines with no references/ layer. Fix: Add a CPU-torch note and pin the GitHub commits; move ASO, branchpoint and HGVS material to references/.

## What I could not verify
- BPHunter, LaBranchoR, BPP, SVM-BPfinder were not run (BPHunter's standalone page redirects to a GitHub 404, checked); the Skill says "none was run here".
- Installs of SpliceTransformer (Google Drive weights, pyensembl index) and CI-SpliceAI were verified by `pip --dry-run` only; the tools were run in the fixer's staged envs (`as-spvp`, `as-spvp-gpu`, `as-cispliceai`) and repo. SpliceTransformer's staged FASTA has no chr7, so the new panel was not scored by it.
- The MMSplice `setuptools<81` / `cyvcf2` note is from TOOLS.md traps 21/23; `as-mmsplice` already has a working cyvcf2 0.34.0, so the failing state was not reproduced. The dry-run plans cyvcf2 0.30.15, which matches the Skill's warning.
- Input 7 is scored from the Skill text applied to real numbers (no agent transcript), as in the pre-fix audit.
- `TOOLS.md` does not yet list `as-spvp`, `as-cispliceai`, `as-spvp-gpu` in detail (the orchestrator records them). I changed no package versions; the only install was a throwaway venv in WSL `/tmp`. Large scratch (chr7 FASTA, GENCODE subsets) is in `F:\OpenScience\as-spvp-reaudit-scratch\`; the gffutils DBs and GTF copies were deleted from `run/out/`.

## Files
- Report: `F:\OpenScience\audits\bio-splice-variant-prediction\eval_report_bio-splice-variant-prediction_result.json` (built and schema-asserted by `run\build_report.py`; this viewer by `run\build_viewer.py`)
- Scripts: `run\*.py`, `run\*.sh` (`w.sh`/`wenv.sh` drive WSL); logs `run\out\*.log`; Skill copy audited `run\skill\` (commit 40aa467b3e6ca58f2aeb4cbf30a8cc2b81cf7197).
