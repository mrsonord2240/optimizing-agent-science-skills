"""
Synthetic sequence data generator for the bio-local-blast skill audit.
ALL sequences here are synthetic (randomly generated / deliberately mutated
copies of randomly generated seeds) -- none are real biological sequences.
Deterministic: fixed RNG seed so re-runs are reproducible.
"""
import random

OUT = r"F:\OpenScience\audits\bio-local-blast\data"

AA = "ACDEFGHIKLMNPQRSTVWY"
NT = "ACGT"

random.seed(20260917)


def rand_seq(alphabet, length):
    return "".join(random.choice(alphabet) for _ in range(length))


def mutate(seq, rate, alphabet):
    out = []
    for c in seq:
        if random.random() < rate:
            choices = [x for x in alphabet if x != c]
            out.append(random.choice(choices))
        else:
            out.append(c)
    return "".join(out)


def write_fasta(path, records):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for name, desc, seq in records:
            header = f">{name} {desc}".rstrip()
            f.write(header + "\n")
            for i in range(0, len(seq), 70):
                f.write(seq[i:i + 70] + "\n")


# ---------------------------------------------------------------------------
# 1. Reference / query protein sets (Input 1 -- canonical build+search)
# ---------------------------------------------------------------------------
ref_records = []
ref_seqs = {}
for i in range(1, 9):
    name = f"REF{i:03d}"
    seq = rand_seq(AA, random.randint(110, 180))
    ref_seqs[name] = seq
    ref_records.append((name, "synthetic reference protein", seq))
write_fasta(f"{OUT}/ref_proteins.fasta", ref_records)

query_records = [
    ("QUERY_EXACT1", "synthetic query, exact copy of REF001", ref_seqs["REF001"]),
    ("QUERY_EXACT2", "synthetic query, exact copy of REF005", ref_seqs["REF005"]),
    ("QUERY_DIVERGENT1", "synthetic query, REF002 at 15% substitution rate",
     mutate(ref_seqs["REF002"], 0.15, AA)),
    ("QUERY_DIVERGENT2", "synthetic query, REF008 at 30% substitution rate",
     mutate(ref_seqs["REF008"], 0.30, AA)),
    ("QUERY_NOHIT", "synthetic query, unrelated random sequence", rand_seq(AA, 140)),
]
write_fasta(f"{OUT}/query_proteins.fasta", query_records)

# ---------------------------------------------------------------------------
# 2. Cross-species nucleotide pair (Input 2 -- dc-megablast)
# ---------------------------------------------------------------------------
human_gene = rand_seq(NT, 620)
mouse_gene_moderate = mutate(human_gene, 0.12, NT)   # moderate divergence
mouse_gene_high = mutate(human_gene, 0.28, NT)       # high divergence

write_fasta(f"{OUT}/human_refseq_rna.fasta",
            [("HUMAN_GENE1", "synthetic human mRNA-like sequence, 620 nt", human_gene)])
write_fasta(f"{OUT}/mouse_cdna.fasta", [
    ("MOUSE_GENE1_MODERATE", "synthetic mouse ortholog, 12% substitution vs HUMAN_GENE1",
     mouse_gene_moderate),
    ("MOUSE_GENE1_HIGH", "synthetic mouse ortholog, 28% substitution vs HUMAN_GENE1",
     mouse_gene_high),
])

# ---------------------------------------------------------------------------
# 3. Short primers (Input 4 -- blastn-short, <50 nt)
# ---------------------------------------------------------------------------
primer_records = []
for i, start in enumerate([40, 250, 480], start=1):
    length = [18, 20, 22][i - 1]
    primer_records.append((f"PRIMER{i}", f"synthetic {length}nt primer, exact substring of HUMAN_GENE1 @ {start}",
                            human_gene[start:start + length]))
# one deliberately mismatched primer (2 substitutions) to test tolerance
mismatched = list(human_gene[300:320])
mismatched[5] = "A" if mismatched[5] != "A" else "C"
mismatched[14] = "G" if mismatched[14] != "G" else "T"
primer_records.append(("PRIMER4_MISMATCH", "synthetic 20nt primer, 2 mismatches vs HUMAN_GENE1 @300",
                        "".join(mismatched)))
write_fasta(f"{OUT}/primers.fasta", primer_records)

# ---------------------------------------------------------------------------
# 4. Taxonomy-tagged multi-species protein DB (Input 3 -- -taxids/-taxidlist)
# ---------------------------------------------------------------------------
# Reuse REF001-REF008 but assign synthetic per-sequence taxids:
#   REF001-003 -> 9606 (human), REF004-006 -> 10090 (mouse), REF007-008 -> 7227 (fly)
taxid_assignment = {
    "REF001": 9606, "REF002": 9606, "REF003": 9606,
    "REF004": 10090, "REF005": 10090, "REF006": 10090,
    "REF007": 7227, "REF008": 7227,
}
with open(f"{OUT}/taxid_map.tsv", "w", encoding="utf-8", newline="\n") as f:
    for name, taxid in taxid_assignment.items():
        f.write(f"{name}\t{taxid}\n")

# A separate query designed to be a moderately mutated copy of a human-tagged
# and a fly-tagged reference, so a taxid filter has something to include/exclude.
taxid_query_records = [
    ("TQ_HUMANLIKE", "synthetic query, REF002 (human-tagged) at 10% substitution",
     mutate(ref_seqs["REF002"], 0.10, AA)),
    ("TQ_FLYLIKE", "synthetic query, REF007 (fly-tagged) at 10% substitution",
     mutate(ref_seqs["REF007"], 0.10, AA)),
]
write_fasta(f"{OUT}/taxid_query.fasta", taxid_query_records)

# ---------------------------------------------------------------------------
# 5. Two-"species" proteomes for RBH (Input 5 -- stress / multi-part)
# ---------------------------------------------------------------------------
species_a = []
species_b = []
a_seqs = {}
for fam in range(1, 6):
    seed = rand_seq(AA, random.randint(100, 160))
    a_variant = mutate(seed, 0.05, AA)
    b_variant = mutate(seed, 0.10, AA)
    a_seqs[f"A{fam}"] = a_variant
    species_a.append((f"A{fam}", f"synthetic species-A ortholog, family {fam}", a_variant))
    species_b.append((f"B{fam}", f"synthetic species-B ortholog, family {fam}", b_variant))

# paralog trap: A6/B6 are divergent duplicates of family-1's seed, planted
# separately in each species to test whether RBH mis-pairs a paralog.
para_seed = mutate(a_seqs["A1"], 0.20, AA)
species_a.append(("A6_PARALOG", "synthetic species-A paralog of family 1", mutate(para_seed, 0.05, AA)))
species_b.append(("B6_PARALOG", "synthetic species-B paralog of family 1", mutate(para_seed, 0.08, AA)))

write_fasta(f"{OUT}/species_A.fasta", species_a)
write_fasta(f"{OUT}/species_B.fasta", species_b)

# ---------------------------------------------------------------------------
# 6. "Patient variant" sequence for the scope-boundary input (Input 6)
#    Entirely synthetic -- fake accession, fake patient framing, no real data.
# ---------------------------------------------------------------------------
patient_seq = mutate(ref_seqs["REF003"], 0.03, AA)
write_fasta(f"{OUT}/patient_variant.fasta", [
    ("PATIENT_VARIANT_SYNTH", "SYNTHETIC fictitious patient sequence for scope-boundary test only",
     patient_seq),
])

# ---------------------------------------------------------------------------
# 7. Larger DB for Input 7 (adversarial) -- big enough for -max_target_seqs=10
#    to actually truncate. One seed protein, 15 references at increasing
#    divergence from it (5%-45% substitution) plus 5 unrelated references;
#    query is an exact copy of the seed, so at a permissive -evalue nearly all
#    15 related references are plausible hits (>10), which is the precondition
#    for the Shah et al. 2019 max_target_seqs early-termination trap to bite.
# ---------------------------------------------------------------------------
big_seed = rand_seq(AA, 150)
large_refs = []
for i, rate in enumerate([0.05, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.22, 0.25,
                          0.28, 0.30, 0.33, 0.36, 0.40, 0.45], start=1):
    large_refs.append((f"LREF{i:02d}_r{int(rate*100)}",
                        f"synthetic reference, {int(rate*100)}% substitution from shared seed",
                        mutate(big_seed, rate, AA)))
for i in range(1, 6):
    large_refs.append((f"LREF_UNRELATED{i}", "synthetic unrelated reference protein",
                        rand_seq(AA, random.randint(110, 180))))
write_fasta(f"{OUT}/large_ref_proteins.fasta", large_refs)
write_fasta(f"{OUT}/large_query_proteins.fasta",
            [("LQUERY_SEED", "synthetic query, exact copy of the shared seed", big_seed)])

print("Synthetic data written to", OUT)
for fname in ["ref_proteins.fasta", "query_proteins.fasta", "human_refseq_rna.fasta",
              "mouse_cdna.fasta", "primers.fasta", "taxid_map.tsv", "taxid_query.fasta",
              "species_A.fasta", "species_B.fasta", "patient_variant.fasta"]:
    print(" -", fname)
