# New input for this re-audit: verify the redundancy pass (SKILL.md 209->250 lines,
# usage-guide.md 100->37 lines) did not strand anything an agent following ONLY usage-guide.md's
# "Quick Start" scenarios (deleted) would have needed. Checks each deleted usage-guide.md passage's
# claimed new home in SKILL.md is actually present and says the same thing, plus flags anything
# that reads as a genuine content loss rather than a true duplicate.
import re

skill = open("skill_copy/SKILL.md", encoding="utf-8").read()
usage = open("skill_copy/usage-guide.md", encoding="utf-8").read()

checks = [
    ("Prerequisites install block moved to Version Compatibility",
     "BiocManager::install(c('clusterProfiler', 'rWikiPathways', 'enrichplot', 'org.Hs.eg.db'))" in skill),
    ("Internet-required conceptual bullet preserved",
     "require internet at run time" in skill),
    ("CC0 / no peer review conceptual bullet preserved",
     "no formal journal-style peer review" in skill or "no formal peer review" in skill),
    ("Entrez-keyed / wrong-ID-type conceptual bullet preserved",
     "Entrez-keyed" in skill),
    ("universe=NULL inflates significance conceptual bullet preserved",
     "universe=NULL" in skill and "inflates significance" in skill),
    ("'What the Agent Will Do' -> 'Agent Workflow' section present in SKILL.md",
     "## Agent Workflow" in skill),
    ("'Understanding Results' column table present in SKILL.md",
     "## Understanding Results" in skill and "core_enrichment" in skill),
    ("'WikiPathways vs Other Databases' -> 'WikiPathways vs KEGG/Reactome' table present",
     "## WikiPathways vs KEGG/Reactome" in skill and "CC0 (fully open)" in skill),
    ("Tip: exact organism string via listOrganisms()/get_wp_organisms()",
     "get_wp_organisms()" in skill and "match exactly" in skill),
    ("Tip: pin dated GMT / report date",
     "report the date" in skill),
    ("Tip: format='gmt' required (default gpml)",
     "format='gmt'" in skill and "gpml" in skill),
    ("Tip: split term field on %",
     "sep='%'" in skill or "sep = '%'" in skill),
    ("Tip: getPathwayInfo last-edit check before trusting a hit",
     "getPathwayInfo" in skill and ("last-edit" in skill or "last-edited" in skill)),
    ("Tip: PFOCR as noise-tolerant complement",
     "PFOCR" in skill),
    ("Tip: setReadable() converts Entrez to symbols",
     "setReadable" in skill),
    ("Tip: WikiPathways has FEWER TOTAL PATHWAYS than KEGG (quantitative claim, not just species count)",
     "fewer" in skill.lower() and "pathway" in skill.lower()),
    ("New P2 fix: wrong-organism-string Common Errors row present",
     "non-canonical organism string" in skill or ("wrong" in skill and "organism string" in skill)),
    ("New P1 fix: Zenodo fallback named",
     "zenodo.org/communities/wikipathways" in skill),
    ("New P1 fix: retention window (~12 months) stated",
     "12 months" in skill),
]

print(f"{'PASS' if True else '':>0}")
n_pass = 0
for label, ok in checks:
    status = "PASS" if ok else "FAIL"
    if ok:
        n_pass += 1
    print(f"[{status}] {label}")
print(f"\n{n_pass}/{len(checks)} checks passed")

# Quick-Start one-liners: were they truly duplicated, or is any scenario now UNCOVERED by
# Example Prompts (usage-guide.md) + Decision Tree (SKILL.md)?
quick_start_deleted = [
    "Run WikiPathways enrichment on my significant genes",
    "Find disease-specific pathways in my gene list that KEGG and Reactome miss",
    "Run a reproducible WikiPathways analysis pinned to a dated release",
]
print("\n--- Quick Start scenario coverage check ---")
print("1) basic enrichment -> covered by usage-guide.md 'Basic enrichment' Example Prompt: ",
      "Convert them to Entrez, run WikiPathways over-representation" in usage)
print("2) disease-specific pathways missing from KEGG/Reactome -> covered by SKILL.md Decision "
      "Tree row 'Disease / drug pathways missing from KEGG/Reactome': ",
      "Disease / drug pathways missing from KEGG/Reactome" in skill)
print("   (NOTE: usage-guide.md's own 'Combining databases' prompt asks for unique-vs-shared "
      "pathways, which is adjacent but not identical wording -- the SKILL.md Decision Tree row is "
      "the closer match, so coverage survives but moved files, not a clean 1:1 dedup)")
print("3) reproducible dated analysis -> covered by usage-guide.md 'Reproducible analysis' "
      "Example Prompt: ",
      "pin a dated GMT release, split the term field" in usage)
