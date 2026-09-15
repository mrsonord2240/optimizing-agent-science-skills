> **Audit record for `bio-proteomics-protein-inference`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/proteomics/protein-inference) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-11 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer: bio-proteomics-protein-inference
Generated: 2026-09-11 · Auditor: sub-auditor for `mass-spec-proteomics-analyst` (round 2) · skill-auditor@1.0
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:proteomics/protein-inference` (read-only; clone verified clean with `git status`)
Role in candidate: supporting (protein grouping + protein-level FDR)

**Result: 67/100, Beta Only (not deployable). Static 73, execution average 62.2, no veto. All 5 inputs executed.**

All data is SYNTHETIC:
- `data/make_idxml.py` (seeded) writes two Comet/Percolator-style idXMLs with PEP scores. Each is filtered at 1% PSM FDR with the decoy PSMs that pass kept, and comes with per-protein ground truth.
  - "std": 1,960 target proteins, 6,150 PSMs, 828 proteins.
  - "deep": 15,655 target proteins, 113,547 PSMs, 9,993 proteins.
- Built-in structures:
  - indistinguishable isoform pairs (X-1 present, X-2 absent, its isoform-specific peptide rarely observed);
  - paralogs with 3 shared peptides;
  - subset fragments (absent, peptides a strict subset of the parent);
  - reversed decoys that mirror the shared-peptide topology.
- `data/proteinGroups.txt` is a copy of the shared SYNTHETIC MaxQuant table.

Tools: nothing was pip-installed. The pyOpenMS 3.1.0 wheel was downloaded to the scratchpad (not installed) only to read its stubs; see `runs/pyopenms31_stub_check.*`.

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical: pyOpenMS grouping + picked FDR | 25 | 33 | 58 | 2/5 | yes | ❌ PARTIAL |
| 2 | Variant A: MaxQuant proteinGroups interpretation | 30 | 47 | 77 | 4/5 | yes | ✅ |
| 3 | Edge: indistinguishable isoforms, tiny counts | 25 | 31 | 56 | 1/4 | yes | ⚠️ |
| 4 | Variant B: EPIFANY / Bayesian | 25 | 35 | 60 | 3/5 | yes | ❌ PARTIAL |
| 5 | Stress: deep data, naive vs picked, two-peptide rule | 26 | 34 | 60 | 2/5 | yes | ⚠️ |

**Execution average: 62.2 / 100 · Assertion pass rate: 12/24 (50%) · Executed: 5/5**

---

## Step 1: Skill Veto

| Dimension | Result | Reason |
|---|---|---|
| T1 Stability | PASS | No crash loops or dependency conflicts. The example exits 0. The pyOpenMS blocks fail deterministically on API names and types, with no instability (scored under correctness). |
| T2 Contract | PASS | Frontmatter has `name` and `description` (plus `tool_type`, `primary_tool`). |
| T3 Determinism | PASS | No randomness in the Skill's code. The same input gives the same output. The parsimony tie-break is input-order dependent, but that is deterministic (Input 3). |
| T4 Security | PASS | No eval/exec of user strings, no network calls, no shell injection. |

## Step 2: Static evaluation (73/100)

| # | Criterion | Score | Note |
|---|---|---|---|
| 1.1 | Completeness | 3/4 | Code for pyOpenMS grouping, EPIFANY and picked FDR. ProteinProphet/Philosopher are named with no command, and the MaxQuant path has no code. |
| 1.2 | Correctness | 2/4 | Several errors:<br>• `EpifanyAlgorithm` does not exist in 3.1.0 or 3.5.0.<br>• `BasicProteinInferenceAlgorithm` is called "parsimony" but is score aggregation.<br>• The naive protein-FDR bias is stated in the wrong direction.<br>• Picked-group FDR is credited to The & Kall 2016.<br>• The example drops indistinguishable proteins.<br>• The comment on `accessions[0]` is wrong. |
| 1.3 | Appropriateness | 3/4 | Right tools and concepts, but it hand-rolls picked FDR that pyOpenMS already provides (`FalseDiscoveryRate.applyPickedProteinFDR`). |
| 2.1 | Fault tolerance | 2/4 | A generic "introspect on AttributeError" block only. No guards for score orientation, decoy prefix, bytes accessions, missing decoys or tiny counts. |
| 2.2 | Error reporting | 2/4 | The Common Errors table is useful, but its suggested `help(pyopenms.EpifanyAlgorithm)` itself raises AttributeError. |
| 2.3 | Recoverability | 3/4 | Stateless; re-runs are identical. No structured codes (Category 3 override). |
| 3.1 | Token cost | 3/4 | 228 lines / 19 KB, all in SKILL.md, no filler. |
| 3.2 | Execution efficiency | 3/4 | Linear. Re-implements picked FDR instead of calling the built-in. |
| 4.1 | Learnability | 2/4 | Following "Basic ... for parsimony grouping" literally gives an 8.6% FDP list with no sign that anything is wrong (Inputs 1, 5). |
| 4.2 | Consistency | 3/4 | The SKILL.md `picked_group_fdr` returns filtered targets while the example's returns every row. `DECOY_` is the default prefix with no mention of `REV__`. |
| 4.3 | Feedback design | 3/4 | "Report groups with a leading protein" is clear, but no output table is specified. |
| 4.4 | Error prevention | 3/4 | Strong failure modes: two-peptide rule, razor quant, proteoform overreach, database-relative uniqueness. Misses score orientation and keeping decoys through the PSM filter. |
| 5.1 | Discoverability | 4/4 | Natural triggers ("which proteins are present", "protein groups", "protein-level FDR"). |
| 5.2 | Forgiveness | 2/4 | Category 3 override: input requirements are only partly stated (PEPs for EPIFANY). |
| 6.1 | Credential safety | 4/4 | No credentials involved. |
| 6.2 | Input validation | 2/4 | None, as in the whole template. |
| 6.3 | Data safety | 3/4 | Local processing, nothing retained. |
| 7.1 | Modularity | 3/4 | Clean sections plus one example. |
| 7.2 | Modifiability | 3/4 | Blocks are independent. |
| 7.3 | Testability | 3/4 | The example is self-contained but has no expected output. All its decoys lose the pick, so the q-value path is never exercised. |
| 8.1 | Trigger precision | 4/4 | Explicit routing to peptide-identification, quantification and top-down. |
| 8.2 | Progressive disclosure | 3/4 | No references/; acceptable at 228 lines. |
| 8.3 | Composability | 3/4 | Related skills exist. No output contract for quantification. |
| 8.4 | Idempotency | 4/4 | Deterministic. |
| 8.5 | Escape hatches | 3/4 | The isoform stop and the tiny-count caution are in prose, not in code. |

Category totals:

| Category | Score |
|---|---|
| Functional suitability | 8/12 |
| Reliability | 7/12 |
| Performance and context | 6/8 |
| Agent usability | 11/16 |
| Human usability | 6/8 |
| Security | 9/12 |
| Maintainability | 9/12 |
| Agent-specific | 17/20 |
| **Total** | **73/100** |

## Gate 8: shipped files are present (PASS)

SKILL.md and usage-guide.md point at no `references/` or `scripts/` files, which confirms the lead's finding. The files present are:
- `SKILL.md` (228 lines)
- `usage-guide.md` (68 lines)
- `examples/protein_groups.py` (104 lines; SKILL.md refers to it as "the reference example")

All four Related Skills exist in the clone:
- `proteomics/peptide-identification`
- `proteomics/quantification`
- `proteomics/data-import`
- `database-access/uniprot-access`

## Gate 7: research scope

No individual-level diagnosis or triage anywhere. PASS.

## Step 3: Classification

- **Category:** 3 Data Analysis.
- **Execution mode:** A (instructions plus code patterns, no scripts/).
- **Complexity: Moderate, N = 5.** The Skill has three task types: pyOpenMS grouping, probabilistic inference, and protein-level FDR. It branches in its decision tree (MaxQuant, FragPipe, deep data, isoform stop) and ships 3 files. That is broader than Simple, but it has no multi-file reference corpus and is not Complex.

## Example smoke test

Ran `examples/protein_groups.py` (copied to `runs/example_protein_groups.py`) → exit 0. Output in `runs/example_smoke.out`:

```
Parsimony kept 5 proteins out of 6 candidates
Dropped (subsumable): ['P_C']
Protein groups passing 1% picked-group FDR: 3
P_A 4 2 False 0.0 | P_B 2 1 False 0.0 | P_D 1 1 False 0.0
```

- All three decoys lose their pick, so every q-value is 0 and the demo never exercises decoy counting.
- Line 100 is a bare `report` expression, a notebook leftover and a no-op.

## pyOpenMS 3.5.0 API probe

From `runs/api_probe*.out` and `runs/pyopenms31_stub_check.out`:

- `EpifanyAlgorithm` is absent in 3.5.0, and in the 3.1.0 wheel (0 occurrences in stubs and binaries). `BayesianProteinInferenceAlgorithm` is present in both.
- `BasicProteinInferenceAlgorithm` has `annotate_indistinguishable_groups`, and it defaults to `true`.
  - Its docstring says "simple protein inference by aggregation of peptide scores". It is not parsimony.
  - `greedy_group_resolution` (default `false`) is the razor-style resolution step.
- `run(pep_ids, prot_ids)` exists.
- `ProteinGroup` exposes `.accessions` (as bytes) and `.probability`.
- `IdXMLFile.load` needs a `PeptideIdentificationList` in 3.5.0. In 3.1.0 it took `List[PeptideIdentification]`, so the Skill's `[]` is a 3.5 regression.
- pyOpenMS already provides picked protein/group FDR: `FalseDiscoveryRate.applyPickedProteinFDR(prot_id, String, decoy_prefix, groups_too)`.

---

## Detailed outputs

### Input 1: Canonical

**Prompt:** "I ran Comet + Percolator and filtered to 1% PSM FDR, keeping the decoy hits. The file is `peptides_1pct_fdr.idXML` (PEP scores). Please group the peptides into proteins with pyOpenMS, give each group a leading protein, and tell me how many protein groups pass 1% picked-group FDR."

**Code:**
- `runs/in1_skill_asis.py`: the SKILL.md block verbatim.
- `runs/in1_adapted.py`: the same block with `PeptideIdentificationList`, then SKILL.md `picked_group_fdr` verbatim, then truth checks.
- `runs/in1_bytes_check.py`

**What ran:**

1. Verbatim block:
   ```
   IdXMLFile().load('peptides_1pct_fdr.idXML', protein_ids, peptide_ids)
   Exception: can not handle type of ('peptides_1pct_fdr.idXML', [], [])
   ```
2. Passing raw `group.accessions` into `picked_group_fdr` → `TypeError: a bytes-like object is required, not 'str'` (accessions are bytes).
3. Adapted run (`in1_adapted.out`):
   ```
   indistinguishable groups: 749   target 690, decoy 59
   groups passing 1% picked-group FDR (Skill function): 619
   true FDP among passing groups: 53/619 = 8.562%
   isoform-family groups: 79; of which 2-member (X-1+X-2 indistinguishable): 73   leading = P00326-1 (alphabetical)
   subsumable fragments observed: 32; reported as their OWN group: 32; fragment groups passing 1%: 27
   absent paralog-B proteins observed via shared peptides: 25; passing 1% as groups: 20
   pyOpenMS applyPickedProteinFDR(groups_too=True): 619 (true FDP 53/619)   <- Skill function matches built-in
   greedy_group_resolution=true: groups 689, passing 567, true FDP 5/567, fragment groups passing 0
   ```

The picked FDR function is correct; the grouping step the Skill calls "parsimony" is not. Setting `greedy_group_resolution` brings FDP to 0.9%.

**Scores:** Basic 25/40 | Specialized 33/60 | Total 58

Layer 1:

| Criterion | Score | Reason |
|---|---|---|
| Functional correctness | 4 | Runs only after a fix; the list claimed at 1% is 8.6% false. |
| Reliability & clarity | 6 | |
| Efficiency | 7 | |
| Scope & safety | 8 | |

Layer 2:

| Criterion | Score | Reason |
|---|---|---|
| Methodological validity | 9/20 | Subsumable and shared-only proteins are counted as groups, so the 1% claim is invalid. |
| Code executability | 6/15 | Fails as written: list type, then bytes. |
| Data QC | 6/10 | Decoys kept, but no guidance on orientation or contaminants. |
| Reproducibility | 7/10 | |
| Security | 5/5 | |

**Assertions (2/5):**
- [PASS] Scope: stays within grouping and protein-group FDR, with quant routed to quantification.
- [FAIL] The pyOpenMS block runs as written on 3.5.0: load raises `can not handle type`.
- [PASS] Indistinguishable isoform pairs are grouped with a leading accession: 73 pairs.
- [FAIL] Groups at 1% have true FDP near 1%: 8.6%.
- [FAIL] Subsumable proteins are not reported as confident groups: 27/32 pass.

### Input 2: Variant A

**Prompt:** "Attached is our MaxQuant proteinGroups.txt (8 runs). Can you explain the group structure (which accession is the leading protein, what razor vs unique means here), tell me how many groups are real at 1% FDR, and whether we should filter to at least 2 unique peptides like my PI wants? I'd like a clean group table."

**Code:** `runs/in2_maxquant.py`. The Skill gives only the decision-tree row "parse groups as-is; quantify on UNIQUE peptides", so this code is agent-written.

**Output** (`in2_maxquant.out`):
```
rows 1560 | bookkeeping: REV 25, CON 20, site-only 15
target groups after removing REV/CON/site: 1500 | protein-group Q-value<=0.01: 1500
multi-member groups: 225 | groups containing an isoform accession (-N): 225
groups with razor-assigned peptides (Razor+unique > Unique): 219
single-peptide groups (Peptides==1): 52 | <2 unique peptides: 57
Skill picked_group_fdr, default prefix 'DECOY_': 1525 pass, of which REV__ rows counted as TARGETS: 25
Skill picked_group_fdr, prefix 'REV__': 1500 pass
```

The answer given to the researcher:
- The leading protein is the first Protein ID. Group membership is kept.
- Razor peptides are credited to the group with most evidence, and matter for quantification (routed there).
- The table reports 1,500 groups at the protein-group level, per MaxQuant.
- Don't apply the two-peptide filter: it would drop 57 groups. Flag them instead.

The Skill says nothing on:
- MaxQuant column semantics. "Unique peptides" there means unique to the group, which conflicts with the Skill's "maps to exactly one protein".
- `Majority protein IDs`.
- The `REV__` prefix.

**Scores:** Basic 30/40 (FC 7, R&C 7, Eff 8, S&S 8) | Specialized 47/60 (Method 15, Code 12, QC 7, Repro 8, Security 5) | Total 77

The REV/CON/site-only filtering came from general knowledge, not from the Skill (QC 7).

**Assertions (4/5):**
- [PASS] Leading protein plus membership.
- [PASS] No two-peptide rule; singles flagged.
- [PASS] Scope: razor-vs-unique routed to quantification.
- [FAIL] The Skill supplies the MaxQuant prefix and column semantics: `DECOY_` default counts 25 `REV__` as targets.
- [PASS] Safety: no individual or clinical interpretation.

### Input 3: Edge

**Prompt:** "Single IP-MS pulldown, 10 peptides total. Two TPM1 isoforms (P09493 and P09493-2) match every TPM1 peptide I saw, and a TrEMBL fragment matches two of them. There are also two decoy hits. Please use your example grouping script to report groups and protein FDR — and can I say isoform 2 is present?"

**Code:** `runs/in3_edge.py`. It execs the shipped example's functions with `SAMPLE_MAP` replaced (as the example's docstring instructs), then runs the same evidence through pyOpenMS Basic.

**Output** (`in3_edge.out`):
```
--- canonical listed first ---
Dropped (subsumable): ['DECOY_P09493-2', 'P09493-2', 'Q5VU61']
Protein groups passing 1% picked-group FDR: 3     (P09493, P67936, P07951 all q = 0.0)
--- same evidence, isoform accession listed first ---
Dropped (subsumable): ['DECOY_P09493-2', 'P09493', 'Q5VU61']
leading_protein P09493-2  [P09493-2] ... q = 0.0
--- pyOpenMS BasicProteinInferenceAlgorithm ---
['P09493', 'P09493-2'] 0.999 | ['Q5VU61'] 0.998 | ['P07951'] 0.994 | ...
```

This confirms the lead's first point. The indistinguishable isoform is reported as subsumable and never grouped, which contradicts Insight #1. Which isoform is kept depends on input order, so the code produces the "isoform X present" overreach that the Skill warns against. The pyOpenMS path groups the isoforms correctly but keeps the subset fragment as its own group.

The Skill's prose leads to the right answer: "No — P09493 and P09493-2 are indistinguishable; you need an isoform-unique peptide or top-down data." Protein FDR from 3 targets and 1-2 decoys is not meaningful (decision-tree row). The code emits no such warning.

**Scores:** Basic 25/40 (FC 5, R&C 5, Eff 7, S&S 8) | Specialized 31/60 (Method 9, Code 6: runs, but has a critical logic bug; QC 5, Repro 6: order-dependent; Security 5) | Total 56

**Assertions (1/4):**
- [FAIL] Indistinguishable proteins form one group.
- [FAIL] The leading protein is independent of input order.
- [PASS] Scope: the isoform claim is declined and routed.
- [FAIL] Tiny-count FDR is flagged by the code path.

### Input 4: Variant B

**Prompt:** "Instead of parsimony, run EPIFANY on my Percolator-scored idXML (`peptides_with_pep.idXML`) and give me group posteriors plus the groups at 1% group FDR."

**Code:**
- `runs/in4_skill_asis.py`: verbatim.
- `runs/in4_adapted.py`: class name and list type fixed; the Skill's `inferPosteriorProbabilities(protein_ids, peptide_ids, False)` call is unchanged.
- `runs/in4_greedy.py`: the same with `True`.

**What ran:**

1. Verbatim block:
   ```
   algo_cls = getattr(pyopenms, 'EpifanyAlgorithm')
   AttributeError: module 'pyopenms' has no attribute 'EpifanyAlgorithm'
   ```
   `help(pyopenms.EpifanyAlgorithm)`, as the Skill suggests, raises the same error. The name is also absent from the 3.1.0 wheel.
2. Adapted run (`in4_adapted.out`):
   ```
   Best params found at a=0.25, b=0.01, g=0.7 ; Annotated 79 indist. protein groups.
   EPIFANY ran in 4.6s; protein score type: Posterior Probability
   as Skill prints: b'P00559-1' 0.997...        <- bytes accession
   groups 749 (decoy 59); passing 1% picked-group FDR: 586; true FDP 20/586 = 3.41%
   fragment groups passing: 3 | absent paralog groups passing: 10
   model-based (posterior) group FDR 1%: 587 groups; true FDP 21/587 = 3.58%
   ```
   `greedy_group_resolution=True` gave identical numbers.

**Scores:** Basic 25/40 (FC 5, R&C 5, Eff 7, S&S 8) | Specialized 35/60 (Method 12: the right model, better than Basic but still 3.4x nominal; Code 5: fails as written; QC 6; Repro 7; Security 5) | Total 60

**Assertions (3/5):**
- [FAIL] The EPIFANY block runs as written.
- [PASS] It runs after the introspection the Skill directs.
- [PASS] It states that PEP input is required.
- [FAIL] 1% group FDR is calibrated: 3.4%.
- [PASS] Scope: stays in inference and FDR.

### Input 5: Stress

**Prompt:** "Deep single-shot run: 113k PSMs at 1% PSM FDR, roughly 10k proteins in the idXML. My collaborator says 1% PSM FDR is already enough and we should just add the two-peptide rule. Compare naive protein-group FDR with picked-group FDR, show what the two-peptide rule does, and tell me what we should report."

**Code:** `runs/in5_stress.py`. It uses the Skill's `picked_group_fdr` verbatim and Basic inference with the list-type fix. Truth comes from `truth_deep.csv`.

**Output** (`in5_stress.out`):
```
groups: 8913 (target 7841, decoy 1072)
A. no protein-level FDR ("1% PSM FDR is enough")   7841 | true FDP 1122/7841 = 14.31% | estimated 13.67%
B. naive group-level target-decoy, 1%              7039 | true FDP  566/7039 =  8.04%
C. Skill picked_group_fdr, 1%                      7167 | true FDP  616/7167 =  8.59%
D. two-peptide rule only                           6633 | true FDP  367/6633 =  5.53% | estimated 0.89%
F. greedy_group_resolution=true + picked 1%        6561 | true FDP   58/6561 =  0.88%
F2. greedy groups + NAIVE group FDR 1%             6469 | true FDP   37/6469 =  0.57%
H. greedy groups + two-peptide rule + picked 1%    6215 | true FDP   25/6215 =  0.40%
   (greedy) true single-peptide groups passing picked 1% that the two-peptide rule deletes: 365
pairing: decoy groups 1072; paired to a same-membership target group: 580; unpaired: 492
   e.g. ['DECOY_P03605A','DECOY_P03605B'] vs target ['P03605A'];  ['DECOY_P07991-2'] vs ['P07991-1','P07991-2']
random subset of 10 groups: 4 decoys, 6 pass at 1% (no warning); 30 groups: 1 decoy, 24 pass
```

What this shows about each claim:

- **"1% PSM is not 1% protein" (Insight #2, first half): confirmed.** With no protein-level FDR, 14.3% of groups are false.
- **The mechanism in the naive-FDR failure mode is reversed.** Non-picked protein-level target-decoy was conservative on properly grouped data: 0.57% true at nominal 1%, with 92 fewer groups than picked. That matches Savitski 2015: the classic approach over-estimates FDR, and picking recovers groups. The Skill's "reported 1%, actual 10-30%" describes case A (no protein-level estimate at all), not the naive decoy count.
- **Picked FDR under the Skill's default grouping is 8.6% false.** The inflation comes from grouping, as in Input 1.
- **Pairing (lead 3):** exact-frozenset matching leaves 46% of decoy groups unpaired. Whenever decoy-group membership differs from its target's (e.g. a random hit on a reversed shared peptide), no pick happens and both groups are counted naively.
- **Small counts:** results are returned with no guard.
- **Two-peptide rule: mixed.** It deleted 365 true single-peptide groups (Skill confirmed), but lowered true FDP (0.88% to 0.40%) rather than raising it. Gupta & Pevzner's direction did not reproduce under a strict 1% PSM pre-filter.

**What to report:** picked-group FDR at 1% on greedy/parsimony-resolved groups (F), and no two-peptide rule. The Skill's own default (C) would have reported 8.6% false groups.

**Scores:** Basic 26/40 (FC 5, R&C 6, Eff 7, S&S 8) | Specialized 34/60 (Method 10, Code 7: the pick function ran verbatim at scale, the loader needed the fix; QC 5, Repro 7, Security 5) | Total 60

**Assertions (2/5):**
- [PASS] Shows PSM 1% is not protein 1%.
- [FAIL] The naive-FDR mechanism as stated holds.
- [FAIL] Default grouping + picked controls FDR at 1% (8.6%).
- [PASS] The two-peptide rule discards real proteins (365).
- [FAIL] Every decoy group is paired (492/1,072 unpaired).

---

## Citation check (lead 4)

| Reference | Verdict | Evidence |
|---|---|---|
| Gupta & Pevzner 2009, JPR 8(9):4173-4181 | Correct, and the claim matches the paper's abstract ("reduces the number of protein identifications in the target database more significantly than in the decoy database and results in increased false discovery rates") | [PubMed 19627159](https://pubmed.ncbi.nlm.nih.gov/19627159/). The FDR direction is condition-dependent (Input 5). |
| Savitski et al. 2015, MCP 14(9):2394-2404 | Correct citation; the Skill's description of what it fixes is wrong in direction | The classic approach over-estimates protein FDR because decoys accumulate ([PMC9718969 summary](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9718969/)). |
| The, Tasnim & Kall 2016, Proteomics 16(18):2461-2469 | Exists, but misattributed | It is about competing null hypotheses. It mentions the picked target-decoy list from Savitski but does not define picked-group FDR ([PMC5096025](https://pmc.ncbi.nlm.nih.gov/articles/PMC5096025)). Picked-group FDR and the finding that "Occam's razor is anticonservative on large data" are from The, Samaras, Kuster & Wilhelm 2022, MCP 21(12):100437 ([PubMed 36328188](https://pubmed.ncbi.nlm.nih.gov/36328188/)). |
| Nesvizhskii 2003; Pfeuffer 2020 | Correct bibliographic data | |

## Research Veto (Category 3)

| Dimension | Result | Detail |
|---|---|---|
| M1 Scientific integrity | PASS | No fabricated identifiers; one misattribution (scored under correctness). |
| M2 Practice boundaries | PASS | Research-only; no individual-level claims. |
| M3 Methodological ground | PASS (with note) | The principles are sound. The mislabelled default tool and the reversed naive-bias statement are implementation and explanation defects, scored in Layer 2 and as P1s. |
| M4 Code usability | PASS (with note) | Positive evidence: the example ran, and `picked_group_fdr` ran verbatim on 749 and 8,913 groups. The pyOpenMS blocks fail on API names and types, which the Skill's Version Compatibility section tells the agent to introspect and fix. After one-token fixes all 5 inputs ran. |

## Final arithmetic

```
Static            73      x 0.4 = 29.2
Execution avg     (58 + 77 + 56 + 60 + 60) / 5 = 311 / 5 = 62.2   x 0.6 = 37.32 -> 37.3
Final             29.2 + 37.3 = 66.5 -> 67
Grade             60-74 -> Beta Only (⚠️); deployable = false; veto_override = false
Floors            Limited-Release floors not met (exec 62.2 < 75, L1 avg 26.2 < 28, L2 avg 36.0 < 42, assertions 50% < 80%);
                  the score band is already Beta Only, so there is no further tier change.
```

As a supporting Skill (threshold at least 75) it does **not** pass. There is no open P0.

## Recommendations

- **[P1] Basic inference is mislabelled as parsimony (Inputs 1, 3, 5).**
  - Problem: subsumable and shared-only proteins become groups, giving 8.6% true FDP at 1%.
  - Fix: call it aggregation and set `greedy_group_resolution='true'` (0.9% FDP here), or add a real Occam step.
- **[P1] `EpifanyAlgorithm` does not exist, and plain lists fail in `IdXMLFile.load` on 3.5 (Inputs 1, 4, 5).**
  - Fix: use `BayesianProteinInferenceAlgorithm`, `PeptideIdentificationList()`, and decode bytes accessions. Update "tested with 3.1+".
- **[P1] The example drops indistinguishable proteins as "subsumable" and the lead depends on input order (Input 3).**
  - Fix: collapse identical-evidence proteins before the greedy loop, add an indistinguishable pair to `SAMPLE_MAP` with the expected output, and delete the bare `report` line.
- **[P1] Naive protein-FDR bias is reversed and picked-group FDR is misattributed (Input 5).**
  - Fix: separate "no protein-level FDR" (anticonservative) from "classic protein target-decoy" (conservative on large data), and cite The et al. 2022 MCP.
- **[P2] `picked_group_fdr` pairing, prefix and tiny counts (Inputs 2, 3, 5).**
  - Problem: exact-set pairing left 46% of decoy groups unpaired; the `DECOY_` default misreads `REV__`; no small-count guard.
  - Fix: point to `FalseDiscoveryRate.applyPickedProteinFDR(pid, String('DECOY_'), True, True)` or the kusterlab `picked_group_fdr`.
- **[P2] Input contract (Inputs 1, 2, 4).**
  - Fix: keep decoy PSMs through the upstream filter; state the score orientation; add a MaxQuant column glossary. Choose the leading protein explicitly: `accessions[0]` is alphabetical in pyOpenMS.
- **[P2] The two-peptide mechanism is stated as universal (Input 5).**
  - Fix: keep the advice, but word the FDR effect as dependent on the PSM threshold.

## Files

- `data/`: `make_idxml.py` (generator), `peptides_1pct_fdr_{std,deep}.idXML`, `psms_1pct_{std,deep}.csv`, `truth_{std,deep}.csv`, `proteinGroups.txt`. All SYNTHETIC.
- `runs/`: every script above with its captured `.out`, the `api_probe*` scripts, and `pyopenms31_stub_check.*`.
