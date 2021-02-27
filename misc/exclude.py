#!/usr/bin/env python3
from netaddr import *
from os import path
import sys

def verifyIP(ip):
    if ip.count(".") != 3:
        return False
    else:
        for octet in ip.split("."):
            if int(octet) < 0 or int(octet) > 255:
                return False
    return True

def parseIP(addr):
    wCnt = addr.count("/")
    tCnt = addr.count("-")
    if (wCnt + tCnt) > 1:
        return False
    elif wCnt == 1:
        ip, sub = addr.split("/")
        if verifyIP(ip) and int(sub) >= 0 and int(sub) <= 32:
            return addr
        else:
            return False
    elif tCnt == 1:
        ip1, ip2 = addr.split("-")
        if ip2.count(".") == 0:
            ip2 = ip1[:ip1.rfind(".")+1] + ip2
        if verifyIP(ip1) and verifyIP(ip2):
            return IPRange(ip1,ip2)
        else:
            return False
    else:
        if verifyIP(addr):
            return addr
        else:
            return False

if len(sys.argv) != 4:
    print("Usage: {} include_file exclude_file output_file".format(sys.argv[0]))
    exit()

scopeFile = sys.argv[1]
excludeFile = sys.argv[2]
outputFile = sys.argv[3]

if not path.exists(scopeFile):
    print("File does not exist: {}".format(scopeFile), file=sys.stderr)
    exit()
if not path.exists(excludeFile):
    print("File does not exist: {}".format(excludeFile), file=sys.stderr)
    exit()

scopeList = IPSet()
excludeList = IPSet()

i = 0
with open(scopeFile,"r") as f:
    print("Reading {}...".format(scopeFile))
    for line in f.read().splitlines():
        i += 1
        if line != "":
            address = parseIP(line)
            if address:
                scopeList.add(address)
            else:
                print("Invalid scope address line: [{}] {}".format(i,line))
print("Initial scope size: {:,} IPs".format(len(scopeList)))

i = 0
with open(excludeFile,"r") as f:
    print("Reading {}...".format(excludeFile))
    for line in f.read().splitlines():
        i += 1
        if line != "":
            address = parseIP(line)
            if address:
                excludeList.add(address)
            else:
                print("Invalid exclusion address line: [{}] {}".format(i,line))
print("Exclusion size: {:,} IPs".format(len(excludeList)))

print("Calculating final scope...")
finalScope = scopeList ^ excludeList
print("Final scope size: {:,} IPs".format(len(finalScope)))

with open(outputFile, "w") as f:
    print("Writing output...")
    for iprange in finalScope.iter_ipranges():
        f.write(str(iprange) + "\n")

print("Done! New scope written to: {}".format(outputFile))