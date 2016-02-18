#!/usr/bin/python
from __future__ import absolute_import, print_function
from janome.tokenizer import Tokenizer
from itertools import groupby
import tweepy, json, sys, re, yaml, getopt, pprint, nltk

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
    """
    :param text: str
    :rtype : str
    """
    text = re.sub(r'[a-zA-Z0-9¥"¥.¥,¥@]+', '', text)
    text = re.sub(r'[!"“#$%&()\*\+\-\.,\/:;<=>?@\[\\\]^_`{|}~]', '', text)
    text = re.sub(r'[\n|\r|\t]', '', text)
    
    jp_chartype_tokenizer = nltk.RegexpTokenizer(u'([ぁ-んー]+|[ァ-ンー]+|[\u4e00-\u9FFF]+|[ぁ-んァ-ンー\u4e00-\u9FFF]+)')
    text = "".join(jp_chartype_tokenizer.tokenize(text))
    return text


def text_on_tweet(api, query, count, lang):
    results = api.search(q=query, count=count, lang=lang)
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

def output_ja_text(api, query, count):
    textdata = filter(text_on_tweet(api, query, count, lang="ja"))
    t = Tokenizer()
    tokens = t.tokenize(textdata)
    words = [token.surface for token in tokens]
    dictionary = count_words(words)
    return "\n".join("\"%s\": %d" % i for i in dictionary.items())
    
def output_textdata(api, query, count):
    textdata = text_on_tweet(api, query, count, lang="en")
    words = text_to_array(textdata)
    dictionary = count_words(words)
    return yaml.dump(dictionary,default_flow_style=False)

    
def output_media(api, query, count):
    results = api.search(q=query, count=count)
    media = ""
    for i in range(0, len(results["statuses"])):
        if "media" in results["statuses"][i]["entities"]:
            for j in range(0, len(results["statuses"][i]["entities"]["media"])):
                media += results["statuses"][i]["entities"]["media"][j]["media_url_https"]
                media += "\n"
    return media
    
def output_raw(api, query, count):
    return api.search(q=query, count=count)

def output_data(api, query, count, metatype):
    d = ""
    if metatype == "t":
        d = output_textdata(api, query, count)
    elif metatype == "r":
        d = output_raw(api, query, count)
    elif metatype == "m":
        d = output_media(api, query, count)
    elif metatype == "j":
        d = output_ja_text(api, query, count)

    return d

#t = Tokenizer()
#tokens = t.tokenize(textdata)

    
def main():

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
            
    consumer_key=data["consumer"]["key"]
    consumer_secret=data["consumer"]["secret"]

    access_token=data["token"]["key"]
    access_token_secret=data["token"]["secret"]
    
    api = load_api(consumer_key, consumer_secret, access_token, access_token_secret)

    print(output_data(api, query, count, metatype))

if __name__ == "__main__":
    main()
