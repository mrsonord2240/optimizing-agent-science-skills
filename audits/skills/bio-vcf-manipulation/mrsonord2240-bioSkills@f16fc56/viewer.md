> **Audit record for `bio-vcf-manipulation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@f16fc56](https://github.com/mrsonord2240/bioSkills/tree/f16fc56a854565e26d87a67d3de2df91e986b056/variant-calling/vcf-manipulation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Final-pass eval viewer: bio-vcf-manipulation

Evaluated 2026-09-24 against `mrsonord2240/bioSkills@f16fc56a854565e26d87a67d3de2df91e986b056:variant-calling/vcf-manipulation`.

Final score: **93/100 — Production Ready (self-audited)**.

Final-pass disclosure: `auditor_independent=false`. The operator who made the correction audited this exact commit, so this is execution evidence, not independent acceptance evidence. Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

## Exact correction

The final source commit tightens the `--naive` concat recovery: a sample-order repair of only one input must use plain `bcftools concat`; `--naive` is valid only after `bcftools view -s <same-order>` has been applied to every input, making both sample columns and headers identical. The existing P1 fix was also reverified: `reheader -f` updates headers only, while `annotate --rename-chrs` updates record CHROM values.

## Execution evidence

All seven archived cases were rerun with WSL bcftools 1.24:

- `p_in1`: default single-sample merge left missing calls missing; `-0` fabricated 62 0/0 calls where the joint truth was missing.
- `p_in2`: ordinary concat and overlap dedup behaved as documented; the old one-file `--naive` advice continued to fail, which is the scenario addressed by the exact correction.
- `p_in3`: normalization changed `isec -n+2` from 9 to 11; all-three was 8.
- `p_in4`: `view -s` updated AC/AN but stale AF remained at 277 records; `+fill-tags` corrected AC/AN/AF.
- `p_in5`: record-level contig rename followed by merge matched the 361-site joint truth across 8 samples; sort then index succeeded.
- `in6`: SV caller calls with near breakpoints did not form a bcftools consensus, confirming the boundary to SV-aware tools.
- `in7`: explicit sample renaming retained both people; `--force-samples` produced the expected prefixed duplicate label.

Two fresh cases passed:

- `runs/final_20260924_fresh_naive_reorder.sh`: plain concat after a one-file reorder and `--naive` after applying the same order to both files each produced 361 records and the joint-truth tuple hash.
- `runs/final_20260924_fresh_contig_records.sh`: `reheader -f` left body CHROM values as `1,2`; `annotate --rename-chrs` followed by merge produced 361 sites, 8 samples, and the joint-truth tuple hash.

The raw machine-readable result is [eval_report_bio-vcf-manipulation_result.json](eval_report_bio-vcf-manipulation_result.json). Console evidence is stored beside each archived run as `final_20260924.out`, with fresh logs in `runs/final_20260924_fresh_*.out`.

## Limits reflected in the score

The nine cases are synthetic and use one current bcftools runtime. The archived sort case emitted a mounted-filesystem temporary-directory chmod warning while still producing a valid indexed 361-record output. Neither limitation is presented as independent or production-scale coverage.
