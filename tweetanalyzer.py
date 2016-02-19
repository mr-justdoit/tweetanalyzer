#!/usr/bin/python
# coding: utf-8
from __future__ import absolute_import, print_function
from janome.tokenizer import Tokenizer
from itertools import groupby
import tweepy, json, sys, re, yaml, getopt, pprint, nltk, codecs, pyaml

with open('data.json') as data_file:
    data = json.load(data_file)


def twitter_auth(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)
    return auth

def load_api(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = twitter_auth(consumer_key, consumer_secret, access_token, access_token_secret)
    return tweepy.API(auth, parser=tweepy.parsers.JSONParser())


def filter(text):
    text = re.sub(r'[a-zA-Z0-9¥"¥.¥,¥@]+', '', text)
    text = re.sub(r'[!"“#$%&()\*\+\-\.,\/:;<=>?@\[\\\]^_`{|}~]', '', text)
    text = re.sub(r'[\n|\r|\t]', '', text)
    
    jp_chartype_tokenizer = nltk.RegexpTokenizer(u'([ぁ-んー]+|[ァ-ンー]+|[\u4e00-\u9FFF]+|[ぁ-んァ-ンー\u4e00-\u9FFF]+)')
    text = "".join(jp_chartype_tokenizer.tokenize(text))
    return text


def text_on_tweet(api, query, count, page, lang):
    results = api.search(q=query, count=count, lang=lang)
    textdata = ""
    max_id = 0
    for j in range(0, page):
        for i in range(0, len(results["statuses"])):
            textdata += results["statuses"][i]["text"]
            textdata += ' '
            max_id = results["statuses"][i]["id"]
        results = api.search(q=query, count=count, lang=lang, max_id=max_id-1)
    return textdata

def text_to_array(textdata):
    #textdata = re.sub(r'https?:\/\/.*[\r\n]*', '', textdata, flags=re.MULTILINE)
    textdata = sorted(textdata.split())
    return textdata

def count_words(words):
    keys = [key for key, group in groupby(words)]
    values = [len(list(group)) for key, group in groupby(words)]
    return dict(zip(keys, values))

def output_ja_text(api, query, count, page):
    textdata = filter(text_on_tweet(api, query, count, page, lang="ja"))
    t = Tokenizer()
    tokens = t.tokenize(textdata)
    words = sorted([token.surface for token in tokens])
    dictionary = count_words(words)
    return pyaml.dump(dictionary, sys.stdout, vspacing=[0, 1])
    
def output_textdata(api, query, count, page):
    textdata = text_on_tweet(api, query, count, page, lang="en")
    words = text_to_array(textdata)
    dictionary = count_words(words)
    return pyaml.dump(dictionary, sys.stdout, vspacing=[0, 1])

    
def output_media(api, query, count, page):
    results = api.search(q=query, count=count)
    media = ""
    max_id = 0
    for k in range(0, page):
        for i in range(0, len(results["statuses"])):
            if "media" in results["statuses"][i]["entities"]:
                for j in range(0, len(results["statuses"][i]["entities"]["media"])):
                    media += results["statuses"][i]["entities"]["media"][j]["media_url_https"]
                    media += "\n"
            max_id = results["statuses"][i]["id"]
        results = api.search(q=query, count=count, max_id=max_id-1)
    return media
    
def output_raw(api, query, count):
    return pyaml.dump(api.search(q=query, count=count), sys.stdout, vspacing=[0, 1])


def output_simplify(api, query, count, page):
    results = api.search(q=query, count=count)
    tweets = []
    for j in range(0, page):
        for i in range(0, len(results["statuses"])):
            who   = results["statuses"][i]["user"]["screen_name"]
            what  = results["statuses"][i]["text"]
            where = results["statuses"][i]["geo"]
            when  = results["statuses"][i]["created_at"]
            tweets.append({"who":who, "what":what, "where":where, "when":when})
            max_id = results["statuses"][i]["id"]
        results = api.search(q=query, count=count, max_id=max_id-1)
    return pyaml.dump(tweets, sys.stdout, vspacing=[0,1])


def output_data(api, query, count, page, metatype):
    d = ""
    if metatype == "t":
        d = output_textdata(api, query, count, page)
    elif metatype == "r":
        d = output_raw(api, query, count)
    elif metatype == "m":
        d = output_media(api, query, count, page)
    elif metatype == "j":
        d = output_ja_text(api, query, count, page)
    elif metatype == "s":
        d = output_simplify(api, query, count, page)

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
    
    api = load_api(data["consumer"]["key"], data["consumer"]["secret"], data["token"]["key"], data["token"]["secret"])

    print(u"%s" % output_data(api, query, count, page, metatype))

if __name__ == "__main__":
    main()
