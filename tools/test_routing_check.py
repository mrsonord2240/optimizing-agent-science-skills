import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest


sys.path.insert(0, str(Path(__file__).parent))
SPEC = importlib.util.spec_from_file_location("routing_check", Path(__file__).with_name("routing_check.py"))
routing = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(routing)

SKILL_MD = ("---\nname: demo-skill\ndescription: Use when testing a demo.\n---\n\n# Demo\n\n"
            "| Your data | Read |\n|---|---|\n| A table | `routes/table.md` |\n| Pairs | `routes/paired.md` |\n\n"
            "After the run:\n\n| Need | Read |\n|---|---|\n| An error | `routes/errors.md` |\n")


def make_skill(root):
    skill = Path(root) / "demo-skill"
    files = {"SKILL.md": SKILL_MD, "routes/table.md": "```bash\npython scripts/table.py in.csv\n```\n",
             "routes/paired.md": "Use the code in `references/paired.md`.\n", "routes/errors.md": "# Errors\n",
             "scripts/table.py": "x\n", "references/paired.md": "y\n", "data/in.csv": "a,b\n1,2\n"}
    for rel, text in files.items():
        (skill / rel).parent.mkdir(parents=True, exist_ok=True)
        (skill / rel).write_text(text, encoding="utf-8")
    return skill


def write_cases(skill, cases):
    path = skill.parent / "cases.json"
    path.write_text(json.dumps(cases), encoding="utf-8")
    return path


class RoutingCheckTests(unittest.TestCase):
    def test_first_table_only(self):
        self.assertEqual(routing.first_table_routes(SKILL_MD), ["routes/table.md", "routes/paired.md"])

    def test_cases_default_expect_and_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = make_skill(tmp)
            data = str(skill / "data")
            good = [{"route": "routes/table.md", "request": "Analyse my table.", "data": data},
                    {"route": "routes/paired.md", "request": "Analyse my pairs.", "data": data}]
            cases = routing.load_cases(skill, write_cases(skill, good))
            self.assertEqual([c["expect"] for c in cases], ["scripts/table.py", None])
            with self.assertRaises(SystemExit) as missing:
                routing.load_cases(skill, write_cases(skill, good[:1]))
            self.assertIn("no case for first-table route routes/paired.md", str(missing.exception))

    def test_cases_reject_leading_request_and_empty_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = make_skill(tmp)
            (skill / "empty").mkdir()
            (skill / "empty" / "in.csv").touch()
            bad = [{"route": "routes/table.md", "request": "Run table.py on my table.", "data": str(skill / "data")},
                   {"route": "routes/paired.md", "request": "Analyse my pairs.", "data": str(skill / "empty")}]
            with self.assertRaises(SystemExit) as rejected:
                routing.load_cases(skill, write_cases(skill, bad))
            self.assertIn("a user would not", str(rejected.exception))
            self.assertIn("no empty file", str(rejected.exception))

    def test_routes_named_in_order(self):
        files = ["errors.md", "paired.md", "table.md"]
        self.assertEqual(routing.routes_named("cat /s/routes/paired.md; cat /s/routes/table.md", files),
                         ["paired.md", "table.md"])
        self.assertEqual(routing.routes_named("cd /s/routes; cat table.md", files), ["table.md"])
        self.assertEqual(routing.routes_named("cat /s/routes/*.md", files), ["*.md"])
        self.assertEqual(routing.routes_named("cat /s/SKILL.md; head data/table.md", files), [])

    def test_reading_a_script_is_not_running_it(self):
        run = routing.RUNNER + re.escape("table.py")
        self.assertIsNone(re.search(run, "cat /s/scripts/table.py"))
        self.assertIsNotNone(re.search(run, "cd /s && python scripts/table.py in.csv"))
        self.assertIsNotNone(re.search(routing.RUNNER + re.escape("de.R"), "source('/s/scripts/de.R')"))


if __name__ == "__main__":
    unittest.main()
