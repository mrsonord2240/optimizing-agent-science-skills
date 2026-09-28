import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = Path(__file__).with_name("publish_audits.py")
SPEC = importlib.util.spec_from_file_location("publish_audits", MODULE_PATH)
publish = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publish)


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


class ModularPublicationTests(unittest.TestCase):
    def make_run(self, root):
        run = root / "raw" / "sample-skill" / "initial-opt10"
        write_json(run / "report.json", {
            "meta": {
                "skill_name": "sample-skill",
                "evaluated_on": "2026-09-28",
                "evaluator_version": "skill-auditor@1.0",
                "category": "Data Analysis",
            },
            "veto_gates": {"skill_veto": {"gate": "PASS"}, "research_veto": {"gate": "PASS"}},
            "static_score": {"subtotal": 80, "max": 100, "categories": {}},
            "dynamic_score": {"execution_avg": 80, "max": 100, "assertion_pass_rate": {"passed": 1, "total": 1}, "inputs": []},
            "final": {"score": 80, "max": 100, "grade": "Beta Only", "grade_symbol": "B", "deployable": False, "veto_override": False},
            "key_strengths": [],
            "recommendations": [{"priority": "P1", "title": "Fix", "observed_in": [1], "problem": "p", "root_cause": "r", "fix": "f"}],
        })
        (run / "viewer.md").write_text("# Viewer\n", encoding="utf-8")
        write_json(run / "source-identity.json", {
            "origin": {
                "repository": "GPTomics/bioSkills",
                "commit": "d91ed3d563019e649dc854c56ccd62551359488a",
                "path": "sample/sample-skill",
                "subtree": "1" * 40,
            },
            "candidate": {
                "branch": "optimize/sample",
                "commit": "2" * 40,
                "content_sha256": "3" * 64,
                "path": str(run / "candidate"),
            },
            "files": [{"path": "SKILL.md", "sha256": "4" * 64, "bytes": 10}],
        })
        (run / "run_cases.py").write_text("print('ok')\n", encoding="utf-8")
        (run / "data").mkdir()
        (run / "data" / "input.tsv").write_text("x\t1\n", encoding="utf-8")
        return run

    def test_modular_run_publishes_exact_report_identity_and_selected_artifacts(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run = self.make_run(root)
            records = root / "records"

            version, count = publish.publish_modular(
                str(records), "sample-skill", str(run), ["run_cases.py", "data/input.tsv"]
            )

            target = records / "audits" / "skills" / "sample-skill" / version
            record = json.loads((target / "record.json").read_text(encoding="utf-8"))
            self.assertEqual(version, "candidate@333333333333-initial-opt10")
            self.assertEqual(count, 2)
            self.assertEqual(record["candidate"]["identity"], "3" * 64)
            self.assertEqual(record["source"]["repository"], "GPTomics/bioSkills")
            self.assertEqual((target / "report.json").read_bytes(), (run / "report.json").read_bytes())
            self.assertEqual((target / "source-identity.json").read_bytes(), (run / "source-identity.json").read_bytes())
            self.assertTrue((target / "scripts" / "run_cases.py").is_file())
            self.assertTrue((target / "scripts" / "data" / "input.tsv").is_file())
            viewer = (target / "viewer.md").read_text(encoding="utf-8")
            self.assertIn("Audited working candidate", viewer)
            self.assertIn("Test inputs and provenance are described", viewer)
            self.assertNotIn("Test data are synthetic", viewer)

            repeated = publish.publish_modular(
                str(records), "sample-skill", str(run), ["run_cases.py", "data/input.tsv"]
            )
            self.assertEqual(repeated, (version, 2))

    def test_modular_run_refuses_existing_record_with_different_report(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run = self.make_run(root)
            records = root / "records"
            version, _ = publish.publish_modular(
                str(records), "sample-skill", str(run), ["run_cases.py"]
            )
            report = json.loads((run / "report.json").read_text(encoding="utf-8"))
            report["final"]["score"] = 79
            write_json(run / "report.json", report)

            with self.assertRaisesRegex(SystemExit, "refusing to overwrite"):
                publish.publish_modular(
                    str(records), "sample-skill", str(run), ["run_cases.py"]
                )
            self.assertEqual(
                json.loads((records / "audits" / "skills" / "sample-skill" / version / "report.json").read_text(encoding="utf-8"))["final"]["score"],
                80,
            )

    def test_modular_run_accepts_normalized_identity_field(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run = self.make_run(root)
            identity_path = run / "source-identity.json"
            identity = json.loads(identity_path.read_text(encoding="utf-8"))
            digest = identity["candidate"].pop("content_sha256")
            identity["candidate"]["identity"] = digest
            write_json(identity_path, identity)

            version, _ = publish.publish_modular(
                str(root / "records"), "sample-skill", str(run), []
            )

            self.assertEqual(version, "candidate@333333333333-initial-opt10")


if __name__ == "__main__":
    unittest.main()
