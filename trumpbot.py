#!/usr/bin/python
'''
    Author : Micah Hoffman (@WebBreacher)
    Description : Trump Retweeting Bot that retweets Android-sourced tweets.

    todo -
        1 - check for errors on tweepy tweeting
        2 - output errors to file for review
        3 - figure out method to ensure that the /tmp/file doesn't get destroyed.
'''

# Import Libraries
import os
import subprocess
import re
import tweepy
from creds import *

# Variables
long_name = 'Donald Trump'
twitter_account = 'realdonaldtrump'
temp_file = '/tmp/trump_temp.png'
tweet_hist_file = '/tmp/trump_lasttweet'


# Functions
# Pulled from Peepingtom (https://bitbucket.org/LaNMaSteR53/peepingtom/src/)
def runCommand(cmd):
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    stdout, stderr = proc.communicate()
    response = ''
    if stdout: response += str(stdout)
    if stderr: response += str(stderr)
    return proc.returncode, response.strip()

def getPic(url):
    cmd = './phantomjs --ssl-protocol=any --ignore-ssl-errors=yes ./capture.js "%s" %s 1000' % (url, temp_file)
    returncode, response = runCommand(cmd)
    print returncode, response
    return returncode


# Set up temp file for most recent tweet id
tweetHistoryFile = open(tweet_hist_file, 'r+')
try:
    last_tweet = tweetHistoryFile.read()
    if last_tweet is None:
        # The tweet history file was empty or invalid
        last_tweet = 5555555555
except:
    print 'Error with last_tweet file'

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Grab the tweets that are more recent than the last one in the last_tweet file
info = api.user_timeline(twitter_account, since_id=last_tweet)

# Cycle through each tweet retrieved and look for the source to be Android
for item in info:
    source = item.source.replace('Twitter for ', '')
    source = source.replace('Twitter ', '')
    tweet_text = "A pic of %s's tweet or retweet: https://twitter.com/%s/status/%d" % (long_name, twitter_account, item.id)

    # Create a pic of the Twitter page
    url = 'https://twitter.com/' + twitter_account + '/status/' + str(item.id)
    pic = getPic(url)

    # Send the tweet
    api.update_with_media(temp_file, tweet_text)
    runCommand('rm %s' % temp_file)

    # Reset the last_tweet to be the more recent one
    if int(last_tweet) < int(item.id):
        last_tweet = item.id

# Reset the position in the last_tweet file to be at the beginning
position = tweetHistoryFile.seek(0, 0);
tweetHistoryFile.write(str(last_tweet))
tweetHistoryFile.close()
