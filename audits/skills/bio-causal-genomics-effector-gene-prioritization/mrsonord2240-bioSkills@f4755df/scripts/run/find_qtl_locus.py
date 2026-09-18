import json
import urllib.request

GQL_URL = "https://api.platform.opentargets.org/api/v4/graphql"

Q = """
query FindQtlLocus {
  credibleSets(studyTypes: [eqtl], page: {index: 0, size: 3}) {
    count
    rows { studyLocusId studyId studyType }
  }
}
"""

def gql(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    req = urllib.request.Request(GQL_URL, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.load(resp)
    if "errors" in body:
        raise RuntimeError(f"GraphQL error: {body['errors']}")
    return body["data"]

data = gql(Q)
print(json.dumps(data, indent=2))
