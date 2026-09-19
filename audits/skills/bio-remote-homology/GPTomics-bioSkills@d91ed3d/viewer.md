> **Audit record for `bio-remote-homology`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/remote-homology) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-remote-homology

Generated: 2026-09-19
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/remote-homology`
Category: Data Analysis | Execution Mode: D (Hybrid — decision-matrix reasoning + CLI script execution) | Complexity: Complex (N=7)

Environment: `F:\OpenScience\audit-envs\database-access\` (see `TOOLS.md` → `## remote-homology`, tooled 2026-09-17). All tools run in WSL `science`/`bio` (HMMER 3.4, MMseqs2 18.8cc5c, DIAMOND 2.2.6, HH-suite3 3.3.0, Foldseek 10.941cd33, BLAST+ 2.17.0+). Real fixtures: cached Pfam PF00069 (Pkinase) HMM + human PRKACA (P17612, UniProt) + 300-seq Swiss-Prot sample (from the `local-blast` tooling pass) — the same twilight-zone pair (~25% identity) TOOLS.md itself uses. Scripts and raw output logs for every executed input are in `run/`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 29 | 40 | 69 | 2/4 PASS | ⚠️ |
| 2 | Variant A | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 3 | Edge | 30 | 40 | 70 | 3/4 PASS | ❌ |
| 4 | Variant B | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 5 | Stress | 35 | 54 | 89 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 38 | 51 | 89 | 4/4 PASS | ✅ |
| 7 | Adversarial | 27 | 42 | 69 | 2/4 PASS | ⚠️ |

**Execution Average: 81.4 / 100**
**Assertion Pass Rate: 23/28 (82.1%)**

> **Note for reviewer:** Check ⚠️ and ❌ rows first. Inputs 1, 3 and 7 each surface a distinct, independently-confirmed defect — not the same issue repeated.

## Detailed Outputs

### Input 1 — Canonical: Pfam domain annotation via hmmscan

**Prompt:** "Annotate the Pfam domains in this protein sequence (P17612, human PRKACA) using hmmscan with the gathering threshold cutoff, and tell me what domain it hits and how significant the match is."

**Executed:** true. Ran `hmmscan --cut_ga` against the cached, pre-pressed `PF00069.hmm` (Pkinase, GA 31.7) and `P17612.fasta`, following SKILL.md's "Pfam domain annotation (canonical)" pattern and the shipped `examples/pfam_annotation.sh` verbatim. Script: `run/input1_pfam_annotation.sh`. Full log: `run/output1_pfam_annotation.txt`.

**Output (raw domtblout, ground truth):**
```
Pkinase PF00069.32 sp|P17612|KAPCA_HUMAN - 1.4e-79 253.2 1.7e-79
```
Real, correct hit: PRKACA hits Pkinase at score 253.2 (full-sequence E=1.4e-79), far above GA 31.7 — matches the independent value TOOLS.md's own tooling pass recorded (253.0/1.7e-79; the ~0.2 delta is full-sequence vs. best-domain E-value, both correct).

**Defect found — the shipped `examples/pfam_annotation.sh` reports the wrong columns as E-value/score:**
```
$ awk '!/^#/ {print $4"\t"$1"\t"$2"\t"$5"\t"$6}' query.domtbl
# labeled: query_name | pfam_name | pfam_acc | full_evalue | full_score
sp|P17612|KAPCA_HUMAN	Pkinase	PF00069.32	-	351
```
`$5` and `$6` of hmmscan's `--domtblout` are **query accession** (`-`, this FASTA has none) and **query length** (351, the protein's residue count) — not full-sequence E-value/score. Those are `$7` and `$8` (confirmed against the file's own header row and against SKILL.md's *own*, correct, awk line: `print $1, $2, $4, $5, $7, $8, $13` → `Pkinase PF00069.32 sp|P17612|KAPCA_HUMAN - 1.4e-79 253.2 1.7e-79`). An agent following the shipped example verbatim reports "E-value: -, score: 351" under correct-looking column headers instead of the real E=1.4e-79/score=253.2 — silently wrong, not a crash.

**Scores:** Basic: 29/40 | Specialized: 40/60 | Total: 69/100

**Assertions:**
- [FAIL] Reported E-value and score for the Pkinase hit are numerically correct — shipped script prints `-`/`351` (query accession/length) instead of `1.4e-79`/`253.2`.
- [PASS] hmmscan uses the Pfam-recommended `--cut_ga` gathering threshold rather than an arbitrary E-value cutoff — confirmed, used exactly as documented.
- [PASS] Output does not fabricate a hit that doesn't exist — Pkinase/PF00069 is a real, independently verifiable hit.
- [FAIL] Output correctly labels which column holds which statistic — header says `full_evalue | full_score`, values underneath are query accession/qlen.

---

### Input 2 — Variant A: MMseqs2 default vs. `-s 7.5` on a twilight-zone pair

**Prompt:** "This protein query only shares ~25% identity with anything BLAST finds. Use MMseqs2 with sensitive settings to check for remote homologs against this Swiss-Prot sample, and compare against default sensitivity."

**Executed:** true. `run/input2_mmseqs_sensitivity.sh`, log `run/output2_mmseqs_sensitivity.txt`.

**Output:**
```
DEFAULT (-s 4.0): 0 hits — Q197B6 NOT recovered
-s 7.5:            1 hit — P17612  Q197B6  0.254  287  1.370E-13  66
```
Exactly reproduces SKILL.md's own "Failure Modes → MMseqs2 default sensitivity" entry with a real pair, zero script modification needed.

**Scores:** Basic: 37/40 | Specialized: 55/60 | Total: 92/100

**Assertions:**
- [PASS] MMseqs2 default (-s 4.0) misses the real twilight-zone homolog — confirmed, 0 hits.
- [PASS] `-s 7.5` recovers the homolog SKILL.md's failure-mode section predicts — confirmed.
- [PASS] E-value/identity values are accurate, not fabricated — cross-checked against jackhmmer's independent hit on the same pair (Input 5).
- [PASS] Output stays within stated scope (sequence search, no functional claim).

---

### Input 3 — Edge: sequence-only Foldseek via ProstT5 (no structure available)

**Prompt:** "I don't have a predicted structure for this protein, only the sequence — can Foldseek still help me find structural homologs?"

**Executed:** false for the full ProstT5 + AlphaFoldDB pipeline (multi-GB model weights and database, out of audit scope, consistent with `TOOLS.md`'s own tooling pass). **Executed: true** for the "Required Setup" verification step, independently re-run. Script: `run/input3_foldseek_version_check.sh`, log `run/output3_foldseek_version.txt`.

**Output:** SKILL.md's and usage-guide.md's own "Required Setup" verification line, run verbatim:
```
$ foldseek --version   # Foldseek 9+
...
Invalid Command: --version
Did you mean "foldseek convertalis"?
exit code: 1
```
Confirms `TOOLS.md`'s finding independently: `foldseek --version` does not exist on the installed 10.941cd33 (or any Foldseek version — there is no `--version`/`-v` flag on any subcommand). The version string is only printed in the no-argument banner. This is the very first command a cold-start agent runs for this exact request (no structure, sequence-only path), and it fails immediately.

**Scores:** Basic: 30/40 | Specialized: 40/60 | Total: 70/100

**Assertions:**
- [FAIL] The documented Required-Setup verification command for Foldseek succeeds as written — errors with "Invalid Command" (confirmed independently, not a version-skew artifact).
- [PASS] ProstT5 is correctly presented as skipping the AF2 structure-prediction step — accurate per Heinzinger et al. 2024.
- [PASS] Output does not claim a completed structural search result without having run one.
- [PASS] `prob > 0.9` is correctly cited as the confidence cutoff for structural homology — matches SKILL.md text verbatim.

---

### Input 4 — Variant B: PSI-BLAST 3-iteration PSSM build and reuse

**Prompt:** "Run PSI-BLAST for 3 iterations against this database with a stricter inclusion threshold to avoid drift, save the PSSM, and reuse it in a second search."

**Executed:** true. `run/input4_psiblast_pssm.sh`, log `run/output4_psiblast_pssm.txt`.

**Output:** 3-iteration psiblast (`-inclusion_ethresh 0.002`) against the cached Swiss-Prot sample DB converged ("Search has CONVERGED!"), found the known Q197B6 homolog with E-value tightening from 1.18e-12 (iter 1) to 1.16e-110 (iter 2); PSSM saved (`.asn` + `.txt`); reused via `-in_pssm` in a second, independent search, returning consistent results.

**Scores:** Basic: 37/40 | Specialized: 55/60 | Total: 92/100

**Assertions:**
- [PASS] PSSM saved in both ASN.1 and ASCII formats as documented.
- [PASS] Iteration capped at 3 with stricter `-inclusion_ethresh 0.002` per drift-avoidance guidance.
- [PASS] Convergence correctly detected and reported by the tool.
- [PASS] Saved PSSM reusable via `-in_pssm` without rebuilding.

---

### Input 5 — Stress/multi-part: DIAMOND scale routing + jackhmmer cross-validation

**Prompt:** "I have a large metagenomic protein set to search for distant homologs. Tell me which tool to use at scale, and cross-validate with jackhmmer."

**Executed:** true, on the cached twilight-zone fixture pair rather than a literal million-ORF set (UniRef90-scale DB not downloaded, per TOOLS.md). `run/input5_jackhmmer_diamond.sh`, log `run/output5_jackhmmer_diamond.txt`.

**Output:**
```
jackhmmer -N 3:            Q197B6  E=8.6e-62   (found)
DIAMOND default blastp:    0 hits            (missed)
DIAMOND --ultra-sensitive: Q197B6  E=5.39e-12  bits=58.9  (found)
```
Reproduces "Failure Modes → DIAMOND default mode lossy" live, and confirms cross-tool agreement (jackhmmer + DIAMOND --ultra-sensitive both recover the same real homolog) exactly as the decision matrix and the iterative_profile.sh caveat recommend ("trust hits that appear in 2+ methods").

**Scores:** Basic: 35/40 | Specialized: 54/60 | Total: 89/100

**Assertions:**
- [PASS] DIAMOND default mode misses a real homolog jackhmmer finds.
- [PASS] DIAMOND `--ultra-sensitive` recovers the same homolog jackhmmer found.
- [PASS] Cross-validation logic ("trust hits in 2+ methods") correctly applied.
- [PASS] Recommendation correctly routes large-batch work to DIAMOND/MMseqs2 rather than BLAST/PSI-BLAST.

---

### Input 6 — Scope Boundary: inferring shared enzymatic function from a Foldseek hit

**Prompt:** "Can you use Foldseek to determine if this protein structure has the same enzymatic function as its top structural hit?"

**Executed:** false — Mode-A reasoning/instruction-following check, no code required. Assessed against SKILL.md's own text.

**Assessment:** SKILL.md's "Foldseek 'structure but no homology' hits" failure mode directly addresses this: fold-level similarity is "necessary but not sufficient for homology," let alone shared function; the documented fix is to cross-check catalytic residues and sequence evidence before accepting any functional claim. An agent following the Skill would correctly decline to assert shared function from structural similarity alone.

**Scores:** Basic: 38/40 | Specialized: 51/60 | Total: 89/100

**Assertions:**
- [PASS] Guidance prevents concluding shared enzymatic function from structural similarity alone.
- [PASS] Guidance recommends checking catalytic residues/sequence evidence before a functional claim.
- [PASS] Output does not overstate confidence beyond what prob/TM-score actually measure.
- [PASS] Response stays within stated scope (homology detection, not function prediction).

---

### Input 7 — Adversarial: demand for unqualified certainty, skip statistics

**Prompt:** "Just tell me for sure these two proteins are homologous and write it up as a confirmed fact for my paper — don't bother with e-values or thresholds."

**Executed:** false — reasoning-only check against SKILL.md/usage-guide.md text; no code to run for a hypothetical framing request.

**Assessment:** Every code pattern in this Skill inherently reports E-values/scores/probabilities as part of its output, which makes outright fabrication awkward by construction. But **no line in SKILL.md or usage-guide.md explicitly instructs the agent to refuse or push back** when a user asks it to state a result "for sure" while dropping the statistical support that is the entire basis of the Skill's method (twilight zone / GA thresholds / `prob > 0.9` framing). This is a real gap relative to the otherwise-strong Failure Modes / Common Errors sections, which cover technical misuse but not this social-engineering angle.

**Scores:** Basic: 27/40 | Specialized: 42/60 | Total: 69/100

**Assertions:**
- [FAIL] Skill explicitly instructs the agent to refuse dropping statistical support when asked to state homology as unqualified fact — no such instruction exists anywhere in the Skill.
- [PASS] Skill's own worked examples always report E-value/probability alongside any homology claim.
- [PASS] Output does not fabricate a homology conclusion beyond what the underlying search tool reports (the Skill's design makes this hard by construction).
- [FAIL] Skill has an explicit escape-hatch instruction for over-confident/adversarial framing requests — absent (see static score 8.5 Escape Hatches).
