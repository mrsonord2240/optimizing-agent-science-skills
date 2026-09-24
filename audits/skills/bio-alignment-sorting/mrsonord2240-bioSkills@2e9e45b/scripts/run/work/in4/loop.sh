#!/bin/bash
cd "$1"
for f in *.bam; do samtools view -H "$f" | head -1; done | sort -u
