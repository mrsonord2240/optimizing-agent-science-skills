#!/usr/bin/env python3
"""Convert a QIIME2-exported SILVA (fasta + Feature ID/Taxon tsv) pair into:
  (a) a DADA2-formatted training fasta (rank-only, semicolon headers, no accessions)
  (b) a DADA2-formatted species fasta (">Accession Genus species")
  (c) a DECIPHER LearnTaxa taxonomy vector file (tab: seqid<TAB>Root;domain;phylum;...;genus;<TAB>seq)
Subsamples to a fixed N (simple random, fixed seed) for R runtime.
"""
import sys, random

def read_fasta(path):
    seqs = {}
    sid = None
    buf = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith(">"):
                if sid is not None:
                    seqs[sid] = "".join(buf)
                sid = line[1:].split()[0]
                buf = []
            else:
                buf.append(line)
        if sid is not None:
            seqs[sid] = "".join(buf)
    return seqs

def read_tax(path):
    tax = {}
    with open(path, encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            fid, taxon = parts[0], parts[1]
            tax[fid] = taxon
    return tax

def parse_ranks(taxon):
    ranks = {"d": "", "p": "", "c": "", "o": "", "f": "", "g": "", "s": ""}
    for token in taxon.split(";"):
        token = token.strip()
        if len(token) >= 3 and token[1:3] == "__":
            ranks[token[0]] = token[3:].strip()
    return ranks

def main():
    fasta_path, tax_path, n_sample, seed, out_prefix = sys.argv[1:6]
    n_sample = int(n_sample)
    seed = int(seed)
    seqs = read_fasta(fasta_path)
    tax = read_tax(tax_path)
    ids = [i for i in seqs if i in tax]
    print(f"sequences: {len(seqs)}  with taxonomy: {len(ids)}", file=sys.stderr)
    rng = random.Random(seed)
    if len(ids) > n_sample:
        ids = rng.sample(ids, n_sample)
    ids.sort()

    with open(out_prefix + "_dada2_train.fasta", "w", encoding="utf-8") as f_train, \
         open(out_prefix + "_dada2_species.fasta", "w", encoding="utf-8") as f_sp, \
         open(out_prefix + "_decipher_tax.tsv", "w", encoding="utf-8") as f_dec:
        n_sp = 0
        for fid in ids:
            seq = seqs[fid]
            r = parse_ranks(tax[fid])
            header = f"{r['d']};{r['p']};{r['c']};{r['o']};{r['f']};{r['g']};"
            f_train.write(f">{header}\n{seq}\n")
            # DADA2 species-fasta header MUST be exactly ">accession Genus species" (species = ONE
            # token). Take the last underscore-delimited token of the s__ label as the epithet and
            # drop placeholder/non-binomial SILVA labels (uncultured, metagenome, clade names, etc.)
            STOPWORDS = {"uncultured", "unidentified", "metagenome", "bacterium", "archaeon",
                         "sp", "clade", "group", "organism", "environmental", "endosymbiont"}
            if r["s"] and r["g"]:
                epithet = r["s"].split("_")[-1]
                if epithet.isalpha() and epithet.lower() not in STOPWORDS:
                    f_sp.write(f">{fid} {r['g']} {epithet}\n{seq}\n")
                    n_sp += 1
            dec_ranks = [x for x in [r['d'], r['p'], r['c'], r['o'], r['f'], r['g']] if x]
            dec_str = "Root;" + ";".join(dec_ranks) + ";"
            f_dec.write(f"{fid}\t{dec_str}\t{seq}\n")
    print(f"wrote {len(ids)} training seqs, {n_sp} species-level seqs", file=sys.stderr)

if __name__ == "__main__":
    main()
