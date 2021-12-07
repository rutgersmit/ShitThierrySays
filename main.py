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

def test():
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

    # reply on retweet with video
    print('reply on retweet with video')
    tweet = api.get_status(1454912491406905358)
    l = shotter.screenshot(tweet)
    os.rename(l, "tests/reply_on_retweet_with_video.png")



if __name__ == '__main__':
    run()
    #test()