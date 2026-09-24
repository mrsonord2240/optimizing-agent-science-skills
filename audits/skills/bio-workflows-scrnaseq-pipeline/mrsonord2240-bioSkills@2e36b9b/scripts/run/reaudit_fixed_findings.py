from pathlib import Path

source = Path(r"F:\OpenScience\worktrees\bio-workflows-scrnaseq-pipeline-fixpass\workflows\scrnaseq-pipeline\SKILL.md").read_text(encoding="utf-8")
for text in ("RunHarmony", "AggregateExpression", "propeller", "[after_loading]", "[after_qc]", "[after_normalization]", "[after_clustering]", "^ENSG", "median(nFeature_RNA)-3*mad"):
    assert text in source, text
print("PASS commit=2e36b9b multi-sample DE/DA checkpoints MAD QC input validation present")
