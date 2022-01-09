import os
import time
import datetime
import tweepy
import logic.config

from os import path
from credentials import *
from logic.screenshotter import Screenshotter


username = logic.config.get_config('twitterhandle')
seleniumurl = logic.config.get_config('seleniumurl')
interval = int(logic.config.get_config('checkinterval'))
consumer_key = logic.config.get_config('consumer_key')
consumer_secret = logic.config.get_config('consumer_secret')
access_token = logic.config.get_config('access_token')
access_token_secret = logic.config.get_config('access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def get_last_id(username) -> int:
    n = f"data/{username}/last_id_file.dat"
    if not os.path.isfile(n):
        set_last_id(username, 1)

    with open(n, 'r') as f:
        val = f.readline()
        f.close()
        
        return int(val)


def set_last_id(username, id) -> None:
    n = f"data/{username}/last_id_file.dat"
    with open(n, 'w') as f:
        f.write(str(id))
        f.close()
    print(f"Saving id {id}")

def run():
    if not path.isdir(f"data/{username}"):
        os.makedirs(f"data/{username}")

    since_id = get_last_id(username)

    tweets = api.user_timeline(screen_name=username,
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts=False,
                            # Necessary to keep full_text
                            # otherwise only the first 140 words are extracted
                            #tweet_mode='extended',
                            since_id=since_id
                            )

    shotter = Screenshotter()
    shotter.init_driver(seleniumurl)
    
    tweets.reverse()
    for tweet in tweets:
        try:
            print(f"New tweet found: https://twitter.com/{tweet.author.screen_name}/status/{tweet.id}", flush=True)
            loc = shotter.screenshot(tweet)
            try:
                post_screenshot(tweet, loc)
            except:
                print(f"Error posting screenshot", flush=True)

            set_last_id(username, tweet.id)

        except:
            print(f"Error screenshotting", flush=True)

    if len(tweets) > 0:
        print(f"Finished posting all new tweets of {username}", flush=True)
    else:
        print(f"No new tweets for {username}", flush=True)

def post_screenshot(original_tweet, screenshot_path):
    media = api.media_upload(screenshot_path)
    tweet = api.update_status("", media_ids=[media.media_id], attachment_url=f"https://twitter.com/{original_tweet.author.screen_name}/status/{original_tweet.id}" )
    print(f"Posted tweet screendump: https://twitter.com/{tweet.author.screen_name}/status/{tweet.id_str}", flush=True)

if __name__ == '__main__':
    print("""
   _____ _     _ _     _______       _ _   _               _____                 
  / ____| |   (_) |   |__   __|     (_) | | |             / ____|                
 | (___ | |__  _| |_     | |_      ___| |_| |_ ___ _ __  | (___   __ _ _   _ ___ 
  \___ \| '_ \| | __|    | \ \ /\ / / | __| __/ _ \ '__|  \___ \ / _` | | | / __|
  ____) | | | | | |_     | |\ V  V /| | |_| ||  __/ |     ____) | (_| | |_| \__ \\
 |_____/|_| |_|_|\__|    |_| \_/\_/ |_|\__|\__\___|_|    |_____/ \__,_|\__, |___/
                                                                        __/ |    
                                                                       |___/     
    """, flush=True)
    while True:
        run()
        next_check = datetime.datetime.now() + datetime.timedelta(0, interval)
        print(
            f"Sleeping for {interval} seconds. Next check at {next_check.strftime('%H:%M:%S')}", flush=True)
        time.sleep(interval)
