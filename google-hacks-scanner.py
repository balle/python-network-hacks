#!/usr/bin/python

import re
import sys
import google
import urllib2

if len(sys.argv) < 2:
    print sys.argv[0] + ": <dict>"
    sys.exit(1)

fh = open(sys.argv[1])

for word in fh.readlines():
    print "\nSearching for " + word.strip()
    results = google.search(word.strip())

    try:
        for link in results:
            if re.search("youtube", link) == None: print  link
    except KeyError:
        pass
    except urllib2.HTTPError, e:
        print "Google search failed: " + str(e)
