import subprocess

subprocess.run(
    ['bash', '-o', 'pipefail', '-c', 'bwa mem ref.fa r1.fq.gz | samtools sort -o py_shim.bam'],
    check=True
)
