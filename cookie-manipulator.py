#!/usr/bin/python

import sys
import httplib2

if len(sys.argv) < 3:
    print sys.argv[0] + ": &lt;url&gt; <key> <value>"
    sys.exit(1)

webclient = httplib2.Http()
headers = {'Cookie': sys.argv[2] + '=' + sys.argv[3]}
response, content = webclient.request(sys.argv[1],
                                      'GET',
                                      headers=headers)
print content
