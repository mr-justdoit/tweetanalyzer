#!/usr/bin/python
from __future__ import absolute_import, print_function

import tweepy,json,sys

with open('data.json') as data_file:
        data = json.load(data_file)

query = sys.argv[1]
        
consumer_key=data["consumer"]["key"]
consumer_secret=data["consumer"]["secret"]

access_token=data["token"]["key"]
access_token_secret=data["token"]["secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
print(api.search(q=query))
