import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("export_bioskills.py")
SPEC = importlib.util.spec_from_file_location("export_bioskills", MODULE_PATH)
export = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(export)


def git(repo, *args):
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True,
        encoding="utf-8",
    ).stdout.strip()


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def row(skill_id, path, **overrides):
    base = {"id": skill_id, "upstream_path": path, "deployable": True, "open_p0": 0,
            "fix_pass": "done", "reaudit": "not needed"}
    base.update(overrides)
    return base


class ExportFixture:
    def __init__(self, root):
        self.provider = root / "provider"
        self.fork = root / "fork"
        origin = root / "origin.git"
        for repo in (self.provider, root / "seed"):
            repo.mkdir()
            git(repo, "init", "-q", "-b", "main")
            self._identify(repo)
        seed = root / "seed"
        write(seed / "cat/old/SKILL.md", "old\n")
        write(seed / "cat/old/stale.md", "stale\n")
        write(seed / "cat/other/SKILL.md", "fork only\n")
        write(seed / "cat/old/run.sh", "echo old\n")
        write(seed / "cat/modes/SKILL.md", "same\n")
        git(seed, "add", "-A")
        git(seed, "update-index", "--chmod=+x", "cat/old/run.sh", "cat/modes/SKILL.md")
        git(seed, "commit", "-q", "-m", "seed")
        git(root, "clone", "-q", "--bare", str(seed), str(origin))
        git(root, "clone", "-q", str(origin), str(self.fork))
        self._identify(self.fork)

    @staticmethod
    def _identify(repo):
        git(repo, "config", "user.name", "Test")
        git(repo, "config", "user.email", "test@example.com")
        git(repo, "config", "core.autocrlf", "false")

    def publish(self, rows, files):
        for path, text in files.items():
            write(self.provider / path, text)
        write(self.provider / "PROVENANCE.json", json.dumps({"skills": rows}))
        git(self.provider, "add", "-A")
        git(self.provider, "commit", "-q", "-m", "shelf")

    def export(self):
        changes, unchanged, skipped = export.build_plan(self.provider, "main", self.fork)
        commit = export.apply_plan(changes, self.provider, "main", self.fork) if changes else None
        return changes, unchanged, skipped, commit


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.fixture = ExportFixture(Path(self.temp.name))

    def tearDown(self):
        self.temp.cleanup()

    def test_exports_exact_trees_and_leaves_other_fork_skills_alone(self):
        fixture = self.fixture
        fixture.publish(
            [row("bio-old", "cat/old"), row("bio-new", "cat/new"),
             row("bio-wip", "cat/wip", reaudit="needed")],
            {"skills/bio-old/SKILL.md": "new bytes\r\n",
             "skills/bio-new/SKILL.md": "added\n",
             "skills/bio-new/scripts/run.sh": "echo hi\n",
             "skills/bio-wip/SKILL.md": "unfinished\n"},
        )
        changes, unchanged, skipped, commit = fixture.export()
        self.assertEqual([(c["id"], c["kind"]) for c in changes],
                         [("bio-new", "added"), ("bio-old", "updated")])
        self.assertEqual((unchanged, skipped), ([], ["bio-wip"]))
        self.assertEqual(git(fixture.fork, "rev-parse", "HEAD:cat/new"),
                         git(fixture.provider, "rev-parse", "main:skills/bio-new"))
        self.assertEqual(git(fixture.fork, "rev-parse", "HEAD:cat/old/SKILL.md"),
                         git(fixture.provider, "rev-parse", "main:skills/bio-old/SKILL.md"))
        self.assertFalse((fixture.fork / "cat/old/run.sh").exists())
        self.assertFalse((fixture.fork / "cat/old/stale.md").exists())
        self.assertFalse((fixture.fork / "cat/wip").exists())
        self.assertEqual((fixture.fork / "cat/other/SKILL.md").read_text(), "fork only\n")
        self.assertEqual((fixture.fork / "cat/new/scripts/run.sh").read_text(), "echo hi\n")
        self.assertEqual(git(fixture.fork, "status", "--porcelain"), "")
        self.assertIn("Update 2 skills", git(fixture.fork, "log", "-1", "--format=%s"))

        again, unchanged, _, second = fixture.export()
        self.assertEqual((again, second), ([], None))
        self.assertEqual(unchanged, ["bio-new", "bio-old"])
        self.assertEqual(git(fixture.fork, "rev-parse", "HEAD"), commit)

    def test_keeps_fork_executable_bits_and_ignores_mode_only_differences(self):
        fixture = self.fixture
        fixture.publish(
            [row("bio-old", "cat/old"), row("bio-modes", "cat/modes")],
            {"skills/bio-old/SKILL.md": "new\n", "skills/bio-old/run.sh": "echo new\n",
             "skills/bio-modes/SKILL.md": "same\n"},
        )
        changes, unchanged, _, _ = fixture.export()
        self.assertEqual([c["id"] for c in changes], ["bio-old"])
        self.assertEqual(unchanged, ["bio-modes"])
        listed = git(fixture.fork, "ls-tree", "-r", "HEAD", "cat/old").splitlines()
        self.assertIn("100755", next(line for line in listed if line.endswith("run.sh")))
        self.assertIn("100644", next(line for line in listed if line.endswith("SKILL.md")))
        self.assertEqual(git(fixture.fork, "show", "HEAD:cat/old/run.sh"), "echo new")

    def test_rejects_unsafe_paths_and_collisions(self):
        fixture = self.fixture
        fixture.publish([row("bio-a", "../escape")], {"skills/bio-a/SKILL.md": "a\n"})
        with self.assertRaises(SystemExit):
            export.build_plan(fixture.provider, "main", fixture.fork)
        fixture.publish([row("bio-a", "cat/same"), row("bio-b", "cat/same")],
                        {"skills/bio-b/SKILL.md": "b\n"})
        with self.assertRaises(SystemExit):
            export.build_plan(fixture.provider, "main", fixture.fork)

    def test_apply_refuses_a_dirty_or_diverged_fork(self):
        fixture = self.fixture
        write(fixture.fork / "cat/other/SKILL.md", "hand edit\n")
        with self.assertRaises(SystemExit):
            export._assert_safe_fork(fixture.fork, "main")
        git(fixture.fork, "commit", "-q", "-am", "local only")
        with self.assertRaises(SystemExit):
            export._assert_safe_fork(fixture.fork, "main")


if __name__ == "__main__":
    unittest.main()
