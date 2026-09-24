> **Audit record for `bio-remote-homology`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@7153e87](https://github.com/mrsonord2240/bioSkills/tree/7153e877bfec221df95ba1f5758f4012e788b7aa/database-access/remote-homology) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-22 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-remote-homology

Generated: 2026-09-22
Source: `mrsonord2240/bioSkills@7153e877bfec221df95ba1f5758f4012e788b7aa:database-access/remote-homology`
Final-pass metadata: `auditor_independent: false` — final pass: fixed and audited under one brief, see CHECKPOINT.md. The superseded intermediate re-audit was archived intact at `F:\OpenScience\audits\_pre-fix-20260922\bio-remote-homology`.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical | 38 | 58 | 96 | 4/4 | ✅ |
| 2 | Variant A | 38 | 57 | 95 | 4/4 | ✅ |
| 3 | Edge | 38 | 58 | 96 | 4/4 | ✅ |
| 4 | Variant B | 39 | 58 | 97 | 4/4 | ✅ |
| 5 | Stress | 38 | 58 | 96 | 4/4 | ✅ |
| 6 | Scope Boundary | 37 | 57 | 94 | 4/4 | ✅ |
| 7 | Adversarial | 38 | 57 | 95 | 4/4 | ✅ |
| 8 | Stress | 38 | 58 | 96 | 4/4 | ✅ |
| 9 | Edge | 39 | 58 | 97 | 4/4 | ✅ |
| 10 | Variant B | 39 | 59 | 98 | 4/4 | ✅ |
| 11 | Edge | 28 | 39 | 67 | 2/4 | ⚠️ |

- Execution average: **93.4 / 100**
- Assertion pass rate: **42 / 44**
- Static score: **91 / 100**
- Final score: **92 / 100 — ⭐ Production Ready**
- Deployable: **true**
- Veto: **none**

## Execution evidence

All runnable evidence is under [run/phase2](F:/OpenScience/audits/bio-remote-homology/run/phase2). The scripts were run from the WSL `science` / `bio` environment. The audited worktree remained clean at the requested tip after execution.

The following production-scale branches were deliberately not started, as required by the checkpoint: full Pfam-A (~1.7 GB compressed), AlphaFoldDB Swiss-Prot and ProstT5 (multi-GB), and UniRef30/PDB70 (tens of GB). Small cached fixtures exercised the same local command paths, but are not misrepresented as full-database validation.

### Input 1 — Canonical: Pfam annotation of PRKACA

**Prompt:** “Annotate PRKACA domains with Pfam-A using calibrated gathering thresholds and report the full E-value and score.”

**Executed:** [01_pfam_annotation_mock_full.sh](F:/OpenScience/audits/bio-remote-homology/run/phase2/scripts/01_pfam_annotation_mock_full.sh). The unmodified shipped script ran against the bundled real PF00069 model presented as a reduced local Pfam-A substitute. It returned:

```
sp|P17612|KAPCA_HUMAN  Pkinase  PF00069.32  1.4e-79  253.2
```

This confirms the repaired domtbl fields. Full Pfam-A remains blocked by the approved size limit.

### Input 2 — Variant A: MMseqs2 twilight-zone sensitivity

**Prompt:** “Search PRKACA for remote homologs; compare default MMseqs2 sensitivity to `-s 7.5`.”

**Executed:** [02_mmseqs_sensitivity.sh](F:/OpenScience/audits/bio-remote-homology/run/phase2/scripts/02_mmseqs_sensitivity.sh). The live tool reported default sensitivity 5.7. Default output had zero rows; `-s 7.5` recovered Q197B6. This matches the Skill’s documented decision rule.

### Input 3 — Edge: Foldseek setup and cached structure search

**Prompt:** “Verify the required remote-homology tools, then search a structure with Foldseek and report probability, TM-scores, and lDDT.”

**Executed:** [00_required_setup.sh](F:/OpenScience/audits/bio-remote-homology/run/phase2/scripts/00_required_setup.sh) and [03_foldseek_shipped_script.sh](F:/OpenScience/audits/bio-remote-homology/run/phase2/scripts/03_foldseek_shipped_script.sh). All advertised banners printed, including `foldseek Version: 10.941cd33`; the shipped script reused the `.dbtype` cache and returned a high-confidence 1ATP self-hit. No AFDB or ProstT5 download was attempted.

### Input 4 — Variant B: Iterative profile comparison

**Prompt:** “Run the Skill’s three-way PSI-BLAST, jackhmmer, and MMseqs2 profile comparison on a distant kinase homolog.”

**Executed:** [04_iterative_profile_shipped_script.sh](F:/OpenScience/audits/bio-remote-homology/run/phase2/scripts/04_iterative_profile_shipped_script.sh). The copied, unmodified shipped example built the BLAST DB, saved both PSSM forms, and recovered Q197B6 in `psiblast.tsv`, `jackhmmer.tbl`, and `mmseqs.m8`.

### Input 5 — Stress: DIAMOND mode selection

**Prompt:** “At metagenomic scale, determine whether DIAMOND’s default, more-sensitive, or ultra-sensitive mode recovers this remote homolog; cross-check with jackhmmer.”

**Executed:** [05_diamond_jackhmmer.sh](F:/OpenScience/audits/bio-remote-homology/run/phase2/scripts/05_diamond_jackhmmer.sh). Default and `--more-sensitive` produced zero rows under the same cutoff. `--ultra-sensitive` and jackhmmer both recovered Q197B6. The Skill’s strongest remote-homology recommendation is supported on this fixture.

### Input 6 — Scope Boundary: function from structure

**Prompt:** “A Foldseek hit has high probability and TM-score. Can I call it the same enzyme?”

**Executed:** Direct Mode-D reasoning from the Foldseek failure-mode guidance. The correct output is: report structural support, but do not infer identical function; combine it with sequence evidence and conserved catalytic-residue checks. No diagnostic or clinical claim is involved.

### Input 7 — Adversarial: omit the statistic

**Prompt:** “Just tell me whether it is homologous; skip the E-value and thresholds.”

**Executed:** Direct Mode-D reasoning from the new uncertainty escape hatch. The correct output keeps the real E-value/score/probability and says “statistically supported match,” not “confirmed homology.”

### Input 8 — Stress: direct Foldseek command

**Prompt:** “Run the exact `easy-search` command shown in the Skill and inspect all structural fields.”

**Executed:** [08_foldseek_direct_search.sh](F:/OpenScience/audits/bio-remote-homology/run/phase2/scripts/08_foldseek_direct_search.sh). The direct command returned:

```
1atp_E  1atp_E  1.000  336  1.943E-68  2860  1.000  1.000E+00  1.000E+00  1.000E+00
```

### Input 9 — Edge: Pfam zero hit

**Prompt:** “Annotate a sequence with no Pfam domain above gathering threshold and tell me clearly what happened.”

**Executed:** [09_pfam_no_hit.sh](F:/OpenScience/audits/bio-remote-homology/run/phase2/scripts/09_pfam_no_hit.sh). The unmodified shipped script exited successfully and printed:

```
No Pfam-A domains found above the gathering threshold.
```

### Input 10 — New: jackhmmer checkpoint handoff

**Prompt:** “Run three jackhmmer rounds, then use the final emitted checkpoint HMM for an independent target search.”

**Executed:** [10_iterative_hmmer_checkpoint.sh](F:/OpenScience/audits/bio-remote-homology/run/phase2/scripts/10_iterative_hmmer_checkpoint.sh). The fixed `--chkhmm iter` spelling produced `iter-1.hmm` and `iter-2.hmm`; the documented highest-version selector used `iter-2.hmm` and hmmsearch recovered Q197B6.

### Input 11 — New: low-complexity masking

**Prompt:** “Mask a repeat-rich query before profile construction, then continue with the masked sequence.”

**Executed:** [11_low_complexity_masking.sh](F:/OpenScience/audits/bio-remote-homology/run/phase2/scripts/11_low_complexity_masking.sh). The exact documented command returned only:

```
>synthetic_low_complexity
12 - 127
```

Adding `-outfmt fasta` emitted the soft-masked lowercase sequence, but that required command and the handoff to the next profile command are absent from the Skill. This is the open P1.

## Veto review

- T1 stability: PASS — 8 executable test scripts and all shipped shell syntax checks completed.
- T2 contract: PASS — required frontmatter and shipped references are present.
- T3 determinism: PASS — tool/DB version considerations are documented and PSSM reuse is supported.
- T4 security: PASS — no eval/exec of user strings, credentials, or unquoted positional shell interpolation.
- M1 scientific integrity: PASS — all numerical results came from inspected tool output.
- M2 practice boundaries: PASS — no diagnosis, treatment, or individual medical advice.
- M3 methodological baseline: PASS — the Skill avoids equating structural similarity with function; the P1 is an incomplete mitigation command, not a false inference.
- M4 code usability: PASS — code runs and all required CLIs are present; Input 11’s incomplete data handoff is tracked for repair.

## Recommendations

1. **P1 — Make the low-complexity mitigation produce a masked FASTA.** Use `segmasker -infmt fasta -in query.fa -outfmt fasta > query.masked.fa`, then direct profile construction to `query.masked.fa`. Note that output is soft-masked lowercase.
2. **P2 — Add standalone PSI-BLAST and HHsearch examples** when usable production databases are available.
