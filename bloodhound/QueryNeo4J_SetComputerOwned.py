#!/usr/bin/env python3
import sys
from os import path
import requests

neo4jurl = 'http://localhost:7474/'
neo4juser = 'neo4j'
neo4jpass = 'BloodHound'

if len(sys.argv) != 2:
    print("Usage: {} string".format(sys.argv[0]))
    exit()

searchString = sys.argv[1]

query = {
    "statements": [ {
        "statement": "MATCH (n:Computer) WHERE n.name = '" + searchString.upper() + "' SET n.owned = True"
    } ]
}

res = requests.post(neo4jurl + 'db/data/transaction/commit', auth=(neo4juser, neo4jpass), json=query)

status = "Failed"
if res.status_code == 200:
    status = "Success"

print("{} - {}".format(searchString.upper(), status))
