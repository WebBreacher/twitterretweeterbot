#!/usr/bin/python
'''
    Author : Micah Hoffman (@WebBreacher)
    Description : Bot that retweets realDonaldTrump if tweet sent from Android (his phone) and not his staff. 
                  I hope the bot helps people see the real Donald not his staffers.
    Tied to the https://twitter.com/IsItTrump Twitter account

    todo -
        1 - check for errors on tweepy tweeting
        2 - output errors to file for review
        3 - figure out method to ensure that the lasttweet file doesn't get destroyed.
'''

# Import Libraries
import os
import subprocess
import re
import tweepy
from creds import *

# Functions
# Pulled from Peepingtom (https://bitbucket.org/LaNMaSteR53/peepingtom/src/)
# Tim Tomes in no way supports or has anything to do with this project
def runCommand(cmd):
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    stdout, stderr = proc.communicate()
    response = ''
    if stdout: response += str(stdout)
    if stderr: response += str(stderr)
    return proc.returncode, response.strip()

# Pulled from Peepingtom (https://bitbucket.org/LaNMaSteR53/peepingtom/src/)
def getPic(url):
    cmd = '/home/ubuntu/tools/trumpdroidretweeter/phantomjs --ssl-protocol=any --ignore-ssl-errors=yes /home/ubuntu/tools/trumpdroidretweeter/capture.js "%s" /tmp/trump_temp.png 1000' % url
    returncode, response = runCommand(cmd)
    print returncode, response
    return returncode

# Set up temp file for most recent tweet id
tweetHistoryFile = open('/home/ubuntu/tools/trumpdroidretweeter/trumpbot_lasttweet', 'r+')
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
info = api.user_timeline('realdonaldtrump', since_id=last_tweet)

# Cycle through each tweet retrieved and look for the source to be Android
for item in info:
    # Strip off the beginning from the 'source'
    source = item.source.replace('Twitter for ', '')
    source = source.replace('Twitter ', '')
    if re.search('android', source, re.I):
        # If the tweet was sent via Android, it most likely is Trump
        tweet_text = 'Trump via %s: https://twitter.com/realdonaldtrump/status/%d' % (source, item.id)
    else:
        # If the tweet was sent with a different client, it is most likely his staff
        tweet_text = 'NOT Trump via %s: https://twitter.com/realdonaldtrump/status/%d' % (source, item.id)

    # Create a pic of the Twitter page
    url = 'https://twitter.com/realdonaldtrump/status/' + str(item.id)
    pic = getPic(url)

    # Send the tweet
    api.update_with_media('/tmp/trump_temp.png', tweet_text)
    
    # Remove the old pic of the tweet
    runCommand('rm /tmp/trump_temp.png')
    
    # Reset the last_tweet to be the more recent one
    if int(last_tweet) < int(item.id):
        last_tweet = item.id

# Reset the position in the last_tweet file to be at the beginning
position = tweetHistoryFile.seek(0, 0);
tweetHistoryFile.write(str(last_tweet))
tweetHistoryFile.close()
