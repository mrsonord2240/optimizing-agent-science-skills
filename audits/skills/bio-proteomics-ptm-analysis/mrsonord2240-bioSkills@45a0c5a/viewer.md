> **Audit record for `bio-proteomics-ptm-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@45a0c5a](https://github.com/mrsonord2240/bioSkills/tree/45a0c5a65b7346d47a7b72b6d0a6eb60ea590317/proteomics/ptm-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-ptm-analysis
Generated: 2026-09-15 (pass-5 confirmation audit of the FIXED Skill)

Source: `mrsonord2240/bioSkills@45a0c5a65b7346d47a7b72b6d0a6eb60ea590317:proteomics/ptm-analysis`
(fix commit `b5355db`). **Supersedes the pass-3 report that scored 85.**
Category: Data Analysis · Execution mode: A · Complexity: Moderate → N = 6 (5 required; 6 run so both
new routes get their own input). Scripts and output: `pass5/`. Every R and Python fence is pulled
programmatically from the fork's SKILL.md and eval'd verbatim — nothing is retyped.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical — label-free MSstatsPTM protein adjustment | 36 | 54 | **90** | 4/4 | yes | ✅ |
| 2 | Variant A — no global proteome, `use_unmod` proxy | 34 | 52 | **86** | 4/4 | yes | ✅ |
| 3 | Adversarial — unadjusted double filter + mislabelled FLR | 36 | 52 | **88** | 4/4 | yes | ✅ |
| 4 | Edge — KSEA over 7 degenerate PX shapes | 37 | 53 | **90** | 5/5 | yes | ✅ |
| 5 | Variant B (**NEW route, the P1 fix**) — TMT/isobaric | 35 | 52 | **87** | 4/5 | yes | ⚠️ |
| 6 | Stress (**NEW**) — TMT misconfiguration, both directions | 33 | 50 | **83** | 4/5 | yes | ⚠️ |

**Execution Average: 87.3 / 100** · **Assertion Pass Rate: 25/27** · **Executed: 6/6**

**Static: 85/100** (was 84) · **Final = 85 × 0.4 + 87.3 × 0.6 = 86.4** → ⭐ Production Ready,
deployable, **clears its 75 supporting floor with room** (and the 85 core floor too). No veto, no P0.

---

## What the fixers claimed, and what I found

| Claim | Verdict | Evidence |
|---|---|---|
| New TMT route verified against planted truth on a synthetic TMT10 pair | **Reproduced in substance** on an independently built TMT10 set | protein-driven **5/8 → 1/8** (claim 6/8 → 1/8); site_regulated **8/8** (exact); masked **0/4 → 3/4** (claim 1/4 → 3/4); sign agreement **11/11**; ρ 0.766 (claim 0.691). 35 ADJUSTED rows vs their 39 — my reshape is not byte-identical to theirs |
| The pass-2 KSEA correctness fix is **unchanged to the last digit** | **Reproduced to 10 s.f.** | BASO `-2.5514840725` FDR `0.008044892010`; PRO `3.3688957209` FDR `0.001132049635`; RANDOM `-0.6524594878` FDR `0.257052399630` |
| The guards were added **around** that fix, not inside it | **Confirmed structurally and numerically** | `ks <- adjusted[is.finite(adjusted$log2FC), ]` present verbatim; all four guards sit outside it; D1/D2/D3/D5 unchanged |
| Label-free regression unchanged (36 ADJUSTED rows, 10 regulated) | **Reproduced cell for cell** | 36 / 10 / masked 2, null 3, site_regulated 5 / 1 non-finite |
| Forward-direction TMT error message | **Reproduced verbatim** | `Extra columns included in the annotation file that are not required … Run, Raw.file, Fraction, TechRepMixture, Channel, Condition, Mixture, BioReplicate` |
| Reverse-direction TMT error message | **Could NOT reproduce** | Three configurations gave three other loud errors, never `A non-empty vector of column names for 'by' is required` |

**New defect found in the added content:** the documented `Channel` index is off by one — filed **P1**.

---

## Detailed Outputs

### Input 1 — Canonical, label-free protein-adjusted site testing (regression)
```
BLOCK ran. names(input): PTM PROTEIN | names(result): PTM.Model PROTEIN.Model ADJUSTED.Model Model.Details
Label: Treatment vs Control | ADJUSTED site rows: 36 | regulated (TREAT lfc=1, BH<0.05): 10

-- PTM.Model (unadjusted) adj.p<0.05 --      -- ADJUSTED.Model adj.p<0.05 --
          class  n tested called                      class  n tested called
         masked  4      3      1                     masked  4      3      3
           null 20     14      4                       null 20     14      4
 protein_driven  8      7      7             protein_driven  8      7      1
 site_regulated  8      8      8             site_regulated  8      8      8

sign agreement on site_regulated: 5 / 5    non-finite log2FC rows: 1 (-Inf)
post-hoc double filter would call: 16 vs TREAT 10
```
Identical to pass-3. Inserting the TMT section changed nothing here. **90/100**.

### Input 2 — Variant A, no global proteome (`use_unmod` proxy)
```
use_unmod = TRUE | evidence rows kept: 507 | PTM rows: 288 | ADJUSTED.Model NULL: FALSE
protein_driven 1/8 called | site_regulated 8/8 | masked 2/4   (vs 3/4 with a real global proteome)
```
The proxy route is measurably weaker, which is exactly why the Skill insists on the label
"proxy-adjusted". **86/100**.

### Input 3 — Adversarial
```
requested list (unadjusted, double filter): 18 sites  -> null 3, protein_driven 6, site_regulated 7
Skill route (ADJUSTED + TREAT):             10 sites  -> masked 2, null 3, site_regulated 5
model-based expected FLR mean(1 - Localization prob) over class I: 0.0382 (NOT an empirical FLR)
```
A third of the requested list is protein abundance or noise, and the FLR substitution is refused with
the correct distinction. **88/100**.

### Input 4 — Edge, KSEA over seven degenerate PX shapes
```
correctness filter line present verbatim: TRUE
guards present: nrow(ks)==0 TRUE | rep(NULL,nrow(ks)) TRUE | nrow(PX)==0 TRUE | coverage TRUE

D1 baseline     sites in PX: 31 | covered by the prior: 14 | kinases 3 | NaN z: 0
                SYN_BASO_KINASE   4  -2.5514840725  0.008044892010
                SYN_RANDOM_KINASE 5  -0.6524594878  0.257052399630
                SYN_PRO_KINASE    5   3.3688957209  0.001132049635
D2 +Inf and -Inf present            -> computes, 0 NaN
D3 NA adjusted p-values             -> computes, identical to D1
D4 prior matching a single site     -> STOP: "The kinase-substrate prior covers 0 of 31 sites …"
D5 zero within-kinase variance      -> computes, 0 NaN
D6 every site non-finite            -> STOP: "No site has a finite log2FC … detected-in-one-condition"
D7 NEW (no gene symbols at all)     -> STOP: "PX is empty after dropping sites with no gene symbol …"
```
D1's numbers match the fix log's claim digit for digit, which is the strongest available evidence that
the guards did not perturb the pass-2 correctness fix. **90/100**.

### Input 5 — NEW route: TMT / isobaric (the pass-3 P1)
**Prompt:** *"Protein-adjust my TMT phosphoproteomics — enriched and global runs are labelled plexes
with a pooled reference channel."*
Data: a synthetic TMT10 evidence pair built by `pass5/make_tmt.py` from this audit's own labelled
label-free set (8 biological channels + 2 pooled `Norm`), so `truth_sites.csv` still applies.

```
TMT block found: 2293 chars | labeling_type: TRUE | data.type TMT: TRUE

(a) channel naming — does SKILL.md's "channel.1 … channel.N" hold?
    annotation_ptm_tmt_ch1.csv (channel.1 … channel.10) -> ERROR: ** Please check the annotation
        file. The channel name must be matched with that in input data.
    annotation_ptm_tmt.csv     (channel.0 … channel.9)  -> COMPLETED

(b) the block, run verbatim
status: COMPLETED
names(input): PTM PROTEIN      models: PTM.Model PROTEIN.Model ADJUSTED.Model Model.Details
ADJUSTED site rows: 35 | Label(s): Treatment vs Control

protein_driven  n= 8 | called PTM 5/8 -> ADJ 1/8
site_regulated  n= 8 | called PTM 8/8 -> ADJ 8/8
masked          n= 4 | called PTM 0/4 -> ADJ 3/4
null            n=20 | called PTM 4/20 -> ADJ 4/20
sign agreement on regulated+masked: 11/11      Spearman rho vs true occupancy log2FC: 0.766
```

The route works and the adjustment is right. But MaxQuant writes TMT10 reporter columns **0-indexed**
(`Reporter intensity corrected 0` … `9`), so the annotation the Skill tells you to build is rejected
at the first call by an error that never mentions the index. Filed **P1**. **87/100**, 4/5.

### Input 6 — NEW: TMT misconfiguration, both directions
```
label-free ANNOTATION with labeling_type = 'TMT':
  "Extra columns included in the annotation file that are not required ... Please only include the
   following columns in the annotation file: Run, Raw.file, Fraction, TechRepMixture, Channel,
   Condition, Mixture, BioReplicate"                                  <- SKILL.md verbatim ✔

TMT annotation on labeling_type = 'LF':
  "Extra columns ... Run, Raw.file, Condition, BioReplicate, IsotopeLabelType"
LF annotation + TMT evidence on labeling_type = 'LF':
  "** Please check annotation. Each MS run (Raw.file) can't have multiple conditions or BioReplicates."
```
The Skill's doctrine — *fails loudly in both directions, and neither message says "wrong labeling
type"* — is confirmed three times over. Its quoted reverse-direction message
(`A non-empty vector of column names for 'by' is required`) is not what this data produces. **83/100**, 4/5.

---

## Veto gates

| Gate | Result | Note |
|---|---|---|
| Stability / Contract / Determinism / Security | PASS | KSEA D1 reproduced across sessions to 10 s.f.; no eval/exec of user strings, no network, no credentials. |
| M1 Scientific Integrity | PASS | The central claim (pass-2 fix untouched) verified numerically. The two tool-behaviour statements that did not hold are recorded as findings, not fabrication. |
| M2 Practice Boundaries | PASS | Input 3's push for an unadjusted "regulated phosphorylation" call and a mislabelled FLR was refused with numbers. |
| M3 Methodological Baseline | PASS | Protein adjustment verified against planted truth in **both** routes; the two TMT traps added are correct and concern the adjustment, not just the quant. |
| M4 Code Usability | PASS | 3/3 R fences parse and were executed; 3/3 Python fences and `examples/phospho_analysis.py` compile. |

## Recommendations

- **P1 — the new TMT section states the wrong `Channel` index.** MaxQuant is 0-indexed; the Skill's
  `channel.1 … channel.N` annotation is rejected outright. Tell the reader to read the reporter-column
  suffixes off their own evidence header.
- **P2 — one of the two new TMT Common Errors messages could not be reproduced**; generalise the row
  to "several loud errors are possible; none names the labeling type".
- **P2 — modification names are hard-coded to phospho, now in three code paths** (the TMT block adds
  a third).
- **P2 — PTM-SEA and empirical FLR are still prescribed but unimplemented**, though ssGSEA2.0 and
  LuciPHOr2 are both installed here.
- **P2 — 391 → 478 lines with no `references/` split** on an always-loaded Skill.
