#!/usr/bin/env python3
"""Delta check: candidate frontmatter parses as YAML, and the marketplace tool's own
skill_category() accepts the declared category. Read-only import of the tool.
Usage: check_frontmatter.py <skill_id> <worktree_root_containing_skills/>"""
import importlib.util, sys, yaml

sid, shelf = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location(
    "mm", r"F:/optimizing-agent-science-skills/tools/marketplace_manifests.py")
mm = importlib.util.module_from_spec(spec); spec.loader.exec_module(mm)
print("VALID_CATEGORIES:", sorted(mm.VALID_CATEGORIES))
print("skill_category():", mm.skill_category(sid, shelf=shelf))
text = open(f"{shelf}/skills/{sid}/SKILL.md", encoding="utf-8").read()
fm = yaml.safe_load(text[3:text.find("\n---", 3)])
print("yaml keys:", list(fm))
print("name matches id:", fm["name"] == sid, "| category:", fm.get("category"), "| author:", fm.get("author"),
      "| license:", fm.get("license"))
