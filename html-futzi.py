#!/usr/bin/python

import re
import cgi
import os
import urllib
import random
import string
from datetime import datetime

logfile = "html-futzi.log"

tags = ('a', 'table', 'tr', 'td', 'th', 'br', 'hr',
        'b', 'i', 'u', 'strike', 'blink', 'sup', 'sub',
        'tt', 'p', 'div', 'span', 'layer', 'small', 'big',
        'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7',
        'center', 'nobr', 'blockquote', 'ul', 'ol', 'li',
        'abbr', 'acronym', 'address', 'applet', 'area',
        'base', 'basefont', 'bdo', 'title', 'meta', 'script',
        'body', 'html', 'head', 'caption', 'button', 'cite',
        'code', 'col', 'colgroup', 'dd', 'del', 'dfn', 'dir',
        'dl', 'dt', 'em', 'fieldset', 'frame', 'iframe', 'form',
        'input', 'ins', 'isindex', 'kbd', 'label', 'legend',
        'link', 'map', 'menu', 'noframes', 'noscript', 'object',
        'optgroup', 'option', 'param', 'pre', 'q', 's', 'samp',
        'select', 'strong', 'style', 'tbody', 'textarea', 'tfoot',
        'thead', 'var')

attrs = ('accesskey', 'charset', 'id', 'idref', 'name', 'class',
         'style', 'titlle', 'dir', 'lang', 'onclick', 'ondblclick',
         'onmousedown', 'onmouseup', 'onmouseover', 'onmousemove',
         'onkeypress', 'onkeydown', 'onkeyup', 'coords', 'href',
         'hreflang', 'onblur', 'onfocus', 'rel', 'rev', 'shape',
         'tabindex', 'target', 'type', 'align', 'alt', 'archive',
         'code', 'codebase', 'height', 'hspace', 'object', 'vspace',
         'width', 'nohref', 'color', 'face', 'size', 'dir', 'cite',
         'alink', 'background', 'bgcolor', 'onload', 'onunload',
         'text', 'vlink', 'clear', 'disabled', 'value', 'valign',
         'span', 'char', 'charoff', 'datetime', 'compact', 'action',
         'accept', 'method', 'accept-charset', 'enctype', 'onreset',
         'onsubmit', 'frameborder', 'border', 'longdesc',
         'marginwidth', 'marginheight', 'noresize', 'noscrolling',
         'src', 'cols', 'rows', 'profile', 'noshade', 'version',
         'hspace', 'ismap', 'usemap', 'checked', 'maxlength',
         'readonly', 'onselect', 'prompt', 'for', 'media',
         'content', 'http-equiv',  'scheme', 'classid', 'data',
         'declare', 'standby', 'start', 'label', 'valuetype',
         'defer', 'event', 'multiple', 'cellpadding',
         'cellspacing', 'frame', 'rules', 'summary', 'abbr',
         'axis', 'colspan', 'headers', 'nowrap', 'rowspan',
         'scope')
delimiters = ('"', "'", " ")
boundaries = (0, 262, 1032, 2056, 4104, 8200)

num_list = range(0, 9)
char_num_list = [x for x in string.lowercase] + num_list
#char_num_list = [x for x in string.printables] + num_list

char_utf_map = {' ': "%u0020", '/': "%u2215", '\\': "%u2215",
                "'": "%u02b9", '"': "%u0022", '>': "%u003e",
                '<': "%u003c", '#': "%uff03", '!': "%uff01",
                '$': "%uff04", '*': "%uff0a", '@': "%u0040",
                '.': "%uff0e", '_': "%uff3f", '(': "%uff08",
                ')': "%uff09", ',': "%uff0c", '%': "%u0025",
                '-': "%uff0d", ';': "%uff1b", ':': "%uff1a",
                '|': "%uff5c", '&': "%uff06", '+': "%uff0b",
                '=': "%uff1d"}

params = cgi.FieldStorage()
brute_limit = int(params.getvalue("limit", 666))
brute_step = int(params.getvalue("step", 23))
dolog = int(params.getvalue("log", 1))
log = None
if dolog: log = open(logfile, "w")


def print_to_browser(input):
    out = re.sub("<", "&lt;", input)
    out = re.sub(">", "&gt;", out)
    out = re.sub("%", "&percent;", out)

    if dolog:
        log.write("[" + \
                  datetime.now().strftime("%d.%m.%Y %H:%M:%S") + \
                  "] " + input + "\n")

    print out + "<br>"
    print input


def print_encoded(input):
    enc = urllib.quote(input)
    print_to_browser(enc)

    enc = ""

    for char in input:
        if char_utf_map.get(char) != None:
            enc += "%u" + char_utf_map[char]
        else:
            enc += char

    print_to_browser(enc)


def play_with(code):
    print_to_browser(code)
    print_encoded(code)


def redirect(i, x):
    print_to_browser("<script>location.href=\"http://" + \
                     os.environ.get("HTTP_HOST") + \
                     "/cgi-bin/html-futzi.py?use_standard=" + \
                     str(params.getvalue("use_standard", 0)) + \
                    "&limit=" + str(brute_limit) + \
                    "&step=" + str(brute_step) + \
                    "&log=" + str(dolog) + \
                     "&i=" + str(i) + "&x=" + str(x) + \
                     "\";</script>")


def fuzz(tag, attr="", eq_sign="", del1="", val="", del2=""):
    # <tag>
    code = "<" + tag + attr + eq_sign + del1 + val + del2 + ">"
    play_with(code)

    # <tag/>
    code = "<" + tag + attr + eq_sign + del1 + val + del2 + "/>"
    play_with(code)

    # <tag></tag>
    code = "<" + tag + attr + eq_sign + del1 + val + del2 + \
        "> </" + tag + ">"
    play_with(code)

    # tag>
    code = tag + attr + eq_sign + del1 + val + del2 + ">"
    play_with(code)

    # <tag
    code = "<" + tag + attr + eq_sign + del1 + val + del2
    play_with(code)

    # <<<<<<<<<<tag>
    code = "<" * 10 + tag + attr + eq_sign + del1 + val + del2 + ">"
    play_with(code)

    # <tag>>>>>>>>>>>
    code = "<" + tag + attr + eq_sign + del1 + val + del2 + ">" * 10
    play_with(code)

    # <tag//////////>
    code = "<" + tag + attr + eq_sign + del1 + val + del2 + "/" * 10 + ">"
    play_with(code)

    # <tag\n>
    code = "<" + tag + attr + eq_sign + del1 + val + del2 + "\n>"
    play_with(code)

    # <\r\ntag>
    code = "<\r\n" + tag + attr + eq_sign + del1 + val + del2 + ">"
    play_with(code)


def get_rand(nr, possibilities):
    result = ""

    for count in range(0, nr):
        x = random.choice(possibilities)
        result += str(x)

    return result


print "Content-type: text/html\n\n"

if params.getvalue("use_standard") == "1":
    print """
    <html>
      <head>
       <title>HTML Futzi</title>
      </head>
    <body>
    """

    for tag in tags:
        fuzz(tag)

        for attr in attrs:
            for d1 in delimiters:
                for d2 in delimiters:
                    for boundary in boundaries:
                        val = get_rand(boundary, char_num_list)
                        fuzz(tag, " " + attr, '=', d1, val, d2)

    print """
    </body>
    </html>
    """
else:
    # Bruteforce mode
    tag = ""
    i = int(params.getvalue("i", 0))

    while i <= brute_limit:
        tag = get_rand(i, char_num_list)
        attr = ""
        x = int(params.getvalue("x", 0))

#        if x == 0:
#            print "<br><br>MUH<br><br>"
        fuzz(tag)

        while x <= brute_limit:
            attr = get_rand(x, char_num_list)
            fuzz(tag, " " + attr)

           for d1 in delimiters:
                for d2 in delimiters:
                    for boundary in boundaries:
                        val = get_rand(boundary, char_num_list)
                        fuzz(tag, " " + attr, '=', d1, val, d2)

            x += brute_step
            if x <= brute_limit: redirect(i, x)

        x = 0
        i += brute_step
        if i <= brute_limit: redirect(i, x)

if dolog: log.close()
