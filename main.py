from os import path
from credentials import *
import tweepy

import secrets

from logic.screenshotter import Screenshotter

last_id_file = 'data/last_id.txt'

def check_paths():
    if not path.isdir('data/screenshots'):
        os.makedirs('data/screenshots')

def get_last_id() -> int:
    if not os.path.isfile(last_id_file):
        set_last_id(1)

    with open(last_id_file, 'r') as f:
        val = f.readline()
        f.close()
        
        return int(val)

def set_last_id(id) -> None:
    with open(last_id_file, 'w') as f:
        f.write(str(id))
        f.close()

def run():
    userID = "thierrybaudet"

    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token, secrets.access_token_secret)
    api = tweepy.API(auth)

    since_id = get_last_id()

    tweets = api.user_timeline(screen_name=userID,
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts=False,
                            # Necessary to keep full_text
                            # otherwise only the first 140 words are extracted
                            #tweet_mode='extended',
                            since_id=since_id
                            )
    shotter = Screenshotter()
    shotter.init_driver()

    for info in tweets:
        print("ID: {}".format(info.id))
        print(info.created_at)
        print(info.text)
        print("\n")

        shotter.screenshot(info.id)

    set_last_id(tweets[0].id)

if __name__ == '__main__':
    run()