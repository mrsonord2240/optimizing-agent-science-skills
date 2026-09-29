import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


MODULE_PATH = Path(__file__).with_name("bind_candidate_audit.py")
SPEC = importlib.util.spec_from_file_location("bind_candidate_audit", MODULE_PATH)
bind = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bind)


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


class CandidateBindingTests(unittest.TestCase):
    def make_fixture(self, root):
        provider = root / "provider"
        provider.mkdir()
        git(provider, "init", "-b", "main")
        git(provider, "config", "user.email", "test@example.com")
        git(provider, "config", "user.name", "Test")
        candidate = root / "candidate"
        candidate.mkdir()
        (candidate / "SKILL.md").write_bytes(b"---\nname: sample-skill\n---\n")
        (candidate / "script.py").write_bytes(b"print('ok')\n")
        provider_skill = provider / "skills" / "sample-skill"
        provider_skill.parent.mkdir(parents=True)
        subprocess.run(["git", "-C", str(provider), "add", "."], check=True)
        provider_skill.mkdir()
        for path in candidate.iterdir():
            (provider_skill / path.name).write_bytes(path.read_bytes())
        subprocess.run(["git", "-C", str(provider), "add", "."], check=True)
        subprocess.run(["git", "-C", str(provider), "commit", "-m", "candidate"], check=True, stdout=subprocess.PIPE)
        commit = git(provider, "rev-parse", "HEAD")

        records = root / "records"
        version = "candidate@" + "3" * 12 + "-reaudit"
        audit = records / "audits" / "skills" / "sample-skill" / version
        audit.mkdir(parents=True)
        write_json(audit / "record.json", {
            "skill_id": "sample-skill",
            "version": version,
            "source": {
                "repository": "GPTomics/bioSkills",
                "commit": bind.ORIGIN_COMMIT,
                "path": "sample/sample-skill",
                "author": "GPTomics",
                "author_url": "https://github.com/GPTomics",
                "license": "MIT",
            },
            "candidate": {"identity": "3" * 64, "path": str(candidate)},
            "audit": {"audited_on": "2026-09-28"},
            "supersedes": None,
            "files": {"report": "report.json", "viewer": "viewer.md", "source_identity": "source-identity.json"},
        })
        write_json(audit / "report.json", {"meta": {"skill_name": "sample-skill"}, "final": {"deployable": True}})
        write_json(audit / "source-identity.json", {"candidate": {"identity": "3" * 64}})
        (audit / "viewer.md").write_text("# Sample audit\n\nBody.\n", encoding="utf-8")
        return records, provider, candidate, version, commit, audit

    def test_binds_byte_identical_provider_commit_without_rewriting_report(self):
        with tempfile.TemporaryDirectory() as temporary:
            records, provider, _, candidate_version, commit, audit = self.make_fixture(Path(temporary))
            original_report = (audit / "report.json").read_bytes()

            version, target = bind.bind_candidate_audit(
                records, provider, "sample-skill", candidate_version, commit
            )

            self.assertEqual(version, f"mrsonord2240-optimized-scientific-skills@{commit[:7]}")
            record = json.loads((target / "record.json").read_text(encoding="utf-8"))
            binding = json.loads((target / "binding.json").read_text(encoding="utf-8"))
            self.assertEqual(record["source"]["commit"], commit)
            self.assertEqual(record["supersedes"], candidate_version)
            self.assertEqual((target / "report.json").read_bytes(), original_report)
            self.assertEqual(binding["file_count"], 2)
            self.assertFalse(binding["report_reexecuted"])
            self.assertIn("match audited candidate", (target / "viewer.md").read_text(encoding="utf-8"))
            self.assertEqual(
                bind.bind_candidate_audit(records, provider, "sample-skill", candidate_version, commit),
                (version, target),
            )

    def test_rejects_provider_byte_mismatch(self):
        with tempfile.TemporaryDirectory() as temporary:
            records, provider, candidate, candidate_version, commit, _ = self.make_fixture(Path(temporary))
            (candidate / "script.py").write_bytes(b"print('changed')\n")

            with self.assertRaisesRegex(SystemExit, "bytes differ"):
                bind.bind_candidate_audit(
                    records, provider, "sample-skill", candidate_version, commit
                )


if __name__ == "__main__":
    unittest.main()
