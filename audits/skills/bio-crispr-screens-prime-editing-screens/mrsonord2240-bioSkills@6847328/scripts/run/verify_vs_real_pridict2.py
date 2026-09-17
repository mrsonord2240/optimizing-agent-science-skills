"""
Cross-check the fixed bundled script's own PBS/RTT geometry (peg_library_filtered.csv,
produced by design_pegrna_pridict2_FIXED.py) against the REAL PRIDICT2 CLI's own output
(predictions_round2/*_pegRNA_Pridict_full.csv, produced by actually running
pridict2_pegRNA_design.py batch on the same loci) for the two loci used this round
(VAR_REALISTIC, VAR_MINUS). Confirms the fixed script's PBS/RTT extraction is not just
internally self-consistent but matches the real, independently-run tool -- including on
the '-' strand branch (VAR_MINUS), which the Skill's own SKILL.md worked example never
exercises (that worked example is +strand only).
"""
import pandas as pd

script_df = pd.read_csv('peg_library_filtered.csv')
real_realistic = pd.read_csv('predictions_round2/VAR_REALISTIC_pegRNA_Pridict_full.csv')
real_minus = pd.read_csv('predictions_round2/VAR_MINUS_pegRNA_Pridict_full.csv')


def find_real_match(real_df, pbs_len, rt_len, strand, spacer):
    target_strand = 'Rv' if strand == '-' else 'Fw'
    # Match on the last 19 bases of the spacer, not all 20 -- PRIDICT2 forces a
    # synthetic 5'-G onto its own reported Spacer-Sequence (documented convention),
    # so the two can legitimately differ at position 0 even for the same candidate.
    sub = real_df[(real_df['PBSlength'] == pbs_len) & (real_df['RTlength'] == rt_len) &
                  (real_df['Target-Strand'] == target_strand) &
                  (real_df['Spacer-Sequence'].str[1:] == spacer[1:])]
    return sub


n_checked = 0
n_matched = 0
for _, row in script_df.iterrows():
    real_df = real_realistic if row['variant_id'] == 'VAR_REALISTIC' else real_minus
    sub = find_real_match(real_df, len(row['pbs']), len(row['rtt']), row['pam_strand'], row['spacer'])
    n_checked += 1
    if sub.empty:
        print(row['variant_id'], row['pam_strand'], 'PBSlen', len(row['pbs']), 'RTlen', len(row['rtt']),
              '-> NOT FOUND in real PRIDICT2 output at this length/strand')
        continue
    real_pbs = sub.iloc[0]['PBSrevcomp']
    real_rt = sub.iloc[0]['RTrevcomp'].upper()  # PRIDICT2 lowercases the installed base
    script_pbs = row['pbs']
    script_rt = row['rtt'].upper()
    pbs_match = script_pbs == real_pbs
    rt_match = script_rt == real_rt
    if pbs_match and rt_match:
        n_matched += 1
    print(row['variant_id'], row['pam_strand'],
          'script_pbs', script_pbs, 'real_pbs', real_pbs, 'MATCH' if pbs_match else 'MISMATCH',
          '| script_rt', script_rt, 'real_rt', real_rt, 'MATCH' if rt_match else 'MISMATCH')

print(f"\n{n_matched}/{n_checked} script candidates found byte-identical (modulo edit-base case) "
      f"in the real, independently-run PRIDICT2 CLI's own output for the same locus/strand/length.")
