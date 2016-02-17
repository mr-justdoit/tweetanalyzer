#!/usr/bin/python
from __future__ import absolute_import, print_function
from janome.tokenizer import Tokenizer
from itertools import groupby
import tweepy, json, sys, re

with open('data.json') as data_file:
    data = json.load(data_file)

query = sys.argv[1]
        
consumer_key=data["consumer"]["key"]
consumer_secret=data["consumer"]["secret"]

access_token=data["token"]["key"]
access_token_secret=data["token"]["secret"]

def twitterAuth(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)
    return auth

def getAPI(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = twitterAuth(consumer_key, consumer_secret, access_token, access_token_secret)
    return tweepy.API(auth, parser=tweepy.parsers.JSONParser())

def getTextsOnTweets(api):
    results = api.search(q=query,rpp=100)
    textdata = ""

    for i in range(0, len(results["statuses"])):
        textdata += results["statuses"][i]["text"]

    return textdata

def textdataToArray(textdata):
    textdata = re.sub(r'https?:\/\/.*[\r\n]*', '', textdata, flags=re.MULTILINE)
    textdata = sorted(textdata.split(' '))
    return textdata

def countWords(words):
    keys = [key for key, group in groupby(words)]
    values = [len(list(group)) for key, group in groupby(words)]
    return dict(zip(keys, values))
    
api = getAPI(consumer_key, consumer_secret, access_token, access_token_secret)
textdata = getTextsOnTweets(api)
words = textdataToArray(textdata)
dictionary = countWords(words)

print(dictionary)


#t = Tokenizer()
#tokens = t.tokenize(textdata)

