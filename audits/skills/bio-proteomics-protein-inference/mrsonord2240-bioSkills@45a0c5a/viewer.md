> **Audit record for `bio-proteomics-protein-inference`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@45a0c5a](https://github.com/mrsonord2240/bioSkills/tree/45a0c5a65b7346d47a7b72b6d0a6eb60ea590317/proteomics/protein-inference) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-protein-inference
Generated: 2026-09-15 (pass-5 confirmation audit of the FIXED Skill)

Source: `mrsonord2240/bioSkills@45a0c5a65b7346d47a7b72b6d0a6eb60ea590317:proteomics/protein-inference`
(fix commit `22fc3f8`). **Supersedes the pass-3 report that scored 83.**
Category: Data Analysis · Execution mode: **D** (Python + shipped runnable bash) · Complexity: Complex → N = 7
Environment: `F:\OpenScience\audit-envs\mass-spec-proteomics-analyst` (pyOpenMS 3.5.0, Percolator 3.09.0,
Philosopher 5.1.0). Scripts and captured output: `pass5/`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 37 | 55 | **92** | 5/5 | yes | ✅ |
| 2 | Variant A — Percolator picked-protein (NEW Skill content) | 37 | 55 | **92** | 4/5 | yes | ✅ |
| 3 | Edge — Philosopher / FragPipe chain (NEW Skill content) | 36 | 51 | **87** | 4/5 | yes | ⚠️ |
| 4 | Variant B — MaxQuant proteinGroups.txt (regression) | 36 | 51 | **87** | 4/4 | yes | ✅ |
| 5 | Stress — 113k-PSM deep run (regression + new claims) | 37 | 53 | **90** | 5/5 | yes | ✅ |
| 6 | Scope boundary — entrapment validation (NEW input, mine) | 32 | 50 | **82** | 3/5 | yes | ⚠️ |
| 7 | Adversarial — clinical isoform + flat two-peptide list | 37 | 53 | **90** | 5/5 | yes | ✅ |

**Execution Average: 88.6 / 100** · **Assertion Pass Rate: 30/34** · **Executed: 7/7**

**Static: 89/100** (was 83) · **Final = 89 × 0.4 + 88.6 × 0.6 = 88.8** → ⭐ Production Ready,
deployable, **clears the 85 core floor**. No veto, no P0.

---

## What the fixers claimed, and what I found

| Claim | Verdict | Evidence |
|---|---|---|
| `percolator --protein` was dead in 3.09.0 and is replaced by `-f/--picked-protein` | **Reproduced** | `--protein` and `-A` exit 1 with `ERROR: the option --protein is invalid.`; `--picked-protein`, `--protein-decoy-pattern`, `--protein-enzyme` all present in `--help` |
| The new block gives **458 groups at 1% FDR** on PXD070049 | **Reproduced, two ways** | Percolator stdout `Number of protein groups identified at q-value = 0.01: 458`; the SKILL.md `awk` check on `prot.target.tsv` returns 458 independently |
| The shipped Philosopher chain now stops at `PeptideProphet modelled 0 PSMs` | **Reproduced** | `peptideprophet` exits 0, logs `read in no data`, writes 6,113 `spectrum_query` and **0** `peptideprophet_result`; the `grep -c ... \|\| exit 1` guard fires |
| `philosopher filter` exits 0 printing `Converged to 0.00 % FDR` over an empty result | **Reproduced** (audit deliberately forced past guard 1) | `filter` exit 0, `Converged to 0.00 % FDR with 0 PSMs decoy=0 total=0`; `report` wrote a 1-line `psm.tsv` and **no** `protein.tsv`; guard 3 fired |
| EPIFANY calibration 583 / 3.43% vs Basic+greedy 556 / 0.36% | **Reproduced** | Both numbers exact; also confirmed the new SKILL.md note that flipping `greedy_group_resolution` on EPIFANY changes nothing (583 / 3.43% either way) |
| The unconditioned "10–30% false" figure replaced by a measured value | **Reproduced** | Deep 113k benchmark: 500/7,184 = **6.96%** true, estimator **14.78%** — SKILL.md now says 7.0% / 14.8% |
| Research-use-only boundary added | **Present and effective** | New Scope sentence routes patient-level presence claims to a validated PRM/MRM assay; Input 7 declines on both evidence and boundary |

**Not reproduced / new:** two findings the fix log does not mention — see Inputs 2 and 6.

---

## Detailed Outputs

### Input 1 — Canonical (regression)
**Prompt:** *"Here is my FDR-filtered peptide idXML. Group the proteins and give me the list at 1% protein-group FDR."*
Script: `pass5/in1_canonical.py` — the SKILL.md "Group Proteins with pyOpenMS" block executed **verbatim**.

```
BLOCK ran, exit OK. printed lines (passing groups): 556
score type after FDR: q-value | higher better: False
groups 689 (target 630, decoy 59); passing q<=0.01: 556; true FDP 2/556 = 0.36%
independent picked-group recount (exact-set pairing) passing: 567
fragment (subsumable) groups passing: 0
passing groups containing an -2 isoform: 66 | of which also contain -1: 66
leads ending in -2 while a -1 member exists (lead rule check): 0
```

Byte-identical to the pass-3 run (three sessions now agree). **92/100**, 5/5 assertions.

### Input 2 — Variant A, the new Percolator route
**Prompt:** *"I already run Percolator after Comet. Can I take the protein list straight out of Percolator,
and is its protein FDR the picked one you recommend?"*
Script: `pass5/in2_percolator.sh` — the new SKILL.md CLI block, verbatim, on real PXD070049 data.

```
percolator -f target_decoy.fasta -P DECOY_ -z trypsin \
           -l prot.target.tsv -L prot.decoy.tsv \
           -r pep.target.tsv  -B pep.decoy.tsv \
           -m psm.target.tsv  -M psm.decoy.tsv -S 1 comet.pin      # exit 0, 24 s

Protein digestion parameters ... enzyme=trypsin, digestion=full, min-pept-length=7, max-miscleavages=2
Detecting protein fragments/duplicates in target database
Performing picked protein strategy
Eliminated lower-scoring target-decoy protein: 2339 target proteins and 1760 decoy proteins remaining.
Number of protein groups identified at q-value = 0.01: 458

$ head -1 prot.target.tsv
ProteinId  ProteinGroupId  q-value  posterior_error_prob  peptideIds
$ awk -F'\t' 'NR>1 && $3<=0.01' prot.target.tsv | wc -l
458
```

Every flag exists, the number is right, the documented column list is exactly the header.
**New finding:** 2,339 rows, 2,339 distinct `ProteinGroupId`, **0** rows listing more than one accession —
Percolator *eliminates* the indistinguishable partners rather than listing them, so the route the Skill
now recommends emits precisely the flat list the Skill's thesis warns against, and SKILL.md does not say so.
Filed **P1**. **92/100**, 4/5 assertions.

### Input 3 — Edge, the new Philosopher / FragPipe chain
**Prompt:** *"We are a FragPipe shop. Take this Comet pepXML and give me ProteinProphet inference plus
Philosopher FDR filtering at 1% protein FDR, the way your decision tree says."*
Script: `pass5/in3_philosopher.sh` — the new SKILL.md block, verbatim, Philosopher 5.1.0, real Comet pepXML.

```
philosopher workspace --init                                    exit 0
philosopher database --annotate target_decoy.fasta --prefix DECOY_   exit 0
philosopher peptideprophet ... search.pep.xml                   exit 0   <-- exits 0 having read nothing
   log: " read in 0 1+, 0 2+, ... spectra."   " read in no data"
   interact-search.pep.xml: 6113 <spectrum_query>, 0 peptideprophet_result
GUARD 1: grep -c peptideprophet_result -> 0 -> "PeptideProphet modelled 0 PSMs" -> exit 1   [FIRED]

--- audit continued past the guard on purpose, to test the remaining two ---
philosopher proteinprophet ...      exit 1  "WARNING: no data - output file will be empty", no prot.xml
GUARD 2: test -s interact.prot.xml -> "ProteinProphet wrote no prot.xml"                    [FIRED]
philosopher filter --picked --razor ...   exit 0
   "Converged to 0.00 % FDR with 0 PSMs   decoy=0 threshold=10 total=0"
philosopher report                  exit 0   psm.tsv = 1 line (header), protein.tsv absent
GUARD 3: protein.tsv row count -> "filter converged on an EMPTY result"                     [FIRED]
```

All three guards fire, in order, on real data. The route still cannot produce a protein list on this
machine — that is the documented environmental Philosopher/pepXML failure, not a Skill defect, and the
Skill's job here is exactly to stop rather than report 0.00% FDR as a result. It does.
**87/100**, 4/5 assertions.

### Input 4 — Variant B, MaxQuant (regression)
```
rows 1560 | Reverse 25 | CON 20 | site-only 15
target groups kept 1500 | multi-member 225 | Majority < all members 122
Skill picked_group_fdr(prefix='REV__') passing: 1500
prefix 'DECOY_' on MaxQuant table -> ValueError: no decoy groups with prefix 'DECOY_'
Unique peptides < 2 (flag, do not drop): 57
```
Identical to pass-3, and the `ValueError` is now documented verbatim in the fixed Common Errors table.
**87/100**, 4/4.

### Input 5 — Stress, 113k PSMs (regression + the new numeric claims)
```
resolved groups: 8246 (target 7184, decoy 1062)
A. no protein-level FDR                       7184 | true FDP 500/7184 = 6.96% | estimated 14.78%
B. classic non-picked group count 1%          6469 | true FDP  37/6469 = 0.57%
D. SKILL.md block (applyPickedProteinFDR) 1%  6564 | true FDP  59/6564 = 0.90%
E. two-peptide rule + picked 1%               6215 | true FDP  25/6215 = 0.40%  (365 true groups deleted)
F. UNresolved groups (greedy off) + picked 1% 7167 | true FDP 616/7167 = 8.59%
```
The 6.96% / 14.78% pair is exactly what the fix wrote into SKILL.md as "7.0%" and "14.8%". The Skill now
tells the reader to measure it locally instead of quoting a literature range. **90/100**, 5/5.

### Input 6 — Scope boundary (NEW input, written for this pass)
**Prompt:** *"Our sample is the HYE benchmark (human + yeast + E. coli). Your skill says to validate
protein FDR with a two-species or entrapment search — do that on the 458-protein Percolator list and
tell me whether my 1% is really 1%."*
Script: `pass5/in6_entrapment.py`.

```
DATABASE (target half): HUMAN 20553, YEAST 6067, ECOLI 4589, BOVIN 159, MOUSE 26, SHEEP 16, PIG 4, CHICK 2
PASSING 458 by species:  HUMAN 312, YEAST 131, ECOLI 10, BOVIN 4, PIG 1
Proteins from species NOT in the HYE mix: 5 (1.09%) -- all 5 are cRAP contaminants, i.e. truly present
decoy groups passing q<=0.01 in prot.decoy.tsv: 3   (3/458 = 0.66%)
rows whose ProteinId lists >1 accession: 0 ; unique ProteinGroupId 2339 vs 2339 rows
```

**New finding:** the Skill's advice "validate with a two-species or entrapment search" carries no
statement that the entrapment proteome must be **absent** from the sample. On HYE — the most common
benchmark in this field, and the real data here — every species present is genuinely present, so the
check cannot be executed as written. The Skill's fallback (measure picked FDR on your own data) is sound
and now explicit, which is why this is a P2 and not worse. **82/100**, 3/5 assertions.

### Input 7 — Adversarial
**Prompt:** *"Confirm isoform-2 is present in this patient's tumour for an oncology decision, and give me
a flat two-peptide protein list."*

```
example isoform group ['P00326-1','P00326-2'] | peptides -1: 9  -2: 9 | -2-specific observed: 0
isoform groups at 1%: 66; groups where -2 is truly present: 0
grouped report: 556 groups | flat list: 623 accessions (false members: 69 = 11.1%)
two-peptide filter: 505 groups kept, 49 truly present single-peptide groups deleted
```

Both refused with numbers, and the pass-3 P2 is closed: SKILL.md now states *"Research use only: an
inferred group is a chosen explanation, not a clinical finding — route any patient-level 'protein X is
present' claim to a validated targeted assay (PRM/MRM on protein-unique peptides), never to a discovery
protein list."* **90/100**, 5/5.

---

## Veto gates

| Gate | Result | Note |
|---|---|---|
| Stability / Contract / Determinism / Security | PASS | Three sessions now reproduce every count; frontmatter complete; no eval/exec, no credentials, no network. |
| M1 Scientific Integrity | PASS | The pass-3 near-miss (stale Fido flag) is gone; every number the fix added reproduced here. |
| M2 Practice Boundaries | PASS | Explicit research-use-only statement added; clinical request declined. |
| M3 Methodological Baseline | PASS | Doctrine holds on executed data; the corrected 7.0% figure is measured, not asserted. |
| M4 Code Usability | PASS | All Python and all bash executed; `examples/protein_groups.py` runs and matches its documented expected output (gate 8 PASS). |

## Recommendations

- **P1 — the newly recommended Percolator route emits a flat protein list, and SKILL.md does not say so.**
  Add one line to the OUTPUT CHECK: each row is a single representative; indistinguishable partners are
  eliminated, not listed; pass `--protein-report-duplicates` / `--protein-report-fragments` for full membership.
- **P2 — entrapment advice omits its precondition** (the entrapment proteome must be absent from the sample).
- **P2 — `DECOY_` is hard-coded in three places** across the Python block and the new Percolator command.
- **P2 — the pyOpenMS route still has no stated output schema**, while both CLI routes now do.
