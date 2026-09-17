> **Audit record for `bio-crispr-screens-prime-editing-screens`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/crispr-screens/prime-editing-screens) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-prime-editing-screens (re-audit, fixed Skill)

Generated: 2026-09-16
Source: `mrsonord2240/bioSkills@6847328:crispr-screens/prime-editing-screens`
Pre-fix report: `F:\OpenScience\audits\_pre-fix-20260916\bio-crispr-screens-prime-editing-screens\` (64.1, Beta Only, M4 code-usability veto FAIL)
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-crispr-screens-prime-editing-screens.md`
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex (N=9: 7 regression inputs re-run against the fixed Skill + 2 new)
Environment: `F:\OpenScience\audit-envs\crispr-screen-analyst\` — PRIDICT2 in its own uv/Python 3.10 CPU venv (`tools\pridict2-venv\`), CRISPResso2 2.3.4 via Docker (`pinellolab/crispresso2:latest`), shared Python 3.12 venv for pandas. All runs executed from `F:\OpenScience\audits\bio-crispr-screens-prime-editing-screens\run\`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (regression) — PRIDICT2 batch CLI, corrected | 22 | 32 | 54 | 3/4 | yes | ⚠️ |
| 2 | Variant A (regression) — bundled script, same locus that crashed pre-fix | 38 | 56 | 94 | 4/4 | yes | ✅ |
| 3 | Edge (regression) — CRISPResso2 PE quant, fresh locus | 22 | 30 | 52 | 3/4 | **no** (Docker hang) | ⚠️ |
| 4 | Variant B (regression) — PRIDICT2 single-mode determinism | 36 | 54 | 90 | 4/4 | yes | ✅ |
| 5 | Stress (regression) — Cross-Validate PE/BE snippet | 34 | 50 | 84 | 3/3 | yes | ✅ |
| 6 | Scope Boundary (regression) — BE vs PE reasoning | 32 | 46 | 78 | 3/3 | yes | ✅ |
| 7 | Adversarial (regression) — patient-scope check | 35 | 48 | 83 | 3/3 | yes | ✅ |
| 8 | New A — minus-strand + no-PAM-guard batch | 38 | 58 | 96 | 4/4 | yes | ✅ |
| 9 | New B — batch CLI followed literally (isolates input-dir gap) | 20 | 28 | 48 | 2/3 | yes | ❌ |

**Execution Average: 75.4 / 100**
**Assertion Pass Rate: 29/32**

**Static Score: 90/100** (up from 70/100 pre-fix) — **Final Score: 90×0.4 + 75.4×0.6 = 36.0 + 45.2 = 81.2 / 100 — ✅ Limited Release** (deployable; Research Veto now PASSES)

---

## Independent verification of the pegRNA architecture (the load-bearing claim)

Before looking at the Skill's diagram, I hand-derived the correct PBS/RTT layout from Anzalone
2019's nCas9 nick geometry for the Skill's own worked-example locus (spacer
`ACGTTGACCTGGAACGTTCA`, NGG PAM immediately 3', C>T edit 11nt downstream of the nick):

- Nick = 3nt upstream of the PAM (standard PE nickase geometry): `cut_pos = pam_pos - 3`.
- PBS = genomic window **upstream** of the nick (part of the protospacer strand itself, must
  never touch the PAM), reverse-complemented onto the pegRNA.
- RTT = genomic window **downstream** of the nick (through the edit), reverse-complemented onto
  the pegRNA.
- Extension on the pegRNA = **RTT-revcomp + PBS-revcomp** (RTT first, PBS last — PBS is the
  pegRNA's 3'-terminal element), because PBS anneals to the nicked strand's 3'-OH to prime RT,
  and RT then reads the RTT template that lies 5' of the PBS on the pegRNA.

Hand computation (shown in full below; verified independently in this session, not copied from
the Skill or the fix log):

```
PBS genomic window (13nt upstream of nick) = TGACCTGGAACGT  ->  revcomp = ACGTTCCAGGTCA
RTT genomic window (18nt downstream, edited) = TCATGGCGATCTGTAAGC  ->  revcomp = GCTTACAGATCGCCATGA
Extension = RTT-revcomp + PBS-revcomp = GCTTACAGATCGCCATGAACGTTCCAGGTCA
```

This is **byte-identical** to SKILL.md's own worked example. The diagram (SPACER-SCAFFOLD-RTT-PBS,
PBS as the 3'-terminal element) is correct.

**Went further than re-deriving the Skill's own example.** Ran the fixed bundled
`examples/design_pegrna_pridict2.py` on two additional, independently-constructed loci
(`run/make_variants_round2.py`) — one forcing its `strand == '-'` branch — and cross-checked its
output against a **freshly, independently-run real PRIDICT2 CLI** on the same loci
(`run/verify_vs_real_pridict2.py`):

```
VAR_MINUS - script_pbs TTCGTAACCGGTT real_pbs TTCGTAACCGGTT MATCH | script_rt ACGGTCTAAGCTCCGGCA real_rt ACGGTCTAAGCTCCGGCA MATCH
VAR_MINUS + script_pbs CGGATCTTAACCG real_pbs CGGATCTTAACCG MATCH | script_rt CCGGAGCTTAGACCGTTA real_rt CCGGAGCTTAGACCGTTA MATCH
VAR_MINUS - script_pbs TCCGGCATTCGTA real_pbs TCCGGCATTCGTA MATCH | script_rt ATCCGTAACGGTCTAAGC real_rt ATCCGTAACGGTCTAAGC MATCH
VAR_REALISTIC + script_pbs ACGTTCCAGGTCA real_pbs ACGTTCCAGGTCA MATCH | script_rt GCTTACAGATCGCCATGA real_rt GCTTACAGATCGCCATGA MATCH
VAR_REALISTIC - script_pbs GCTTGGCCAATGG real_pbs GCTTGGCCAATGG MATCH | script_rt GTTCATGGCGATCTGTAA real_rt GTTCATGGCGATCTGTAA MATCH

5/5 script candidates found byte-identical (modulo edit-base case) in the real, independently-run
PRIDICT2 CLI's own output for the same locus/strand/length.
```

5/5 match, on **both strands**, on a locus never seen in SKILL.md's own example. This is the
strongest evidence available that the fix is not overfit to the worked example it was written
against.

Also independently verified **zero PAM overlap** across all 5 candidates by exact genomic
coordinate arithmetic (`run/verify_pbs_pam_overlap.py`) — the pre-fix defect where a PBS could
contain the PAM itself does not recur.

---

## Detailed Outputs

### Input 1 — Canonical (regression): PRIDICT2 batch CLI, fully corrected command

**Setup.** Two fresh 242nt loci (`VAR_REALISTIC`, `VAR_MINUS`), each with >100nt flanking on
both sides of the edit as PRIDICT2 requires, in the now-correct `sequence_name,editseq` format,
run with `--summarize K562` (the corrected flag usage).

**Execution log (`executed: true`):**
```
$ python pridict2_pegRNA_design.py batch --input-fname pridict2_batch_round2.csv \
    --output-dir predictions_round2/ --cores 1 --summarize K562
FileNotFoundError: [Errno 2] No such file or directory: '...\run\input\pridict2_batch_round2.csv'
```
Both pre-fix defects (`--summarize` needing a value, CSV column `editseq` not `sequence`) are
confirmed fixed — this is a **new** finding: the CLI's `--input-dir` defaults to `./input`, and
SKILL.md's own heredoc recipe writes the CSV to the current directory, not `./input/`. Creating
`input/` and moving the CSV there let the identical command complete:
```
Summarization completed! Summary file saved as 20260916_1957_summary_K562_batch_summary.csv
Batch processing completed!
```
`predictions_round2/*_pegRNA_Pridict_full.csv`: 765 rows/variant, real K562 scores 42.7%-49.3%,
non-trivial and varied — not a stub.

**Scores:** Basic: 22/40 | Specialized: 32/60 | Total: 54/100

**Assertions:**
- [PASS] `--summarize` value matches real CLI — fixed.
- [PASS] CSV column `editseq` matches real CLI — fixed.
- [FAIL] Literal recipe (CSV in cwd) completes without error — new: `input/` dir requirement undocumented.
- [PASS] Once corrected, batch mode produces real, non-trivial predictions.

---

### Input 2 — Variant A (regression): bundled script, same locus that crashed pre-fix

**Setup.** Identical 60nt-context locus to the pre-fix audit's Input 2 (edit 11nt from a real NGG
PAM) that raised `KeyError: 'pridict2_efficiency'` pre-fix.

**Execution log (`executed: true`):**
```
$ python design_pegrna_pridict2_FIXED.py
Variants attempted: 1
Variants with >=1 pegRNA passing PRIDICT2 >50%: 1
Total pegRNAs (top 3 per variant): 2
```
No crash. Top candidate (+strand): `pbs=ACGTTCCAGGTCA`, `rtt=GCTTACAGATCGCCATGA` — byte-identical
to this audit's own independent hand-derivation (see above) and to SKILL.md's worked example.
PAM-overlap check (`run/verify_pbs_pam_overlap.py`): no overlap for either candidate.

**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100

**Assertions:**
- [PASS] Runs end-to-end without crashing.
- [PASS] No PBS/PAM overlap (exact-coordinate check).
- [PASS] PBS/RTT match independent hand-derivation exactly.
- [PASS] No fabricated claim of real PRIDICT2 output (still honestly labeled placeholder).

---

### Input 3 — Edge (regression): CRISPResso2 PE quantification, fresh locus

**Setup.** A new 143bp locus, 420 synthetic reads (35.7%/50%/14.3% ref-clean/prime-edited/indel,
a different composition than the pre-fix audit's 40/40/20) — built specifically to
independently re-confirm the diagram fix beyond SKILL.md's own worked example
(`run/make_crispresso_round2.py`).

**Execution log (`executed: false` for the live-tool run):** `docker run` (both with a volume
mount, against two different mount directories including one already proven to work in this same
environment per `TOOLS.md`, and with no mount at all — `CRISPResso --version`) left the container
stuck in `Created` state indefinitely across 4 attempts. `docker version`, `docker ps`, and
`docker rm -f` all responded normally throughout the same window — this is a Docker
Desktop container-start hang on this shared machine at the time of the audit, not a Skill defect.

**Substituted:** a direct Python check reproducing CRISPResso2's own substring/revcomp
allele-matching logic (`run/crispresso_orientation_proxy_check.py`):
```
revcomp(extension_correct) in edited_amplicon: True
revcomp(extension_wrong)   in edited_amplicon: False
```
The fixed RTT-then-PBS order is the only one that can match; the pre-fix PBS-then-RTT order still
cannot — consistent with SKILL.md's own warning text. The pre-fix audit's own real, already-executed
CRISPResso2 run (different locus, `executed: true`, exact 40.0%/33.33% match to ground truth)
remains on file as the live-tool confirmation of this exact mechanism.

**Scores:** Basic: 22/40 | Specialized: 30/60 | Total: 52/100

**Assertions:**
- [PASS] Correct order's revcomp found in edited amplicon.
- [PASS] Wrong order's revcomp not found in edited amplicon.
- [FAIL] Live CRISPResso2 run executed this pass — blocked by Docker hang, not a Skill defect.
- [PASS] No fabricated CRISPResso2 percentage for this non-executed locus.

---

### Input 4 — Variant B (regression): PRIDICT2 single-mode determinism

**Execution log (`executed: true`):** Single-mode top K562 score for `VAR_REALISTIC`:
`49.268120527267456` — byte-identical to this pass's own batch-mode run (Input 1) and to the
pre-fix audit's independently-run scores (same value, **third** independent reproduction across
two audit passes). 5'-G spacer convention now documented in SKILL.md; independently reconfirmed
via `VAR_MINUS`'s real PRIDICT2 output (`Spacer-Sequence` first base forced to `G`, differing from
the script's true-genomic first base at that one position only).

**Scores:** Basic: 36/40 | Specialized: 54/60 | Total: 90/100

**Assertions:** all 4 PASS (determinism; convention now documented; convention reconfirmed on a
new locus; PBSlength/RTlength self-consistent).

---

### Input 5 — Stress (regression): Cross-Validate PE/BE snippet

**Execution log (`executed: true`):** Fresh 4-variant `be_hits_r2.tsv`/`pe_hits_r2.tsv`, ran the
snippet exactly as SKILL.md now shows it (with `import numpy as np; import pandas as pd`):
```
  variant_id  be_fdr  pe_fdr  be_lfc  pe_lfc  high_confidence
0         V1    0.01    0.02     1.8     1.5             True
1         V2    0.20    0.01     0.5     0.9            False
2         V3    0.03    0.02    -2.1    -1.9             True
3         V4    0.04    0.15     1.2     1.0            False
```
No `NameError`; concordance logic hand-verified correct.

**Scores:** Basic: 34/40 | Specialized: 50/60 | Total: 84/100 — 3/3 assertions PASS.

---

### Inputs 6-7 — Scope Boundary / Adversarial (regression, reasoning only)

Unaffected by this round's code fixes (pure SKILL.md/usage-guide.md content checks). Re-verified
against the current file versions: unchanged from pre-fix, both still 3/3 PASS.
Basic/Specialized/Total: 32/46/78 and 35/48/83 respectively.

---

### Input 8 — New A: minus-strand + no-PAM-guard batch

**Setup.** A mixed 3-variant batch: `VAR_REALISTIC` (regression locus), `VAR_MINUS` (new — its
only usable NGG PAM sits on the minus strand of the given context, forcing the script's
`strand == '-'` branch), `VAR_NO_PAM` (new — constructed with no NGG/CCN PAM within 35nt of the
edit, i.e. genuinely PE-undesignable).

**Execution log (`executed: true`):**
```
No PE-designable PAM/PBS/RTT window for 1 variant(s): ['VAR_NO_PAM'] -- excluded before PRIDICT2
scoring, not a script error.
Variants attempted: 3
Variants with >=1 pegRNA passing PRIDICT2 >50%: 2
Total pegRNAs (top 3 per variant): 5
```
No crash. `VAR_NO_PAM` cleanly excluded with a specific message — directly fixes the pre-fix P0's
"raw traceback, no guard" finding. All 5 candidates (both strands, both designable variants)
independently verified: zero PAM overlap (`run/verify_pbs_pam_overlap.py`), and for `VAR_MINUS`
specifically, byte-identical to a freshly, independently-run real PRIDICT2 CLI's own output on the
same locus (`run/verify_vs_real_pridict2.py`, 5/5 match — see "Independent verification" above).

**Scores:** Basic: 38/40 | Specialized: 58/60 | Total: 96/100 — 4/4 assertions PASS.

---

### Input 9 — New B: batch CLI followed literally (isolates the input-dir gap)

**Setup.** A clean scratch directory containing only the CSV SKILL.md's own heredoc example tells
the user to create — nothing else.

**Execution log (`executed: true`):**
```
$ python pridict2_pegRNA_design.py batch --input-fname variants.csv --output-dir predictions/ \
    --cores 1 --summarize K562
FileNotFoundError: [Errno 2] No such file or directory: '<scratch>\input\variants.csv'
```
Confirms the CLI's own `--help` default is `--input-dir ./input` (source-inspected:
`pridict2_pegRNA_design.py:1106`). After `mkdir input && mv variants.csv input/`, the identical
command succeeds. This is a documentation gap, not a functional break — but it does mean the
documented recipe, followed exactly, crashes on the very first line.

**Scores:** Basic: 20/40 | Specialized: 28/60 | Total: 48/100

**Assertions:**
- [FAIL] Literal recipe completes without error.
- [PASS] The resulting crash is loud and immediately diagnosable (names the missing path), not a silent wrong answer.
- [PASS] Everything else is correct once `input/` exists.

---

## Research Veto

- **M1 Scientific Integrity: PASS** — unchanged, all citations real and correctly attributed.
- **M2 Practice Boundaries: PASS** — unchanged, reconfirmed via Input 7.
- **M3 Methodological Ground: PASS** — unchanged.
- **M4 Code Usability: PASS** (flipped from FAIL pre-fix) — all three pre-fix defects
  independently confirmed fixed by fresh execution on both regression and new inputs, including
  cross-validation against a freshly-run real PRIDICT2 CLI on loci and strands never covered by
  the Skill's own worked example. One new, lesser-severity defect found (undocumented `input/`
  directory requirement) is a loud, immediately-diagnosable crash rather than a silent
  wrong-science result, and is scored as P1 rather than a veto trigger.

> **Note for reviewer.** The single most important result in this re-audit is the 5/5 byte-identical
> match between the fixed bundled script's PBS/RTT output and a freshly, independently-run real
> PRIDICT2 CLI, on a locus and strand the Skill's own worked example never exercises. That is
> stronger evidence than re-deriving the Skill's own example alone would have been. The second
> most important finding is the new P1 (undocumented `input/` directory) — worth fixing, but not in
> the same severity class as the pre-fix silent-0%-editing defect it replaces as the Skill's most
> prominent open issue.
