import os
import webbrowser

import tweepy
from dotenv import load_dotenv

"""
.env
  TW_KEY=<consumer key>
  TW_KEY_SEC=<consumer key_secret>
  TW_ACC_TOKEN=<access token>
  TW_ACC_TOKEN_SEC=<access token_secret>
"""


def create_token():
    """Twitter APIのアクセストークンを生成し，.envに保存する"""

    load_dotenv()

    CONSUMER_KEY = os.environ.get("TW_KEY")
    CONSUMER_SECRET = os.environ.get("TW_KEY_SEC")

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print("Error! Failed to get request token.")

    print(redirect_url)
    webbrowser.open(redirect_url)

    verifier = input("input verifier:")

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print("Error! Failed to get access token.")

    with open(".env", "a") as f:
        f.write("\n" + "TW_ACC_TOKEN=" + str(auth.access_token) + "\n")
        f.write("TW_ACC_TOKEN_SEC=" + str(auth.access_token_secret))


def generate_api():
    """Twitter APIを生成

    Returns:
        API: Twitter API
    """
    load_dotenv()

    CONSUMER_KEY = os.environ.get("TW_KEY")
    CONSUMER_SECRET = os.environ.get("TW_KEY_SEC")
    ACCESS_TOKEN_KEY = os.environ.get("TW_ACC_TOKEN")
    ACCESS_TOKEN_SECRET = os.environ.get("TW_ACC_TOKEN_SEC")

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api
