#!/usr/bin/python
from __future__ import absolute_import, print_function
from janome.tokenizer import Tokenizer
from itertools import groupby
import tweepy, json, sys, re, yaml, getopt

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

def text_on_tweet(api, query, count="100"):
    results = api.search(q=query, count=count, lang="en")
    textdata = ""
    for i in range(0, len(results["statuses"])):
        textdata += results["statuses"][i]["text"]
        textdata += ' '
    return textdata

def text_to_array(textdata):
    #textdata = re.sub(r'https?:\/\/.*[\r\n]*', '', textdata, flags=re.MULTILINE)
    textdata = sorted(textdata.split())
    return textdata

def count_words(words):
    keys = [key for key, group in groupby(words)]
    values = [len(list(group)) for key, group in groupby(words)]
    return dict(zip(keys, values))

def output_textdata(api, query, count):
    textdata = text_on_tweet(api, query, count)
    words = text_to_array(textdata)
    dictionary = count_words(words)
    print(yaml.dump(dictionary,default_flow_style=False))

def output_media(api, query, count):
    results = api.search(q=query, count=count)
    media = ""
    for i in range(0, len(results["statuses"])):
        if "media" in results["statuses"][i]["entities"]:
            for j in range(0, len(results["statuses"][i]["entities"]["media"])):
                media += results["statuses"][i]["entities"]["media"][j]["media_url_https"]
                media += "\n"
    print(media)
    
def output_raw(api, query, count="100"):
    print(api.search(q=query, count=count, lang="en"))

def output_data(api, query, count, metatype):
    if metatype == "t":
        output_textdata(api, query, count)
    elif metatype == "r":
        output_raw(api, query, count)
    elif metatype == "m":
        output_media(api, query, count)


#t = Tokenizer()
#tokens = t.tokenize(textdata)

    
def main():
    consumer_key=data["consumer"]["key"]
    consumer_secret=data["consumer"]["secret"]
    
    access_token=data["token"]["key"]
    access_token_secret=data["token"]["secret"]
    
    api = load_api(consumer_key, consumer_secret, access_token, access_token_secret)

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'q:t:c:h')
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
        
    #print(opts)
    query = ""
    metatype = 't'
    count = 100

    for o, a in opts:
        if o == "-q":
            query = a
        elif o == "-t":
            metatype = a
        elif o == "-c":
            count = a

    output_data(api, query, count, metatype)

if __name__ == "__main__":
    main()
