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
    source = item.source.replace('Twitter for ', '')
    source = source.replace('Twitter ', '')
    tweet_split = item.text.split()
    first_words = '%s %s %s %s...' % (tweet_split[0], tweet_split[1], tweet_split[2], tweet_split[3])
    last_words = '%s %s %s %s' % (tweet_split[-4], tweet_split[-3], tweet_split[-2], tweet_split[-1])
    if re.search('android', source, re.I):
        # If the tweet was sent via Android, most likely is Trump
        tweet_text = 'Trump via %s: "%s%s" https://twitter.com/realdonaldtrump/status/%d' % (source, first_words, last_words, item.id)
        # Check for > 140 chars
        if len(tweet_text) > 139:
            tweet_text = 'Trump via %s: "%s %s...%s %s" https://twitter.com/realdonaldtrump/status/%d' % (source, tweet_split[0], tweet_split[1], tweet_split[-2], tweet_split[-1], item.id)
    else:
        # If the tweet was sent with a different client, it is most likely his staff
        tweet_text = 'NOT Trump via %s: "%s%s" https://twitter.com/realdonaldtrump/status/%d' % (source, first_words, last_words, item.id)
        # Check for > 140 chars
        if len(tweet_text) > 139:
            tweet_text = 'NOT Trump via %s: "%s %s...%s %s" https://twitter.com/realdonaldtrump/status/%d' % (source, tweet_split[0], tweet_split[1], tweet_split[-2], tweet_split[-1], item.id)
    
    # Send the tweet
    api.update_status(status=tweet_text)

    # Reset the last_tweet to be the more recent one
    if int(last_tweet) < int(item.id):
        last_tweet = item.id

# Reset the position in the last_tweet file to be at the beginning
position = tweetHistoryFile.seek(0, 0);
tweetHistoryFile.write(str(last_tweet))
tweetHistoryFile.close()
