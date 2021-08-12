import tweepy
import settings as st

auth = tweepy.OAuthHandler(st.CONSUMER_KEY, st.CONSUMER_SECRET)
auth.set_access_token(st.ACCESS_TOKEN_KEY, st.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def main():
    pass

if __name__ == '__main__':
    main()
