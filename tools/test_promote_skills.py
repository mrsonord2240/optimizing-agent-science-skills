import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("promote_skills.py")
SPEC = importlib.util.spec_from_file_location("promote_skills", MODULE_PATH)
promote = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(promote)


def git(repo, *args):
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True,
        encoding="utf-8",
    ).stdout.strip()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def skill_text(name, extra=""):
    return (
        "---\n"
        f"name: {name}\n"
        "category: Data Analysis\n"
        "license: MIT\n"
        "author: GPTomics\n"
        "---\n"
        f"# {name}\n{extra}"
    )


class PromotionFixture:
    def __init__(self, root):
        self.root = Path(root)
        self.records = self.root / "records"
        self.upstream = self.records / "external" / "GPTomics__bioSkills"
        self.provider = self.root / "provider"
        self.holds = self.records / "config" / "marketplace_submission_holds.json"
        self.records.mkdir()
        self._init_repo(self.upstream)
        self._init_repo(self.provider)
        write_json(self.holds, {"schema_version": 1, "holds": []})

    @staticmethod
    def _init_repo(path):
        path.mkdir(parents=True)
        git(path, "init", "-b", "main")
        git(path, "config", "user.email", "tests@example.com")
        git(path, "config", "user.name", "Promotion Tests")

    def add_upstream_skill(self, skill_id, folder=None, extra=""):
        folder = folder or f"data/{skill_id}"
        path = self.upstream / folder / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(skill_text(skill_id, extra), encoding="utf-8")
        return folder

    def commit_upstream(self):
        git(self.upstream, "add", ".")
        git(self.upstream, "commit", "-m", "upstream")
        return git(self.upstream, "rev-parse", "HEAD")

    def add_provider_skill(self, skill_id, extra=""):
        path = self.provider / "skills" / skill_id / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(skill_text(skill_id, extra), encoding="utf-8")

    def commit_provider(self, message="provider"):
        git(self.provider, "add", ".")
        git(self.provider, "commit", "-m", message)
        return git(self.provider, "rev-parse", "HEAD")

    def write_metadata(self, existing_rows, remaining, excluded=None):
        write_json(self.provider / "PROVENANCE.json", {
            "schema_version": 1,
            "generated": "2026-09-24",
            "note": "keep me",
            "sources": {"legacy": {"keep": True}},
            "skills": existing_rows,
        })
        write_json(self.provider / "REMAINING.json", {
            "schema_version": 1,
            "generated": "2026-09-24",
            "source": "GPTomics/bioSkills@old",
            "reconciliation": {},
            "remaining": remaining,
            "excluded": excluded or [],
            "out_of_scope": [],
        })
        (self.provider / "REMAINING.md").write_text("old\n", encoding="utf-8")
        self.commit_provider("metadata")

    def audit(self, skill_id, commit, *, deployable=True, p0=False, veto=False,
              supersedes=None, version=None):
        version = version or f"mrsonord2240-optimized-scientific-skills@{commit[:7]}"
        base = self.records / "audits" / "skills" / skill_id / version
        write_json(base / "record.json", {
            "skill_id": skill_id,
            "version": version,
            "source": {
                "repository": "mrsonord2240/optimized-scientific-skills",
                "commit": commit,
                "path": f"skills/{skill_id}",
            },
            "audit": {"audited_on": "2026-09-27"},
            "supersedes": supersedes,
        })
        write_json(base / "report.json", {
            "meta": {"category": "Data Analysis", "evaluated_on": "2026-09-27"},
            "veto_gates": {
                "skill_veto": {"gate": "FAIL" if veto else "PASS"},
                "research_veto": {"gate": "PASS"},
            },
            "final": {
                "score": 94 if deployable else 70,
                "grade": "Production Ready" if deployable else "Beta Only",
                "deployable": deployable,
            },
            "recommendations": ([{"priority": "P0"}] if p0 else []),
        })
        return version


class PromotionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.fixture = PromotionFixture(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_latest_audit_follows_supersedes_chain(self):
        f = self.fixture
        f.add_upstream_skill("new-skill")
        f.commit_upstream()
        f.add_provider_skill("new-skill")
        old_commit = f.commit_provider("old")
        old = f.audit("new-skill", old_commit, deployable=False, version="old")
        new = f.audit("new-skill", old_commit, supersedes=old, version="new")

        latest = promote.load_latest_audits(f.records)["new-skill"]

        self.assertEqual(latest["version"], new)
        self.assertTrue(latest["report"]["final"]["deployable"])

    def test_append_only_reconciliation_preserves_existing_row_and_skill_bytes(self):
        f = self.fixture
        old_path = f.add_upstream_skill("old-skill")
        new_path = f.add_upstream_skill("new-skill")
        upstream_commit = f.commit_upstream()
        f.add_provider_skill("old-skill", "fixed old\n")
        f.add_provider_skill("new-skill", "fixed new\n")
        audited_commit = f.commit_provider("audited bytes")
        existing = {
            "id": "old-skill", "upstream_path": old_path, "score": 91,
            "grade": "Production Ready", "deployable": True, "open_p0": 0,
            "fix_pass": "done", "reaudit": "not needed", "marketplace_ready": False,
            "custom_field": "must survive",
        }
        f.write_metadata(
            [existing],
            [{"id": "new-skill", "upstream_path": new_path}],
            [{"id": "new-skill", "upstream_path": new_path, "score": 70}],
        )
        f.audit("new-skill", audited_commit)
        before = promote.tree_fingerprint(f.provider, "main", "skills")
        old_bytes = (f.provider / "skills" / "old-skill" / "SKILL.md").read_bytes()
        new_bytes = (f.provider / "skills" / "new-skill" / "SKILL.md").read_bytes()

        result = promote.build_metadata(
            f.records, f.provider, f.upstream, upstream_commit, f.holds,
        )

        rows = {row["id"]: row for row in result.provenance["skills"]}
        self.assertEqual(rows["old-skill"]["custom_field"], "must survive")
        self.assertEqual(rows["old-skill"]["score"], 91)
        self.assertFalse(rows["old-skill"]["marketplace_ready"])
        self.assertEqual(rows["new-skill"]["reaudit"], "not needed")
        self.assertEqual(rows["new-skill"]["relative_to_upstream"], "modified")
        self.assertEqual(result.remaining["remaining"], [])
        self.assertEqual(result.remaining["excluded"], [])

        promote.write_metadata(f.provider, result)
        self.assertEqual(before, promote.tree_fingerprint(f.provider, "main", "skills"))
        self.assertEqual(
            old_bytes, (f.provider / "skills" / "old-skill" / "SKILL.md").read_bytes()
        )
        self.assertEqual(
            new_bytes, (f.provider / "skills" / "new-skill" / "SKILL.md").read_bytes()
        )
        f.commit_provider("reconciled metadata")
        repeated = promote.build_metadata(
            f.records, f.provider, f.upstream, upstream_commit, f.holds,
        )
        self.assertEqual(result.provenance, repeated.provenance)
        self.assertEqual(result.remaining, repeated.remaining)
        self.assertEqual(result.remaining_md, repeated.remaining_md)

    def test_new_skill_requires_provider_ancestor_and_exact_audited_bytes(self):
        f = self.fixture
        path = f.add_upstream_skill("new-skill")
        upstream_commit = f.commit_upstream()
        f.add_provider_skill("new-skill", "audited\n")
        audited_commit = f.commit_provider("audited")
        f.write_metadata([], [{"id": "new-skill", "upstream_path": path}])
        (f.provider / "skills" / "new-skill" / "SKILL.md").write_text(
            skill_text("new-skill", "changed after audit\n"), encoding="utf-8")
        changed_commit = f.commit_provider("changed")
        f.audit("new-skill", audited_commit)

        result = promote.build_metadata(
            f.records, f.provider, f.upstream, upstream_commit, f.holds,
        )

        self.assertEqual(result.provenance["skills"], [])
        self.assertIn("bytes differ", "\n".join(result.messages))
        self.assertEqual(git(f.provider, "rev-parse", "main"), changed_commit)

        git(f.provider, "checkout", "-b", "unmerged", audited_commit)
        (f.provider / "branch.txt").write_text("branch\n", encoding="utf-8")
        unmerged_commit = f.commit_provider("unmerged")
        git(f.provider, "checkout", "main")
        f.audit("new-skill", unmerged_commit, version="unmerged")
        old_version = f"mrsonord2240-optimized-scientific-skills@{audited_commit[:7]}"
        record = f.records / "audits" / "skills" / "new-skill" / "unmerged" / "record.json"
        data = json.loads(record.read_text(encoding="utf-8"))
        data["supersedes"] = old_version
        write_json(record, data)

        result = promote.build_metadata(
            f.records, f.provider, f.upstream, upstream_commit, f.holds,
        )
        self.assertEqual(result.provenance["skills"], [])
        self.assertIn("not an ancestor", "\n".join(result.messages))

    def test_new_skill_rejects_p0_veto_and_non_deployable_latest_audits(self):
        for suffix, kwargs, expected in [
            ("p0", {"p0": True}, "open P0"),
            ("veto", {"veto": True}, "veto"),
            ("failed", {"deployable": False}, "not deployable"),
        ]:
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as tmp:
                f = PromotionFixture(tmp)
                sid = f"new-{suffix}"
                path = f.add_upstream_skill(sid)
                upstream_commit = f.commit_upstream()
                f.add_provider_skill(sid)
                commit = f.commit_provider()
                f.write_metadata([], [{"id": sid, "upstream_path": path}])
                f.audit(sid, commit, **kwargs)
                result = promote.build_metadata(
                    f.records, f.provider, f.upstream, upstream_commit, f.holds,
                )
                self.assertEqual(result.provenance["skills"], [])
                self.assertIn(expected, "\n".join(result.messages))

    def test_cross_repository_classification_accepts_only_declaration_additions(self):
        f = self.fixture
        path = f.add_upstream_skill("declarations", extra="same\n")
        upstream_commit = f.commit_upstream()
        f.add_provider_skill("declarations", "same\n")
        provider_commit = f.commit_provider()
        kind, changed = promote.classify_across_repositories(
            f.provider, provider_commit, "skills/declarations",
            f.upstream, upstream_commit, path,
        )
        self.assertEqual((kind, changed), ("unmodified", []))

        provider_skill = f.provider / "skills" / "declarations" / "SKILL.md"
        provider_skill.write_text(
            skill_text("declarations", "same\n").replace(
                "author: GPTomics\n", "author: GPTomics\nnew_field: real change\n"
            ),
            encoding="utf-8",
        )
        modified_commit = f.commit_provider("modified")
        kind, changed = promote.classify_across_repositories(
            f.provider, modified_commit, "skills/declarations",
            f.upstream, upstream_commit, path,
        )
        self.assertEqual(kind, "modified")
        self.assertEqual(changed, ["SKILL.md"])


if __name__ == "__main__":
    unittest.main()
