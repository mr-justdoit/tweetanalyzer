from __future__ import absolute_import, print_function

import tweepy,json

with open('data.json') as data_file:
        data = json.load(data_file)

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key=data["consumer"]["key"]
consumer_secret=data["consumer"]["secret"]

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token=data["token"]["key"]
access_token_secret=data["token"]["secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
print(api.me().name)
