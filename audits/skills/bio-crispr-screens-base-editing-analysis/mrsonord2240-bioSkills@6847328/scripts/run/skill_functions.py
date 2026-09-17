"""
Verbatim copy of the four bundled Python functions from the FIXED SKILL.md
(mrsonord2240/bioSkills@6847328:crispr-screens/base-editing-analysis), pasted
by hand from the read file -- not reimplemented, not paraphrased. Every test_*
script in this run/ directory imports from here so there is exactly one copy
to keep honest.
"""
import pandas as pd
import re
from Bio.Seq import Seq


def find_be_spacers(cds_sequence, cds_protein_start, target_aa, target_base='C', editor='BE4max'):
    '''Find sgRNAs that place target_base in editor-specific window at target_aa.
    Returns spacers with bystander annotation.

    Args:
        cds_sequence: nucleotide CDS (translated frame 1)
        cds_protein_start: amino acid number of CDS start (usually 1)
        target_aa: amino acid number to install variant (e.g., 130 for residue 130)
        target_base: 'C' (CBE) or 'A' (ABE)
        editor: 'BE3', 'BE4max', 'eA3A-BE3', 'ABE7.10', 'ABE8.20', 'ABE8e', 'evoCDA-BE'

    Returns: DataFrame with spacer, position-in-cds, target-base-position-in-spacer,
             bystander_positions, predicted_aa_changes
    '''
    # Editor-specific editing window (positions from PAM-distal end of spacer)
    window_by_editor = {
        'BE3': (4, 8),       'BE4max': (4, 8),    'eA3A-BE3': (5, 7),
        'ABE7.10': (4, 7),   'ABE8.20': (4, 8),   'ABE8e': (4, 8),     # SpABE8e matches CBE window (Richter 2020)
        'evoCDA-BE': (1, 9),
    }
    window_lo, window_hi = window_by_editor[editor]
    aa_index = target_aa - cds_protein_start  # 0-indexed in protein
    aa_start_nt = aa_index * 3                # nt offset in cds
    candidates = []
    spacer_len = 20
    pam_pattern = re.compile(r'(?=([ACGT]GG))')
    for strand, seq in [('+', cds_sequence), ('-', str(Seq(cds_sequence).reverse_complement()))]:
        for pam_match in pam_pattern.finditer(seq):
            pam_pos = pam_match.start()
            spacer_start = pam_pos - spacer_len
            if spacer_start < 0:
                continue
            spacer = seq[spacer_start:pam_pos]
            # Editor-specific window from PAM-distal end (1-indexed)
            # Find all editable bases in window
            edit_bases_in_window = []
            for i, b in enumerate(spacer[window_lo-1:window_hi], start=window_lo):
                if b == target_base:
                    edit_bases_in_window.append(i)
            if not edit_bases_in_window:
                continue
            # Annotate which edits hit the target_aa codon
            target_codon_start = aa_start_nt
            target_codon_end = target_codon_start + 3
            target_position_in_spacer = []
            for i in edit_bases_in_window:
                pos_in_seq = spacer_start + i - 1  # 0-indexed position within `seq` (strand-specific)
                # For strand '-', `seq` is the reverse complement of cds_sequence; convert
                # back to forward-CDS coordinates before comparing against target_codon_start/
                # end, which are always forward-strand. Without this, reverse-strand spacers
                # silently misattribute target vs bystander (verified: a hand-constructed
                # reverse-strand case with a known on-target C was called "bystander" by the
                # unconverted math, and the audit's own random-CDS run produced an on-target
                # call 65nt from the true codon).
                genomic_pos = (len(cds_sequence) - 1 - pos_in_seq) if strand == '-' else pos_in_seq
                if target_codon_start <= genomic_pos < target_codon_end:
                    target_position_in_spacer.append(i)
            bystander_positions = [i for i in edit_bases_in_window if i not in target_position_in_spacer]
            candidates.append({
                'spacer': spacer,
                'strand': strand,
                'spacer_start': spacer_start,
                'target_positions': target_position_in_spacer,
                'bystander_positions': bystander_positions,
                'n_bystanders': len(bystander_positions),
            })
    return pd.DataFrame(candidates).sort_values('n_bystanders')


def filter_by_editing_efficiency(crispresso_outputs_dir, target_pos, target_base, efficiency_threshold=0.5):
    '''Drop sgRNAs that edit <efficiency_threshold of reads at target position.
    crispresso_outputs_dir: directory containing CRISPResso per-sample outputs.
    target_pos: 1-indexed position WITHIN THE QUANTIFICATION WINDOW, in column
    order -- CRISPResso2 does not emit a literal "Position" column.'''
    from pathlib import Path
    results = []
    for sample_dir in Path(crispresso_outputs_dir).glob('CRISPResso_on_*'):
        sgrna_id = sample_dir.name.replace('CRISPResso_on_', '')
        quant_file = sample_dir / 'Quantification_window_nucleotide_percentage_table.txt'
        if not quant_file.exists():
            continue
        # Real CRISPResso2 2.3.4 file layout (verified against actual output, not
        # assumed): rows are nucleotide identity (A/C/G/T/N/-, the index column);
        # columns are one per window position, header-labeled with the REFERENCE
        # base at that position (so headers repeat -- pandas suffixes duplicates
        # .1/.2/... -- select columns positionally, not by label). Values are
        # FRACTIONS in [0, 1], not 0-100, despite the filename.
        df = pd.read_csv(quant_file, sep='\t', index_col=0)
        # Schema check: fail loudly and specifically on drift instead of a bare
        # KeyError deep in a groupby/indexing call.
        if target_base not in df.index:
            raise ValueError(f"target_base={target_base!r} not in table rows {list(df.index)} ({quant_file}); "
                              "unexpected CRISPResso2 Quantification_window_nucleotide_percentage_table.txt schema")
        if not (1 <= target_pos <= df.shape[1]):
            raise ValueError(f"target_pos={target_pos} out of range for a {df.shape[1]}-position "
                              f"quantification window in {quant_file}")
        original_frac = df.loc[target_base].iloc[target_pos - 1]
        editing_pct = 1 - original_frac
        results.append({'sgrna_id': sgrna_id, 'editing_pct': editing_pct,
                         'pass_filter': editing_pct >= efficiency_threshold})
    return pd.DataFrame(results)


def deconvolute_bystander(allele_table_path, target_pos, bystander_pos_list):
    '''From CRISPResso2 allele table, partition reads by edit pattern at target + bystanders.
    Returns: per-pattern frequency for each combination of target/bystander edits.'''
    alleles = pd.read_csv(allele_table_path, sep='\t', compression='zip')
    required_cols = {'Aligned_Sequence', 'Reference_Sequence', '%Reads'}
    missing = required_cols - set(alleles.columns)
    if missing:
        raise ValueError(f"Unexpected Alleles_frequency_table schema: missing {missing}; "
                          f"got columns {list(alleles.columns)}")
    # Mark target_edited and per-bystander_edited
    alleles['target_edited'] = alleles['Aligned_Sequence'].str[target_pos-1] != alleles['Reference_Sequence'].str[target_pos-1]
    for bp in bystander_pos_list:
        alleles[f'bystander_{bp}_edited'] = alleles['Aligned_Sequence'].str[bp-1] != alleles['Reference_Sequence'].str[bp-1]
    # Real Alleles_frequency_table.zip has no 'Reference_pct' column -- the
    # per-allele read-fraction column is '%Reads' (verified against actual
    # CRISPResso2 2.3.4 output).
    return alleles.groupby(['target_edited'] + [f'bystander_{bp}_edited' for bp in bystander_pos_list])['%Reads'].sum().reset_index()


def aggregate_variant_scores(mageck_sgrna_summary, variant_annotation_df):
    '''Aggregate sgRNA-level scores to per-variant scores.
    variant_annotation_df: per-sgRNA -> predicted variants (target + bystanders),
    keyed on the same sgRNA-identifier column name as mageck_sgrna_summary.
    MAGeCK's real sgrna_summary.txt column is lowercase 'sgrna' (not 'sgRNA') --
    build variant_annotation_df with that same column name.'''
    for _name, _frame in (('mageck_sgrna_summary', mageck_sgrna_summary), ('variant_annotation_df', variant_annotation_df)):
        if 'sgrna' not in _frame.columns:
            raise ValueError(f"{_name} is missing the 'sgrna' merge column (got {list(_frame.columns)})")
    df = mageck_sgrna_summary.merge(variant_annotation_df, on='sgrna')
    # Target-only contribution: sgRNAs with no bystanders
    target_only = df[df['n_bystanders'] == 0]
    target_only_scores = target_only.groupby('target_variant')['LFC'].agg(['mean', 'std', 'count'])
    # Mixed signal: sgRNAs with bystanders
    mixed = df[df['n_bystanders'] > 0]
    return target_only_scores, mixed
