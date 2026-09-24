import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import test from "node:test";

const root = new URL("..", import.meta.url).pathname.replace(/^\//, "");
const source = String.raw`
import importlib.util
import json
from pathlib import Path

root = Path(r"${root}")
ids = {
    "bio-causal-genomics-mediation-analysis",
    "bio-causal-genomics-pleiotropy-detection",
}
for name in ("promote_skills", "marketplace_manifests"):
    spec = importlib.util.spec_from_file_location(name, root / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    holds = module.load_marketplace_holds(root / "config" / "marketplace_submission_holds.json")
    assert set(holds) == ids
    assert all({"marketplace_submission", "marketplace_intake"}.issubset(v["scope"])
               for v in holds.values())
    if name == "promote_skills":
        for hold in holds.values():
            row = {"grade": "Production Ready", "fix_pass": "done", "reaudit": "not needed"}
            module.set_marketplace_status(row, hold)
            assert row["marketplace_ready"] is False
            assert row["marketplace_hold"] == hold
print(json.dumps(sorted(ids)))
`;

test("both marketplace paths load the two exact duplicate-ID holds", () => {
  const output = execFileSync("python", ["-c", source], { encoding: "utf8" });
  assert.deepEqual(JSON.parse(output), [
    "bio-causal-genomics-mediation-analysis",
    "bio-causal-genomics-pleiotropy-detection",
  ]);
});

test("default and targeted paths keep held IDs out of manifests and intake", () => {
  const output = execFileSync("python", ["-c", String.raw`
import contextlib
import importlib.util
import io
import json
import sys
import tempfile
from pathlib import Path

root = Path(r"${root}")
spec = importlib.util.spec_from_file_location("marketplace_manifests", root / "tools" / "marketplace_manifests.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
held = [
    "bio-causal-genomics-mediation-analysis",
    "bio-causal-genomics-pleiotropy-detection",
]
with tempfile.TemporaryDirectory() as tmp:
    shelf = Path(tmp) / "shelf"
    shelf.mkdir()
    (shelf / "PROVENANCE.json").write_text(json.dumps({"skills": [
        {"id": sid, "marketplace_ready": True, "upstream_path": "causal-genomics/x"}
        for sid in held
    ]}), encoding="utf-8")
    module.SHELF = str(shelf)
    module.marketplace_ids = lambda: set()
    module.git = lambda *args: ""
    outputs = []
    for targeted in (False, True):
        sys.argv = ["marketplace_manifests.py", "--out", str(Path(tmp) / ("targeted" if targeted else "default")),
                    "--intake", str(Path(tmp) / "must-not-run")]
        if targeted:
            sys.argv += ["--skill", held[0], "--skill", held[1]]
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            module.main()
        outputs.append(captured.getvalue())
assert all("wrote 0 manifests" in result for result in outputs)
assert outputs[1].count("submission hold:") == 2
print(json.dumps({"intake_ran": any("INTAKE REJECTED" in result for result in outputs), "outputs": outputs}))
`], { encoding: "utf8" });
  const result = JSON.parse(output);
  assert.equal(result.intake_ran, false);
  assert.match(result.outputs[1], /bio-causal-genomics-mediation-analysis/);
  assert.match(result.outputs[1], /bio-causal-genomics-pleiotropy-detection/);
});

test("manifest category comes from Skill frontmatter and is fail-closed", () => {
  const output = execFileSync("python", ["-c", String.raw`
import importlib.util
import json
import tempfile
from pathlib import Path

root = Path(r"${root}")
spec = importlib.util.spec_from_file_location("marketplace_manifests", root / "tools" / "marketplace_manifests.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
with tempfile.TemporaryDirectory() as tmp:
    shelf = Path(tmp)
    skill = shelf / "skills" / "example"
    skill.mkdir(parents=True)
    path = skill / "SKILL.md"
    path.write_text("---\nname: example\ncategory: Evidence Insight\n---\n", encoding="utf-8")
    assert module.skill_category("example", shelf) == "Evidence Insight"
    path.write_text("---\nname: example\ncategory: Made Up\n---\n", encoding="utf-8")
    try:
        module.skill_category("example", shelf)
    except SystemExit as exc:
        assert "invalid marketplace category" in str(exc)
    else:
        raise AssertionError("invalid category was accepted")
print(json.dumps({"ok": True}))
`], { encoding: "utf8" });
  assert.deepEqual(JSON.parse(output), { ok: true });
});
