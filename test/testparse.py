#!/usr/bin/python
# coding: utf-8
import urllib.request as urllib2
import html2text
import re
import sys
import getopt


def output_time(text, time):
    if time == "h":
        texts = re.findall(r"[0-9][0-9]:[0-9][0-9]:[0-9][0-9]", text)
        for i in range(0, len(texts)):
            texts[i] = texts[i].split(":")[0]
    elif time == "m":
        texts = re.findall(r"[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]", text)
        for i in range(0, len(texts)):
            texts[i] = texts[i].split("/")[1]

    for i in range(0, len(texts)):
        print(texts[i])


def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:t:h')
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    time = "h"
    url = ""
    text = ""

    for o, a in opts:
        if o == "-u":
            url = a
            html = str(urllib2.urlopen(url).read())

            h = html2text.HTML2Text()
            text = h.handle(html)

        if o == "-t":
            time = a
            output_time(text, time)


if __name__ == "__main__":
    main()
