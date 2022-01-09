from os import path
import tweepy
import logic.config

from credentials import *
from logic.screenshotter import Screenshotter


seleniumurl = logic.config.get_config('seleniumurl')
consumer_key = logic.config.get_config('consumer_key')
consumer_secret = logic.config.get_config('consumer_secret')
access_token = logic.config.get_config('access_token')
access_token_secret = logic.config.get_config('access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

shotter = Screenshotter()
shotter.init_driver(seleniumurl)

if not path.isdir('tests'):
    os.makedirs('tests')

# original tweet without replies
print('original tweet without replies')
tweet = api.get_status(1466505804090122253)
l = shotter.screenshot(tweet)
os.rename(l, "tests/original_tweet_without_replies.png")

# original tweet with replies
print('original tweet with replies')
tweet = api.get_status(1467873464216440842)
l = shotter.screenshot(tweet)
os.rename(l, "tests/original_tweet_with_replies.png")

# reply on deleted tweet
print('reply on deleted tweet')
tweet = api.get_status(1454179653858603010)
l = shotter.screenshot(tweet)
os.rename(l, "tests/reply_on_deleted_tweet.png")

# reply on tweet with image
print('reply on tweet with image')
tweet = api.get_status(1454499417395015691)
l = shotter.screenshot(tweet)
os.rename(l, "tests/reply_on_tweet_with_image.png")

# quoted deleted tweet
print('quoted deleted tweet')
tweet = api.get_status(1448380249998303232)
l = shotter.screenshot(tweet)
os.rename(l, "tests/quoted_deleted_tweet.png")

# reply on retweet with video
print('reply on retweet with video')
tweet = api.get_status(1454912491406905358)
l = shotter.screenshot(tweet)
os.rename(l, "tests/reply_on_retweet_with_video.png")

print('long thread conversation tweet')
tweet = api.get_status(1462773987407060996)
l = shotter.screenshot(tweet)
os.rename(l, "tests/long_thread_conversation_tweet.png")
