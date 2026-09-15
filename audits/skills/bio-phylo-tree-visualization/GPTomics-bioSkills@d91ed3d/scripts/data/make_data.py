"""Generate SYNTHETIC inputs for the bio-phylo-tree-visualization audit (2026-09-15).

Outputs (all synthetic, known truth):
  primates16_true.nwk      known 16-taxon primate-named tree (subs/site)
  primates16_aln.fa        AliSim HKY+G4 1000 bp alignment simulated on it
  iq/primates16.treefile   IQ-TREE 2.4.0 ML tree with SH-aLRT/UFBoot node labels
  big320.nwk               320-tip birth-death tree (DendroPy, seed 20260915), realistic isolate names
  big320_meta.tsv          per-tip metadata (host, year, lineage) for ring/strip annotation
  beast_mcc.tree           hand-written BEAST2/TreeAnnotator-format MCC Nexus (height_95%_HPD, posterior) built
                           from a known ultrametric 10-taxon time tree
  beast_truth.tsv          true node ages used to build it
Run from this folder: python make_data.py
"""
import os, random, subprocess, sys
import dendropy

HERE = os.path.dirname(os.path.abspath(__file__))
IQ = r'F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\tools\bin\iqtree2.exe'
random.seed(20260915)

# 1. 16-taxon tree -> AliSim -> IQ-TREE (SH-aLRT/UFBoot labels)
TRUE16 = ('((((((((Homo_sapiens:0.020,(Pan_troglodytes:0.008,Pan_paniscus:0.008):0.012):0.004,'
          'Gorilla_gorilla:0.030):0.012,Pongo_abelii:0.050):0.010,Hylobates_lar:0.060):0.020,'
          '(((Macaca_mulatta:0.020,Papio_anubis:0.020):0.010,Chlorocebus_sabaeus:0.035):0.010,'
          'Colobus_guereza:0.050):0.020):0.030,((Callithrix_jacchus:0.050,Saimiri_boliviensis:0.050):0.008,'
          'Aotus_nancymaae:0.055):0.040):0.050,Tarsius_syrichta:0.150):0.020,'
          '(Microcebus_murinus:0.100,Otolemur_garnettii:0.110):0.050);')
with open(os.path.join(HERE, 'primates16_true.nwk'), 'w', encoding='utf-8') as f:
    f.write(TRUE16 + '\n')
os.makedirs(os.path.join(HERE, 'iq'), exist_ok=True)
if not os.path.exists(os.path.join(HERE, 'iq', 'primates16.treefile')):
    subprocess.run([IQ, '--alisim', os.path.join(HERE, 'primates16_aln'), '-t', os.path.join(HERE, 'primates16_true.nwk'),
                    '-m', 'HKY{2.5}+G4{0.5}', '--length', '1000', '--seed', '7', '-af', 'fasta', '-redo'],
                   check=True, cwd=HERE, stdout=subprocess.DEVNULL)
    subprocess.run([IQ, '-s', os.path.join(HERE, 'primates16_aln.fa'), '-m', 'MFP', '-B', '1000', '-alrt', '1000',
                    '-T', '4', '--seed', '12345', '--prefix', os.path.join(HERE, 'iq', 'primates16'), '-redo'],
                   check=True, cwd=HERE, stdout=open(os.path.join(HERE, 'iq', 'primates16.stdout'), 'w'))

# 2. 320-tip birth-death tree with isolate-style names + metadata
rng = random.Random(20260915)
t = dendropy.model.birthdeath.birth_death_tree(birth_rate=1.0, death_rate=0.3, num_extant_tips=320, rng=rng)
hosts = ['Human', 'Bat', 'Pangolin', 'Civet', 'Camel']
rows = ['label\thost\tyear\tlineage']
for i, leaf in enumerate(t.leaf_node_iter(), 1):
    host = rng.choice(hosts); year = rng.randint(2012, 2024)
    name = f'CoV_{host}_{rng.choice(["CHN","KEN","SAU","USA","VNM","BRA"])}_{i:03d}_{year}'
    leaf.taxon.label = name
    rows.append(f'{name}\t{host}\t{year}\tL{(i * 7) % 6 + 1}')
t.write(path=os.path.join(HERE, 'big320.nwk'), schema='newick', suppress_rooting=True, unquoted_underscores=True)
with open(os.path.join(HERE, 'big320_meta.tsv'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(rows) + '\n')

# 3. BEAST2 TreeAnnotator-style MCC tree (hand-built from a known time tree; SYNTHETIC)
# (name, children, age Ma, posterior, HPD half-width fraction)
taxa = ['Anolis_carolinensis', 'Gallus_gallus', 'Taeniopygia_guttata', 'Alligator_mississippiensis',
        'Chelonia_mydas', 'Homo_sapiens', 'Mus_musculus', 'Canis_lupus', 'Monodelphis_domestica',
        'Ornithorhynchus_anatinus']
# internal nodes: (left, right, age, posterior)
nodes = {
    'birds': (('T', 1), ('T', 2), 95.0, 1.00),
    'archo': (('N', 'birds'), ('T', 3), 245.0, 1.00),
    'archelo': (('N', 'archo'), ('T', 4), 255.0, 0.62),
    'saur': (('T', 0), ('N', 'archelo'), 280.0, 0.97),
    'euarch': (('T', 5), ('T', 6), 90.0, 1.00),
    'boreo': (('N', 'euarch'), ('T', 7), 96.0, 0.88),
    'ther': (('N', 'boreo'), ('T', 8), 160.0, 1.00),
    'mamm': (('N', 'ther'), ('T', 9), 180.0, 0.99),
    'root': (('N', 'saur'), ('N', 'mamm'), 318.0, 1.00),
}
truth = ['node\ttrue_age_Ma\tposterior\thpd_low\thpd_high']

def fmt(x):
    return f'{x:.6g}'

def build(ref, parent_age):
    kind, key = ref
    if kind == 'T':
        idx = key + 1
        ann = (f'[&height=0.0,height_95%_HPD={{0.0,0.0}},height_median=0.0,height_range={{0.0,0.0}},'
               f'length={fmt(parent_age)},length_95%_HPD={{{fmt(parent_age*0.8)},{fmt(parent_age*1.2)}}},posterior=1.0]')
        return f'{idx}{ann}:{fmt(parent_age)}'
    l, r, age, post = nodes[key]
    w = 0.08 + 0.10 * (1 - post) * 3  # weaker nodes get wider HPD
    lo, hi = age * (1 - w), age * (1 + w * 0.8)
    truth.append(f'{key}\t{age}\t{post}\t{lo:.2f}\t{hi:.2f}')
    ann = (f'[&height={fmt(age)},height_95%_HPD={{{fmt(round(lo,4))},{fmt(round(hi,4))}}},height_median={fmt(age)},'
           f'height_range={{{fmt(round(lo*0.9,4))},{fmt(round(hi*1.1,4))}}},posterior={post}]')
    inner = f'({build(l, age)},{build(r, age)})'
    if key == 'root':
        return inner + ann
    return inner + ann + f':{fmt(parent_age - age)}'

# tip branch lengths = parent age (tips at 0), internal = parent - child age
def build_root():
    l, r, age, post = nodes['root']
    return build(('N', 'root'), age)

# fix tip lengths: build() passes parent_age for tips which is correct (tip height 0)
newick = build_root()
lines = ['#NEXUS', '', 'Begin taxa;', f'\tDimensions ntax={len(taxa)};', '\t\tTaxlabels']
lines += [f'\t\t\t{t_}' for t_ in taxa] + ['\t\t\t;', 'End;', 'Begin trees;', '\tTranslate']
lines += [f'\t\t{i+1} {t_}' + (',' if i < len(taxa) - 1 else '') for i, t_ in enumerate(taxa)]
lines += [';', f'tree TREE1 = [&R] {newick};', 'End;', '']
with open(os.path.join(HERE, 'beast_mcc.tree'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
with open(os.path.join(HERE, 'beast_truth.tsv'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(truth) + '\n')

# 4. SYNTHETIC trait table for the 16 primates (for heatmap columns; values invented, not real biology data)
tips16 = [x.split(':')[0].strip('(') for x in TRUE16.replace(')', ',').split(',') if x.strip('();') and x.strip('(')[0].isalpha()]
diets = {'Homo': 'Omnivore', 'Pan': 'Frugivore', 'Gorilla': 'Folivore', 'Pongo': 'Frugivore', 'Hylobates': 'Frugivore',
         'Macaca': 'Omnivore', 'Papio': 'Omnivore', 'Chlorocebus': 'Omnivore', 'Colobus': 'Folivore',
         'Callithrix': 'Gummivore', 'Saimiri': 'Insectivore', 'Aotus': 'Frugivore', 'Tarsius': 'Insectivore',
         'Microcebus': 'Omnivore', 'Otolemur': 'Insectivore'}
with open(os.path.join(HERE, 'primates16_traits.tsv'), 'w', encoding='utf-8') as f:
    f.write('label\tdiet\tlog10_mass_g\n')
    for tip in tips16:
        f.write(f'{tip}\t{diets[tip.split("_")[0]]}\t{rng.uniform(1.8, 5.2):.2f}\n')

# 5. MrBayes 3.2.7a posterior consensus on the same alignment (short chain; SYNTHETIC)
MB = r'F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\tools\bin\mb.exe'
mbdir = os.path.join(HERE, 'mb')
if not os.path.exists(os.path.join(mbdir, 'primates16.nex.con.tre')):
    os.makedirs(mbdir, exist_ok=True)
    from Bio import AlignIO
    aln = AlignIO.read(os.path.join(HERE, 'primates16_aln.fa'), 'fasta')
    for rec in aln:
        rec.annotations['molecule_type'] = 'DNA'
    AlignIO.write(aln, os.path.join(mbdir, 'primates16.nex'), 'nexus')
    with open(os.path.join(mbdir, 'run.mb'), 'w', encoding='utf-8') as f:
        f.write('set autoclose=yes nowarn=yes seed=11 swapseed=11;\nexecute primates16.nex;\nlset nst=2 rates=gamma;\n'
                'outgroup Otolemur_garnettii;\nmcmc ngen=30000 samplefreq=100 nruns=2 nchains=2 printfreq=10000;\n'
                'sumt burnin=75;\nquit;\n')
    subprocess.run([MB, 'run.mb'], check=True, cwd=mbdir, stdout=open(os.path.join(mbdir, 'mb.stdout'), 'w'))
print('done')
