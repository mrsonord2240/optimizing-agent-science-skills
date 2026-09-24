# bio-scaffold-analysis fix pass — 2026-09-24

## Source

- Repository/worktree: `F:\OpenScience\worktrees\bio-scaffold-analysis-fixpass`
- Branch: `agent/fix-bio-scaffold-analysis`
- Base: `80118b2aa7a282506e2661ce9c8bc8a810d0a1fb`
- Final source commit: `ca93ac599c17ee0c898c2a443777a60ebcd96177`

## Resolved audit findings

- **P1 — MMPA recipe:** added the required `mmpdb loadprops -p props.tsv data.mmpdb` step; defined the tab-separated ID/property contract; replaced the nonexistent ranking/confidence claim with the actual property-prefixed transform fields and explicit sorting guidance.
- **P1 — split pathology:** replaced largest-first train filling with deterministic balanced group allocation, retained whole-scaffold isolation, added optional diagnostics, and asserts that a multi-scaffold library cannot silently yield an all-singleton test set.
- **P2 — worked strings:** replaced hand-written equivalent SMILES with RDKit 2026.03.6 canonical output.
- **P2 — generic framework scale:** added a clearly library-specific 1,500-compound reference measurement (857 Bemis-Murcko vs 583 generic frameworks; 1.47-fold collapse; largest generic group spans four Bemis-Murcko scaffolds).

## Exact-commit validation

- `ca93ac5` worktree clean; `git diff --check HEAD^ HEAD` passed.
- Bundled splitter on the audited 1,500-compound fixture: requested 0.8, 0.7, and 0.9 train fractions achieved exactly; scaffold overlap was 0 for each; test singleton-compound fractions were 0.407, 0.407, and 0.400; same-seed result was identical.
- Canonical worked outputs matched exactly: `O=C(NCC1CCCC1)c1ccccc1` and `CC(CCC1CCCC1)C1CCCCC1`.
- mmpdb 3.1.4 focused property validation loaded 1,064 pIC50 records, recalculated 45,317 rule statistics, and produced 135 transforms with `pIC50_count`, `pIC50_avg`, `pIC50_std`, `pIC50_paired_t`, and `pIC50_p_value`.
- Skill-creator quick validation was run. It reports the upstream legacy frontmatter fields `tool_type`, `primary_tool`, and `author` as unsupported by that generic validator; these predate this focused repair and were left unchanged.

## Re-audit result

- **93/100 — Production Ready**
- **Assertions: 30/30**
- **Open P0/P1/P2: 0/0/0**

## Artifacts

- Canonical JSON: `F:\OpenScience\audits\bio-scaffold-analysis\eval_report_bio-scaffold-analysis_result.json`
- Canonical viewer: `F:\OpenScience\audits\bio-scaffold-analysis\eval_viewer_bio-scaffold-analysis.md`
- Focused evidence: `F:\OpenScience\audits\bio-scaffold-analysis\re-audit-20260924\run-focused\`
- Preserved pre-fix canonical report/viewer: `F:\OpenScience\audits\bio-scaffold-analysis\re-audit-20260924\pre-fix\`

No remaining P0, P1, or P2 findings.
