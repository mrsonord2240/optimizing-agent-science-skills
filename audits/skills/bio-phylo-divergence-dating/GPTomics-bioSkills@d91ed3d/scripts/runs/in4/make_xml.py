"""Input 4: BEAST 2.7 XML (hand-written; BEAUti is GUI-only) for the SYNTHETIC 8-taxon locus loc1.
Ages in Myr. Strict clock, HKY+G4, Yule; calibrations: (A,B) offset-lognormal minimum 15 Ma,
(G,H) uniform 35-55 Ma, root uniform 80-120 Ma. Writes withdata.xml and prioronly.xml
(identical except sampleFromPrior="true", the Skill's edit)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "data")
seqs = {}
name = None
for line in open(os.path.join(DATA, "loc1.fa")):
    line = line.strip()
    if line.startswith(">"):
        name = line[1:]
        seqs[name] = ""
    elif name:
        seqs[name] += line

NS = ("beast.base.core:beast.base.inference:beast.base.evolution.alignment:beast.base.evolution.tree:"
      "beast.base.evolution.tree.coalescent:beast.base.util:beast.base.math:beast.base.evolution.operator:"
      "beast.base.inference.operator:beast.base.evolution.sitemodel:beast.base.evolution.substitutionmodel:"
      "beast.base.evolution.likelihood:beast.base.evolution.branchratemodel:beast.base.evolution.speciation:"
      "beast.base.inference.distribution:beast.base.inference.parameter")


def taxset(tid, members, first):
    inner = "".join((f'<taxon id="{m}" spec="Taxon"/>' if m not in first else f'<taxon idref="{m}"/>')
                    for m in members)
    first.update(members)
    return f'<taxonset id="{tid}" spec="TaxonSet">{inner}</taxonset>'


def xml(sample_from_prior):
    seen = set()
    ts = [taxset("AB", ["A", "B"], seen), taxset("GH", ["G", "H"], seen),
          taxset("ALL", ["A", "B", "C", "D", "E", "F", "G", "H"], seen)]
    sfp = ' sampleFromPrior="true"' if sample_from_prior else ""
    data = "\n".join(f'    <sequence taxon="{k}" value="{v}"/>' for k, v in sorted(seqs.items()))
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<beast version="2.7" namespace="{NS}">
<data id="alignment" spec="Alignment" dataType="nucleotide">
{data}
</data>
{ts[0]}
{ts[1]}
{ts[2]}
<run id="mcmc" spec="MCMC" chainLength="2000000"{sfp}>
  <state id="state" storeEvery="5000">
    <tree id="tree" spec="beast.base.evolution.tree.Tree" name="stateNode"><taxonset spec="TaxonSet" alignment="@alignment"/></tree>
    <parameter id="kappa" spec="parameter.RealParameter" lower="0.0" name="stateNode">2.0</parameter>
    <parameter id="gammaShape" spec="parameter.RealParameter" lower="0.0" name="stateNode">1.0</parameter>
    <parameter id="clockRate" spec="parameter.RealParameter" lower="0.0" name="stateNode">0.001</parameter>
    <parameter id="birthRate" spec="parameter.RealParameter" lower="0.0" name="stateNode">0.01</parameter>
  </state>
  <init spec="beast.base.evolution.tree.TreeParser" initial="@tree" taxa="@alignment" IsLabelledNewick="true"
        newick="(((A:25,B:25):35,(C:30,D:30):30):40,((E:20,F:20):50,(G:40,H:40):30):30);"/>
  <distribution id="posterior" spec="CompoundDistribution">
    <distribution id="prior" spec="CompoundDistribution">
      <distribution id="YuleModel" spec="YuleModel" tree="@tree" birthDiffRate="@birthRate"/>
      <distribution id="birthRatePrior" spec="Prior" x="@birthRate"><distr spec="Exponential" mean="0.1"/></distribution>
      <distribution id="kappaPrior" spec="Prior" x="@kappa"><distr spec="LogNormalDistributionModel" M="1.0" S="1.25"/></distribution>
      <distribution id="gammaShapePrior" spec="Prior" x="@gammaShape"><distr spec="Exponential" mean="1.0"/></distribution>
      <distribution id="clockRatePrior" spec="Prior" x="@clockRate"><distr spec="LogNormalDistributionModel" M="-6.0" S="1.0"/></distribution>
      <distribution id="AB.prior" spec="MRCAPrior" tree="@tree" taxonset="@AB" monophyletic="true">
        <distr spec="LogNormalDistributionModel" offset="15.0" M="1.0" S="1.0"/></distribution>
      <distribution id="GH.prior" spec="MRCAPrior" tree="@tree" taxonset="@GH" monophyletic="true">
        <distr spec="beast.base.inference.distribution.Uniform" lower="35.0" upper="55.0"/></distribution>
      <distribution id="root.prior" spec="MRCAPrior" tree="@tree" taxonset="@ALL">
        <distr spec="beast.base.inference.distribution.Uniform" lower="80.0" upper="120.0"/></distribution>
    </distribution>
    <distribution id="likelihood" spec="CompoundDistribution">
      <distribution id="treeLikelihood" spec="TreeLikelihood" data="@alignment" tree="@tree">
        <siteModel id="siteModel" spec="SiteModel" gammaCategoryCount="4" shape="@gammaShape">
          <substModel id="hky" spec="HKY" kappa="@kappa"><frequencies spec="Frequencies" data="@alignment"/></substModel>
        </siteModel>
        <branchRateModel id="clock" spec="StrictClockModel" clock.rate="@clockRate"/>
      </distribution>
    </distribution>
  </distribution>
  <operator spec="ScaleOperator" parameter="@kappa" scaleFactor="0.5" weight="1"/>
  <operator spec="ScaleOperator" parameter="@gammaShape" scaleFactor="0.5" weight="1"/>
  <operator spec="ScaleOperator" parameter="@clockRate" scaleFactor="0.75" weight="3"/>
  <operator spec="ScaleOperator" parameter="@birthRate" scaleFactor="0.75" weight="3"/>
  <operator spec="UpDownOperator" scaleFactor="0.75" weight="3" up="@clockRate" down="@tree"/>
  <operator spec="ScaleOperator" tree="@tree" scaleFactor="0.75" weight="3"/>
  <operator spec="ScaleOperator" tree="@tree" rootOnly="true" scaleFactor="0.75" weight="3"/>
  <operator spec="Uniform" tree="@tree" weight="30"/>
  <operator spec="SubtreeSlide" tree="@tree" weight="15"/>
  <operator spec="Exchange" tree="@tree" isNarrow="true" weight="15"/>
  <operator spec="Exchange" tree="@tree" isNarrow="false" weight="3"/>
  <operator spec="WilsonBalding" tree="@tree" weight="3"/>
  <logger id="tracelog" fileName="dating.log" logEvery="1000">
    <log idref="posterior"/><log idref="likelihood"/><log idref="prior"/>
    <log spec="beast.base.evolution.tree.TreeHeightLogger" tree="@tree"/>
    <log idref="AB.prior"/><log idref="GH.prior"/><log idref="root.prior"/>
    <log idref="clockRate"/><log idref="kappa"/><log idref="gammaShape"/><log idref="birthRate"/>
  </logger>
  <logger id="treelog" fileName="dating.trees" logEvery="1000" mode="tree"><log idref="tree"/></logger>
  <logger id="screenlog" logEvery="200000"><log idref="posterior"/><log idref="likelihood"/><log idref="prior"/></logger>
</run>
</beast>
"""


for fn, sfp in (("withdata.xml", False), ("prioronly.xml", True)):
    open(os.path.join(HERE, fn), "w", encoding="utf-8", newline="\n").write(xml(sfp))
    print("wrote", fn)
