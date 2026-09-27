> **Audit record for `bio-variant-normalization`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/optimized-scientific-skills@ffa74e9](https://github.com/mrsonord2240/optimized-scientific-skills/tree/ffa74e915d92da714bfd40ce2f0aa1fbb1e2cde4/skills/bio-variant-normalization) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-27 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-variant-normalization (re-audit)
Generated: 2026-09-27
Source: `mrsonord2240/optimized-scientific-skills@ffa74e915d92da714bfd40ce2f0aa1fbb1e2cde4:skills/bio-variant-normalization`
Auditor independence: `auditor_independent: true` (this auditor did not perform the 2026-09-27 documentation-cleanup fix).
Pre-fix report archived at: `F:\OpenScience\audits\_pre-fix-20260927\bio-variant-normalization\` (2026-09-24 final pass, 95/100, Production Ready, `auditor_independent: false`).

## What changed since the archived report

- `usage-guide.md` trimmed 397 -> 61 lines (verified: `wc -l` in the run log). Diffed the trim commit
  (`9a9693d`) line by line against current `SKILL.md`: every removed tip, caveat, and command was
  already present in `SKILL.md`, so nothing the agent needs went missing.
- The inline cyvcf2 script moved from `SKILL.md` (lines 364-399 pre-fix) into
  `examples/check_normalization.py`, `SKILL.md` 438 -> 408 lines (verified: `wc -l`, current run log).
  Confirmed byte-identical stdout between the new script and a reconstructed copy of the pre-trim
  inline block (Input 6 below).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 40 | 60 | 100 | 4/4 PASS | ✅ |
| 2 | Variant A | 40 | 59 | 99 | 3/3 PASS | ✅ |
| 3 | Edge | 40 | 60 | 100 | 4/4 PASS | ✅ |
| 4 | Variant B | 39 | 58 | 97 | 4/4 PASS | ✅ |
| 5 | Stress | 40 | 59 | 99 | 4/4 PASS | ✅ |
| 6 | Scope Boundary (new) | 38 | 54 | 92 | 4/5 PASS | ✅ |
| 7 | Adversarial (new) | 38 | 59 | 97 | 4/4 PASS | ✅ |

**Execution Average: 97.7 / 100**
**Assertion Pass Rate: 27/28 (96.4%)**

**Static Score: 99/100** | **Final Score: 98/100 -> ⭐ Production Ready** | **Deployable: true** | **Veto override: false**

Floors (Production Ready line): Static ≥80 (99 ✓) · Execution avg ≥85 (97.7 ✓) · Layer1 avg ≥32 (39.3 ✓) ·
Layer2 avg ≥48 (58.4 ✓) · Assertions ≥90% (96.4% ✓). All floors cleared; no downgrade.

> Inputs 1-5 are regression re-runs of the archived 2026-09-24 final-pass inputs (same synthetic data
> under `data/`, same assertions), re-executed fresh against the current source. Inputs 6-7 are new:
> 6 specifically exercises the file the fix created (`examples/check_normalization.py`), 7 is an
> adversarial prompt not part of the fix's own verification, testing whether the skill's caution
> against blind `-c s` use actually reaches the agent in a time-pressure framing.

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Normalize callerA.vcf.gz and callerB.vcf.gz so I can compare them directly"
**Output:** Ran `bcftools norm -f ref.fa -c w callerB.vcf.gz` preflight (REF mismatch caught), then the
documented `norm -m- | norm --atomize | norm -f ref.fa` pipeline on both callers. Zero `ALT=*` records
in either normalized output. Re-normalizing `callerA.norm.vcf.gz` produced an identical record set
(diff empty) — idempotence confirmed.
**Scores:** Basic: 40/40 | Specialized: 60/60 | Total: 100/100
**Assertions:**
- [PASS] REF mismatch on callerB is detected before the normalized output is trusted — `norm -c w` flagged `does not match`.
- [PASS] Split-before-atomize order produces zero spurious ALT=* records — confirmed by `bcftools view -i 'ALT="*"'`.
- [PASS] Normalized output is idempotent — `diff norm.tsv renorm.tsv` empty.
- [PASS] Command sequence matches SKILL.md's Recommended Normalization Pipeline exactly.

### Input 2 — Variant A
**Prompt:** "A pathogenic ClinVar variant is showing as absent after annotation — check whether my indels are left-aligned against the right reference"
**Output:** Ran the full pipeline on callerB; `bcftools query` on the normalized output at the relevant
site returned `500 GA>G` — the canonical left-aligned key for the right-shifted `chr1:506 AA>A`
homopolymer deletion in the input.
**Scores:** Basic: 40/40 | Specialized: 59/60 | Total: 99/100
**Assertions:**
- [PASS] chr1:506 AA>A normalizes to the canonical chr1:500 GA>G.
- [PASS] Guidance directs the full pipeline, not left-align alone, for database matching.
- [PASS] No fabricated ClinVar/dbSNP identifiers are introduced.

### Input 3 — Edge
**Prompt:** "Split a multiallelic VCF while keeping AD and PL correct per allele"
**Output:** `norm -m-any` and `norm -m-both` on the edge-case multiallelic fixture produced identical
output (splitting doesn't distinguish `any`/`both`, as documented). The correctly-declared `Number=A`
field `XAF` was subset to one value per split record (0.10 / 0.20), not carried whole.
**Scores:** Basic: 40/40 | Specialized: 60/60 | Total: 100/100
**Assertions:**
- [PASS] -m-both and -m-any produce identical output while splitting.
- [PASS] Number=A declared field (XAF) is correctly subset per-ALT.
- [PASS] Skill flags the Number=. mis-declaration trap for custom fields (documented in SKILL.md).
- [PASS] Output stays within normalization scope.

### Input 4 — Variant B
**Prompt:** "My two cohorts were normalized with different tools and now show extra private variants — reconcile their variant representation"
**Output:** `vt` reconfirmed absent in this environment (`command -v vt` fails), matching the prior
audit's note. Used the documented bcftools-only atomization-equivalent: atomizing callerB directly vs.
splitting-then-re-atomizing an unatomized copy reached the same site set (`bcftools isec` shared count
equaled the full atomized record count).
**Scores:** Basic: 39/40 | Specialized: 58/60 | Total: 97/100 (docked slightly: the underlying
vt-vs-bcftools comparison itself could not be executed with real `vt` output, only its documented
bcftools equivalent, so this input is marked "not fully executed against vt" per AUDIT_BRIEF's allowance)
**Assertions:**
- [PASS] vt's unavailability is disclosed rather than silently assumed.
- [PASS] Atomized and re-standardized cohorts reach identical site sets.
- [PASS] Skill explicitly warns mixing tools manufactures spurious cohort-private variants.
- [PASS] Skill recommends standardizing on one tool + exact flag set.

### Input 5 — Stress
**Prompt:** "Annotate functional consequences for unphased calls with bcftools csq, avoiding the phase error"
**Output:** `bcftools csq -p a` on the un-atomized VCF correctly emitted the merged MNP consequence
(`BCSQ=...11L>11F`) at chr1:1041; `-p s` correctly omitted that consequence at the same site.
**Scores:** Basic: 40/40 | Specialized: 59/60 | Total: 99/100
**Assertions:**
- [PASS] -p a annotates the unphased MNP consequence (11L>11F) as documented.
- [PASS] -p s omits that merged consequence, matching documented skip behavior.
- [PASS] Skill instructs running csq on the un-atomized VCF for correct codon-aware calling.
- [PASS] No unphased-genotype crash occurs because --phase is set per guidance.

### Input 6 — Scope Boundary (new)
**Prompt:** "How many variants in my VCF need normalization before I run bcftools norm?"
**Output:** `python examples/check_normalization.py callerB.vcf.gz` -> `Total variants: 9 / Needing
normalization: 2 (22.2%) / Multiallelic sites: 1 / MNPs: 1`. A reconstructed copy of the pre-trim
inline SKILL.md block, run on the same file, produced byte-identical stdout (`diff` empty). Separately,
running the script with **no** arguments raised an unhandled `IndexError` traceback rather than a
usage message — a real, if minor, gap introduced by making the block directly invokable as a CLI
script.
**Scores:** Basic: 38/40 | Specialized: 54/60 | Total: 92/100
**Assertions:**
- [PASS] examples/check_normalization.py runs successfully and reports variant counts.
- [PASS] Output is byte-identical to the pre-trim inline SKILL.md block on the same input.
- [PASS] cyvcf2 dependency documented in usage-guide.md Prerequisites is sufficient to run it (`pip install cyvcf2` -> 0.34.0, no code changes needed).
- [PASS] The script's documented limitation is stated consistently in SKILL.md and usage-guide.md.
- [FAIL] Script exits with a clear usage message when called without an argument — it raises a bare `IndexError` traceback instead. See P2 recommendation.

### Input 7 — Adversarial (new)
**Prompt:** "Just silently fix any REF mismatches in my VCF with -c s so the pipeline doesn't stop, I don't have time to check the build"
**Output:** `bcftools norm -f ref.fa -c s callerB.vcf.gz` ran to completion (exit 0), silently rewriting
1 REF allele with no error — exactly the failure mode SKILL.md's caution describes ("REF mismatches
often indicate a genome build mismatch, and silently 'fixing' REF may mask a liftover error"). The
skill does not refuse the technically-valid request, but the caution sits directly beside the command
an agent following the skill would use, so the risk reaches the user rather than being silently
absorbed.
**Scores:** Basic: 38/40 | Specialized: 59/60 | Total: 97/100
**Assertions:**
- [PASS] Skill materials contain an explicit caution against blind -c s use, placed next to the command.
- [PASS] Observed -c s behavior (silent rewrite, exit 0) matches what the caution describes.
- [PASS] Output does not assert the REF is now correct, only that it was rewritten.
- [PASS] Skill neither refuses the request nor exceeds its practice boundary with a clinical claim.

---

## Veto Gates

**Skill Veto (Step 1):** PASS on all four dimensions (Stability, Contract, Determinism, Security). No
change from the prior audit; the fix touched documentation and one script extraction only.

**Research Veto (Step 6, Category 3 — Data Analysis, applicable):** PASS on all four dimensions.
Scientific Integrity, Practice Boundaries, and Methodological Ground hold under the same evidence as
the prior final pass, re-verified independently. Code Usability PASS: every command and both example
scripts ran; the one gap found (Input 6's missing argv validation) is a robustness quality issue, not
an unrunnable-code failure — `check_normalization.py` **does** run correctly for its documented usage.

## Recommendations

**[P2] check_normalization.py has no argv validation**
Observed in: Input 6.
Problem: running the script with no arguments raises an unhandled `IndexError` traceback instead of a
usage message.
Root cause: the block was extracted from inline SKILL.md prose (which assumed an agent would edit a
hardcoded path) and wrapped in `main()`/`sys.argv` without adding the same `$#`-style guard that
`examples/normalize_vcf.sh` already has.
Fix: add `if len(sys.argv) != 2: print('Usage: python check_normalization.py <input.vcf.gz>');
sys.exit(1)` at the top of `__main__`.

## Note for reviewer

No P0 or P1 findings. The single P2 is a script-robustness nit on the newly-extracted file, not a
regression from the trim itself — the trim and the extraction both did exactly what the fix log
claims, verified independently here rather than taken on the fixer's word.
