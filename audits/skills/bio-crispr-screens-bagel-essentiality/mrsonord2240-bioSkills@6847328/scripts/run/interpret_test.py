import pandas as pd
import warnings

ASSAY_CONTROLS = {'LacZ', 'luciferase', 'EGFP'}

def interpret_bagel(bf_path, bf_essential=6, bf_tumor_suppressor=-6,
                     screen_type='dropout', control_genes=ASSAY_CONTROLS,
                     tumor_suppressor_frac_warn=0.05):
    df = pd.read_csv(bf_path, sep='\t')
    df = df[~df['GENE'].isin(control_genes)].copy()
    df['call'] = 'neutral'
    df.loc[df['BF'] > bf_essential, 'call'] = 'essential'
    if screen_type in ('enrichment', 'both'):
        df.loc[df['BF'] < bf_tumor_suppressor, 'call'] = 'tumor_suppressor'
        frac = (df['call'] == 'tumor_suppressor').mean()
        if frac > tumor_suppressor_frac_warn:
            warnings.warn(
                f"{frac:.1%} of genes flagged tumor_suppressor -- implausibly high; "
                "this usually means a dropout-only screen is being scored for "
                "enrichment. Re-check screen_type and BF<-6 calls against literature "
                "before reporting."
            )
    return df.sort_values('BF', ascending=False)

print("=== default (screen_type='dropout') ===")
r1 = interpret_bagel('bayes_factor.txt')
print("calls:", r1['call'].value_counts().to_dict())
print("LacZ/luciferase/EGFP present:", set(['LacZ','luciferase','EGFP']) & set(r1['GENE']))

print()
print("=== screen_type='enrichment' ===")
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    r2 = interpret_bagel('bayes_factor.txt', screen_type='enrichment')
    print("calls:", r2['call'].value_counts().to_dict())
    print("warnings fired:", [str(x.message)[:80] for x in w])
print("bottom 10 by BF (most negative):")
print(r2.nsmallest(10, 'BF')[['GENE','BF','call']].to_string(index=False))
