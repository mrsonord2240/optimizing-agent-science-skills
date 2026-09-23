from pathlib import Path

skill = Path(r"F:\OpenScience\wt\ncbi-datasets-cli\database-access\ncbi-datasets-cli\SKILL.md").read_text()
for phrase in ("PubMed | no", "SRA reads | no", "BLAST | no", "Exit 0 alone is not success", "--ortholog all", "`rehydrate` does not verify"):
    assert phrase in skill, phrase
print("SCOPE_AND_INTEGRITY_GUARDRAILS=PASS")
