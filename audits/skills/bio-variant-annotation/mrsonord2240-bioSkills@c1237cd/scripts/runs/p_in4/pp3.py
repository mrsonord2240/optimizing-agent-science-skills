"""Input 4: one calibrated predictor for PP3/BP4 (SKILL.md 'Pathogenicity predictors').
Scores are a SYNTHETIC example variant, not a real one."""
variant = {'SIFT': 0.01, 'PolyPhen2': 0.95, 'CADD_phred': 21.0, 'REVEL': 0.70}

# REVEL thresholds exactly as SKILL.md states them (Pejaver 2022; Moderate/Strong flagged 'verify').
def revel_strength(s):
    if s >= 0.932: return 'PP3_Strong'
    if s >= 0.773: return 'PP3_Moderate'
    if s >= 0.644: return 'PP3_Supporting'
    if s <= 0.016: return 'BP4_Strong'
    if s <= 0.183: return 'BP4_Moderate'
    if s <= 0.290: return 'BP4_Supporting'
    return 'indeterminate (no PP3/BP4)'

print('Stacked legacy report :', ', '.join(f'{k}={v}' for k, v in variant.items()), '-> "4 lines of damaging evidence"')
print('Skill rule            : ONE calibrated missense predictor ->', 'REVEL', variant['REVEL'], '=>', revel_strength(variant['REVEL']))
print('Not counted           : SIFT/PolyPhen (components of REVEL), CADD (genome-wide ranking tool, not missense PP3)')
for s in (0.29, 0.30, 0.644, 0.773, 0.932, 0.016):
    print(f'  REVEL {s:<6} -> {revel_strength(s)}')
