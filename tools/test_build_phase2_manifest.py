"""Focused tests for the evidence predicates used by build_phase2_manifest.py."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("build_phase2_manifest.py")
SPEC = importlib.util.spec_from_file_location("phase2_manifest", MODULE_PATH)
assert SPEC and SPEC.loader
MANIFEST = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MANIFEST
SPEC.loader.exec_module(MANIFEST)


class Phase2ManifestTests(unittest.TestCase):
    def test_frontmatter_name_requires_yaml_header(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "SKILL.md"
            path.write_text("---\nname: bio-example\n---\nbody\n", encoding="utf-8")
            self.assertEqual(MANIFEST.parse_frontmatter_name(path), "bio-example")
            path.write_text("name: bio-example\n", encoding="utf-8")
            self.assertIsNone(MANIFEST.parse_frontmatter_name(path))

    def test_checkpoint_rejects_wrong_worktree_and_accepts_template(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint = Path(temporary) / "CHECKPOINT.md"
            checkpoint.write_text(
                "# bio-example — final pass checkpoint\n\n"
                "Worktree `F:\\OpenScience\\wt\\right-one`\n\n"
                "## Fixed this phase\n- fixed\n\n"
                "## Still blocked (needs a decision)\n- none\n\n"
                "## Ran, not previously verified\n- ran\n",
                encoding="utf-8",
            )
            state, details = MANIFEST.validate_checkpoint(checkpoint, "bio-example", Path("right-one"))
            self.assertEqual(state, "ok")
            self.assertEqual(details["worktree_reference"], "matched")
            state, _ = MANIFEST.validate_checkpoint(checkpoint, "bio-example", Path("other-one"))
            self.assertEqual(state, "bad")
            checkpoint.write_text(checkpoint.read_text(encoding="utf-8") + "\n## Result\n- extra\n", encoding="utf-8")
            state, _ = MANIFEST.validate_checkpoint(checkpoint, "bio-example", Path("right-one"))
            self.assertEqual(state, "ok")

    def test_since_is_start_of_recovery_day_not_current_clock_time(self) -> None:
        self.assertEqual(MANIFEST.SINCE, "2026-09-21T00:00:00-07:00")

    def test_phase2_report_needs_false_flag_exact_tip_and_folder(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            report = Path(temporary) / "report.json"
            report.write_text(
                json.dumps({"source": "repo@abc123d:folder/path", "meta": {"auditor_independent": False}}),
                encoding="utf-8",
            )
            folder = Path("folder/path")
            self.assertTrue(MANIFEST.report_audits_tip(report, "abc123def456", folder))
            self.assertFalse(MANIFEST.report_audits_tip(report, "def456abc123", folder))
            self.assertFalse(MANIFEST.report_audits_tip(report, "abc123def456", Path("other/path")))
            report.write_text(json.dumps({"source": "repo@abc123d:folder/path", "meta": {}}), encoding="utf-8")
            self.assertFalse(MANIFEST.report_audits_tip(report, "abc123def456", folder))

    def test_preserve_tracker_keeps_a_valid_existing_backup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            tracker, backup = root / "tracker.json", root / "backup.json"
            tracker.write_text('[{"id": "old"}]', encoding="utf-8")
            backup.write_text('[{"id": "original"}]', encoding="utf-8")
            self.assertEqual(MANIFEST.preserve_tracker_once(tracker, backup), "backup-already-valid")
            self.assertEqual(json.loads(backup.read_text(encoding="utf-8")), [{"id": "original"}])


if __name__ == "__main__":
    unittest.main()
