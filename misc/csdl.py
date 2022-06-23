#!/usr/bin/env python3
import requests
import os
import re
import tempfile
import tarfile

baseurl = 'https://download.cobaltstrike.com'
key = os.environ['COBALT_STRIKE_KEY']

sess = requests.Session()

resp = sess.post(f"{baseurl}/download", 
    data={
        'dlkey':key
    },
    headers={
        'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36'
    })

r = re.findall('\/(\w+\/[a-z0-9]{32}\/\w+)\/', resp.text)

resp = sess.get(f"{baseurl}/{r[0]}/cobaltstrike-dist.tgz")

fd, cspath = tempfile.mkstemp(suffix='.tgz',prefix='cstrike_')
with os.fdopen(fd, 'wb') as f:
    f.write(resp.content)

tf = tarfile.open(cspath)
tf.extractall('/opt')
tf.close()

os.remove(cspath)