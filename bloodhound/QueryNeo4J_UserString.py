#!/usr/bin/env python3
import sys
from os import path
import requests

neo4jurl = 'http://localhost:7474/'
neo4juser = 'neo4j'
neo4jpass = 'Bloodhound'

if len(sys.argv) != 2:
    print("Usage: {} string".format(sys.argv[0]))
    exit()

searchString = sys.argv[1]

query = {
    "statements": [ {
        "statement": "MATCH (n:User) WHERE n.name contains '" + searchString.upper() + "' RETURN n"
    } ]
}

res = requests.post(neo4jurl + 'db/data/transaction/commit', auth=(neo4juser, neo4jpass), json=query)
resjson = res.json()
try:
    for data in resjson['results'][0]['data']:
        print("{} : {}".format(data['row'][0]['name'], data['row'][0]['enabled']))
except:
    pass
