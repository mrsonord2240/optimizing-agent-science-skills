#!/usr/bin/env python3
"""Focused unit tests for the direct OpenRouter Mercury launcher."""

from __future__ import annotations

import json
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_mercury_worker as worker


def completed_result(summary: str = "done") -> dict[str, object]:
    return {
        "status": "completed",
        "summary": summary,
        "evidence": [],
        "files_examined": ["README.md"],
        "issues": [],
        "recommended_next_action": "review",
    }


class MercuryWorkerTests(unittest.TestCase):
    def test_process_environment_key_wins(self) -> None:
        self.assertEqual(
            worker.resolve_openrouter_key({"OPENROUTER_API_KEY": " test-key "}),
            "test-key",
        )

    def test_missing_key_raises_for_explicit_environment(self) -> None:
        with self.assertRaises(worker.LauncherError):
            worker.resolve_openrouter_key({})

    def test_redact_removes_secret(self) -> None:
        self.assertEqual(
            worker.redact("prefix secret-value suffix", "secret-value"),
            "prefix [REDACTED] suffix",
        )

    def test_workspace_rejects_absolute_and_escaping_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = worker.ReadOnlyWorkspace(Path(directory))
            with self.assertRaises(worker.LauncherError):
                workspace._resolve("../outside.txt")
            with self.assertRaises(worker.LauncherError):
                workspace._resolve("C:\\Windows\\win.ini")

    def test_read_and_search_tools_are_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                "alpha\nbeta alpha\ngamma\n", encoding="utf-8"
            )
            workspace = worker.ReadOnlyWorkspace(root)
            read = workspace.read_text_file(
                {"path": "README.md", "start_line": 2, "max_lines": 1}
            )
            self.assertEqual(read["content"], "2: beta alpha")
            self.assertTrue(read["truncated"])
            search = workspace.search_text(
                {"query": "alpha", "file_glob": "*.md", "max_results": 1}
            )
            self.assertEqual(len(search["matches"]), 1)
            self.assertTrue(search["limit_reached"])

    def test_payload_contains_tools_schema_and_no_secret(self) -> None:
        payload = worker.build_payload(
            model=worker.DEFAULT_MODEL,
            messages=[{"role": "user", "content": "task"}],
            effort="low",
            max_output_tokens=1000,
            session_id="test-session",
        )
        self.assertEqual(payload["model"], worker.DEFAULT_MODEL)
        self.assertEqual(payload["parallel_tool_calls"], False)
        self.assertEqual(payload["response_format"]["type"], "json_schema")
        self.assertEqual(len(payload["tools"]), 3)
        self.assertNotIn("secret", json.dumps(payload).lower())

    def test_agent_loop_executes_tool_then_returns_structured_result(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Test\n", encoding="utf-8")
            workspace = worker.ReadOnlyWorkspace(root)
            calls: list[dict[str, object]] = []

            def fake_request(payload, api_key, timeout_seconds, max_retries):
                calls.append(payload)
                if len(calls) == 1:
                    message = {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": "call-1",
                                "type": "function",
                                "function": {
                                    "name": "read_text_file",
                                    "arguments": json.dumps({"path": "README.md"}),
                                },
                            }
                        ],
                    }
                    finish = "tool_calls"
                else:
                    message = {
                        "role": "assistant",
                        "content": json.dumps(completed_result()),
                    }
                    finish = "stop"
                return {
                    "id": f"response-{len(calls)}",
                    "model": worker.DEFAULT_MODEL,
                    "choices": [{"message": message, "finish_reason": finish}],
                    "usage": {
                        "prompt_tokens": 10,
                        "completion_tokens": 5,
                        "cost": 0.00001,
                    },
                }

            result = worker.run_agent_loop(
                workspace=workspace,
                task_text="Read README.md",
                api_key="secret",
                model=worker.DEFAULT_MODEL,
                effort="low",
                max_turns=3,
                max_output_tokens=1000,
                max_cost_usd=0.01,
                request_timeout_seconds=10,
                max_retries=0,
                deadline=time.monotonic() + 10,
                request_function=fake_request,
            )
            self.assertEqual(result["turns"], 2)
            self.assertEqual(result["usage"]["prompt_tokens"], 20)
            self.assertEqual(result["structured_result"]["status"], "completed")
            self.assertEqual(workspace.trace[0]["name"], "read_text_file")
            self.assertEqual(calls[1]["messages"][-1]["role"], "tool")

    def test_structured_result_rejects_extra_keys(self) -> None:
        value = completed_result()
        value["unexpected"] = True
        with self.assertRaises(worker.LauncherError):
            worker.validate_structured_result(value)

    def test_json_response_tolerates_fence_decoration(self) -> None:
        expected = {"status": "completed"}
        self.assertEqual(
            worker.parse_json_response('```json\n{"status":"completed"}\n```'),
            expected,
        )
        self.assertEqual(
            worker.parse_json_response('{"status":"completed"}\n```'),
            expected,
        )


if __name__ == "__main__":
    unittest.main()
