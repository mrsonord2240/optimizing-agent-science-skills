import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = Path(__file__).with_name("skill_preflight.py")
SPEC = importlib.util.spec_from_file_location("skill_preflight", MODULE_PATH)
preflight = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preflight)

GOOD_SKILL_MD = (b"---\nname: demo-skill\ndescription: Demo.\nlicense: MIT\n"
                 b"category: Data Analysis\nauthor: Someone\n---\n\nBody.\n")


def make_skill(root, files):
    skill = Path(root) / "demo-skill"
    for rel, data in files.items():
        path = skill / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return str(skill)


class PreflightTests(unittest.TestCase):
    def test_identity_is_sha256_manifest_v1(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = {"SKILL.md": GOOD_SKILL_MD, "LICENSE": b"MIT\n", "b/Z.py": b"x\n", "b/a.py": b"y\n"}
            skill = make_skill(tmp, files)
            rows = sorted(files.items(), key=lambda kv: kv[0].encode("utf-8"))
            text = "\n".join(f"{p}\t{len(d)}\t{hashlib.sha256(d).hexdigest()}" for p, d in rows)
            self.assertEqual(preflight.identity(skill)[0], hashlib.sha256(text.encode()).hexdigest())

    def test_clean_skill_passes_offline(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = preflight.check(make_skill(tmp, {"SKILL.md": GOOD_SKILL_MD, "LICENSE": b"MIT\n"}), None, None)
            self.assertEqual(result["fail"], [])
            self.assertEqual(result["warn"], [])

    def test_hygiene_and_frontmatter_failures(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad_md = GOOD_SKILL_MD.replace(b"category: Data Analysis\n", b"").replace(b"\n", b"\r\n")
            skill = make_skill(tmp, {"SKILL.md": bad_md, "LICENSE": b"MIT\n", "scripts/LICENSE": b"MIT\n",
                                     "scripts/__pycache__/x.pyc": b"\0", "references/a.md": b"\xef\xbb\xbfhi\n"})
            fails = " | ".join(preflight.check(skill, None, None)["fail"])
            for expected in ("CRLF", "nested license", "bytecode cache", "UTF-8 BOM", "SKILL.md missing"):
                self.assertIn(expected, fails)

    def test_missing_category_fails_and_missing_license_warns(self):
        with tempfile.TemporaryDirectory() as tmp:
            md = GOOD_SKILL_MD.replace(b"category: Data Analysis\n", b"").replace(b"license: MIT\n", b"")
            result = preflight.check(make_skill(tmp, {"SKILL.md": md}), None, None)
            self.assertTrue(any("category" in f for f in result["fail"]))
            self.assertTrue(any("license" in w for w in result["warn"]))
            self.assertTrue(any("LICENSE" in w for w in result["warn"]))

    def test_collisions(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = make_skill(tmp, {"SKILL.md": GOOD_SKILL_MD, "LICENSE": b"MIT\n"})
            self.assertTrue(preflight.check(skill, {"demo-skill"}, set())["fail"])
            self.assertTrue(preflight.check(skill, set(), {"demo-skill"})["fail"])
            near = preflight.check(skill, {"demo-skill-plus"}, set())
            self.assertEqual(near["fail"], [])
            self.assertTrue(near["warn"])


if __name__ == "__main__":
    unittest.main()
