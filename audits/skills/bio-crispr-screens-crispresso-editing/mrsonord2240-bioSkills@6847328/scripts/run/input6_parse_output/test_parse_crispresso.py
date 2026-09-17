"""
Regression test for the audit's P0 finding: SKILL.md's parse_crispresso() function,
transcribed VERBATIM from the fixed SKILL.md (crispr-screens/crispresso-editing,
mrsonord2240/bioSkills@6847328), run against real CRISPResso2 2.3.4 Docker output
(CRISPResso_on_input1_noqfilter, a fresh run this audit produced on FANC.Cas9.fastq).

Pre-fix, this function crashed with ValueError: too many values to unpack because it assumed
CRISPResso_mapping_statistics.txt was one key\\tvalue pair per line, and it read a
READS_ALIGNED_PERCENTAGE column that doesn't exist in the real file.
"""
import pandas as pd
import json
from pathlib import Path


def parse_crispresso(output_dir):
    '''Extract key metrics from CRISPResso output directory.'''
    out = {}
    # Mapping statistics: 7-column, 2-row TSV (header + one data row); no percentage column,
    # so compute mapping_pct from READS ALIGNED / READS IN INPUTS.
    map_stats = pd.read_csv(Path(output_dir) / 'CRISPResso_mapping_statistics.txt', sep='\t').iloc[0]
    out['reads_in_input'] = int(map_stats['READS IN INPUTS'])
    out['reads_aligned'] = int(map_stats['READS ALIGNED'])
    out['mapping_pct'] = out['reads_aligned'] / out['reads_in_input'] * 100
    # Editing quantification
    quant = pd.read_csv(Path(output_dir) / 'CRISPResso_quantification_of_editing_frequency.txt', sep='\t')
    out['editing_quant'] = quant.set_index('Amplicon').to_dict()
    # JSON metadata
    info_path = Path(output_dir) / 'CRISPResso2_info.json'
    if info_path.exists():
        out['info'] = json.loads(info_path.read_text())
    return out


if __name__ == '__main__':
    import sys

    output_dir = sys.argv[1] if len(sys.argv) > 1 else \
        r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\crispresso-editing-audit\CRISPResso_on_input1_noqfilter"

    result = parse_crispresso(output_dir)
    print("reads_in_input:", result['reads_in_input'])
    print("reads_aligned:", result['reads_aligned'])
    print("mapping_pct:", result['mapping_pct'])
    print("editing_quant['Modified%']['Reference']:", result['editing_quant']['Modified%']['Reference'])
    print("info key present:", 'info' in result)

    # Assertions against known ground truth for this real dataset (upstream expected result:
    # 26.38297872% Modified, byte-identical, when run WITHOUT --min_average_read_quality 30)
    assert result['reads_in_input'] == 250, f"expected 250, got {result['reads_in_input']}"
    assert result['reads_aligned'] == 235, f"expected 235, got {result['reads_aligned']}"
    assert abs(result['mapping_pct'] - 94.0) < 0.01, f"expected 94.0, got {result['mapping_pct']}"
    assert abs(result['editing_quant']['Modified%']['Reference'] - 26.38297872) < 1e-6, \
        f"expected 26.38297872, got {result['editing_quant']['Modified%']['Reference']}"
    print("\nALL ASSERTIONS PASSED -- parse_crispresso() runs correctly against real CRISPResso2 output.")
