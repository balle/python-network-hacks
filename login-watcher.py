#!/usr/bin/python

import os
import re
import tailer
import random


logfile = "/var/log/auth.log"
max_failed = 3
max_failed_cmd = "/sbin/shutdown -h now"
failed_login = {}

success_patterns = [
    re.compile("Accepted password for (?P<user>.+?) from \
               (?P<host>.+?) port"),
    re.compile("session opened for user (?P<user>.+?) by"),
    ]

failed_patterns = [
    re.compile("Failed password for (?P<user>.+?) from \
               (?P<host>.+?) port"),
    re.compile("FAILED LOGIN (\(\d\)) on `(.+?)' FOR \
               `(?P<user>.+?)'"),
    re.compile("authentication failure\;.+?\
               user\=(?P<user>.+?)\s+.+?\s+user\=(.+)")
    ]

shutdown_msgs = [
    "Eat my shorts",
    "Follow the white rabbit",
    "System will explode in three seconds!",
    "Go home and leave me alone.",
    "Game... Over!"
    ]


def check_match(line, pattern, failed_login_check):
    found = False
    match = pattern.search(line)

    if(match != None):
        found = True
        failed_login.setdefault(match.group('user'), 0)

        # Remote login failed
        if(match.group('host') != None and failed_login_check):
            os.system("echo 'Login for user " + \
                      match.group('user') + \
                      " from host " + match.group('host') + \
                      " failed!' | festival --tts")
            failed_login[match.group('user')] += 1

        # Remote login successfull
        elif(match.group('host') != None and \
             not failed_login_check):
            os.system("echo 'User " + match.group('user') + \
                      " logged in from host " + \
                      match.group('host') + \
                      "' | festival --tts")
            failed_login[match.group('user')] = 0

        # Local login failed
        elif(match.group('user') != "CRON" and \
             failed_login_check):
            os.system("echo 'User " + match.group('user') + \
                          " logged in' | festival --tts")
            failed_login[match.group('user')] += 1

        # Local login successfull
        elif(match.group('user') != "CRON" and \
             not failed_login_check):
            os.system("echo 'User " + match.group('user') + \
                      " logged in' | festival --tts")
            failed_login[match.group('user')] = 0

        # Too many failed login?
        if failed_login[match.group('user')] >= max_failed:
            os.system("echo '" + random.choice(shutdown_msgs) + \
                      "' | festival --tts")
            os.system(max_failed_cmd)

    return found


for line in tailer.follow(open(logfile)):
    found = False

    for pattern in failed_patterns:
        found = check_match(line, pattern, True)
        if found: break

    if not found:
        for pattern in success_patterns:
            found = check_match(line, pattern, False)
            if found: break
