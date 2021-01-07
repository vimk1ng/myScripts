#!/usr/bin/env python3
import sys
from os import path
import requests
import re

neo4jurl = 'http://localhost:7474/'
neo4juser = 'neo4j'
neo4jpass = 'BloodHound'

if len(sys.argv) != 3:
    print("Usage: {} filename domain".format(sys.argv[0]), file=sys.stderr)
    exit()

filename = sys.argv[1]
domain = sys.argv[2]

if not path.exists(filename):
    print("Invalid filename", file=sys.stderr)
    print("Usage: {} filename".format(sys.argv[0]), file=sys.stderr)
    exit()

cEnabled = 0
cDisabled = 0
cNotFound = 0
cBadRow = 0
reUsername = "^.*?\\\\(.+?):::.*$"

f = open(filename, 'r')
for c, searchLine in enumerate(f):
    reSU = re.search(reUsername, searchLine)
    if reSU:
        searchUser = reSU.group(1)
        #print("Trying {}".format(searchUser))
        query = {
            "statements": [ {
                "statement": "MATCH (n:User) WHERE n.name = '" + searchUser.upper().rstrip() + "@" + domain.upper() + "' RETURN n"
            } ]
        }

        res = requests.post(neo4jurl + 'db/data/transaction/commit', auth=(neo4juser, neo4jpass), json=query)
        if res.status_code == 401:
            print("Could not login to Neo4J. Please check the neo4jurl, neo4juser, and neo4jpass in the script.", file=sys.stderr)
            exit()
        resjson = res.json()
        try:
            for row in resjson['results'][0]['data'][0]['row']:
                #print("{} : {}".format(row['name'], row['enabled']))
                if row['enabled'] == True:
                    print("{}".format(searchLine.rstrip()))
                    cEnabled += 1
                else:
                    cDisabled += 1
        except:
            cNotFound += 1
            continue
    else:
        cBadRow += 1

f.close()

print("Search Completed. (Enabled: {}    Disabled: {}    Not Found: {}    Bad Rows: {})".format(cEnabled, cDisabled, cNotFound, cBadRow), file=sys.stderr)

