#!/usr/bin/python3

import sys
import getopt
import requests

def usage():
    print(sys.argv[0] + """
    -f <query_file>
    -F(ile_mode)
    -h <host>
    -p <port>""")
    sys.exit(0)


# Try to get url from server
def surf(url, query):
        print("GET " + query)

        try:
                r = requests.get(url)

                if r.status_code == 200:
                        print("FOUND " + query)
        except requests.exceptions.ConnectionError as e:
                print("Got error for " + url + \
                      ": " + str(e))
                sys.exit(1)


# Dictionary file
query_file = "web-queries.txt"

# Target http server and port
host = None
port = 80

# Run in file mode?
file_mode = False

# Parsing parameter
try:
    cmd_opts = "f:Fh:p:"
    opts, args = getopt.getopt(sys.argv[1:], cmd_opts)
except getopt.GetoptError:
    usage()

for opt in opts:
    if opt[0] == "-f":
        query_file = opt[1]
    elif opt[0] == "-F":
        file_mode = True
    elif opt[0] == "-h":
        host = opt[1]
    elif opt[0] == "-p":
        port = opt[1]

if not host:
    usage()

if port == 443:
    url = "https://" + host
elif port != 80:
    url = "http://" + host + ":" + port
else:
    url = "http://" + host

# This pattern will be added to each query
salts = ('~', '~1', '.back', '.bak',
         '.old', '.orig', '_backup')

# Read dictionary and handle each query
for query in open(query_file):
        query = query.strip("\n")

        # Try dictionary traversal
        for dir_sep in ['/', '//', '/test/../']:
                url += dir_sep + query

                if file_mode:
                        for salt in salts:
                                url += salt
                                surf(url,
                                     dir_sep + query + salt)
                else:
                        surf(url, dir_sep + query)
