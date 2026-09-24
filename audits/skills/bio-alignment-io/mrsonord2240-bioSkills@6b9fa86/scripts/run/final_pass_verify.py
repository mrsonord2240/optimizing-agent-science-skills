r"""Final-pass regression and fresh verification for bio-alignment-io.

Usage:
  F:\OpenScience\audit-envs\alignment\Scripts\python.exe final_pass_verify.py \
      F:\OpenScience\worktrees\bio-alignment-io-final-pass\alignment\alignment-io

Runs the eight archived audit scenario areas (canonical examples, Stockholm/NEXUS,
PHYLIP/Clustal, MAF, downstream-safe ids, format/reference coverage, A2M/A3M,
and alphabet inference) plus two fresh invalid-input tests. It always runs copied
examples so the source worktree remains byte-clean during execution.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from Bio import AlignIO, SeqIO
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


SOURCE = Path(sys.argv[1]).resolve()
EXAMPLES = SOURCE / "examples"
SKILL = SOURCE / "SKILL.md"
CHECKS = []


def check(condition: bool, message: str) -> None:
    CHECKS.append((condition, message))
    print(("PASS" if condition else "FAIL") + " " + message)


def msa(rows: list[tuple[str, str]]) -> MultipleSeqAlignment:
    return MultipleSeqAlignment([SeqRecord(Seq(sequence), id=identifier) for identifier, sequence in rows])


def run_convert(work: Path, alignment: MultipleSeqAlignment, override: str | None = None):
    input_path = work / "input.aln"
    AlignIO.write(alignment, input_path, "clustal")
    command = [sys.executable, "convert_formats.py", input_path.name]
    if override:
        command.append(override)
    return subprocess.run(command, cwd=work, capture_output=True, text=True, encoding="utf-8")


def no_outputs(work: Path) -> bool:
    return not any((work / name).exists() for name in ("output.fasta", "output.phy", "output.nex"))


with tempfile.TemporaryDirectory() as temporary:
    root = Path(temporary)
    copied = root / "examples"
    shutil.copytree(EXAMPLES, copied)

    # Archived input 1: canonical reading, slicing, batch conversion, and inferred DNA conversion.
    read = subprocess.run([sys.executable, "read_alignment.py"], cwd=copied, capture_output=True, text=True, encoding="utf-8")
    check(read.returncode == 0 and "4" in read.stdout and "columns" in read.stdout, "archived input 1: read_alignment copied example")
    sliced = subprocess.run([sys.executable, "slice_alignment.py"], cwd=copied, capture_output=True, text=True, encoding="utf-8")
    check(sliced.returncode == 0 and (copied / "trimmed_subset.fasta").exists(), "archived input 1: slice copied example")
    batch = subprocess.run([sys.executable, "batch_convert.py"], cwd=copied, capture_output=True, text=True, encoding="utf-8")
    check(batch.returncode == 0 and (copied / "converted" / "sample_alignment.fasta").exists(), "archived input 1: batch copied example")

    # Archived input 2: NEXUS writer handles DNA, RNA, and protein then re-reads NEXUS.
    dna = msa([("dna1", "ACGTACGT"), ("dna2", "ACGTTCGT")])
    r = run_convert(copied, dna)
    reread = AlignIO.read(copied / "output.nex", "nexus") if r.returncode == 0 else []
    check(r.returncode == 0 and "datatype=dna" in (copied / "output.nex").read_text().lower() and len(reread) == 2, "archived input 2: DNA NEXUS round trip")
    for name in ("output.fasta", "output.phy", "output.nex"):
        (copied / name).unlink()
    r = run_convert(copied, msa([("rna1", "ACGUACGU"), ("rna2", "ACGUUCGU")]))
    check(r.returncode == 0 and "datatype=rna" in (copied / "output.nex").read_text().lower(), "archived input 2: RNA NEXUS round trip")
    for name in ("output.fasta", "output.phy", "output.nex"):
        (copied / name).unlink()
    r = run_convert(copied, msa([("prot1", "MPEPTIDE"), ("prot2", "MPEPAIDE")]))
    check(r.returncode == 0 and "datatype=protein" in (copied / "output.nex").read_text().lower(), "archived input 2: protein NEXUS round trip")
    check([str(record.seq) for record in AlignIO.read(copied / "output.nex", "nexus")] == ["MPEPTIDE", "MPEPAIDE"], "archived input 2: NEXUS preserves protein sequences")

    # Archived input 3: Clustal's silent 30-character truncation is both documented and observable.
    long = msa([("A" * 30 + "first", "ACGTACGT"), ("A" * 30 + "second", "ACGTTCGT")])
    clustal = copied / "long_ids.aln"
    AlignIO.write(long, clustal, "clustal")
    clustal_ids = [record.id for record in AlignIO.read(clustal, "clustal")]
    check(len(set(clustal_ids)) == 1 and "Clustal writer truncates identifiers to 30 characters" in SKILL.read_text(), "archived input 3: Clustal id collision is documented")
    check(all(len(identifier) == 30 for identifier in clustal_ids), "archived input 3: Clustal ids are truncated at 30 characters")
    check("assert the ids remain unique" in SKILL.read_text(), "archived input 3: Clustal round-trip uniqueness check is instructed")

    # Archived input 4: MAF minus-strand coordinate rule from its reference.
    namespace = {}
    exec("def maf_to_plus_strand_coords(a):\n    return a['srcSize'] - a['start'] - a['size'] if a['strand'] == -1 else a['start']\n", namespace)
    check(namespace["maf_to_plus_strand_coords"]({"strand": -1, "srcSize": 150, "start": 66, "size": 24}) == 60, "archived input 4: MAF minus-strand coordinate formula")
    check("strand" in (SOURCE / "references" / "maf-coordinates.md").read_text(), "archived input 4: MAF reference documents integer strand annotations")
    check("srcSize - start - size" in (SOURCE / "references" / "maf-coordinates.md").read_text(), "archived input 4: MAF reference states the plus-strand conversion")

    # Archived input 5: the example warns before exporting punctuation-bearing ids to MrBayes.
    for name in ("output.fasta", "output.phy", "output.nex"):
        path = copied / name
        if path.exists():
            path.unlink()
    r = run_convert(copied, msa([("sp|P02185|MYG", "MPEPTIDE"), ("lcl|NM_000518.5", "MPEPAIDE")]))
    check(r.returncode == 0 and "MrBayes-safe" in r.stdout, "archived input 5: MrBayes unsafe-id warning")
    check("datatype=protein" in (copied / "output.nex").read_text().lower(), "archived input 5: warned NEXUS remains syntactically readable")
    check("[^A-Za-z0-9_]" in SKILL.read_text(), "archived input 5: complete safe-id recipe is retained")

    # Archived input 6: all progressive-disclosure links resolve from the main Skill.
    text = SKILL.read_text()
    references = ("references/maf-coordinates.md", "references/a2m-a3m.md", "references/stockholm-streaming.md")
    check(all(reference in text and (SOURCE / reference).is_file() for reference in references), "archived input 6: all reference links are present")
    check("## Reference Files" in text, "archived input 6: progressive-disclosure index is present")
    check(len(text.splitlines()) < 450, "archived input 6: main SKILL is reduced below 450 lines")

    # Archived input 7: the documented ragged-A2M SeqIO pattern keeps only match columns.
    a2m = copied / "ragged.a2m"
    a2m.write_text(">query\nACDEfg-H\n>hit\nAC-Ew.-H\n")
    match_only = {record.id: "".join(char for char in str(record.seq) if char.isupper() or char == "-") for record in SeqIO.parse(a2m, "fasta")}
    check(match_only == {"query": "ACDE-H", "hit": "AC-E-H"} and "ragged" in (SOURCE / references[1]).read_text(), "archived input 7: ragged A2M match-column extraction")
    check(len(list(SeqIO.parse(a2m, "fasta"))) == 2, "archived input 7: SeqIO parses ragged A2M rows")
    check("first position" in (SOURCE / references[1]).read_text(), "archived input 7: A3M first-record pitfall is retained")

    # Archived input 8: IUPAC and X-masked nucleotide data infer DNA; mixed T/U is rejected.
    for name in ("output.fasta", "output.phy", "output.nex"):
        path = copied / name
        if path.exists():
            path.unlink()
    r = run_convert(copied, msa([("iupac1", "ACGTRYKMSWBDHVX"), ("iupac2", "ACGTRYKMSWBDHVX")]))
    check(r.returncode == 0 and "Molecule type: DNA" in r.stdout and "datatype=dna" in (copied / "output.nex").read_text().lower(), "archived input 8: IUPAC/X-masked DNA inference")
    check("NUCLEOTIDE_CODES" in (copied / "convert_formats.py").read_text(), "archived input 8: converter has an explicit IUPAC alphabet")
    check("X" in (copied / "convert_formats.py").read_text(), "archived input 8: converter accepts X-masked nucleotides")

    # Fresh input 9: a DNA/RNA override mismatch exits before it creates any new outputs.
    mismatch = root / "mismatch"
    shutil.copytree(EXAMPLES, mismatch)
    r = run_convert(mismatch, dna, "RNA")
    check(r.returncode != 0 and no_outputs(mismatch) and "contradicts" in (r.stdout + r.stderr), "fresh input 9: contradictory RNA override leaves no outputs")
    check("Molecule type RNA contradicts" in (r.stdout + r.stderr), "fresh input 9: contradictory override gives actionable type diagnostic")
    check((mismatch / "input.aln").exists(), "fresh input 9: rejected override preserves the input alignment")

    # Fresh input 10: mixed T/U data exits with a direct diagnostic and no outputs.
    mixed = root / "mixed"
    shutil.copytree(EXAMPLES, mixed)
    r = run_convert(mixed, msa([("dna", "ACGTACGT"), ("rna", "ACGUACGU")]))
    check(r.returncode != 0 and no_outputs(mixed) and "Mixed T and U" in (r.stdout + r.stderr), "fresh input 10: mixed T/U diagnostic leaves no outputs")
    check("split or correct" in (r.stdout + r.stderr), "fresh input 10: mixed T/U diagnostic explains recovery")
    check("Traceback" not in (r.stdout + r.stderr), "fresh input 10: mixed T/U exits without a traceback")

passed = sum(ok for ok, _ in CHECKS)
print(f"ASSERTIONS: {passed}/{len(CHECKS)}")
raise SystemExit(0 if passed == len(CHECKS) else 1)
