#!/usr/bin/python
# coding: utf-8
from __future__ import absolute_import, print_function
import tweepy
import json
import sys
import getopt
import pyaml
import textmining

with open('data.json') as data_file:
    data = json.load(data_file)


def twitter_auth(consumer_key, consumer_secret, access_token,
                 access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)
    return auth


def load_api(consumer_key, consumer_secret, access_token, access_token_secret):
    return tweepy.API(
        twitter_auth(consumer_key, consumer_secret, access_token,
                     access_token_secret),
        parser=tweepy.parsers.JSONParser())


def text_on_tweet(api, query, count, page, lang):
    results = api.search(q=query, count=count, lang=lang)
    textdata = ""
    max_id = 0
    for j in range(0, page):
        for i in range(0, len(results["statuses"])):
            d = results["statuses"][i]
            textdata += d["text"]
            textdata += ' '
            max_id = d["id"]
        results = api.search(q=query,
                             count=count,
                             lang=lang,
                             max_id=max_id - 1)
    return textdata


def output_media(api, query, count, page):
    results = api.search(q=query, count=count)
    media = ""
    pid = []
    for k in range(0, page):
        for i in range(0, len(results["statuses"])):
            d = results["statuses"][i]
            if "media" in d["entities"]:
                for j in range(0, len(d["entities"]["media"])):
                    media += d["entities"]["media"][j]["media_url_https"]
                    media += "\n"
            pid.append(d["id"])
        results = api.search(q=query, count=count, max_id=pid.pop() - 1)
    return print(media)


def output_url(api, query, count, page):
    results = api.search(q=query, count=count)
    url = ""
    pid = []
    for k in range(0, page):
        for i in range(0, len(results["statuses"])):
            d = results["statuses"][i]
            if "urls" in d["entities"]:
                for j in range(0, len(d["entities"]["urls"])):
                    url += d["entities"]["urls"][j]["expanded_url"]
                    url += "\n"
            pid.append(d["id"])
        results = api.search(q=query, count=count, max_id=pid.pop() - 1)
    return print(url)


def output_raw(api, query, count):
    return pyaml.dump(
        api.search(q=query,
                   count=count),
        sys.stdout,
        vspacing=[0, 1])


def output_simplify(api, query, count, page):
    results = api.search(q=query, count=count)
    tweets = []
    d = ""
    for j in range(0, page):
        if len(results["statuses"]) == 0:
            return
        for i in range(0, len(results["statuses"])):
            d = results["statuses"][i]
            tweets.append({"id": d["id"],
                           "user": d["user"]["screen_name"],
                           "text": d["text"],
                           "geo": d["geo"],
                           "time": d["created_at"],
                           "lang": d["lang"]})
        results = api.search(q=query, count=count, max_id=d["id"] - 1)
    return pyaml.dump(tweets, sys.stdout, vspacing=[0, 1])


def output_data(api, query, count, page, metatype):
    d = ""
    if metatype == "t":
        textdata = text_on_tweet(api, query, count, page, lang="en")
        d = textmining.output_textdata(textdata)
    elif metatype == "r":
        d = output_raw(api, query, count)
    elif metatype == "m":
        d = output_media(api, query, count, page)
    elif metatype == "j":
        textdata = text_on_tweet(api, query, count, page, lang="ja")
        d = textmining.output_ja_text(textdata, ["名詞"])
    elif metatype == "s":
        d = output_simplify(api, query, count, page)
    elif metatype == "u":
        d = output_url(api, query, count, page)

    return d


def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'q:t:c:p:h')
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    query = ""
    metatype = 't'
    count = 1
    page = 1

    for o, a in opts:
        if o == "-q":
            query = a
        elif o == "-t":
            metatype = a
        elif o == "-c":
            count = int(a)
        elif o == "-p":
            page = int(a)

    api = load_api(data["consumer"]["key"], data["consumer"]["secret"],
                   data["token"]["key"], data["token"]["secret"])

    output_data(api, query, count, page, metatype)


if __name__ == "__main__":
    main()
