from pathlib import Path
import subprocess
import sys

run_dir = Path(__file__).parent
viewer = Path(sys.argv[1])

(run_dir / "qual_zero.vcf").write_text(
    "##fileformat=VCFv4.2\n"
    "##contig=<ID=chr1,length=100>\n"
    "##FORMAT=<ID=GT,Number=1,Type=String,Description=Genotype>\n"
    "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tS1\n"
    "chr1\t10\t.\tA\tT\t0\tPASS\t.\tGT\t0/1\n"
    "chr1\t11\t.\tC\tG\t.\tPASS\t.\tGT\t0/1\n"
)

(run_dir / "caller_fields.vcf").write_text(
    "##fileformat=VCFv4.2\n"
    "##contig=<ID=chr1,length=100>\n"
    "##FORMAT=<ID=GT,Number=1,Type=String,Description=Genotype>\n"
    "##FORMAT=<ID=GQ,Number=1,Type=Integer,Description=Genotype Quality>\n"
    "##FORMAT=<ID=PL,Number=G,Type=Integer,Description=Phred-scaled genotype likelihoods>\n"
    "##FORMAT=<ID=GL,Number=G,Type=Float,Description=Log10-scaled genotype likelihoods>\n"
    "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tS1\n"
    "chr1\t20\t.\tG\tA\t30\tPASS\t.\tGT:GQ:PL:GL\t0/1:8:8,0,12:-0.8,0,-1.2\n"
    "chr1\t21\t.\tG\tT\t30\tPASS\t.\tGT:GQ:PL\t0/1:99:8,0,12\n"
)

viewer_run = subprocess.run(
    [sys.executable, str(viewer), str(run_dir / "qual_zero.vcf"), "2"],
    check=True,
    text=True,
    capture_output=True,
)
assert "chr1:10\tA>T\tQUAL=0.0" in viewer_run.stdout
assert "chr1:11\tC>G\tQUAL=." in viewer_run.stdout
print("fresh-1 QUAL zero and missing rendering: PASS")
print(viewer_run.stdout.rstrip())

from cyvcf2 import VCF

records = list(VCF(str(run_dir / "caller_fields.vcf")))
assert records[0].genotypes[0][:2] == [0, 1]
assert records[0].format("GQ")[0][0] == 8
assert records[0].format("PL")[0].tolist() == [8, 0, 12]
assert records[1].format("GQ")[0][0] == 99
assert records[1].format("PL")[0].tolist() == [8, 0, 12]
print("fresh-2 caller-emitted GT/GQ and PL parsing: PASS")
print("record1 GL -> PL relative scaling: [-0.8,0,-1.2] -> [8,0,12]; emitted GQ=8")
print("record2 preserves caller-emitted GQ=99 despite the PL gap=8; do not reconstruct GQ")
