# trumpdroidretweeter
Python code to take a screenshot of the tweet or retweet made by realDonaldTrump or someone else and then it tweets out the pic with a link to the original tweet.

# Blog With More Details
Visit my blog at https://webbreacher.com/2016/12/07/trump-twitter-bot/ for more information about this bot

# Features
- Takes a pic of the target's Twitter status so that you have a copy of it even if they delete the original
- Can be used on public Twitter user by changing the Variables at the top of the Python file

# Requirements
- Requires phantomjs binary in the same dir as the script (unless you alter the script)
- Requires capture.js in the same dir as the script (unless you alter the script)
- Create the temp file (by default /tmp/trump_lasttweet) and put in there a number for the tweet you want to start at.
    - To get this number, visit the Twitter profile of your target (such as https://twitter.com/realDonaldTrump/)
    - Find a tweet you'd like to start at and press the date link for when it was tweeted
    - That should bring up a URL that looks like https://twitter.com/realDonaldTrump/status/883064346519187456
    - The number at the end of the URL (the whole number) needs to go into the temp file

# Thanks
Big thanks to lanmaster53 (Tim Tomes) for use of Peepingtom code
Also thanks to Mubix (Rob Fuller) for suggesting screenshotting content.
