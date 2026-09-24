> **Audit record for `bio-pathway-reactome`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@e66cde9](https://github.com/mrsonord2240/bioSkills/tree/e66cde984eb21bf2a9767ea6616c96aafeba3c04/pathway-analysis/reactome-pathways) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-pathway-reactome final-pass audit

## Canonical final summary

**Final:** 89/100 — ⭐ Production Ready; deployable: true.

**89/100 ⭐ — Production Ready.** Exact source: `mrsonord2240/bioSkills@e66cde984eb21bf2a9767ea6616c96aafeba3c04:pathway-analysis/reactome-pathways`.

Final-pass metadata: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

This final report scores six retained private-Linux inputs under `run/phase2_e66cde9_linux_20260923/`: package load; exact ORA (20 rows, CSV); exact bounded GSEA (54 rows, planted pathway rank 1, CSV); SYMBOL/URL edge behavior; measured-universe result (193 measured versus 11146 default denominator); and unsupported-organism boundary. All six runners exited 0, with 10/10 retained assertions. `input07_invalid_organism.R` is retained as an unscored corroborating control to avoid duplicating the scored organism boundary.

The sole P2 operational recommendation is to document/use the private Linux R/Bioconductor route because the equivalent Windows ReactomePA stack exits 2816 at teardown.
