#!/usr/bin/python
'''
    Author : Micah Hoffman (@WebBreacher)
    Description : Trump Retweeting Bot that retweets Android-sourced tweets.
'''

# Import Libraries
import re
import tweepy
from creds import *

# Set up temp file for most recent tweet id
tweetHistoryFile = open('/tmp/trumpbot_lasttweet', 'r+')
last_tweet = tweetHistoryFile.read()
if last_tweet is None:
    # The tweet history file was empty or invalid
    last_tweet = 5555555555

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Grab the tweets that are more recent than the last one in the last_tweet file
info = api.user_timeline('realdonaldtrump', since_id=last_tweet)

# Cycle through each tweet retrieved and look for the source to be Android
for item in info:
    if re.search('android', item.source, re.I):
        tweet_text = 'Trump/%s RT:  https://twitter.com/realdonaldtrump/status/%d' % (item.source, item.id)
    else:
        tweet_text = 'NOT Trump/%s RT:  https://twitter.com/realdonaldtrump/status/%d' % (item.source, item.id)
    
    # Send the tweet
    api.update_status(status=tweet_text)

    # Reset the last_tweet to be the more recent one
    if int(last_tweet) < int(item.id):
        last_tweet = item.id

# Reset the position in the last_tweet file to be at the beginning
position = tweetHistoryFile.seek(0, 0);
tweetHistoryFile.write(str(last_tweet))
tweetHistoryFile.close()
