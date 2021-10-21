import os
import webbrowser

import tweepy
from dotenv import load_dotenv


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


def generate_api_v1(OAuth=1) -> tweepy.API:
    """Twitter API v1を生成

    Args:
        OAuth (int): 1: OAuth 1a
                     2: OAuth 2

    Returns:
        API: Twitter API
    """

    load_dotenv()
    CONSUMER_KEY = os.environ.get("TW_KEY")
    CONSUMER_SECRET = os.environ.get("TW_KEY_SEC")

    if OAuth == 1:
        ACCESS_TOKEN_KEY = os.environ.get("TW_ACC_TOKEN")
        ACCESS_TOKEN_SECRET = os.environ.get("TW_ACC_TOKEN_SEC")

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    elif OAuth == 2:
        auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


def generate_api_v2(OAuth=1) -> tweepy.Client:
    """Twitter API v2を生成

    Args:
        OAuth (int): 1: OAuth 1a
                     2: OAuth 2

    Returns:
        tweepy.Client: Twitter API v2
    """

    load_dotenv()
    CONSUMER_KEY = os.environ.get("TW_KEY")
    CONSUMER_SECRET = os.environ.get("TW_KEY_SEC")

    if OAuth == 1:
        ACCESS_TOKEN_KEY = os.environ.get("TW_ACC_TOKEN")
        ACCESS_TOKEN_SECRET = os.environ.get("TW_ACC_TOKEN_SEC")
        client = tweepy.Client(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_TOKEN_KEY,
            access_token_secret=ACCESS_TOKEN_SECRET,
            wait_on_rate_limit=True,
        )
    elif OAuth == 2:
        BEARER_TOKEN = os.environ.get("TW_BEARER_TOKEN")
        client = tweepy.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            wait_on_rate_limit=True,
        )

    return client


def enum_token() -> dict:
    """Twitter APIのアクセストークンを辞書で出力する

    Returns:
        dict: Twitter APIのアクセストークン

    Examples:
        tokens = enum_token()
        stream = Stream(
            tokens["CONSUMER_KEY"],
            tokens["CONSUMER_SECRET"],
            tokens["ACCESS_TOKEN"],
            tokens["ACCESS_TOKEN_SECRET"],
        )
    """

    load_dotenv()
    tokens = {
        "CONSUMER_KEY": os.environ.get("TW_KEY"),
        "CONSUMER_SECRET": os.environ.get("TW_KEY_SEC"),
        "ACCESS_TOKEN": os.environ.get("TW_ACC_TOKEN"),
        "ACCESS_TOKEN_SECRET": os.environ.get("TW_ACC_TOKEN_SEC"),
    }
    return tokens
