#!/bin/bash
# Version notes in the SKILL: "-T added in samtools 1.22", "--config (samtools 1.17+)", "-aa" -- checked against the samtools NEWS (ncbi/samtools_NEWS.md, fetched 2026-09-20).
cd "$(dirname "$0")/ncbi"
awk '/^Release [0-9]/{rel=$2} /consensus -T ref.fa/{print "release " rel ": " $0} /instrument specific profiles/{print "release " rel ": " $0} /New -aa mode for consensus/{print "release " rel ": " $0}' samtools_NEWS.md
