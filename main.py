from os import path
import tweepy
import logic.config

from credentials import *
from logic.screenshotter import Screenshotter


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


def run():
    username = logic.config.get_config('twitterhandle')
    seleniumurl = logic.config.get_config('seleniumurl')
    consumer_key = logic.config.get_config('consumer_key')
    consumer_secret = logic.config.get_config('consumer_secret')
    access_token = logic.config.get_config('access_token')
    access_token_secret = logic.config.get_config('access_token_secret')

    if not path.isdir(f"data/{username}"):
        os.makedirs(f"data/{username}")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

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
        print("ID: {}".format(tweet.id))
        print(tweet.created_at)
        print(tweet.text)
        print("\n")

        #loc = shotter.screenshot(info.author.screen_name, info.id)
        loc = shotter.screenshot(tweet)
        print(f"Saved at {loc}", flush=True)

    if len(tweets) > 0:
        set_last_id(username, tweets[0].id)
    else:
        print(f"No new tweets for {username}")

if __name__ == '__main__':
    run()
    #test()