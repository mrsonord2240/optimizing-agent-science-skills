#!/usr/bin/env bash
# Live, public, unauthenticated Open Targets Platform GraphQL API calls (allowed per
# the audit brief). Verifies the SKILL.md-documented "modern" L2G query shape against
# the LIVE schema via introspection, then a real credibleSet lookup for PCSK9.
set -euo pipefail
GQL="https://api.platform.opentargets.org/api/v4/graphql"

# 1. Confirm credibleSet/credibleSets exist on Query (matches SKILL.md's
#    `credibleSet(studyLocusId)` entry point).
curl -s -X POST "$GQL" -H "Content-Type: application/json" \
  -d '{"query":"query { __schema { queryType { fields(includeDeprecated: true) { name } } } }"}'
echo

# 2. Confirm CredibleSet.l2GPredictions and its nested shape (L2GPredictions.rows ->
#    L2GPrediction { studyLocusId, features, shapBaseValue, score, target }) match
#    SKILL.md's documented modern query exactly.
curl -s -X POST "$GQL" -H "Content-Type: application/json" \
  -d '{"query":"query { __type(name: \"CredibleSet\") { fields { name } } }"}'
echo
curl -s -X POST "$GQL" -H "Content-Type: application/json" \
  -d '{"query":"query { __type(name: \"L2GPrediction\") { fields { name } } }"}'
echo

# 3. Real lookup: PCSK9's credible sets (target ENSG00000169174), with counts by
#    studyType. Result: 46 credible sets, all pqtl/eqtl/tuqtl (23/20/3); NONE of the
#    sampled rows had l2GPredictions computed (count=0) -- L2G is populated for GWAS
#    trait loci, not molecular-QTL credible sets, in the current Platform release.
#    This is a genuine, useful finding: an agent following the Skill verbatim on a
#    gene like PCSK9 needs to know to look up GWAS-type (not QTL-type) credible sets,
#    which the Skill does not explicitly say.
curl -s -X POST "$GQL" -H "Content-Type: application/json" \
  -d '{"query":"query{ target(ensemblId:\"ENSG00000169174\"){ approvedSymbol credibleSets(page:{index:0,size:46}){ count rows{ studyLocusId studyId studyType l2GPredictions{count} } } } }"}'
echo
