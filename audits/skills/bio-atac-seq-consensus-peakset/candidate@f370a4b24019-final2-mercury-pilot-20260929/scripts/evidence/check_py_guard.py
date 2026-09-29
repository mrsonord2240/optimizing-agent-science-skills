"""Exercise the exact connected pybedtools function's guards with a fake BedTool sink."""
from __future__ import annotations

import ast
from pathlib import Path
import tempfile

METHODS = Path(
    "/mnt/openscience/wt/mercury-pilot-consensus-peakset/skills/"
    "bio-atac-seq-consensus-peakset/references/method-reference.md"
)


class Saved:
    def __init__(self, rows, path):
        self.rows = rows
        self.path = path


class FakeBedTool:
    def __init__(self, rows):
        self.rows = rows

    def saveas(self, path):
        return Saved(self.rows, path)


created = []


class FakePybedtools:
    @staticmethod
    def BedTool(rows):
        created.append(rows)
        return FakeBedTool(rows)


lines = METHODS.read_text(encoding="utf-8").splitlines()
start = next(i for i, line in enumerate(lines) if line.startswith("def fix_width_recenter("))
end = next(i for i in range(start, len(lines)) if lines[i].strip() == "```")
function_source = "\n".join(lines[start:end])
module = ast.parse(function_source, filename=str(METHODS))
function = next(node for node in module.body if isinstance(node, ast.FunctionDef))
namespace = {"pbt": FakePybedtools}
exec(compile(ast.Module(body=[function], type_ignores=[]), str(METHODS), "exec"), namespace)
recenter = namespace["fix_width_recenter"]


def record(start: int, end: int, summit: str) -> str:
    fields = ["chr1", str(start), str(end), "peak", "1000", "+", "5.5", "10", "9", summit]
    return "\t".join(fields)


def run_rows(rows: list[str], expected_error: str | None = None):
    before = len(created)
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "fixture.narrowPeak"
        source.write_text("\n".join(rows) + "\n", encoding="utf-8")
        try:
            result = recenter(str(source), out_path="mock.bed")
        except Exception as exc:
            assert expected_error is not None, f"unexpected failure: {exc}"
            message = str(exc)
            assert expected_error in message, message
            assert len(created) == before, "invalid input reached BedTool/output construction"
            print(f"REJECT {expected_error}: {message}")
            return None
        assert expected_error is None, "invalid input was accepted"
        assert result.path == "mock.bed"
        print(f"ACCEPT rows={result.rows}")
        return result.rows


valid = run_rows([record(1000, 1100, "0"), record(1000, 1100, "99")])
assert valid == [
    ["chr1", "750", "1251", "peak", "5.5", "+"],
    ["chr1", "849", "1350", "peak", "5.5", "+"],
]
assert all(int(row[2]) - int(row[1]) == 501 for row in valid)
run_rows(["\t".join(record(1000, 1100, "0").split("\t")[:9])], "expected 10 narrowPeak columns")
run_rows([record(1000, 1100, "-1")], "summit offset -1 means no summit was called")
run_rows([record(1000, 1100, "-2")], "summit offset must be within the narrowPeak interval")
run_rows([record(1000, 1100, "100")], "summit offset must be within the narrowPeak interval")
run_rows([record(1000, 1100, "0"), record(2000, 2100, "-1")], "fixture.narrowPeak line 2")
print("Python guard checks passed; invalid inputs failed before BedTool construction.")
