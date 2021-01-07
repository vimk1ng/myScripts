#!/usr/bin/env python3
import sys
from os import path
import requests

neo4jurl = 'http://localhost:7474/'
neo4juser = 'neo4j'
neo4jpass = 'BloodHound'

if len(sys.argv) != 2:
    print("Usage: {} filename".format(sys.argv[0]))
    exit()

filename = sys.argv[1]

if not path.exists(filename):
    print("Invalid filename")
    print("Usage: {} filename".format(sys.argv[0]))
    exit()

f = open(filename, 'r')
for c, searchUser in enumerate(f):
    query = {
        "statements": [ {
            "statement": "MATCH (n:User) WHERE n.name = '" + searchUser.upper().rstrip() + "' RETURN n"
        } ]
    }

    res = requests.post(neo4jurl + 'db/data/transaction/commit', auth=(neo4juser, neo4jpass), json=query)
    resjson = res.json()
    try:
        for row in resjson['results'][0]['data'][0]['row']:
            print("{} : {}".format(row['name'], row['enabled']))
    except:
        continue

f.close()
