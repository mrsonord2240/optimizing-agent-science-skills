"""Functions copied VERBATIM from SKILL.md (bio-alignment-msa-parsing @354b499). Do not edit."""
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from collections import Counter
import numpy as np
import pandas as pd
import re

def get_sequence_by_id(alignment, seq_id):
    for record in alignment:
        if record.id == seq_id:
            return record
    return None

def find_conserved_positions(alignment, threshold=1.0):
    conserved = []
    for col_idx in range(alignment.get_alignment_length()):
        column = alignment[:, col_idx]
        counts = Counter(column)
        most_common_char, most_common_count = counts.most_common(1)[0]
        if most_common_char != '-':
            conservation = most_common_count / len(alignment)
            if conservation >= threshold:
                conserved.append((col_idx, most_common_char))
    return conserved

def gaps_per_column(alignment):
    return [alignment[:, i].count('-') for i in range(alignment.get_alignment_length())]

def find_gappy_columns(alignment, threshold=0.5):
    gappy = []
    num_seqs = len(alignment)
    for col_idx in range(alignment.get_alignment_length()):
        column = alignment[:, col_idx]
        gap_fraction = column.count('-') / num_seqs
        if gap_fraction >= threshold:
            gappy.append(col_idx)
    return gappy

def remove_gappy_columns(alignment, threshold=0.5):
    num_seqs = len(alignment)
    keep_columns = []
    for col_idx in range(alignment.get_alignment_length()):
        column = alignment[:, col_idx]
        gap_fraction = column.count('-') / num_seqs
        if gap_fraction < threshold:
            keep_columns.append(col_idx)

    new_records = []
    for record in alignment:
        new_seq = ''.join(str(record.seq)[i] for i in keep_columns)
        new_records.append(SeqRecord(Seq(new_seq), id=record.id, description=record.description))
    return MultipleSeqAlignment(new_records)

def consensus_sequence(alignment, threshold=0.5, gap_char='-', ambiguous='N'):
    consensus = []
    for col_idx in range(alignment.get_alignment_length()):
        column = alignment[:, col_idx]
        counts = Counter(column)
        most_common_char, most_common_count = counts.most_common(1)[0]
        if most_common_char == gap_char:
            counts.pop(gap_char, None)
            if counts:
                most_common_char, most_common_count = counts.most_common(1)[0]
            else:
                most_common_char = gap_char

        if most_common_count / len(alignment) >= threshold:
            consensus.append(most_common_char)
        else:
            consensus.append(ambiguous)
    return ''.join(consensus)

def extract_ungapped_regions(alignment, ref_idx=0):
    ref_seq = str(alignment[ref_idx].seq)
    ungapped_cols = [i for i, char in enumerate(ref_seq) if char != '-']

    new_records = []
    for record in alignment:
        new_seq = ''.join(str(record.seq)[i] for i in ungapped_cols)
        new_records.append(SeqRecord(Seq(new_seq), id=record.id, description=record.description))
    return MultipleSeqAlignment(new_records)

def filter_by_id(alignment, pattern):
    regex = re.compile(pattern)
    return MultipleSeqAlignment([r for r in alignment if regex.search(r.id)])

def filter_by_gap_content(alignment, max_gap_fraction=0.1):
    return MultipleSeqAlignment(
        [r for r in alignment if str(r.seq).count('-') / len(r.seq) <= max_gap_fraction]
    )

def remove_duplicates(alignment):
    seen = set()
    return MultipleSeqAlignment([r for r in alignment if not (str(r.seq) in seen or seen.add(str(r.seq)))])

def coordinate_map(record):
    chars = np.frombuffer(str(record.seq).encode('ascii'), dtype=np.uint8)
    is_residue = chars != ord('-')
    seq_to_aln = np.flatnonzero(is_residue)
    aln_to_seq = np.where(is_residue, np.cumsum(is_residue) - 1, -1)
    return seq_to_aln, aln_to_seq

def henikoff_weights(alignment):
    seq_array = np.array([list(str(r.seq)) for r in alignment])
    weights = np.zeros(len(alignment))
    for col_idx in range(seq_array.shape[1]):
        residues, inverse, counts = np.unique(seq_array[:, col_idx], return_inverse=True, return_counts=True)
        if '-' in residues:
            continue
        weights += 1.0 / (len(residues) * counts[inverse])
    return weights / weights.sum()
